"""Tests for Stripe MCP tools (no live Stripe API calls)."""

from __future__ import annotations

import json
import os
from unittest.mock import MagicMock, patch

import pytest

from stripe_mcp.server import (
    _id,
    stripe_get_balance,
    stripe_get_customer,
    stripe_list_customers,
)


def test_id_accepts_valid_customer():
    assert _id("customer", "cus_xxxxxxxxxxxxxxxx") == "cus_xxxxxxxxxxxxxxxx"


@pytest.mark.parametrize(
    "value",
    ["bad", "cus_short", "cus_!!!!bad!!!", "other_xxxxxxxxxxxxxx"],
)
def test_id_rejects_invalid_customer(value: str):
    with pytest.raises(ValueError):
        _id("customer", value)


def test_balance_without_api_key(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("STRIPE_SECRET_KEY", raising=False)
    out = json.loads(stripe_get_balance())
    assert out == {"error": "STRIPE_SECRET_KEY is not set"}


def test_balance_with_mock_stripe(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_test_fake")
    mock_bal = MagicMock()
    mock_bal.to_dict.return_value = {"object": "balance", "available": []}
    with patch("stripe_mcp.server.stripe.Balance.retrieve", return_value=mock_bal):
        out = json.loads(stripe_get_balance())
    assert out["object"] == "balance"


def test_list_customers_clamps_limit(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_test_fake")
    mock_list = MagicMock()
    mock_list.data = []
    mock_list.has_more = False
    with patch("stripe_mcp.server.stripe.Customer.list", return_value=mock_list) as m:
        stripe_list_customers(limit=500)
    assert m.call_args[1]["limit"] == 100


def test_get_customer_invalid_id(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_test_fake")
    out = json.loads(stripe_get_customer("not_a_customer"))
    assert "error" in out
