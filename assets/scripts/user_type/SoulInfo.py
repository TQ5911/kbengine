# -*- coding: utf-8 -*-
"""魂魄实例数据。

词条格式 [affixId, quality, value]。
基础词条、稀有词条、幸运词条分开存。
previewWash / previewClash 为 None 表示没有未保留的洗练结果；
有字典则表示已经洗出、尚未点保留或放弃，稀有词条列表可以为空。
bindFromWash 是普通属性是否可交易，bindFromInherit 是默认等级是否可交易。
bindFromClash 是稀有属性是否可交易。高阶对冲会改它：被消耗魂魄的普通属性和默认等级都可交易，稀有变为可交易；有一项不可交易，稀有变为不可交易。
三条都可交易才可交易。获得时不再单独记绑定：可交易则三条都可交易；
不可交易则洗练和继承不可交易，对冲仍可交易。镶嵌在装备上的魂魄同样记这三条。
"""
import random
import dataUtils
import gameconfig
import LogTrackingMgr
import soul_soulNumQuality
import soul_soulRconst as SSRCD
import AffixInfo


def _qualityScores():
    return SSRCD.datas['soulLevelList']['value']


def calcBaseQualityScore(baseProps):
    """界面评分：基础词条品质分之和。品质从 1 起，对应 soulLevelList。"""
    scores = _qualityScores()
    total = 0
    for prop in baseProps or []:
        if len(prop) < 2:
            continue
        quality = int(prop[1])
        if 1 <= quality <= len(scores):
            total += scores[quality - 1]
    return total


def pickBaseQualityCombo(randomId, curLevel):
    """按导表 randomID2levelQuality 取品质组合。这一档没有组合时返回空列表。"""
    levelMap = soul_soulNumQuality.randomID2levelQuality.get(int(randomId))
    if not levelMap:
        return []
    pair = levelMap.get(int(curLevel or 0))
    if not pair:
        return []
    qualities, weights = pair
    picked = random.choices(qualities, weights=weights, k=1)[0]
    return list(picked)


def calcBindType(payload):
    """洗练、对冲、继承都可交易时，魂魄才可交易。"""
    import gameconst
    if payload and (payload.get('bindFromWash') or payload.get('bindFromClash')
            or payload.get('bindFromInherit')):
        return gameconst.ItemBindType.BIND
    return gameconst.ItemBindType.NORMAL


def rareBoundFromClashMaterial(materialPayload):
    """高阶对冲后，稀有属性的交易状态。

    被消耗魂魄的普通属性、默认等级都可交易时返回 0。有一项不可交易时返回 1。
    """
    materialPayload = normalizePayload(materialPayload)
    if materialPayload.get('bindFromWash') or materialPayload.get('bindFromInherit'):
        return 1
    return 0


def applyGainTradeFlags(payload, tradable):
    """魂魄刚获得时写入三条来源。已有洗练、对冲、继承记录时不覆盖。"""
    if payload.get('bindFromWash') or payload.get('bindFromClash') or payload.get('bindFromInherit'):
        return payload
    if tradable:
        payload['bindFromWash'] = 0
        payload['bindFromClash'] = 0
        payload['bindFromInherit'] = 0
    else:
        payload['bindFromWash'] = 1
        payload['bindFromClash'] = 0
        payload['bindFromInherit'] = 1
    return payload


def setWashPreview(payload, itemId, schoolId, allowLucky=False):
    """按默认等级重随，结果写入 previewWash。不改当前词条。

    allowLucky 为真时，没有幸运词条才可能随出新的。已有幸运词条仍按洗没概率处理。
    """
    import utils
    payload = normalizePayload(payload)
    rolled = utils.rollEquipSoulWash(itemId, schoolId, payload['defLevel'], payload['luckyProp'], allowLucky)
    if not rolled:
        return None
    payload['previewWash'] = {
        'baseProps': rolled['baseProps'],
        'luckyProp': rolled['luckyProp'],
    }
    return payload


def keepWashPreview(payload):
    """点保留：用 previewWash 覆盖基础词条和幸运词条，并清掉预览。没有预览时返回 None。"""
    payload = normalizePayload(payload)
    wash = payload['previewWash']
    if not wash:
        return None
    payload['baseProps'] = list(wash['baseProps'])
    payload['luckyProp'] = list(wash['luckyProp']) if wash['luckyProp'] else []
    payload['previewWash'] = None
    return payload


def previewItemWash(item, schoolId, allowLucky=False):
    payload = setWashPreview(readItem(item), item.itemId, schoolId, allowLucky)
    if not payload:
        return None
    writeItem(item, payload)
    return payload['previewWash']


def keepItemWash(item, materialBound=None):
    current = readItem(item)
    if materialBound is None and current['previewWash']:
        materialBound = current['previewWash'].get('materialBound')
    payload = keepWashPreview(current)
    if not payload:
        return None
    payload['bindFromWash'] = 1 if materialBound else 0
    writeItem(item, payload)
    item.bindType = calcBindType(payload)
    return payload


def previewEquipWash(equipAttr, schoolId, allowLucky=False):
    if not getattr(equipAttr, 'soulItemId', 0):
        return None
    payload = setWashPreview(readEquip(equipAttr), equipAttr.soulItemId, schoolId, allowLucky)
    if not payload:
        return None
    writeEquip(equipAttr, payload)
    return payload['previewWash']


def keepEquipWash(equipAttr, materialBound=None):
    current = readEquip(equipAttr)
    if materialBound is None and current['previewWash']:
        materialBound = current['previewWash'].get('materialBound')
    payload = keepWashPreview(current)
    if not payload:
        return None
    payload['bindFromWash'] = 1 if materialBound else 0
    writeEquip(equipAttr, payload)
    return payload


def discardWashPreview(payload):
    """放弃未保留的洗练预览。没有预览时返回 None。"""
    payload = normalizePayload(payload)
    if not payload['previewWash']:
        return None
    payload['previewWash'] = None
    return payload


def discardItemWash(item):
    payload = discardWashPreview(readItem(item))
    if not payload:
        return None
    writeItem(item, payload)
    return payload


def discardEquipWash(equipAttr):
    payload = discardWashPreview(readEquip(equipAttr))
    if not payload:
        return None
    writeEquip(equipAttr, payload)
    return payload


def setClashPreview(payload, itemId, schoolId, curLevel, materialQuality=0):
    """按被消耗魂魄的当前等级重随稀有词条，结果写入 previewClash。不改当前词条。

    品质上限看被洗练魂魄自己的默认等级和品质。蓝色走 soulRareCeiling，紫色走 soulRareCeiling2，金色走 soulRareCeiling3。
    组合概率库读 rarePropertyNumQuality：材料品质给目标品质对冲时，用对应的库 ID。
    """
    import utils
    payload = normalizePayload(payload)
    rolled = utils.rollEquipSoulClash(itemId, schoolId, curLevel, payload['defLevel'], materialQuality)
    if rolled is None:
        return None
    payload['previewClash'] = {
        'rareProps': rolled['rareProps'],
    }
    return payload


def keepClashPreview(payload):
    """点保留：用 previewClash 覆盖稀有词条，并清掉预览。没有预览时返回 None。"""
    payload = normalizePayload(payload)
    clash = payload['previewClash']
    if not clash:
        return None
    payload['rareProps'] = list(clash['rareProps'])
    payload['previewClash'] = None
    return payload


def keepItemClash(item, materialBound=None):
    current = readItem(item)
    if materialBound is None and current['previewClash']:
        materialBound = current['previewClash'].get('materialBound')
    payload = keepClashPreview(current)
    if not payload:
        return None
    payload['bindFromClash'] = 1 if materialBound else 0
    writeItem(item, payload)
    item.bindType = calcBindType(payload)
    return payload


def keepEquipClash(equipAttr, materialBound=None):
    current = readEquip(equipAttr)
    if materialBound is None and current['previewClash']:
        materialBound = current['previewClash'].get('materialBound')
    payload = keepClashPreview(current)
    if not payload:
        return None
    payload['bindFromClash'] = 1 if materialBound else 0
    writeEquip(equipAttr, payload)
    return payload


def discardClashPreview(payload):
    """放弃未保留的对冲预览。没有预览时返回 None。稀有词条为空也算有预览。"""
    payload = normalizePayload(payload)
    if not payload['previewClash']:
        return None
    payload['previewClash'] = None
    return payload


def discardItemClash(item):
    payload = discardClashPreview(readItem(item))
    if not payload:
        return None
    writeItem(item, payload)
    return payload


def discardEquipClash(equipAttr):
    payload = discardClashPreview(readEquip(equipAttr))
    if not payload:
        return None
    writeEquip(equipAttr, payload)
    return payload


def replaceDefLevel(payload, newDefLevel):
    """用材料魂魄的默认等级替换当前默认等级。词条不变。低于当前默认等级时返回 None。"""
    payload = normalizePayload(payload)
    if newDefLevel < payload['defLevel']:
        return None
    payload['defLevel'] = newDefLevel
    return payload


def replaceItemDefLevel(item, newDefLevel, materialBound):
    payload = replaceDefLevel(readItem(item), newDefLevel)
    if not payload:
        return None
    payload['bindFromInherit'] = 1 if materialBound else 0
    writeItem(item, payload)
    item.bindType = calcBindType(payload)
    return payload


def replaceEquipDefLevel(equipAttr, newDefLevel, materialBound):
    payload = replaceDefLevel(readEquip(equipAttr), newDefLevel)
    if not payload:
        return None
    payload['bindFromInherit'] = 1 if materialBound else 0
    writeEquip(equipAttr, payload)
    return payload


def normalizeProp(prop):
    if not isinstance(prop, (list, tuple)) or len(prop) < 3:
        return None
    try:
        affixId = int(prop[0])
        quality = int(prop[1])
        value = prop[2]
    except (TypeError, ValueError):
        return None
    if affixId <= 0:
        return None
    return [affixId, quality, value]


def normalizePropList(props):
    ret = []
    for prop in props or []:
        one = normalizeProp(prop)
        if one:
            ret.append(one)
    return ret


def normalizeLucky(prop):
    if not prop:
        return []
    one = normalizeProp(prop)
    return one if one else []


def _normalizePreviewWash(raw):
    if raw is None:
        return None
    if not isinstance(raw, dict):
        return None
    return {
        'baseProps': normalizePropList(raw.get('baseProps')),
        'luckyProp': normalizeLucky(raw.get('luckyProp')),
        'materialBound': 1 if raw.get('materialBound') else 0,
    }


def _normalizePreviewClash(raw):
    if raw is None:
        return None
    if not isinstance(raw, dict):
        return None
    return {
        'rareProps': normalizePropList(raw.get('rareProps')),
        'materialBound': 1 if raw.get('materialBound') else 0,
    }


def emptyPayload():
    return {
        'defLevel': 0,
        'baseProps': [],
        'rareProps': [],
        'luckyProp': [],
        'bindFromWash': 0,
        'bindFromClash': 0,
        'bindFromInherit': 0,
        'previewWash': None,
        'previewClash': None,
    }


def payloadFromLegacy(rollProps, defLevel=0):
    payload = emptyPayload()
    payload['defLevel'] = int(defLevel or 0)
    payload['baseProps'] = normalizePropList(rollProps)
    return payload


def normalizePayload(data):
    """兼容词条列表，以及魂魄数据包。"""
    if data is None:
        return emptyPayload()
    if isinstance(data, (list, tuple)):
        return payloadFromLegacy(data)
    if not isinstance(data, dict):
        return emptyPayload()
    payload = emptyPayload()
    payload['defLevel'] = int(data.get('defLevel', 0) or 0)
    payload['baseProps'] = normalizePropList(data.get('baseProps'))
    payload['rareProps'] = normalizePropList(data.get('rareProps'))
    payload['luckyProp'] = normalizeLucky(data.get('luckyProp'))
    payload['bindFromWash'] = data.get('bindFromWash', 0) or 0
    payload['bindFromClash'] = data.get('bindFromClash', 0) or 0
    payload['bindFromInherit'] = data.get('bindFromInherit', 0) or 0
    payload['previewWash'] = _normalizePreviewWash(data.get('previewWash'))
    payload['previewClash'] = _normalizePreviewClash(data.get('previewClash'))
    return payload


def hasAnyProp(payload):
    if not payload:
        return False
    return bool(payload.get('baseProps') or payload.get('rareProps') or payload.get('luckyProp'))


def propToAffix(prop):
    one = normalizeProp(prop)
    if not one:
        return None
    affix = AffixInfo.Affix(one[0])
    affix.affixVal = one[2]
    return affix


def propsToAffixes(props):
    affixes = []
    for prop in props or []:
        affix = propToAffix(prop)
        if affix:
            affixes.append(affix)
    return affixes


def propToClient(prop):
    return {
        'affixId': int(prop[0]),
        'affixVal': float(prop[2]),
        'quality': int(prop[1]),
    }


def propsToClient(props):
    return [propToClient(prop) for prop in props or []]


def clientFields(payload):
    """装备下发用的固定结构，字段和 CLI_EQUIP_ITEM_VAL 对齐。"""
    payload = normalizePayload(payload)
    wash = payload['previewWash']
    clash = payload['previewClash']
    lucky = [payload['luckyProp']] if payload['luckyProp'] else []
    washLucky = []
    washBase = []
    if wash:
        washBase = wash['baseProps']
        if wash['luckyProp']:
            washLucky = [wash['luckyProp']]
    return {
        'soulDefLevel': int(payload['defLevel']),
        'soulBaseAffixes': propsToClient(payload['baseProps']),
        'soulRareAffixes': propsToClient(payload['rareProps']),
        'soulLuckyAffix': propsToClient(lucky),
        'soulBindFromWash': int(payload['bindFromWash'] or 0),
        'soulBindFromClash': int(payload['bindFromClash'] or 0),
        'soulBindFromInherit': int(payload['bindFromInherit'] or 0),
        'soulHasPreviewWash': 1 if wash else 0,
        'soulPreviewWashBase': propsToClient(washBase),
        'soulPreviewWashLucky': propsToClient(washLucky),
        'soulHasPreviewClash': 1 if clash else 0,
        'soulPreviewClashRare': propsToClient(clash['rareProps']) if clash else [],
    }


def readItem(item):
    rollProps = getattr(item, 'rollProps', None)
    if not hasattr(item, 'soulBaseProps'):
        if isinstance(rollProps, dict):
            return normalizePayload(rollProps)
        return payloadFromLegacy(rollProps)
    payload = emptyPayload()
    payload['defLevel'] = int(getattr(item, 'soulDefLevel', 0) or 0)
    payload['baseProps'] = normalizePropList(item.soulBaseProps)
    payload['rareProps'] = normalizePropList(getattr(item, 'soulRareProps', []))
    payload['luckyProp'] = normalizeLucky(getattr(item, 'soulLuckyProp', []))
    payload['bindFromWash'] = getattr(item, 'soulBindFromWash', 0) or 0
    payload['bindFromClash'] = getattr(item, 'soulBindFromClash', 0) or 0
    payload['bindFromInherit'] = getattr(item, 'soulBindFromInherit', 0) or 0
    payload['previewWash'] = _normalizePreviewWash(getattr(item, 'soulPreviewWash', None))
    payload['previewClash'] = _normalizePreviewClash(getattr(item, 'soulPreviewClash', None))
    return payload


def writeItem(item, payload):
    payload = normalizePayload(payload)
    item.soulDefLevel = payload['defLevel']
    item.soulBaseProps = payload['baseProps']
    item.soulRareProps = payload['rareProps']
    item.soulLuckyProp = payload['luckyProp']
    item.soulBindFromWash = payload['bindFromWash']
    item.soulBindFromClash = payload['bindFromClash']
    item.soulBindFromInherit = payload['bindFromInherit']
    item.soulPreviewWash = payload['previewWash']
    item.soulPreviewClash = payload['previewClash']
    item.rollProps = payload
    return payload


def initItem(item, kwargs):
    if kwargs.get('soulPayload') is not None:
        payload = normalizePayload(kwargs['soulPayload'])
    else:
        rollProps = getattr(item, 'rollProps', None)
        if isinstance(rollProps, dict):
            payload = normalizePayload(rollProps)
        else:
            payload = payloadFromLegacy(rollProps, defLevel=kwargs.get('soulDefLevel', 0))
        if kwargs.get('soulRareProps'):
            payload['rareProps'] = normalizePropList(kwargs['soulRareProps'])
        if kwargs.get('soulLuckyProp'):
            payload['luckyProp'] = normalizeLucky(kwargs['soulLuckyProp'])
        if kwargs.get('soulPreviewWash') is not None:
            payload['previewWash'] = _normalizePreviewWash(kwargs['soulPreviewWash'])
        if kwargs.get('soulPreviewClash') is not None:
            payload['previewClash'] = _normalizePreviewClash(kwargs['soulPreviewClash'])
        import gameconst
        applyGainTradeFlags(payload, item.bindType != gameconst.ItemBindType.BIND)
    payload = writeItem(item, payload)
    item.bindType = calcBindType(payload)
    return payload


def ensureItem(item):
    if not item.isSoul():
        return None
    payload = writeItem(item, readItem(item))
    item.bindType = calcBindType(payload)
    return payload


def itemPersistDict(item):
    payload = readItem(item)
    return {
        'soulDefLevel': payload['defLevel'],
        'soulBaseProps': payload['baseProps'],
        'soulRareProps': payload['rareProps'],
        'soulLuckyProp': payload['luckyProp'],
        'soulBindFromWash': payload['bindFromWash'],
        'soulBindFromClash': payload['bindFromClash'],
        'soulBindFromInherit': payload['bindFromInherit'],
        'soulPreviewWash': payload['previewWash'],
        'soulPreviewClash': payload['previewClash'],
    }


def readEquip(equipAttr):
    payload = emptyPayload()
    payload['defLevel'] = int(getattr(equipAttr, 'soulDefLevel', 0) or 0)
    payload['baseProps'] = normalizePropList(getattr(equipAttr, 'soulBaseProps', []))
    payload['rareProps'] = normalizePropList(getattr(equipAttr, 'soulRareProps', []))
    payload['luckyProp'] = normalizeLucky(getattr(equipAttr, 'soulLuckyProp', []))
    payload['bindFromWash'] = getattr(equipAttr, 'soulBindFromWash', 0) or 0
    payload['bindFromClash'] = getattr(equipAttr, 'soulBindFromClash', 0) or 0
    payload['bindFromInherit'] = getattr(equipAttr, 'soulBindFromInherit', 0) or 0
    payload['previewWash'] = _normalizePreviewWash(getattr(equipAttr, 'soulPreviewWash', None))
    payload['previewClash'] = _normalizePreviewClash(getattr(equipAttr, 'soulPreviewClash', None))
    return payload


def writeEquip(equipAttr, payload, legacyAffixes=None):
    """legacyAffixes 是旧档里的 Affix 列表，没有分类字段时当成基础词条，品质记 0。"""
    if payload is None and legacyAffixes is not None:
        baseProps = []
        for affix in legacyAffixes:
            baseProps.append([affix.afxId, 0, affix.affixVal])
        payload = payloadFromLegacy(baseProps)
    payload = normalizePayload(payload)
    equipAttr.soulDefLevel = payload['defLevel']
    equipAttr.soulBaseProps = payload['baseProps']
    equipAttr.soulRareProps = payload['rareProps']
    equipAttr.soulLuckyProp = payload['luckyProp']
    equipAttr.soulBindFromWash = payload['bindFromWash']
    equipAttr.soulBindFromClash = payload['bindFromClash']
    equipAttr.soulBindFromInherit = payload['bindFromInherit']
    equipAttr.soulPreviewWash = payload['previewWash']
    equipAttr.soulPreviewClash = payload['previewClash']
    equipAttr.soulAffixes = propsToAffixes(payload['baseProps'])
    return payload


def _affixLogRows(props, luckyProp=None):
    """日志词条。有幸运词条时接在基础词条后面。"""
    rows = []
    for prop in normalizePropList(props):
        rows.append({'affixId': prop[0], 'affixVal': prop[2]})
    lucky = normalizeLucky(luckyProp)
    if lucky:
        rows.append({'affixId': lucky[0], 'affixVal': lucky[2]})
    return rows


def trackSoul(gbid, distinctId, event, opUUID, soulItem, equipItem, bindType, beforePayload,
              afterBase=None, afterLucky=None, afterRare=None, afterLevel=None, affixOpType=''):
    """魂魄埋点。等级记默认等级。没有对应物品时 ID 填 0。"""
    beforePayload = normalizePayload(beforePayload)
    baseBefore = beforePayload['baseProps']
    luckyBefore = beforePayload['luckyProp']
    rareBefore = beforePayload['rareProps']
    levelBefore = int(beforePayload['defLevel'] or 0)
    baseAfter = baseBefore if afterBase is None else afterBase
    luckyAfter = luckyBefore if afterLucky is None else afterLucky
    rareAfter = rareBefore if afterRare is None else afterRare
    levelAfter = levelBefore if afterLevel is None else int(afterLevel)
    soulItemId = soulItem.itemId if soulItem else 0
    soulUniqueId = soulItem.uniqueId if soulItem else 0
    if equipItem:
        if not soulItemId:
            soulItemId = equipItem.equipAttr.soulItemId or 0
        equipItemId = equipItem.itemId
        equipUniqueId = equipItem.uniqueId
    else:
        equipItemId = 0
        equipUniqueId = 0
    itemData = dataUtils.getCommItemData(int(soulItemId or 0)) or {}
    soulQuality = int(itemData.get('quality', 0) or 0)
    common = (
        gbid, distinctId, opUUID, gameconfig.serverId(), gameconfig.gameId(),
        int(soulItemId or 0), soulUniqueId or 0,
        int(equipItemId or 0), equipUniqueId or 0,
        soulQuality,
        int(bindType if bindType is not None else calcBindType(beforePayload)),
        _affixLogRows(baseBefore, luckyBefore),
        _affixLogRows(baseAfter, luckyAfter),
        _affixLogRows(rareBefore),
        _affixLogRows(rareAfter),
        levelBefore, levelAfter,
    )
    mgr = LogTrackingMgr.LogTrackingMgr
    if event == 'Soul_Level_Change':
        mgr.Soul_Level_Change(*common)
    elif event == 'Soul_Wash_Normal':
        luckyNum = 1 if normalizeLucky(luckyAfter) else 0
        mgr.Soul_Wash_Normal(*common, luckyNum, affixOpType or '')
    elif event == 'Soul_Wash_HighRank':
        mgr.Soul_Wash_HighRank(*common, affixOpType or '')
