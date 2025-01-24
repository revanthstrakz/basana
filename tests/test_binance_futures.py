import pytest
from decimal import Decimal
from basana.external.binance.client import APIClient
from basana.external.binance.exchange import Exchange
from basana.core.enums import OrderOperation
from basana.core.pair import Pair

@pytest.fixture
def binance_client():
    return APIClient(api_key="your_api_key", api_secret="your_api_secret")

@pytest.fixture
def binance_exchange(binance_client):
    return Exchange(api_client=binance_client)

def test_futures_account_integration(binance_exchange):
    futures_account = binance_exchange.futures_account
    assert futures_account is not None

def test_create_futures_order(binance_exchange):
    futures_account = binance_exchange.futures_account
    order = futures_account.create_order(
        symbol="BTCUSDT",
        side="BUY",
        type="LIMIT",
        time_in_force="GTC",
        quantity=Decimal("0.001"),
        price=Decimal("30000")
    )
    assert order is not None
    assert order["symbol"] == "BTCUSDT"
    assert order["side"] == "BUY"
    assert order["type"] == "LIMIT"

def test_query_futures_order(binance_exchange):
    futures_account = binance_exchange.futures_account
    order = futures_account.create_order(
        symbol="BTCUSDT",
        side="BUY",
        type="LIMIT",
        time_in_force="GTC",
        quantity=Decimal("0.001"),
        price=Decimal("30000")
    )
    order_info = futures_account.query_order(symbol="BTCUSDT", order_id=order["orderId"])
    assert order_info is not None
    assert order_info["symbol"] == "BTCUSDT"
    assert order_info["orderId"] == order["orderId"]

def test_cancel_futures_order(binance_exchange):
    futures_account = binance_exchange.futures_account
    order = futures_account.create_order(
        symbol="BTCUSDT",
        side="BUY",
        type="LIMIT",
        time_in_force="GTC",
        quantity=Decimal("0.001"),
        price=Decimal("30000")
    )
    cancel_result = futures_account.cancel_order(symbol="BTCUSDT", order_id=order["orderId"])
    assert cancel_result is not None
    assert cancel_result["orderId"] == order["orderId"]

def test_get_open_futures_orders(binance_exchange):
    futures_account = binance_exchange.futures_account
    open_orders = futures_account.get_open_orders(symbol="BTCUSDT")
    assert open_orders is not None
    assert isinstance(open_orders, list)

def test_get_futures_trades(binance_exchange):
    futures_account = binance_exchange.futures_account
    trades = futures_account.get_trades(symbol="BTCUSDT")
    assert trades is not None
    assert isinstance(trades, list)
