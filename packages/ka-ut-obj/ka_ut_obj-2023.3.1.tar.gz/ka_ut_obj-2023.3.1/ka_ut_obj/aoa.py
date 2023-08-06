# coding=utf-8

# from ka_ut_com.log import Log

from ka_ut_obj.arr import Arr

from typing import Any, Dict, List

T_AoA = List[List[Any]]
T_AoD = List[Dict[Any, Any]]


class AoA:
    """ Manage Array of Arrays
    """
    @staticmethod
    def nvl(aoa: T_AoA) -> T_AoA:
        """ nvl function similar to SQL NVL function
        """
        if aoa is None:
            return []
        return aoa

    @staticmethod
    def to_aod(
            aoa: T_AoA, keys: List[Any]) -> T_AoD:
        """ Migrate Array of Arrays to Array of Dictionaries
        """
        aod: T_AoD = []
        for _arr in aoa:
            dic = Arr.to_dic(_arr, keys)
            aod.append(dic)
        return aod

    @staticmethod
    def to_doa_from_2cols(aoa, a_ix):
        doa = {}
        if len(a_ix) < 2:
            return doa
        for arr in aoa:
            arr0 = arr[a_ix[0]]
            arr1 = arr[a_ix[1]]

            if arr0 not in doa:
                doa[arr0] = []
            if isinstance(arr1, (tuple, list)):
                doa[arr0].extend(arr1)
            else:
                doa[arr0].append(arr1)
        return doa

    @staticmethod
    def to_dic_from_2cols(aoa, a_ix):
        dic = {}
        if len(a_ix) < 2:
            return dic
        for arr in aoa:
            if arr[a_ix[1]] is None:
                continue
            dic[arr[a_ix[0]]] = arr[a_ix[1]]
        return dic

    @staticmethod
    def to_arr_from_2cols(aoa, a_ix):
        arr_new = []
        for arr in aoa:
            arr0 = arr[a_ix[0]]
            arr1 = arr[a_ix[1]]
            arr_new.append(arr0)
            if isinstance(arr1, (tuple, list)):
                arr_new.extend(arr1)
            else:
                arr_new.append(arr1)
        return list(set(arr_new))
