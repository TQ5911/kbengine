import sys
import os
import dummy

sys.path.append('../../scripts/server_common')
sys.path.append('../../scripts/data')

fakeMods = ['KBEngine', 'utils', 'KBEDebug', 'ResMgr', 'gameengine', 'gameconst','crontab']
for mod in fakeMods:
    sys.modules[mod] = dummy.dummy

import gameconfig

indent = ' '*4
linesep = '\n'

def _(content, ni=1):
    lines = content.split(linesep)

    ret = ''
    for i, line in enumerate(lines):
        if i==len(lines)-1 and not line:
            break

        ret += indent*ni+line+linesep

    return ret

def convFunc(dic):
    def __(f):
        dic[f.__name__] = f
        return f
    return __

def exportToCS(toFile=None):
    convFuncMap = {}

    @convFunc(convFuncMap)
    def Bool(v):
        if v:
            return 'bool', 'true'
        else:
            return 'bool', 'false'

    @convFunc(convFuncMap)
    def Str(v):
        return 'string', '"%s"'%v

    @convFunc(convFuncMap)
    def Int(v):
        return 'int', str(v)

    @convFunc(convFuncMap)
    def Float(v):
        return 'double', str(v)

    code = 'public class GameConfigBase'+linesep
    code += '{'+linesep
    for originName, vfunc, default, defaultv, desc, cid, flags in sorted(gameconfig.CONFIG.values(), key=lambda v:v[5]):
        csType, csVal = convFuncMap[vfunc.__name__](defaultv)
        if gameconfig.ConfigFlag.CLIENT not in flags:
            continue

        declareLine = 'public static %s %s=%s;%s'%(csType, originName, csVal, linesep)

        code += _(declareLine)

    for originName, vfunc, default, defaultv, desc, cid, flags in sorted(gameconfig.CONFIG.values(), key=lambda v:v[5]):
        csType, csVal = convFuncMap[vfunc.__name__](defaultv)
        if gameconfig.ConfigFlag.CLIENT not in flags:
            continue

        changed = 'public virtual void %sChanged(%s oldVal)%s'%(originName, csType, linesep)
        changed += '{'+linesep
        changed += '}'+linesep
        code += _(changed)

    updateFuncStr = 'public void updateClientConfig(uint cid, string val)'+linesep
    updateFuncStr += '{'+linesep
    updateSwitch = 'switch(cid)'+linesep
    updateSwitch += '{'+linesep
    for originName, vfunc, default, defaultv, desc, cid, flags in sorted(gameconfig.CONFIG.values(), key=lambda v:v[5]):
        csType, csVal = convFuncMap[vfunc.__name__](defaultv)
        if gameconfig.ConfigFlag.CLIENT not in flags:
            continue

        updateCase = 'case %s:'%cid+linesep
        updateCaseBody = '%s oldV%s=%s;%s'%(csType, cid, originName, linesep)
        if csType=='string':
            updateCaseBody += '%s=%s;'%(originName, csVal)
        else:
            updateCaseBody += '%s=%s.Parse(val);%s'%(originName, csType, linesep)

        updateCaseBody += '%sChanged(oldV%s);%s'%(originName, cid, linesep)
        updateCaseBody += 'break;'+linesep

        #print(_(updateCaseBody))
        updateCase += _(updateCaseBody)

        updateSwitch += _(updateCase)

    updateSwitch += _('default:'+linesep)
    updateSwitch += _('break;'+linesep, 2)
    updateSwitch += '}'+linesep

    #print(_(updateSwitch))
    updateFuncStr += _(updateSwitch)
    updateFuncStr += '}'+linesep

    code += _(updateFuncStr)
    code+='}'

    if not toFile:
        print(code)
    else:
        with open(toFile, 'w') as outfile:
            outfile.write(code)

def exportToTS():
    pass

if __name__ == '__main__':
    if sys.argv[1]=='cs':
        toFile = None
        if len(sys.argv)==3:
            toFile = sys.argv[2]

        exportToCS(toFile)