#!/usr/bin/env python3
import ipaddress
import re
import shutil
import subprocess
from typing import Dict, List

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("kali-linux")
MAX_OUTPUT_CHARS = 20000
HOSTNAME_PATTERN = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*$"
)


def _is_valid_target(value: str) -> bool:
    target = value.strip()
    if not target:
        return False

    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        pass

    try:
        ipaddress.ip_network(target, strict=False)
        return True
    except ValueError:
        pass

    return bool(HOSTNAME_PATTERN.fullmatch(target))


def _run_process(args: List[str], timeout_seconds: int) -> Dict[str, str | int]:
    completed = subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        check=False,
    )

    return {
        "command": " ".join(args),
        "exit_code": completed.returncode,
        "stdout": completed.stdout[-MAX_OUTPUT_CHARS:],
        "stderr": completed.stderr[-MAX_OUTPUT_CHARS:],
    }


@mcp.tool()
def run_command(command: str, timeout_seconds: int = 60) -> Dict[str, str | int]:
    """Run a shell command inside the Kali Linux container."""
    if timeout_seconds < 1 or timeout_seconds > 600:
        raise ValueError("timeout_seconds must be between 1 and 600")
    if not command.strip():
        raise ValueError("command must not be empty")

    completed = subprocess.run(
        ["bash", "-lc", command],
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        check=False,
    )

    # Keep responses bounded so large outputs do not overwhelm the client.
    stdout = completed.stdout[-MAX_OUTPUT_CHARS:]
    stderr = completed.stderr[-MAX_OUTPUT_CHARS:]

    return {
        "exit_code": completed.returncode,
        "stdout": stdout,
        "stderr": stderr,
    }


@mcp.tool()
def get_system_info() -> Dict[str, str]:
    """Return basic OS information for the running container."""
    os_release = subprocess.run(
        ["bash", "-lc", "cat /etc/os-release"],
        capture_output=True,
        text=True,
        check=False,
    )

    kernel = subprocess.run(
        ["bash", "-lc", "uname -a"],
        capture_output=True,
        text=True,
        check=False,
    )

    return {
        "os_release": os_release.stdout.strip(),
        "kernel": kernel.stdout.strip(),
    }


@mcp.tool()
def list_security_tools() -> List[str]:
    """List common security tool binaries available in this image."""
    candidates = [
        "nmap",
        "nc",
        "dig",
        "whois",
        "curl",
        "git",
        "python3",
    ]
    return [name for name in candidates if shutil.which(name)]


@mcp.tool()
def nmap_top_ports_scan(
    target: str, top_ports: int = 100, timeout_seconds: int = 180
) -> Dict[str, str | int]:
    """Run an nmap service/version scan against the top ports for a target."""
    if not _is_valid_target(target):
        raise ValueError("target must be a valid IP, CIDR, or hostname")
    if top_ports < 1 or top_ports > 1000:
        raise ValueError("top_ports must be between 1 and 1000")
    if timeout_seconds < 1 or timeout_seconds > 600:
        raise ValueError("timeout_seconds must be between 1 and 600")

    args = ["nmap", "-sV", "--top-ports", str(top_ports), "-T3", target]
    return _run_process(args, timeout_seconds=timeout_seconds)


@mcp.tool()
def whois_lookup(target: str, timeout_seconds: int = 60) -> Dict[str, str | int]:
    """Run whois for a hostname/domain/IP target."""
    if not _is_valid_target(target):
        raise ValueError("target must be a valid IP, CIDR, or hostname")
    if timeout_seconds < 1 or timeout_seconds > 600:
        raise ValueError("timeout_seconds must be between 1 and 600")

    args = ["whois", target]
    return _run_process(args, timeout_seconds=timeout_seconds)


@mcp.tool()
def dig_lookup(
    name: str, record_type: str = "A", timeout_seconds: int = 30
) -> Dict[str, str | int]:
    """Query DNS with dig and return short-form output."""
    valid_types = {"A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "PTR"}
    upper_type = record_type.upper()

    if not _is_valid_target(name):
        raise ValueError("name must be a valid IP, CIDR, or hostname")
    if upper_type not in valid_types:
        raise ValueError(
            "record_type must be one of A, AAAA, MX, NS, TXT, CNAME, SOA, PTR"
        )
    if timeout_seconds < 1 or timeout_seconds > 600:
        raise ValueError("timeout_seconds must be between 1 and 600")

    args = ["dig", "+short", name, upper_type]
    return _run_process(args, timeout_seconds=timeout_seconds)


@mcp.tool()
def ping_check(
    target: str, count: int = 4, timeout_seconds: int = 20
) -> Dict[str, str | int]:
    """Ping a target to verify basic network reachability."""
    if not _is_valid_target(target):
        raise ValueError("target must be a valid IP, CIDR, or hostname")
    if count < 1 or count > 10:
        raise ValueError("count must be between 1 and 10")
    if timeout_seconds < 1 or timeout_seconds > 120:
        raise ValueError("timeout_seconds must be between 1 and 120")

    args = ["ping", "-c", str(count), target]
    return _run_process(args, timeout_seconds=timeout_seconds)


if __name__ == "__main__":
    mcp.run(transport="stdio")
