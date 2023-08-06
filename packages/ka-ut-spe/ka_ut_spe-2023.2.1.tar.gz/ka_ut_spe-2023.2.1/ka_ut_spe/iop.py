# coding=utf-8

import datetime
import os
import string

from ka_ut_com.log import Log

from ka_ut_app.ka_json import Json as UtaJson
from ka_ut_app.ka_toml import Toml as UtaToml
from ka_ut_app.ka_txt import Txt as UtaTxt
from ka_ut_app.ka_yaml import Yaml as UtaYaml
from ka_ut_app.ka_py import Py as UtaPy
from ka_ut_app.ka_xlsx import Workbook


class Arr:
    """ io for Array
    """
    @staticmethod
    def write(arr: list, path: str) -> None:
        with open(path, 'wt') as fd:
            string = '\n'.join(arr)
            fd.write(string)


class XmlStr:
    """ io for Xml String
    """
    @staticmethod
    def write(xmlstr: str, path: str) -> None:
        with open(path, 'w') as fd:
            fd.write(xmlstr)


class Dic:
    """ io for Dictionary
    """
    class Txt:
        @staticmethod
        def write(dic: dict, path_: str, indent: int = 2) -> None:
            UtaTxt.write(dic, path_, indent=indent)

    class Json:
        @staticmethod
        def write(dic: dict, path_: str, indent: int = 2) -> None:
            UtaJson.write(dic, path_, indent=indent)

    class Yaml:
        @staticmethod
        def write(dic: dict, path: str, indent: int = 2) -> None:
            UtaYaml.write(dic, path, indent=indent)


class Obj:
    """ Manage I/O for Object
    """
    Format2Function = {
        "yaml": UtaYaml,
        "json": UtaJson,
        "toml": UtaToml,
        "py": UtaPy}

    @staticmethod
    def sh_obj_type_short(obj_type, **kwargs):
        obj_types = kwargs.get('obj_types')
        if obj_types is None:
            return obj_type
        if obj_type in obj_types:
            return obj_types[obj_type]
        return obj_type

    @classmethod
    def sh_sw_out(cls, obj_type, file_format, **kwargs):
        sw_out = kwargs.get('sw_out')
        if sw_out is not None:
            Log.Eq.debug("sw_out", sw_out)
            return sw_out
        s_sw_out = f"sw_out_{file_format}"
        sw_out = kwargs.get(s_sw_out)
        if sw_out is not None:
            Log.Eq.debug("s_sw_out", s_sw_out)
            Log.Eq.debug("sw_out", sw_out)
            return sw_out
        s_sw_out = f"sw_out_{obj_type}_{file_format}"
        sw_out = kwargs.get(s_sw_out)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print(f"s_sw_out = {s_sw_out}")
        print(f"obj_type = {obj_type}")
        print(f"kwargs = {kwargs}")
        print(f"sw_out = {sw_out}")
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        if sw_out is not None:
            return sw_out
        obj_type_short = cls.sh_obj_type_short(obj_type, **kwargs)
        if obj_type_short is None:
            return False
        s_sw_out = f"sw_out_{obj_type_short}_{file_format}"
        return kwargs.get(s_sw_out, False)

    @classmethod
    def sh_dir_out(cls, obj_type, **kwargs):
        _dir_out = kwargs.get("dir_out")
        if _dir_out is not None:
            return _dir_out
        _dir_out = kwargs.get(f"dir_out_{obj_type}")
        if _dir_out is not None:
            return _dir_out
        obj_type_short = cls.sh_obj_type_short(obj_type, **kwargs)
        _dir_out = kwargs.get(f"dir_out_{obj_type_short}")
        return _dir_out

    @classmethod
    def sh_path_out(cls, obj_type, **kwargs):
        path_out = kwargs.get('path_out')
        if path_out is not None:
            return path_out
        s_path_out = f'path_out_{obj_type}'
        path_out = kwargs.get(f'path_out_{obj_type}')
        print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        print(f"obj_type = {obj_type}")
        print(f"s_path_out = {s_path_out}")
        print(f"path_out = {path_out}")
        print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        if path_out is not None:
            return path_out
        obj_type_short = cls.sh_obj_type_short(obj_type, **kwargs)
        if obj_type_short is not None:
            path_out = kwargs.get(f'path_out_{obj_type_short}')
        return path_out

    @classmethod
    def sh_path_out_by_dir(cls, obj_type, file_format, **kwargs):
        dir_out = cls.sh_dir_out(obj_type, **kwargs)
        file = kwargs.get('file')
        _file = f"{file}.{file_format}"
        if dir_out is None:
            return _file
        return os.path.join(dir_out, _file)

    @classmethod
    def sh_dic_substitute(cls, obj_type, file_format, **kwargs):
        file = kwargs.get('file')
        dic = {}
        if file is not None:
            dic['file'] = file
        if obj_type is not None:
            dic['obj_type'] = obj_type
        obj_type_short = cls.sh_obj_type_short(obj_type, **kwargs)
        if obj_type_short is not None:
            dic['obj_type_short'] = obj_type_short
        if file_format is not None:
            dic['file_format'] = file_format

        sw_today = cls.sh_sw_out(obj_type, 'today', **kwargs)
        if sw_today:
            dic['today'] = f'.{datetime.date.today().strftime("%Y%m%d")}'
        else:
            dic['today'] = ''
        return dic

    @classmethod
    def get_path_out(cls, obj_type, file_format, **kwargs):
        path_out = cls.sh_path_out(obj_type, **kwargs)
        if path_out is None:
            path_out = cls.sh_path_out_by_dir(obj_type, file_format, **kwargs)
        if path_out is None:
            return None
        dic_substitute = cls.sh_dic_substitute(obj_type, file_format, **kwargs)
        path_out_template = string.Template(path_out)
        _path_out = path_out_template.safe_substitute(dic_substitute)
        Log.Eq.debug("_path_out", _path_out)
        return _path_out

    @classmethod
    def write(cls, obj, obj_type, **kwargs):
        Log.Eq.debug("obj", obj)
        for file_format, file_function in cls.Format2Function.items():
            sw_out = cls.sh_sw_out(obj_type, file_format, **kwargs)
            print(f"obj_type = {obj_type}")
            print(f"file_format = {file_format}")
            print(f"sw_out = {sw_out}")
            if not sw_out:
                continue
            path_out = cls.get_path_out(obj_type, file_format, **kwargs)
            file_function.write(obj, path_out)


class Xlsx:

    @staticmethod
    def read_sheet_names(path):
        return Workbook.read_sheet_names(path)

    @staticmethod
    def read_sheet_to_dic(path, sheet_id):
        return Workbook.read_sheet_to_dic(path, sheet_id)

    @staticmethod
    def read_sheet_to_arr(path, sheet_id):
        return Workbook.read_sheet_to_arr(path, sheet_id)

    @staticmethod
    def read_sheets_to_aoa(path, **kwargs):
        sheet_ids = kwargs.get("sheet_ids")
        return Workbook.read_sheets_to_aoa(path, sheet_ids)

    @staticmethod
    def read_workbooks_sheets_to_ao_aoa(path, **kwargs):
        sheet_ids = kwargs.get("sheet_ids")
        return Workbook.read_workbook_sheets_to_aoa(
            path, sheet_ids=sheet_ids)


# class Json:
#
#     @staticmethod
#     def json_read_to_dic(path):
#         return Json.read(path)
#
#
# class Yaml:
#
#     @staticmethod
#     def yaml_read_to_dic(path):
#         return Yaml.read(path)


class Path:
    """ io for path
    """
    @staticmethod
    def sh_splitext(path, **kwargs):
        a_path = os.path.splitext(path)
        dir = a_path[0]
        ext = a_path[1].strip(".").lower()
        return dir, ext

    @classmethod
    def read_path(cls, path, **kwargs):
        path_dir, path_ext = cls.sh_splitext(path, **kwargs)
        if path_ext == "xlsx":
            read_cmd = kwargs.get("read_cmd", "sheet_to_dic")
            if read_cmd == "sheet_to_dic":
                sheet_id = kwargs.get("sheet_id")
                return Xlsx.read_sheet_to_dic(path, sheet_id)
            elif read_cmd == "read_sheet_to_aod":
                sheet_id = kwargs.get("sheet_id")
                return Xlsx.read_sheet_to_aod(path, sheet_id)
            elif read_cmd == "read_sheets_to_aod":
                return Xlsx.read_sheets_to_aod(path, sheet_id)
        elif path_ext == "json":
            return UtaJson.read(path)
        elif path_ext in ["yaml", "yml"]:
            return UtaYaml.read(path)

    @classmethod
    def read_paths(cls, paths, **kwargs):
        arr = []
        for path in paths:
            obj = cls.read_path(path, **kwargs)
            arr.append(obj)
        return arr

    @classmethod
    def read(cls, path, **kwargs):
        Log.Eq.debug("kwargs", kwargs)
        Log.Eq.debug("path", path)
        if isinstance(path, (tuple, list)):
            return cls.read_paths(path, **kwargs)
        else:
            return cls.read_paths(path, **kwargs)
