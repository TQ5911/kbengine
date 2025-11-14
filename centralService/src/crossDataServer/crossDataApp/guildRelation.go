package crossDataApp

import (
	"strconv"
	"strings"
)

type GuildRelation struct {
	guildPair    string
	relationType int
	endTime      int64
	guildUUID1   uint64
	guildUUID2   uint64
}

func (gr *GuildRelation) InGuild(guildUUID uint64) bool {
	return gr.guildUUID1 == guildUUID || gr.guildUUID2 == guildUUID
}

func SplitPair(guildPair string) (uint64, uint64) {
	guildUUIDs := strings.Split(guildPair, "-")
	if len(guildUUIDs) != 2 {
		return 0, 0
	}
	guildUUID1, err := strconv.ParseUint(guildUUIDs[0], 10, 64)
	if err != nil {
		return 0, 0
	}
	guildUUID2, err := strconv.ParseUint(guildUUIDs[1], 10, 64)
	if err != nil {
		return 0, 0
	}

	return guildUUID1, guildUUID2

}

func NewGuildRelationFromPair(guildPair string, relationType int, endTime int64) *GuildRelation {
	guildUUID1, guildUUID2 := SplitPair(guildPair)
	return &GuildRelation{
		guildPair:    guildPair,
		relationType: relationType,
		endTime:      endTime,
		guildUUID1:   guildUUID1,
		guildUUID2:   guildUUID2,
	}
}

func NewGuildRelationFromUUID(guildUUID1 uint64, guildUUID2 uint64, relationType int, endTime int64) *GuildRelation {
	return &GuildRelation{
		guildPair:    generateGuildPair(guildUUID1, guildUUID2),
		relationType: relationType,
		endTime:      endTime,
		guildUUID1:   guildUUID1,
		guildUUID2:   guildUUID2,
	}
}

func (gr *GuildRelation) toPairGuildUUID() (uint64, uint64) {
	guildUUIDs := strings.Split(gr.guildPair, "-")
	if len(guildUUIDs) != 2 {
		return 0, 0
	}
	guildUUID1, err := strconv.ParseUint(guildUUIDs[0], 10, 64)
	if err != nil {
		return 0, 0
	}
	guildUUID2, err := strconv.ParseUint(guildUUIDs[1], 10, 64)
	if err != nil {
		return 0, 0
	}

	return guildUUID1, guildUUID2
}
