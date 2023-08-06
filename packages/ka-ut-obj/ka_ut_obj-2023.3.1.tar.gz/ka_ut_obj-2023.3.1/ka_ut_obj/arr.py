# coding=utf-8

from ka_ut_com.log import Log

from typing import Literal, Any, Dict, List, Union, Callable


class Arr:
    """ Manage Array
    """
    @staticmethod
    def join_filter_none(
            arr: None | list,
            separator=' ') -> None | str:
        return separator.join(filter(lambda item: item is not None, arr))

    @staticmethod
    def encode(
            arr: None | list) -> None | str:
        Log.Eq.debug("args", arr)
        if arr is None or len(arr) == 0:
            return None
        arr_joined = ' '.join(arr)
        if arr_joined == '':
            return None
        return f"{arr_joined} ".replace(' ', '%20')

    @staticmethod
    def is_empty(
            arr: None | list) -> Literal[True, False]:
        if arr is None:
            return True
        if isinstance(arr, (list, tuple)):
            if arr == []:
                return True
        return False

    @classmethod
    def is_not_empty(
            cls, arr: None | list) -> Literal[True, False]:
        return not cls.is_empty(arr)

    @staticmethod
    def sh_item(
            arr: None | List, ii: int) -> None | Any:
        if arr is None:
            return arr
        if arr == []:
            return None
        return arr[ii]

    @staticmethod
    def sh_items_str(
            arr: None | List, start: int, end: int) -> None | str:
        if arr is None:
            return arr
        if arr == []:
            return None
        return ' '.join(arr[start:end])

    @staticmethod
    def sh_item_lower(
            arr: None | list, ii: int) -> None | Any:
        if arr is None:
            return arr
        if arr == []:
            return None
        return arr[ii].lower()

    @staticmethod
    def sh_item_if(
          string: None | str,
          arr: None | List,
          ii: int) -> None | Any:
        if arr is None:
            return arr
        if arr == []:
            return None
        item = arr[ii]
        if string in item:
            return item
        return None

    @classmethod
    def sh_item0(
            cls, arr: List) -> Any:
        if arr == []:
            return None
        return cls.sh_item(arr, 0)

    @classmethod
    def sh_item0_if(
            cls, string: str, arr: list) -> Any:
        return cls.sh_item_if(string, arr, 0)

    @staticmethod
    def append(
            arr: None | List,
            item: Union[None, List, str]) -> None:
        if arr is None:
            return
        if item is None:
            return
        if isinstance(item, list):
            if item == []:
                return
        elif isinstance(item, str):
            if item == '':
                return
        arr.append(item)

    @staticmethod
    def append_unique(
            arr: List,
            item: Union[None, List, str]) -> None:
        if item is None:
            return
        if isinstance(item, list):
            if item == []:
                return
        elif isinstance(item, str):
            if item == '':
                return
        if item not in arr:
            arr.append(item)

    @staticmethod
    def extend(
            arr: None | List, item: Union[None, List, str]) -> None:
        if arr is None:
            return
        if item is None:
            return
        if isinstance(item, list):
            if item == []:
                return
        elif isinstance(item, str):
            if item == '':
                return
        arr.extend(item)

    @staticmethod
    def apply_str(
            arr: None | list) -> None | list:
        if arr is None:
            return arr
        _arr: List = []
        for item in arr:
            if item is None:
                _arr.append(item)
            elif isinstance(item, str):
                _arr.append(item)
            else:
                _arr.append(str(item))
        return _arr

    @staticmethod
    def apply_function(
            arr: None | list,
            function: Callable, **kwargs) -> None | List:
        if arr is None:
            return arr
        _arr: List = []
        for item in arr:
            _item = function(item, **kwargs)
            if _item is None:
                continue
            _arr.append(_item)
        return _arr

    @staticmethod
    def to_dic(
            arr: List, keys: List) -> Dict:
        dic = {}
        for ii in range(len(arr)):
            dic[keys[ii]] = arr[ii]
        return dic

    @staticmethod
    def merge(
            arr0: List, arr1: List) -> None | List:
        if arr0 != []:
            if arr1 != []:
                arr0.extend(arr1)
            return arr0
        else:
            if arr1 != []:
                return arr1
        return arr0

    @staticmethod
    def sh_subarray(
            arr: None | List, from_: int, to_: int) -> None | List:
        if arr == [] or arr is None:
            return arr
        if from_ >= to_:
            return arr

        from_new = max(0, from_)
        len_arr = len(arr)
        if to_ < len_arr:
            to_new = to_ + 1
        else:
            to_new = len_arr
        return arr[from_new:to_new]

    @staticmethod
    def get_key_value(
            arr: None | list,
            ix: int = 0,
            default: str = '',
            key: str = 'Title') -> None | str:
        if arr is None:
            return arr
        if ix >= len(arr):
            return default
        arr_ix = arr[ix]
        key_ = arr_ix.text.replace('\n', ' ').strip()

        if key_ == key:
            ix_next = ix + 1
            value = arr[ix_next].text.replace('\n', ' ').strip()
        else:
            value = ''

        Log.Eq.debug("arr", arr)
        Log.Eq.debug("arr_ix", arr_ix)
        Log.Eq.debug("key_", key_)
        Log.Eq.debug("value", value)

        return value

    @staticmethod
    def get_text(
            arr: None | list,
            ix: int = 0,
            default: str = '') -> None | str:
        if arr is None:
            return None
        if ix >= len(arr):
            return default
        arr_ix = arr[ix]
        arr_ix_text = arr_ix.text.replace('\n', ' ').strip()

        Log.Eq.debug("arr", arr)
        Log.Eq.debug("arr_ix", arr_ix)
        Log.Eq.debug("arr_ix_text", arr_ix_text)

        return arr_ix_text

    @staticmethod
    def get_text_split(
            arr: None | list,
            ix0: int = 0,
            default: str = '',
            ix1=0,
            separator: str = 'see less') -> None | str:
        if arr is None:
            return None
        if ix0 >= len(arr):
            return default
        arr_ix0 = arr[ix0]
        arr_ix0_text = arr_ix0.text.replace('\n', ' ').strip()
        arr_ix0_text_split_ix1 = arr_ix0_text.split(separator)[ix1].strip()

        Log.Eq.debug("arr", arr)
        Log.Eq.debug("arr_ix0", arr_ix0)
        Log.Eq.debug("arr_ix0_text", arr_ix0_text)
        Log.Eq.debug("arr_ix0_text_split_ix1", arr_ix0_text_split_ix1)

        return arr_ix0_text_split_ix1
