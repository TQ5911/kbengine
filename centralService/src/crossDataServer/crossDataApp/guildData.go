package crossDataApp

import (
	"centralService/src/appLog"
	"centralService/src/crossDataServer/crossDataApp/gameServerService"
	"database/sql"
	"fmt"
	"slices"
	"sync"
	"time"
)

const (
	RELATION_TYPE_NONE  = 0
	RELATION_TYPE_UNION = 1
	RELATION_TYPE_ENEMY = 2
)

type GuildData struct {
	guildInfos            map[uint64]*GuildInfoCache
	guildRelations        map[string]*GuildRelation
	enemyRelationPairList []string
	relationLock          sync.RWMutex
	relationVersion       int
	relationVersionId     int
}

func NewGuildData(db *sql.DB) *GuildData {
	sql := "SELECT guild_pair, relation_type, end_time FROM guild_relation"
	rows, err := db.Query(sql)
	if err != nil {
		appLog.Error("query guild relation error:", err.Error())
		return nil
	}
	defer rows.Close()

	guildRelations := make(map[string]*GuildRelation)
	enemyRelationPairList := make([]string, 0)

	for rows.Next() {
		var guildPair string
		var relationType int
		var endTime int64
		err = rows.Scan(&guildPair, &relationType, &endTime)
		if err != nil {
			appLog.Error("scan guild relation error:", err.Error())
			continue
		}
		guildRelations[guildPair] = NewGuildRelationFromPair(guildPair, relationType, endTime)

		if relationType == RELATION_TYPE_ENEMY {
			enemyRelationPairList = append(enemyRelationPairList, guildPair)
		}
	}

	sql = "SELECT id, version FROM relation_version"
	rows, err = db.Query(sql)
	if err != nil {
		appLog.Error("query relation version error:", err.Error())
		return nil
	}
	defer rows.Close()

	id := -1
	version := 0
	for rows.Next() {
		err = rows.Scan(&id, &version)
		if err != nil {
			appLog.Error("scan relation version error:", err.Error())
			continue
		}
		break
	}

	if id == -1 {
		sql = "INSERT INTO relation_version (version) VALUES (1)"
		_, err = db.Exec(sql)
		if err != nil {
			appLog.Error("insert relation version error:", err.Error())
			return nil
		}

		// get last insert id
		sql = "SELECT LAST_INSERT_ID()"
		err = db.QueryRow(sql).Scan(&id)
		if err != nil {
			appLog.Error("get last insert id error:", err.Error())
			return nil
		}
		version = 1
	}

	gd := &GuildData{
		guildInfos:            make(map[uint64]*GuildInfoCache),
		guildRelations:        guildRelations,
		enemyRelationPairList: enemyRelationPairList,
		relationLock:          sync.RWMutex{},
		relationVersion:       version,
		relationVersionId:     id,
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

func (gd *GuildData) RemoveGuildInfo(guildUUID uint64, db *sql.DB, crossDataApp *CrossDataApp) {
	delete(gd.guildInfos, guildUUID)

	removeEnemyList := make([]uint64, 0)
	removeUnionList := make([]uint64, 0)

	for _, guildRelation := range gd.guildRelations {
		if guildRelation.relationType == RELATION_TYPE_ENEMY {
			if guildRelation.guildUUID1 == guildUUID {
				removeEnemyList = append(removeEnemyList, guildRelation.guildUUID2)
			} else if guildRelation.guildUUID2 == guildUUID {
				removeEnemyList = append(removeEnemyList, guildRelation.guildUUID1)
			}
		} else if guildRelation.relationType == RELATION_TYPE_UNION {
			if guildRelation.guildUUID1 == guildUUID {
				removeUnionList = append(removeUnionList, guildRelation.guildUUID2)
			} else if guildRelation.guildUUID2 == guildUUID {
				removeUnionList = append(removeUnionList, guildRelation.guildUUID1)
			}
		}
	}

	for _, anotherGuildUUID := range removeEnemyList {
		removeMsg := gd.RemoveGuildRelation(guildUUID, anotherGuildUUID, RELATION_TYPE_ENEMY, true, db)
		if removeMsg != nil {
			crossDataApp.BroadcastRemoveGuildRelation(removeMsg)
		}
	}

	for _, anotherGuildUUID := range removeUnionList {
		removeMsg := gd.RemoveGuildRelation(guildUUID, anotherGuildUUID, RELATION_TYPE_UNION, true, db)
		if removeMsg != nil {
			crossDataApp.BroadcastRemoveGuildRelation(removeMsg)
		}
	}
}

func generateGuildPair(guildUUID1 uint64, guildUUID2 uint64) string {
	if guildUUID1 < guildUUID2 {
		return fmt.Sprintf("%d-%d", guildUUID1, guildUUID2)
	}
	return fmt.Sprintf("%d-%d", guildUUID2, guildUUID1)
}

func updateGuildRelation(guildPair string, relationType int, endTime int64, db *sql.DB) {
	sql := "UPDATE guild_relation SET relation_type = ?, end_time = ? WHERE guild_pair = ?"
	_, err := db.Exec(sql, relationType, endTime, guildPair)
	if err != nil {
		appLog.Error("update guild relation error:", err.Error())
	}
}

func insertGuildRelation(guildPair string, relationType int, endTime int64, db *sql.DB) {
	sql := "INSERT INTO guild_relation (guild_pair, relation_type, end_time) VALUES (?, ?, ?)"
	_, err := db.Exec(sql, guildPair, relationType, endTime)
	if err != nil {
		appLog.Error("insert guild relation error:", err.Error())
	}
}

func (gd *GuildData) updateRelationVersion(db *sql.DB) {
	newVersion := gd.relationVersion + 1
	sql := "UPDATE relation_version SET version = ? WHERE id = ?"
	_, err := db.Exec(sql, newVersion, gd.relationVersionId)
	if err != nil {
		appLog.Error("update relation version error:", err.Error())
	}
	gd.relationVersion = newVersion
}

func (gd *GuildData) addEnemyRelationPair(guildPair string) {
	if !slices.Contains(gd.enemyRelationPairList, guildPair) {
		gd.enemyRelationPairList = append(gd.enemyRelationPairList, guildPair)
	}
}

func (gd *GuildData) removeEnemyRelationPair(guildPair string) {
	gd.enemyRelationPairList = slices.DeleteFunc(gd.enemyRelationPairList, func(pair string) bool {
		return pair == guildPair
	})
}

func (gd *GuildData) AddGuildRelation(
	guildUUID1 uint64,
	guildUUID2 uint64,
	relationType int,
	endTime int64,
	db *sql.DB,
) (*gameServerService.BroadcastGuildRelationSingle, int) {
	if gd.guildInfos[guildUUID1] == nil || gd.guildInfos[guildUUID2] == nil {
		appLog.Error("guild info not found:", guildUUID1, guildUUID2)
		return nil, ERROR_CODE_NOT_FOUND_GUILD
	}

	guildPair := generateGuildPair(guildUUID1, guildUUID2)

	gd.relationLock.Lock()
	defer gd.relationLock.Unlock()
	guildRelationInfo := gd.guildRelations[guildPair]
	if guildRelationInfo != nil {
		appLog.Info("guild relation already exists:", guildPair)
		if guildRelationInfo.relationType == relationType {
			appLog.Info("guild relation already exists:", guildPair)
			return nil, ERROR_CODE_RELATION_ALREADY_EXISTS
		}

		if guildRelationInfo.relationType == RELATION_TYPE_ENEMY {
			appLog.Info("guild relation already exists:", guildPair)
			return nil, ERROR_CODE_RELATION_ALREADY_EXISTS
		}

		updateGuildRelation(guildPair, relationType, endTime, db)
	} else {
		relationNum1 := gd.getGuildRelationNum(guildUUID1, relationType)
		if relationType == RELATION_TYPE_UNION {
			if relationNum1 >= CrossDataConfig.UnionMaxNum {
				appLog.Info("guild union num max:", guildUUID1)
				return nil, ERROR_CODE_RELATION_MAX_NUM_GUILD1
			}
		} else if relationType == RELATION_TYPE_ENEMY {
			if relationNum1 >= CrossDataConfig.EnemyMaxNum {
				appLog.Info("guild enemy num max:", guildUUID1)
				return nil, ERROR_CODE_RELATION_MAX_NUM_GUILD1
			}
		}

		relationNum2 := gd.getGuildRelationNum(guildUUID2, relationType)
		if relationType == RELATION_TYPE_UNION {
			if relationNum2 >= CrossDataConfig.UnionMaxNum {
				appLog.Info("guild union num max:", guildUUID2)
				return nil, ERROR_CODE_RELATION_MAX_NUM_GUILD2
			}
		} else if relationType == RELATION_TYPE_ENEMY {
			if relationNum2 >= CrossDataConfig.EnemyMaxNum {
				appLog.Info("guild enemy num max:", guildUUID2)
				return nil, ERROR_CODE_RELATION_MAX_NUM_GUILD2
			}
		}

		insertGuildRelation(guildPair, relationType, endTime, db)
	}

	guildRelationInfo = NewGuildRelationFromPair(guildPair, relationType, endTime)

	gd.guildRelations[guildPair] = guildRelationInfo

	gd.updateRelationVersion(db)

	if relationType == RELATION_TYPE_ENEMY {
		gd.addEnemyRelationPair(guildPair)
	}

	return &gameServerService.BroadcastGuildRelationSingle{
		GuildRelation: &gameServerService.GuildRelation{
			GuildUUID1:   guildUUID1,
			GuildUUID2:   guildUUID2,
			RelationType: int32(relationType),
		},
		Version: uint32(gd.relationVersion),
	}, ERROR_CODE_SUCCESS
}

func (gd *GuildData) AllRelation() *gameServerService.GuildRelationAll {
	guildRelations := make([]*gameServerService.GuildRelation, 0)
	for _, guildRelation := range gd.guildRelations {
		guildUUID1, guildUUID2 := guildRelation.toPairGuildUUID()
		guildRelations = append(guildRelations, &gameServerService.GuildRelation{
			GuildUUID1:   guildUUID1,
			GuildUUID2:   guildUUID2,
			RelationType: int32(guildRelation.relationType),
		})
	}

	return &gameServerService.GuildRelationAll{
		GuildRelations: guildRelations,
		Version:        uint32(gd.relationVersion),
	}
}

func (gd *GuildData) RemoveGuildRelation(
	guildUUID1 uint64,
	guildUUID2 uint64,
	targetRelationType int,
	force bool,
	db *sql.DB,
) *gameServerService.BroadcastRemoveGuildRelation {
	guildPair := generateGuildPair(guildUUID1, guildUUID2)
	gd.relationLock.Lock()
	defer gd.relationLock.Unlock()
	guildRelationInfo := gd.guildRelations[guildPair]
	if guildRelationInfo == nil {
		appLog.Info("guild relation not found:", guildPair)
		return nil
	}

	if guildRelationInfo.relationType != targetRelationType {
		appLog.Info("guild relation type not match:", guildPair)
		return nil
	}

	if !force && guildRelationInfo.relationType == RELATION_TYPE_ENEMY {
		appLog.Info("guild relation enemy could not be removed:", guildPair)
		return nil
	}

	sql := "DELETE FROM guild_relation WHERE guild_pair = ?"
	_, err := db.Exec(sql, guildPair)
	if err != nil {
		appLog.Error("delete guild relation error:", err.Error())
	}

	delete(gd.guildRelations, guildPair)
	gd.updateRelationVersion(db)

	if guildRelationInfo.relationType == RELATION_TYPE_ENEMY {
		gd.removeEnemyRelationPair(guildPair)
	}

	return &gameServerService.BroadcastRemoveGuildRelation{
		GuildUUID1: guildUUID1,
		GuildUUID2: guildUUID2,
		Version:    uint32(gd.relationVersion),
	}
}

func (gd *GuildData) checkAndRemoveExpiredRelation(db *sql.DB, crossDataApp *CrossDataApp) {
	now := time.Now().Unix()
	removeList := make([][2]uint64, 0)
	for _, guildPair := range gd.enemyRelationPairList {
		guildRelationInfo := gd.guildRelations[guildPair]
		if guildRelationInfo == nil {
			continue
		}

		if guildRelationInfo.endTime < now {
			guildUUID1, guildUUID2 := guildRelationInfo.toPairGuildUUID()
			removeList = append(removeList, [2]uint64{guildUUID1, guildUUID2})
		}
	}

	for _, guildPair := range removeList {
		removeMsg := gd.RemoveGuildRelation(guildPair[0], guildPair[1], RELATION_TYPE_ENEMY, true, db)
		if removeMsg != nil {
			crossDataApp.BroadcastRemoveGuildRelation(removeMsg)
		}
	}
}

func (gd *GuildData) getGuildRelationNum(guildUUID uint64, relationType int) int {
	num := 0
	for _, guildRelation := range gd.guildRelations {
		if !guildRelation.InGuild(guildUUID) {
			continue
		}

		if guildRelation.relationType == relationType {
			num++
		}
	}
	return num
}

func (gd *GuildData) getEnemyGuildInfos(guildUUID uint64) []*gameServerService.EnemyGuildInfo {
	guildInfos := make([]*gameServerService.EnemyGuildInfo, 0)
	for _, guildRelation := range gd.guildRelations {
		if !guildRelation.InGuild(guildUUID) {
			continue
		}

		anotherGuildUUID := guildRelation.guildUUID1
		if anotherGuildUUID == guildUUID {
			anotherGuildUUID = guildRelation.guildUUID2
		}

		guildInfo := gd.getGuildInfo(anotherGuildUUID)
		if guildInfo == nil {
			continue
		}

		guildInfos = append(guildInfos, &gameServerService.EnemyGuildInfo{
			GuildUUID:  anotherGuildUUID,
			GuildName:  guildInfo.GuildName,
			ServerId:   guildInfo.ServerId,
			Flag:       guildInfo.Flag,
			GuildScore: guildInfo.GuildScore,
			GuildLevel: guildInfo.GuildLevel,
			EndTime:    uint32(guildRelation.endTime),
			MemberCnt:  guildInfo.MemberCnt,
			GuildIcon:  guildInfo.GuildIcon,
		})
	}

	return guildInfos
}
