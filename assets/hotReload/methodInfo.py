# -*- coding: utf-8 -*-
import sys
import os
import ast,symtable
import re
import astor
import const


indentPt = re.compile(r'(\s*)')

def prettySource(items):
    res = ''.join(items)
    return res

def _attrLeftName(node):
    while isinstance(node, ast.Attribute):
        node = node.value
    return node.id if isinstance(node, ast.Name) else None

class MethodInfo(object):
    def __init__(self, component, moduleName, clsName, methodName):
        self.inModuleNameData = moduleName
        self.compoent = component
        self.classname = clsName
        self.name = methodName
        self.sourceLines = None
        self.sourceCodeData = ''
        self.codePath = ''
        self.symtable = None
        self.decratorMods = set()

        self.replaceDecorator = {}

        self.init()

    def checkClassValid(self):
        if not self.classname:
            return False

        if self.classname == 'None':
            return False

        return True

    def init(self):
        if self.compoent == const.CELLAPP:
            pathList = const.CELL_PATH
        elif self.compoent == const.BASEAPP:
            pathList = const.BASE_PATH
        else:
            pathList = const.INTERFACE_PATH

        for _folder in pathList:
            _testPath = os.path.join(_folder, '{}.py'.format(self.inModuleNameData))
            if os.path.exists(_testPath):
                self.codePath = _testPath
                break

        with open(self.codePath, 'r', encoding='utf-8') as fScript:
            _script = fScript.read()
            scriptAst = ast.parse(_script)
            for _node in scriptAst.body:
                if self.checkClassValid():#class member function
                    if isinstance(_node, ast.ClassDef) and _node.name==self.classname:
                        for _cNode in _node.body:
                            if isinstance(_cNode, ast.FunctionDef) and _cNode.name==self.name:
                                self.sourceCodeData = astor.to_source(_cNode, pretty_source=prettySource)
                                self.sourceLines = [_line+'\n' for _line in self.sourceCodeData.split('\n')]
                                self.symtable = symtable.symtable(self.sourceCodeData, 'string', 'exec')
                                break
                        break
                else:#module function
                    if isinstance(_node, ast.FunctionDef) and _node.name==self.name:
                        self.sourceCodeData = astor.to_source(_node, pretty_source=prettySource)
                        self.sourceLines = [_line+'\n' for _line in self.sourceCodeData.split('\n')]
                        self.symtable = symtable.symtable(self.sourceCodeData, 'string', 'exec')

            if not self.sourceCodeData:
                if self.classname:
                    print('method not found: {}.{}.{}'.format(self.inModuleNameData, self.classname, self.name))
                else:
                    print('method not found: {}.{}'.format(self.inModuleNameData, self.name))
                exit(-1)


        methodAst = ast.parse(self.sourceCodeData)

        for _node in methodAst.body:
            if isinstance(_node, ast.FunctionDef):
                for decInfo in _node.decorator_list:
                    if isinstance(decInfo, ast.Name):
                        self.decratorMods.add(self.inModuleNameData)
                        self.replaceDecorator['@'+decInfo.id] = '@{}.{}'.format(self.inModuleNameData, decInfo.id)
                    elif isinstance(decInfo, ast.Call):
                        self.decratorMods.add(_attrLeftName(decInfo.func))
                        for arg in decInfo.args:
                            name = _attrLeftName(arg)
                            if name:
                                self.decratorMods.add(name)
                        for kw in decInfo.keywords:
                            name = _attrLeftName(kw.value)
                            if name:
                                self.decratorMods.add(name)
                    else:
                        self.decratorMods.add(decInfo.value.id)

    def replaceSymbol(self, old, new):
        for i, _line in enumerate(self.sourceLines):
            self.sourceLines[i] = re.sub(r'\b{}\b'.format(old), new, _line)

        self.sourceCodeData = '\n'.join(self.sourceLines)

