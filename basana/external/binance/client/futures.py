# Basana
#
# Copyright 2022 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from decimal import Decimal
from typing import Any, Dict, List, Optional

from . import base


class FuturesAccount:
    def __init__(self, client: base.BaseClient):
        self._client = client

    async def create_order(
            self, symbol: str, side: str, type: str, time_in_force: Optional[str] = None,
            quantity: Optional[Decimal] = None, price: Optional[Decimal] = None,
            stop_price: Optional[Decimal] = None, new_client_order_id: Optional[str] = None, **kwargs: Dict[str, Any]
    ) -> dict:
        params: Dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": type,
        }
        base.set_optional_params(params, (
            ("timeInForce", time_in_force),
            ("quantity", quantity),
            ("price", price),
            ("stopPrice", stop_price),
            ("newClientOrderId", new_client_order_id),
        ))
        params.update(kwargs)
        return await self._client.make_request("POST", "/fapi/v1/order", data=params, send_sig=True)

    async def query_order(
            self, symbol: str, order_id: Optional[int] = None, orig_client_order_id: Optional[str] = None
    ) -> dict:
        assert (order_id is not None) ^ (orig_client_order_id is not None), \
            "Either order_id or orig_client_order_id should be set"

        params: Dict[str, Any] = {
            "symbol": symbol,
        }
        base.set_optional_params(params, (
            ("orderId", order_id),
            ("origClientOrderId", orig_client_order_id),
        ))
        return await self._client.make_request("GET", "/fapi/v1/order", qs_params=params, send_sig=True)

    async def get_open_orders(
            self, symbol: Optional[str] = None
    ) -> dict:
        params: Dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        return await self._client.make_request("GET", "/fapi/v1/openOrders", qs_params=params, send_sig=True)

    async def cancel_order(
            self, symbol: str, order_id: Optional[int] = None, orig_client_order_id: Optional[str] = None
    ) -> dict:
        assert (order_id is not None) ^ (orig_client_order_id is not None), \
            "Either order_id or orig_client_order_id should be set"

        params: Dict[str, Any] = {
            "symbol": symbol,
        }
        base.set_optional_params(params, (
            ("orderId", order_id),
            ("origClientOrderId", orig_client_order_id),
        ))
        return await self._client.make_request("DELETE", "/fapi/v1/order", qs_params=params, send_sig=True)

    async def get_trades(self, symbol: str, order_id: Optional[int] = None) -> List[dict]:
        params: Dict[str, Any] = {
            "symbol": symbol,
        }
        if order_id is not None:
            params["orderId"] = order_id
        return await self._client.make_request("GET", "/fapi/v1/userTrades", qs_params=params, send_sig=True)

    async def create_listen_key(self) -> dict:
        return await self._client.make_request("POST", "/fapi/v1/listenKey", send_key=True)

    async def keep_alive_listen_key(self, listen_key: str) -> dict:
        params: Dict[str, Any] = {
            "listenKey": listen_key,
        }
        return await self._client.make_request("PUT", "/fapi/v1/listenKey", send_key=True, data=params)
