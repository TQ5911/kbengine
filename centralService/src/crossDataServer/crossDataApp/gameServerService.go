package crossDataApp

import (
	"centralService/src/appLog"
	gameServerService "centralService/src/crossDataServer/crossDataApp/gameServerService"
	"centralService/src/trpc"
	"errors"
	"fmt"
)

type GameServerService struct {
	*trpc.ServerEndPoint
	app      *CrossDataApp
	serverId uint32
}

func (gss *GameServerService) OnLoseConnection() {
	appLog.Info("on lose connection")
	gss.app.removeGameServer(gss)
}

func (gss *GameServerService) RegisterGameServer(in *gameServerService.RegisterGameServerRequest) (*gameServerService.Void, error) {
	appLog.Info("register game server:", in.ServerId)
	server := gss.app.getGameServer(in.ServerId)
	if server != nil {
		return nil, errors.New(fmt.Sprint("baseapp is already registered: ", in.ServerId))
	}

	if in.ServerId == 0 {
		return nil, errors.New(fmt.Sprint("invalid ServerId: ", in.ServerId))
	}

	gss.serverId = in.ServerId

	gss.app.addGameServer(gss)
	allRelation := gss.app.guildData.AllRelation()
	_, err := gss.GetClientEndPoint().(*gameServerService.GameServerClient).OnGuildRelationAll(allRelation)
	return nil, err
}

func (gss *GameServerService) ActiveTick(in *gameServerService.Void) (*gameServerService.Void, error) {
	_, err := gss.GetClientEndPoint().(*gameServerService.GameServerClient).ActiveTickCallback(&gameServerService.Void{})
	return nil, err
}

func (gss *GameServerService) AddGuildInfo(in *gameServerService.AddGuildInfoRequest) (*gameServerService.Void, error) {
	appLog.Info("add guild info:", in.GuildInfo.GuildUUID, in.GuildInfo.GuildName)
	gss.app.guildData.AddGuildInfo(&GuildInfoCache{
		guildUUID:        in.GuildInfo.GuildUUID,
		guildName:        in.GuildInfo.GuildName,
		serverId:         in.GuildInfo.ServerId,
		flag:             in.GuildInfo.Flag,
		guildScore:       in.GuildInfo.GuildScore,
		guildLevel:       in.GuildInfo.GuildLevel,
		guildIcon:        in.GuildInfo.GuildIcon,
		memberCnt:        in.GuildInfo.MemberCnt,
		maxGuildUnionNum: in.GuildInfo.MaxGuildUnionNum,
	})

	_, err := gss.GetClientEndPoint().(*gameServerService.GameServerClient).OnAddGuildInfo(&gameServerService.AddGuildInfoResult{
		Uuid: in.Uuid,
	})
	return nil, err
}

func (gss *GameServerService) GetGuildInfos(in *gameServerService.GetGuildInfosRequest) (*gameServerService.Void, error) {
	appLog.Info("get guild infos:", in.Uuid)
	guildInfos := gss.app.guildData.getGuildInfos(in.ServerId)
	_, err := gss.GetClientEndPoint().(*gameServerService.GameServerClient).OnGetGuildInfos(&gameServerService.GetGuildInfosResult{
		Uuid:       in.Uuid,
		GuildInfos: guildInfos,
	})
	return nil, err
}

func (gss *GameServerService) GetGuildInfosByGuildUUID(in *gameServerService.GetGuildInfosByGuildUUIDRequest) (*gameServerService.Void, error) {
	appLog.Info("get guild infos by guild uuid:", in.Uuid)
	guildInfos := gss.app.guildData.getGuildInfosByGuildUUID(in.GuildUUIDs)
	_, err := gss.GetClientEndPoint().(*gameServerService.GameServerClient).OnGetGuildInfos(&gameServerService.GetGuildInfosResult{
		Uuid:       in.Uuid,
		GuildInfos: guildInfos,
	})
	return nil, err
}

func (gss *GameServerService) GetEnemyGuildInfos(in *gameServerService.GetEnemyGuildInfosRequest) (*gameServerService.Void, error) {
	appLog.Info("get enemy guild infos:", in.GuildUUID)
	guildInfos := gss.app.guildData.getEnemyGuildInfos(in.GuildUUID)
	_, err := gss.GetClientEndPoint().(*gameServerService.GameServerClient).OnGetEnemyGuildInfos(&gameServerService.GetEnemyGuildInfosResult{
		Uuid:            in.Uuid,
		EnemyGuildInfos: guildInfos,
	})
	return nil, err
}

func (gss *GameServerService) RemoveGuildInfo(in *gameServerService.RemoveGuildInfoRequest) (*gameServerService.Void, error) {
	appLog.Info("remove guild info:", in.GuildUUID)
	gss.app.guildData.RemoveGuildInfo(in.GuildUUID, gss.app.db, gss.app)
	return nil, nil
}

func (gss *GameServerService) BroadcastGuildRelationSingleMsg(relation *gameServerService.BroadcastGuildRelationSingle) {
	for _, server := range gss.app.gameServers {
		server.GetClientEndPoint().(*gameServerService.GameServerClient).OnBroadcastGuildRelationSingle(relation)
	}
}

func (gss *GameServerService) AddGuildRelation(in *gameServerService.AddGuildRelationRequest) (*gameServerService.Void, error) {
	appLog.Info("add guild relation:", in.GuildUUID1, in.GuildUUID2)
	relation, errCode := gss.app.guildData.AddGuildRelation(in.GuildUUID1, in.GuildUUID2, int(in.RelationType), in.EndTime, gss.app.db)

	// 获取对方的工会信息返回给己方
	receiverGuildInfo := gss.app.guildData.getGuildInfo(in.GuildUUID2)

	if relation != nil {
		gss.BroadcastGuildRelationSingleMsg(relation)
		_, err := gss.GetClientEndPoint().(*gameServerService.GameServerClient).OnAddGuildRelation(&gameServerService.AddGuildRelationResult{
			Uuid:      in.Uuid,
			Success:   true,
			GuildInfo: receiverGuildInfo,
			ErrCode:   uint32(errCode),
		})

		if err != nil {
			appLog.Error("on add guild relation error1:", err)
		}

		// 通知对方
		senderGuildInfo := gss.app.guildData.getGuildInfo(in.GuildUUID1)
		receiverServer := gss.app.getGameServer(receiverGuildInfo.ServerId)
		receiverServer.GetClientEndPoint().(*gameServerService.GameServerClient).OnNotifyGuildRelation(&gameServerService.OnNotifyGuildRelation{
			GuildInfo:         senderGuildInfo,
			RelationType:      int32(in.RelationType),
			ReceiverGuildUUID: in.GuildUUID2,
		})
		return nil, err
	}

	_, err := gss.GetClientEndPoint().(*gameServerService.GameServerClient).OnAddGuildRelation(&gameServerService.AddGuildRelationResult{
		Uuid:      in.Uuid,
		Success:   false,
		GuildInfo: receiverGuildInfo,
		ErrCode:   uint32(errCode),
	})

	if err != nil {
		appLog.Error("on add guild relation error2:", err)
	}

	return nil, err
}

func (gss *GameServerService) RemoveGuildRelation(in *gameServerService.RemoveGuildRelationRequest) (*gameServerService.Void, error) {
	appLog.Info("remove guild relation:", in.GuildUUID1, in.GuildUUID2)
	relation := gss.app.guildData.RemoveGuildRelation(in.GuildUUID1, in.GuildUUID2, int(in.RelationType), false, gss.app.db)
	receiverGuildInfo := gss.app.guildData.getGuildInfo(in.GuildUUID2)
	if relation != nil {
		gss.app.BroadcastRemoveGuildRelation(relation)
		_, err := gss.GetClientEndPoint().(*gameServerService.GameServerClient).OnRemoveGuildRelation(&gameServerService.RemoveGuildRelationResult{
			Success:   true,
			Uuid:      in.Uuid,
			GuildInfo: receiverGuildInfo,
		})

		if in.RelationType == int32(RELATION_TYPE_UNION) {
			senderGuildInfo := gss.app.guildData.getGuildInfo(in.GuildUUID1)
			receiverServer := gss.app.getGameServer(receiverGuildInfo.ServerId)
			receiverServer.GetClientEndPoint().(*gameServerService.GameServerClient).OnNotifyGuildCancelUnion(&gameServerService.OnNotifyGuildCancelUnion{
				GuildInfo:         senderGuildInfo,
				ReceiverGuildUUID: in.GuildUUID2,
			})
		}
		return nil, err
	}

	_, err := gss.GetClientEndPoint().(*gameServerService.GameServerClient).OnRemoveGuildRelation(&gameServerService.RemoveGuildRelationResult{
		Success:   false,
		Uuid:      in.Uuid,
		GuildInfo: receiverGuildInfo,
	})
	return nil, err
}

func (gss *GameServerService) ApplyGuildUnion(in *gameServerService.ApplyGuildUnionRequest) (*gameServerService.Void, error) {
	appLog.Info("apply guild union:", in.SenderGuildUUID, in.ReceiverGuildUUID)
	senderGuildInfo := gss.app.guildData.getGuildInfo(in.SenderGuildUUID)
	receiverGuildInfo := gss.app.guildData.getGuildInfo(in.ReceiverGuildUUID)
	if senderGuildInfo == nil || receiverGuildInfo == nil {
		appLog.Error("guild not found:", in.SenderGuildUUID, in.ReceiverGuildUUID)
		return nil, nil
	}

	receiverServer := gss.app.getGameServer(receiverGuildInfo.ServerId)
	if receiverServer == nil {
		appLog.Error("receiver server not found:", receiverGuildInfo.ServerId)
		return nil, nil
	}

	receiverServer.GetClientEndPoint().(*gameServerService.GameServerClient).OnApplyGuildUnion(&gameServerService.OnApplyGuildUnionRequest{
		SenderGuildUUID:   in.SenderGuildUUID,
		ReceiverGuildUUID: in.ReceiverGuildUUID,
		SenderGuildInfo:   senderGuildInfo,
	})

	_, err := gss.GetClientEndPoint().(*gameServerService.GameServerClient).OnApplyGuildUnionResult(&gameServerService.ApplyGuildUnionResult{
		Uuid:              in.Uuid,
		ReceiverGuildInfo: receiverGuildInfo,
	})
	return nil, err
}

func (gss *GameServerService) RemoveReceiverGuildApplyUnion(in *gameServerService.RemoveReceiverGuildApplyUnionRequest) (*gameServerService.Void, error) {
	appLog.Info("remove receiver guild apply union:", in.SenderGuildUUID, in.ReceiverGuildUUID)
	receiverGuildInfo := gss.app.guildData.getGuildInfo(in.ReceiverGuildUUID)
	if receiverGuildInfo == nil {
		appLog.Error("receiver guild not found:", in.ReceiverGuildUUID)
		return nil, nil
	}

	receiverServer := gss.app.getGameServer(receiverGuildInfo.ServerId)
	if receiverServer == nil {
		appLog.Error("receiver server not found:", receiverGuildInfo.ServerId)
		return nil, nil
	}

	receiverServer.GetClientEndPoint().(*gameServerService.GameServerClient).OnNotifyRemoveReceiverGuildApplyUnion(&gameServerService.NotifyRemoveReceiverGuildApplyUnion{
		SenderGuildUUID:   in.SenderGuildUUID,
		ReceiverGuildUUID: in.ReceiverGuildUUID,
	})
	return nil, nil
}

func (gss *GameServerService) GetCrossServerGuildDetail(in *gameServerService.GetCrossServerGuildDetailRequest) (*gameServerService.Void, error) {
	appLog.Info("get cross server guild detail:", in.GuildUUID)
	guildInfo := gss.app.guildData.getGuildInfo(in.GuildUUID)
	if guildInfo == nil {
		appLog.Error("guild not found:", in.GuildUUID)
		return nil, nil
	}

	receiverServer := gss.app.getGameServer(guildInfo.ServerId)
	if receiverServer == nil {
		appLog.Error("receiver server not found:", guildInfo.ServerId)
		return nil, nil
	}

	receiverServer.GetClientEndPoint().(*gameServerService.GameServerClient).OnGetCrossServerGuildDetailToOtherServer(&gameServerService.GetCrossServerGuildDetailToOtherServer{
		GuildUUID:      in.GuildUUID,
		SenderServerId: in.SenderServerId,
		Uuid:           in.Uuid,
	})
	return nil, nil
}

func (gss *GameServerService) GetCrossServerGuildDetailFromOtherServer(in *gameServerService.GetCrossServerGuildDetailFromOtherServer) (*gameServerService.Void, error) {
	appLog.Info("get cross server guild detail from other server:", in.GuildDetailInfo.GuildUUID)
	receiverServer := gss.app.getGameServer(in.SenderServerId)
	if receiverServer == nil {
		appLog.Error("receiver server not found:", in.SenderServerId)
		return nil, nil
	}

	receiverServer.GetClientEndPoint().(*gameServerService.GameServerClient).OnGetCrossServerGuildDetail(&gameServerService.GetCrossServerGuildDetailResult{
		GuildDetailInfo: in.GuildDetailInfo,
		Uuid:            in.Uuid,
	})
	return nil, nil
}

func (gss *GameServerService) DoOnCrossGuildRequest(in *gameServerService.DoOnCrossGuildRequest) (*gameServerService.Void, error) {
	appLog.Info("do on cross guild request:", in.GuildUUID, in.Func)
	receiverGuildInfo := gss.app.guildData.getGuildInfo(in.GuildUUID)
	if receiverGuildInfo == nil {
		if in.Uuid != 0 {
			gss.GetClientEndPoint().(*gameServerService.GameServerClient).OnDoOnCrossGuildResult(&gameServerService.DoOnCrossGuildResult{
				Uuid:    in.Uuid,
				Success: false,
				Result:  nil,
			})
		}
		return nil, nil
	}

	receiverServer := gss.app.getGameServer(receiverGuildInfo.ServerId)
	if receiverServer == nil {
		appLog.Error("receiver server not found:", receiverGuildInfo.ServerId)
		return nil, nil
	}

	receiverServer.GetClientEndPoint().(*gameServerService.GameServerClient).OnDoOnCrossGuildToGameServer(&gameServerService.DoOnCrossGuildToGameServer{
		GuildUUID:      in.GuildUUID,
		Func:           in.Func,
		Args:           in.Args,
		Uuid:           in.Uuid,
		SenderServerId: gss.serverId,
	})
	return nil, nil
}

func (gss *GameServerService) DoOnCrossGuildResultBack(in *gameServerService.DoOnCrossGuildResultBack) (*gameServerService.Void, error) {
	appLog.Info("on do on cross guild result back:", in.Uuid, in.ServerId)
	receiverServer := gss.app.getGameServer(in.ServerId)
	if receiverServer == nil {
		appLog.Error("receiver server not found:", in.ServerId)
		return nil, nil
	}

	receiverServer.GetClientEndPoint().(*gameServerService.GameServerClient).OnDoOnCrossGuildResult(&gameServerService.DoOnCrossGuildResult{
		Uuid:    in.Uuid,
		Success: in.Success,
		Result:  in.Result,
	})
	return nil, nil
}
