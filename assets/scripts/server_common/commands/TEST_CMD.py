# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from commands.CMD_COMMON import *
import gzip
import json
import utils
import dataUtils
import gameconfig
import gameengine
import dropAward
import awardContext
import buff_buff as BBD
import base64
import importlib
import inspect
import ast
import time
import types
import fightProp_define as FDD

# 判断当前进程类型
IS_BASE = (KBEngine.component == 'baseapp')
import skill_skill as SSD
import visible_visible as UVVD
import actionContext
import gamerefresh

callApps = gmCommand._callApps
forwardCommand = gmCommand.forwardCommand


@gm_cmd('$getAllGMCmds', (), RONE, BASE, '获取所有指令', ALLSIDE, GOD_GROUPS)
def getAllGMCmds(su):
    if KBEngine.publish():
        su.onCommandResult(0, 'can not run in publish server', {})
        return
    data = utils.man_gm_cmds()
    su.onCommandResult(0, 'ok' , {"data": data})

@gm_cmd('$getAllPlayers', (), RONE, BASE, '获取所有在线用户', ALLSIDE, GOD_GROUPS)
def getAllPlayers(su):
    if KBEngine.publish():
        su.onCommandResult(0, 'can not run in publish server', {})
        return
    gameengine.callBaseApps("utils.getAllAvatarByGm", (su, gameglobal.localBaseApp))

@gm_cmd('$getAvatarAoiMonster', (Player("gbId/Id"), Int("range")), RARG(0), CELL, '获取玩家AOI附近怪物', ALLSIDE, GOD_GROUPS, minArgs=1)
def getAvatarAoiMonster(su, player, range=30):
    monsterdata = []
    for ent in player.entitiesInRange(range, 'Monster'):
        monsterdata.append({'entityId': ent.id, 'MonsterName': ent.name})
    for ent in player.entitiesInRange(range, 'Summon'):
        monsterdata.append({'entityId': ent.id, 'MonsterName': ent.name})
    for ent in player.entitiesInRange(range, 'Creation'):
        monsterdata.append({'entityId': ent.id, 'MonsterName': ent.name})
    return su.onCommandResult(0, 'ok' , {"data": monsterdata})

@gm_cmd('$getEntprop', (Player("gbId/Id"),Int('entid'),), RARG(0), CELL, '获取实体属性', ALLSIDE, GOD_GROUPS)
def getEntprop(su,player,entid):

    entprops = {}
    ent = KBEngine.entities.get(entid)
    for propName, propData in FDD.datas.items():
        if not hasattr(ent, propName):
            continue
        entprops[propName] = {
            "value": getattr(ent, propName),
            "name": propData['name']  
        }

    sorted_items = sorted(
    entprops.items(),
    key=lambda kv: 1 if kv[1]["value"] == 0 else 0
)
    entprops = {k: v for k, v in sorted_items}
    
    return su.onCommandResult(0, 'ok', {"data": entprops})

@gm_cmd('$setEntProp', (Player("gbId/Id"),Int('entid'),Str("propName"), Float("value"),), RARG(0), gameconst.CELL, '修改属性', ALLSIDE, GOD_GROUPS)
def setEntProp(su, player,entid,propName,value):
    ent = KBEngine.entities.get(entid)
    if not hasattr(ent, propName):
        return su.onCommandResult(0, f'Faild,{ent.name} 没有 {propName} 属性', {})
    else:
        curVal = ent.getProp(propName)
        if type(curVal) is int:
            newvalue = int(value)
        else:
            newvalue = float(value)
        ent.setProp(f'{propName}', newvalue, gameconst.SourceType.Default)
        return su.onCommandResult(0, f'ok,{ent.name} 的 {propName} 属性从 {curVal} 修改为 {value}',{} )

@gm_cmd('$getEntSkillDic', (Player("gbId/Id"),Int('entid')), RARG(0), gameconst.CELL, '获取实体技能信息', ALLSIDE, GOD_GROUPS)
def getEntSkillDic(su, player, entid):
    
    mod = importlib.import_module('skill_skill')
    ent = KBEngine.entities.get(entid)
    datas = getattr(mod, 'datas', None)
    if not hasattr(ent, 'skillDic'):
        return su.onCommandResult(0, f'Failed, {getattr(ent, "name", entid)} 没有 skillDic 方法', {})
    weight_map = {}
    if hasattr(ent, 'IsMonster') and hasattr(ent, 'skillPropInfo'):
        skill_ids, weights = ent.skillPropInfo
        weight_map = {sid: w for sid, w in zip(skill_ids, weights)}
    entskilldic = {}
    for skill_id, skill_obj in ent.skillDic.items():        
        # 获取技能action
        try:
            action_func = datas.get(skill_id, {}).get('action', None)
            if action_func:
                skillaction = _getTableValue(action_func)
            else:
                skillaction = "None"
        except Exception as e:
            skillaction = f"<获取失败: {str(e)}>"
        
        entskilldic[skill_id] = {
            'skillid': skill_id,
            'name': skill_obj.getSkillName(skill_id),
            'skilllevel': skill_obj.skillLv,
            'weight': weight_map.get(skill_id),
            'action': skillaction
        }
    return su.onCommandResult(0, 'ok', entskilldic)




@gm_cmd('$replaceMonsterSkill', (Player("gbId/Id"),Int('entid'),Str('skillList')), RARG(0), gameconst.CELL, '替换怪物技能', ALLSIDE, GOD_GROUPS)
def replaceMonsterSkill(su, player,entid,skillList):

    ent = KBEngine.entities.get(entid)
    if not hasattr(ent, 'skillDic'):
        return su.onCommandResult(0, f'Failed, {getattr(ent, "name", entid)} 没有 skillDic 方法', {})
    if not hasattr(ent, 'IsMonster'):
        return su.onCommandResult(0, f'Failed, {getattr(ent, "name", entid)} 不是怪物', {})
    newSkillList = ast.literal_eval(skillList)
    ent.changeAllSkill(newSkillList)
    return su.onCommandResult(0, 'ok,替换成功', ent.skillDic)

@gm_cmd('$getEntBuffinfo', (Player("gbId/Id"),Int('entid')), RARG(0), gameconst.CELL, '获取实体buff信息', ALLSIDE, GOD_GROUPS)
def getEntBuffinfo(su, player,entid):
    import utils
    entbuffdic = {}
    ent = KBEngine.entities.get(entid)
    mod = importlib.import_module('buff_buff')
    datas = getattr(mod, 'datas', None)
    if not hasattr(ent, 'buffDic'):
        return su.onCommandResult(0, f'Failed, {getattr(ent, "name", entid)} 没有 buffDic 方法', {})
    for buffid,buffmap in ent.buffDic.items():
        if not buffmap:
            continue  
        buffdict = None
        for buffSrcKey, buffVal in buffmap.items():
            if buffVal:
                buffdict = buffVal
                break
                
        if buffdict is None:
            continue  
            
        entbuffdic[buffid] = {
            'buffid': int(buffid),  # 确保是普通int
            'name': str(datas[buffid].get('name', None)) if datas[buffid].get('name') else None,
            'bufflv': int(buffdict.level),  # 确保是普通int
            'time': float(buffdict.getBuffDuration()),  # 确保是普通float
            'starttime': float(buffdict.tStartTime),  # 确保是普通float
            'servertime':int(utils.getNow())
            # 'effectlist': effectlist_normal
        }

    return su.onCommandResult(0, 'ok,获取实体buff信息成功', entbuffdic)

@gm_cmd('$GMtoolsaddEntBuff', (Int('entityid'), Int('buffId'), Int('lv'), Int('time')), RONE, CELL, 'GM工具给实体加buff', ALLSIDE, GOD_GROUPS,minArgs=3)
def GMtoolsaddEntBuff(su, entityid, buffId, buffLv,time=-1):
    ent = KBEngine.entities.get(entityid)
    if buffId in BBD.datas and ent:
        ent.addBuff(buffId, buffLv, entityid,time)
        return True, '执行成功'
    else:
        return False, '执行失败'
    
@gm_cmd('$delEntBuff', (Player("gbId/Id"),Int('entid'),Int('buffid')), RARG(0), gameconst.CELL, '删除实体buff', ALLSIDE, GOD_GROUPS)
def delEntBuff(su, player,entid,buffid):
    ent = KBEngine.entities.get(entid)
    if not hasattr(ent, 'buffDic'):
        return su.onCommandResult(0, f'Failed, {getattr(ent, "name", entid)} 没有 buffDic 方法', {})
    ent.removeBuff(buffid)
    return su.onCommandResult(0, 'ok,获取实体buff信息成功', {})
    
@gm_cmd('$getEntScoreinfo', (Player("gbId/Id"),Str('entlist')), RALL, gameconst.CELL, '获取实体战力信息', ALLSIDE, GOD_GROUPS)
def getEntScoreinfo(su, player,entlist):
    entscoredic = {}
    entlist_parsed = ast.literal_eval(entlist)
    for entid in entlist_parsed:
        entid_int = int(entid)
        ent = KBEngine.entities.get(entid_int)
        if not ent:
            continue  # 实体不存在，跳过
        if not hasattr(ent, 'scoresInfo'):
            continue  # 实体没有scoresInfo属性，跳过
        try:
            score_data = {
                'totalScore': ent.scoresInfo.totalScore,
                'rewardFightProp': ent.scoresInfo.rewardFightProp,
                'equipments': ent.scoresInfo.equipments,
                'level': ent.scoresInfo.level,
                'mount': ent.scoresInfo.mount,
                'pet': ent.scoresInfo.pet,
                'skill': ent.scoresInfo.skill,
            }
            for key, value in score_data.items():
                if hasattr(value, '__dict__'):
                    score_data[key] = str(value)
            
            entscoredic[str(entid_int)] = score_data
        except Exception as e:
            continue
    return su.onCommandResult(0, 'ok', entscoredic)

@gm_cmd('$getEntBodyEquipmentInfo', (Player("gbId/Id"),Int('entid')), RARG(0), gameconst.CELL, '获取实体装备信息', ALLSIDE, GOD_GROUPS)
def getEntBodyEquipmentInfo(su, player,entid):
    bodyequipinfo = {}
    ent = KBEngine.entities.get(entid)
    if not hasattr(ent, 'bodyEquipData'):
        return su.onCommandResult(0, f'Failed, {getattr(ent, "name", entid)} 没有 bodyEquipData 方法', {})
    for equipType,equipdata in ent.bodyEquipData.equips_map.items():
        bodyrandomAffixesInfo = {}
        bodyblessInfo = {}

        for randomAffixesInfo in equipdata.equipAttr.spiritAffixes:
            affixeid = randomAffixesInfo.toAfxClientDic().get('affixId')
            affixValue = randomAffixesInfo.toAfxClientDic().get('affixVal')
            affixscore = randomAffixesInfo.getAfxScore()
            bodyrandomAffixesInfo[affixeid] = {
                '附灵ID': affixeid,
                '附灵的值': affixValue,
                '附灵的战力': affixscore,
            }
            
        for blessInfo in equipdata.equipAttr.blessAffixes:
            blessId = blessInfo.toAfxClientDic().get('affixId')
            blessValue = blessInfo.toAfxClientDic().get('affixVal')
            blessscore = blessInfo.getAfxScore()
            bodyblessInfo[blessId] = {
                '祝福ID': blessId,
                '祝福的值': blessValue,
                '祝福的战力': blessscore,
            }
        if equipdata.getItemName() in bodyequipinfo:
            bodyequipinfo[equipdata.getItemName()+'2'] = {
            '装备名字': equipdata.getItemName(),
            '装备品阶': equipdata.grade(),
            '装备品质': equipdata.quality,
            '装备战力': equipdata.getEquipScore(),
            '装备ID': equipdata.itemId,
            '装备基础词条':equipdata.getBaseAttrInfo(),
            '装备的随机基础词条':equipdata.equipAttr.baseAttrsByAfxVal,
            '装备的强化等级':equipdata.getEnhanceLevel(),
            '装备的强化属性':equipdata.equipAttr.enhancementAttrs,
            '装备的附灵属性':bodyrandomAffixesInfo,
            '装备的祝福属性':bodyblessInfo
        }
        else:
            bodyequipinfo[equipdata.getItemName()] = {
                '装备名字': equipdata.getItemName(),
                '装备品阶': equipdata.grade(),
                '装备品质': equipdata.quality,
                '装备战力': equipdata.getEquipScore(),
                '装备ID': equipdata.itemId,
                '装备基础词条':equipdata.getBaseAttrInfo(),
                '装备的随机基础词条':equipdata.equipAttr.baseAttrsByAfxVal,
                '装备的强化等级':equipdata.getEnhanceLevel(),
                '装备的强化属性':equipdata.equipAttr.enhancementAttrs,
                '装备的附灵属性':bodyrandomAffixesInfo,
                '装备的祝福属性':bodyblessInfo
            }
    return su.onCommandResult(0, 'ok', bodyequipinfo)

    

@gm_cmd('$unlockAllFunc', (Player("gbId/Id"),), RARG(0), BASE, '解锁所有功能', ALLSIDE, GOD_GROUPS)
def unlockAllFunc(su, player):
    import actionContext
    maxLv = 0
    forwardCommand(su,"$SkipNewbieTask", player.id)
    for _, data in UVVD.datas.items():
        lvLimit = data.get('level', 0)
        taskId = data.get('task', 0)
        if taskId > 0 and dataUtils.getTaskData(taskId):
            rootTaskId = dataUtils.getRootTaskId(taskId)
            player.baseTaskClaim(rootTaskId, actionContext.ClaimTaskCtx(claimSrc=gameconst.ClaimTaskSrc.GM), needCheck=False)
            player.gmForceSubmitTask(taskId)
        if lvLimit > maxLv:
            maxLv = lvLimit
    if maxLv > 0:
        forwardCommand(su,"$setlv", player.id, maxLv)
    return True, '执行成功'


# 统计掉落 路由那边需要随便选一个stub来固定所在base，不然第二次来取cache的话可能会串
@gm_cmd('$statDropByDropId', (Int("dropId"), Int("count"), Int("Level"), Int("school"), Int("sex")), RSTUB('PlayerStub'), BASE, 
    '根据掉落id统计掉落', ALLSIDE, GOD_GROUPS, minArgs=2)
def statDropByDropId(su, playerStub, dropId, count, level=0, school=0, sex=0):
    from test import dropTest
    dropUnit = dropTest.DropUnit(su, count)
    ret, data, process_info = dropUnit.batchGenAward(dropId, level, school, sex)
    if ret:
        su.onCommandResult(0, 'ok', {'data': {f"{dropId}_{count}_{level}_{school}_{sex}": data}})
    else:
        su.onCommandResult(0, 'wait', {'msg': data, 'process_info': process_info})


@gm_cmd('$statDropByDunNo', (Int("dunNo"), Int("count")), RSTUB('PlayerStub'), BASE, 
    '根据副本编号统计掉落', ALLSIDE, GOD_GROUPS)
def statDropByDunNo(su, playerStub, dunNo, count):
    from test import dropTest
    dropUnit = dropTest.DropUnit(su, count)
    ret, content, process_info = dropUnit.getDunDrop(dunNo, count)
    if ret:
        content = gzip.compress(json.dumps(content).encode('utf-8'))
        su.onCommandResult(0, 'ok', {'data': str(content)})
    else:
        su.onCommandResult(0, 'wait', {'msg': content, 'process_info': process_info})

@gm_cmd('$hookModuleFunc', (Str("moduleName"), Str("prefix")), RALL, ALL, 
    'hook模块方法，输出入参和回参', ALLSIDE, GOD_GROUPS, minArgs=1)
def hookModuleFunc(su, moduleName, prefix=''):
    from test import functionHooker
    import sys
    mod = sys.modules.get(moduleName)
    if mod is None:
        return su.onCommandResult(1, f'module {moduleName} not found', {})
    functionHooker.hook_specific_module(moduleName, prefix=prefix, verbose=True)
    return su.onCommandResult(0, f'hook module {moduleName} success', {})

@gm_cmd('$hookClassFunc', (Str("moduleName"), Str("className"), Str("prefix")), RALL, ALL, 
    'hook类方法，输出入参和回参', ALLSIDE, GOD_GROUPS, minArgs=2)
def hookClassFunc(su, moduleName, className, prefix=''):
    from test import functionHooker
    import sys
    mod = sys.modules.get(moduleName)
    if mod is None:
        return su.onCommandResult(1, f'module {moduleName} not found', {})
    functionHooker.hook_specific_class(moduleName, className, prefix=prefix, verbose=True)
    return su.onCommandResult(0, f'hook class {className} in module {moduleName} success', {})

@gm_cmd('$hookFunc', (Str("moduleName"), Str("className"), Str("funcName"), Int("traceDepth"), Str("prefix")), RALL, ALL, 
    'hook指定函数，输出入参和回参', ALLSIDE, GOD_GROUPS, minArgs=3)
def hookFunc(su, moduleName, className, funcName, traceDepth=0, prefix=''):
    from test import functionHooker
    import sys
    mod = sys.modules.get(moduleName)
    if mod is None:
        return su.onCommandResult(1, f'module {moduleName} not found', {})
    functionHooker.hook_specific_class_method(moduleName, className, funcName, prefix=prefix, show_traceback=bool(traceDepth), traceback_depth=traceDepth, verbose=True)
    return su.onCommandResult(0, f'hook class {className} func {funcName} in module {moduleName} success', {})

@gm_cmd('$hookShowLog', (Int("is_open"),), RALL, ALL, 
    'hook打印开关', ALLSIDE, GOD_GROUPS)
def hookShowLog(su, is_open):
    from test import functionHooker
    functionHooker.hook_print_open(bool(is_open))
    return su.onCommandResult(0, f'hook print open: {is_open}', {})

@gm_cmd('$refreshData', (Str('moduleName'),), RALL, ALL, '刷新表格数据', ALLSIDE, GOD_GROUPS, minArgs=0)
def refreshData(su, moduleName=None):
    """刷新表格数据，在所有进程中执行"""
    
    # 确定当前进程类型
    process_type = 'BaseApp' if IS_BASE else 'CellApp'
    try:
        import gamerefresh
        if moduleName and moduleName.strip():
            gamerefresh.refreshData(moduleName)
            return su.onCommandResult(0, f'{process_type}进程刷新 {moduleName} 数据成功', {})
        else:
            gamerefresh.refreshData()
            return su.onCommandResult(0, f'{process_type}进程刷新所有数据成功', {})
    except Exception as e:
        return su.onCommandResult(1, f'{process_type}进程刷新数据失败: {str(e)}', {})



@gm_cmd('$setdata', (Str('moduleName'), Str('key'), Str('attrName'), Str('value'), Int('isBase64')), RALL, ALL, '修改内存数据(支持普通值和函数)', ALLSIDE, GOD_GROUPS, minArgs=4)
def setMemoryData(su, moduleName, key, attrName, value, isBase64=0):
    """修改内存数据，支持普通字段和函数表达式，在所有进程中执行"""
    # 确定当前进程类型
    process_type = 'BaseApp' if IS_BASE else 'CellApp'
    # 直接在当前进程中执行修改
    return _setMemoryDataInProcess(su, moduleName, key, attrName, value, isBase64, process_type)

def _translateValue(value, valueType, module_dict=None):
    """根据valueType转换value"""
    try:
        DEBUG_MSG(f'_translateValue:: {value} {type(value)} to {valueType}')
        import ast
        if valueType == 'int':
            if type(value) is bool:
                value = 1 if value else 0
            else:
                value = int(value)
        elif valueType == 'float':
            value = float(value)
        elif valueType == 'str':
            value = str(value)
        elif valueType == 'bool':
            value = value.lower() in ('true', '1', 'yes')
        elif valueType == 'list':
            value = ast.literal_eval(value) if isinstance(value, str) else list(value)
        elif valueType == 'dict':
            value = ast.literal_eval(value) if isinstance(value, str) else dict(value)
        elif valueType == 'tuple':
            value = ast.literal_eval(value) if isinstance(value, str) else tuple(value)
        elif valueType == 'function':
            if value == '':
                return True, "转换成功", None
            # 解析函数名
            rootNode = ast.parse(value)
            funcName = None
            for node in ast.walk(rootNode):
                if isinstance(node, ast.FunctionDef):
                    funcName = node.name
                    break
            if not funcName:
                return False, '函数定义不正确，无法找到函数名', None
            # 在原模块的全局命名空间中编译函数，保留所有导入的模块
            exec(value, module_dict)
            if funcName not in module_dict:
                return False, f'函数 {funcName} 编译失败', None
            # 获取编译好的函数对象
            new_func = module_dict[funcName]
            # 添加源码属性，用于getEntSkillDic获取源码
            new_func.__source_code__ = value
            value = new_func
        else:
            # 默认尝试eval
            value = eval(value)
        return True, "转换成功", value
    except Exception as e:
        return False, f"转换失败: {str(e)}", value

def _setMemoryDataInProcess(su, moduleName, key, attrName, value, isBase64, processType):
    """在指定进程中修改内存数据的公共逻辑"""
    try:
        # 导入模块
        import sys
        mod = sys.modules.get(moduleName)
        if mod is None:
            return su.onCommandResult(1, f'{processType}进程: 模块 {moduleName} 未加载', {})
        # 获取模块的datas属性
        datas = getattr(mod, 'datas', None)
        if datas is None:
            return su.onCommandResult(1, f'{processType}进程: 模块 {moduleName} 没有 datas 属性', {})
        # 处理key类型
        ori_keys = datas.keys()
        ori_key_type = type(next(iter(ori_keys))) if ori_keys else str
        _, _, key_cast = _translateValue(key, ori_key_type.__name__)
        if key_cast not in datas:
            return su.onCommandResult(1, f'{processType}进程: key {key} 不在 {moduleName}.datas 中', {})
        # 获取目标数据对象
        target_data = datas[key_cast]
        # 根据目标属性的当前值类型进行转换
        target_value = target_data.get(attrName, None)
        
        if target_value is not None:
            valueType = type(target_value).__name__
        else:
            for v in datas.values():
                tmp_value = v.get(attrName, None)
                if tmp_value is not None:
                    valueType = type(tmp_value).__name__
                    break
        # 判断value类型并处理
        if isBase64 :
            # 直接内存替换方案 - 不编译，直接创建函数对象
            try:
                value = base64.b64decode(value).decode('utf-8')
            except Exception as e:
                return su.onCommandResult(1, f'{processType}进程: base64解码失败: {str(e)}', {})
        try:
            ret, msg, parsed_value = _translateValue(value, valueType, mod.__dict__)
            if not ret:
                return su.onCommandResult(1, f'{processType}进程: {msg}', {})
            # 设置到数据中
            if hasattr(target_data, '_data'):
                target_data._data[attrName] = parsed_value
            else:
                target_data[attrName] = parsed_value
        except Exception as e:
            return su.onCommandResult(1, f'{processType}进程: 值设置失败: {str(e)}', {})
        import gamerefresh
        gamerefresh.refreshData(' ') # 主要为了调用clearCacheInTick
        return su.onCommandResult(0, f'{processType}进程修改 {moduleName}.datas[{key_cast}].{attrName} 成功 {target_data[attrName]}', {attrName: value})
    except Exception as e:
        return su.onCommandResult(1, f'{processType}进程修改失败: {str(e)}', {})

def _getTableValue(value):
    """递归获取表格值，处理函数和自定义类"""
    value_type = type(value).__name__
    if callable(value):
        # 尝试获取源码
        try:
            if hasattr(value, '__source_code__'):
                # 动态函数，有源码属性
                func_source = value.__source_code__
            else:
                # 普通函数，用inspect获取源码
                import inspect
                func_source = inspect.getsource(value).strip()
        except:
            # 无法获取源码，显示函数名和类型
            func_source = f"<func: {getattr(value, '__name__', 'unknown')} - {type(value).__name__}>"
        return func_source
    elif value_type == 'RODict':
        # 处理自定义类，提取_data属性
        return {k: _getTableValue(v) for k, v in value._data.items()}
    elif value_type == 'ROList':
        # 处理自定义类，提取_data属性
        return [_getTableValue(v) for v in value._data]
    elif value_type == 'ROSet':
        # 处理自定义类，提取_data属性
        return set([_getTableValue(v) for v in value._data])
    return value

@gm_cmd('$getdata', (Str('moduleName'), Str('key'), Str('attrName')), RONE, CELL, '获取内存数据', ALLSIDE, GOD_GROUPS, minArgs=2)
def getMemoryData(su, moduleName, key, attrName=None):
    # 导入模块
    import sys
    mod = sys.modules.get(moduleName)
    if mod is None:
        return su.onCommandResult(1, f' 模块 {moduleName} 未加载', {})
    # 获取模块的datas属性
    datas = getattr(mod, 'datas', None)
    if datas is None:
        return su.onCommandResult(1, f' 模块 {moduleName} 没有 datas 属性', {})
    # 处理key类型
    ori_keys = datas.keys()
    ori_key_type = type(next(iter(ori_keys))) if ori_keys else str
    _, _, key_cast = _translateValue(key, ori_key_type.__name__)
    if key_cast not in datas:
        return su.onCommandResult(1, f'key {key} 不在 {moduleName}.datas 中', {})
    # 获取目标数据对象
    target_data = datas[key_cast]
    if attrName:
        if attrName not in target_data:
            return su.onCommandResult(1, f'属性 {attrName} 不在 {moduleName}.datas[{key}]. 中', {})
        value = _getTableValue(target_data[attrName])
        return su.onCommandResult(0, 'ok', {attrName: value})
    else:
        # rodict类型，提取_data, 否则无法json序列化
        if hasattr(target_data, '_data'):
            new_data = {k: _getTableValue(v) for k, v in target_data._data.items()}
        else:
            new_data = {k: _getTableValue(v) for k, v in target_data.items()}
        DEBUG_MSG("GM: getMemoryData ~ ", new_data)
        return su.onCommandResult(0, 'ok', new_data)

@gm_cmd('$reqWorkshopSetAutoMF', (Player("gbId/Id"), Int('autoMF')), RARG(0), gameconst.BASE, '测试开启自动合成制作', ALLSIDE, GOD_GROUPS)
def reqWorkshopSetAutoMF(su, player, autoMF):
    INFO_MSG("GM: reqWorkshopSetAutoMF ~ ", autoMF)
    return player.reqWorkshopSetAutoMF(autoMF)

@gm_cmd('$reqWorkshopMF', (Player("gbId/Id"), Int('itemID'), Int('batchCount')), RARG(0), gameconst.BASE, '测试合成制作', ALLSIDE, GOD_GROUPS)
def reqWorkshopMF(su, player, itemID, batchCount):
    INFO_MSG("GM: reqWorkshopMF ~ ", itemID, batchCount)
    return player.reqWorkshopMF(itemID, batchCount)

@gm_cmd('$getServerAllEntities', (), RALL, ALL, '获取服务器所有实体', ALLSIDE, GOD_GROUPS)
def getServerAllEntities(su):
    """获取服务器所有实体，按进程类型分类返回"""
    
    # 获取当前进程信息
    componentNo = KBEngine.getComponentGroupOrder()
    process_type = 'BaseApp' if IS_BASE else 'CellApp'
    process_name = f'{process_type.lower()}{componentNo:02d}'
    
    # 收集当前进程中的所有实体
    entity_classes = {}
    total_entity_count = 0
    
    # 定义需要限制显示ID数量的实体类型
    limited_types = {''}
    
    for entity in KBEngine.entities.values():
        class_name = entity.className
        
        if class_name not in entity_classes:
            entity_classes[class_name] = {
                'count': 0,
                'entity_ids': [],
                'is_limited': class_name in limited_types
            }
        
        entity_classes[class_name]['count'] += 1
        
        # 对于数量较多的实体类型，只保存少量ID作为示例
        if class_name in limited_types:
            if len(entity_classes[class_name]['entity_ids']) < 3:
                entity_classes[class_name]['entity_ids'].append(entity.id)
        else:
            # 其他类型保存所有ID
            entity_classes[class_name]['entity_ids'].append(entity.id)
            
        total_entity_count += 1
    
    # 构造返回数据
    result_data = {
        'process_info': {
            'process_name': process_name,
            'process_type': process_type,
            'component_order': componentNo
        },
        'entity_summary': {
            'total_entity_count': total_entity_count,
            'unique_entity_types': len(entity_classes)
        },
        'entity_details': entity_classes,
        'limited_types': list(limited_types)
    }
    
    return su.onCommandResult(0, f'{process_name}进程实体统计完成', result_data)


@gm_cmd('$getStubAllProp', (Str("processType"), Int('entityId'), Str('attrPath')), RALL, ALL, '获取指定进程实体属性', ALLSIDE, GOD_GROUPS, minArgs=2)
def getStubAllProp(su, processType, entityId, attrPath=""):
    """获取指定实体的所有属性，按类型分类显示"""
    try:
        # 解析目标进程
        if processType.startswith('base'):
            target_type, target_component = 'baseapp', int(processType[4:]) if len(processType) > 4 else 1
        elif processType.startswith('cell'):
            target_type, target_component = 'cellapp', int(processType[4:]) if len(processType) > 4 else 1
        else:
            return su.onCommandResult(1, f'无效的进程类型: {processType}', {})

        # 检查是否为目标进程
        current_type = KBEngine.component
        current_component = KBEngine.getComponentGroupOrder()
        if current_type != target_type or current_component != target_component:
            return su.onCommandResult(0, '', {})  # 非目标进程返回空数据

        # 获取实体
        entity = KBEngine.entities.get(entityId)
        if not entity:
            return su.onCommandResult(1, f'实体{entityId}不存在', {
                "process_info": {"type": current_type, "component": current_component, "process_name": processType, "matched": True},
                "target_info": {"path": f"entity.{entityId}", "object_type": "Unknown"},
                "attributes": {"公共": {"error": "实体不存在"}, "私有": {}, "函数/方法": {}, "特殊属性": {}}
            })

        # 获取目标对象
        if attrPath:
            try:
                target_obj = eval(f"entity.{attrPath}", {"__builtins__": {}}, {'entity': entity})
                current_path = f"entity.{attrPath}"
            except Exception as e:
                return su.onCommandResult(1, f'路径访问失败: {attrPath}, 错误: {str(e)}', {})
        else:
            target_obj = entity
            current_path = "entity"

        # 获取分类属性并返回结果
        classified_attrs = _get_entity_attributes_classified(target_obj, processType)
        return su.onCommandResult(0, f'获取实体{entityId}属性完成', {
            "process_info": {"type": current_type, "component": current_component, "process_name": processType, "matched": True},
            "target_info": {"path": current_path, "object_type": type(target_obj).__name__},
            "attributes": classified_attrs
        })
        
    except Exception as e:
        import traceback
        return su.onCommandResult(1, f"获取实体属性时出错: {str(e)}\n{traceback.format_exc()}", {})


def _get_entity_attributes_classified(target_obj, process_name):
    """获取对象的分类属性"""
    classified = {"公共": {}, "私有": {}, "函数/方法": {}, "特殊属性": {}}
    
    try:
        # 处理容器类型：字典、RODict、列表
        if isinstance(target_obj, dict) or type(target_obj).__name__ == 'RODict':
            # 字典类型展开键值对
            items_iter = None
            try:
                items_iter = target_obj.items()
            except:
                try:
                    items_iter = [(k, target_obj[k]) for k in target_obj]
                except:
                    pass
            
            if items_iter:
                for key, value in items_iter:
                    try:
                        classified["公共"][str(key)] = _get_simple_value(value)
                    except:
                        classified["公共"][str(key)] = "<error>"
            return classified
        
        elif isinstance(target_obj, (list, tuple)):
            # 列表类型展开索引值对
            for i, value in enumerate(target_obj):
                try:
                    classified["公共"][str(i)] = _get_simple_value(value)
                except:
                    classified["公共"][str(i)] = "<error>"
            return classified
        
        elif isinstance(target_obj, (set, frozenset)):
            try:
                values_list = list(target_obj)
                for i, value in enumerate(values_list):
                    try:
                        classified["公共"][str(i)] = _get_simple_value(value)
                    except:
                        classified["公共"][str(i)] = "<error>"
            except:
                classified["公共"]["error"] = "无法遍历set内容"
            return classified
        # 普通对象：按属性名分类
        skip_attrs = {'canDestroy', 'destroy', 'destroyEntity', 'writeToDB', 'createCellEntity', 'destroyCellEntity', 'teleport', 'addTimer', 'delTimer', 'giveClientTo'}
        
        for attr_name in dir(target_obj):
            if attr_name in skip_attrs:
                continue
                
            try:
                attr_value = getattr(target_obj, attr_name)
                simple_value = _get_simple_value(attr_value)
                
                # 按名称分类
                if attr_name.startswith('__') and attr_name.endswith('__'):
                    classified["特殊属性"][attr_name] = simple_value
                elif attr_name.startswith('_'):
                    classified["私有"][attr_name] = simple_value
                elif callable(attr_value):
                    classified["函数/方法"][attr_name] = simple_value
                else:
                    classified["公共"][attr_name] = simple_value
            except:
                classified["公共"][attr_name] = "<无法访问>"
                
    except:
        classified["公共"]["error"] = "获取属性时出错"
    
    return classified


def _get_simple_value(value):
    """获取属性值的简化字符串表示"""
    try:
        if value is None:
            return 'None'
        elif isinstance(value, bool):
            return str(value)
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            return f'"{value[:50]}..."' if len(value) > 50 else f'"{value}"'
        elif isinstance(value, (list, tuple)):
            # 列表和元组也可以展开查看内容
            return f"{type(value).__name__}[{len(value)}] [可展开]"
        elif isinstance(value, dict):
            # 字典也可以展开查看内容
            return f"dict[{len(value)}] [可展开]"
        elif isinstance(value, set):
            # set集合类型也可以展开查看内容
            return f"set[{len(value)}] [可展开]"
        elif callable(value):
            return f"<{type(value).__name__}>"
        else:
            # 检查常见的游戏类型
            class_name = type(value).__name__
            
            # Vector3 类型特殊处理
            if class_name == 'Vector3':
                try:
                    if hasattr(value, 'x') and hasattr(value, 'y') and hasattr(value, 'z'):
                        return f"Vector3({value.x}, {value.y}, {value.z}) [可展开]"
                except:
                    pass
            
            # MAILBOX 类型特殊处理
            elif class_name == 'MAILBOX':
                try:
                    if hasattr(value, 'id'):
                        return f"MAILBOX(id={value.id}) [可展开]"
                except:
                    pass
            
            # RODict 类型特殊处理
            elif class_name == 'RODict':
                try:
                    return f"RODict[{len(value)}] [可展开]"
                except:
                    pass
            
            # 检查是否是可展开的复杂对象
            if (hasattr(value, '__dict__') and 
                not isinstance(value, (str, int, float, bool, list, tuple, dict)) and
                hasattr(value, '__class__')):
                # 这是一个自定义类实例，可以展开
                return f"<{class_name}> [可展开]"
            else:
                return f"<{class_name}>"
    except Exception:
        return "<unknown>"


@gm_cmd('$broadcastSystemMsg', (Str('message'),), RONE, BASE, '向系统频道广播消息', ALLSIDE, GOD_GROUPS)
def broadcastSystemMsg(su, message):
    #给机器人广播使用
    try:
        strmessage = base64.b64decode(message).decode('utf-8')
        system_avatar_info = {
            'gbId': 0, 
            'name': '系统',
            'level': 0,
            'vipLevel': 0,
            'school': 0,
            'sex': 0
        }
        
        # 只在一个BaseApp进程中执行，然后向所有BaseApp广播
        gameengine.broadcastBaseapp('broadcastToAllAvatar',
                                    (gameconst.BASE, 'onRecvChannelMsg',
                                     (gameconst.ChatChannel.SYSTEM, system_avatar_info, strmessage), ()))
        
        return su.onCommandResult(0, f'系统消息广播成功: {strmessage}', {})
        
    except Exception as e:
        return su.onCommandResult(1, f'系统消息广播失败: {str(e)}', {})

# --------------------------dev test only cmd segment----------------------------------------------------------------------------------------------------------------------------------------- 
@gm_cmd('$modifyEquipEnhanceLevel', (Player("gbId/Id"), Int("slotID"), Int("enhanceLevel")), RARG(0), gameconst.CELL, '修改装备强化等级', ALLSIDE, GOD_GROUPS)
def modifyEquipEnhanceLevel(su, player, slotID, enhanceLevel):
    ret = player.gmModifyEquipEnhanceLevel(slotID, enhanceLevel)
    if not ret:
        return False, '执行失败'
    return True, '执行成功'

@gm_cmd('$dressAllEquipments', (Player("gbId/Id"), ), RARG(0), gameconst.CELL, '穿戴所有装备', ALLSIDE, GOD_GROUPS)
def dressAllEquipments(su, player):
    ret = player.gmDressEquips()
    if not ret:
        return False, '执行失败'
    return True, '执行成功'

@gm_cmd('$glyphWashingEquipments', (Player("gbId/Id"), Int("equipPos"), Int("itemId"), Int("affixId")), RARG(0), gameconst.CELL, '给指定的装备洗铭文', ALLSIDE, GOD_GROUPS)
def glyphWashingEquipments(su, player, equipPos, itemId, affixId):
    ret = player.gmGlyphWashingEquips(equipPos, itemId, affixId)
    if not ret:
        return False, '执行失败'
    return True, '执行成功'

# --------------------------dev test only cmd segment-----------------------------------------------------------------------------------------------------------------------------------------
