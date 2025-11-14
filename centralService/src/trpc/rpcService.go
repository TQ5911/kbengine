package trpc

type methodHandler func(srv IEndPoint, dec func(interface{}) error) (interface{}, error)

type IEndPoint interface {
	GetRpcChannel() *RpcChannel
	SetRpcChannel(channel *RpcChannel)
}

type ClientEndPoint struct {
	Channel *RpcChannel
}

func (self *ClientEndPoint) GetRpcChannel() *RpcChannel {
	return self.Channel
}

func (self *ClientEndPoint) SetRpcChannel(channel *RpcChannel)  {
	self.Channel = channel
}

type MethodDesc struct {
	MethodName string
	MethodIndex int16
	Handler methodHandler
}

// ServiceDesc represents an RPC service's specification.
type ServiceDesc struct {
	ServiceName string

	Methods     []MethodDesc
}

type ServerEndPoint struct {
	ServiceDesc *ServiceDesc
	Client      IEndPoint
}

func (self *ServerEndPoint) GetServiceDesc() *ServiceDesc{
	return self.ServiceDesc
}

func (self *ServerEndPoint) SetClientEndPoint(ep IEndPoint) {
	self.Client = ep
}

func (self *ServerEndPoint) GetClientEndPoint() IEndPoint {
	return self.Client
}

func (self *ServerEndPoint) GetRpcChannel() *RpcChannel{
	return self.Client.GetRpcChannel()
}

func (self *ServerEndPoint) SetRpcChannel(channel *RpcChannel)  {
	self.Client.SetRpcChannel(channel)
}

func (self *ServerEndPoint) Serve(){
	self.GetRpcChannel().Process()
}

type IServerEndPoint interface {
	GetRpcChannel() *RpcChannel
	SetRpcChannel(channel *RpcChannel)

	Serve()
	GetServiceDesc() *ServiceDesc
	OnLoseConnection()
	SetClientEndPoint(IEndPoint)
	GetClientEndPoint() IEndPoint
}

type IChannelService interface {
	OnLoseConnection()
	GetServiceDesc() *ServiceDesc
}