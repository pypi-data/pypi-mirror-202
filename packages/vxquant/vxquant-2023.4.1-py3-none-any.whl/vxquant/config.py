"""配置文件"""
import json
from pathlib import Path
from typing import Union
from vxquant.apis import vxMdAPI, vxTdAPI, vxTeller
from vxsched import vxContext, vxscheduler
from vxutils import logger, vxWrapper


__default_config__ = {
    "custom_context": {},
    "init_privoder_context": {
        "class": "",
        "params": {},
    },
    "mdapi": {},
    "tdapi": {"channel": "default", "providers": {}},
    "accountdb": {
        "class": "vxquant.accountdb.sqlitedb.vxSQLiteAccountDB",
        "params": {"db_uri": "data/vxquant.db"},
        "accounts": [
            {
                "portfolio_id": "default",
                "account_id": "default",
                "init_balance": 1_000_000.00,
                "if_exists": "ignore",
                "channel": "default",
            },
        ],
    },
    "notify": {},
    "preset_events": {
        "before_trade": "09:15:00",
        "on_trade": "09:30:00",
        "noon_break_start": "11:30:00",
        "noon_break_end": "13:00:00",
        "before_close": "14:45:00",
        "on_close": "14:55:00",
        "after_close": "15:30:00",
        "on_settle": "16:30:00",
    },
}


class vxQuantConfig(vxContext):
    """vxQuant配置文件"""

    _default_config: dict = __default_config__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_json(
        self, config_file: Union[str, Path] = "etc/config.json", encoding="utf-8"
    ) -> None:
        """加载配置文件

        Keyword Arguments:
            config_file {Union[str,Path]} -- 配置文件路径 (default: {"etc/config.json"})

        Example:

            {
                "custom_context":{
                        "trader": "C:\\Program Files\\miniQMT\\",
                        ...
                },
                "mdapi": {
                    "current": {
                        "class": "vxquant.providers.miniqmt.vxMiniQMTHQProvider",
                        "params": {}
                    },
                    ...
                },
                "tdapi": {
                    "channel" :"channel_name1",

                    "providers":{
                        "current": {
                            "class": "vxquant.providers.miniqmt.vxMiniQMTHQProvider",
                            "params": {}
                        },
                        "order_batch": {
                            "class":"vxquant.providers.miniqmt.vxMiniQMTOrderBatchProvider",
                            "params": {}
                        },
                        ...
                    }
                },
                "accountdb": {
                    "class": "vxquant.accountdb.sqlitedb.vxSQLiteAccountDB",
                    "params": {"db_uri": "data/vxquant.db"},
                    "accounts": [
                        {
                            "portfolio_id": "default",
                            "account_id": "default",
                            "init_balance": 4000000,
                            "if_exists": "ignore",
                            "channel": "default",
                        },
                    ],
                },
                "notify": {},
                "cachedb": "~/.data/vxcache.db"
            }

        """
        try:
            with open(config_file, "r", encoding=encoding) as fp:
                kwargs = json.load(fp)
        except OSError:
            kwargs = {}

        self.update(kwargs)
        logger.info(f"通过{config_file}初始化context完成.")

    def create_context(self, **kwargs) -> vxContext:
        """创建context"""

        context = vxContext(kwargs)

        if "accountdb" not in kwargs:
            try:
                context.accountdb = vxWrapper.init_by_config(self.accountdb.to_dict())
                logger.info(f"初始化账户数据库: {context.accountdb}")
            except Exception as e:
                logger.error(f"初始化账户数据库失败: {e}")
                context.accountdb = None

        if "scheduler" not in kwargs:
            context.scheduler = vxscheduler

        for mod_name, mod_config in self.custom_context.items():
            try:
                context[mod_name] = vxWrapper.init_by_config(mod_config.to_dict())
                logger.info(f"初始化{mod_name}: {kwargs[mod_name]}")
            except Exception as e:
                logger.error(f"初始化{mod_name}失败: {e}")

        if "init_privoder_context" in self.keys():
            init_func = vxWrapper.init_by_config(self.init_privoder_context.to_dict())
            context = init_func(context=context, **self.init_privoder_context.params)

        if "mdapi" in self.keys():
            try:
                context.mdapi = vxMdAPI(**self.mdapi.to_dict())
                context.mdapi.set_context(context)
                vxticks = context.mdapi.current("SHSE.000300")
                logger.info(
                    f"测试实时行情接口: {'SHSE.000300'} --"
                    f" {vxticks['SHSE.000300'].lasttrade:,.2f}"
                )
                cal = context.mdapi.calender(start_date="2005-01-01")

            except Exception as e:
                logger.error(f"初始化行情接口失败: {e}")
                context.mdapi = vxMdAPI()
                logger.info(f"使用默认行情接口: {context.mdapi}")

        if "tdapi" in self.keys():
            try:
                context.tdapi = vxTdAPI(**self.tdapi.providers.to_dict())
                context.tdapi.set_context(context)
                accountinfo = context.tdapi.get_account()
                logger.info(
                    f"测试交易接口:{accountinfo.account_id} 账户余额:"
                    f" {accountinfo.nav:,.2f}元)"
                )

                context.teller = vxTeller(
                    mdapi=context.mdapi, accountdb=context.accountdb
                )
                context.teller.register_scheduler(vxscheduler)
                context.teller.add_channel(self.tdapi.channel, context.tdapi)
            except Exception as e:
                logger.error(f"初始化交易接口失败: {e}")
                context.tdapi = None
                context.teller = None

        try:
            if context.teller:
                for account_config in self.accountdb.accounts:
                    context.teller.create_account(**account_config.to_dict())
                    logger.info(
                        f"{account_config.portfolio_id} 创建账户:"
                        f" {account_config.account_id} 通道: {account_config.channel}"
                    )
            else:
                logger.warning(f"没有交易接口,不创建账户.")
        except Exception as e:
            logger.error(f"初始化账户失败: {e},账户配置: {self.accountdb.accounts}")

        return context


vxQCONFIG = vxQuantConfig()


if __name__ == "__main__":
    vxQCONFIG.load_json()
    context = vxQCONFIG.create_context()
    print(context.mdapi.current("SHSE.000300"))
    print(context.mdapi.calendar(start_date="2020-01-01", end_date="2023-01-31"))
