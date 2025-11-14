package Auction

const (
	_ = iota
	SERVICE_CLIENT_AUTH
	SERVICE_GAME_SERVER
)

const (
	UNKNOWN_ERR = iota
	AUCTION_OK
	PARAM_ERROR

	AUCTION_TYPE_ERR                = 20000 // 交易行类型错误
	AUCTION_ALREADY_IN_AUCTION      = 20001 // 交易物品已经在交易行
	AUCTION_ITEM_ATTR_NOT_DEFINED   = 20002 // 交易物品属性没有定义
	AUCTION_INDEX_ALREADY_ADDED     = 20003 // 交易行索引已经存在
	AUCTION_INDEX_NOT_FOUND         = 20004 // 交易行索引没有找到
	AUCTION_NOT_IN_AUCTION          = 20005 // 交易行物品没有找见
	AUCTION_CACHE_NOT_INIT          = 20006 // 玩家交易数据没有初始化完毕
	AUCTION_AVATAR_GRID_FULL        = 20007 // 玩家可交易数量已满
	AUCTION_DEDUCT_ITEM_ERROR       = 20008 // 玩家(出售时)尝试扣除物品失败
	AUCTION_DEDUCT_ITEM_NOT_FOUND   = 20009 // 玩家(出售时候)没有找到物品
	AUCTION_BUY_ITEM_NOT_ENOUGH     = 20010 // 玩家购买物品时物品交易行数量不足
	AUCTION_COIN_NOU_ENOUGH         = 20011 // 玩家铜贝不足
	AUCTION_ITEM_IS_LOCKED          = 20012 // 交易行物品被锁住(暂时有其他交易进行)
	AUCTION_BUY_MUST_NOT_BE_STACKED = 20013 // 交易物品必须不可堆叠
	AUCTION_BUY_MUST_BE_STACKED     = 20014 // 交易物品必须可堆叠
	AUCTION_SALE_ITEM_NUM_ERROR     = 20015 // 交易物品數量错误
	AUCTION_ITEM_ALREADY_BE_BINDED  = 20016 // 交易物品被绑定
	AUCTION_IS_IN_NOTIFY            = 20017 // 交易物品在公示期
	// AUCTION_CANNOT_CANCEL_SALE              = 20018)     // 交易物品暂时无法下架
	AUCTION_REVIEW_NOT_FOUND             = 20019 // 审核物品(铜贝/金丝玉贝)未找到
	AUCTION_REVIEWED_NUMBER_NOT_ENOUGH   = 20020 // 已审核物品不足
	AUCTION_ITEM_IN_COOLDOWN             = 20021 // 交易物品正在冷却
	AUCTION_PLAYER_BAG_GRID_NOT_ENOUGH   = 20022 // 玩家背包剩余格子不足
	AUCTION_CANCEL_SALE_ITEM_NOT_FOUND   = 20023 // 下架物品没有找到
	AUCTION_CANCEL_SALE_GBID_NOT_MATCH   = 20024 // 下架物品PlayerGBID不匹配
	AUCTION_ITEM_CANNOT_CANCEL_SALE      = 20025 // 物品无法被下架
	AUCTION_IS_EXPIRED                   = 20026 // 物品已经过期
	AUCTION_PLAYER_BAG_IS_LOCKED         = 20027 // 玩家背包被锁住, 无法交易
	AUCTION_BUY_CHECK_NOT_MATCH          = 20028 // 玩家购买时校验不通过
	AUCTION_FOLLOWED_ITEM_MAXIMUM        = 20029 // 玩家关注物品到达上限
	AUCTION_SALE_RECOMMAND_PRICE_NOT_DEF = 20030 // itemId没有对应推荐定价
	AUCTION_SALE_RECOMMAND_PRICE_OOF     = 20031 // itemId定价超过推荐百分比
	AUCTION_UNLOCK_GRID_MAXIMUN          = 20032 // 交易行解锁格子到达上限
	AUCTION_UNLOCK_COST_NOT_ENOUGH       = 20033 // 交易行解锁格子扣除物品不足
	AUCTION_MONEY_NOU_ENOUGH             = 20034 // 玩家金币不足
	AUCTION_PLAYER_NOT_IN_GUILD          = 20035 // 玩家不在对应帮会中
	AUCTION_HOMECOMP_ITEM_UN_IDENTIFIED  = 20037 // 出售家具未鉴定
	AUCTION_PLAYER_BAG_TYPE_UNKNOWN      = 20038 // 交易行背包类型未知
	AUCTION_CANNOT_BUY_SELF_ITEM         = 20039 // 交易行无法购买自己卖出的商品
	AUCTION_PLAYER_MAIL_SPACE_FULL       = 20040 // 玩家邮件剩余空间不足
	AUCTION_SALED_ITEM_REJECTED          = 20041 // 交易行对应物品无法出售

	AUCTION_IDIP_GM_BAN = 20100 // IDIP禁止
)

const (
	ServiceStatus_None         = 0
	ServiceStatus_Connected    = 1
	ServiceStatus_Disconnected = 2
)

const (
	BAG_TYPE_NORMAL  = 0
	BAG_TYPE_ITEM    = 1
	BAG_TYPE_COLLECT = 2
	BAG_TYPE_CLOTH   = 3
)

const (
	AUCTION_SOURCE_UNKNOWN = iota
	AUCTION_SOURCE_PLAYER  // 玩家上架
)

const (
	AUCTION_STATUS_INIT    = iota
	AUCTION_STATUS_NOTIFY  // 通知
	AUCTION_STATUS_SELLING // 上架
	AUCTION_STATUS_REVIEW  // 审核
	AUCTION_STATUS_SOLD    // 已售
	AUCTION_STATUS_CANCEL  // 取消
	AUCTION_STATUS_EXPIRED // 过期
)

const (
	AUCTION_TYPE_UNKNOWN = iota
	AUCTION_TYPE_COIN    // 金币交易行
)

const (
	INDEX_KEY_ITEMID     = "itemId"
	INDEX_KEY_PLAYERGBID = "fromPlayerGBID"
)

var auctionIndexKeys = []string{ // 拍卖行索引信息
	INDEX_KEY_ITEMID,
	INDEX_KEY_PLAYERGBID}

// 32位的hash函数
func DirectUInt32Sharding(key uint32) uint32 {
	return key
}

// 64位的hash函数
func DirectUInt64Sharding(key uint64) uint32 {
	return uint32(key) ^ uint32(key>>32)
}
