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
    """Live `claude` CLI sessions as (pid, rss_mb, cwd).

    Two backends. psutil, when importable, works identically on macOS, Linux
    and Windows and is the only one of the two that can see native Windows
    processes at all (Git Bash's ps stops at MSYS). Without psutil the original
    ps+lsof path still serves POSIX, and Windows gets a clear message instead
    of a silent empty list, because "no sessions found" and "cannot look" must
    not read the same.
    """
    try:
        import psutil
    except ImportError:
        psutil = None
    if psutil is not None:
        found = []
        for pr in psutil.process_iter(["pid", "name", "cmdline", "memory_info"]):
            try:
                cmd = " ".join(pr.info["cmdline"] or [])
                name = (pr.info["name"] or "").lower()
                if "claude" not in name and "claude" not in cmd:
                    continue
                if ("stream-json" in cmd or "mcp-server" in cmd
                        or "reap_idle" in cmd or "claude-mem" in cmd):
                    continue
                # the CLI itself, not every node child mentioning the word
                if not (name.startswith("claude")
                        or cmd.rstrip().endswith("claude")
                        or " claude " in f" {cmd} "):
                    continue
                found.append((pr.info["pid"],
                              pr.info["memory_info"].rss // (1024*1024),
                              pr.cwd()))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return found
    if sys.platform == "win32":
        log("ABORT: Windows pe psutil chahiye (pip install psutil), warna "
            "native processes dikhte hi nahi")
        return []
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
    # Claude flattens path separators and "_" to "-" when naming the project
    # directory. Rather than hand-maintaining per-OS rules for ":" and "\\",
    # collapse every non-alphanumeric to "-" and, if that exact name is absent,
    # look for a case-insensitive match. A miss returns None, and None is
    # treated as "cannot tell", which never kills anything.
    import re
    slug = re.sub(r"[^A-Za-z0-9]", "-", cwd)
    d = PROJECTS / slug
    if not d.is_dir():
        d = None
        try:
            for cand in PROJECTS.iterdir():
                if cand.name.lower() == slug.lower():
                    d = cand
                    break
        except OSError:
            return None
        if d is None:
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
