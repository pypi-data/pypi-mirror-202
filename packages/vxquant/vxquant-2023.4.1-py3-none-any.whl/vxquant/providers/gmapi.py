"""掘金量化tick行情数据"""

import polars as pl
from tqdm import tqdm
from typing import List, Dict, Union, Any
from vxquant.providers.base import ProviderContext
from vxquant.providers.base import (
    vxHQProvider,
    vxGetAccountProvider,
    vxGetExecutionReportsProvider,
    vxGetOrdersProvider,
    vxGetPositionsProvider,
    vxOrderBatchProvider,
    vxOrderCancelProvider,
    vxDownloadInstrumentsProvider,
    vxUpdateInstruments,
    vxCalendarProvider,
)
from vxquant.model.tools.gmData import (
    gmTickConvter,
    gmAccountinfoConvter,
    gmCashPositionConvter,
    gmOrderConvter,
    gmPositionConvter,
    gmTradeConvter,
)
from vxquant.model.exchange import (
    vxTick,
    vxAccountInfo,
    vxCashPosition,
    vxPosition,
    vxOrder,
    vxTrade,
)
from vxquant.model.instruments import vxInstruments
from vxquant.model.typehint import InstrumentType
from vxsched import vxContext
from vxutils import to_timestring, vxtime, logger, to_datetime

try:
    from gm import api as gm_api

except ImportError as e:
    raise ImportError("掘金量化库并未安装，请使用pip install gm 安装") from e


def init_provider_context(
    context: vxContext, gm_token: str = "", gm_strategyid: str = ""
):
    if gm_token:
        gm_api.set_token(gm_token)

    context.gmcontext.accountdb = context.accountdb
    context.gmcontext.scheduler = context.scheduler
    context.gm_strategyid = gm_strategyid
    context.gm_token = gm_token

    return context


class vxGMHQProvider(vxHQProvider):
    _BATCH_SIZE = 100

    def _hq(self, *symbols: List[InstrumentType]) -> Dict[InstrumentType, vxTick]:
        allticks = []
        for i in range(0, len(symbols), self._BATCH_SIZE):
            gmticks = gm_api.current(symbols=symbols[i : i + self._BATCH_SIZE])
            allticks.extend(gmticks)

        return dict(map(lambda gmtick: gmTickConvter(gmtick, key="symbol"), gmticks))


class vxGMDownloadStockInstrumentsProvider(vxDownloadInstrumentsProvider):
    def __call__(self, *instrument_names: List[str]) -> None:
        return super().__call__(*instrument_names)

    def get_cnstocks(self) -> List[vxInstruments]:
        """获取所有股票列表"""
        logger.info("开始获取所有股票列表")
        datas = gm_api.get_instruments(
            symbols=None,
            exchanges=["SHSE", "SZSE"],
            sec_types=gm_api.SEC_TYPE_STOCK,
            skip_suspended=False,
            skip_st=False,
            fields=",".join(["symbol", "listed_date", "delisted_date"]),
            df=False,
        )
        cnstocks = vxInstruments("cnstocks")
        for data in datas:
            cnstocks.add_instrument(
                symbol=data["symbol"],
                start_date=data["listed_date"],
                end_date=data["delisted_date"],
            )

        pbar = tqdm(
            gm_api.get_trading_dates(
                "SHSE", "2005-01-01", f"""{to_timestring(vxtime.now(),"%Y")}-12-31"""
            )
        )
        st_stocks = vxInstruments("st_stocks")
        suspended_stocks = vxInstruments("suspended_stocks")

        for trade_date in pbar:
            """处理 {trade_date} 的股票"""
            pbar.set_description(f"处理 {trade_date} 的股票")
            symbols = cnstocks.list_instruments(trade_date)
            df = pl.from_pandas(
                gm_api.get_history_instruments(
                    symbols, start_date=trade_date, end_date=trade_date, df=True
                )
            )
            if len(symbols) != df.shape[0]:
                logger.warning(
                    f"需要下载的symbols{len(symbols)}个，实际下载: {df.shape[0]}"
                )

            if df.is_empty():
                logger.warning(f"{trade_date} 没有获取相应数据")
                continue
            st_symbols = df.filter(pl.col("sec_level").is_in([2, 3]))["symbol"]
            if not st_symbols.is_empty():
                st_stocks.update_components(
                    {symbol: 1.0 for symbol in st_symbols}, trade_date
                )

            suspended_symbols = df.filter(pl.col("is_suspended") == 1)["symbol"]
            if not suspended_symbols.is_empty():
                suspended_stocks.update_components(
                    {symbol: 1.0 for symbol in suspended_symbols}, trade_date
                )

        return [cnstocks, st_stocks, suspended_stocks]

    def get_cbonds(self) -> vxInstruments:
        """下载全量可转债成分数据

        Returns:
            vxInstruments -- 'cbonds' 股票池
        """
        datas = gm_api.get_instruments(
            symbols=None,
            exchanges=["SHSE", "SZSE"],
            sec_types=gm_api.SEC_TYPE_BOND_CONVERTIBLE,
            skip_suspended=False,
            skip_st=False,
            fields=",".join(["symbol", "listed_date", "delisted_date"]),
            df=False,
        )
        cncbonds = vxInstruments("cncbonds")
        for data in datas:
            cncbonds.add_instrument(
                symbol=data["symbol"],
                start_date=data["listed_date"],
                end_date=data["delisted_date"],
            )

        pbar = tqdm(
            gm_api.get_trading_dates(
                "SHSE", "2005-01-01", f"""{to_timestring(vxtime.now(),"%Y")}-12-31"""
            )
        )
        st_cbonds = vxInstruments("st_cbonds")
        suspended_cbonds = vxInstruments("suspended_cbonds")
        for trade_date in pbar:
            pbar.set_description(f"处理 {trade_date} 的可转债")
            symbols = cncbonds.list_instruments(trade_date)
            df = pl.from_pandas(
                gm_api.get_history_instruments(
                    symbols, start_date=trade_date, end_date=trade_date, df=True
                )
            )
            st_symbols = df.filter(pl.col("sec_level").is_in(2, 3))["symbol"]
            if not st_symbols.is_empty():
                st_cbonds.update_components(
                    {symbol: 1.0 for symbol in st_symbols}, trade_date
                )

            suspended_symbols = df.filter(pl.col("is_suspended") == 1)["symbol"]
            if not suspended_symbols.is_empty():
                suspended_cbonds.update_components(
                    {symbol: 1.0 for symbol in suspended_symbols}, trade_date
                )
        return [cncbonds, st_cbonds, suspended_cbonds]

    def get_indexs(self) -> vxInstruments:
        """所有指数代码数据

        Returns:
            vxInstruments -- 'cnindexs' 股票池
        """
        datas = gm_api.get_instruments(
            symbols=None,
            exchanges=["SHSE", "SZSE"],
            sec_types=gm_api.SEC_TYPE_INDEX,
            skip_suspended=False,
            skip_st=False,
            fields=",".join(["symbol", "listed_date", "delisted_date"]),
            df=False,
        )
        cnindexes = vxInstruments("cnindexes")
        for data in datas:
            cnindexes.add_instrument(
                symbol=data["symbol"],
                start_date=data["listed_date"],
                end_date=data["delisted_date"],
            )
        return [cnindexes]

    def get_industry(self, industry_names: List[str] = None) -> List[vxInstruments]:
        """获取申万行业成分股

        Arguments:
            industry_names {List[str]} -- 行业名称 {default: None} 当前为None时，全部行业成分股数据

        Returns:
            List[vxInstruments] -- 行业成分股
        """

    def get_index_constituents(
        self, index_symbols: List[str] = None
    ) -> List[vxInstruments]:
        """获取指数的成分股

        Keyword Arguments:
            index_symbols {List[str]} -- 指数代码,若为None时,获取: ['SHSE.000300','SHSE.000905','SHSE.000852'] (default: {None})

        Returns:
            List[vxInstruments] -- 指数成分股
        """
        if not index_symbols:
            index_symbols = ["SHSE.000300", "SHSE.000905", "SHSE.000852"]
        index_constituents = {
            index_symbol: vxInstruments(index_symbol) for index_symbol in index_symbols
        }

        last_year = to_datetime(vxtime.now()).year
        for year in range(2005, last_year + 1):
            for index_symbol in index_symbols:
                datas = gm_api.get_history_constituents(
                    index_symbol, f"{year}-01-01", f"{year}-12-31"
                )
                for data in datas:
                    index_constituents[index_symbol].update_components(
                        data["constuents"], data["trade_date"]
                    )
        return list(index_constituents.values())


class vxGMUpdateInstruments(vxUpdateInstruments):
    pass


class vxGMCalendarProvider(vxCalendarProvider):
    def get_trade_dates(self, market: str = "cn") -> List[InstrumentType]:
        return gm_api.get_trading_dates(
            "SHSE", "2005-01-01", f"""{to_timestring(vxtime.now(),"%Y")}-12-31"""
        )


class vxGMGetAccountProvider(vxGetAccountProvider):
    def __call__(self, account_id: str = None) -> vxAccountInfo:
        gmcash = self.context["gmcontext"].account(account_id).cash
        return gmAccountinfoConvter(gmcash)


class vxGMGetCreditAccountProvider(vxGetAccountProvider):
    def __call__(self, account_id: str = None) -> vxAccountInfo:
        gmcash = self.context["gmcontext"].account(account_id).cash
        return gmAccountinfoConvter(gmcash)


class vxGMGetPositionsProvider(vxGetPositionsProvider):
    def __call__(
        self, symbol: InstrumentType = None, account_id: str = None
    ) -> Dict[InstrumentType, Union[vxPosition, vxCashPosition]]:
        if symbol and symbol == "CNY":
            gmcash = self.context["gmcontext"].account(account_id).cash
            return {"CNY": gmCashPositionConvter(gmcash)}
        elif symbol:
            gmposition = (
                self.context["gmcontext"].account(account_id).position(symbol, 1)
            )
            return {symbol: gmPositionConvter(gmposition)} if gmposition else None

        gmcash = self.context["gmcontext"].account(account_id).cash
        vxpositions = {"CNY": gmCashPositionConvter(gmcash)}
        gmpositions = self.context["gmcontext"].account().positions()
        vxpositions.update(
            map(
                lambda gmposition: gmPositionConvter(gmposition, key="symbol"),
                gmpositions,
            )
        )

        return vxpositions


class vxGMGetOrdersProvider(vxGetOrdersProvider):
    def __call__(
        self, account_id: str = None, filter_finished: bool = False
    ) -> Dict[str, vxOrder]:
        gmorders = (
            gm_api.get_unfinished_orders() if filter_finished else gm_api.get_orders()
        )
        return dict(
            map(
                lambda gmorder: gmOrderConvter(gmorder, key="exchange_order_id"),
                gmorders,
            )
        )


class vxGMGetExecutionReportsProvider(vxGetExecutionReportsProvider):
    def __call__(
        self, account_id: str = None, order_id: str = None, trade_id: str = None
    ) -> Dict[str, vxTrade]:
        gmtrades = gm_api.get_execution_reports()
        if order_id:
            gmtrades = [
                gmtrade for gmtrade in gmtrades if gmtrade.cl_ord_id == order_id
            ]

        if trade_id:
            gmtrades = [gmtrade for gmtrade in gmtrades if gmtrade.exec_id == trade_id]

        return dict(
            map(lambda gmtrade: gmTradeConvter(gmtrade, key="trade_id"), gmtrades)
        )


class vxGMOrderBatchProvider(vxOrderBatchProvider):
    def __call__(self, *vxorders) -> List[vxOrder]:
        if len(vxorders) == 1 and isinstance(vxorders[0], list):
            vxorders = vxorders[0]

        gmorders = gm_api.order_batch(
            [
                {
                    "symbol": vxorder.symbol,
                    "volume": vxorder.volume,
                    "price": vxorder.price,
                    "side": vxorder.order_direction.value,
                    "order_type": vxorder.order_type.value,
                    "position_effect": vxorder.order_offset.value,
                    "order_business": gm_api.OrderBusiness_NORMAL,
                    "position_src": gm_api.PositionSrc_L1,
                }
                for vxorder in vxorders
            ]
        )
        for vxorder, gmorder in zip(vxorders, gmorders):
            vxorder.exchange_order_id = gmorder.cl_ord_id
            if not vxorder.account_id:
                vxorder.account_id = gmorder.account_id
        return vxorders


class vxGMCreditOrderBatchProvider(vxOrderBatchProvider):
    def __call__(self, *vxorders) -> List[vxOrder]:
        raise NotImplementedError


class vxGMOrderCancelProvider(vxOrderCancelProvider):
    def __call__(self, *vxorders) -> None:
        if len(vxorders) == 1 and isinstance(vxorders[0], list):
            vxorders = vxorders[0]

        wait_cancel_orders = [
            {"cl_ord_id": vxorder.exchange_order_id, "account_id": ""}
            for vxorder in vxorders
            if vxorder.exchange_order_id
        ]
        return gm_api.order_cancel(wait_cancel_orders)
