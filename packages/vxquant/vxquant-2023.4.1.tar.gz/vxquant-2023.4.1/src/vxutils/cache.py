"""缓存

支持

"""

import pickle
import inspect
import hashlib
from pathlib import Path
from collections import OrderedDict
from typing import Any, Dict, Type, Union, Callable, List
from vxutils import vxtime, to_timestring, to_timestamp, to_json, logger


__all__ = ["MissingCache", "CacheUnit", "DiskCacheUnit", "vxLRUCache", "vxSQLiteCache"]
_ENDOFTIME = to_timestamp("2199-12-31 23:59:59")


class MissingCache(Exception):
    pass


class CacheUnit:
    _key = None
    _value = None
    _expired_dt = _ENDOFTIME

    def __init__(self, key: str, value: Any, expired_dt: float = None) -> None:
        self._key = key
        self._value = value
        self._expired_dt = to_timestamp(expired_dt or _ENDOFTIME)

    @property
    def key(self) -> str:
        return self._key

    @property
    def value(self) -> Any:
        return self._value

    @property
    def expired_dt(self) -> float:
        return self._expired_dt

    @property
    def size(self) -> float:
        return 1

    @property
    def is_expired(self) -> float:
        return self._expired_dt < vxtime.now()

    def __str__(self) -> str:
        return (
            f"< {self.__class__.__name__} key: {self._key} _value:"
            f" {self._value} has expired >"
            if self.is_expired
            else (
                f"< {self.__class__.__name__} key: {self._key} _value:"
                f" {self._value} will expired at: {to_timestring(self.expired_dt)} > "
            )
        )

    __repr__ = __str__

    def __getstate__(self) -> Dict:
        return {"key": self.key, "value": self.value, "expired_dt": self.expired_dt}

    def __setstate(self, state: Dict) -> None:
        self.__init__(**state)

    @classmethod
    def set_cache_params(cls, *args, **kwargs) -> None:
        pass

    @classmethod
    def init_cache(cls) -> OrderedDict:
        return OrderedDict()

    def clear(self) -> None:
        del self._value

    def __lt__(self, other: "CacheUnit") -> bool:
        return (self.expired_dt, self._value) > (other.expired_dt, other._value)

    def __gt__(self, other: "CacheUnit") -> bool:
        return (self.expired_dt, self._value) < (other.expired_dt, other._value)

    def __eq__(self, other: "CacheUnit") -> bool:
        return (self.expired_dt, self._value) == (other.expired_dt, other._value)

    def __hash__(self) -> int:
        return hash((self._value, self._expired_dt))


class DiskCacheUnit(CacheUnit):
    _path = Path.home().joinpath(".vxcache").absolute()

    def __init__(self, key: str, value: Any, expired_dt: float = 0) -> None:
        value_file = Path(self._path, f"{key}.dat")
        super().__init__(key, value_file.absolute(), expired_dt)
        self.value = value

    @property
    def value(self) -> Any:
        with open(self._value, "rb") as f:
            cache_obj = pickle.load(f)
            return cache_obj["value"]

    @value.setter
    def value(self, value: Any) -> None:
        with open(self._value, "wb") as fp:
            pickle.dump(
                {"key": self.key, "value": value, "expired_dt": self._expired_dt}, fp
            )

    @property
    def size(self) -> float:
        return self._value.stat().st_size

    @classmethod
    def set_cache_params(cls, cache_dir: Union[str, Path]) -> None:
        cls._path = Path(cache_dir)
        cls._path.mkdir(parents=True, exist_ok=True)
        logger.info(f"设置换成目录为: {cls._path}")

    @classmethod
    def init_cache(cls) -> OrderedDict:
        if not Path(cls._path).exists():
            Path(cls._path).mkdir(parents=True, exist_ok=True)
            return OrderedDict()

        cache_objs = []
        for value_file in cls._path.glob("*.dat"):
            with open(value_file, "rb") as fp:
                cache_params = pickle.load(fp)

            if (
                isinstance(cache_params, dict)
                and cache_params["expired_dt"] > vxtime.now()
            ):
                cache_objs.append(cls(**cache_params))
            else:
                logger.warning(f"cache_params error: {value_file} 删除")
                Path(value_file).unlink()

        return OrderedDict(
            {cache_obj.key: cache_obj for cache_obj in sorted(cache_objs)}
        )

    def clear(self) -> None:
        self._value.unlink(missing_ok=True)


class vxLRUCache:
    """Cache"""

    def __init__(
        self,
        size_limit: float = 0,
        unit_factory: Type[CacheUnit] = None,
    ):
        # self._lock = Lock()
        self.size_limit = size_limit * 1000  # M
        self._size = 0
        self._unit_factory = unit_factory or CacheUnit
        self._storage = OrderedDict()

        for key, cache_obj in self._unit_factory.init_cache().items():
            self.__setitem__(key, cache_obj)

    @property
    def storage(self) -> Dict:
        return {
            key: cache_obj
            for key, cache_obj in self._storage.items()
            if not cache_obj.is_expired
        }

    def keys(self) -> List[str]:
        # with self._lock:
        return [
            key for key, cache_obj in self._storage.items() if not cache_obj.is_expired
        ]

    def set(self, key, value, ttl=0) -> None:
        expired_dt = vxtime.now() + ttl if ttl > 0 else _ENDOFTIME
        cache_obj = (
            value
            if isinstance(value, CacheUnit)
            else self._unit_factory(key, value, expired_dt)
        )

        # with self._lock:
        self._adjust_size(key, cache_obj)
        self._storage[key] = cache_obj
        self._storage.move_to_end(key)

        if self.limited:
            # pop the oldest items beyond size limit
            while self._size > self.size_limit:
                self.popitem(last=False)

    def get(self, key, default=None) -> Any:
        cache_obj = self._storage.get(key, None)
        if cache_obj is None or cache_obj.is_expired:
            return default
        self._storage.move_to_end(key)
        return cache_obj.value

    def __setitem__(self, key, value):
        cache_obj = (
            value
            if isinstance(value, CacheUnit)
            else self._unit_factory(key, value, _ENDOFTIME)
        )
        # precalculate the size after od.__setitem__
        # with self._lock:
        self._adjust_size(key, cache_obj)
        self._storage[key] = cache_obj
        self._storage.move_to_end(key)

        if self.limited:
            # pop the oldest items beyond size limit
            while self._size > self.size_limit:
                self.popitem(last=False)

    def __getitem__(self, key):
        # with self._lock:
        cache_obj = self._storage.get(key, None)
        if cache_obj is None or cache_obj.is_expired:
            raise MissingCache(key)
        self._storage.move_to_end(key)
        return cache_obj.value

    def __contains__(self, key):
        # with self._lock:
        return key in self._storage and self._storage[key].is_expired is False

    def __len__(self):
        # with self._lock:
        return len(self._storage)

    def __repr__(self):
        storage_string = "".join(
            f"\t== {cache_obj}\n" for cache_obj in list(self.storage.values())[-5:]
        )
        return (
            f"{self.__class__.__name__}<size_limit:{self.size_limit if self.limited else 'no limit'} total_size:{self.total_size}>\n{storage_string}"
        )

    def set_limit_size(self, limit):
        self.size_limit = limit

    @property
    def limited(self):
        """whether memory cache is limited"""
        return self.size_limit > 0

    @property
    def total_size(self):
        return self._size

    def clear(self):
        # with self._lock:
        self._size = 0
        for cache_obj in self._storage.values():
            cache_obj.clear()
        self._storage.clear()

    def popitem(self, last=False):
        if len(self._storage) == 0:
            return None, None

        # with self._lock:
        k, cache_obj = self._storage.popitem(last=last)
        self._size -= cache_obj.size
        value = cache_obj.value
        cache_obj.clear()

        return k, value

    def pop(self, key, default=None):
        # with self._lock:
        cache_obj = self._storage.pop(key, None)
        if cache_obj is None:
            return default

        self._size -= cache_obj.size
        cache_obj.clear()
        return default if cache_obj.is_expired else cache_obj.value

    def _adjust_size(self, key, cache_obj):
        if key in self._storage:
            self._size -= self._storage[key].size

        self._size += cache_obj.size

    def __call__(self, func: Callable) -> Any:
        def wapper(*args, **kwargs):
            try:
                ba = inspect.signature(func).bind(*args, **kwargs)
                ba.apply_defaults()
                string = to_json(ba.arguments, sort_keys=True, default=str)
                key = hashlib.md5(string.encode()).hexdigest()
                retval = self.__getitem__(key)
            except MissingCache:
                retval = func(*args, **kwargs)
                self.__setitem__(key, retval)

            return retval

        return wapper

    def update(self, ttl=0, **kwargs):
        for key, value in kwargs.items():
            self.set(key, value, ttl)


# diskcache = vxLRUCache(size_limit=1000, unit_factory=DiskCacheUnit)


SHARED_MEMORY_CACHE = "file:shm_cachedb?mode=memory&cache=shared"

import pickle
from functools import wraps
from vxutils.database.sqlite import vxSQLiteDB
from vxutils.dataclass import (
    vxDataClass,
    vxUUIDField,
    vxDatetimeField,
    vxBytesField,
)


class _CacheUnit(vxDataClass):
    key: str = vxUUIDField(False)
    value: Any = vxBytesField()
    expired_dt: float = vxDatetimeField()


class vxSQLiteCache:
    def __init__(self, db_uri: Union[str, Path] = None) -> None:
        if db_uri is None:
            db_uri = SHARED_MEMORY_CACHE

        self._conn = vxSQLiteDB.connect(db_uri)
        self._conn.create_table("__cache__", ["key"], _CacheUnit)
        self._last_remove_expired_dt = 0
        with self._conn.start_session() as session:
            self._remove_expired(session)

    def __contains__(self, key) -> bool:
        with self._conn.start_session() as session:
            self._remove_expired(session)
            cache_unit = session.findone(
                "__cache__", f"expired_dt> {vxtime.now()}", key=key
            )
            return bool(cache_unit)

    def __len__(self) -> int:
        with self._conn.start_session() as session:
            return len(session.distinct("__cache__", "key"))

    def __getitem__(self, key) -> Any:
        if not key:
            raise ValueError("key can't be empty")
        with self._conn.start_session() as session:
            self._remove_expired(session)
            cache_unit = session.findone(
                "__cache__", f"""expired_dt > {vxtime.now()}""", key=key
            )
            if cache_unit is None:
                raise MissingCache(key)
            return pickle.loads(cache_unit.value)

    def get(self, key: str, default: Any = None) -> Any:
        """获取缓存内容

        Arguments:
            key {str} -- 缓存key
            default {Any} -- 默认值 {default=None}, 如果缓存不存在，返回默认值

        Returns:
            Any -- 缓存内容
        """
        if not key:
            raise ValueError("key can't be empty")

        with self._conn.start_session() as session:
            self._remove_expired(session)
            cache_unit = session.findone(
                "__cache__", f"""expired_dt > {vxtime.now()}""", key=key
            )
            return pickle.loads(cache_unit.value) if cache_unit else default

    def get_many(self, *keys: List[str]) -> Dict:
        """获取缓存内容

        Returns:
            Dict -- 缓存内容
        """
        if not keys:
            raise ValueError("keys can't be empty")

        if len(keys) == 1 and isinstance(keys[0], (tuple, list)):
            keys = keys[0]

        with self._conn.start_session() as session:
            self._remove_expired(session)
            conditions = [
                f"""key in ('{"', '".join(keys)}')""",
                f"""expired_dt > {vxtime.now()}""",
            ]
            cur = session.find("__cache__", *conditions)
            return {
                cache_unit.key: pickle.loads(cache_unit.value) for cache_unit in cur
            }

    def set(
        self, key: str, value: Any, expired_dt: float = None, ttl: float = None
    ) -> None:
        """设置缓存内容

        Arguments:
            key {str} -- 缓存key
            value {Any} -- 缓存内容
            expired_dt {float} -- 超时时间 (default: {None})
            ttl {float} -- 生命周期，单位：s (default: {None})
        """
        if ttl:
            expired_dt = vxtime.now() + ttl

        if expired_dt is None:
            expired_dt = _ENDOFTIME

        _value = pickle.dumps(value)
        cache_unit = _CacheUnit(key=key, value=_value, expired_dt=expired_dt)
        with self._conn.start_session() as session:
            self._remove_expired(session)
            session.save("__cache__", cache_unit)

    def pop(self, key: str, default: Any = None) -> Any:
        """弹出缓存内容

        Arguments:
            key {str} -- 缓存key
            default {Any} -- 缺省值 (default: {None})

        Returns:
            Any -- 缓存内容
        """
        if not key:
            raise ValueError("key can't be empty")

        with self._conn.start_session() as session:
            self._remove_expired(session)
            cache_unit = session.findone(
                "__cache__", f"""expired_dt > {vxtime.now()}""", key=key
            )
            if cache_unit:
                session.delete("__cache__", key=key)
                return pickle.loads(cache_unit.value)
            return default

    def _remove_expired(self, session: vxSQLiteDB) -> Any:
        """删除超时内容"""
        now = vxtime.now()
        if self._last_remove_expired_dt + 60 > now:
            return
        self._last_remove_expired_dt = now
        session.delete("__cache__", f"expired_dt < {self._last_remove_expired_dt}")

    def update(
        self, cacheobjs: Dict, expired_dt: float = None, ttl: float = None
    ) -> None:
        """批量更新

        Keyword Arguments:
            expired_dt {float} -- 超时时间 (default: {None})
            cacheobjs {dict} -- 缓存内容
        """
        if ttl:
            expired_dt = vxtime.now() + ttl

        if expired_dt is None or expired_dt > _ENDOFTIME:
            expired_dt = _ENDOFTIME
        cache_units = [
            _CacheUnit(key=key, value=pickle.dumps(value), expired_dt=expired_dt)
            for key, value in cacheobjs.items()
        ]
        with self._conn.start_session() as session:
            self._remove_expired(session)
            session.save("__cache__", cache_units)

    def clear(self) -> None:
        """清空所有缓存内容"""
        with self._conn.start_session() as session:
            session.truncate("__cache__")

    def keys(self) -> List[str]:
        """获取所有key"""
        with self._conn.start_session() as session:
            return session.distinct("__cache__", "key", f"expired_dt > {vxtime.now()}")

    def hash_keys(self, obj: Any) -> str:
        """将keys进行hash

        Arguments:
            obj {Any} -- 需要hash的对象

        Returns:
            str -- hash后的keys
        """
        try:
            return hash(obj)
        except TypeError:
            return hash(to_json(obj.__dict__, sort_keys=True, default=str))

    def __call__(self, ttl: float = None) -> Any:
        def deco(func: Callable) -> Callable:
            @wraps(func)
            def wapper(*args, **kwargs):
                try:
                    ba = inspect.signature(func).bind(*args, **kwargs)
                    ba.apply_defaults()
                    string = to_json(ba.arguments, sort_keys=True, default=str)
                    key = hashlib.md5(string.encode()).hexdigest()
                    retval = self[key]
                except MissingCache:
                    retval = func(*args, **kwargs)
                    self.set(key, retval, ttl=ttl)

                return retval

            return wapper

        return deco


_cache_path = Path.home().joinpath(".cache")
_cache_path.mkdir(parents=True, exist_ok=True)
diskcache = vxSQLiteCache(str(_cache_path.joinpath("vxcache.dat").absolute()))

if __name__ == "__main__":
    # @c(ttl=10)
    @diskcache(ttl=10)
    def test(n):
        if n < 2:
            return n
        return test(n - 1) + test(n - 2)

    with vxtime.timeit():
        print(test(20))
