"""配置文件"""
import sys
import json
import textwrap
import argparse
from typing import Union
from pathlib import Path

from concurrent.futures import ThreadPoolExecutor as Executor
from vxsched import vxContext
from vxsched.core import vxscheduler
from vxutils import vxLRUCache, logger, DiskCacheUnit
from vxquant.apis import vxMdAPI, vxTdAPI
from vxquant.cli import vxCommand

_cache_path = Path.home().joinpath(".vxcache").absolute()

_default_config = {
    "params": {},
    "providers": {
        "mdapi": {},
        "tdapi": {},
    },
    "settings": {"modules": [], "cache_dir": _cache_path},
}


def run_quant(
    config_file: Union[str, Path] = "etc/config.json",
    mod_path: Union[str, Path] = "mod",
):
    try:
        with open(config_file, "r") as fp:
            kwargs = json.load(fp)
    except OSError:
        kwargs = {}
    logger.debug(f"加载配置文件: {kwargs},默认值: {_default_config}")
    context = vxContext(_default_config, **kwargs)

    context.memcache = vxLRUCache()
    logger.info(f"初始化内存缓存完成: {context.memcache}")

    cache_dir = context.settings.get("cache_dir", _cache_path)
    DiskCacheUnit.set_cache_params(cache_dir)
    context.settings["cache_dir"] = cache_dir

    try:
        mdapi_settings = context.providers.mdapi.to_dict()
    except AttributeError:
        mdapi_settings = {}
    context.mdapi = vxMdAPI(**mdapi_settings)

    logger.info(f"初始化mdapi 完成.{context.mdapi}")

    try:
        tdapi_settings = context.providers.tdapi.to_dict()
    except AttributeError:
        tdapi_settings = {}
    context.tdapi = vxTdAPI(**tdapi_settings)
    logger.info(f"初始化tdapi 完成{context.tdapi}")
    logger.info(f"通过{config_file}初始化context完成.")

    for mod in context.settings.modules:
        vxscheduler.load_modules(mod)

    vxscheduler.load_modules(mod_path)

    try:
        vxscheduler.start(
            context, executor=Executor(thread_name_prefix="vxquant"), blocking=True
        )
    finally:
        _context = vxContext(_default_config)
        for key in ["params", "settings", "providers"]:
            _context[key] = context[key]

        # _context.save_json(config_file)
        logger.info(f"保存配置文件: {config_file}")


desc = """
vxquant是一个量化金融框架Python包，用于为个人提供实盘交易以及量化研究支持，使用户更加专注于交易策略的编写。
框架具有以下特点：
1. 支持多账户体系运行
2. 支持掘金量化实盘以及模拟盘
3. 支持miniQMT实盘以及模拟盘
本命令为vxquant框架命令行接口，本接口可方便执行以下命令.
"""


def main(args=None) -> int:
    if args is None:
        args = sys.argv[1:]
    if len(args) == 0:
        args = ["-h"]

    parser = argparse.ArgumentParser(
        prog="vxquant",
        usage="vxquant <command> [options]",
        description=textwrap.dedent(desc),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )

    parser.add_argument(
        "-v",
        "--version",
        help="显示vxquant版本",
        action="version",
        version="2023.3.1",
    )
    parser.add_argument("-h", "--help", help="显示当前帮助信息", action="help")
    sub_parser = parser.add_subparsers(metavar="命令列表", dest="cmd")

    for command in vxCommand.cmds.values():
        command.set_parser(sub_parser)

    args = parser.parse_args(args)
    command = vxCommand.cmds[args.cmd]
    command(args)

    # if args.verbose:
    #    logger.setLevel("DEBUG")

    # run_quant(config_file=args.config, mod_path=args.mod)


if __name__ == "__main__":
    main()
