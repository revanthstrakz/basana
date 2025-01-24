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
import logging

from . import helpers
from basana.core import bar, event, websockets as core_ws
from basana.core.pair import Pair


logger = logging.getLogger(__name__)


class Bar(bar.Bar):
    def __init__(self, pair: Pair, json: dict):
        super().__init__(
            helpers.timestamp_to_datetime(int(json["t"])), pair, Decimal(json["o"]), Decimal(json["h"]),
            Decimal(json["l"]), Decimal(json["c"]), Decimal(json["v"])
        )
        self.pair: Pair = pair
        self.json: dict = json


# Generate BarEvents events from websocket messages.
class WebSocketEventSource(core_ws.ChannelEventSource):
    def __init__(self, pair: Pair, producer: event.Producer):
        super().__init__(producer=producer)
        self._pair: Pair = pair

    async def push_from_message(self, message: dict):
        kline_event = message["data"]
        kline = kline_event["k"]
        # Wait for the last update to the kline.
        if kline["x"] is False:
            return
        self.push(bar.BarEvent(
            helpers.timestamp_to_datetime(int(kline_event["E"])),
            Bar(self._pair, kline)
        ))


def get_channel(pair: Pair, interval: str) -> str:
    return "{}@kline_{}".format(helpers.pair_to_order_book_symbol(pair).lower(), interval)


class FuturesBar(bar.Bar):
    def __init__(self, pair: Pair, json: dict):
        super().__init__(
            helpers.timestamp_to_datetime(int(json["t"])), pair, Decimal(json["o"]), Decimal(json["h"]),
            Decimal(json["l"]), Decimal(json["c"]), Decimal(json["v"])
        )
        self.pair: Pair = pair
        self.json: dict = json


# Generate BarEvents events from websocket messages for futures market.
class FuturesWebSocketEventSource(core_ws.ChannelEventSource):
    def __init__(self, pair: Pair, producer: event.Producer):
        super().__init__(producer=producer)
        self._pair: Pair = pair

    async def push_from_message(self, message: dict):
        kline_event = message["data"]
        kline = kline_event["k"]
        # Wait for the last update to the kline.
        if kline["x"] is False:
            return
        self.push(bar.BarEvent(
            helpers.timestamp_to_datetime(int(kline_event["E"])),
            FuturesBar(self._pair, kline)
        ))


def get_futures_channel(pair: Pair, interval: str) -> str:
    return "{}@kline_{}".format(helpers.pair_to_order_book_symbol(pair).lower(), interval)


class FuturesTrade:
    def __init__(self, pair: Pair, json: dict):
        assert json["e"] == "trade"

        self.pair: Pair = pair
        self.json: dict = json

    @property
    def id(self) -> str:
        return str(self.json["t"])

    @property
    def datetime(self) -> datetime.datetime:
        return helpers.timestamp_to_datetime(int(self.json["T"]))

    @property
    def price(self) -> Decimal:
        return Decimal(self.json["p"])

    @property
    def amount(self) -> Decimal:
        return Decimal(self.json["q"])

    @property
    def buy_order_id(self) -> str:
        return str(self.json["b"])

    @property
    def sell_order_id(self) -> str:
        return str(self.json["a"])


class FuturesTradeEvent(event.Event):
    def __init__(self, when: datetime.datetime, trade: FuturesTrade):
        super().__init__(when)
        self.trade: FuturesTrade = trade


class FuturesTradeWebSocketEventSource(core_ws.ChannelEventSource):
    def __init__(self, pair: Pair, producer: event.Producer):
        super().__init__(producer=producer)
        self._pair: Pair = pair

    async def push_from_message(self, message: dict):
        trade_event = message["data"]
        self.push(FuturesTradeEvent(
            helpers.timestamp_to_datetime(int(trade_event["E"])),
            FuturesTrade(self._pair, trade_event)
        ))


def get_futures_trade_channel(pair: Pair) -> str:
    return "{}@trade".format(helpers.pair_to_order_book_symbol(pair).lower())


class FuturesOrderBook:
    def __init__(self, pair: Pair, json: dict):
        self.pair: Pair = pair
        self.json: dict = json

    @property
    def bids(self) -> List[order_book.Entry]:
        return [
            order_book.Entry(price=Decimal(entry[0]), volume=Decimal(entry[1])) for entry in self.json["bids"]
        ]

    @property
    def asks(self) -> List[order_book.Entry]:
        return [
            order_book.Entry(price=Decimal(entry[0]), volume=Decimal(entry[1])) for entry in self.json["asks"]
        ]


class FuturesOrderBookEvent(event.Event):
    def __init__(self, when: datetime.datetime, order_book: FuturesOrderBook):
        super().__init__(when)
        self.order_book: FuturesOrderBook = order_book


class FuturesOrderBookWebSocketEventSource(core_ws.ChannelEventSource):
    def __init__(self, pair: Pair, producer: event.Producer):
        super().__init__(producer=producer)
        self._pair: Pair = pair

    async def push_from_message(self, message: dict):
        order_book_event = message["data"]
        self.push(FuturesOrderBookEvent(
            dt.utc_now(),
            FuturesOrderBook(self._pair, order_book_event)
        ))


def get_futures_order_book_channel(pair: Pair, depth: int) -> str:
    assert depth in [5, 10, 20], "Invalid depth"
    return "{}@depth{}".format(helpers.pair_to_order_book_symbol(pair).lower(), depth)
