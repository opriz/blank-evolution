# OpenClaw Configuration

This directory is for OpenClaw configuration documentation.

## Key Settings

### Stream Output (TUI)

Enable streaming output in TUI:

```bash
openclaw config set agents.defaults.blockStreamingDefault "off"
openclaw gateway restart
```

Disable streaming (block mode):

```bash
openclaw config set agents.defaults.blockStreamingDefault "on"
openclaw gateway restart
```

### Gateway

```bash
# Start gateway
openclaw gateway

# Restart gateway
openclaw gateway restart

# Check status
openclaw status
```

### TUI

```bash
# Start TUI
openclaw tui

# With options
openclaw tui --deliver --thinking medium
```

## Config File Location

`~/.openclaw/openclaw.json`

Note: Do not commit this file to git as it contains sensitive credentials.
