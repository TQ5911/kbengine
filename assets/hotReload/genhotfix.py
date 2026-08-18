# -*- coding: utf-8 -*-
import sys
import ast,symtable
import re
import itertools
import const
import methodInfo as MI

INDENT = ' '*4

IMPORT_PT = re.compile(r'import\s+([a-zA-Z0-9_]+)')
IMPORT_AS_PT = re.compile(r'import\s+.+\s+as\s+([a-zA-Z0-9_]+)')
FROM_IMPORT_PT = re.compile(r'from\s+([a-zA-Z0-9_.]+)\s+import\s+')
MULTI_IMPORT_PT = re.compile(
    r"(?:^|\n)\s*import\s+([ \t]*[A-Za-z_][A-Za-z0-9_]*"
    r"(?:\s*,\s*[A-Za-z_][A-Za-z0-9_]*)*)\s*(?:\n|$|;)",
    re.M
)


NEW_METHOD_BEGIN_MARK = '# --auto genterate mark--'

def getImportInfo(methodInfo:MI.MethodInfo):
    _importLines = []
    fileObject = open(methodInfo.codePath, 'rb')
    if not fileObject:
        return _importLines

    func = methodInfo.symtable.lookup(methodInfo.name).get_namespace()
    funcGlobals = func.get_globals()

    importedMods = ['KBEngine']

    rawText = fileObject.read().decode('utf-8', 'ignore')
    fileObject.close()

    def _splitImportStatements(text):
        i = 0
        n = len(text)
        stmts = []
        while i < n:
            # 跳过空白
            while i < n and text[i] in ' \t\r\n':
                i += 1
            if i >= n:
                break
            start = i
            if text[i] == '#':
                # 注释行到换行
                while i < n and text[i] != '\n':
                    i += 1
                stmts.append(text[start:i])
                continue
            # 找到本语句的结束：换行、分号，且跳过括号/字符串
            paren = 0
            inStr = None
            while i < n:
                c = text[i]
                if inStr:
                    if c == '\\':
                        i += 2; continue
                    if c == inStr:
                        inStr = None
                elif c in ('"', "'"):
                    inStr = c
                elif c == '\\' and i + 1 < n and text[i+1] in ('\n', '\r'):
                    if text[i+1] == '\r' and i + 2 < n and text[i+2] == '\n':
                        i += 3
                    else:
                        i += 2
                    continue
                elif c == '(':
                    paren += 1
                elif c == ')':
                    paren -= 1
                elif paren == 0 and c in (';', '\n'):
                    i += 1
                    break
                i += 1
            stmts.append(text[start:i])
        return stmts

    for strLine in _splitImportStatements(rawText):
        if strLine.strip().startswith('#'):
            continue
        if re.search(r'\bimport\s*\*', strLine):
            continue

        matchMultiImport = MULTI_IMPORT_PT.search(strLine)
        if matchMultiImport:
            modules = matchMultiImport.group(1).split(',')
            for mod in modules:
                mod = mod.strip()
                if mod in funcGlobals:
                    _importLines.append(strLine.replace('\r\n', '\n').lstrip())
                    importedMods.append(mod)

            continue

        # 优先匹配 `from ... import ...`，因为 IMPORT_PT 会把 `import y` 匹配上
        # 导致 `from x import y` 走错分支。
        matchFrom = FROM_IMPORT_PT.search(strLine)
        if matchFrom:
            moduleName = matchFrom.group(1).split('.')[0].strip()
            _importLines.append(strLine.replace('\r\n', '\n'))
            if moduleName not in importedMods:
                importedMods.append(moduleName)

            rest = strLine[matchFrom.end():]
            for sym in re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', rest):
                if sym in ('import',) or sym == moduleName:
                    continue
                if sym in funcGlobals and sym not in importedMods:
                    importedMods.append(sym)

            continue

        matchAs = IMPORT_AS_PT.search(strLine)
        if matchAs:
            moduleName = matchAs.group(1).strip()
            if moduleName in funcGlobals or moduleName in methodInfo.decratorMods:
                _importLines.append(strLine.replace('\r\n', '\n'))
                if moduleName not in importedMods:
                    importedMods.append(moduleName)
            continue

        matchImport = IMPORT_PT.search(strLine)
        if matchImport:
            moduleName = matchImport.group(1).strip()
            if moduleName in funcGlobals or moduleName in methodInfo.decratorMods:
                _importLines.append(strLine.replace('\r\n', '\n'))
                importedMods.append(moduleName)


    #dealing @utils.isMySelf
    for decMod in methodInfo.decratorMods:
        if decMod not in importedMods:
            _importLines.append('import {}\n'.format(decMod))

    _importLines.append('import {}\n'.format(methodInfo.inModuleNameData))

    # 从类型注解和默认值里找需要 import 的模块
    # 注意：Python 的 symtable.get_globals() 不会收集仅出现在类型注解里的名字
    # （比如 def f(x: dropAward.MailWealthVal): pass 里的 dropAward），
    # 所以这部分得自己遍历 AST 来补齐。
    try:
        method_ast = ast.parse(methodInfo.sourceCodeData)
        func_def_node = method_ast.body[0]
        if isinstance(func_def_node, ast.FunctionDef):
            import astor

            # 递归地从类型注解里提取最外层模块名。
            # 对应示例：
            #   dropAward.MailWealthVal  -> ['dropAward']   （ast.Attribute，点号链）
            #   List[dropAward.X]        -> ['dropAward']   （ast.Subscript，泛型）
            #   int | dropAward.X        -> ['dropAward']   （ast.BinOp，PEP 604 的 |）
            #   Union[X, dropAward.Y]    -> ['X','dropAward']（ast.Tuple，老式 Union/Tuple）
            def _extractAnnModules(annNode):
                mods = []
                if isinstance(annNode, ast.Attribute):
                    # 沿点号链向左回溯到最左边的 Name
                    # 例如 dropAward.MailWealthVal -> dropAward
                    #      a.b.c.d.X             -> a
                    node = annNode.value
                    while isinstance(node, ast.Attribute):
                        node = node.value
                    if isinstance(node, ast.Name):
                        mods.append(node.id)
                elif isinstance(annNode, ast.Subscript):
                    # 泛型，例如 List[dropAward.X]：分别递归容器和内部类型
                    mods.extend(_extractAnnModules(annNode.value))
                    mods.extend(_extractAnnModules(annNode.slice))
                elif isinstance(annNode, ast.BinOp):
                    # PEP 604 的联合语法：int | dropAward.X
                    mods.extend(_extractAnnModules(annNode.left))
                    mods.extend(_extractAnnModules(annNode.right))
                elif isinstance(annNode, ast.Tuple):
                    # 老式 typing.Union/Tuple 等
                    for elt in annNode.elts:
                        mods.extend(_extractAnnModules(elt))
                # 裸的 ast.Name（直接写个标识符）这里故意忽略：
                # 没法判断它是内置类型、局部变量还是模块名，乱加 import 风险大。
                return mods

            # 把模块名追加成 `import xxx`，要求是合法标识符且未添加过
            def _addMod(mod):
                if mod and mod not in importedMods and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', mod):
                    _importLines.append('import {}\n'.format(mod))
                    importedMods.append(mod)

            # 1) 处理返回值注解，例如 def f() -> dropAward.X
            if func_def_node.returns:
                for m in _extractAnnModules(func_def_node.returns):
                    _addMod(m)

            # 2) 处理参数注解，覆盖位置专用、位置参数、关键字专用参数
            allArgs = (func_def_node.args.posonlyargs
                       + func_def_node.args.args
                       + func_def_node.args.kwonlyargs)
            for arg in allArgs:
                if arg.annotation:
                    for m in _extractAnnModules(arg.annotation):
                        _addMod(m)

            # 3) 处理默认值，例如 def f(x=dropAward.MailWealthVal())
            #    这部分原先就有，保留以兼容旧逻辑
            for default_arg in func_def_node.args.defaults:
                arg_str = astor.to_source(default_arg).strip()
                match = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)\.', arg_str)
                if match:
                    _addMod(match.group(1))
    except Exception as e:
        print("Warning: Could not parse annotations/defaults for extra imports: {}".format(e))


    return importedMods, _importLines

def setupSysPath(comp):
    if comp == const.CELLAPP:
        sys.path.extend(const.CELL_PATH)
    elif comp == const.BASEAPP:
        sys.path.extend(const.BASE_PATH)
    elif comp == const.INTERFACE:
        sys.path.extend(const.INTERFACE_PATH)
    else:
        print("supported components: {}|{}".format(const.BASEAPP, const.CELLAPP))
        exit(1)

def appendNewMethod(scriptPath, comp, newMethodLines):
    _newScriptLines = []
    with open(scriptPath, 'r', encoding='utf-8') as fScript:
        inTargetBlock = False
        _done = False
        for line in fScript.readlines():
            if _done:
                _newScriptLines.append(line)
                continue
            if re.search(r'\brefreshCell\b', line):
                inTargetBlock = (comp==const.CELLAPP)
            elif re.search(r'\brefreshBase\b', line):
                inTargetBlock = (comp==const.BASEAPP)
            elif re.search(r'\brefreshInterface\b', line):
                inTargetBlock = (comp==const.INTERFACE)

            if inTargetBlock and NEW_METHOD_BEGIN_MARK in line:
                _newScriptLines.extend(['{}{}'.format(INDENT, nl) for nl in newMethodLines])
                _newScriptLines.append('\n')
                _done = True

            _newScriptLines.append(line)

        if not _done:
            print('error:cannot find target block')
            return False

    with open(scriptPath, 'w', encoding='utf-8') as fScript:
        for line in _newScriptLines:
            fScript.writelines([line])

    return True


def generateCode(scriptPath, component, moduleName, clsName, methodName):
    _info = MI.MethodInfo(component, moduleName, clsName, methodName)
    importedMods, resultLines = getImportInfo(_info)
    resultLines.append('\n')

    fSource = open(_info.codePath, 'r', encoding='utf-8')
    src = fSource.read()
    fSource.close()
    srcSym = symtable.symtable(src, _info.codePath, 'exec')

    replaceGlobals = {}

    #find local defined module variable
    func = _info.symtable.lookup(_info.name).get_namespace()
    funcGlobals = func.get_globals()
    for _var in funcGlobals:
        try:
            sb = srcSym.lookup(_var)
        except:
            continue

        if sb.is_imported():
            assert _var in importedMods, "missing import for _var={!r}, importedMods={}".format(_var, importedMods)

        if sb.is_assigned():
            replaceGlobals[sb.get_name()] = '{}.{}'.format(_info.inModuleNameData, sb.get_name())

    #replace module variable
    for old, new in itertools.chain(replaceGlobals.items(), _info.replaceDecorator.items()):
        _info.replaceSymbol(old, new)

    resultLines.extend(_info.sourceLines)

    #assign method finally
    if _info.checkClassValid():
        resultLines.append('{}.{}.{} = {}\n'.format(moduleName, clsName, methodName, methodName))
        #resultLines.append("hotpatch_method({}.{}, '{}', {})\n".format(moduleName, clsName, methodName, methodName))
    else:
        resultLines.append('{}.{} = {}\n'.format(moduleName, methodName, methodName))

    #write to hotReload.py
    if appendNewMethod(scriptPath, component, resultLines):
        print('generate complete!')



if __name__ == "__main__":
    if len(sys.argv)==5:
        comp = sys.argv[1]
        mod = sys.argv[2]
        _cls = sys.argv[3]
        method = sys.argv[4]
    elif len(sys.argv)==4:
        comp = sys.argv[1]
        mod = sys.argv[2]
        _cls = ''
        method = sys.argv[3]
    else:
        print("fix class method usage: genhotfix.py comp, mod, class, method")
        print("fix mod method usage: genhotfix.py comp, mod, method")
        exit(1)

    targetFile = '../scripts/server_common/hotReload.py'

    setupSysPath(comp)
    generateCode(targetFile, comp, mod, _cls, method)





