"""接口基础类"""

from typing import Optional, Union, Dict, List
from vxquant.model.preset import vxMarketPreset
from vxquant.model.typehint import DateTimeType
from vxquant.model.exchange import (
    vxOrder,
    vxAccountInfo,
    vxPosition,
    vxCashPosition,
    vxTrade,
    vxTransferInfo,
    vxPortfolioInfo,
)
from vxquant.model.contants import (
    OrderDirection,
    OrderStatus,
    OrderType,
    SecType,
    TradeStatus,
)
from vxquant.accountdb.base import vxAccountDB
from vxquant.exceptions import NoEnoughCash, NoEnoughPosition
from vxsched.triggers import vxIntervalTrigger, vxOnceTrigger
from vxsched import vxContext, vxEvent, vxScheduler
from vxutils import (
    vxWrapper,
    vxAPIWrappers,
    logger,
    to_timestamp,
    vxtime,
    to_datetime,
    combine_datetime,
)

vxPositionType = Union[vxPosition, vxCashPosition]


def sub_volume(
    position: Union[vxCashPosition, vxPosition], volume: Union[float, int]
) -> Union[vxCashPosition, vxPosition]:
    """扣减持仓量

    Arguments:
        position {Union[vxCashPosition, vxPosition]} -- 需要扣减的持仓
        volume {Union[float, int]} -- 扣减量

    Raises:
        NoEnoughPosition: 扣减持仓不足

    Returns:
        Union[vxCashPosition, vxPosition] -- 扣减后的持仓
    """
    if volume > position.available:
        raise NoEnoughPosition(
            f"{position.symbol}可用余额({position.available:,.2f})"
            f" 小于需扣减{volume:,.2f}"
        )

    delta = position.volume_his - volume
    position.volume_his = max(delta, 0)
    position.volume_today += min(delta, 0)
    return position


class vxMdAPI(vxAPIWrappers):
    """行情接口类"""

    __defaults__ = {
        "current": {"class": "vxquant.providers.tdx.MultiTdxHQProvider", "params": {}},
        "calendar": {
            "class": "vxquant.providers.spiders.calendar_sse.CNCalenderProvider",
            "params": {},
        },
        "instruments": {
            "class": "vxquant.providers.local.vxLocalInstrumentsProvider",
            "params": {},
        },
        "features": {
            "class": "vxquant.providers.local.vxLocalFeaturesProvider",
            "params": {},
        },
    }

    def set_context(self, context):
        for provider in self.__dict__.values():
            if hasattr(provider, "set_context"):
                provider.set_context(context)


class vxTdAPI(vxAPIWrappers):
    """交易接口类"""

    __defaults__ = {
        "current": {"class": "vxquant.providers.tdx.MultiTdxHQProvider", "params": {}},
        "get_account": {},
        "get_positions": {},
        "get_orders": {},
        "get_execution_reports": {},
        "order_batch": {},
        "order_cancel": {},
    }

    def set_context(self, context):
        for provider in self.__dict__.values():
            if hasattr(provider, "set_context"):
                provider.set_context(context)

    def order_volume(
        self,
        symbol: str,
        volume: int,
        price: Optional[float] = 0,
        account_id: str = None,
    ) -> vxOrder:
        """下单

        Arguments:
            account_id {str} -- 账户ID
            symbol {str} -- 证券代码
            volume {int} -- 委托数量
            price {Optional[float]} -- 委托价格,若price为None,则使用市价委托 (default: {None})

        Returns:
            vxorder {vxOrder} -- 下单委托订单号
        """
        if volume == 0:
            raise ValueError("volume can't be 0.")

        order_type = OrderType.Limit
        if not price:
            ticks = self.current(symbol)
            price = ticks[symbol].ask1_p if volume > 0 else ticks[symbol].bid1_p
            order_type = (
                OrderType.Limit
                if vxMarketPreset(symbol).security_type == SecType.BOND_CONVERTIBLE
                else OrderType.Market
            )

        vxorder = vxOrder(
            account_id=account_id,
            symbol=symbol,
            volume=abs(volume),
            price=price,
            order_offset="Open" if volume > 0 else "Close",
            order_direction="Buy" if volume > 0 else "Sell",
            order_type=order_type,
            status="PendingNew",
        )
        ret_orders = self.order_batch(vxorder)
        return ret_orders[0]


class vxTeller:
    """交易员类"""

    def __init__(
        self,
        accountdb: Union[vxAccountDB, Dict],
        mdapi: Union[vxMdAPI, Dict] = None,
        channels: Dict = None,
    ):
        self._db: vxAccountDB = vxWrapper.init_by_config(accountdb)

        if isinstance(mdapi, dict):
            mdapi = vxWrapper.init_by_config(mdapi)

        self._mdapi = mdapi or vxMdAPI()

        self._channels = {}
        if channels:
            for channel_name, tdapi in channels.items():
                if isinstance(tdapi, dict):
                    tdapi = vxWrapper.init_by_config(tdapi)

                self.add_channel(channel_name, tdapi)

        self._sched: vxScheduler = None

    def create_account(
        self,
        portfolio_id: str,
        account_id: str,
        init_balance=1_000_000.0,
        created_dt: DateTimeType = None,
        if_exists: str = "ignore",
        channel: str = "sim",
    ) -> vxAccountInfo:
        """创建账户

        Arguments:
            portfolio_id {str} -- 组合ID
            account_id {str} -- 账户ID

        Keyword Arguments:
            init_balance {float} -- 初始资金 (default: {1,000,000.0})
            created_dt {DateTimeType} -- 创建时间 (default: {None})
            if_exists {str} -- 若已存在,则delete || ignore  (default: {"ignore"})
            channel {str} -- 委托下单通道 (default: {"sim"})

        Returns:
            vxAccountInfo -- 已创建的账户信息
        """
        with self._db.start_session() as session:
            accountinfo = session.create_account(
                portfolio_id, account_id, init_balance, created_dt, if_exists, channel
            )
            if channel not in self._channels:
                logger.warning(
                    f"channel {channel} not found, please add it before place an order."
                )
            return accountinfo

    def add_channel(self, channel: str, tdapi: vxTdAPI) -> None:
        """增加交易通道

        Arguments:
            channel {str} -- 交易通道名称
            tdapi {vxTdAPI} -- 交易接口
        """
        broker_account = tdapi.get_account()
        broker_positions = tdapi.get_positions()
        broker_orders = tdapi.get_orders()
        broker_trades = tdapi.get_execution_reports()
        with self._db.start_session() as session:
            try:
                session.sync_with_broker(
                    broker_account, broker_positions, broker_orders, broker_trades
                )
            except Exception as e:
                logger.warning(f"同步账户信息失败: {e}")

        self._channels[channel] = tdapi
        logger.info(f"channel {channel} added.")
        return

    def deposit(
        self, account_id: str, amount: float, transfer_dt: DateTimeType = None
    ) -> vxTransferInfo:
        """转入资金

        Arguments:
            account_id {str} -- 账户ID
            amount {float} -- 转入金额
            transfer_dt {DateTimeType} -- 转入时间 (default: {None})

        Returns:
            vxTransferInfo -- 转账信息
        """
        if amount < 0:
            raise ValueError(f"转入金额({amount})应大于0 .")

        with self._db.start_session() as session:
            transfer_dt = to_timestamp(transfer_dt or vxtime.now())

            # 转账交易记录
            transferinfo = vxTransferInfo(
                account_id=account_id,
                amount=amount,
                transfer_direction="In",
                created_dt=transfer_dt,
            )

            cash = session.findone("positions", account_id=account_id, symbol="CNY")
            cash = vxCashPosition(**cash.message)
            cash.volume_today += amount

            accountinfo = session.findone("accounts", account_id=account_id)
            accountinfo.deposit += amount
            accountinfo.fund_shares += amount / accountinfo.fund_nav_yd
            accountinfo.balance = cash.marketvalue
            accountinfo.frozen = cash.frozen

            session.save("transferinfos", transferinfo)
            session.save("positions", cash)
            session.save("accounts", accountinfo)

        return transferinfo

    def withdraw(
        self, account_id: str, amount: float, transfer_dt: DateTimeType = None
    ) -> vxTransferInfo:
        """转出资金

        Arguments:
            account_id {str} -- 账户ID
            amount {float} -- 转出金额
            transfer_dt {DateTimeType} -- 转出时间 (default: {None})

        Returns:
            vxTransferInfo -- 转账信息
        """
        if amount < 0:
            raise ValueError(f"转出金额({amount})应大于0 .")

        with self._db.start_session() as session:
            cash = session.findone(
                "positions",
                account_id=account_id,
                symbol="CNY",
            )
            if cash.available < amount:
                raise NoEnoughCash("可用资金不足")

            cash = vxCashPosition(**cash.message)
            cash = sub_volume(cash, amount)

            # 转账交易记录
            transfer_dt = to_timestamp(transfer_dt or vxtime.now())
            transferinfo = vxTransferInfo(
                account_id=account_id,
                amount=amount,
                transfer_direction="Out",
                created_dt=transfer_dt,
            )

            accountinfo = session.findone("accounts", account_id=account_id)
            accountinfo.withdraw += amount
            accountinfo.fund_shares -= amount / accountinfo.fund_nav_yd
            accountinfo.balance = cash.marketvalue
            accountinfo.frozen = cash.frozen

            session.save("transferinfos", transferinfo)
            session.save("positions", cash)
            session.save("accounts", accountinfo)

        return transferinfo

    def get_accounts(
        self, account_id: str = None
    ) -> Union[vxAccountInfo, Dict[str, vxAccountInfo]]:
        """查询子账户信息

        Arguments:
            account_id {str} -- 账户ID,如果为None则返回所有账户信息

        Returns:
            Union[vxAccountInfo, Dict[str, vxAccountInfo]] -- 账户信息
        """
        with self._db.start_session() as session:
            return (
                session.findone(
                    "accounts", account_id=account_id, settle_date=self._db.settle_date
                )
                if account_id
                else list(session.find("accounts", settle_date=self._db.settle_date))
            )

    def get_positions(
        self, account_id: str, symbol: str = None
    ) -> Dict[str, vxPositionType]:
        """获取账户持仓

        Arguments:
            account_id {str} -- 账户ID
            symbol {str} -- 持仓证券symbol，若为None，则返回全部持仓 (default: {None})

        Returns:
            Dict[str, vxPositionType] -- 持仓信息
        """
        with self._db.start_session() as session:
            if symbol:
                pos = session.findone(
                    "positions",
                    account_id=account_id,
                    symbol=symbol,
                    settle_date=self._db.settle_date,
                )
                return vxCashPosition(pos.message) if symbol == "CNY" else pos

            positions = {}
            for p in session.find(
                "positions", account_id=account_id, settle_date=self._db.settle_date
            ):
                if p.symbol == "CNY":
                    p = vxCashPosition(p.message)
                positions[p.symbol] = p

            return positions

    def get_orders(
        self,
        account_id: str,
        order_id: str = None,
        exchange_order_id: str = None,
        filter_finished=False,
    ) -> Dict[str, vxOrder]:
        """查询订单信息

        Arguments:
            account_id {str} -- 账户ID
            order_id {str} -- 委托订单号 (default: {None})
            exchange_order_id {str} -- 交易所委托订单号 (default: {None})
            filter_finished {bool} -- 是否过滤已完成的订单 (default: {False})

        Returns:
            Dict[str, vxOrder] -- 委托订单
        """
        query = {"account_id": account_id}
        if order_id:
            query["order_id"] = order_id

        if exchange_order_id:
            query["exchange_order_id"] = exchange_order_id

        condisiotns = [
            f"""created_dt > {vxtime.today()}""",
            f"""created_dt < {self._db.settle_date} """,
        ]
        if filter_finished:
            condisiotns.append("""status in ("New", "PendingNew", "PartiallyFilled")""")

        with self._db.start_session() as session:
            cur = session.find("orders", *condisiotns, **query)
            return {o.exchange_order_id: o for o in cur}

    def get_execution_reports(
        self,
        account_id: str,
        trade_id: str = None,
        order_id: str = None,
        exchange_order_id: str = None,
    ) -> Dict[str, vxTrade]:
        """查询成交信息

        Arguments:
            account_id {str} -- 账户ID

        Returns:
            Dict[str, vxTrade] -- 成交回报
        """
        query = {"account_id": account_id}
        conditions = [
            f"""created_dt > {vxtime.today()}""",
            f"""created_dt < {self._db.settle_date} """,
        ]
        if trade_id:
            query["trade_id"] = trade_id
        if order_id:
            query["order_id"] = order_id
        if exchange_order_id:
            query["exchange_order_id"] = exchange_order_id
        with self._db.start_session() as session:
            cur = session.find("trades", *conditions, **query)
            return {t.trade_id: t for t in cur}

    def get_transferinfos(self, account_id: str) -> Dict[str, vxTransferInfo]:
        """查询资金流水

        Arguments:
            account_id {str} -- 账户ID

        Returns:
            Dict[str, vxTransferInfo] -- 资金流水
        """
        with self._db.start_session() as session:
            cur = session.find(
                "transferinfos",
                f"created_dt > {vxtime.now()}",
                f"created_dt < {self._db.settle_date}",
                account_id=account_id,
            )
            return {t.transfer_id: t for t in cur}

    def order_volume(
        self, account_id: str, symbol: str, volume: float, price: float = None
    ) -> vxOrder:
        """委托下单

        Arguments:
            account_id {str} -- 账户ID
            symbol {str} -- 证券代码
            volume {float} -- 委托数量，正数为买入，负数为卖出
            price {float} -- 委托价格,若price为None，则通过市价委托下单 (default: {None})

        Returns:
            vxOrder -- 下单的信息
        """
        if volume == 0:
            raise ValueError("volume can't be 0.")

        accountinfo = self._db.findone("accounts", account_id=account_id)

        if accountinfo is None:
            raise ValueError(f"account {account_id} not found.")

        if accountinfo.channel not in self._channels:
            raise ValueError(f"channel {accountinfo.channel} not found.")

        tradeapi = self._channels[accountinfo.channel]

        order_type = OrderType.Limit
        if not price:
            ticks = tradeapi.current(symbol)
            price = ticks[symbol].ask1_p if volume > 0 else ticks[symbol].bid1_p
            order_type = (
                OrderType.Limit
                if vxMarketPreset(symbol).security_type == SecType.BOND_CONVERTIBLE
                else OrderType.Market
            )

        vxorder = vxOrder(
            account_id=account_id,
            symbol=symbol,
            volume=abs(volume),
            price=price,
            order_offset="Open" if volume > 0 else "Close",
            order_direction="Buy" if volume > 0 else "Sell",
            order_type=order_type,
            status="PendingNew",
        )
        with self._db.start_session() as session:
            frozen_symbol = symbol if volume < 0 else "CNY"
            frozen_volume = abs(volume) if volume < 0 else price * volume * 1.003
            position = session.findone(
                "positions",
                f"available >= {frozen_volume}",
                account_id=vxorder.account_id,
                symbol=frozen_symbol,
            )
            if not position:
                raise (
                    NoEnoughCash(f"可用资金不足，需要冻结资金{frozen_volume:,.2f}元")
                    if frozen_symbol == "CNY"
                    else NoEnoughPosition(
                        f"{symbol}持仓可用持仓不足,冻结仓位{frozen_volume:,.2f}"
                    )
                )

            ret_orders = tradeapi.order_batch(vxorder)
            session.save("orders", ret_orders[0])
            if ret_orders[0].order_direction == OrderDirection.Buy:
                session.update_cash_position_frozens(account_ids=[account_id])
            else:
                session.update_symbol_position_frozens(account_ids=[account_id])
            session.update_accountinfos([account_id])
            logger.info(
                f"[新增] 委托订单: {ret_orders[0].exchange_order_id} : {ret_orders[0]}"
            )

        return ret_orders[0]

    def order_cancel(self, order: vxOrder) -> None:
        """撤单

        Arguments:
            *orders {List[str]} -- 订单号
        """
        accountinfo = self._db.findone("accounts", account_id=order.account_id)

        if accountinfo is None:
            raise ValueError(f"account {order.account_id} not found.")

        if accountinfo.channel not in self._channels:
            raise ValueError(f"channel {accountinfo.channel} not found.")

        tradeapi = self._channels[accountinfo.channel]
        tradeapi.order_cancel(order)

    def on_tick(self, context: vxContext, event: vxEvent) -> None:
        "更新行情事件"
        symbols = self._db.distinct("positions", "symbol", "symbol != 'CNY'")
        vxticks = self._mdapi.current(*symbols)
        with self._db.start_session() as session:
            session.update_position_lasttrades(list(vxticks.values()))

    # * def on_broker_order_status(self, context: vxContext, event: vxEvent) -> None:
    # *     "更新订单状态事件"
    # *     broker_order = event.data
    # *     if not isinstance(broker_order, vxOrder):
    # *         logger.error(f"broker_order {broker_order} is not a vxOrder instance.")
    # *         return

    # *     with self._db.start_session() as session:
    # *         vxorder = session.update_order(broker_order)

    # *     if self._sched and vxorder:
    # *         self._sched.submit_event("on_order_status", vxorder)

    # * def on_broker_execution_report(self, context: vxContext, event: vxEvent) -> None:
    # *     "更新成交回报事件"
    # *     broker_trade = event.data
    # *     if not isinstance(broker_trade, vxTrade):
    # *         logger.error(f"broker_trade {broker_trade} is not a vxTrade instance.")
    # *         return

    # *     with self._db.start_session() as session:
    # *         vxtrade = session.update_trade(broker_trade)

    # *     if self._sched and vxtrade:
    # *         self._sched.submit_event("on_execution_report", vxtrade)

    def after_close(self, context: vxContext, event: vxEvent) -> None:
        "收盘后事件"
        with self._db.start_session() as session:
            for channel_name, tdapi in self._channels.items():
                broker_account = tdapi.get_account()
                broker_positions = tdapi.get_positions()
                broker_orders = tdapi.get_orders()
                broker_trades = tdapi.get_execution_reports()
                try:
                    session.sync_with_broker(
                        broker_account, broker_positions, broker_orders, broker_trades
                    )
                    logger.info(f"channel({channel_name})同步账户信息成功")
                except Exception as e:
                    logger.warning(f"channel({channel_name})同步账户信息失败: {e}")

            for order in session.find(
                "orders", "status in ('PendingNew','New','PartiallyFilled')"
            ):
                order.status = "Expired"
                session.update_order(order)

            session.update_cash_position_frozens([])
            session.update_symbol_position_frozens([])
            session.update_accountinfos([])
            logger.info("所有未终结order状态更新为Expired")
        self._sched.stop()

    def day_begin(self, context: vxContext, event: vxEvent) -> None:
        """开盘前准备事件"""

        if vxtime.is_holiday():
            logger.info("今天是节假日，不进行交易")
            return

        with self._db.start_session() as session:
            session.update_settle_date(vxtime.today("23:59:59"))

        if vxtime.now() < vxtime.today("09:00:00"):
            self._sched.submit_event(
                "on_tick",
                trigger=vxIntervalTrigger(
                    1,
                    start_dt=vxtime.today("09:30:00"),
                    end_dt=vxtime.today("11:30:00"),
                ),
            )
            self._sched.submit_event(
                "before_trade", trigger=vxOnceTrigger(vxtime.today("09:15:00"))
            )
            self._sched.submit_event(
                "on_trade", trigger=vxOnceTrigger(vxtime.today("09:30:00"))
            )

        if vxtime.now() < vxtime.today("11:30:00"):
            self._sched.submit_event(
                "noon_break_start", trigger=vxOnceTrigger(vxtime.today("11:30:00"))
            )

        if vxtime.now() < vxtime.today("13:00:00"):
            self._sched.submit_event(
                "noon_break_end", trigger=vxOnceTrigger(vxtime.today("13:00:00"))
            )
            self._sched.submit_event(
                "on_tick",
                trigger=vxIntervalTrigger(
                    1,
                    start_dt=vxtime.today("13:00:00"),
                    end_dt=vxtime.today("15:30:00"),
                ),
            )

        if vxtime.now() < vxtime.today("15:00:00"):
            self._sched.submit_event(
                "before_close",
                trigger=vxOnceTrigger(vxtime.today("14:45:00")),
            )
            self._sched.submit_event(
                "on_trade",
                trigger=vxOnceTrigger(vxtime.today("14:55:00")),
            )
            self._sched.submit_event(
                "after_close", trigger=vxOnceTrigger(vxtime.today("15:30:00"))
            )

    def register_scheduler(self, sched: vxScheduler):
        sched.register("on_tick", handler=self.on_tick)
        # sched.register("on_broker_order_status", handler=self.on_broker_order_status)
        # sched.register(
        #    "on_broker_execution_report", handler=self.on_broker_execution_report
        # )
        sched.register("after_close", handler=self.after_close)
        sched.register("before_day", handler=self.day_begin)
        if vxtime.now() < vxtime.today("15:00:00"):
            sched.submit_event("day_begin", trigger=vxOnceTrigger(vxtime.today()))
        self._sched = sched


if __name__ == "__main__":
    db_config = {
        "class": "vxquant.accountdb.sqlitedb.vxSQLiteAccountDB",
        "params": {"db_uri": "dist/vxquant.db"},
    }
    teller = vxTeller(db_config)
    teller.create_account("test", "test", 1000000, if_exists="delete")
    accountinfos = teller.get_accounts("test")
    print(accountinfos)
    positions = teller.get_positions("test")
    print(positions)
    t = teller.get_transferinfos("test")
    print(t)
    order = teller.order_volume("test", "SHSE.600000", 100, 10.3)
    print(order)
    exit(0)
    # tdapi.create_account(
    #    "test", init_balance=1000000, created_dt="2021-01-01", if_exists="delete"
    # )
    # tdapi.deposit("test", 10000, "2021-01-02")
    # print("转入1万元后: ", tdapi._db.findone("accounts", account_id="test"))
    # print("账户现金: ", tdapi._db.findone("positions", account_id="test", symbol="CNY"))
    # tdapi.withdraw("test", 10000, "2021-01-02")
    # print("转出1万元后: ", tdapi._db.findone("accounts", account_id="test"))
    # print("账户现金: ", tdapi._db.findone("positions", account_id="test", symbol="CNY"))

    # logger.info("=" * 60)
    # for p in tdapi._db.find("transferinfos"):
    #    print(p)
    accountinfo = tdapi.get_account(account_id="test")
    # print(accountinfo)
    positions = tdapi.get_positions(account_id="test")
    for symbol, p in positions.items():
        print(symbol, type(p), p.volume)

    orders = tdapi.get_orders(account_id="test", filter_finished=True)
    print(orders)
    trades = tdapi.get_trades(account_id="test")
    print(trades)
    transferinfos = tdapi.get_transferinfos(account_id="test")
    # print(transferinfos, len(transferinfos))
    order1 = tdapi.order_volume(account_id="test", symbol="SHSE.600000", volume=10000)

    # order2 = tdapi.order_volume(account_id="test", symbol="SHSE.600036", volume=1000)
    orders = tdapi.get_orders(account_id="test", filter_finished=True)
    assert order1.order_id in orders
    print(f"{order1.order_id} 在orders列表中")
    logger.info("=" * 60)
    trade1 = vxTrade(
        account_id="helloworld",
        order_id="other_order_id",
        exchange_order_id=order1.exchange_order_id,
        order_direction=order1.order_direction,
        order_offset=order1.order_offset,
        symbol=order1.symbol,
        volume=order1.volume - 1000,
        price=order1.price - 0.01,
        commission=194.13,
        status="Trade",
    )
    print(trade1)
    context = vxContext()
    event1 = vxEvent("on_broker_execution_report", data=trade1)
    tdapi.on_broker_execution_report(context, event1)
    # positions = tdapi.get_positions(account_id="test")
    # print(positions)
    order1.filled_volume = trade1.volume
    order1.filled_amount += trade1.price * trade1.volume + trade1.commission

    order1.status = OrderStatus.PartiallyFilled
    event2 = vxEvent("on_broker_order_status", data=order1)

    tdapi.on_broker_order_status(context, event2)
    # frozen = 0
    # for i in orders.values():
    #    frozen += i.price * i.volume * 1.003
    #    print(i.price, i.volume, i.filled_volume)
    # print(frozen)
    positions = tdapi.get_positions(account_id="test")
    for symbol, position in positions.items():
        print(symbol, position)

    accountinfo = tdapi.get_account(account_id="test")
    print("accountinfo = ", accountinfo)
    tdapi.after_close(context, event1)
    event1.data = None
    tdapi.on_settle(context, event1)

    # cur = tdapi._db.get_connection().execute(
    #    """select * from orders where account_id='test' and status in ('OrderStatus.PendingNew');"""
    # )
    # for i in cur:
    #    print(i)
