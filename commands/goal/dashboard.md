---
name: goal:dashboard
description: Open the Goal Agent web dashboard in your browser
allowed-tools: [Bash]
---

# /goal:dashboard

Open the Goal Agent web dashboard on localhost.

## What It Does

Starts a local web server that displays your goal progress, content calendar, network, and lets you run all goal commands from a browser UI.

## Execution

Run the dashboard server:

```bash
node "$HOME/.claude/plugins/data/goal-agent@ishaquehassan/dashboard/server.js"
```

Set the working directory to where your goal state files live:

```bash
GOAL_AGENT_WORKDIR="$(pwd)" node "$HOME/.claude/plugins/data/goal-agent@ishaquehassan/dashboard/server.js"
```

The server will:
1. Start on port 8080 (or next available port)
2. Auto-open your browser
3. Show your goal dashboard with live updates

Press Ctrl+C to stop.

## Instructions

1. Use Bash to run the server command above with GOAL_AGENT_WORKDIR set to the current working directory
2. Tell the user the dashboard is running and they can open the URL shown in the output
3. The server runs in foreground, so the user needs to stop it manually with Ctrl+C
