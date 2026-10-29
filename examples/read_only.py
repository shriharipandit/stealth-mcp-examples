#!/usr/bin/env python3
"""Call read-only tools on the public Stealth MCP server."""
import argparse
import json
import sys
import urllib.error
import urllib.request

URL = "https://stealth.net/mcp"
VERSION = "2025-11-25"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "MCP-Protocol-Version": VERSION,
}


def request(method, params=None, request_id=None):
    message = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        message["params"] = params
    if request_id is not None:
        message["id"] = request_id
    data = json.dumps(message).encode("utf-8")
    req = urllib.request.Request(URL, data=data, headers=HEADERS, method="POST")
    with urllib.request.urlopen(req, timeout=20) as response:
        body = response.read()
    if request_id is None:
        return None
    result = json.loads(body)
    if result.get("id") != request_id:
        raise ValueError("Unexpected JSON-RPC response ID")
    if "error" in result:
        raise ValueError("JSON-RPC error: " + json.dumps(result["error"]))
    if not isinstance(result.get("result"), dict):
        raise ValueError("Missing JSON-RPC result")
    return result["result"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("pricing", help="Get current pricing")
    availability = sub.add_parser("availability", help="Check an NYC business address")
    availability.add_argument("--address", required=True)
    availability.add_argument("--borough", required=True,
                              choices=["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"])
    args = parser.parse_args()
    initialized = request("initialize", {"protocolVersion": VERSION, "capabilities": {},
                          "clientInfo": {"name": "stealth-read-only-example", "version": "1.0.0"}}, 1)
    if initialized.get("protocolVersion") != VERSION:
        raise ValueError("Server did not negotiate the expected MCP protocol version")
    request("notifications/initialized")
    name = "get_pricing" if args.command == "pricing" else "check_building_availability"
    arguments = {} if args.command == "pricing" else {"address": args.address, "borough": args.borough}
    result = request("tools/call", {"name": name, "arguments": arguments}, 2)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result.get("isError"):
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        print("MCP request failed: " + str(exc), file=sys.stderr)
        sys.exit(1)
