package Router

import (
	"centralService/src/appLog"
	"centralService/src/router/routerApp/routerCluster"
	"centralService/src/trpc"
	"net"
	"strconv"
	"sync"
	"time"

	"github.com/google/uuid"
)

const (
	routerClusterConnectTimeout = 5 * time.Second
	routerClusterReadTimeout    = 10 * time.Second
)

type RouterNodeMeta struct {
	RouterId      uint32
	ClusterAddr   string
	GameServerIds []uint32
	LastTickMs    int64
}

// RouterNodeState: 与一个对端 router 节点对应的状态。
//   - Client: 该连接上持有的 client 桩（用于本端主动 forwardToGameServer）
//   - 本端作为被连接方时（NewService 创建的 server 端），StartServer 启动 Serve 循环
type RouterNodeState struct {
	mu      sync.Mutex
	routerId uint32
	addr     string
	client   *routerCluster.RouterNodeServiceClient
	channel  *trpc.RpcChannel
	closing  bool
	closed   chan struct{}
}

// 新建"作为 client 端"发起的连接（小 ID 端主动 dial 大 ID 端）
// app 透传进来: 虽是本端 dial, 但 conn 同样要接收对端 (大 ID) 的 RPC,
// 特别是 ForwardToGameServer —— 本节点需要能 getGameServer 把消息投到本节点游戏服。
func newRouterNodeStateAsClient(routerId uint32, addr string, app *RouterApp) (*RouterNodeState, error) {
	conn, err := net.DialTimeout("tcp", addr, routerClusterConnectTimeout)
	if err != nil {
		return nil, err
	}
	rpcUUID := uuid.New()
	channel := trpc.NewRpcChannel(rpcUUID, conn)
	clientStub := routerCluster.NewRouterNodeServiceClient(channel)
	endPoint := &routerNodeService{
		ServerEndPoint: routerCluster.NewRouterNodeServiceService(clientStub),
		app:            app,
	}
	channel.SetEndPoint(endPoint)
	state := &RouterNodeState{
		routerId: routerId,
		addr:     addr,
		client:   clientStub,
		channel:  channel,
		closed:   make(chan struct{}),
	}
	endPoint.incomingState = state
	go func() {
		endPoint.Serve()
		close(state.closed)
	}()
	return state, nil
}

// 新建"作为 server 端"接收的连接（大 ID 端被小 ID 连过来）
// app 用于让 routerNodeService 能访问 clusterTopology 等
func newRouterNodeStateAsServer(conn net.Conn, app *RouterApp) *RouterNodeState {
	rpcUUID := uuid.New()
	channel := trpc.NewRpcChannel(rpcUUID, conn)
	clientStub := routerCluster.NewRouterNodeServiceClient(channel)
	endPoint := &routerNodeService{
		ServerEndPoint: routerCluster.NewRouterNodeServiceService(clientStub),
		app:            app,
	}
	channel.SetEndPoint(endPoint)
	state := &RouterNodeState{
		addr:    conn.RemoteAddr().String(),
		client:  clientStub,
		channel: channel,
		closed:  make(chan struct{}),
	}
	endPoint.incomingState = state
	go func() {
		endPoint.Serve()
		close(state.closed)
	}()
	return state
}

func (s *RouterNodeState) RouterId() uint32 {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.routerId
}

func (s *RouterNodeState) Addr() string {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.addr
}

func (s *RouterNodeState) Client() *routerCluster.RouterNodeServiceClient {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.client
}

func (s *RouterNodeState) SetAddr(addr string) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.addr = addr
}

func (s *RouterNodeState) SetRouterId(id uint32) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.routerId = id
}

func (s *RouterNodeState) Close() {
	s.mu.Lock()
	if s.closing {
		s.mu.Unlock()
		return
	}
	s.closing = true
	ch := s.channel
	s.mu.Unlock()
	if ch != nil {
		ch.Disconnect()
	}
}

func (s *RouterNodeState) Closed() <-chan struct{} {
	return s.closed
}

// Serve 实现 trpc.IServerEndPoint 接口，供 common.Run 框架调用。
// 连接已经在 NewRouterNodeStateAs{Server,Client} 里启动了 Serve 循环，
// 这里仅做阻塞直到连接关闭。
func (s *RouterNodeState) Serve() {
	<-s.closed
}

// OnLoseConnection 实现 trpc.IServerEndPoint 接口。
// 真正的清理由 RouterNodeState 自己的 Serve 循环结束后触发，
// 这里只记一条诊断日志。
func (s *RouterNodeState) OnLoseConnection() {
	s.mu.Lock()
	rid := s.routerId
	addr := s.addr
	s.mu.Unlock()
	appLog.Infof("routerCluster: OnLoseConnection, routerId=%d addr=%s", rid, addr)
}

// GetServiceDesc 实现 trpc.IChannelService 接口。
func (s *RouterNodeState) GetServiceDesc() *trpc.ServiceDesc {
	return &routerCluster.RouterNodeServiceServiceDesc
}

// GetRpcChannel / SetRpcChannel 实现 trpc.IEndPoint 接口
func (s *RouterNodeState) GetRpcChannel() *trpc.RpcChannel {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.channel
}

func (s *RouterNodeState) SetRpcChannel(ch *trpc.RpcChannel) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.channel = ch
}

// SetClientEndPoint / GetClientEndPoint: 让 routerNodeService 的 client 引用挂到这里
func (s *RouterNodeState) SetClientEndPoint(ep trpc.IEndPoint) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if c, ok := ep.(*routerCluster.RouterNodeServiceClient); ok {
		s.client = c
	}
}

func (s *RouterNodeState) GetClientEndPoint() trpc.IEndPoint {
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.client == nil {
		return nil
	}
	return s.client
}

type ClusterTopology struct {
	mu       sync.RWMutex
	app      *RouterApp
	nodes    map[uint32]*RouterNodeState
}

func newClusterTopology(app *RouterApp) *ClusterTopology {
	return &ClusterTopology{
		app:   app,
		nodes: make(map[uint32]*RouterNodeState),
	}
}

// RegisterIncomingConn: 被连接方（大 ID 端）在 NewService 里调用，
// 把这条被动接受的连接挂到 topology，等待对端首次 ping 携带 routerId 后填回。
func (t *ClusterTopology) RegisterIncomingConn(state *RouterNodeState) {
	t.mu.Lock()
	defer t.mu.Unlock()
	t.nodes[0] = state // routerId 暂未填回，单独索引在 incoming 列表
	appLog.Infof("routerCluster: accepted incoming node conn, remoteAddr=%s, pending ping for routerId", state.Addr())
}

// RegisterByPing: 被连接方在收到对端 ping 时调用，登记 routerId。
// 这条连接可能是：
//   - 我们之前 RegisterIncomingConn 注册的（pending routerId=0）
//   - 或者已经存在的某条连接
func (t *ClusterTopology) RegisterByPing(routerId uint32, addr string) {
	if routerId == 0 {
		return
	}
	t.mu.Lock()
	defer t.mu.Unlock()

	if existing, ok := t.nodes[routerId]; ok {
		if existing.Addr() != addr {
			existing.SetAddr(addr)
		}
		// 把 pending 槽位里 addr 匹配的 state 关联上 routerId
		if pending, ok := t.nodes[0]; ok && pending.Addr() == addr {
			pending.SetRouterId(routerId)
			delete(t.nodes, 0)
			t.nodes[routerId] = pending
		}
		return
	}

	// 没找到任何记录：要么是被连接方首次 ping（pending 已存在但 addr 不匹配）
	// 要么是节点 offline 又重新连上来但本地没有 pending
	if pending, ok := t.nodes[0]; ok && pending.Addr() == addr {
		pending.SetRouterId(routerId)
		delete(t.nodes, 0)
		t.nodes[routerId] = pending
		appLog.Infof("routerCluster: registered incoming routerId=%d via ping, addr=%s", routerId, addr)
		return
	}

	appLog.Warnf("routerCluster: received ping from routerId=%d addr=%s but no matching incoming conn found", routerId, addr)
}

// Get 返回到指定 router 节点的连接状态（用于发起 forwardToGameServer）
func (t *ClusterTopology) Get(routerId uint32) *RouterNodeState {
	t.mu.RLock()
	defer t.mu.RUnlock()
	return t.nodes[routerId]
}

// Reconcile 根据 (myRouterId, 当前已知的全集群 router meta) 调整到其他节点的连接：
//   - 小 ID 端主动 Dial 大 ID 端；
//   - 大 ID 端保留对端连过来的连接，不主动建；
//   - 已不在线（meta 缺失 / lastTick 过老）的节点 → 关闭连接；
//   - 同 routerId 多条连接时只保留最新的。
func (t *ClusterTopology) Reconcile(metas map[uint32]*RouterNodeMeta) {
	t.mu.Lock()
	defer t.mu.Unlock()

	myId := RouterConfig.RouterId
	now := time.Now()

	// 1) 清理过期节点
	for rid, state := range t.nodes {
		if rid == 0 {
			// pending 状态：长时间没收到 ping → 关闭
			continue
		}
		meta, ok := metas[rid]
		if !ok {
			state.Close()
			delete(t.nodes, rid)
			appLog.Infof("routerCluster: closed node conn (meta gone), routerId=%d", rid)
			continue
		}
		if meta.LastTickMs > 0 {
			age := now.UnixMilli() - meta.LastTickMs
			if age > int64(routerMetaStaleTTL/time.Millisecond) {
				state.Close()
				delete(t.nodes, rid)
				appLog.Warnf("routerCluster: closed stale node conn (lastTick=%dms ago), routerId=%d", age, rid)
				continue
			}
		}
		if meta.ClusterAddr != "" && meta.ClusterAddr != state.Addr() {
			state.SetAddr(meta.ClusterAddr)
		}
	}

	// 2) 对所有 meta 中比自己 ID 大的节点，若尚未建连接 → 主动 dial
	for rid, meta := range metas {
		if rid == myId {
			continue
		}
		if rid < myId {
			continue
		}
		if _, exists := t.nodes[rid]; exists {
			continue
		}
		if meta.ClusterAddr == "" {
			continue
		}
		state, err := newRouterNodeStateAsClient(rid, meta.ClusterAddr, t.app)
		if err != nil {
			appLog.Warnf("routerCluster: dial to routerId=%d addr=%s failed: %s", rid, meta.ClusterAddr, err.Error())
			continue
		}
		t.nodes[rid] = state
		appLog.Infof("routerCluster: dialed (small-id side) to routerId=%d addr=%s", rid, meta.ClusterAddr)
	}
}

func (t *ClusterTopology) CloseAll() {
	t.mu.Lock()
	defer t.mu.Unlock()
	for _, state := range t.nodes {
		state.Close()
	}
	t.nodes = make(map[uint32]*RouterNodeState)
}

// PeersToPing: 返回本端作为 small ID 的连接对应的 peer routerId 列表。
// 供 tick 周期主动发 ping 续命使用, 选取规则是 peerId > myId。
func (t *ClusterTopology) PeersToPing(myId uint32) []uint32 {
	t.mu.RLock()
	defer t.mu.RUnlock()
	out := make([]uint32, 0, len(t.nodes))
	for rid := range t.nodes {
		if rid == 0 || rid == myId {
			continue
		}
		if rid > myId {
			out = append(out, rid)
		}
	}
	return out
}

// LookupAddr: routerNodeService 收到断开时尝试反查 routerId
func (t *ClusterTopology) LookupAddr(addr string) uint32 {
	t.mu.RLock()
	defer t.mu.RUnlock()
	for rid, s := range t.nodes {
		if s.Addr() == addr {
			return rid
		}
	}
	return 0
}

// RemoveByAddr: routerNodeService 在 OnLoseConnection 时调用
func (t *ClusterTopology) RemoveByAddr(addr string) {
	t.mu.Lock()
	defer t.mu.Unlock()
	for rid, s := range t.nodes {
		if s.Addr() == addr {
			s.Close()
			delete(t.nodes, rid)
			appLog.Infof("routerCluster: removed node by addr, routerId=%d addr=%s", rid, addr)
			return
		}
	}
}

// MarkBroken: 业务转发写失败时调用，主动摘除该 router 节点连接。
// 调用后 topology 中不再有该 routerId 的 state，下一次 Reconcile 会按 meta 重建。
func (t *ClusterTopology) MarkBroken(routerId uint32) {
	if routerId == 0 {
		return
	}
	t.mu.Lock()
	defer t.mu.Unlock()
	if s, ok := t.nodes[routerId]; ok {
		s.Close()
		delete(t.nodes, routerId)
		appLog.Warnf("routerCluster: marked broken and closed node conn, routerId=%d", routerId)
	}
}

func parseHostPort(addr string) (string, uint16, error) {
	colon := -1
	for i := len(addr) - 1; i >= 0; i-- {
		if addr[i] == ':' {
			colon = i
			break
		}
	}
	if colon < 0 {
		return "", 0, &net.AddrError{Err: "missing port in address", Addr: addr}
	}
	host := addr[:colon]
	portStr := addr[colon+1:]
	port64, err := strconv.ParseUint(portStr, 10, 16)
	if err != nil {
		return "", 0, err
	}
	return host, uint16(port64), nil
}
