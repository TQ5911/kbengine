#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#
# Distributed under terms of the MIT license.
from __future__ import unicode_literals, division

from ._model import BaseFlow, OptionInputParamMixin, OverOneTickMixin
from .exceptions import EP_ElementError


class Branch(BaseFlow):

    CONDITION_KEY = '_condition'
    BINDING_TRUE = 1
    BINDING_FALSE = 2

    def __init__(self, eventId, controller=None, **kwargs):
        super().__init__(eventId, controller, **kwargs)
        self.regr_flow_handler(self._branch_handler, 1)

    def _branch_handler(self, this, srcE, obj, **refParams):
        if self.CONDITION_KEY not in refParams:
            raise TypeError('must bind condition first')

        cond_result  = refParams[self.CONDITION_KEY]
        self.trigger_all(self.BINDING_TRUE, obj) if cond_result \
            else self.trigger_all(self.BINDING_FALSE, obj)

    def bind_condition(self, condition, key):
        self.referenceArgument(condition, key, self.CONDITION_KEY)

    def unbind_condition(self):
        self.unReferenceArgument(self.CONDITION_KEY)

    def rebind_condition(self, new_condition, key):
        self.unReferenceArgument(self.CONDITION_KEY)
        self.referenceArgument(new_condition, key, self.CONDITION_KEY)

    def bind_true_element(self, element, element_idx):
        self.bind_element(element, self.BINDING_TRUE, element_idx)

    def bind_false_element(self, element, element_idx):
        self.bind_element(element, self.BINDING_FALSE, element_idx)


class DoN(BaseFlow, OptionInputParamMixin):

    LOOP_N_REFKEY = '_LOOP_N'
    LOOP_N_SELF_KEY = '_LOOP_N_S'

    ENTER_INPUT_IDX = 1
    RESET_INPUT_IDX = 2

    BINDING_OUTPUT = 1

    def __init__(self, eventId, controller=None, **kwargs):
        super(DoN, self).__init__(eventId, controller, **kwargs)
        self._looping_count = 0
        self.regr_flow_handler(self._handle_enter_input, self.ENTER_INPUT_IDX)
        self.regr_flow_handler(self._handle_reset_input, self.RESET_INPUT_IDX)

    def get_loop_n(self, default=0):
        return int(self.get_op_ref_param(self.LOOP_N_REFKEY, default))

    def set_loop_n(self, n=0, src=None, src_key=None):
        self.set_op_ref_param(n, p_key=self.LOOP_N_SELF_KEY,
                              op_key=self.LOOP_N_REFKEY,
                              src=src, src_key=src_key or self.LOOP_N_SELF_KEY)

    def _handle_enter_input(self, this, srcE, obj, **refParams):
        if self._looping_count >= self.get_loop_n():
            return
        self._looping_count += 1
        self.trigger_all(self.BINDING_OUTPUT, obj)

    def _handle_reset_input(self, this, srcE, obj, **refParams):
        self._looping_count = 0

    def bind_exit_element(self, element, element_idx):
        self.bind_element(element, self.BINDING_OUTPUT, element_idx)


class DoOnce(DoN):

    BOOL_START_OPEN = 0
    BOOL_START_CLOSED = 1

    def set_start_closed(self, src=None, src_key=None):
        self.set_loop_n(self.BOOL_START_CLOSED, src, src_key)

    def set_start_open(self, src=None, src_key=None):
        self.set_loop_n(self.BOOL_START_OPEN, src, src_key)

    def get_loop_n(self, default=0):
        return bool(super(DoOnce, self).get_loop_n(default=default))

    def is_start_closed(self):
        return self.get_loop_n(self.BOOL_START_OPEN)


class FlipFlop(BaseFlow):

    PARAM_IS_A_KEY = 'is_a'

    BINDING_A_IDX = 1
    BINDING_B_IDX = 2

    def __init__(self, eventId, controller=None, **kwargs):
        super(FlipFlop, self).__init__(eventId, controller, **kwargs)
        self._is_a = False
        self.putArgument(self.PARAM_IS_A_KEY, self.is_a)
        self.regr_flow_handler(self._handle_flipflop, 1)

    def _handle_flipflop(self, this, srcE, obj, **referenceArgument):
        if not self._is_a:
            self._is_a = not self._is_a
            self.trigger_all(self.BINDING_A_IDX, obj)
        else:
            self._is_a = not self._is_a
            self.trigger_all(self.BINDING_B_IDX, obj)

    def is_a(self):
        return bool(self._is_a)

    def bind_a_element(self, element, element_idx):
        self.bind_element(element, self.BINDING_A_IDX, element_idx)

    def bind_b_element(self, element, element_idx):
        self.bind_element(element, self.BINDING_B_IDX, element_idx)


class BaseForLoop(BaseFlow, OptionInputParamMixin, OverOneTickMixin):

    FIRST_IDX_REFKEY = '_F_IDX'
    FIRST_IDX_SELF_KEY = '_F_IDX_S'
    LAST_IDX_REFKEY = '_L_IDX'
    LAST_IDX_SELF_KEY = '_L_IDX_S'
    LOOPING_COUNTERS_KEY = '_LC_S'

    ENTER_LOOP_BODY_IDX = 1

    BINDING_LOOP_BODY = 1
    BINDING_COMPLETE = 2

    def __init__(self, eventId, controller=None, **kwargs):
        super(BaseForLoop, self).__init__(eventId, controller, **kwargs)
        self._looping_counters = {}
        self.regr_flow_handler(self._handle_looping, self.ENTER_LOOP_BODY_IDX)
        self.putArgument(self.LOOPING_COUNTERS_KEY, self.get_looping_counters_copy)

    def get_looping_counters_copy(self):
        return {k: v for k, v in self._looping_counters.items()}

    def get_first_index(self, default=0):
        return int(self.get_op_ref_param(self.FIRST_IDX_REFKEY, default))

    def getLastIndex(self, default=0):
        return int(self.get_op_ref_param(self.LAST_IDX_REFKEY, default))

    def set_first_index(self, idx=0, src=None, src_key=None):
        self.set_op_ref_param(idx, p_key=self.FIRST_IDX_SELF_KEY,
                              op_key=self.FIRST_IDX_REFKEY,
                              src=src, src_key=src_key or self.FIRST_IDX_SELF_KEY)

    def set_last_index(self, idx=0, src=None, src_key=None):
        self.set_op_ref_param(idx, p_key=self.LAST_IDX_SELF_KEY,
                              op_key=self.LAST_IDX_REFKEY,
                              src=src, src_key=src_key or self.LAST_IDX_SELF_KEY)

    def _handle_looping(self, this, srcE, ctx, **refParams):
        fst_idx = self.get_first_index()
        self._looping_counters.setdefault(ctx.tid, fst_idx)
        i = self._looping_counters[ctx.tid]
        if i < fst_idx:
            del self._looping_counters[ctx.tid]
            return
        elif i > self.getLastIndex():
            try:
                self.trigger_all(self.BINDING_COMPLETE, ctx)
            finally:
                if ctx.tid in self._looping_counters:
                    del self._looping_counters[ctx.tid]
            return
        try:
            self.trigger_all(self.BINDING_LOOP_BODY, ctx)
        except Exception as e:
            # when trigger raise any exception, remove counter and raise
            # this exception outer scope
            if ctx.tid in self._looping_counters:
                del self._looping_counters[ctx.tid]
            raise e
        else:
            self._looping_counters[ctx.tid] += 1
            self.next(ctx, **refParams)

    def bind_loop_body(self, element, element_idx):
        self.bind_element(element, self.BINDING_LOOP_BODY, element_idx)

    def bind_complete(self, element, element_idx):
        self.bind_element(element, self.BINDING_COMPLETE, element_idx)


class BaseForLoopWithBreak(BaseForLoop):

    BREAK_LOOP_IDX = 2

    def __init__(self, eventId, controller=None, **kwargs):
        super().__init__(eventId, controller, **kwargs)
        self.regr_flow_handler(self._handle_break, self.BREAK_LOOP_IDX)
        self._looping_breakers = {}

    def _handle_break(self, this, srcE, ctx, **refParams):
        if not ctx or ctx.tid not in self._looping_counters:
            raise EP_ElementError('ctx not found in looping counters', self)
        self._looping_breakers[ctx.tid] = True

    def _handle_looping(self, this, srcE, ctx, **refParams):
        if self._looping_breakers.pop(ctx.tid, False):
            self._looping_counters.pop(ctx.tid, None)
            return
        return super()._handle_looping(self, srcE, ctx, **refParams)


class BaseWhileLoop(BaseFlow, OptionInputParamMixin, OverOneTickMixin):

    CONDITION_KEY = '_condition'

    ENTER_LOOP_BODY_IDX = 1

    BINDING_LOOP_BODY = 1
    BINDING_COMPLETE = 2

    def __init__(self, eventId, controller=None, **kwargs):
        super(BaseWhileLoop, self).__init__(eventId, controller, **kwargs)
        self.regr_flow_handler(self._handle_looping, self.ENTER_LOOP_BODY_IDX)

    def bind_condition(self, condition, key):
        self.referenceArgument(condition, key, self.CONDITION_KEY)

    def unbind_condition(self):
        self.unReferenceArgument(self.CONDITION_KEY)

    def rebind_condition(self, new_condition, key):
        self.unReferenceArgument(self.CONDITION_KEY)
        self.referenceArgument(new_condition, key, self.CONDITION_KEY)

    def _handle_looping(self, this, srcE, ctx, **refParams):
        # default whileloop condition should be true
        cond = self.get_ref_param(self.CONDITION_KEY, True)
        if not cond:
            self.trigger_all(self.BINDING_COMPLETE, ctx)
            return
        self.trigger_all(self.BINDING_LOOP_BODY, ctx)
        self.next(ctx, **refParams)

    def bind_loop_body(self, element, element_idx):
        self.bind_element(element, self.BINDING_LOOP_BODY, element_idx)

    def bind_complete(self, element, element_idx):
        self.bind_element(element, self.BINDING_COMPLETE, element_idx)


class Sequence(BaseFlow):
    def __init__(self, eventId, controller=None, **kwargs):
        super().__init__(eventId, controller, **kwargs)
        self.regr_flow_handler(self._handle_sequence, 1)

    def _handle_sequence(self, this, srcE, ctx, **refParams):
        for idx in sorted(self._binded_dic.keys()):
            self.trigger_all(idx)


class Gate(BaseFlow, OptionInputParamMixin):

    BOOL_START_OPEN = False
    BOOL_START_CLOSED = True

    ENTER_IDX = 1
    OPEN_IDX = 2
    CLOSE_IDX = 3
    TOGGLE_IDX = 4

    BINDING_OUTPUT = 1

    GATE_START_CLOSED_REFKEY = '_START_CLOSED'
    GATE_START_CLOSED_SELF_KEY = '_START_CLOSED_S'

    def __init__(self, eventId, controller=None, **kwargs):
        super().__init__(eventId, controller, **kwargs)
        self.regr_flow_handler(self._handle_enter, self.ENTER_IDX)
        self.regr_flow_handler(self._handle_open, self.OPEN_IDX)
        self.regr_flow_handler(self._handle_close, self.CLOSE_IDX)
        self.regr_flow_handler(self._handle_toggle, self.TOGGLE_IDX)
        self._closed_flag = None  # in default, start_closed not set

    def set_start_closed(self):
        self.set_start_status(status=self.BOOL_START_CLOSED)

    def set_start_open(self):
        self.set_start_status(status=self.BOOL_START_OPEN)

    def set_start_status(self, status=False, src=None, src_key=None):
        self.set_op_ref_param(
            status,
            p_key=self.GATE_START_CLOSED_SELF_KEY,
            op_key=self.GATE_START_CLOSED_REFKEY,
            src=src, src_key=src_key or self.GATE_START_CLOSED_SELF_KEY)

    def is_start_closed(self):
        return bool(self.get_op_ref_param(self.GATE_START_CLOSED_REFKEY,
                                          self.BOOL_START_OPEN))

    def _handle_enter(self, this, srcE, obj, **refParams):
        if self._closed_flag is None:
            self._closed_flag = True if self.is_start_closed() else False

        if self._closed_flag:
            return

        self.trigger_all(self.BINDING_OUTPUT, obj)

    def _handle_open(self, this, srcE, obj, **refParams):
        self._closed_flag = False

    def _handle_close(self, this, srcE, obj, **refParams):
        self._closed_flag = True

    def _handle_toggle(self, this, srcE, obj, **refParams):
        if self._closed_flag is None:
            self._closed_flag = True if self.is_start_closed() else False
        self._closed_flag = not self._closed_flag

    def bind_exit_element(self, element, element_idx):
        self.bind_element(element, self.BINDING_OUTPUT, element_idx)
