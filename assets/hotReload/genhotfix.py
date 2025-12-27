# -*- coding: utf-8 -*-
import sys
import os
import ast,symtable
import re
import itertools
import methodInfo as MI
import const

INDENT = ' '*4

IMPORT_PT = re.compile(r'import\s+([a-zA-Z0-9_]+)')
IMPORT_AS_PT = re.compile(r'import\s+.+\s+as\s+([a-zA-Z0-9_]+)')
MULTI_IMPORT_PT = re.compile(
    r"(?:^|\n)\s*import\s+([ \t]*[A-Za-z_][A-Za-z0-9_]*"
    r"(?:\s*,\s*[A-Za-z_][A-Za-z0-9_]*)*)\s*(?:\n|$|;)",
    re.M
)


NEW_METHOD_BEGIN_MARK = '# --auto genterate mark--'

def getImportInfo(methodInfo:MI.MethodInfo):
    importLines = []
    fileObject = open(methodInfo.codePath, 'rb')
    if not fileObject:
        return importLines

    func = methodInfo.symtable.lookup(methodInfo.name).get_namespace()
    funcGlobals = func.get_globals()

    importedMods = ['KBEngine']
    for line in fileObject:
        strLine = line.decode('utf-8', 'ignore')
        if strLine.strip().startswith('#'):
            continue

        matchMultiImport = MULTI_IMPORT_PT.search(strLine)
        if matchMultiImport:
            modules = matchMultiImport.group(1).split(',')
            for mod in modules:
                mod = mod.strip()
                if mod in funcGlobals:
                    importLines.append(strLine.replace('\r\n', '\n').lstrip())
                    importedMods.append(mod)

            continue

        matchImport = IMPORT_AS_PT.search(strLine) or IMPORT_PT.search(strLine)
        if matchImport:
            moduleName = matchImport.groups()[0].strip()
            if moduleName in funcGlobals:
                importLines.append(strLine.replace('\r\n', '\n'))
                importedMods.append(moduleName)

            continue


    #dealing @utils.isMySelf
    for decMod in methodInfo.decratorMods:
        if decMod not in importedMods:
            importLines.append('import {}\n'.format(decMod))

    importLines.append('import {}\n'.format(methodInfo.inModuleName))

    fileObject.close()
    return importedMods, importLines

def setupSysPath(component):
    if component == const.CELLAPP:
        sys.path.extend(const.CELL_PATH)
    elif component == const.BASEAPP:
        sys.path.extend(const.BASE_PATH)
    elif component == const.INTERFACE:
        sys.path.extend(const.INTERFACE_PATH)
    else:
        print("supported components: {}|{}".format(const.CELLAPP, const.BASEAPP))
        exit(1)

def appendNewMethod(scriptPath, component, newMethodLines):
    newScriptLines = []
    with open(scriptPath, 'r', encoding='utf-8') as fScript:
        inTargetBlock = False
        done = False
        for line in fScript.readlines():
            if done:
                newScriptLines.append(line)
                continue
            if re.search(r'\brefreshCell\b', line):
                inTargetBlock = (component==const.CELLAPP)
            elif re.search(r'\brefreshBase\b', line):
                inTargetBlock = (component==const.BASEAPP)
            elif re.search(r'\brefreshInterface\b', line):
                inTargetBlock = (component==const.INTERFACE)

            if inTargetBlock and NEW_METHOD_BEGIN_MARK in line:
                newScriptLines.extend(['{}{}'.format(INDENT, nl) for nl in newMethodLines])
                newScriptLines.append('\n')
                done = True

            newScriptLines.append(line)

        if not done:
            print('error:cannot find target block')
            return False

    with open(scriptPath, 'w', encoding='utf-8') as fScript:
        for line in newScriptLines:
            fScript.writelines([line])

    return True


def generateCode(scriptPath, component, moduleName, clsName, methodName):
    info = MI.MethodInfo(component, moduleName, clsName, methodName)
    importedMods, resultLines = getImportInfo(info)
    resultLines.append('\n')

    fSource = open(info.codePath, 'r', encoding='utf-8')
    src = fSource.read()
    fSource.close()
    srcSym = symtable.symtable(src, info.codePath, 'exec')

    replaceGlobals = {}

    #find local defined module variable
    func = info.symtable.lookup(info.name).get_namespace()
    funcGlobals = func.get_globals()
    for var in funcGlobals:
        try:
            sb = srcSym.lookup(var)
        except:
            continue

        if sb.is_imported():
            assert var in importedMods

        if sb.is_assigned():
            replaceGlobals[sb.get_name()] = '{}.{}'.format(info.inModuleName, sb.get_name())

    #replace module variable
    for old, new in itertools.chain(replaceGlobals.items(), info.replaceDecorator.items()):
        info.replaceSymbol(old, new)

    resultLines.extend(info.sourceLines)

    #assign method finally
    if info.checkClassValid():
        resultLines.append('{}.{}.{} = {}\n'.format(moduleName, clsName, methodName, methodName))
        #resultLines.append("hotpatch_method({}.{}, '{}', {})\n".format(moduleName, clsName, methodName, methodName))
    else:
        resultLines.append('{}.{} = {}\n'.format(moduleName, methodName, methodName))

    #write to hotReload.py
    if appendNewMethod(scriptPath, component, resultLines):
        print('generate complete!')



if __name__ == "__main__":
    if len(sys.argv)==5:
        component = sys.argv[1]
        module = sys.argv[2]
        cls = sys.argv[3]
        method = sys.argv[4]
    elif len(sys.argv)==4:
        component = sys.argv[1]
        module = sys.argv[2]
        cls = ''
        method = sys.argv[3]
    else:
        print("fix class method usage: genhotfix.py component, module, class, method")
        print("fix module method usage: genhotfix.py component, module, method")
        exit(1)

    targetFile = '../scripts/server_common/hotReload.py'

    setupSysPath(component)
    generateCode(targetFile, component, module, cls, method)





