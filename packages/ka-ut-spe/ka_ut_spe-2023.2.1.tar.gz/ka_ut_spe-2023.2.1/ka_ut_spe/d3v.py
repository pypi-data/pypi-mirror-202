# coding=utf-8

from datetime import date

from ka_ut_obj.ka_d3v import D3V as UtoD3V

from ka_ut_app.ka_csv import Csv as KaCsv


class D3V:

    class Csv:

        @staticmethod
        def write(d3, cfg_io_out, d3_nm, **kwargs):
            _sw = kwargs.get('sw_' + d3_nm)
            if not _sw:
                return
            # _path = cfg_io_out[d3_nm]["csv"]["path"]
            _keys = cfg_io_out[d3_nm]["keys"]
            _aoa = UtoD3V.yield_values(d3)
            today = date.today().strftime("%Y%m%d")
            _path = kwargs.get(f'path_out_{d3_nm}').format(today=today)
            KaCsv.AoA.write(_aoa, _path, _keys, **kwargs)
