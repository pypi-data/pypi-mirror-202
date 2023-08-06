# coding=utf-8

import re

from typing import Any, List

T_AoA = List[List]


class Str:
    """ Manage String Class
    """
    @staticmethod
    def is_odd(string: str) -> bool:
        if string.isnumeric():
            if int(string) % 2 == 0:
                return False
            return True
        else:
            return False

    @staticmethod
    def is_integer(string: str) -> bool:
        if string[0] in ('-', '+'):
            return string[1:].isdigit()
        return string.isdigit()

    @staticmethod
    def is_boolean(string) -> bool:
        if string.strip().lower() in ['true', 'false']:
            return True
        return False

    @staticmethod
    def is_undefined(string: None | str) -> bool:
        """ nvl function similar to SQL NVL function
        """
        if string is None or string == '':
            return True
        return False

    @staticmethod
    def nvl(string: None | str) -> None | str:
        """ nvl function similar to SQL NVL function
        """
        if string is None:
            return ''
        return string

    @staticmethod
    def strip_n(string: str):
        """ Replace new line by Blank and strip Blanks
        """
        return string.replace('\n', ' ').strip()

    @staticmethod
    def remove(string: str, a_to_remove: List) -> str:
        """ Replace new line by Blank and strip Blanks
        """
        for to_remove in a_to_remove:
            string = string.replace(to_remove, '')
        return string

    @staticmethod
    def sh_boolean(string: str) -> bool:
        """ Show valid Boolean string as boolean
        """
        if string.lower() == 'true':
            return True
        elif string.lower() == 'false':
            return False
        else:
            raise ValueError

    @staticmethod
    def sh_float(string: str):
        """ Returns Float if string is of Type Float
            otherwise None
        """
        try:
            return float(string)
        except ValueError:
            return None

    @staticmethod
    def sh_int(string: str):
        """ Returns Int if string is of Type Int
            otherwise None
        """
        try:
            return int(string)
        except ValueError:
            return None

    # @staticmethod
    # def to_int(string: str):
    #     """ Returns Int if string is of Type Int
    #         otherwise None
    #     """
    #     try:
    #         return int(string)
    #     except ValueError:
    #         return None

    @staticmethod
    def sh_first_item(string: str) -> Any:
        """ Show first substring of string
        """
        return string.split()[0]

    @classmethod
    def sh_a_int(cls, string: str, sep: str) -> Any:
        """ Show first substring of string
        """
        # arr = string.split(sep)
        arr = re.split(sep, string)
        arr_new = []
        for item in arr:
            _item = item.strip()
            if not isinstance(_item, str):
                continue
            if not _item.isdigit():
                continue
            arr_new.append(cls.to_int(_item))
        return arr_new
