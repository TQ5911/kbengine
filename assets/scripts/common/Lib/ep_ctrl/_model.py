#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#
# Distributed under terms of the MIT license.

""" _model中包含所有基础Element类定义"""

from __future__ import unicode_literals, division
# hook dict as OrderedDict
from collections import OrderedDict as dict
from functools import wraps

from .exceptions import EP_ElementError, EP_ElementCheckerError
from .utils import EMPTY_FUNC, api_need_implement


class _BindData(object):
    def __init__(self, idx, e, e_idx):
        self.org_idx = idx
        self.element = e
        self.element_idx = e_idx



def stopped_cancel_trigger(fn):
    @wraps(fn)
    def __(self, *args, **kwargs):
        if self.stopped:
            return
        return fn(self, *args, **kwargs)
    return __


class _BasicElement(object):
    """ 所有Element都从该类继承, 每个element都被划分为以下部分::

    * input - 被触发部分
    * struc - element本身包含的部分
    * output - 触发部分

    output含有多个触发脚(element_idx), 每个触发角可以绑定多个Element,
    可以选择触发同一个element_idx上的一个或者多个Element, 或者触发
    多个element_idx的一个或多个Element, 具体触发取决于具体实现

    input决定了被触发时的行为, 被触发时可以通过
    :py:meth:`_BasicElement.get_ref_param` 取得多个可选参数的值在触发方法中使用

    struc本身含有param字典, 可以在Element本身注册 ``key:value`` 键对值,
    可以绑定如 ``{'foo': 'bar'}`` 或者绑定一个无参方法, 如
    ``{'foo', mo.obj.demo_func}`` , 获得该param会自动调用 ``demo_func()`` 

    组件触发关系如下
        PE -Out-> -In-> E -Out-> ...

    :cvar tuple __self_params__: 自检参数元组, 写入该元组中的参数在调用
        :py:meth:`_BasicElement.self_check` 时会被强制检查是否被赋值, 没有赋值会抛出
        :py:exc:`ep_ctrl.exceptions.EP_ElementCheckerError` 异常
    :cvar tuple __ref_params__: 自检引用参数元组, 使用方法同 
            :py:attr:`_BasicElement.__self_params__` 相同

    :ivar int _element_id: Element唯一标识.
    :ivar str _element_name: Element名字
    :ivar dict _params: Element本身所有属性, 可以绑定一个值或者方法
    :varType _params: dict[str, ``object`` or ``callable_obj`` ]
    :ivar Controller _controller: Element所属Controller
    :varType _controller: :py:class:`ep_ctrl.controller.Controller`
    :ivar dict _be_bind_dic: 被绑定Element关系字典
    :varType _be_bind_dic: dict[e_idx(被绑定触发角id), dict[eid, :py:class:`_BindData` ]]
    :ivar dict _ref_params_dic: 被触发时可以引用的外部绑定参数
    :varType _ref_params_dic: dict[ref_name, tuple[ ``Element`` , ``e_name`` ]]
    :ivar dict _binded_dic: 绑定的Element关系字典
    :varType _binded_dic: dict[e_idx, dict[eid, :py:class:`_BindData` ]]
    """

    __self_params__ = ()
    __ref_params__ = ()

    def __init__(self, event_id, controller, name=None, **kwargs):

        def _get_name():
            if not name:
                return "{}_{}".format(
                        self.__class__.__name__, event_id)
            return name

        name = _get_name()
        # general attributes
        self._element_id = event_id
        self._element_name = name
        self.rename(name)
        self._params = dict()
        self._controller = controller
        # inputside __init__
        self._be_bind_dic = {}
        self._ref_params_dic = {}
        # outputside __init__
        self._binded_dic = {}
        # regr to controller
        self._controller and self._controller.regr_element(self)

    @property
    def id(self):
        """ Element ID
        
        :return: element id
        :rtype: :py:attr:`_BasicElement._element_id` 
        """
        return self._element_id


    @property
    def name(self):
        """ Element Name

        :return: element name
        :rtype: :py:attr:`_BasicElement._element_name`
        """
        return self._element_name

    @property
    def controller(self):
        """ Element Controller
        
        :return: element controller
        :rtype: :py:attr:`_BasicElement._controller`
        """
        return self._controller

    def rename(self, new_name, no_eid=False):
        if not new_name:
            return
        elif new_name.endswith('_{}'.format(self._element_id)) or no_eid:
            self._element_name = new_name
        else:
            self._element_name = "{}_{}".format(new_name, self._element_id)

    @property
    def stopped(self):
        """ Stopped check flag
        
        :retrun: stopped flag
        :rtype: bool
        """
        if not self._controller:
            return False
        return self._controller.stopped

    def add_param(self, key, getter):
        """ Add an element param
        
        :param str key: param name
        :param getter: param value
        :type getter: variable or function/method
        """
        self._params[key] = getter

    def get_param(self, key, default=None):
        """ Get an element param
        
        :param str key: param name
        :param default: default value
        :return: param value or default
        """
        if key not in self._params:
            return default
        getter = self._params.get(key, EMPTY_FUNC)
        r = getter() if callable(getter) else getter
        return r

    def has_param(self, key):
        """ Check has param in element

        :param str key: param key
        :return: is param key in element params
        :rtype: bool
        """
        return key in self._params

    def bind_element(self, e, idx, e_idx):
        """Bind Element which need to be triggered by self::

          +--------------+        +--------------------+
          |-- self --idx1-----+   |e_idx1-- binded e --|
          |--      --idx2|    +--->e_idx2--          --|
          +--------------+        +--------------------+

        :param Element e: element to be bind
        :type e: :py:class:`_BasicElement`: or its subclass
        :param int idx: self binded idx
        :param int e_idx: be binbed element idx
        """
        self._binded_dic.setdefault(idx, dict())
        eid = e.id
        if eid in self._binded_dic[idx]:
            raise EP_ElementError(
                'repeated bind element, {}'.format(idx), self)
        e._be_binded_element(self, idx, e_idx)
        self._binded_dic[idx][e.id] = _BindData(idx, e, e_idx)

    def _be_binded_element(self, src_e, src_idx, idx):
        self._be_bind_dic.setdefault(src_idx, {})
        self._be_bind_dic[src_idx][src_e.id] \
            = _BindData(idx, src_e, src_idx) 

    def is_binded(self, eid, idx=None):
        """ Check eid has binded

        :param int eid: element id
        :param idx: check with special bind idx, if this param is None,
            all element binded pool will be checked.
        :type idx: int or None
        :return: eid has binded
        :rtype: bool
        """
        return self._is_binded_noidx(eid) if idx is None else \
            self._is_binded(eid, idx)

    def _is_binded_noidx(self, eid):
        for _id, _dic in self._binded_dic.items():
            if eid in _dic:
                return True
        return False

    def _is_binded(self, eid, idx):
        _dic = self._binded_dic.get(idx)
        if _dic and eid in _dic:
            return True
        return False

    def is_be_bind(self, eid, idx=None):
        """ Check eid has be binded

        :param int eid: element id
        :param idx: check with special be binded idx
        :type idx: int or None
        :return: eid is be binded 
        :rtype: bool
        """
        return self._is_be_bind_noidx(eid) if idx is None else \
            self._is_be_bind(eid, idx)

    def _is_be_bind_noidx(self, eid):
        for _id, _dic in self._be_bind_dic.items():
            if eid in _dic:
                return True
        return False

    def _is_be_bind(self, eid, idx):
        _dic = self._be_bind_dic.get(idx)
        if _dic and eid in _dic:
            return True
        return False

    def unbind_element(self, eid, idx=None):
        """ unbind element by element id
        
        :param int eid: element id
        :param idx: unbined eid's element pool idx, if set None,
            all poll will be found and unbind.
        :type idx: None or int
        """
        if idx is None:
            self._unbind_element_noidx(eid)
        else:
            self._unbind_element(eid, idx)

    def _unbind_element_noidx(self, eid):
        for _id, _dic in self._binded_dic.items():
            if eid in _dic:
                self._unbind_element(eid, _id)
            
    def _unbind_element(self, eid, idx):
        if idx not in self._binded_dic:
            return 
        e = self._binded_dic[idx].pop(eid, None)
        e and e.element._be_unbinded_element(self.id, idx, e.element_idx)

    def _be_unbinded_element(self, src_eid, src_idx, idx):
        if src_idx not in self._be_bind_dic:
            return 
        self._be_bind_dic[src_idx].pop(src_eid, None)

    def ref_param(self, src, src_key, key):
        """ Reference param to self::

             <TRIGGERED_E> ----------+
                                     |
          +-----------------+        |      +---------------+
          |---  src  -------|        +--|---->      self ---|
          |--- -param(src_key) ---------|-> ref_key --------| 
          +-----------------+               +---------------+

        :param src: refrence source element
        :type src: :py:class:`_BasicElement` or its subclass
        :param str src_key: ref source element param key
        :param str key: self reference key
        :raises EP_ElementError: if ref param failed
        """
        if key in self._ref_params_dic:
            raise EP_ElementError(
                'Cannot bind param, duplicate key define: {}'.format(key),
                self)
        if not src.has_param(src_key):
            raise EP_ElementError(
                'Cannot bind param, src param not define, {}'.format(src_key),
                self)
        self._ref_params_dic[key] = (src, src_key)
   
    def unref_param(self, key):
        """ Un-reference param
        
        :param str key: unref key
        """
        self._ref_params_dic.pop(key, None)

    def get_ref_param(self, key, default=None):
        """ get reference param value

        :param str key: ref key
        :param default: default value when not found ref value
        :return: ref_value or default
        """
        src, src_key = self._ref_params_dic.get(key, (None, None))
        if src is None:
            return default
        return src.get_param(src_key, default)

    def has_ref_param(self, key):
        """ Check ref key defined in ``ref_params`` """
        return key in self._ref_params_dic

    def _pkg_all_ref_params(self):
        result = {}
        for key, (src, src_key) in self._ref_params_dic.items():
            val = src.get_param(src_key)
            result.update({key: val})
        return result

    @stopped_cancel_trigger
    def trigger_all(self, idx, obj=None):
        """ Trigger all binded elements in given idx
        
        :param int idx: triggered element pool idx
        :param BaseContext obj: triggered context, in most of time
        it's optional, but in some cases like :py:class:`BaseVar` ,
        context is mandatory param.
        """
        for e in self._binded_dic.get(idx, {}).values():
            self._trigger(e, obj)

    @stopped_cancel_trigger
    def trigger(self, idx, eid, obj=None):
        """ Tirgger special element in given idx

        :param int idx: triggered element pool idx
        :param int eid: triggered element id
        :param BaseContext obj: tiggered context
        """
        e = self._binded_dic.get(idx, {}).get(eid, None)
        self._trigger(e, obj)

    def _trigger(self, e, obj):
        e.element.be_triggered(self, e.org_idx, e.element_idx, obj)

    @stopped_cancel_trigger
    def be_triggered(self, src_e, src_idx, idx, obj):
        if not self.is_be_bind(src_e.id, src_idx):
            raise EP_ElementError(
                'Cannot be triggered, src is not be bind, {}'.format(src_e.id),
                self)
        return self.handle_be_triggered(
            src_e, src_idx, idx, obj, **self._pkg_all_ref_params())

    @api_need_implement
    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        """be triggered handler, implement in subclass::

            src_e ------+           +-----------------
                  src_idx1 --+      |        e -> handle_be_triggerd
                  src_idx2   +--obj---> idx1 ---> idx |
                  ....  |           |   idx2          |
            ------------+           |  ...            +--+
                               +-----> ref_1| ref_params |
                    ref_d------+  +--> ref_2|
                                  | |  ...
                                  | +-------------------
                                ...

        :param src_e: source element
        :type src_e: :py:class:`_BasicElement` or its subclass
        :param int src_idx: source element pool idx
        :param int idx: self element idx
        :param BaseContext obj: triggered context
        :param **ref_params: kv pairs of reference params
        """

    def self_check(self):
        """ Check self is valid 
        
        :raise EP_ElementCheckerError: if param define in 
            :py:attr:`_BasicElement.__self_params__` or ref_param define in 
            :py:attr:`_BasicElement.__ref_params__` not found.
        :return: self element id
        :rtype: :py:attr:`_BasicElement.id`
        """
        self._check_params()
        self._check_refparams()
        return self._element_id

    def _check_params(self):
        for p in self.__self_params__:
            if p not in self._params:
                raise EP_ElementCheckerError(
                    'check params failed, {} not found'.format(p), self)

    def _check_refparams(self):
        for p in self.__ref_params__:
            if p not in self._ref_params_dic:
                raise EP_ElementCheckerError(
                    'check ref params failed, {} not found'.format(p), self)


class OptionInputParamMixin(object):
    """Option input param mixin class extend origin element to support 
       optional input param.

       E.G.1: self bind: ``E1(p1) --> E2(ref_1)``   

       E.G.2: ref bind:  ``E2(p1) --> E2(ref_1)`` 
    """

    def get_op_ref_param(self, op_key, default=None):
        """get optional reference param
        
        :param str op_key: option param key
        :default: default value
        :return: op_ref value or default value
        """
        return self.get_ref_param(op_key, default)

    def set_op_ref_param(self, d=None, p_key=None, op_key=None,
                         src=None, src_key=None):
        """set optional reference param::

          - no src:
              +--------E--------
          +--------p_key->d(param)
          |   |
          +->op_key(ref_param)
              +-----------------

          - src:
            +--------------+       +-------E----
            |src  src_key------> op_key
            +--------------+       +------------

        :param d: param value, failed if ``src`` set
        :param str p_key: self binded key, failed if `src` set
        :param str op_key: reference key
        :param src: source element, if src set, self bind will be failed
        :type src: :py:class:`_BasicElement` or its subclass
        :param str src_key: source element key
        """
        self.unref_param(op_key)
        self.ref_param(src, src_key, op_key) if src else \
            self._set_op_ref_param(d, p_key, op_key)

    def _set_op_ref_param(self, d, p_key, op_key):
        self.add_param(p_key, d)
        self.ref_param(self, p_key, op_key)


class OverOneTickMixin(object):
    
    def next(self, ctx, **ref_params):
        """ Next triggered API

        ``next`` 方法适用于多帧操作情况, 根据不同逻辑实现next方法, 达到
        多帧操作Element.

        E.G. 令全局方法 ``_callback`` 可以将设置X秒后回调, 实现方法:

            def next(self, ctx, **ref_params):
                _callback(delay=1, obj=self, func_name='handle_be_triggered',
                          func_args=(self, 1, 1, ctx), func_kwargs=ref_params)

        :param BaseContext ctx: element context
        :param **ref_params: kv pairs for reference params values
        """
        raise NotImplementedError('loop next action not define')


class _SingleHandlerMixin(object):

    def _regr_handler(self, handler):
        if not callable(handler):
            raise TypeError(
                '{} handle must be callable'.format(self.__class__.__name__))
        self._handler = handler


class BaseEvent(_BasicElement, _SingleHandlerMixin):
    """event base class, all events subclass must inherited from
       this basic class::
       
      INPUT:
        1. ref params: when be triggered, those params will be package 
           as ``**kwargs`` and be afferent into ``handle_be_triggered`` method.
        2. be_binded map: record be binded elements

      ORIGIN:
        1. params: regr params for elements self, param value can be directly
           var or a called function/obj with no position args.
        2. id: element identify id.             
      
      OUTPUT: 
           binded dic: record binded elements
    
    :cvar EVENT_BIND_IDX: event bind idx
    
    :ivar function _handler: event handler function
    
    E.G. handler function::

        def something_handler(this_element, source_element, context, **ref_params):
            ...
        
    """

    EVENT_BIND_IDX = 1

    def __init__(self, event_id, controller, event_handler=None, **kwargs):
        super().__init__(event_id, controller, **kwargs)
        self._handler = EMPTY_FUNC
        if event_handler is not None:
            self.regr_event_handler(event_handler)

    def regr_event_handler(self, event_handler):
        """ registry event handler
        
        event_handler must have these params::

            - self_e
            - src_e
            - context
            - **ref_params

        :param event_handler: callbale object
        """
        self._regr_handler(event_handler)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        self._handler(self, src_e, obj, **ref_params)


class _MultiHandlersMixin(object):

    def _regr_handler(self, handler, inputing_idx):
        if not callable(handler):
            raise TypeError(
                '{} handle must be callable'.format(self.__class__.__name__))
        self._handlers[inputing_idx] = handler


class BaseFlow(_BasicElement, _MultiHandlersMixin):
    """flow base class, all flow controller must inherited from
       this basic class
    """ 

    def __init__(self, event_id, controller, **kwargs):
        super().__init__(event_id, controller, **kwargs)
        self._handlers = {}

    def regr_flow_handler(self, flow_handler, inputing_idx):
        """ registry flow handler
        
                +---------F-----------+
            ---idx1--> flow_handler_1 --> 
            ---idx2--> flow_handler_2 --> ...
              ----> ...               |
                +---------------------+

        :param flow_handler: callabale object 
        :param inputing_idx: handled element triggered pool idx
        """
        self._regr_handler(flow_handler, inputing_idx)

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        if idx not in self._handlers:
            raise AttributeError(
                'Cannot be triggered flow, handler not found '
                '{} -> {}'.format(src_idx, idx))
        self._handlers[idx](self, src_e, obj, **ref_params)


class BaseVar(_BasicElement):
    """ 基础变量类, 所有变量相关实现需要继承 :py:class:`BaseVar` 
    
    :ivar str _var_name: regr variable name
    """

    def __init__(self, eid, controller, var_name, **kwargs):
        if not controller:
            raise TypeError(
                '{} must set controller'.format(self.__class__.__name__))
        super().__init__(eid, controller, **kwargs)
        self._var_name = var_name
        self.add_param(var_name, self._get_variable)

    @property
    def var_name(self):
        return self._var_name

    @property
    def var_value(self):
        if not self.has_param(self._var_name):
            raise KeyError(
                'var {} not in self param'.format(self._var_name))
        if not self._controller.has_variable(self._var_name):
            raise KeyError(
                'var {} not define in global'.format(self._var_name))
        return self.get_param(self._var_name)

    def _get_variable(self):
        return self._controller.get_variable(self._var_name)
