Binance Futures
===============

This section provides documentation for Binance futures account integration and examples for creating, querying, and canceling futures orders.

Binance Futures Account Integration
-----------------------------------

To integrate Binance futures account, you need to create an instance of the `APIClient` and access the `futures_account` property.

Example:

.. code-block:: python

    from basana.external.binance.client import APIClient

    api_client = APIClient(api_key="your_api_key", api_secret="your_api_secret")
    futures_account = api_client.futures_account

Creating Futures Orders
-----------------------

To create a futures order, use the `create_order` method of the `futures_account`.

Example:

.. code-block:: python

    from decimal import Decimal

    order = futures_account.create_order(
        symbol="BTCUSDT",
        side="BUY",
        type="LIMIT",
        time_in_force="GTC",
        quantity=Decimal("0.001"),
        price=Decimal("30000")
    )

Querying Futures Orders
-----------------------

To query a futures order, use the `query_order` method of the `futures_account`.

Example:

.. code-block:: python

    order_info = futures_account.query_order(symbol="BTCUSDT", order_id=order["orderId"])

Canceling Futures Orders
-------------------------

To cancel a futures order, use the `cancel_order` method of the `futures_account`.

Example:

.. code-block:: python

    cancel_result = futures_account.cancel_order(symbol="BTCUSDT", order_id=order["orderId"])

Getting Open Futures Orders
----------------------------

To get open futures orders, use the `get_open_orders` method of the `futures_account`.

Example:

.. code-block:: python

    open_orders = futures_account.get_open_orders(symbol="BTCUSDT")

Getting Futures Trades
-----------------------

To get futures trades, use the `get_trades` method of the `futures_account`.

Example:

.. code-block:: python

    trades = futures_account.get_trades(symbol="BTCUSDT")
