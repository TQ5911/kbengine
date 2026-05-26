# -*- encoding:utf-8 -*-

import ai.py_trees as py_trees

class BehaviourMeta(type):
    def __new__(cls, name, bases, namespace, **kwargs):
        new_cls = super(BehaviourMeta, cls).__new__(cls, name, bases, namespace, **kwargs)
        oringinInit = new_cls.__init__
        def __init__(self, name='', args=(), aiController=None):
            oringinInit(self, name)
            # self.aiController = aiController
            self.args = args

        def udpate(self, treeOwner):
            method = getattr(treeOwner, self.method, None)
            if method:
                return method(*self.args)
            else:
                raise Exception('monster behaviour failed: %s'%self.method)



        setattr(new_cls, '__init__', __init__)
        setattr(new_cls, 'update', udpate)

        return new_cls

class BehaviourMetaCustom(type):
    def __new__(cls, name, bases, namespace, **kwargs):
        new_cls = super(BehaviourMetaCustom, cls).__new__(cls, name, bases, namespace, **kwargs)
        oringinInit = new_cls.__init__
        def __init__(self, name='', args=(), aiController=None, method=None):
            oringinInit(self, name)
            # self.aiController = aiController
            self.args = args
            self.outMethod = method
            #print('self.outMethod--------------------------------------------', self.outMethod)

        def udpate(self, treeOwner):
            if self.outMethod:
                return self.outMethod(treeOwner)

        setattr(new_cls, '__init__', __init__)
        setattr(new_cls, 'update', udpate)

        return new_cls

class ConditionMeta(type):
    def __new__(cls, name, bases, namespace, **kwargs):
        new_cls = super(ConditionMeta, cls).__new__(cls, name, bases, namespace, **kwargs)
        oringinInit = new_cls.__init__
        def __init__(self, name='', args=(), aiController=None):
            oringinInit(self, name)
            # self.aiController = aiController
            self.args = args

        def externalCondition(self, treeOwner):
            method = getattr(treeOwner, self.method)
            if method:
                return method(*self.args)
            else:
                raise Exception('monster behaviour failed: %s'%self.method)

        setattr(new_cls, '__init__', __init__)
        setattr(new_cls, 'externalCondition', externalCondition)

        return new_cls

class ConditionMetaCustom(type):
    def __new__(cls, name, bases, namespace, **kwargs):
        new_cls = super(ConditionMetaCustom, cls).__new__(cls, name, bases, namespace, **kwargs)
        oringinInit = new_cls.__init__
        def __init__(self, name='', args=(), aiController=None, method=None):
            oringinInit(self, name)
            # self.aiController = aiController
            self.args = args
            self.outMethod = method
            #print('self.outMethod--------------------------------------------', self.outMethod)

        def externalCondition(self, treeOwner):
            #print('externalCondition--------------------------------------------', self.outMethod)
            if self.outMethod:
                # method = self.outMethod
                # testFunction = lambda self = self.aiController.owner, outMethod = self.outMethod: eval(outMethod)
                return self.outMethod(treeOwner)
            else:
                method = getattr(treeOwner, self.method)
                if method:
                    return method(*self.args)
                else:
                    raise Exception('monster behaviour failed: %s'%self.method)

        setattr(new_cls, '__init__', __init__)
        setattr(new_cls, 'externalCondition', externalCondition)

        return new_cls

class Patrol(py_trees.behaviour.Behaviour, metaclass=BehaviourMeta):
    method = 'patrol'

class StopPatrol(py_trees.behaviour.Behaviour, metaclass=BehaviourMeta):
    method = 'stopPatrol'

class Relive(py_trees.behaviour.Behaviour, metaclass=BehaviourMeta):
    method = 'relive'

class Attack(py_trees.behaviour.Behaviour, metaclass=BehaviourMeta):
    method = 'attack'


#condition节点
class ShouldPatrol(py_trees.composites.Condition, metaclass=ConditionMeta):
    method = 'shouldPatrol'

class ShouldStopPatrol(py_trees.composites.Condition, metaclass=ConditionMeta):
    method = 'shouldStopPatrol'

class IsDead(py_trees.behaviour.Behaviour, metaclass=BehaviourMeta):
    method = 'isDead'

class ShouldAttack(py_trees.composites.Condition, metaclass=ConditionMeta):
    method = 'shouldBotAttack'
