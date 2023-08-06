"""
seldom cache
"""
import json
from seldom.logging import log
from seldom.utils.lru_cache import cache


@cache()
def json_func(key, value):
    return value


class Cache:
    """
    Cache through JSON files
    """

    # @staticmethod
    # def clear(name: str = None) -> None:
    #     """
    #     Clearing cached
    #     :param name: key
    #     """
    #     if name is None:
    #         with open(DATA_PATH, "w+", encoding="utf-8") as json_file:
    #             json.dump({}, json_file)
    #             log.info("Clear all cache data")
    #
    #     else:
    #         with open(DATA_PATH, "r+", encoding="utf-8") as json_file:
    #             save_data = json.load(json_file)
    #             del save_data[name]
    #             json.dump(save_data, json_file)
    #             log.info(f"Clear cache data: {name}")
    #
    #         with open(DATA_PATH, "w+", encoding="utf-8") as json_file:
    #             json.dump(save_data, json_file)

    @staticmethod
    def set(data: dict) -> None:
        """
        Setting cached
        :param data:
        """
        for k, v in data.items():
            json_func(k, v)

    @staticmethod
    def get(name=None):
        """
        Getting cached
        :param name: key
        :return:
        """
        json_func(name, v)
        with open(DATA_PATH, "r+", encoding="utf-8") as json_file:
            save_data = json.load(json_file)
            if name is None:
                return save_data

            value = save_data.get(name, None)
            if value is not None:
                log.info(f"Get cache data: {name} = {value}")

            return value


cache = Cache()
