# PROJECT_HEADER

**Project:** Stripe MCP  
**Type:** MCP Server  
**Status:** Active  
**Primary Language:** Python 3.12+  
**Repository:** https://github.com/seayniclabs/stripe-mcp  
**Last Updated:** 2026-06-09

## Overview

Read-only Stripe MCP server exposing account data (customers, payments, invoices, products, pricing) as structured tool calls for AI assistants. No mutation capabilities — designed for safe, audit-friendly queries only.

## Current State

Stripe-MCP is a read-only Python 3.12+ Stripe MCP server published on PyPI as `stripe-mcp`. Latest commit (6521e9c) fixes aiohttp dependency (CVE-2026-34993). Clean repository (no uncommitted changes). Exposes Stripe account data via stdio MCP protocol; used by Claude Code and Claude Desktop for safe, audit-friendly Stripe queries. No mutation capabilities—designed for read-only analysis and reporting. Supports live and test keys; integrates Stripe Python SDK v13+.

## Assessment — 2026-06-10

**Last Updated:** 2026-06-10

### Errors & Risks

- [LOW] Dependency `aiohttp` historically CVE-prone — already patched once (6521e9c); should add automated CVE scanning to CI
- [LOW] Python 3.12+ requirement is strict; 3.11 support would broaden user base (not a risk, design choice)
- [LOW] No explicit logging for API key usage — if user provides invalid key, error is silent (JSON `{"error": "..."}` response only)
- [NONE] No mutation risks detected; all tools are genuinely read-only (verified by grep: no create/update/delete/refund calls)

### Security

- **Auth:** STRIPE_SECRET_KEY sourced from environment (good practice); no key validation at startup (accepts any string, Stripe API validates on first call).
- **Rate Limiting:** None at MCP level (relies on Stripe API limits); acceptable for AI assistant use (low QPS).
- **Input Validation:** Stripe ID validation is strong (`_id()` function checks prefix, length, character set); prevents injection attempts.
- **Mutation Prevention:** Explicitly read-only by design; no mutation tools exposed (verified by code review).
- **Error Handling:** Catches `stripe.StripeError` and returns JSON error (good); ValueError also caught.
- **Key Preference:** Code recommends restricted key with read permissions only (good practice documented).
- **Logging:** No sensitive logging visible; Stripe SDK handles its own logs (filtered at WARNING level).

**12-Control Checklist:**
1. ✅ Auth — STRIPE_SECRET_KEY from environment; no hardcoded keys
2. ✅ Rate Limiting — Not applicable (Stripe handles); MCP calls are low-frequency
3. ✅ Input Validation — Strong ID prefix/length/charset validation
4. ✅ SQL Injection — Not applicable (no SQL; Stripe REST API calls only)
5. ✅ CORS — Not applicable (stdio transport)
6. ✅ Streaming — Not applicable (MCP returns JSON only)
7. ✅ Deserialization — Stripe SDK handles deserialization; library only serializes to JSON
8. ✅ Error Handling — Explicit error catching; generic JSON responses to client
9. ✅ HTTPS — Stripe SDK enforces TLS; `api.stripe.com` is HTTPS-only
10. ✅ Secrets — STRIPE_SECRET_KEY from environment; no hardcoded values
11. ✅ Data Isolation — Single-tenant (one Stripe account per key); N/A multi-tenant
12. ⚠️ Dependency Pinning — pyproject.toml has pinned ranges (e.g., `aiohttp>=3.13.4,<4`) but not exact versions; consider lock file for reproducibility

### Improvements

1. **Add CVE scanning to CI** — Use `pip-audit` or OWASP Dependency-Check in CI pipeline; fail on known vulnerabilities.
2. **Recommend live vs test keys** — Document that live key requires explicit opt-in (env var with strict name like `STRIPE_LIVE_SECRET_KEY`); warn in --help.
3. **Add key fingerprinting** — Log hash of API key on startup (first 8 chars of hash only, never full key) so user can verify correct key is loaded.
4. **Add timeout to all API calls** — Stripe SDK should have a global timeout to prevent hanging on network failures; verify timeout is set in integration tests.
5. **Publish typed stubs** — If not already published, add `py.typed` marker and consider publishing `.pyi` files on PyPI for better IDE support.
6. **Add list pagination helpers** — `stripe_list_customers()` accepts `starting_after` cursor; document pagination pattern in README with examples.
7. **Consider rate-limit headers** — Stripe includes rate-limit info in response headers; optionally parse and warn if approaching quota.

### Cost

- **Library Only:** No cost to Seaynic Labs (PyPI hosting is free; GitHub hosting is free).
- **Stripe Usage:** Depends on end-user's Stripe account and query frequency. MCP queries (list, get) are **read-only** and don't incur transaction fees; only API rate limits apply.
- **No Upgrade Needed:** Functionality and cost are appropriate.

### Performance

- **Cold Start:** Python 3.12+ startup ~500ms (acceptable for MCP).
- **API Calls:** Stripe SDK calls are network-bound; typical latency 200–500ms per query (depends on Stripe infrastructure).
- **List Pagination:** Stripe's cursor-based pagination is efficient; limit defaults to 10, max 100 (good UX defaults).
- **No Bottlenecks:** Library is thin wrapper; performance depends entirely on Stripe API.

### Verdict

**Grade: A–** (Production-Ready, Read-Only Safe)

Solid read-only MCP server; genuinely mutation-proof; secrets handling is correct; error handling is robust. Only minor improvements: add CVE scanning to CI, document live-key workflow, and add optional key fingerprinting. No blockers. Ready for production use by Claude Code and Claude Desktop users.

---

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

## Next Steps

1. **[Priority: Med]** Add mutation capabilities (Phase 2) — implement safe mutation operations (create invoices, update metadata) with explicit approval gates; require STRIPE_ADMIN_KEY.

2. **[Priority: Med]** Implement analytics tools — add revenue reporting, customer cohort analysis, payment trend analysis; enable business intelligence queries.

3. **[Priority: Low]** Add webhook management tools — expose webhook creation/management/testing via MCP; enable safe automation of webhook workflows.

## Documentation

- **README:** Installation, tool reference, usage examples
- **PyPI:** https://pypi.org/project/stripe-mcp/
- **GitHub:** Repository, issues, release notes

## License

MIT
