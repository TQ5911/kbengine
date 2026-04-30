#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#
# Distributed under terms of the MIT license.
from __future__ import unicode_literals, division


class EP_ElementError(RuntimeError):
    """Basic element exception/error"""

    def __init__(self, msg, err_node, *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
        self.err_node = err_node

class EP_ControllerError(RuntimeError):

    def __init__(self, msg, err_node, *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
        self.err_node = err_node


class EP_ElementCheckerError(EP_ElementError):
    """raise for check params/refParams fail"""
