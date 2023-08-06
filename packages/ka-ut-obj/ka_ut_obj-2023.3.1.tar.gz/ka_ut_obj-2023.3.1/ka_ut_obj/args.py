# coding=utf-8

from ka_ut_com.pacmod import Pacmod

from ka_ut_obj.str import Str


class Args:
    """ Manage Arguments and Keyword Arguments
    """
    class Key:
        @staticmethod
        def sh(key):
            if key.startswith(('d_', 'a_', 'aoa_', 'f_')):
                return key[2:]
            else:
                return key

    class Value:
        class SysArgv:
            @staticmethod
            def sh(key, value):
                if key.startswith('sw_'):
                    return Str.sh_boolean(value)
                elif key.startswith('d_'):
                    return Str.sh_dic(value)
                elif key.startswith('a_'):
                    return Str.sh_arr(value)
                elif key.startswith('aoa_'):
                    return Str.sh_aoa(value)
                elif key.startswith('f_'):
                    return value
                else:
                    if Str.is_integer(value):
                        return int(value)
                    else:
                        return value

        @staticmethod
        def sh(key, value):
            if key.startswith('d_'):
                return value
            return value

    @classmethod
    def sh_d_eq(cls, a_s_eq, **kwargs):
        """ Manage Argument Equates
        """
        root_cls = kwargs.get('root_cls')
        sh_parms = kwargs.get('sh_parms')
        sh_prof = kwargs.get('sh_prof')
        if sh_parms is not None:
            parms = sh_parms()
        else:
            parms = []
        d_eq = {}

        for s_eq in a_s_eq[1:]:
            key, value = s_eq.split('=')

            if key not in parms:
                msg = (f"Wrong parameter: {key}; "
                       f"valid parameters are: {parms}")
                raise Exception(msg)
                # return {}

            key_ = cls.Key.sh(key)
            value_ = cls.Value.SysArgv.sh(key, value)
            d_eq[key_] = value_

        for key in parms:
            key_ = cls.Key.sh(key)
            if key_ not in d_eq:
                default = parms[key]
                if default is not None:
                    value_ = cls.Value.sh(key, default)
                    d_eq[key_] = value_

        tenant = d_eq.get('tenant')
        d_eq['pacmod_curr'] = Pacmod.sh(root_cls, tenant)
        d_eq['sh_prof'] = sh_prof

        return d_eq
