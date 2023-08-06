import os
import uuid
import pickle
import shutil
import tempfile
from functools import wraps as func_wraps


class DiskCache(object):
    """缓存数据到磁盘

    实例化参数:
    -----
        cache_path: 缓存文件的路径
    """

    _NAMESPACE = uuid.UUID("c875fb30-a8a8-402d-a796-225a6b065cad")

    def __init__(self, cache_path=None):
        if cache_path:
            self.cache_path = os.path.abspath(cache_path)
        else:
            self.cache_path = os.path.join(tempfile.gettempdir(), ".diskcache")

    def __call__(self, func):
        """返回一个包装后的函数

        如果磁盘中没有缓存，则调用函数获得结果并缓存后再返回
        如果磁盘中有缓存，则直接返回缓存的结果
        """
        @func_wraps(func)
        def wrapper(*args, **kw):
            params_uuid = uuid.uuid5(self._NAMESPACE, "-".join(map(str, (args, kw))))
            key = '{}-{}.cache'.format(func.__name__, str(params_uuid))
            cache_file = os.path.join(self.cache_path, key)

            if not os.path.exists(self.cache_path):
                os.makedirs(self.cache_path)

            try:
                with open(cache_file, 'rb') as f:
                    val = pickle.load(f)
            except Exception:
                val = func(*args, **kw)
                try:
                    with open(cache_file, 'wb') as f:
                        pickle.dump(val, f)
                except Exception:
                    pass
            return val
        return wrapper

    def clear(self, func_name):
        """清理指定函数调用的缓存"""
        for cache_file in os.listdir(self.cache_path):
            if cache_file.startswith(func_name + "-"):
                os.remove(os.path.join(self.cache_path, cache_file))

    def clear_all(self):
        """清理所有缓存"""
        if os.path.exists(self.cache_path):
            shutil.rmtree(self.cache_path)


disk_disk = DiskCache()
