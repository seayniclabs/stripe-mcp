# Stripe MCP (read-only)

Small [Model Context Protocol](https://modelcontextprotocol.io) server for **read-only** Stripe data: balance, customers, payment intents, invoices, products, prices.

**Repository:** https://github.com/seayniclabs/stripe-mcp

- **Free**, self-hosted, stdio transport
- **No** create/update/delete tools — use a [restricted key](https://docs.stripe.com/keys#create-restricted-api-secret-key) with read-only permissions when possible

## Requirements

- **Python 3.10+** (recommended: install with [uv](https://docs.astral.sh/uv/))
- A Stripe secret key (`sk_test_...` or `sk_live_...`) in the environment

## Setup

```bash
cd stripe-mcp
uv venv --python 3.12
uv pip install -r requirements.txt
export STRIPE_SECRET_KEY=sk_test_...
```

## Run

```bash
.venv/bin/python server.py
```

## Claude Code

```bash
claude mcp add stripe -e STRIPE_SECRET_KEY=sk_test_xxx -- /absolute/path/to/stripe-mcp/.venv/bin/python /absolute/path/to/stripe-mcp/server.py
```

(Use your real key via env file or shell; avoid committing keys.)

## Tools

| Tool | Purpose |
|------|---------|
| `stripe_get_balance` | Account balance |
| `stripe_list_customers` | Paginated customers |
| `stripe_get_customer` | One customer |
| `stripe_list_payment_intents` | Payment intents |
| `stripe_get_payment_intent` | One payment intent |
| `stripe_list_invoices` | Invoices |
| `stripe_list_products` | Products |
| `stripe_list_prices` | Prices |

## License

MIT
