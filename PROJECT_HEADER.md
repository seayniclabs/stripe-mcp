# PROJECT_HEADER

**Project:** Stripe MCP  
**Type:** MCP Server  
**Status:** Active  
**Primary Language:** Python 3.12+  
**Repository:** https://github.com/seayniclabs/stripe-mcp  
**Last Updated:** 2026-06-09

## Overview

Read-only Stripe MCP server exposing account data (customers, payments, invoices, products, pricing) as structured tool calls for AI assistants. No mutation capabilities — designed for safe, audit-friendly queries only.

## Tech Stack

- **Runtime:** Python 3.12+
- **Framework:** FastMCP (Anthropic Model Context Protocol)
- **API Client:** Stripe Python SDK (v13+)
- **Deployment:** PyPI distribution (`stripe-mcp`)

## Infrastructure

### Network Resources

- **Protocol:** stdio (MCP server over stdin/stdout)
- **Deployment:** Local developer machine or CI/CD (no hosting)
- **Integration:** Claude Code, Claude Desktop, or any MCP client

### Service Dependencies

**Integrations (Outbound):**
- Stripe API (REST, live or test key) — `api.stripe.com`

**Integrations (Inbound):**
- Claude Code / Claude Desktop (MCP client)
- Any MCP-compatible IDE or tool

## Key Features

1. **Account Balance** — `stripe_get_balance`
2. **Customer Lookup** — `stripe_get_customer`, `stripe_list_customers` (paginated)
3. **Payment Intents** — `stripe_get_payment_intent`, `stripe_list_payment_intents`
4. **Invoices** — `stripe_list_invoices` (optional customer filter)
5. **Products & Pricing** — `stripe_list_products`, `stripe_list_prices`
6. **ID Validation** — Stripe prefix checks before API calls (e.g., `cus_*`, `pi_*`)
7. **Security** — Read-only by design; no create/update/delete tools

## Configuration

**Stripe Key:** Environment variable `STRIPE_SECRET_KEY` (test or live, prefer restricted key)

**Key Type:** Restricted API key with **read-only** permissions

```bash
export STRIPE_SECRET_KEY=sk_test_...
```

## Development

**Setup:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
```

**Run:**
```bash
stripe-mcp
# or
python -m stripe_mcp
```

**Test:**
```bash
pytest -v --cov=stripe_mcp
```

## Deployment

**Installation:**
```bash
pip install stripe-mcp
```

**Claude Code:**
```bash
claude mcp add stripe-mcp -e STRIPE_SECRET_KEY=sk_test_xxx -- stripe-mcp
```

**Claude Desktop** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "stripe-mcp": {
      "command": "stripe-mcp",
      "env": {
        "STRIPE_SECRET_KEY": "sk_test_..."
      }
    }
  }
}
```

## Documentation

- **README:** Installation, tool reference, usage examples
- **PyPI:** https://pypi.org/project/stripe-mcp/
- **GitHub:** Repository, issues, release notes

## License

MIT
