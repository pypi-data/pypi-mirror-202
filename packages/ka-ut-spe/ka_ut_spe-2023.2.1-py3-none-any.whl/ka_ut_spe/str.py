# coding=utf-8

from ka_ut_app.ka_yaml import Yaml

from typing import Any, Optional


class Str:
    """ Manage String Class
    """
    @staticmethod
    def sh_arr(string: str) -> Optional[Any]:
        """ Show valid Array string as Array
        """
        return Yaml.safe_load(string)

    @staticmethod
    def sh_dic(string: str) -> Optional[Any]:
        """ Show valid Dictionary string as Dictionary
        """
        return Yaml.safe_load(string)
