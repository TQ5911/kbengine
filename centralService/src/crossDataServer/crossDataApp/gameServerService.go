package crossDataApp

import (
	"centralService/src/appLog"
	"centralService/src/common"
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
	return nil, nil
}

func (gss *GameServerService) ActiveTick(in *gameServerService.Void) (*gameServerService.Void, error) {
	_, err := gss.GetClientEndPoint().(*gameServerService.GameServerClient).ActiveTickCallback(&gameServerService.Void{})
	return nil, err
}

func (gss *GameServerService) AddGuildInfo(in *gameServerService.AddGuildInfoRequest) (*gameServerService.Void, error) {
	appLog.Info("add guild info:", in.GuildInfo.GuildUUID, in.GuildInfo.GuildName)
	gss.app.guildData.AddGuildInfo(&GuildInfoCache{
		guildUUID:  in.GuildInfo.GuildUUID,
		guildName:  in.GuildInfo.GuildName,
		serverId:   in.GuildInfo.ServerId,
		flag:       in.GuildInfo.Flag,
		guildScore: in.GuildInfo.GuildScore,
		guildLevel: in.GuildInfo.GuildLevel,
		guildIcon:  in.GuildInfo.GuildIcon,
		memberCnt:  in.GuildInfo.MemberCnt,
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

func (gss *GameServerService) RemoveGuildInfo(in *gameServerService.RemoveGuildInfoRequest) (*gameServerService.Void, error) {
	appLog.Info("remove guild info:", in.GuildUUID)
	gss.app.guildData.RemoveGuildInfo(in.GuildUUID, gss.app)
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

func (gss *GameServerService) SaveSiegeWarData(in *gameServerService.SaveSiegeWarDataRequest) (*gameServerService.Void, error) {
	appLog.Info("save siege war data, uuid:", in.Uuid, "size:", len(in.Data))
	data := make([]byte, len(in.Data))
	copy(data, in.Data)
	uuid := in.Uuid
	common.ExecuteConcurrently(func() {
		err := gss.app.siegeWarData.Save(data)
		_, cbErr := gss.GetClientEndPoint().(*gameServerService.GameServerClient).OnSaveSiegeWarData(&gameServerService.SaveSiegeWarDataResult{
			Uuid:    uuid,
			Success: err == nil,
		})
		if cbErr != nil {
			appLog.Error("on save siege war data callback error:", cbErr)
		}
	})
	return nil, nil
}

func (gss *GameServerService) LoadSiegeWarData(in *gameServerService.LoadSiegeWarDataRequest) (*gameServerService.Void, error) {
	appLog.Info("load siege war data, uuid:", in.Uuid)
	uuid := in.Uuid
	common.ExecuteConcurrently(func() {
		data := gss.app.siegeWarData.Load()
		_, cbErr := gss.GetClientEndPoint().(*gameServerService.GameServerClient).OnLoadSiegeWarData(&gameServerService.LoadSiegeWarDataResult{
			Data:    data,
			Uuid:    uuid,
			Success: true,
		})
		if cbErr != nil {
			appLog.Error("on load siege war data callback error:", cbErr)
		}
	})
	return nil, nil
}
