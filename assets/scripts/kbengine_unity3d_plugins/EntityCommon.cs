namespace KBEngine
{
	using UnityEngine;
	using System;
	using System.Collections;
	using System.Collections.Generic;

	public class EntityCommon : EntityCommonProperty
	{
		public virtual void aiChatToPlayer(UInt32 arg1, UInt32 arg2) {} //Monster Summon Npc AvatarReplica 
		public virtual void checkTextSecurityResp(CHECK_TEXT_SECURITY_RESP arg1) {} //Account Avatar Accounting Avataring 
		public virtual void drawCube(Vector3 arg1, Vector3 arg2, float arg3, float arg4) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void minorAccountConstraintTip(UInt64 arg1) {} //Account Accounting 
		public virtual void notifyCastingSkill(UInt32 arg1, double arg2) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onAddAureole(CLIENT_AUREOLE_VAL arg1) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onAddAureoleFromOthers(CLIENT_AUREOLE_VAL arg1) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onAddBuff(CLIENT_BUFF_VAL arg1) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onAddPassiveSkill(UInt32 arg1, UInt32 arg2) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onAddSkill(UInt32 arg1, UInt32 arg2, Byte arg3, double arg4, float arg5, Byte arg6) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onAnotherClientLogin() {} //Avatar Avataring 
		public virtual void onBornAction() {} //Monster Npc AvatarReplica 
		public virtual void onBreakAwayStuckSuccess() {} //Avatar Avataring 
		public virtual void onBreakCastingSkill(Int32 arg1, UInt32 arg2, Int32 arg3) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onBreakChannelingSkill(Int32 arg1, UInt32 arg2, Int32 arg3) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onClientDataSyncFinished() {} //Avatar Avataring 
		public virtual void onDead(Int32 arg1) {} //Avatar Monster Summon Npc AvatarReplica 
		public virtual void onExitShiftByConflict(Vector3 arg1) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onGameConfigChanged(List<string> arg1, List<Byte> arg2) {} //Account Avatar 
		public virtual void onGetAureoleInfo(Int32 arg1, CLIENT_AUREOLES arg2) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onGetBuffInfo(Int32 arg1, CLIENT_BUFFS arg2) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onHotfixVersion(string arg1) {} //Account Avatar 
		public virtual void onKickAnotherAccount() {} //Account Accounting 
		public virtual void onMessage(Int32 arg1, List<string> arg2) {} //Account Avatar Monster Summon Npc Creation AvatarReplica Accounting Avataring 
		public virtual void onOthersSkillDamage(Int32 arg1, List<Int32> arg2) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onPatchVersion(string arg1) {} //Account Avatar 
		public virtual void onRecvAvatarChannelMsg(UInt32 arg1, CHAT_CHANNEL_AVATAR_INFO arg2, CHAT_MSG_DATA arg3) {} //Avatar Avataring 
		public virtual void onRemoveAureole(Int32 arg1) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onRemoveAureoleFromOthers(Int32 arg1) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onRemoveBuff(Int32 arg1, List<UInt64> arg2) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onRemoveCompleteWitness(List<Int32> arg1) {} //Avatar Avataring 
		public virtual void onSetAddSkillCd(UInt32 arg1, float arg2, double arg3, Byte arg4, double arg5, SByte arg6, SByte arg7, Byte arg8) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onShooterSkillCanUse(UInt32 arg1, double arg2, Byte arg3) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onSkillDamage(SKILL_DAMAGE_INFO arg1) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onStartPlayEmote(UInt16 arg1) {} //Avatar Avataring 
		public virtual void onStateChangedForce(Byte arg1) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onStopPlayEmote() {} //Avatar Avataring 
		public virtual void onUpdateAureoles(CLIENT_AUREOLES arg1) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onUpdateAureolesFromOthers(AUREOLE_FROM_OTHERS arg1) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onUpdateBuff(CLIENT_BUFF_VAL arg1) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onUpdateBuffs(CLIENT_BUFFS arg1) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onUseCasting(Int32 arg1, UInt32 arg2, Int32 arg3, List<float> arg4, List<Int32> arg5, List<float> arg6) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onUseChanneling(Int32 arg1, UInt32 arg2, Int32 arg3, List<float> arg4, List<Int32> arg5, Int32 arg6, List<float> arg7) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onUseSkill(Byte arg1, UInt32 arg2, Int32 arg3, List<float> arg4, List<Int32> arg5, List<float> arg6) {} //Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void popDialog(Int32 arg1) {} //Avatar Monster Summon Npc Collection Accounting Avataring 
		public virtual void showPopoverMsg(UInt32 arg1) {} //Avatar Monster Summon Npc Collection Accounting Avataring 
		public virtual void showPopoverMsgWithArg(UInt32 arg1, List<string> arg2) {} //Avatar Monster Summon Npc Collection Accounting Avataring 
		public virtual void syncServerTime(Int64 arg1, float arg2) {} //Avatar Avataring 
		public virtual void updateForbidSkillTags(List<UInt16> arg1) {} //Avatar Monster Summon Npc Creation AvatarReplica 


		public virtual void onAdjCDChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onAntiFatalChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onAppearanceChanged(APPEARANCE_INFO oldValue) {}	//Avatar AvatarReplica Avataring 
		public virtual void onBePushedSpeedChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onBornStateChanged(Byte oldValue) {}	//Monster Summon Npc Collection AvatarReplica 
		public virtual void onCopperChanged(float oldValue) {}	//Avatar AvatarReplica 
		public virtual void onDmgArmorChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onExpGrowChanged(float oldValue) {}	//Avatar AvatarReplica 
		public virtual void onFirstHateTargetIdChanged(Int32 oldValue) {}	//Monster Summon Npc AvatarReplica 
		public virtual void onForceChanged(Int32 oldValue) {}	//Space WaitMapSpace CubeSpaceMgr WonderLandSpaceMgr AbyssSpaceMgr WorldLineSpaceMgr SiegeWarSpaceMgr DungeonSpaceMgr MonsterGrp Avatar Monster Summon Barrier Teleporter CityBattleTeleporter CoreAreaFlag Npc Collection Creation DuelFlag AvatarReplica RebornPos 
		public virtual void onFullHpChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onFullMpChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onGameEntityIdChanged(Int64 oldValue) {}	//MonsterGrp Monster Summon Barrier Teleporter CityBattleTeleporter CoreAreaFlag Npc Collection Creation AvatarReplica RebornPos 
		public virtual void onGatherRateChanged(float oldValue) {}	//Avatar AvatarReplica 
		public virtual void onGbIdChanged(UInt64 oldValue) {}	//Avatar Avataring 
		public virtual void onHealHpRatioChanged(Byte oldValue) {}	//Avatar AvatarReplica 
		public virtual void onHealMpRatioChanged(Byte oldValue) {}	//Avatar AvatarReplica 
		public virtual void onHostIdChanged(Int32 oldValue) {}	//Summon Creation 
		public virtual void onHpChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onIgnoreArmorChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onIsBossChanged(Byte oldValue) {}	//Monster Summon Npc AvatarReplica 
		public virtual void onIsWitnessCompleteChanged(Byte oldValue) {}	//Avatar Monster Summon Npc Creation AvatarReplica Avataring 
		public virtual void onLevelChanged(UInt32 oldValue) {}	//Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onMedicineRateChanged(float oldValue) {}	//Avatar AvatarReplica 
		public virtual void onMiningRateChanged(float oldValue) {}	//Avatar AvatarReplica 
		public virtual void onMpChanged(Int32 oldValue) {}	//Avatar AvatarReplica 
		public virtual void onMulCDChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onMulSpeedChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onNameChanged(string oldValue) {}	//Avatar Monster Summon Teleporter Npc Collection Creation AvatarReplica Avataring 
		public virtual void onSchoolChanged(UInt16 oldValue) {}	//Avatar AvatarReplica Avataring 
		public virtual void onSelectedTargetIdChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation AvatarReplica 
		public virtual void onSexChanged(Byte oldValue) {}	//Avatar AvatarReplica Avataring 
		public virtual void onSiegeWarCampChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc AvatarReplica 
		public virtual void onSpaceNoChanged(UInt32 oldValue) {}	//Space WaitMapSpace CubeSpaceMgr WonderLandSpaceMgr AbyssSpaceMgr WorldLineSpaceMgr SiegeWarSpaceMgr DungeonSpaceMgr MonsterGrp Avatar Monster Summon Barrier Teleporter CityBattleTeleporter CoreAreaFlag Npc Collection Creation DuelFlag AvatarReplica Avataring RebornPos 
		public virtual void onSpeedChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation AvatarReplica Avataring 
		public virtual void onStateChanged(Int64 oldValue) {}	//Avatar Monster Summon Npc Creation AvatarReplica Avataring 
		public virtual void onState2Changed(Int64 oldValue) {}	//Avatar Monster Summon Npc Creation AvatarReplica Avataring 
		public virtual void onSummonSlotIdxChanged(Byte oldValue) {}	//Avatar AvatarReplica 
		public virtual void onTeleporterIdChanged(Int32 oldValue) {}	//Teleporter CityBattleTeleporter 
		public virtual void onUltraSkillPowerChanged(Byte oldValue) {}	//Avatar AvatarReplica 
	}
}
