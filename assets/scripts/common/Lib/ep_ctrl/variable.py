#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#
# Distributed under terms of the MIT license.
from __future__ import unicode_literals, division

from .utils import EMPTY_FUNC
from ._model import BaseVar


class VarGetter(BaseVar):
    
    def _be_binded_element(self, *args, **kwargs):
        """VarGetter cannot be binded by other elements"""
        raise TypeError('VarGetter not support be binded')

    def _be_unbinded_element(self, *args, **kwargs):
        """VarGetter cannot be un-bind by other elements"""        


class VarSetter(BaseVar):

    def __init__(self, eid, controller, var_name, new_var_value, **kwargs):
        super().__init__(eid, controller, var_name, **kwargs)
        self._new_var_value = new_var_value

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        self._modify_variable()
        self.trigger_all(1, obj)

    def _modify_variable(self):
        self._controller.set_variable(self._var_name, self._new_var_value)
