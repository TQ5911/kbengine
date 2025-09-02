# -*- coding: utf-8 -*-
import sys
import os
import ast,symtable
import re
import inspect
import astor
import const


indentPt = re.compile(r'(\s*)')

def prettySource(items):
    res = ''.join(items)
    return res

class MethodInfo(object):
    def __init__(self, component, moduleName, clsName, methodName):
        self.compoent = component
        self.inModuleName = moduleName
        self.classname = clsName
        self.name = methodName
        self.sourceLines = None
        self.sourceCode = ''
        self.symtable = None
        self.codePath = ''
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
        if self.compoent == const.BASEAPP:
            pathList = const.BASE_PATH
        elif self.compoent == const.CELLAPP:
            pathList = const.CELL_PATH
        else:
            pathList = const.INTERFACE_PATH

        for folder in pathList:
            testPath = os.path.join(folder, '{}.py'.format(self.inModuleName))
            if os.path.exists(testPath):
                self.codePath = testPath
                break

        with open(self.codePath, 'r', encoding='utf-8') as fScript:
            script = fScript.read()
            scriptAst = ast.parse(script)
            for node in scriptAst.body:
                if self.checkClassValid():#class member function
                    if isinstance(node, ast.ClassDef) and node.name==self.classname:
                        for cNode in node.body:
                            if isinstance(cNode, ast.FunctionDef) and cNode.name==self.name:
                                self.sourceCode = astor.to_source(cNode, pretty_source=prettySource)
                                self.sourceLines = [line+'\n' for line in self.sourceCode.split('\n')]
                                self.symtable = symtable.symtable(self.sourceCode, 'string', 'exec')
                                break
                        break
                else:#module function
                    if isinstance(node, ast.FunctionDef) and node.name==self.name:
                        self.sourceCode = astor.to_source(node, pretty_source=prettySource)
                        self.sourceLines = [line+'\n' for line in self.sourceCode.split('\n')]
                        self.symtable = symtable.symtable(self.sourceCode, 'string', 'exec')

            if not self.sourceCode:
                if self.classname:
                    print('method not found: {}.{}.{}'.format(self.inModuleName, self.classname, self.name))
                else:
                    print('method not found: {}.{}'.format(self.inModuleName, self.name))
                exit(-1)


        methodAst = ast.parse(self.sourceCode)

        for node in methodAst.body:
            if isinstance(node, ast.FunctionDef):
                for decInfo in node.decorator_list:
                    if isinstance(decInfo, ast.Name):
                        self.decratorMods.add(self.inModuleName)
                        self.replaceDecorator['@'+decInfo.id] = '@{}.{}'.format(self.inModuleName, decInfo.id)
                    elif isinstance(decInfo, ast.Call):
                        self.decratorMods.add(decInfo.func.value.id)
                    else:
                        self.decratorMods.add(decInfo.value.id)

    def replaceSymbol(self, old, new):
        for i, line in enumerate(self.sourceLines):
            self.sourceLines[i] = re.sub(r'\b{}\b'.format(old), new, line)

        self.sourceCode = '\n'.join(self.sourceLines)

