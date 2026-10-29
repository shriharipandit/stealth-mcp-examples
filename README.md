# Stealth Communications MCP examples

Connect an AI assistant or application to Stealth's public Model Context Protocol (MCP) service to check New York City fiber availability and retrieve current Dedicated Internet pricing.

- MCP endpoint: `https://stealth.net/mcp` (Streamable HTTP)
- [Developer guide and complete tool schemas](https://stealth.net/developers/mcp)
- [Online ordering terms](https://stealth.net/services/internet/dedicated/online-order-terms)
- [Independent service status](https://mcptry.com/servers/net.stealth/mcp)

This repository contains documentation and example client code. The hosted server's implementation is not included. No API key is required for the public endpoint.

## Connect a client

Connect a compatible MCP client to `https://stealth.net/mcp` using Streamable HTTP. See the [developer guide](https://stealth.net/developers/mcp) for connection details and raw JSON-RPC examples.

## Run read-only examples

Python 3.9 or later is required; no extra packages are needed. From this directory:

```sh
python3 examples/read_only.py pricing
python3 examples/read_only.py availability --address '50 Broad St' --borough Manhattan
```

These commands contact the live service. They do not place orders or submit inquiries. The availability example sends the address to Stealth; use an address you are authorized to share. Results, prices, and eligibility can change; use the live response rather than relying on static examples.

The example uses the supported MCP protocol version `2025-11-25`, initializes the connection, and calls one read-only tool. Errors and rate limits are reported rather than retried automatically. For production integrations, use a maintained MCP SDK and handle retry and rate-limit responses appropriately.

## Available tools

| Tool | Purpose |
| --- | --- |
| `check_building_availability` | Search a NYC address and retrieve candidates and eligibility. |
| `get_pricing` | Retrieve current prices, installation fees, and service terms. |
| `prepare_order` | Prepare a quote for a selected eligible building; does not place an order. |
| `place_order` | Submit a reviewed order after explicit customer authorization and acceptance. |
| `prepare_availability_inquiry` | Prepare an inquiry for manual review; sends nothing. |
| `submit_availability_inquiry` | Submit the reviewed inquiry after explicit customer approval. |

For required inputs, conditions, signed tokens, and current terms, consult the live tool schemas and [developer guide](https://stealth.net/developers/mcp). Ask the customer to select the correct building when multiple candidates are returned. Never submit an order or inquiry without the required explicit customer approval. If a submission is interrupted, follow the guide's instructions to retry using the same token.

## Service limits and privacy

Public requests are subject to service limits; see the developer guide for current details. Do not put customer contact information, tokens, or secrets into issue reports or public logs. Review the privacy guidance in the developer guide before sharing customer information.

## License

The example code and documentation are provided for use under the [MIT License](LICENSE).
