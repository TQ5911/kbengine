using RuntimeInspectorNamespace;
using System;
using System.Collections.Generic;
using UnityEngine;

namespace KBEngine
{

    public class ModelEntity : KBEngine.EntityCommon
    {
        public ViewEntity m_ViewEntity;
        public bool m_ActiveInClient = true;
        public ModelEntity()
        {

        }

        #region 服务器调用客户端方法

        #region 技能相关

        //public override void onAddSkill(uint skillId, uint level, byte extraLevel, double tNextCast, float skillCd)
        //{
        //    CLIENT_SKILL_VAL skill = new CLIENT_SKILL_VAL();
        //    skill.skillId = skillId;
        //    skill.tNextCast = tNextCast;
        //    skill.skillCd = skillCd;
        //    //skill.extraSkillLv = extraLevel;

        //    if (DataUserInfoManager.Instance.allSkills == null)
        //    {
        //        DataUserInfoManager.Instance.allSkills = new Dictionary<uint, CLIENT_SKILL_VAL>();
        //    }

        //    if (DataUserInfoManager.Instance.allSkills.ContainsKey(skillId))
        //    {
        //        DataUserInfoManager.Instance.allSkills[skillId] = skill;
        //    }
        //    else
        //    {
        //        DataUserInfoManager.Instance.allSkills.Add(skillId, skill);
        //    }

        //    EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_UPDATE_SKILLS, this.id);
        //}

        //public override void onAddPassiveSkill(uint skillId, uint level)
        //{
        //    CLIENT_PASSIVESKILL_VAL skill = new CLIENT_PASSIVESKILL_VAL();
        //    skill.skillId = skillId;
        //    skill.level = level;

        //    if (DataUserInfoManager.Instance.allPassiveSkills == null)
        //    {
        //        DataUserInfoManager.Instance.allPassiveSkills = new Dictionary<uint, CLIENT_PASSIVESKILL_VAL>();
        //    }

        //    if (DataUserInfoManager.Instance.allPassiveSkills.ContainsKey(skillId))
        //    {
        //        DataUserInfoManager.Instance.allPassiveSkills[skillId] = skill;
        //    }
        //    else
        //    {
        //        DataUserInfoManager.Instance.allPassiveSkills.Add(skillId, skill);
        //    }
        //}

        /// <summary>
        /// AOI内所有的entity释放招式回调
        /// </summary>
        /// <param name="objID">释放者id</param>
        /// <param name="skillID"></param>
        public override void onUseSkill(Byte success, UInt32 skillID, Int32 targetID, List<float> skillParam, List<Int32> targetIDList, List<float> extraParams)
        {
            Int32 objID = this.id;
            bool isSuccess = success > 0 ? true : false;
            int index = 0;
            if (hasView)
                view.OnUseSkill(skillID, targetID, skillParam, extraParams, targetIDList, index, isSuccess, 0);
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_USE_SKILL, objID, skillID, targetID, skillParam, targetIDList, index, isSuccess, 0);
        }

        /// <summary>
        /// 引导技能回调
        /// </summary>
        /// <param name="objID"></param>
        /// <param name="skillID"></param>
        /// <param name="targetID"></param>
        /// <param name="skillParam"></param>
        /// <param name="targetIDList"></param>
        /// <param name="index">当前是引导技能的第几次回调</param>
        public override void onUseChanneling(Int32 objID, UInt32 skillID, Int32 targetID, List<float> skillParam, List<Int32> targetIDList, Int32 index, List<float> extraParams)
        {
            bool isSuccess = true;
            if (hasView)
                view.OnUseSkill(skillID, targetID, skillParam, extraParams, targetIDList, index, isSuccess, 0);
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_USE_SKILL, objID, skillID, targetID, skillParam, targetIDList, index, isSuccess, 0);
            //EventMgr.Instance.SendEvent(EventDef.EVENT_TARGET_ONCASTSKILL, this.id, skillID, KBEngineTime.GetServerRealTimeMS() / 1000d);
        }

        /// <summary>
        /// 吟唱回调
        /// </summary>
        /// <param name="objID"></param>
        /// <param name="skillID"></param>
        /// <param name="targetID"></param>
        /// <param name="skillParam"></param>
        /// <param name="targetIDList"></param>
        public override void onUseCasting(Int32 objID, UInt32 skillID, Int32 targetID, List<float> skillParam, List<Int32> targetIDList, List<float> extraParams)
        {
            if (hasView)
                view.OnStartCasting(skillID, targetID, skillParam, extraParams, targetIDList);
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_USE_CASTING, objID, skillID, targetID, skillParam, targetIDList);
            //EventMgr.Instance.SendEvent(EventDef.EVENT_TARGET_ONCASTSKILL, objID, skillID, KBEngineTime.GetServerRealTimeMS() / 1000d);
        }

        /// <summary>
        /// AOI范围外释放吟唱技能后，释放过程中进入视野
        /// </summary>
        /// <param name="skillId"></param>
        /// <param name="timeStamp"></param>
        public override void notifyCastingSkill(uint skillId, double timeStamp)
        {
            //EventMgr.Instance.SendEvent(EventDef.EVENT_TARGET_ONCASTSKILL, this.id, skillId, timeStamp);
        }

        ///// <summary>
        ///// 蓄力技能蓄力过程中被打断
        ///// </summary>
        ////Avatar Monster Summon Creation Pet AvatarMirror
        //public override void onBreakChargeSkill(Int32 objId, UInt32 skillID)
        //{
        //    EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_BREAK_CHARGE_SKILL, id, skillID);
        //}

        public override void onBreakChannelingSkill(Int32 objId, UInt32 skillID, int reason)
        {
            if (hasView)
                view.OnServerBreakChannelingSkill(skillID);
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_BREAK_CHANNEL_SKILL, id, skillID);
            //EventMgr.Instance.SendEvent(EventDef.EVENT_TARGET_ONCASTSKILL, this.id, skillID, KBEngineTime.GetServerRealTimeMS() / 1000d, false);

            if (objId != KBEngineApp.app.player().id) return;
            switch (reason)
            {
                case 1:
                    UITipsManager.ShowMessage(54000132);
                    break;
                case 2:
                    UITipsManager.ShowMessage(54000134);
                    break;
                case 3:
                    var msgId = Table_const_const.m_MpNotEnough_msgID;
                    UITipsManager.ShowMessage(msgId);
                    break;
            }
        }

        public override void onBreakCastingSkill(int objId, uint skillID, int reason)
        {
            if (hasView)
                view.OnServerBreakCastingSkill(skillID);
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_BREAK_CASTING_SKILL, id, skillID);
            //EventMgr.Instance.SendEvent(EventDef.EVENT_TARGET_ONCASTSKILL, this.id, skillID, KBEngineTime.GetServerRealTimeMS() / 1000d, false);

            if (objId != KBEngineApp.app.player().id) return;
            switch (reason)
            {
                case 1:
                    UITipsManager.ShowMessage(54000133);
                    break;
                case 2:
                    UITipsManager.ShowMessage(54000134);
                    break;
                case 3:
                    var msgId = Table_const_const.m_MpNotEnough_msgID;
                    UITipsManager.ShowMessage(msgId);
                    break;
            }
        }

        ///// <summary>
        ///// 这个专门给玩家的蓄力技用的，服务器检测到超时后自动释放
        ///// </summary>
        ///// <param name="skillId"></param>
        //public override void onServerUseSkill(UInt32 skillId)
        //{
        //    if (!this.isPlayer())
        //    {
        //        return;
        //    }

        //    EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SERVER_USE_SKILL, id, skillId);
        //}
        /// <summary>
        /// 释放的招式的效果
        /// </summary>
        /// <param name="info"></param>
        public override void onSkillDamage(SKILL_DAMAGE_INFO info)
        {
            BattleManager.Instance.OnHandleSkillDamages(info);
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SKILL_DAMAGE, id, info);
        }

        public override void onOthersSkillDamage(Int32 sourceId, List<Int32> targetIdList)
        {
            BattleManager.Instance.OnHandleSkillDamagesSimple(id, sourceId, targetIdList);
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SKILL_SIMPLE_DAMAGE, id, sourceId, targetIdList);
        }

        ///// <summary>
        ///// 闪现结束回调
        ///// </summary>
        ///// <param name="skillid"></param>
        //public override void onSkillTeleport(UInt32 skillid, Vector3 pos)
        //{
        //    BattleManager.Instance.OnHandleSkillTeleport(this, skillid, pos);
        //    //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SKILL_TELEPORT, id, skillid, pos);
        //}

        ///// <summary>
        ///// 对抗状态（用于飄字）
        ///// </summary>
        ///// <param name="casterId"></param>
        ///// <param name="targetId"></param>
        ///// <param name="state"></param>
        ///// <param name="value"></param>
        //public override void onAddStateRet(Int32 casterId, Int32 targetId, Int32 state, Int32 damageType)
        //{
        //    BattleManager.Instance.OnHandleSkillAddState(casterId, targetId, state, damageType);
        //    //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SKILL_ADD_STATE, casterId, targetId, state, damageType);
        //}

        //public override void onSetAddSkillCd(uint skillID, float cd, double nextCastTime, Byte isReset)
        //{
        //    if (DataUserInfoManager.Instance.skillBuilds == null)
        //    {
        //        return;
        //    }

        //    //foreach (CLIENT_SKILLS item in skillBuilds.Values)
        //    //{
        //    //    for (int i = 0; i < item.skills.Count; i++)
        //    //    {
        //    //        if (item.skills[i].skillId == skillID)
        //    //        {
        //    //            item.skills[i].skillCd = cd;
        //    //            item.skills[i].tNextCast = nextCastTime;
        //    //        }
        //    //    }
        //    //}

        //    if (DataUserInfoManager.Instance.allSkills.ContainsKey(skillID))
        //    {
        //        DataUserInfoManager.Instance.allSkills[skillID].skillCd = cd;
        //        DataUserInfoManager.Instance.allSkills[skillID].tNextCast = nextCastTime;
        //    }

        //    //GLog.LogError("Set SkillCD: {0}  {1} {2}", skillID, cd, nextCastTime);
        //    EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SKILL_UPDATE_CD, id, skillID, isReset == 1 ? true : false);
        //}

        public override void drawCube(Vector3 position, Vector3 forward, float width, float height)
        {
#if GM
            GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
            GameObject.Destroy(cube.GetComponent<BoxCollider>());
            cube.transform.position = position;
            cube.transform.forward = forward;
            cube.transform.localScale = new Vector3(width, 1, height);
            DestroyObjectByTime d = cube.AddComponent<DestroyObjectByTime>();
            d.DestroyByTime(5);
#endif
        }
        #endregion 技能相关

        ////Monster Summon Pet AvatarMirror
        //public override void aiChatToPlayer(UInt32 arg1, UInt32 arg2)
        //{

        //}

        ////Avatar Monster Summon Creation Pet AvatarMirror
        //public override void onBornAction()
        //{

        //}

        //Avatar Monster Summon Pet AvatarMirror
        public override void onDead(Int32 arg1)
        {
            BattleManager.Instance.OnHandleDead(this);
            EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_DEAD, this);
        }

        ///// <summary>
        ///// 神符掉落
        ///// </summary>
        ///// <param name="pos"></param>
        ///// <param name="ids"></param>
        //public override void onDropRuneIds(List<float> pos, Int32 groupId, List<Int32> ids)
        //{
        //    EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_DROP_RUNE_IDS, pos, groupId, ids);
        //}

        ///// <summary>
        ///// 移除神符
        ///// </summary>
        ///// <param name="groupId"></param>
        //public override void onRemoveRune(UInt32 spaceNO, Int32 groupId)
        //{
        //    EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_REMOVE_RUNE_IDS, spaceNO, groupId);
        //}

        ///// <summary>
        ///// 刷新神符
        ///// </summary>
        //public override void onUpdateRunes(RUNE_INFO runeInfo)
        //{
        //    EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_UPDATE_RUNE_IDS, runeInfo);
        //}

        //Account Avatar Monster Summon Creation Pet AvatarMirror
        public override void onMessage(Int32 id, List<string> param)
        {
            if (id / 1000000 == 58)
            {
                GLog.Log($"onMessage  chatMessage表的消息{id}，暂时不显示!  {MyUtils.ListToString(param)}");
                return;
            }

            UITipsManager.ShowMessage((uint)id, null, null, param.ToArray());

            //if (param .Count == 0)
            //{
            //    UITipsManager.ShowMessage((uint)id);
            //}
            //else if (param .Count == 1)
            //{
            //    UITipsManager.ShowMessage((uint)id, null, null, param[0]);
            //}
            //else if (param.Count == 2)
            //{
            //    UITipsManager.ShowMessage((uint)id, null, null, param[0], param[1]);
            //}
            //else if (param.Count == 3)
            //{
            //    UITipsManager.ShowMessage((uint)id, null, null, param[0], param[1], param[2]);
            //}
            //else if (param.Count == 4)
            //{
            //    UITipsManager.ShowMessage((uint)id, null, null, param[0], param[1], param[2], param[3]);
            //}
        }

        //Avatar Monster Summon Creation Pet AvatarMirror

        //Avatar Monster Summon Creation Pet AvatarMirror

        #region 光环相关

        public List<CLIENT_AUREOLE_VAL> clientAureoles;

        public override void onAddAureole(CLIENT_AUREOLE_VAL aureole)
        {
            if (clientAureoles == null)
            {
                clientAureoles = new List<CLIENT_AUREOLE_VAL>();
            }

            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_ADD_AUREOLE, id, aureole.aureoleId, aureole.level);
        }

        public override void onRemoveAureole(Int32 aureoleId)
        {
            if (clientAureoles == null)
            {
                return;
            }

            for (int i = 0; i < clientAureoles.Count; i++)
            {
                if (clientAureoles[i].aureoleId == aureoleId)
                {
                    clientAureoles.RemoveAt(i);
                    break;
                }
            }

            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_REMOVE_AUREOLE, id, aureoleId);
        }

        public override void onUpdateAureoles(CLIENT_AUREOLES aureoles)
        {
            clientAureoles = aureoles.aureoles;
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_UPDATE_AUREOLE, id, clientAureoles);
        }

        /// <summary>
        /// 获取target身上的所有光环信息
        /// </summary>
        /// <param name="targetID"></param>
        public void getAureoleInfo(int targetID)
        {
            cellCall("getAureoleInfo", targetID);
        }

        public override void onGetAureoleInfo(int targetID, CLIENT_AUREOLES aureoles)
        {
            Entity target = KBEngineApp.app.findEntity(targetID);
            if (target != null)
            {
                clientAureoles = aureoles.aureoles;
                //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_UPDATE_AUREOLE, targetID, clientAureoles);
            }
        }

        public override void onAddAureoleFromOthers(CLIENT_AUREOLE_VAL aureole)
        {
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_ADD_AUREOLE_FROM_OTHERS, id, aureoleId, level);
        }

        public override void onRemoveAureoleFromOthers(Int32 aureoleId)
        {
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_REMOVE_AUREOLE_FROM_OTHERS, id, aureoleId);
        }

        public override void onUpdateAureolesFromOthers(AUREOLE_FROM_OTHERS aureoles)
        {
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_UPDATE_AUREOLE_FROM_OTHERS, id, aureoles);
        }

        #endregion

        #region buff相关

        public CLIENT_BUFFS buffs = null;

        /// <summary>
        /// 这个只有在登录或者断线重连的时候才会发送！
        /// 只有Player会调用
        /// </summary>
        /// <param name="arg1"></param>
        public override void onUpdateBuffs(CLIENT_BUFFS allBuffs)
        {
            buffs = allBuffs;
            BuffManager.Instance.InitBuffs(this);
            EventMgr.Instance.SendEvent(EventDef.EVENT_UI_UPDATE_BUFF, this);
            if (isPlayer())
                EventMgr.Instance.SendEvent(EventDef.EVENT_UI_UPDATE_BUFF_PLAYER);
        }

        public override void onUpdateBuff(CLIENT_BUFF_VAL arg1)
        {
            if (buffs == null)
            {
                buffs = new CLIENT_BUFFS();
            }

            bool exist = false;
            for (int i = 0; i < buffs.buffs.Count; i++)
            {
                if (buffs.buffs[i].buffId == arg1.buffId &&
                    buffs.buffs[i].srcKey == arg1.srcKey)
                {
                    exist = true;
                    double oldEndTime = buffs.buffs[i].endTimeStamp;
                    buffs.buffs[i] = arg1;
                    if (arg1.endTimeStamp == 0 || arg1.endTimeStamp >= oldEndTime)
                    {
                        BuffManager.Instance.RefreshBuff(this, arg1);
                    }
                    break;
                }
            }
            if (!exist)
            {
                buffs.buffs.Add(arg1);
                BuffManager.Instance.RefreshBuff(this, arg1);
            }

            EventMgr.Instance.SendEvent(EventDef.EVENT_UI_UPDATE_BUFF, this);
            if (isPlayer())
                EventMgr.Instance.SendEvent(EventDef.EVENT_UI_UPDATE_BUFF_PLAYER);
        }
        /// <summary>
        /// 所有战斗单位都会调用
        /// </summary>
        /// <param name="buffID"></param>
        /// <param name="level"></param>
        /// <param name="releaserID"></param>
        /// <param name="targetID"></param>
        public override void onAddBuff(CLIENT_BUFF_VAL arg1)
        {
            if (buffs == null)
            {
                buffs = new CLIENT_BUFFS();
            }

            bool exist = false;
            for (int i = 0; i < buffs.buffs.Count; i++)
            {
                if (buffs.buffs[i].buffId == arg1.buffId &&
                    buffs.buffs[i].srcKey == arg1.srcKey)
                {
                    exist = true;
                    buffs.buffs[i] = arg1;
                }
            }

            if (!exist)
            {
                buffs.buffs.Add(arg1);
            }

            BuffManager.Instance.AddBuff(this, arg1);

            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_ADD_BUFF, this.id, arg1);

            EventMgr.Instance.SendEvent(EventDef.EVENT_UI_UPDATE_BUFF, this);
            if (isPlayer())
                EventMgr.Instance.SendEvent(EventDef.EVENT_UI_UPDATE_BUFF_PLAYER);
        }

        /// <summary>
        /// 移除buff
        /// </summary>
        /// <param name="buffID"></param>
        /// <param name="removedSrcKeys">个数为0代表移除所有该id的buff</param>
        public override void onRemoveBuff(int buffID, List<ulong> removedSrcKeys)
        {
            //int targetID = this.id;
            if (buffs == null)
            {
                return;
            }

            for (int i = 0; i < buffs.buffs.Count; i++)
            {
                if (buffs.buffs[i].buffId == buffID)
                {
                    if (removedSrcKeys.Count == 0 ||
                        removedSrcKeys.Contains(buffs.buffs[i].srcKey))
                    {
                        CLIENT_BUFF_VAL buff = buffs.buffs[i];
                        buffs.buffs.RemoveAt(i);
                        BuffManager.Instance.RemoveBuff(this, buff);
                    }
                }
            }

            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_REMOVE_BUFF, this.id, buffID, removedSrcKeys);

            EventMgr.Instance.SendEvent(EventDef.EVENT_UI_UPDATE_BUFF, this);
            if (isPlayer())
                EventMgr.Instance.SendEvent(EventDef.EVENT_UI_UPDATE_BUFF_PLAYER);
        }

        /// <summary>
        /// 获得某一个对象身上所有的buff信息
        /// 可以用于查看boss身上的buff
        /// 除了Player外的其他战斗单位会调用
        /// </summary>
        /// <param name="targetID"></param>
        /// <param name="buffs"></param>
        public override void onGetBuffInfo(int targetID, CLIENT_BUFFS buffs)
        {
            Entity target = KBEngineApp.app.findEntity(targetID);
            if (target != null)
            {
                ModelEntity t = target as ModelEntity;
                t.buffs = buffs;
                BuffManager.Instance.InitBuffs(t);

                EventMgr.Instance.SendEvent(EventDef.EVENT_UI_UPDATE_BUFF, t);
            }

            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_UPDATE_BUFFS, targetID);
        }

        private void CheckBuffInfo()
        {
            ViewEntityManager.Instance.CheckBuffInfo(this);
        }
        #endregion

        #endregion 服务器调用客户端方法

        #region 属性变化

        public override void onAdjCDChanged(float oldValue)
        {
            //if (hasView)
            //    view.m_adjcd = adjCD;
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SET_AdjCD, this.id, adjCD);
        }

        //public override void onBuffDicChanged(SERVER_BUFFS oldValue)
        //{
        //    object v = getDefinedProperty("buffDic");
        //    EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_UPDATE_BUFF, id, v);

        //}

        //public override void onChaosAntiChanged(Int32 oldValue) { }
        //public override void onChaosEnhChanged(Int32 oldValue) { }
        //public override void onChargeSpeedChanged(float oldValue)
        //{
        //    object v = getDefinedProperty("chargeSpeed");
        //    EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SET_CHARGE_SPEED, id, v);
        //}
        //public override void onDieWithHostChanged(Byte oldValue) { }
        //public override void onDodgeChanged(Int32 oldValue) { }
        //public override void onFatalChanged(Int32 oldValue) { }
        //public override void onFireAntiChanged(Int32 oldValue) { }
        //public override void onFireEnhChanged(Int32 oldValue) { }
        public override void onForceChanged(Int32 oldValue)
        {
            if (force != oldValue)
            {
                BattleManager.Instance.OnHandleForceChange(this);
                //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SET_FORCE, id, force);
            }
        }

        public override void onSiegeWarCampChanged(int oldValue)
        {
            BattleManager.Instance.OnHandleForceChange(this);
        }

        //public override void onFrozenAntiChanged(Int32 oldValue) { }
        //public override void onFrozenEnhChanged(Int32 oldValue) { }

        public override void onFullHpChanged(Int32 oldValue)
        {
            if (fullHp != oldValue)
            {
                if (isPlayer())
                {
                    PropCalculator.Instance.SetServerValue(PropDataConsant.FullHp, oldValue);
                }
                if (hasView)
                    view.HpMax = fullHp;
                EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SET_FULL_HP, this);
            }
        }

        public override void onFullMpChanged(Int32 oldValue)
        {
            if (fullMp != oldValue)
            {
                if (isPlayer())
                {
                    PropCalculator.Instance.SetServerValue(PropDataConsant.FullMp, oldValue);
                }
                if (hasView)
                    view.MpMax = fullMp;
                EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SET_FULL_MP, this);
            }
        }
        //public override void onGameEntityIdChanged(Int64 oldValue) { }
        //public override void onGbIdChanged(UInt64 oldValue) { }

        //public void onHaveMpChanged(Byte oldValue)
        //{
        //    object v = getDefinedProperty("haveMp");
        //    if ((Byte)v != oldValue)
        //    {
        //        EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SET_HAVE_MP, this.id, v.ToString() == "1");
        //    }
        //}
        //public override void onHitChanged(Int32 oldValue) { }
        //public override void onHostIdChanged(Int32 oldValue) { }

        public override void onHpChanged(Int32 oldValue)
        {
            if (hp != oldValue)
            {
                if (hasView)
                    view.Hp = hp;
                EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SET_HP, this);
            }
        }

        public override void onLevelChanged(UInt32 oldValue)
        {
            if (level != oldValue)
            {
                if (hasView)
                    view.Level = level;
                EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SET_LEVEL, this);
            }
        }

        public override void onIsWitnessCompleteChanged(Byte oldValue)
        {

            if (isWitnessComplete != oldValue)
            {
                if (hasView)
                {
                    view.EntityWitnessType = (ViewEntity.WitnessType)isWitnessComplete;
                }
                //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SET_WITNESSCOMPLETE, this.id, isWitnessComplete, oldValue);
            }

            CheckBuffInfo();
        }

        //public override void onMortalChanged(float oldValue) { }


        //public override void onMulBloodSuckChanged(float oldValue) { }
        public override void onMulCDChanged(float oldValue)
        {
            if (hasView)
                view.Mulcd = mulCD;
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SET_MulCD, this.id, mulCD);
        }

        public override void onNameChanged(string oldValue)
        {
            if (hasView)
                view.Name = name;
            if (isPlayer())
                EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SET_NAME);
        }

        public override void onSpeedChanged(float oldValue)
        {
            if (speed != oldValue)
            {
                if (hasView)
                    view.CurrentSpeed = speed;
                //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SET_SPEED, id, speed);
            }
        }

        public override void onStateChanged(Int64 oldValue)
        {
            //object v = getDefinedProperty("state");
            //当我是主角，且没有被其他玩家控制的时候，说明我是由自己控制的，也就是由玩家手机操作控制，所以这里就屏蔽服务器下发的位置
            //if (isPlayer() == true && isControlled == false) return;
            if (hasView)
                view.FullState = view.GetCurrentState();
            EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SET_STATE, this);
            if (isPlayer())
            {
                EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SET_STATE_PLAYER);
            }
        }

        public override void onState2Changed(Int64 oldValue)
        {
            if (hasView)
                view.FullState = view.GetCurrentState();
            EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SET_STATE, this);
            if (isPlayer())
            {
                EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SET_STATE_PLAYER);
            }
        }

        public override void onStateChangedForce(byte state)
        {
            //已有此状态后，又被设置一次才会触发此接口
            //目前只有击倒
            if (hasView)
            {
                view.RefreshStateAnim(state);
            }
        }

        //public override void onStunAntiChanged(Int32 oldValue) { }
        //public override void onStunEnhChanged(Int32 oldValue) { }
        //public override void onSummonIdChanged(Int32 oldValue) { }
        //public override void onThunderAntiChanged(Int32 oldValue) { }
        //public override void onThunderEnhChanged(Int32 oldValue) { }
        //public override void onWaterAntiChanged(Int32 oldValue) { }
        //public override void onWaterEnhChanged(Int32 oldValue) { }

        /// <summary>
        /// 目标的目标发生变化
        /// </summary>
        /// <param name="oldValue"></param>
        public override void onSelectedTargetIdChanged(int oldValue)
        {
            GLog.Log($"onSelectedTargetIdChanged {this.id}: {this.selectedTargetId}");
            if (hasView)
                view.OnSelectedTargetIdChanged();
            EventMgr.Instance.SendEvent(EventDef.EVENT_TARGET_ONTARGETCHANGED, this.id);

            var vc = ViewEntityManager.Instance.GetCollectionByEntityId(selectedTargetId);
            if (vc)
            {
                vc.NavToCollect();
            }
            //EventMgr.Instance.SendEvent(EventDef.EVENT_GATHER_ONSELECT_COLLECTION, this.selectedTargetId);
        }

        /// <summary>
        /// 怪物仇恨目标改变
        /// </summary>
        /// <param name="oldValue"></param>
        public override void onFirstHateTargetIdChanged(int oldValue)
        {
            EventMgr.Instance.SendEvent(EventDef.EVENT_TARGET_ONHATETARGETCHANGED, this.id);
        }

        public override void onAntiFatalChanged(int oldValue)
        {
            if (isPlayer())
            {
                PropCalculator.Instance.SetServerValue(PropDataConsant.AntiFatal, oldValue);
            }
        }

        public override void onIgnoreArmorChanged(float oldValue)
        {
            if (isPlayer())
            {
                PropCalculator.Instance.SetServerValue(PropDataConsant.IgnoreArmor, oldValue);
            }
        }

        public override void onDmgArmorChanged(float oldValue)
        {
            if (isPlayer())
            {
                PropCalculator.Instance.SetServerValue(PropDataConsant.DmgArmor, oldValue);
            }
        }



        #endregion 属性变化

        //#region 客户端调用服务器
        //public void setState(int state)
        //{
        //    cellCall("clientSetState", state);
        //}

        ///// <summary>
        ///// GM指令
        ///// </summary>
        //public void RunGmCommand(string cmd)
        //{
        //    if (!isPlayer()) return;
        //    if (string.IsNullOrEmpty(cmd)) return;
        //    baseCall("runGmCommand", cmd);
        //}

        ///// <summary>
        ///// 复活
        ///// </summary>
        ///// <param name="type">1 原地复活 2就近复活 3出生点复活</param>
        //public void Relive(int type)
        //{
        //    if (type != ReliveType.LocalRelive && type != ReliveType.NearbyRelive && type != ReliveType.OriginRelive)
        //        return;
        //    cellCall("relive", type);
        //}

        ///// <summary>
        ///// 玩家区域改变
        ///// </summary>
        ///// <param id="id"> 区域id</param>
        //public void ReachNewArea(int id)
        //{
        //    cellCall("reachNewArea", id);
        //}

        ///// <summary>
        ///// 选择神符
        ///// </summary>
        ///// <param name="arg"></param>
        //public void GetRune(int arg1, int arg2)
        //{
        //    cellCall("getRune", arg1, arg2);
        //}

        ///// <summary>
        ///// 取消释放蓄力技能，目前用于蓄力时间小于最小蓄力时间的时候调用
        ///// </summary>
        ///// <param name="skillID"></param>
        //public void CancelChargeSkill(UInt32 skillID)
        //{
        //    cellCall("cancelChargeSkill", skillID);
        //}

        ///// <summary>
        ///// 移除一个状态，目前只允许移除使用技能状态
        ///// </summary>
        ///// <param name="stateID"></param>
        //public void ClientRemoveState(int stateID)
        //{
        //    cellCall("clientRemoveState", stateID);
        //}

        ///// <summary>
        ///// 加载场景完成
        ///// </summary>
        ///// <param name="isLogin">0:非登录加载， 1：登录加载</param>
        //public void LoadSceneFinish(int isLogin = 0)
        //{
        //    cellCall("loadSceneFinish", isLogin);
        //}

        ///// <summary>
        ///// 获取target身上的所有buff信息
        ///// </summary>
        ///// <param name="targetID"></param>
        //public void getBuffInfo(int targetID)
        //{
        //    cellCall("getBuffInfo", targetID);
        //}

        //#endregion

        #region 消息弹窗相关

        public override void popDialog(int arg1)
        {
            GLog.Log($"popDialog {id} {arg1}");
            UITipsManager.ShowPopDialog((uint)arg1);
        }
        public override void showPopoverMsg(UInt32 id)
        {
            GLog.Log($"showPopoverMsg {id}");
            //EventMgr.Instance.SendEvent(EventDef.EVENT_UI_MSG_SHOW_CHAT, this.id, (int)id);
        }

        #endregion

        public override void OnModelViewLoad(ViewEntity ve)
        {
            m_ViewEntity = ve;
            if (!m_ActiveInClient)
                m_ViewEntity.gameObject.SetActive(false);
        }

        public virtual void SetClientActive(bool active)
        {
            if (active != m_ActiveInClient)
            {
                m_ActiveInClient = active;
                if (m_ViewEntity != null)
                    m_ViewEntity.gameObject.SetActive(active);
            }
        }

        public override void onEnterWorld()
        {

            base.onEnterWorld();
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_ENTER_WORLD, this);
            BattleManager.Instance.OnHandleEnterWorld(this);
            if (isPlayer())
            {


                EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_ENTER_WORLD_PLAYER, this);
            }

            if (!KBEngineApp.app.getInitArgs().isOnInitCallPropertysSetMethods)
            {
                onDirectionChanged(Vector3.zero);
                // onEnterSpace();
            }
            //GLog.LogError("~~~~~  onEnterWorld this=" + this.id);
            CheckBuffInfo();
        }

        public override void onEnterSpace()
        {
            base.onEnterSpace();
            //这里需要判断是否是玩家本身
            if (isPlayer())
            {
                // uint spaceNo = (uint)getDefinedProperty("spaceNo");
                //0没有意义，先屏蔽
                if (spaceNo > 0)
                {
                    EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_ENTER_SCENE_PLAYER, spaceNo, oldSpaceNo);
                }
            }
        }

        public override void onSpaceNoChanged(UInt32 oldValue)
        {
            onEnterSpace();
        }

        public override void onPositionChanged(Vector3 oldValue)
        {
            if (isPlayer())
                KBEngineApp.app.entityServerPos(position);
            if (hasView)
                view.OnPositionChanged(position, false);
            if (isPlayer())
                EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_POSITION_CHANGED);
        }

        public override void onDirectionChanged(Vector3 oldValue)
        {
            direction.x = direction.x * 360 / ((float)System.Math.PI * 2);
            direction.y = direction.y * 360 / ((float)System.Math.PI * 2);
            direction.z = direction.z * 360 / ((float)System.Math.PI * 2);
            if (hasView)
                view.OnDirectionChanged(direction);
            if (isPlayer())
                EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_DIRECTION_CHANGED);
        }

        public override void onLeaveWorld()
        {
            base.onLeaveWorld();
            BattleManager.Instance.OnHandleLeavaWorld(this);
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_LEAVE_WORLD, this);
        }

        public override void onLeaveSpace()
        {
            base.onLeaveSpace();
            if (isPlayer())
            {
                DataUserInfoManager.Instance.OnPlayerLeaveSpace();
                //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_LEAVE_SPACE_PLAYER, this);
            }
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_LEAVE_SPACE, this);
        }

        public override void onControlled(bool _isControlled)
        {
            isControlled = _isControlled;
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_CONTROLLED, id, isControlled);
        }


        public override void onMulSpeedChanged(float oldValue)
        {
            if (isPlayer())
            {
                PropCalculator.Instance.SetServerValue(PropDataConsant.MulSpeed, oldValue);
            }
        }

        #region patch
        public override void onPatchVersion(string patchVersion)
        {
            if (string.IsNullOrEmpty(patchVersion))
            {
                GLog.LogError("Error:patch content is null or empty");
                return;
            }

            GLog.Log("min patch version:{0}", patchVersion);
            if (MyUtils.Compare4StopsVersion(MainStart.GetPatchVersion(), patchVersion) < 0)
            {
                UITipsManager.ShowMessage(Table_login_set.m_PatchUpdate_restart, AppRestart.Instance.Restart);
            }
        }
        #endregion
    }
}