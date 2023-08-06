# coding=utf-8

# from ka_ut_com.log import Log

from ka_ut_app.ka_json import Json


class Obj:
    """ Manage Object
    """
    class Json:

        @classmethod
        def write(obj, path_, **kwargs):
            sw_verify = kwargs.get('sw_orjson', False)
            if sw_verify:
                if not Obj.verify_key_type_str(obj):
                    # print(f'fuck:path_ = {path_}')
                    return
            Json.write(obj, path_, **kwargs)
