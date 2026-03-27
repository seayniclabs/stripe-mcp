#!/usr/bin/env python3
"""
Stripe MCP — read-only tools for balances, customers, payment intents, invoices,
products, and prices. Uses STRIPE_SECRET_KEY from the environment (stdio transport).

Free / self-hosted. No write operations.
"""

from __future__ import annotations

import json
import logging
import os
import re
from collections.abc import Callable
from typing import Any

import stripe
from mcp.server.fastmcp import FastMCP

logging.getLogger("stripe").setLevel(logging.WARNING)

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")

mcp = FastMCP(
    "Stripe (read-only)",
    instructions=(
        "Read-only Stripe account data. Requires STRIPE_SECRET_KEY. "
        "Prefer a restricted key with read permissions only."
    ),
)


def _no_key() -> str:
    return json.dumps({"error": "STRIPE_SECRET_KEY is not set"})


def _as_json(obj: Any) -> str:
    if hasattr(obj, "to_dict") and not isinstance(obj, dict):
        obj = obj.to_dict()
    return json.dumps(obj, indent=2, default=str)


def _stripe_tool(fn: Callable[[], Any]) -> str:
    if not stripe.api_key:
        return _no_key()
    try:
        return _as_json(fn())
    except ValueError as e:
        return json.dumps({"error": str(e)})
    except stripe.StripeError as e:
        err: dict[str, Any] = {"error": str(e), "type": e.__class__.__name__}
        if getattr(e, "code", None):
            err["code"] = e.code
        return json.dumps(err)


_PREFIXES = {
    "customer": "cus_",
    "payment_intent": "pi_",
    "invoice": "in_",
    "charge": "ch_",
    "product": "prod_",
    "price": "price_",
}


def _id(kind: str, value: str) -> str:
    p = _PREFIXES[kind]
    if not value.startswith(p) or len(value) < len(p) + 8:
        raise ValueError(f"Invalid {kind} id (expected prefix {p})")
    if not re.match(r"^[a-zA-Z0-9_]+$", value):
        raise ValueError(f"Invalid {kind} id characters")
    return value


def _list_payload(result: Any) -> dict[str, Any]:
    rows = []
    for x in result.data:
        rows.append(x.to_dict() if hasattr(x, "to_dict") else x)
    return {"data": rows, "has_more": result.has_more}


@mcp.tool()
def stripe_get_balance() -> str:
    """Retrieve the connected account balance (available and pending amounts)."""
    return _stripe_tool(lambda: stripe.Balance.retrieve())


@mcp.tool()
def stripe_list_customers(limit: int = 10, starting_after: str | None = None) -> str:
    """List customers (newest first). limit 1-100; optional starting_after cursor (cus_...)."""
    def run() -> dict[str, Any]:
        lim = max(1, min(100, int(limit)))
        params: dict[str, Any] = {"limit": lim}
        if starting_after:
            params["starting_after"] = _id("customer", starting_after)
        return _list_payload(stripe.Customer.list(**params))

    return _stripe_tool(run)


@mcp.tool()
def stripe_get_customer(customer_id: str) -> str:
    """Retrieve a single customer by id (cus_...)."""
    def run() -> Any:
        return stripe.Customer.retrieve(_id("customer", customer_id))

    return _stripe_tool(run)


@mcp.tool()
def stripe_list_payment_intents(
    limit: int = 10, customer_id: str | None = None
) -> str:
    """List payment intents. Optional filter by customer_id (cus_...)."""
    def run() -> dict[str, Any]:
        lim = max(1, min(100, int(limit)))
        params: dict[str, Any] = {"limit": lim}
        if customer_id:
            params["customer"] = _id("customer", customer_id)
        return _list_payload(stripe.PaymentIntent.list(**params))

    return _stripe_tool(run)


@mcp.tool()
def stripe_list_invoices(limit: int = 10, customer_id: str | None = None) -> str:
    """List invoices. Optional filter by customer_id (cus_...)."""
    def run() -> dict[str, Any]:
        lim = max(1, min(100, int(limit)))
        params: dict[str, Any] = {"limit": lim}
        if customer_id:
            params["customer"] = _id("customer", customer_id)
        return _list_payload(stripe.Invoice.list(**params))

    return _stripe_tool(run)


@mcp.tool()
def stripe_list_products(limit: int = 10, active: bool | None = None) -> str:
    """List products. Optionally filter active=true/false."""
    def run() -> dict[str, Any]:
        lim = max(1, min(100, int(limit)))
        params: dict[str, Any] = {"limit": lim}
        if active is not None:
            params["active"] = active
        return _list_payload(stripe.Product.list(**params))

    return _stripe_tool(run)


@mcp.tool()
def stripe_list_prices(limit: int = 10, product_id: str | None = None) -> str:
    """List prices. Optional product_id (prod_...) filter."""
    def run() -> dict[str, Any]:
        lim = max(1, min(100, int(limit)))
        params: dict[str, Any] = {"limit": lim}
        if product_id:
            params["product"] = _id("product", product_id)
        return _list_payload(stripe.Price.list(**params))

    return _stripe_tool(run)


@mcp.tool()
def stripe_get_payment_intent(payment_intent_id: str) -> str:
    """Retrieve one payment intent by id (pi_...)."""
    def run() -> Any:
        return stripe.PaymentIntent.retrieve(_id("payment_intent", payment_intent_id))

    return _stripe_tool(run)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
