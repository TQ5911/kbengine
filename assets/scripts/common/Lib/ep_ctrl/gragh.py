#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 weooh qinzezzhen@outlook.com
#
# Distributed under terms of the MIT license.
from __future__ import unicode_literals, division


class BaseElementGraghBuilder(object):
    def __init__(self):
        self._name_hooks = {}
        
    def build(self, element):
        data = self._build_view_str(element)
        rb_data = list(self._build_view_bind_relation(element))
        rc_data = list(self._build_view_ref_relation(element))
        return element.name, data, rb_data, rc_data

    def _trans_in(self, e, idx):
        return "IN_{}".format(idx)

    def _trans_out(self, e, idx):
        return "OUT_{}".format(idx)

    def _trans_ref_param(self, e, name):
        return "REF_{}".format(name)

    def _trans_param(self, e, name):
        return "PRM_{}".format(name)

    def _build_view_str(self, e):
        _temp_e = r"""
{{ 
    {name} |
    {{  
        {{ {inputs} | {ref_params} }} |
        {{ {outputs} }}
    }} |
    {params}
}}
"""
        _temp_ref = r"<{0}> {0}"
        _temp_ref_v = r"<{0}> {0} = {1}"

        outputs = '|'.join(_temp_ref.format(self._trans_out(e, i))
                           for i in e._binded_dic.keys())
        ref_params = '|'.join(_temp_ref.format(self._trans_ref_param(e, i))
                              for i in e._ref_params_dic.keys())

        def _pkg_params(e, i):
                _p = e.get_param(i)
                if isinstance(_p, (list, dict)):
                    return '{}()'.format(_p.__class__.__name__)
                elif isinstance(_p, str) and len(_p) > 10:
                    return "{}...".format(_p[:10])
                return _p

        params = '|'.join(
            _temp_ref_v.format(
                self._trans_param(e, i), _pkg_params(e, i))
            for i in e._params.keys())
        _input_set = set()
        for _be_bind_dic in e._be_bind_dic.values():
            for _be_bind_data in _be_bind_dic.values():
                _input_set.add(_be_bind_data.org_idx)
        inputs = '|'.join(_temp_ref.format(self._trans_in(e, i))
                          for i in _input_set)

        return _temp_e.format(name=e.name,
                              inputs=inputs,
                              outputs=outputs,
                              ref_params=ref_params,
                              params=params)


    def _build_view_bind_relation(self, e):
        for idx, bind_dic in e._binded_dic.items():
            for bind_data in bind_dic.values():
                r_data_1 = "{}:{}".format(e.name,
                                          self._trans_out(e, idx))
                te = bind_data.element
                r_data_2 = "{}:{}".format(
                        te.name,
                        self._trans_in(te, bind_data.element_idx))
                yield r_data_1, r_data_2

    def _build_view_ref_relation(self, e):
        for name, (org_e, org_name) in e._ref_params_dic.items():
            r_data_2 = '{}:{}'.format(
                e.name, self._trans_ref_param(e, name))
            r_data_1 = "{}:{}".format(
                org_e.name, self._trans_param(org_e, org_name))
            yield r_data_1, r_data_2

