# Stripe MCP

**Read-Only Stripe MCP Server**

[![License: MIT](https://img.shields.io/badge/License-MIT-635BFF.svg)](LICENSE)

*Account data for AI tools — balance, customers, payments, invoices, catalog — without write access.*

---

## What It Does

Stripe MCP is a [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that exposes **read-only** [Stripe](https://stripe.com/) API data as structured tool calls. Use it from Claude Code, Claude Desktop, or any MCP client. There are **no** create, update, or delete tools.

---

## Tools

| Tool | Description | Key parameters |
|------|-------------|------------------|
| `stripe_get_balance` | Connected account balance | — |
| `stripe_list_customers` | List customers (paginated) | `limit` (1–100), `starting_after` (`cus_...`) |
| `stripe_get_customer` | Retrieve one customer | `customer_id` (`cus_...`) |
| `stripe_list_payment_intents` | List payment intents | `limit`, optional `customer_id` |
| `stripe_get_payment_intent` | Retrieve one payment intent | `payment_intent_id` (`pi_...`) |
| `stripe_list_invoices` | List invoices | `limit`, optional `customer_id` |
| `stripe_list_products` | List products | `limit`, optional `active` |
| `stripe_list_prices` | List prices | `limit`, optional `product_id` (`prod_...`) |

---

## Installation

From PyPI (after first release):

```bash
pip install stripe-mcp
```

Or install from a git clone in editable mode:

```bash
git clone https://github.com/seayniclabs/stripe-mcp.git
cd stripe-mcp
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
```

Requires **Python 3.12+**.

Set a Stripe secret key (test or live):

```bash
export STRIPE_SECRET_KEY=sk_test_...
```

Prefer a [restricted API key](https://docs.stripe.com/keys#create-restricted-api-secret-key) with **read-only** permissions.

---

## Usage

Run the server (stdio transport):

```bash
stripe-mcp
```

Or via module:

```bash
python -m stripe_mcp
```

### Claude Code

```bash
claude mcp add stripe-mcp -e STRIPE_SECRET_KEY=sk_test_xxx -- stripe-mcp
```

If using a venv, pass the full path to `stripe-mcp` inside `.venv/bin/`.

### Claude Desktop

Add to `claude_desktop_config.json`:

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

---

## Security

- **Read-only by design** — no tools mutate Stripe objects.
- **Validate IDs** — customer, payment intent, and product IDs are checked for expected Stripe prefixes before API calls.
- **Secrets in the environment only** — never commit `STRIPE_SECRET_KEY`; use env vars or your MCP client’s secret mechanism.
- **Stripe SDK logging** — the `stripe` logger is set to WARNING to reduce noise in stdio sessions.

---

## Development

```bash
pip install -e ".[test]"
pytest -v --cov=stripe_mcp
```

---

## License

[MIT](LICENSE)
