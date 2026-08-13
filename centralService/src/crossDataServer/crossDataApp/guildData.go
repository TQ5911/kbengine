package crossDataApp

import (
	"centralService/src/crossDataServer/crossDataApp/gameServerService"
	"sync"
)

const (
	RELATION_TYPE_NONE  = 0
	RELATION_TYPE_UNION = 1
	RELATION_TYPE_ENEMY = 2
)

type GuildData struct {
	guildInfos            map[uint64]*GuildInfoCache
	enemyRelationPairList []string
	relationLock          sync.RWMutex
	relationVersion       int
	relationVersionId     int
}

func NewGuildData() *GuildData {
	gd := &GuildData{
		guildInfos:   make(map[uint64]*GuildInfoCache),
		relationLock: sync.RWMutex{},
	}

	return gd
}

func (gd *GuildData) getGuildInfo(guildUUID uint64) *gameServerService.GuildInfo {
	guildInfo := gd.guildInfos[guildUUID]
	if guildInfo == nil {
		return nil
	}
	return &gameServerService.GuildInfo{
		GuildUUID:  guildInfo.guildUUID,
		GuildName:  guildInfo.guildName,
		ServerId:   guildInfo.serverId,
		Flag:       guildInfo.flag,
		GuildScore: guildInfo.guildScore,
		GuildLevel: guildInfo.guildLevel,
		GuildIcon:  guildInfo.guildIcon,
		MemberCnt:  guildInfo.memberCnt,
	}
}

func (gd *GuildData) getGuildInfos(excludeServerId uint32) []*gameServerService.GuildInfo {
	guildInfos := make([]*gameServerService.GuildInfo, 0)
	for _, guildInfo := range gd.guildInfos {
		if guildInfo.serverId == excludeServerId {
			continue
		}

		guildInfos = append(guildInfos, &gameServerService.GuildInfo{
			GuildUUID:  guildInfo.guildUUID,
			GuildName:  guildInfo.guildName,
			ServerId:   guildInfo.serverId,
			Flag:       guildInfo.flag,
			GuildScore: guildInfo.guildScore,
			GuildLevel: guildInfo.guildLevel,
			GuildIcon:  guildInfo.guildIcon,
			MemberCnt:  guildInfo.memberCnt,
		})
	}
	return guildInfos
}

func (gd *GuildData) getGuildInfosByGuildUUID(guildUUIDs []uint64) []*gameServerService.GuildInfo {
	guildInfos := make([]*gameServerService.GuildInfo, 0)
	for _, guildUUID := range guildUUIDs {
		guildInfo := gd.guildInfos[guildUUID]
		if guildInfo == nil {
			continue
		}

		guildInfos = append(guildInfos, &gameServerService.GuildInfo{
			GuildUUID:  guildInfo.guildUUID,
			GuildName:  guildInfo.guildName,
			ServerId:   guildInfo.serverId,
			Flag:       guildInfo.flag,
			GuildScore: guildInfo.guildScore,
			GuildLevel: guildInfo.guildLevel,
			GuildIcon:  guildInfo.guildIcon,
			MemberCnt:  guildInfo.memberCnt,
		})
	}
	return guildInfos
}

func (gd *GuildData) AddGuildInfo(guildInfo *GuildInfoCache) {
	gd.guildInfos[guildInfo.guildUUID] = guildInfo
}

func (gd *GuildData) RemoveGuildInfo(guildUUID uint64, crossDataApp *CrossDataApp) {
	delete(gd.guildInfos, guildUUID)
}
