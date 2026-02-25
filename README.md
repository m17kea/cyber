# Kali Linux MCP via Docker MCP Toolkit + Codex

This repository now contains a **Kali Linux MCP server** that runs in a Docker container, is registered with the **Docker MCP Toolkit**, and is connected to **Codex**.

## What was set up

1. A custom MCP server implemented in Python (`FastMCP`) that runs inside a Kali Linux container.
2. A Docker image for that server: `cyber-kali-mcp:latest`.
3. A Docker MCP Toolkit catalog entry (`kali-linux`) that points to that image.
4. Docker MCP Toolkit server enablement for `kali-linux`.
5. Codex global MCP client linkage to Docker MCP (`MCP_DOCKER`).

## Files added

- `kali-mcp/kali_mcp_server.py`
- `kali-mcp/Dockerfile`
- `docker-mcp-kali-catalog.yaml`

## Prerequisites

- Docker Desktop with `docker mcp` CLI available.
- Codex CLI installed.
- Ability to run Docker containers locally.

## Exact steps performed

### 1) Build the Kali MCP image

```bash
docker build -t cyber-kali-mcp:latest -f kali-mcp/Dockerfile kali-mcp
```

### 2) Import the custom catalog into Docker MCP Toolkit

```bash
docker mcp catalog import ./docker-mcp-kali-catalog.yaml
```

### 3) Enable the Kali MCP server

```bash
docker mcp server enable kali-linux
```

### 4) Verify Docker MCP server registration

```bash
docker mcp server ls
docker mcp catalog ls
```

Expected key result: `kali-linux` appears in enabled servers.

### 5) Validate gateway startup and tool discovery

```bash
docker mcp gateway run --dry-run --servers kali-linux --verbose
```

Expected key result: it lists `kali-linux` and reports `3 tools`.
Expected key result: it lists `kali-linux` and reports `7 tools`.

### 6) Connect Docker MCP Toolkit to Codex (global)

```bash
docker mcp client connect codex -g
```

Note: Codex supports Docker MCP connection as a **global** config (not repo-local).

### 7) Verify Codex sees Docker MCP

```bash
codex mcp list
```

Expected key result: an entry like:

- `MCP_DOCKER  docker  mcp gateway run`

## Current MCP tools exposed by this Kali server

- `run_command(command, timeout_seconds=60)`
- `get_system_info()`
- `list_security_tools()`
- `nmap_top_ports_scan(target, top_ports=100, timeout_seconds=180)`
- `whois_lookup(target, timeout_seconds=60)`
- `dig_lookup(name, record_type="A", timeout_seconds=30)`
- `ping_check(target, count=4, timeout_seconds=20)`

## Example prompts to run in Codex

- `Use kali-linux get_system_info`
- `Use kali-linux list_security_tools`
- `Use kali-linux nmap_top_ports_scan for scanme.nmap.org with top_ports 100`
- `Use kali-linux whois_lookup for openai.com`
- `Use kali-linux dig_lookup for openai.com with record_type MX`
- `Use kali-linux ping_check for 1.1.1.1`

## Quick sanity check for the container itself

```bash
docker run --rm cyber-kali-mcp:latest bash -lc 'cat /etc/os-release | head -n 2 && echo --- && nmap --version | head -n 1'
```

## Day-2 operations

### Rebuild after code changes

```bash
docker build -t cyber-kali-mcp:latest -f kali-mcp/Dockerfile kali-mcp
```

### Re-import catalog (if changed)

```bash
docker mcp catalog import ./docker-mcp-kali-catalog.yaml
```

### Disable Kali MCP server

```bash
docker mcp server disable kali-linux
```

### Disconnect Docker MCP from Codex

```bash
docker mcp client disconnect codex -g
```

## Security notes

- `run_command` executes shell commands inside the Kali container.
- Keep this setup on trusted hosts only.
- Do not mount sensitive host paths into this image unless you intentionally need that access.
