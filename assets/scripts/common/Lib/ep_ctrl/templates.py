#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 weooh qinzezzhen@outlook.com 
#
# Distributed under terms of the MIT license.
from __future__ import unicode_literals, division


def build_delay_for_loop(loop_event, delay_event=None):
    """带有延迟的循环, 由延迟事件触发循环事件
    
    :param _BasicElement loop_event: 循环控制事件
    :param _BasicElemetn delay_event: 延迟事件, ``None`` 代表不延迟
    :return: 整合后的事件
    """

    if not delay_event:
        return loop_event
    delay_event.bind_element(loop_event, 1, 1)
    return delay_event

