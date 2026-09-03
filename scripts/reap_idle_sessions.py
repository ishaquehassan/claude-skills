#!/usr/bin/env python3
"""
Close Claude Code sessions nobody has spoken to in a while.

Why this exists: sessions opened in terminal tabs are never closed, so they
pile up. Eleven of them were live at once on a 16GB machine, holding 2.7GB
between them and pushing 1.6M pageouts into an almost-full swap file.

The subtle part is deciding what "idle" means. Two obvious signals are both
wrong, and both were measured to be wrong before this was written:

  * Process age. A session that had been running for ten days had a human
    message in it one minute earlier. Age says nothing about use.
  * Transcript file mtime. Every transcript on the machine showed the same
    mtime, to the minute, because something bulk-touched them all (the
    claude-mem plugin walks them). It reports activity that never happened.

What is actually true is the timestamp on the last `"type":"user"` entry
inside the transcript itself, which only moves when a person types. That is
what this reads.

Safety: SIGTERM only, so the session flushes its state and stays resumable
with `claude --continue` in the same directory. Nothing is deleted, ever.
"""

import datetime, json, os, signal, subprocess, sys, time
from pathlib import Path

IDLE_DAYS = float(os.environ.get("CLAUDE_REAP_IDLE_DAYS", "3"))
DRY_RUN = "--dry-run" in sys.argv or os.environ.get("CLAUDE_REAP_DRY") == "1"
PROJECTS = Path.home() / ".claude" / "projects"
LOG = Path.home() / ".claude" / "reap.log"

# Reading the tail is enough and keeps this cheap: transcripts reach 150MB and
# the last human turn is never far from the end.
TAIL_BYTES = 2_000_000


def log(msg):
    line = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}  {msg}"
    print(line)
    try:
        with LOG.open("a") as f:
            f.write(line + "\n")
    except OSError:
        pass


def sessions():
    """Live `claude` CLI sessions as (pid, rss_mb, cwd)."""
    out = subprocess.run(
        ["ps", "-axo", "pid=,rss=,command="], capture_output=True, text=True
    ).stdout
    found = []
    for line in out.splitlines():
        parts = line.split(None, 2)
        if len(parts) < 3:
            continue
        pid, rss, cmd = parts
        # The bare CLI only. Headless `--output-format stream-json` children are
        # spawned by plugins and manage their own lifetime.
        if "claude " not in cmd and not cmd.rstrip().endswith("claude"):
            continue
        if "stream-json" in cmd or "mcp-server" in cmd or "reap_idle" in cmd:
            continue
        try:
            pid = int(pid)
        except ValueError:
            continue
        cwd = ""
        try:
            r = subprocess.run(
                ["lsof", "-a", "-p", str(pid), "-d", "cwd", "-Fn"],
                capture_output=True, text=True, timeout=10,
            ).stdout
            for l in r.splitlines():
                if l.startswith("n"):
                    cwd = l[1:]
                    break
        except (subprocess.SubprocessError, OSError):
            pass
        found.append((pid, int(rss) // 1024, cwd))
    return found


def last_human_turn(cwd):
    """Epoch seconds of the last message a person typed, or None."""
    if not cwd:
        return None
    # Claude flattens both "/" and "_" to "-" when naming the project directory.
    slug = cwd.replace("/", "-").replace("_", "-")
    d = PROJECTS / slug
    if not d.is_dir():
        return None
    newest = None
    for f in d.glob("*.jsonl"):
        try:
            size = f.stat().st_size
            with f.open("rb") as fh:
                if size > TAIL_BYTES:
                    fh.seek(size - TAIL_BYTES)
                    fh.readline()          # drop the partial line
                data = fh.read().decode("utf-8", "ignore")
        except OSError:
            continue
        for line in reversed(data.splitlines()):
            try:
                o = json.loads(line)
            except ValueError:
                continue
            if o.get("type") == "user" and o.get("timestamp"):
                try:
                    t = datetime.datetime.fromisoformat(
                        o["timestamp"].replace("Z", "+00:00")
                    ).timestamp()
                except ValueError:
                    continue
                if newest is None or t > newest:
                    newest = t
                break
    return newest


def main():
    now = time.time()
    cutoff = IDLE_DAYS * 86400
    reaped = freed = 0

    for pid, rss, cwd in sessions():
        last = last_human_turn(cwd)
        name = os.path.basename(cwd) or "?"

        # No readable transcript means no evidence of idleness. Leave it alone;
        # a false positive here kills someone's live work.
        if last is None:
            log(f"skip  pid={pid} {name}: koi transcript nahi, chhor raha hoon")
            continue

        idle_h = (now - last) / 3600
        if idle_h * 3600 < cutoff:
            log(f"keep  pid={pid} {rss}MB {name}: {idle_h:.1f}h pehle baat hui")
            continue

        if DRY_RUN:
            log(f"WOULD REAP pid={pid} {rss}MB {name}: {idle_h/24:.1f} din khamosh")
            continue

        try:
            os.kill(pid, signal.SIGTERM)
            reaped += 1
            freed += rss
            log(f"REAP  pid={pid} {rss}MB {name}: {idle_h/24:.1f} din khamosh, "
                f"wapas: cd {cwd} && claude --continue")
        except (ProcessLookupError, PermissionError) as e:
            log(f"fail  pid={pid} {name}: {e}")

    log(f"done. {reaped} band kiye, ~{freed}MB, cutoff {IDLE_DAYS} din"
        + ("  [DRY RUN]" if DRY_RUN else ""))


if __name__ == "__main__":
    main()
