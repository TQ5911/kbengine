using AOT;
namespace KBEngine
{
	using UnityEngine; 
	using System; 
	using System.Collections; 
	using System.Collections.Generic;
	using System.Text;
	using System.Threading;
	using System.Text.RegularExpressions;
	
	using MessageID = System.UInt16;
	using MessageLength = System.UInt16;

    /*
		这是KBEngine插件的核心模块
		包括网络创建、持久化协议、entities的管理、以及引起对外可调用接口。
		
		一些可以参考的地方:
		http://www.kbengine.org/docs/programming/clientsdkprogramming.html
		http://www.kbengine.org/docs/programming/kbe_message_format.html
		
		http://www.kbengine.org/cn/docs/programming/clientsdkprogramming.html
		http://www.kbengine.org/cn/docs/programming/kbe_message_format.html
	*/
    public class KBEngineApp
    {
        public static KBEngineApp app = null;
        private NetworkInterfaceBase _networkInterface = null;

        KBEngineArgs _args = null;

        // 客户端的类别
        // http://www.kbengine.org/docs/programming/clientsdkprogramming.html
        // http://www.kbengine.org/cn/docs/programming/clientsdkprogramming.html
        public enum CLIENT_TYPE
        {
            // Mobile(Phone, Pad)
            CLIENT_TYPE_MOBILE = 1,

            // Windows Application program
            CLIENT_TYPE_WIN = 2,

            // Linux Application program
            CLIENT_TYPE_LINUX = 3,

            // Mac Application program
            CLIENT_TYPE_MAC = 4,

            // Web，HTML5，Flash
            CLIENT_TYPE_BROWSER = 5,

            // bots
            CLIENT_TYPE_BOTS = 6,

            // Mini-Client
            CLIENT_TYPE_MINI = 7,
        };

        //加密通信类型
        public enum NETWORK_ENCRYPT_TYPE
        {
            //无加密
            ENCRYPT_TYPE_NONE = 0,

            //Blowfish
            ENCRYPT_TYPE_BLOWFISH = 1,
        };

        public int accountType = 0;
        public string username = "kbengine";
        public string password = "123456";

        // 服务端分配的baseapp地址
        public string baseappIPv6 = "";
        public string baseappIP = "";
        public UInt16 baseappTcpPortIpv6 = 0;
        public UInt16 baseappUdpPortIpv6 = 0;
        public UInt16 baseappTcpPort = 0;
        public UInt16 baseappUdpPort = 0;

        // 当前状态
        public string currserver = "";
        public string currstate = "";

        // 服务端下行以及客户端上行用于登录时处理的账号绑定的二进制信息
        // 该信息由用户自己进行扩展
        private byte[] _serverdatas = new byte[0];
        private byte[] _clientdatas = new byte[0];

        // 通信协议加密，blowfish协议
        public byte[] _encryptedKey = new byte[0];

        // 服务端与客户端的版本号以及协议MD5
        public string serverVersion = "";
        public string clientVersion = "2.5.8";
        public string serverScriptVersion = "";
        public string clientScriptVersion = "0.1.0";
        public string serverProtocolMD5 = "9506842A6628D1E732A0FAA2B8FC8CB3";
        public string serverEntitydefMD5 = "A14B71B0AF29FECE542C551DE24BE3AD";

        // 当前玩家的实体id与实体类别
        public UInt64 entity_uuid = 0;
        public Int32 entity_id = 0;
        public string entity_type = "";

        private List<Entity> _controlledEntities = new List<Entity>();

        // 当前服务端最后一次同步过来的玩家位置
        private Vector3 _entityServerPos = new Vector3(0f, 0f, 0f);

        // space的数据，具体看API手册关于spaceData
        // https://github.com/kbengine/kbengine/tree/master/docs/api
        private Dictionary<string, string> _spacedatas = new Dictionary<string, string>();

        // 所有实体都保存于这里， 请参看API手册关于entities部分
        // https://github.com/kbengine/kbengine/tree/master/docs/api
        public Dictionary<Int32, Entity> entities = new Dictionary<Int32, Entity>();

        // 在玩家View范围小于256个实体时我们可以通过一字节索引来找到entity
        private List<Int32> _entityIDAliasIDList = new List<Int32>();
        private Dictionary<Int32, MemoryStream> _bufferedCreateEntityMessages = new Dictionary<Int32, MemoryStream>();
        private Dictionary<Int32, List<MemoryStream>> _bufferedCreateEntityMessagesMulti = new Dictionary<Int32, List<MemoryStream>>();

        // 所有服务端错误码对应的错误描述
        private ServerErrorDescrs _serverErrs = new ServerErrorDescrs();

        private System.DateTime _lastTickTime = System.DateTime.Now;
        private System.DateTime _lastTickCBTime = System.DateTime.Now;
        private System.DateTime _lastUpdateToServerTime = System.DateTime.Now;

        //上传玩家信息到服务器间隔，单位毫秒
        private float _updatePlayerToServerPeroid = 100.0f;
        private const int _1MS_TO_100NS = 10000;

        //加密过滤器
        private EncryptionFilter _filter = null;

        // 玩家当前所在空间的id， 以及空间对应的资源
        public UInt32 spaceID = 0;
        public string spaceResPath = "";
        public bool isLoadedGeometry = false;

        // 按照标准，每个客户端部分都应该包含这个属性
        public const string component = "client";

        public bool helloDone = false;
        public bool isReconnecting = false;
        public bool _disableUpdatePos = false;
        public bool enableBufferMultiMsgs = true;

        public KBEngineApp(KBEngineArgs args)
        {
            if (app != null)
                throw new Exception("Only one instance of KBEngineApp!");

            app = this;
            Event.outEventsImmediately = !args.isMultiThreads;

            initialize(args);
        }

        public static KBEngineApp getSingleton()
        {
            if (KBEngineApp.app == null)
            {
                throw new Exception("Please create KBEngineApp!");
            }

            return KBEngineApp.app;
        }

        public virtual bool initialize(KBEngineArgs args)
        {
            _args = args;
            _updatePlayerToServerPeroid = (float)_args.syncPlayerMS;

            EntityDef.init();

            // LuaTable kbengineLua = XLuaManager.Instance.GetLuaTable("KBEngine/generated/KBEngineLua");
            // kbengineLua.Get("serverEntitydefMD5", out serverEntitydefMD5);
            // kbengineLua.Get("serverProtocolMD5", out serverProtocolMD5);

            initNetwork();

            // 注册事件
            installEvents();

            return true;
        }

        void initNetwork()
        {
            _filter = null;
            Messages.init();
            _networkInterface = new NetworkInterfaceTCP();
        }

        void installEvents()
        {
            Event.registerIn(EventInTypes.createAccount, this, "createAccount");
            Event.registerIn(EventInTypes.login, this, "login");
            Event.registerIn(EventInTypes.logout, this, "logout");
            Event.registerIn(EventInTypes.reloginBaseapp, this, "reloginBaseapp");
            Event.registerIn(EventInTypes.resetPassword, this, "resetPassword");
            Event.registerIn(EventInTypes.bindAccountEmail, this, "bindAccountEmail");
            Event.registerIn(EventInTypes.newPassword, this, "newPassword");

            // 内部事件
            Event.registerIn("_closeNetwork", this, "_closeNetwork");
            //EventMgr.Instance.RegistListener(EventDef.EVENT_KBE_CREATEACCOUNT, CreateAccount);
        }

        public KBEngineArgs getInitArgs()
        {
            return _args;
        }

        public virtual void destroy()
        {
            Dbg.WARNING_MSG("KBEngine::destroy()");

            //EventMgr.Instance.UnRegistListener(EventDef.EVENT_KBE_CREATEACCOUNT, CreateAccount);

            if (currserver == "baseapp")
                logout();

            reset();
            KBEngine.Event.deregisterIn(this);
            resetMessages();

            KBEngineApp.app = null;
        }

        public void CreateAccount(params object[] pSender)
        {
            string username = pSender[0].ToString();
            string password = pSender[1].ToString();
            byte[] datas = System.Text.Encoding.UTF8.GetBytes(pSender[2].ToString());
            createAccount(username, password, datas);
        }

        public NetworkInterfaceBase networkInterface()
        {
            return _networkInterface;
        }

        public byte[] serverdatas()
        {
            return _serverdatas;
        }

        public void entityServerPos(Vector3 pos)
        {
            _entityServerPos = pos;
        }

        public Vector3 getEntityServerPos()
        {
            return _entityServerPos;
        }

        public void resetMessages()
        {
            _serverErrs.Clear();
            Messages.clear();
            EntityDef.reset();

            Entity.clear();
            Dbg.DEBUG_MSG("KBEngine::resetMessages()");
        }

        public virtual void reset()
        {
            KBEngine.Event.clearFiredEvents();

            clearEntities(true);

            currserver = "";
            currstate = "";
            _serverdatas = new byte[0];
            serverVersion = "";
            serverScriptVersion = "";

            entity_uuid = 0;
            entity_id = 0;
            entity_type = "";

            _entityIDAliasIDList.Clear();
            _bufferedCreateEntityMessages.Clear();

            _lastTickTime = System.DateTime.Now;
            _lastTickCBTime = System.DateTime.Now;
            _lastUpdateToServerTime = System.DateTime.Now;

            spaceID = 0;
            spaceResPath = "";
            isLoadedGeometry = false;

            if (_networkInterface != null)
                _networkInterface.reset();

            _filter = null;
            _encryptedKey = new byte[0];
            _networkInterface = new NetworkInterfaceTCP();

            _spacedatas.Clear();
            helloDone = false;
            isReconnecting = false;

        }

        public static bool validEmail(string strEmail)
        {
            return Regex.IsMatch(strEmail, @"^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)
				|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$");
        }

        /*
			插件的主循环处理函数
		*/
        public virtual void process()
        {
            //先判断是否断线了，如果切后台回来已经断线那就没必要处理缓冲区里已经收到的数据了
            //那些数据已经没意义了
            checkHeartBeatTimeout();
            // 处理网络
            if (_networkInterface != null)
                _networkInterface.process();

            // 处理外层抛入的事件
            Event.processInEvents();

            // 向服务端发送心跳以及同步角色信息到服务端
            sendTick();
        }

        /*
			当前玩家entity
		*/
        public Entity player()
        {
            Entity e;
            if (entities.TryGetValue(entity_id, out e))
                return e;

            return null;
        }

        public Entity getEntity(int eid)
        {
            Entity e;
            if (entities.TryGetValue(eid, out e))
                return e;

            return null;
        }

        public void dealBufferedEntityMsgs(Int32 eid)
        {
            if (enableBufferMultiMsgs)
            {
                List<MemoryStream> entityMessageList = null;
                if (_bufferedCreateEntityMessagesMulti.TryGetValue(eid, out entityMessageList))
                {
                    for (int i = 0; i < entityMessageList.Count; i++)
                    {
                        Client_onUpdatePropertys(entityMessageList[i]);
                    }

                    _bufferedCreateEntityMessagesMulti.Remove(eid);

                    for (int i = 0; i < entityMessageList.Count; i++)
                    {
                        entityMessageList[i].reclaimObject();
                    }
                }
            }
            else
            {
                MemoryStream entityMessage = null;
                _bufferedCreateEntityMessages.TryGetValue(eid, out entityMessage);

                if (entityMessage != null)
                {
                    Client_onUpdatePropertys(entityMessage);
                    _bufferedCreateEntityMessages.Remove(eid);
                    entityMessage.reclaimObject();
                }
            }
        }

        public bool checkAliasListValid(List<Int32> aliasList)
        {
            if (aliasList.Count != _entityIDAliasIDList.Count)
            {
                Dbg.ERROR_MSG("checkAliasListValid: aliasList.Count != _entityIDAliasIDList.Count" + " aliasList.Count=" + aliasList.Count + " _entityIDAliasIDList.Count=" + _entityIDAliasIDList.Count);
                return false;
            }

            for (int i = 0; i < aliasList.Count; i++)
            {
                if (aliasList[i] != _entityIDAliasIDList[i])
                {
                    Dbg.ERROR_MSG("checkAliasListValid: aliasList[" + i + "] != _entityIDAliasIDList[" + i + "]" + " aliasList[" + i + "]=" + aliasList[i] + " _entityIDAliasIDList[" + i + "]=" + _entityIDAliasIDList[i]);
                    return false;
                }
            }

            Dbg.DEBUG_MSG("checkAliasListValid: aliasList valid!");
            return true;
        }

        public void disconnect()
        {
            _networkInterface.close();
        }

        public void _closeNetwork(NetworkInterfaceBase networkInterface)
        {
            networkInterface.close();
        }

        public bool checkHeartBeatTimeout()
        {
            if (_networkInterface == null || _networkInterface.connected == false)
                return true;
            TimeSpan span = DateTime.Now - _lastTickTime;
            //超过30认为掉线了，小于0认为往回调设备时间，也按照断线处理，断线重连后会重新跟服务器校时
            if (span.TotalSeconds >= 30 || span.TotalSeconds < 0)
            {
                Dbg.ERROR_MSG("sendTick: Receive appTick timeout!");
                _networkInterface.close();
                return true;
            }
            return false;
        }

        /*
			向服务端发送心跳以及同步角色信息到服务端
		*/
        public void sendTick()
        {
            if (checkHeartBeatTimeout())
                return;

            TimeSpan span = DateTime.Now - _lastTickTime;

            // 更新玩家的位置与朝向到服务端
            updatePlayerToServer();

            if (helloDone && _args.serverHeartbeatTick > 0 && span.TotalSeconds > _args.serverHeartbeatTick)
            {
                span = _lastTickCBTime - _lastTickTime;

                // 如果心跳回调接收时间小于心跳发送时间，说明没有收到回调
                // 此时应该通知客户端掉线了
                if (span.TotalSeconds < 0)
                {
                    Dbg.ERROR_MSG("sendTick: Receive appTick timeout!");
                    _networkInterface.close();
                    return;
                }

                Message Loginapp_onClientActiveTickMsg = null;
                Message Baseapp_onClientActiveTickMsg = null;

                Messages.messages.TryGetValue("Loginapp_onClientActiveTick", out Loginapp_onClientActiveTickMsg);
                Messages.messages.TryGetValue("Baseapp_onClientActiveTick", out Baseapp_onClientActiveTickMsg);

                if (currserver == "loginapp")
                {
                    if (Loginapp_onClientActiveTickMsg != null)
                    {
                        Bundle bundle = Bundle.createObject();
                        bundle.newMessage(Messages.messages["Loginapp_onClientActiveTick"]);
                        bundle.send(_networkInterface);
                    }
                }
                else
                {
                    if (Baseapp_onClientActiveTickMsg != null)
                    {
                        Bundle bundle = Bundle.createObject();
                        bundle.newMessage(Messages.messages["Baseapp_onClientActiveTick"]);
                        bundle.send(_networkInterface);
                    }
                }

                _lastTickTime = System.DateTime.Now;
            }
        }

        /*
			服务器心跳回调
		*/
        public void Client_onAppActiveTickCB()
        {
            _lastTickCBTime = System.DateTime.Now;

            TimeSpan span = _lastTickCBTime - _lastTickTime;
            EventMgr.Instance.SendEvent(EventDef.EVENT_NET_DELAY, (int)span.TotalMilliseconds);
        }

        /*
			与服务端握手，与任何一个进程连接之后应该第一时间进行握手
		*/
        public void hello()
        {
            if (_args.networkEncryptType == NETWORK_ENCRYPT_TYPE.ENCRYPT_TYPE_BLOWFISH)
            {
                _filter = new BlowfishFilter();
                _encryptedKey = ((BlowfishFilter)_filter).key();
            }
            helloDone = false;
            Bundle bundle = Bundle.createObject();
            if (currserver == "loginapp")
                bundle.newMessage(Messages.messages["Loginapp_hello"]);
            else
                bundle.newMessage(Messages.messages["Baseapp_hello"]);

            bundle.writeString(clientVersion);
            bundle.writeString(clientScriptVersion);
            bundle.writeBlob(_encryptedKey);
            bundle.send(_networkInterface, checkHello: false);

            if (_filter != null)
            {
                _networkInterface.setFilter(_filter);
                _filter = null;
            }
        }

        /*
			握手之后服务端的回调
		*/
        public void Client_onHelloCB(MemoryStream stream)
        {
            helloDone = true;
            String curServerVersion = stream.readString();
            String curServerScriptVersion = stream.readString();
            String curServerProtocolMD5 = stream.readString();
            String curServerEntitydefMD5 = stream.readString();
            Int32 ctype = stream.readInt32();
            Int64 now = stream.readInt64();

            Dbg.DEBUG_MSG("KBEngine::Client_onHelloCB: verInfo(" + curServerVersion
                + "), scriptVersion(" + curServerScriptVersion + "), srvProtocolMD5(" + curServerProtocolMD5
                + "), srvEntitydefMD5(" + curServerEntitydefMD5 + "), + ctype(" + ctype + ")!");

            if (curServerVersion != "Getting")
            {
                serverVersion = curServerVersion;

                /* 
				if(serverProtocolMD5 != currentServerProtocolMD5)
				{
					Dbg.ERROR_MSG("Client_onHelloCB: digest not match! serverProtocolMD5=" + serverProtocolMD5 + "(server: " + currentServerProtocolMD5 + ")");
					Event.fireAll(EventOutTypes.onVersionNotMatch, clientVersion, serverVersion);
					return;
				}
				*/

                if (serverEntitydefMD5 != curServerEntitydefMD5)
                {
                    Dbg.ERROR_MSG("Client_onHelloCB: SCRIPT digest not match! serverEntitydefMD5=" + serverEntitydefMD5 + "(server: " + curServerEntitydefMD5 + ")");
                    Event.fireAll(EventOutTypes.onVersionNotMatch, clientVersion, serverVersion);
                    EventMgr.Instance.SendEvent(EventDef.EVENT_KBE_SCRIPT_VERSION_NOT_MATCH, clientVersion, serverVersion, clientScriptVersion, curServerScriptVersion, serverEntitydefMD5, curServerEntitydefMD5);
                    return;
                }
                /*if (serverProtocolMD5 != curServerProtocolMD5)
                {
                    Dbg.ERROR_MSG("Client_onHelloCB: ENGINE digest not match! serverProtocolMD5=" + serverProtocolMD5 + "(server: " + curServerProtocolMD5 + ")");
                    Event.fireAll(EventOutTypes.onVersionNotMatch, clientVersion, serverVersion);
                    EventMgr.Instance.SendEvent(EventDef.EVENT_KBE_SCRIPT_VERSION_NOT_MATCH, clientVersion, serverVersion, clientScriptVersion, curServerScriptVersion, serverProtocolMD5, curServerProtocolMD5);
                    return;
                }*/
            }

            onServerDigest();

            if (currserver == "baseapp")
            {
                KBEngineTime.SetDeltaTime(now);
                onLogin_baseapp();
            }
            else
            {
                onLogin_loginapp();
            }
        }

        /*
			服务端错误描述导入了
		*/
        public void Client_onImportServerErrorsDescr(MemoryStream stream)
        {
            // 无需实现，已由插件生成静态代码
        }

        /*
			从服务端返回的二进制流导入客户端消息协议
		*/
        public void Client_onImportClientMessages(MemoryStream stream)
        {
            // 无需实现，已由插件生成静态代码
        }

        /*
			从服务端返回的二进制流导入客户端消息协议
		*/
        public void Client_onImportClientEntityDef(MemoryStream stream)
        {
            // 无需实现，已由插件生成静态代码
        }

        public void Client_onImportClientSDK(MemoryStream stream)
        {
            int remainingFiles = 0;
            remainingFiles = stream.readInt32();

            string fileName;
            fileName = stream.readString();

            int fileSize = 0;
            fileSize = stream.readInt32();

            byte[] fileDatas = new byte[0];
            fileDatas = stream.readBlob();

            Event.fireIn("onImportClientSDK", remainingFiles, fileName, fileSize, fileDatas);
        }

        /*
			引擎版本不匹配
		*/
        public void Client_onVersionNotMatch(MemoryStream stream)
        {
            serverVersion = stream.readString();

            Dbg.ERROR_MSG("Client_onVersionNotMatch: verInfo=" + clientVersion + "(server: " + serverVersion + ")");
            //Event.fireAll(EventOutTypes.onVersionNotMatch, clientVersion, serverVersion);
            //EventMgr.Instance.SendEvent(EventDef.EVENT_KBE_VERSION_NOT_MATCH, clientVersion, serverVersion);
        }

        /*
			脚本版本不匹配
		*/
        public void Client_onScriptVersionNotMatch(MemoryStream stream)
        {
            serverScriptVersion = stream.readString();

            Dbg.ERROR_MSG("Client_onScriptVersionNotMatch: verInfo=" + clientScriptVersion + "(server: " + serverScriptVersion + ")");
            //Event.fireAll(EventOutTypes.onScriptVersionNotMatch, clientScriptVersion, serverScriptVersion);
            EventMgr.Instance.SendEvent(EventDef.EVENT_KBE_SCRIPT_VERSION_NOT_MATCH, clientScriptVersion, clientScriptVersion);
        }

        /*
			被服务端踢出
		*/
        public void Client_onKicked(UInt16 failedcode)
        {
            Dbg.DEBUG_MSG("Client_onKicked: failedcode=" + failedcode + "(" + serverErr(failedcode) + ")");
            Event.fireAll(EventOutTypes.onKicked, failedcode);
            EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_KICKED, failedcode);
        }

        /*
			登录到服务端，必须登录完成loginapp与网关(baseapp)，登录流程才算完毕
		*/
        public void login(int accountType, string username, string password, byte[] datas)
        {
            KBEngineApp.app.accountType = accountType;
            KBEngineApp.app.username = username;
            KBEngineApp.app.password = password;
            KBEngineApp.app._clientdatas = datas;

            KBEngineApp.app.login_loginapp(true);
            EventMgr.Instance.SendEvent(EventDef.EVENT_NET_CONNECTION);
        }

        /*
			登录到服务端(loginapp), 登录成功后还必须登录到网关(baseapp)登录流程才算完毕
		*/
        public void login_loginapp(bool noconnect)
        {
            if (noconnect)
            {
                reset();
                _networkInterface.connectTo(_args.ip, _args.port, onConnectTo_loginapp_callback, null);
            }
            else
            {
                Dbg.DEBUG_MSG("KBEngine::login_loginapp(): send login! username=" + username);
                Bundle bundle = Bundle.createObject();
                bundle.newMessage(Messages.messages["Loginapp_login"]);
                bundle.writeInt8((sbyte)_args.clientType);
                bundle.writeBlob(KBEngineApp.app._clientdatas);
                bundle.writeString(getRealAccountName());
                bundle.writeString(password);
                bundle.writeString(serverEntitydefMD5);
                bundle.send(_networkInterface);
            }
        }

        private void onConnectTo_loginapp_callback(string ip, int port, bool success, object userData)
        {
            _lastTickCBTime = System.DateTime.Now;

            if (!success)
            {
                Dbg.ERROR_MSG(string.Format("KBEngine::login_loginapp(): connect {0}:{1} error!", ip, port));
                return;
            }

            currserver = "loginapp";
            currstate = "login";

            Dbg.DEBUG_MSG(string.Format("KBEngine::login_loginapp(): connect {0}:{1} success!", ip, port));

            PlayerPrefs.SetString("IPAddress", ip);

            hello();
        }

        private void onLogin_loginapp()
        {
            _lastTickCBTime = System.DateTime.Now;
            login_loginapp(false);
        }

        /*
			登录到服务端，登录到网关(baseapp)
		*/
        public void login_baseapp(bool noconnect)
        {
            isReconnecting = false;
            Dbg.DEBUG_MSG(string.Format("KBEngine::login_baseapp(): connect {0}", noconnect));

            if (noconnect)
            {
                //Event.fireOut(EventOutTypes.onLoginBaseapp);
                //EventMgr.Instance.SendEvent(EventDef.EVENT_KBE_ON_LOGIN_BASEAPP);

                _networkInterface.reset();
                clearSpace(false);

                if (_args.forceDisableUDP || baseappUdpPort == 0)
                {
                    _networkInterface = new NetworkInterfaceTCP();
#if UNITY_IOS && !UNITY_EDITOR
 					//baseapp没有外网ipv6
 					if (VersionUtils.IsInAudit())
                     {
 						//为了应对ios审核，这里只能写死域名
 						baseappIP = "shenhe-baseapp.yunxingu.com";
                     }
#endif
                    _networkInterface.connectTo(baseappIP, baseappTcpPort, onConnectTo_baseapp_callback, null);
                }
                else
                {
                    _networkInterface = new NetworkInterfaceKCP();
#if UNITY_IOS && !UNITY_EDITOR
                     if (VersionUtils.IsInAudit())
                     {
 						//为了应对ios审核，这里只能写死域名
 						baseappIP = "shenhe-baseapp.yunxingu.com";
 					}
#endif
                    _networkInterface.connectTo(baseappIP, baseappUdpPort, onConnectTo_baseapp_callback, null);
                }
            }
            else
            {
                Bundle bundle = Bundle.createObject();
                bundle.newMessage(Messages.messages["Baseapp_loginBaseapp"]);
                bundle.writeString(getRealAccountName());
                bundle.writeString(password);
                bundle.send(_networkInterface);
            }
        }

        private void onConnectTo_baseapp_callback(string ip, int port, bool success, object userData)
        {
            _lastTickCBTime = System.DateTime.Now;

            if (!success)
            {
                Dbg.ERROR_MSG(string.Format("KBEngine::onConnectTo_baseapp_callback(): connect {0}:{1} error!", ip, port));
                return;
            }

            currserver = "baseapp";
            currstate = "";

            Dbg.DEBUG_MSG(string.Format("KBEngine::onConnectTo_baseapp_callback(): connect {0}:{1} success!", ip, port));

            hello();
        }

        private void onLogin_baseapp()
        {
            _lastTickCBTime = System.DateTime.Now;
            login_baseapp(false);
        }

        /*
			重登录到网关(baseapp)
			一些移动类应用容易掉线，可以使用该功能快速的重新与服务端建立通信
		*/
        public void reloginBaseapp()
        {
            _lastTickTime = System.DateTime.Now;
            _lastTickCBTime = System.DateTime.Now;

            if (_networkInterface.valid())
                return;

            Event.fireAll(EventOutTypes.onReloginBaseapp);

            _networkInterface.reset();
            clearSpace(false);
            helloDone = false;

            if (_args.forceDisableUDP || baseappUdpPort == 0)
            {
                _networkInterface = new NetworkInterfaceTCP();
                if (NetworkInterfaceBase.IsIpv6OnlyEnv())
                {
                    _networkInterface.connectTo(baseappIPv6, baseappTcpPortIpv6, onReConnectTo_baseapp_callback, null);
                }
                else
                {
                    _networkInterface.connectTo(baseappIP, baseappTcpPort, onReConnectTo_baseapp_callback, null);
                }
            }
            else
            {
                _networkInterface = new NetworkInterfaceKCP();
                if (NetworkInterfaceBase.IsIpv6OnlyEnv())
                {
                    _networkInterface.connectTo(baseappIPv6, baseappUdpPortIpv6, onReConnectTo_baseapp_callback, null);
                }
                else
                {
                    _networkInterface.connectTo(baseappIP, baseappUdpPort, onReConnectTo_baseapp_callback, null);
                }
            }
        }

        private void onReConnectTo_baseapp_callback(string ip, int port, bool success, object userData)
        {
            if (!success)
            {
                Dbg.ERROR_MSG(string.Format("KBEngine::reloginBaseapp(): connect {0}:{1} error!", ip, port));
                return;
            }

            Dbg.DEBUG_MSG(string.Format("KBEngine::relogin_baseapp(): connect {0}:{1} success!", ip, port));
            helloDone = false;
            isReconnecting = true;
            Bundle bundle = Bundle.createObject();
            bundle.newMessage(Messages.messages["Baseapp_tryReloginBaseapp"]);
            bundle.writeString(username);
            bundle.writeString(password);
            bundle.writeUint64(entity_uuid);
            bundle.writeInt32(entity_id);
            bundle.send(_networkInterface, checkHello: false);

            _lastTickCBTime = System.DateTime.Now;
        }

        /*
			登出baseapp
		*/
        public void logout()
        {
            Bundle bundle = Bundle.createObject();
            bundle.newMessage(Messages.messages["Baseapp_logoutBaseapp"]);
            bundle.writeUint64(entity_uuid);
            bundle.writeInt32(entity_id);
            bundle.send(_networkInterface);
        }

        /*
			通过错误id得到错误描述
		*/
        public string serverErr(UInt16 id)
        {
            return _serverErrs.serverErrStr(id);
        }

        public void onOpenLoginapp_resetpassword()
        {
            Dbg.DEBUG_MSG("KBEngine::onOpenLoginapp_resetpassword: successfully!");
            currserver = "loginapp";
            currstate = "resetpassword";
            _lastTickCBTime = System.DateTime.Now;

            resetpassword_loginapp(false);
        }

        /*
			重置密码, 通过loginapp
		*/
        public void resetPassword(string username)
        {
            KBEngineApp.app.username = username;
            resetpassword_loginapp(true);
        }

        /*
			重置密码, 通过loginapp
		*/
        public void resetpassword_loginapp(bool noconnect)
        {
            if (noconnect)
            {
                reset();
                _networkInterface.connectTo(_args.ip, _args.port, onConnectTo_resetpassword_callback, null);
            }
            else
            {
                Bundle bundle = Bundle.createObject();
                bundle.newMessage(Messages.messages["Loginapp_reqAccountResetPassword"]);
                bundle.writeString(username);
                bundle.send(_networkInterface);
            }
        }

        private void onConnectTo_resetpassword_callback(string ip, int port, bool success, object userData)
        {
            _lastTickCBTime = System.DateTime.Now;

            if (!success)
            {
                Dbg.ERROR_MSG(string.Format("KBEngine::resetpassword_loginapp(): connect {0}:{1} error!", ip, port));
                return;
            }

            Dbg.DEBUG_MSG(string.Format("KBEngine::resetpassword_loginapp(): connect {0}:{1} success!", ip, port));
            onOpenLoginapp_resetpassword();
        }

        public void Client_onReqAccountResetPasswordCB(UInt16 failcode)
        {
            if (failcode != 0)
            {
                Dbg.ERROR_MSG("KBEngine::Client_onReqAccountResetPasswordCB: " + username + " failed! code=" + failcode + "(" + serverErr(failcode) + ")!");
                return;
            }

            Dbg.DEBUG_MSG("KBEngine::Client_onReqAccountResetPasswordCB: " + username + " success!");
        }

        /*
			绑定Email，通过baseapp
		*/
        public void bindAccountEmail(string emailAddress)
        {
            Bundle bundle = Bundle.createObject();
            bundle.newMessage(Messages.messages["Baseapp_reqAccountBindEmail"]);
            bundle.writeInt32(entity_id);
            bundle.writeString(password);
            bundle.writeString(emailAddress);
            bundle.send(_networkInterface);
        }

        public void Client_onReqAccountBindEmailCB(UInt16 failcode)
        {
            if (failcode != 0)
            {
                Dbg.ERROR_MSG("KBEngine::Client_onReqAccountBindEmailCB: " + username + " failed! code=" + failcode + "(" + serverErr(failcode) + ")!");
                return;
            }

            Dbg.DEBUG_MSG("KBEngine::Client_onReqAccountBindEmailCB: " + username + " success!");
        }

        /*
			设置新密码，通过baseapp， 必须玩家登录在线操作所以是baseapp。
		*/
        public void newPassword(string old_password, string new_password)
        {
            Bundle bundle = Bundle.createObject();
            bundle.newMessage(Messages.messages["Baseapp_reqAccountNewPassword"]);
            bundle.writeInt32(entity_id);
            bundle.writeString(old_password);
            bundle.writeString(new_password);
            bundle.send(_networkInterface);
        }

        public void Client_onReqAccountNewPasswordCB(UInt16 failcode)
        {
            if (failcode != 0)
            {
                Dbg.ERROR_MSG("KBEngine::Client_onReqAccountNewPasswordCB: " + username + " failed! code=" + failcode + "(" + serverErr(failcode) + ")!");
                return;
            }

            Dbg.DEBUG_MSG("KBEngine::Client_onReqAccountNewPasswordCB: " + username + " success!");
        }

        public void createAccount(string username, string password, byte[] datas)
        {
            KBEngineApp.app.username = username;
            KBEngineApp.app.password = password;
            KBEngineApp.app._clientdatas = datas;

            KBEngineApp.app.createAccount_loginapp(true);
        }

        /*
			创建账号，通过loginapp
		*/
        public void createAccount_loginapp(bool noconnect)
        {
            if (noconnect)
            {
                reset();
                _networkInterface.connectTo(_args.ip, _args.port, onConnectTo_createAccount_callback, null);
            }
            else
            {
                Bundle bundle = Bundle.createObject();
                bundle.newMessage(Messages.messages["Loginapp_reqCreateAccount"]);
                bundle.writeString(username);
                bundle.writeString(password);
                bundle.writeBlob(KBEngineApp.app._clientdatas);
                bundle.send(_networkInterface);
            }
        }

        public void onOpenLoginapp_createAccount()
        {
            Dbg.DEBUG_MSG("KBEngine::onOpenLoginapp_createAccount: successfully!");
            currserver = "loginapp";
            currstate = "createAccount";
            _lastTickCBTime = System.DateTime.Now;

            createAccount_loginapp(false);
        }

        private void onConnectTo_createAccount_callback(string ip, int port, bool success, object userData)
        {
            _lastTickCBTime = System.DateTime.Now;

            if (!success)
            {
                Dbg.ERROR_MSG(string.Format("KBEngine::createAccount_loginapp(): connect {0}:{1} error!", ip, port));
                return;
            }

            Dbg.DEBUG_MSG(string.Format("KBEngine::createAccount_loginapp(): connect {0}:{1} success!", ip, port));
            onOpenLoginapp_createAccount();
        }

        /*
			获得了服务端摘要信息， 摘要包括协议MD5， entitydefMD5
		*/
        public void onServerDigest()
        {
        }

        /*
			登录loginapp失败了
		*/
        public void Client_onLoginFailed(MemoryStream stream)
        {
            UInt16 failedcode = stream.readUint16();
            _serverdatas = stream.readBlob();
            //Dbg.ERROR_MSG("KBEngine::Client_onLoginFailed: failedcode(" + failedcode + ":" + serverErr(failedcode) + "), datas(" + _serverdatas.Length + ")!");
            //Event.fireAll(EventOutTypes.onLoginFailed, failedcode, _serverdatas);
            EventMgr.Instance.SendEvent(EventDef.EVENT_KBE_ONLOGIN_FAILED, failedcode, System.Text.Encoding.UTF8.GetString(_serverdatas));

            string reason = serverErr(failedcode);
            Dbg.DEBUG_MSG("KBEngine::Client_onLoginFailed: failedcode(" + failedcode + "), reason: " + reason + " datas(" + _serverdatas.Length + ")!");
        }

        private String getRealAccountName()
        {
            return accountType + ":" + username;
        }

        /*
			登录loginapp成功了
		*/
        public void Client_onLoginSuccessfully(MemoryStream stream)
        {
            var accountName = stream.readString();
            string[] parts = accountName.Split(':');
            if (parts.Length > 1)
            {
                accountType = int.Parse(parts[0]);
                username = parts[1];
            }
            else
            {
                accountType = 1;
                username = accountName;
            }

            baseappIPv6 = stream.readString();
            baseappIP = stream.readString();
            baseappTcpPortIpv6 = stream.readUint16();
            baseappUdpPortIpv6 = stream.readUint16();
            baseappTcpPort = stream.readUint16();
            baseappUdpPort = stream.readUint16();
            _serverdatas = stream.readBlob();

            PlayerPrefs.SetString(AccountCache.Account, username);
            PlayerPrefs.SetString(AccountCache.Password, password);

            Dbg.DEBUG_MSG("KBEngine::Client_onLoginSuccessfully: accountName(" + accountName + "), addr(" + baseappIPv6 + ":" + baseappTcpPortIpv6 + "|" + baseappUdpPortIpv6 + ";" +
                    baseappIP + ":" + baseappTcpPort + "|" + baseappUdpPort + "), datas(" + _serverdatas.Length + ")!");

            login_baseapp(true);
        }

        /*
			登录baseapp失败了
		*/
        public void Client_onLoginBaseappFailed(UInt16 failedcode)
        {
            Dbg.ERROR_MSG("KBEngine::Client_onLoginBaseappFailed: failedcode=" + failedcode + "(" + serverErr(failedcode) + ")!");
            //Event.fireAll(EventOutTypes.onLoginBaseappFailed, failedcode);
            EventMgr.Instance.SendEvent(EventDef.EVENT_KBE_LOGIN_BASEAPP_FAILED, failedcode);
        }

        /*
			重登录baseapp失败了
		*/
        public void Client_onReloginBaseappFailed(UInt16 failedcode)
        {
            isReconnecting = false;
            Dbg.ERROR_MSG("KBEngine::Client_onReloginBaseappFailed: failedcode=" + failedcode + "(" + serverErr(failedcode) + ")!");
            //Event.fireAll(EventOutTypes.onReloginBaseappFailed, failedcode);
            EventMgr.Instance.SendEvent(EventDef.EVENT_NET_RECONNECTED_FAILED, failedcode);
        }

        /*
			登录baseapp成功了
		*/
        public void Client_onReloginBaseappSuccessfully(MemoryStream stream)
        {
            helloDone = true;
            if (_args.networkEncryptType == NETWORK_ENCRYPT_TYPE.ENCRYPT_TYPE_BLOWFISH)
            {
                _filter = new BlowfishFilter(_encryptedKey);
                _networkInterface.setFilter(_filter);
                _filter = null;
            }

            Bundle bundle = Bundle.createObject();
            bundle.newMessage(Messages.messages["Baseapp_doReloginBaseapp"]);
            bundle.send(_networkInterface);

            entity_uuid = stream.readUint64();
            Dbg.DEBUG_MSG("KBEngine::Client_onReloginBaseappSuccessfully: name(" + username + ")!");
            //Event.fireAll(EventOutTypes.onReloginBaseappSuccessfully);

        }

        /*
			服务端通知创建一个角色
		*/
        public void Client_onCreatedProxies(UInt64 rndUUID, Int32 eid, string entityType)
        {
            if (isReconnecting)
            {
                isReconnecting = false;
                EventMgr.Instance.SendEvent(EventDef.EVENT_NET_RECONNECTED_SUCCESS);
            }

            Dbg.DEBUG_MSG("KBEngine::Client_onCreatedProxies: eid(" + eid + "), entityType(" + entityType + ")!");

            entity_uuid = rndUUID;
            entity_id = eid;
            entity_type = entityType;

            if (!this.entities.ContainsKey(eid))
            {
                ScriptModule module = null;
                if (!EntityDef.moduledefs.TryGetValue(entityType, out module))
                {
                    Dbg.ERROR_MSG("KBEngine::Client_onCreatedProxies: not found module(" + entityType + ")!");
                    return;
                }

                Type runclass = module.entityScript;
                if (runclass == null)
                    runclass = typeof(KBEngine.EntityCommon);

                Entity entity = (Entity)Activator.CreateInstance(runclass);
                entity.id = eid;
                entity.className = entityType;
                entity.onGetBase();

                entities[eid] = entity;

                // entity.initLuaEnt();

                dealBufferedEntityMsgs(eid);

                entity.__init__();
                entity.attachComponents();
                entity.inited = true;

                if (_args.isOnInitCallPropertysSetMethods)
                    entity.callPropertysSetMethods();
            }
            else
            {
                dealBufferedEntityMsgs(eid);
            }
        }

        public Entity findEntity(Int32 entityID)
        {
            Entity entity = null;

            if (!entities.TryGetValue(entityID, out entity))
            {
                return null;
            }

            return entity;
        }

        /*
			通过流数据获得View实体的ID
		*/
        public Int32 getViewEntityIDFromStream(MemoryStream stream)
        {
            if (!_args.useAliasEntityID)
                return stream.readInt32();

            Int32 id = 0;
            if (_entityIDAliasIDList.Count > 255)
            {
                id = stream.readInt32();
            }
            else
            {
                byte aliasID = stream.readUint8();

                // 如果为0且客户端上一步是重登陆或者重连操作并且服务端entity在断线期间一直处于在线状态
                // 则可以忽略这个错误, 因为cellapp可能一直在向baseapp发送同步消息， 当客户端重连上时未等
                // 服务端初始化步骤开始则收到同步信息, 此时这里就会出错。
                if (_entityIDAliasIDList.Count <= aliasID)
                    return 0;

                id = _entityIDAliasIDList[aliasID];
            }

            return id;
        }

        /*
			服务端使用优化的方式更新实体属性数据
		*/
        public void Client_onUpdatePropertysOptimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);
            onUpdatePropertys_(eid, stream);
        }

        /*
			服务端更新实体属性数据
		*/
        public void Client_onUpdatePropertys(MemoryStream stream)
        {
            Int32 eid = stream.readInt32();
            onUpdatePropertys_(eid, stream);
        }

        public void onUpdatePropertys_(Int32 eid, MemoryStream stream)
        {
            Entity entity = null;

            if (!entities.TryGetValue(eid, out entity))
            {
                if (enableBufferMultiMsgs)
                {
                    List<MemoryStream> entityMessageList = null;
                    if (!_bufferedCreateEntityMessagesMulti.TryGetValue(eid, out entityMessageList))
                    {
                        _bufferedCreateEntityMessagesMulti[eid] = new List<MemoryStream>();
                    }
                }
                else
                {
                    MemoryStream entityMessage = null;
                    if (_bufferedCreateEntityMessages.TryGetValue(eid, out entityMessage))
                    {
                        Dbg.ERROR_MSG("KBEngine::Client_onUpdatePropertys: entity(" + eid + ") not found!");
                        return;
                    }
                }

                MemoryStream stream1 = MemoryStream.createObject();
                stream1.wpos = stream.wpos;
                stream1.rpos = stream.rpos - 4;
                Array.Copy(stream.data(), stream1.data(), stream.wpos);
                if (enableBufferMultiMsgs)
                    _bufferedCreateEntityMessagesMulti[eid].Add(stream1);
                else
                    _bufferedCreateEntityMessages[eid] = stream1;
                return;
            }

            entity.onUpdatePropertys(stream);
        }

        /*
			服务端使用优化的方式调用实体方法
		*/
        public void Client_onRemoteMethodCallOptimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);
            onRemoteMethodCall_(eid, stream);
        }

        /*
			服务端调用实体方法
		*/
        public void Client_onRemoteMethodCall(MemoryStream stream)
        {
            Int32 eid = stream.readInt32();
            onRemoteMethodCall_(eid, stream);
        }

        public void onRemoteMethodCall_(Int32 eid, MemoryStream stream)
        {
            Entity entity = null;

            if (!entities.TryGetValue(eid, out entity))
            {
                Dbg.ERROR_MSG("KBEngine::Client_onRemoteMethodCall: entity(" + eid + ") not found!");
                return;
            }

            entity.onRemoteMethodCall(stream);
        }

        /*
			服务端通知一个实体进入了世界(如果实体是当前玩家则玩家第一次在一个space中创建了， 如果是其他实体则是其他实体进入了玩家的View)
		*/
        public void Client_onEntityEnterWorld(MemoryStream stream)
        {
            Int32 eid = stream.readInt32();
            if (entity_id > 0 && entity_id != eid)
            {
                if (_entityIDAliasIDList.Contains(eid))
                {
                    Dbg.DEBUG_MSG("KBEngine::Client_onEntityEnterWorld: entity(" + eid + ") already exists!");
                    return;
                }
                _entityIDAliasIDList.Add(eid);
            }

            UInt16 uentityType;
            if (EntityDef.idmoduledefs.Count > 255)
                uentityType = stream.readUint16();
            else
                uentityType = stream.readUint8();

            sbyte isOnGround = 1;

            if (stream.length() > 0)
                isOnGround = stream.readInt8();

            string entityType = EntityDef.idmoduledefs[uentityType].name;
            // Dbg.DEBUG_MSG("KBEngine::Client_onEntityEnterWorld: " + entityType + "(" + eid + "), spaceID(" + KBEngineApp.app.spaceID + ")!");

            Entity entity = null;

            if (!entities.TryGetValue(eid, out entity))
            {
                if (enableBufferMultiMsgs)
                {
                    List<MemoryStream> entityMessageList = null;
                    if (!_bufferedCreateEntityMessagesMulti.TryGetValue(eid, out entityMessageList))
                    {
                        Dbg.ERROR_MSG("KBEngine::Client_onEntityEnterWorld: entity(" + eid + ") not found!");
                        return;
                    }
                }
                else
                {
                    MemoryStream entityMessage = null;
                    if (!_bufferedCreateEntityMessages.TryGetValue(eid, out entityMessage))
                    {
                        Dbg.ERROR_MSG("KBEngine::Client_onEntityEnterWorld: entity(" + eid + ") not found!");
                        return;
                    }
                }
                ScriptModule module = null;
                if (!EntityDef.moduledefs.TryGetValue(entityType, out module))
                {
                    Dbg.ERROR_MSG("KBEngine::Client_onEntityEnterWorld: not found module(" + entityType + ")!");
                }

                Type runclass = module.entityScript;
                if (runclass == null)
                    runclass = typeof(KBEngine.EntityCommon);

                entity = (Entity)Activator.CreateInstance(runclass);
                entity.id = eid;
                entity.className = entityType;
                entity.onGetCell();

                entities[eid] = entity;
                // entity.initLuaEnt();

                dealBufferedEntityMsgs(eid);

                entity.isOnGround = isOnGround > 0;
                //entity.onDirectionChanged(entity.direction);
                //entity.onPositionChanged(entity.position);

                entity.__init__();
                entity.attachComponents();
                entity.inited = true;
                entity.inWorld = true;
                entity.enterWorld();

                if (_args.isOnInitCallPropertysSetMethods)
                    entity.callPropertysSetMethods();
            }
            else
            {
                if (!entity.inWorld)
                {
                    // 安全起见， 这里清空一下
                    // 如果服务端上使用giveClientTo切换控制权
                    // 之前的实体已经进入世界， 切换后的实体也进入世界， 这里可能会残留之前那个实体进入世界的信息
                    _entityIDAliasIDList.Clear();
                    clearEntities(false);
                    entities[entity.id] = entity;

                    entity.onGetCell();

                    //entity.onDirectionChanged(entity.direction);
                    //entity.onPositionChanged(entity.position);				

                    _entityServerPos = entity.position;
                    entity.isOnGround = isOnGround > 0;
                    entity.inWorld = true;
                    entity.enterWorld();

                    if (_args.isOnInitCallPropertysSetMethods)
                        entity.callPropertysSetMethods();
                }
            }
        }

        /*
			服务端使用优化的方式通知一个实体离开了世界(如果实体是当前玩家则玩家离开了space， 如果是其他实体则是其他实体离开了玩家的View)
		*/
        public void Client_onEntityLeaveWorldOptimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);
            KBEngineApp.app.Client_onEntityLeaveWorld(eid);
        }

        /*
			服务端通知一个实体离开了世界(如果实体是当前玩家则玩家离开了space， 如果是其他实体则是其他实体离开了玩家的View)
		*/
        public void Client_onEntityLeaveWorld(Int32 eid)
        {
            Entity entity = null;

            if (!entities.TryGetValue(eid, out entity))
            {
                Dbg.WARNING_MSG("KBEngine::Client_onEntityLeaveWorld: entity(" + eid + ") not found!");
                return;
            }

            if (entity.inWorld)
                entity.leaveWorld();

            if (entity_id == eid)
            {
                clearSpace(false);
                entity.onLoseCell();
            }
            else
            {
                if (_controlledEntities.Remove(entity))
                    Event.fireOut(EventOutTypes.onLoseControlledEntity, entity);

                entities.Remove(eid);
                entity.destroy();
                _entityIDAliasIDList.Remove(eid);
            }
        }

        /*
			服务端通知当前玩家进入了一个新的space
		*/
        public void Client_onEntityEnterSpace(MemoryStream stream)
        {
            Int32 eid = stream.readInt32();
            spaceID = stream.readUint32();

            sbyte isOnGround = 1;

            if (stream.length() > 0)
                isOnGround = stream.readInt8();

            Entity entity = null;

            if (!entities.TryGetValue(eid, out entity))
            {
                Dbg.ERROR_MSG("KBEngine::Client_onEntityEnterSpace: entity(" + eid + ") not found!");
                return;
            }

            entity.isOnGround = isOnGround > 0;
            _entityServerPos = entity.position;
            entity.enterSpace();
        }

        /*
			服务端通知当前玩家离开了space
		*/
        public void Client_onEntityLeaveSpace(Int32 eid)
        {
            Entity entity = null;

            if (!entities.TryGetValue(eid, out entity))
            {
                Dbg.ERROR_MSG("KBEngine::Client_onEntityLeaveSpace: entity(" + eid + ") not found!");
                return;
            }

            entity.leaveSpace();
            clearSpace(false);
        }

        /*
			账号创建返回结果
		*/
        public void Client_onCreateAccountResult(MemoryStream stream)
        {
            UInt16 retcode = stream.readUint16();
            byte[] datas = stream.readBlob();

            //Event.fireOut(EventOutTypes.onCreateAccountResult, retcode, datas);
            //EventMgr.Instance.SendEvent(EventDef.EVENT_KBE_CREATEACCOUNT_RESULT, retcode, datas);

            if (retcode != 0)
            {
                Dbg.WARNING_MSG("KBEngine::Client_onCreateAccountResult: " + username + " create is failed! code=" + retcode + "(" + serverErr(retcode) + ")!");
                return;
            }

            Dbg.DEBUG_MSG("KBEngine::Client_onCreateAccountResult: " + username + " create is successfully!");
        }

        /*
			告诉客户端：你当前负责（或取消）控制谁的位移同步
		*/
        public void Client_onControlEntity(Int32 eid, sbyte isControlled)
        {
            Entity entity = null;

            if (!entities.TryGetValue(eid, out entity))
            {
                Dbg.ERROR_MSG("KBEngine::Client_onControlEntity: entity(" + eid + ") not found!");
                return;
            }

            var isCont = isControlled != 0;
            if (isCont)
            {
                // 如果被控制者是玩家自己，那表示玩家自己被其它人控制了
                // 所以玩家自己不应该进入这个被控制列表
                if (player().id != entity.id)
                {
                    _controlledEntities.Add(entity);
                }
            }
            else
            {
                _controlledEntities.Remove(entity);
            }

            entity.isControlled = isCont;

            try
            {
                entity.onControlled(isCont);
                Event.fireOut(EventOutTypes.onControlled, entity, isCont);
            }
            catch (Exception e)
            {
                Dbg.ERROR_MSG(string.Format("KBEngine::Client_onControlEntity: entity id = '{0}', is controlled = '{1}', error = '{1}'", eid, isCont, e));
            }
        }

        public void enableUpdatePlayer()
        {
            _disableUpdatePos = false;
        }

        public void disableUpdatePlayer()
        {
            _disableUpdatePos = true;
        }

        private float m_lastUpdateToServerFixedTime = 0;
        /*
			更新当前玩家的位置与朝向到服务端， 可以通过开关_syncPlayerMS关闭这个机制
		*/
        public void updatePlayerToServer(bool isForce = false)
        {
            if (_updatePlayerToServerPeroid <= 0.01f || spaceID == 0)
            {
                return;
            }

            //var now = DateTime.Now;
            //TimeSpan span = now - _lastUpdateToServerTime;



            m_lastUpdateToServerFixedTime += Time.fixedDeltaTime;

            if (!isForce && m_lastUpdateToServerFixedTime < 0.09f /*span.Ticks < _updatePlayerToServerPeroid * _1MS_TO_100NS*/)
            {
                return;
            }

            Entity playerEntity = player();
            if (playerEntity == null 
                || playerEntity.inWorld == false 
                || !KBEngineApp.app.helloDone)
            {
                return;
            }
            if (MyUtils.IsClassType(playerEntity.classType, ClassType.Avatar))
            {
                Avatar avatar = (Avatar)playerEntity;
                if (avatar.IsObPlayer()
                    || avatar.isControlled
                    || avatar.HasState((int)CHARACTER_STATE.CS_SERVER_CONTROL))
                {
                    return;
                }
            }

            if (!isForce)
            {
                if (playerEntity.ServerSetPosition || playerEntity.isShifting)
                {
                    return;
                }

                if (playerEntity.hasView && playerEntity.view is ViewControl viewAvatar)
                {
                    if (!viewAvatar.IsClientControlledTransform())
                    {
                        return;
                    }
                }
            }

            //_lastUpdateToServerTime = now; // - (span - TimeSpan.FromTicks(Convert.ToInt64(_updatePlayerToServerPeroid * _1MS_TO_100NS)));



            Vector3 position = playerEntity.position;
            Vector3 direction = playerEntity.direction;
            bool isOnGround = playerEntity.isOnGround;

            bool posHasChanged = Vector3.Distance(playerEntity._entityLastLocalPos, position) > 0.001f;
            bool dirHasChanged = Vector3.Distance(playerEntity._entityLastLocalDir, direction) > 0.001f;
            bool isOnGroundChanged = playerEntity._entityLastLocalIsOnGround != isOnGround;

            if (posHasChanged || dirHasChanged || isOnGroundChanged)
            {
                //GLog.LogError($"KBEngine::updatePlayerToServer: {playerEntity._entityLastLocalPos}=>{position} dir={Vector3.Distance(playerEntity._entityLastLocalPos, position)} {span.TotalSeconds}");

                playerEntity._entityLastLocalPos = position;
                playerEntity._entityLastLocalDir = direction;
                playerEntity._entityLastLocalIsOnGround = isOnGround;
                //disable期间客户端服务器各自移动，但需要保持终点一致
                //disable期间_entityLastLocalPos仍然修改，所以即使重新enable后也不会把终点同步过去
                if (!_disableUpdatePos)
                {
                    m_lastUpdateToServerFixedTime = 0;

                    Bundle bundle = Bundle.createObject();
                    bundle.newMessage(Messages.messages["Baseapp_onUpdateDataFromClient"]);
                    bundle.writeFloat(position.x);
                    bundle.writeFloat(position.y);
                    bundle.writeFloat(position.z);

                    double x = ((double)direction.x / 360 * (System.Math.PI * 2));
                    double y = ((double)direction.y / 360 * (System.Math.PI * 2));
                    double z = ((double)direction.z / 360 * (System.Math.PI * 2));

                    // 根据弧度转角度公式会出现负数
                    // unity会自动转化到0~360度之间，这里需要做一个还原
                    if (x - System.Math.PI > 0.0)
                        x -= System.Math.PI * 2;

                    if (y - System.Math.PI > 0.0)
                        y -= System.Math.PI * 2;

                    if (z - System.Math.PI > 0.0)
                        z -= System.Math.PI * 2;

                    bundle.writeFloat((float)x);
                    bundle.writeFloat((float)y);
                    bundle.writeFloat((float)z);
                    bundle.writeUint8((Byte)(playerEntity.isOnGround == true ? 1 : 0));
                    bundle.writeUint32(spaceID);
                    bundle.send(_networkInterface);
                }
            }

            /*
            // 开始同步所有被控制了的entity的位置
            if (!_disableUpdatePos)
            {
                for (int i = 0; i < _controlledEntities.Count; ++i)
                {
                    var entity = _controlledEntities[i];
                    position = entity.position;
                    direction = entity.direction;
                    isOnGround = entity.isOnGround;

                    posHasChanged = Vector3.Distance(entity._entityLastLocalPos, position) > 0.001f;
                    dirHasChanged = Vector3.Distance(entity._entityLastLocalDir, direction) > 0.001f;
                    isOnGroundChanged = entity._entityLastLocalIsOnGround != isOnGround;

                    if (posHasChanged || dirHasChanged || isOnGroundChanged)
                    {
                        entity._entityLastLocalPos = position;
                        entity._entityLastLocalDir = direction;
                        entity._entityLastLocalIsOnGround = isOnGround;

                        Bundle bundle = Bundle.createObject();
                        bundle.newMessage(Messages.messages["Baseapp_onUpdateDataFromClientForControlledEntity"]);
                        bundle.writeInt32(entity.id);
                        bundle.writeFloat(position.x);
                        bundle.writeFloat(position.y);
                        bundle.writeFloat(position.z);

                        double x = ((double)direction.x / 360 * (System.Math.PI * 2));
                        double y = ((double)direction.y / 360 * (System.Math.PI * 2));
                        double z = ((double)direction.z / 360 * (System.Math.PI * 2));

                        // 根据弧度转角度公式会出现负数
                        // unity会自动转化到0~360度之间，这里需要做一个还原
                        if (x - System.Math.PI > 0.0)
                            x -= System.Math.PI * 2;

                        if (y - System.Math.PI > 0.0)
                            y -= System.Math.PI * 2;

                        if (z - System.Math.PI > 0.0)
                            z -= System.Math.PI * 2;

                        bundle.writeFloat((float)x);
                        bundle.writeFloat((float)y);
                        bundle.writeFloat((float)z);
                        bundle.writeUint8((Byte)(entity.isOnGround == true ? 1 : 0));
                        bundle.writeUint32(spaceID);
                        bundle.send(_networkInterface);
                    }
                }
            }
			*/
        }

        /*
			当前space添加了关于几何等信息的映射资源
			客户端可以通过这个资源信息来加载对应的场景
		*/
        public void addSpaceGeometryMapping(UInt32 uspaceID, string respath)
        {
            Dbg.DEBUG_MSG("KBEngine::addSpaceGeometryMapping: spaceID(" + uspaceID + "), respath(" + respath + ")!");

            isLoadedGeometry = true;
            spaceID = uspaceID;
            spaceResPath = respath;
            Event.fireOut(EventOutTypes.addSpaceGeometryMapping, spaceResPath);
        }

        public void clearSpace(bool isall)
        {
            _entityIDAliasIDList.Clear();
            _spacedatas.Clear();
            clearEntities(isall);
            isLoadedGeometry = false;
            spaceID = 0;
        }

        public void clearEntities(bool isall)
        {
            _controlledEntities.Clear();

            if (!isall)
            {
                Entity entity = player();

                foreach (KeyValuePair<Int32, Entity> dic in entities)
                {
                    if (entity != null && dic.Key == entity.id)
                        continue;

                    if (dic.Value.inWorld)
                        dic.Value.leaveWorld();

                    dic.Value.destroy();
                }

                entities.Clear();
                if (entity != null)
                    entities[entity.id] = entity;
            }
            else
            {
                foreach (KeyValuePair<Int32, Entity> dic in entities)
                {
                    if (dic.Value.inWorld)
                        dic.Value.leaveWorld();

                    dic.Value.destroy();
                }

                entities.Clear();
            }
        }

        /*
			服务端初始化客户端的spacedata， spacedata请参考API
		*/
        public void Client_initSpaceData(MemoryStream stream)
        {
            /*
				在onEntityLeaveSpace，onEntityLeaveWorld和onEntityDestroyed的時候都已经调用过，这里不用重复调用了，
				不然会导致客户端实体创建好了又删除重新创建一次
			*/
            //clearSpace(false);
            spaceID = stream.readUint32();

            while (stream.length() > 0)
            {
                string key = stream.readString();
                string val = stream.readString();
                Client_setSpaceData(spaceID, key, val);
            }

            Dbg.DEBUG_MSG("KBEngine::Client_initSpaceData: spaceID(" + spaceID + "), size(" + _spacedatas.Count + ")!");
        }

        /*
			服务端设置客户端的spacedata， spacedata请参考API
		*/
        public void Client_setSpaceData(UInt32 spaceID, string key, string value)
        {
            Dbg.DEBUG_MSG("KBEngine::Client_setSpaceData: spaceID(" + spaceID + "), key(" + key + "), value(" + value + ")!");
            _spacedatas[key] = value;

            if (key == "_mapping")
                addSpaceGeometryMapping(spaceID, value);

            Event.fireOut(EventOutTypes.onSetSpaceData, spaceID, key, value);
        }

        /*
			服务端删除客户端的spacedata， spacedata请参考API
		*/
        public void Client_delSpaceData(UInt32 spaceID, string key)
        {
            Dbg.DEBUG_MSG("KBEngine::Client_delSpaceData: spaceID(" + spaceID + "), key(" + key + ")");
            _spacedatas.Remove(key);
            Event.fireOut(EventOutTypes.onDelSpaceData, spaceID, key);
        }

        public string getSpaceData(string key)
        {
            string val = "";

            if (!_spacedatas.TryGetValue(key, out val))
            {
                return "";
            }

            return val;
        }

        /*
			服务端通知强制销毁一个实体
		*/
        public void Client_onEntityDestroyed(Int32 eid)
        {
            Dbg.DEBUG_MSG("KBEngine::Client_onEntityDestroyed: entity(" + eid + ")");

            Entity entity = null;

            if (!entities.TryGetValue(eid, out entity))
            {
                Dbg.ERROR_MSG("KBEngine::Client_onEntityDestroyed: entity(" + eid + ") not found!");
                return;
            }

            if (entity.inWorld)
            {
                if (entity_id == eid)
                    clearSpace(false);

                entity.leaveWorld();
            }

            if (_controlledEntities.Remove(entity))
                Event.fireOut(EventOutTypes.onLoseControlledEntity, entity);

            entities.Remove(eid);
            entity.destroy();
        }

        /*
			服务端更新玩家的基础位置， 客户端以这个基础位置加上便宜值计算出玩家周围实体的坐标
            只是更新基础位置，玩家位置不需要变化，这个主要用于客户端在控制玩家，服务器基础位置变化后同步给客户端
            因为是客户端控制位置，所以这个时候不需要设置玩家位置，服务器控制将通过onUpdatePlayerPos同步
		*/
        public void Client_onUpdateBasePos(float x, float y, float z)
        {
            _entityServerPos.x = x;
            _entityServerPos.y = y;
            _entityServerPos.z = z;

            Entity entity = player();
            if (entity == null)
            {
                return;
            }
            if (MyUtils.IsClassType(entity.classType, ClassType.Avatar))
            {
                Avatar avatar = (Avatar)entity;
                if (!avatar.isControlled && !avatar.HasState((int)CHARACTER_STATE.CS_SERVER_CONTROL) && !avatar.IsObPlayer())
                {
                    return;
                }
            }
            else if (MyUtils.IsClassType(entity.classType, ClassType.Avataring))
            {
                return;
            }

            entity.position.Set(_entityServerPos.x, _entityServerPos.y, _entityServerPos.z);
            Event.fireOut(EventOutTypes.updatePosition, entity);
            entity.onSetPosition();
            entity.onUpdateVolatileData();
        }

        public void Client_onUpdateBasePosXZ(float x, float z)
        {
            _entityServerPos.x = x;
            _entityServerPos.z = z;

            Entity entity = player();
            if (entity == null)
            {
                return;
            }
            if (MyUtils.IsClassType(entity.classType, ClassType.Avatar))
            {
                Avatar avatar = (Avatar)entity;
                if (!avatar.isControlled && !avatar.HasState((int)CHARACTER_STATE.CS_SERVER_CONTROL) && !avatar.IsObPlayer())
                {
                    return;
                }
            }
            else if (MyUtils.IsClassType(entity.classType, ClassType.Avataring))
            {
                return;
            }

            entity.position.x = _entityServerPos.x;
            entity.position.z = _entityServerPos.z;
            Event.fireOut(EventOutTypes.updatePosition, entity);
            entity.onSetPosition();
            entity.onUpdateVolatileData();
        }

        /*
           服务器控制玩家移动，需要平滑，无条件接受
           因为位置是服务器在控制，所以同时需要更新基础位置
        */
        public void Client_onUpdatePlayerPos(MemoryStream ms)
        {
            Vector3 xyz = ms.readPackXYZ();
            float x = _entityServerPos.x + xyz.x;
            float y = _entityServerPos.y + xyz.y;
            float z = _entityServerPos.z + xyz.z;

            var entity = player();
            if (entity != null)
            {
                entity.position.Set(x, y, z);
                Event.fireOut(EventOutTypes.updatePosition, entity);
                entity.onSetPosition();
                entity.onUpdateVolatileData();
            }

            _entityServerPos.x = x;
            _entityServerPos.y = y;
            _entityServerPos.z = z;
        }

        public void Client_onUpdatePlayerXZ(MemoryStream ms)
        {
            Vector2 xz = ms.readPackXZ();
            float x = _entityServerPos.x + xz.x;
            float z = _entityServerPos.z + xz.y;

            var entity = player();
            if (entity != null)
            {
                entity.position.x = x;
                entity.position.z = z;
                Event.fireOut(EventOutTypes.updatePosition, entity);
                entity.onSetPosition();
                entity.onUpdateVolatileData();
            }

            _entityServerPos.x = x;
            _entityServerPos.z = z;
        }

        public void Client_onUpdatePlayerXZ_y(MemoryStream ms)
        {
            Vector2 xz = ms.readPackXZ();
            float x = _entityServerPos.x + xz.x;
            float z = _entityServerPos.z + xz.y;
            float yawRad = ms.readFloat();

            var entity = player();
            if (entity != null)
            {
                entity.position.x = x;
                entity.position.z = z;
                float yaw = yawRad * 360 / ((float)System.Math.PI * 2);
                entity.direction.Set(entity.direction.x, entity.direction.y, yaw);
                Event.fireOut(EventOutTypes.updatePosition, entity);
                entity.onSetPosition();
                entity.onSetDirection();
                entity.onUpdateVolatileData();
            }
            _entityServerPos.x = x;
            _entityServerPos.z = z;
        }

        public void Client_onUpdatePlayerPos_y(MemoryStream ms)
        {
            Vector3 xyz = ms.readPackXYZ();
            float x = _entityServerPos.x + xyz.x;
            float y = _entityServerPos.y + xyz.y;
            float z = _entityServerPos.z + xyz.z;
            float yawRad = ms.readFloat();

            var entity = player();
            if (entity != null)
            {
                entity.position.Set(x, y, z);
                float yaw = yawRad * 360 / ((float)System.Math.PI * 2);
                entity.direction.Set(entity.direction.x, entity.direction.y, yaw);
                Event.fireOut(EventOutTypes.updatePosition, entity);
                entity.onSetPosition();
                entity.onSetDirection();
                entity.onUpdateVolatileData();
            }

            _entityServerPos.x = x;
            _entityServerPos.y = y;
            _entityServerPos.z = z;
        }

        public void Client_onUpdateBaseDir(MemoryStream stream)
        {
            float yaw, pitch, roll;
            yaw = stream.readFloat() * 360 / ((float)System.Math.PI * 2);
            pitch = stream.readFloat() * 360 / ((float)System.Math.PI * 2);
            roll = stream.readFloat() * 360 / ((float)System.Math.PI * 2);

            var entity = player();
            if (entity != null && entity.isControlled)
            {
                entity.direction.Set(roll, pitch, yaw);
                Event.fireOut(EventOutTypes.set_direction, entity);
                entity.onSetDirection();
                entity.onUpdateVolatileData();
            }
        }

        public void Client_onUpdateData(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);
            Entity entity = null;

            if (!entities.TryGetValue(eid, out entity))
            {
                Dbg.ERROR_MSG("KBEngine::Client_onUpdateData: entity(" + eid + ") not found!");
                return;
            }
        }

        /*
			服务端强制设置了玩家的坐标 
			例如：在服务端使用avatar.position=(0,0,0), 或者玩家位置与速度异常时会强制拉回到一个位置
		*/
        public void Client_onSetEntityPosAndDir(MemoryStream stream)
        {
            Int32 eid = stream.readInt32();
            Entity entity = null;

            if (!entities.TryGetValue(eid, out entity))
            {
                Dbg.ERROR_MSG("KBEngine::Client_onSetEntityPosAndDir: entity(" + eid + ") not found!");
                return;
            }

            Vector3 old_position = new Vector3(entity.position.x, entity.position.y, entity.position.z);
            Vector3 old_direction = new Vector3(entity.direction.x, entity.direction.y, entity.direction.z);

            entity.position.x = stream.readFloat();
            entity.position.y = stream.readFloat();
            entity.position.z = stream.readFloat();

            if (eid == entity_id)
                _entityServerPos.Set(entity.position.x, entity.position.y, entity.position.z);

            entity.direction.x = stream.readFloat();
            entity.direction.y = stream.readFloat();
            entity.direction.z = stream.readFloat();

            entity.onDirectionChanged(old_direction);
            entity.onPositionChanged(old_position);

            entity._entityLastLocalPos = entity.position;
            entity._entityLastLocalDir = entity.direction;
            entity._entityLastLocalIsOnGround = entity.isOnGround;
        }

        public void Client_onUpdateData_ypr(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float y = stream.readFloat();
            float p = stream.readFloat();
            float r = stream.readFloat();

            _updateVolatileData(eid, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, y, p, r, -1, false);
        }

        public void Client_onUpdateData_yp(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float y = stream.readFloat();
            float p = stream.readFloat();

            _updateVolatileData(eid, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, y, p, KBEMath.KBE_FLT_MAX, -1, false);
        }

        public void Client_onUpdateData_yr(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float y = stream.readFloat();
            float r = stream.readFloat();

            _updateVolatileData(eid, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, y, KBEMath.KBE_FLT_MAX, r, -1, false);
        }

        public void Client_onUpdateData_pr(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float p = stream.readFloat();
            float r = stream.readFloat();

            _updateVolatileData(eid, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, p, r, -1, false);
        }

        public void Client_onUpdateData_y(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float y = stream.readFloat();

            _updateVolatileData(eid, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, y, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, -1, false);
        }

        public void Client_onUpdateData_p(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float p = stream.readFloat();

            _updateVolatileData(eid, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, p, KBEMath.KBE_FLT_MAX, -1, false);
        }

        public void Client_onUpdateData_r(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float r = stream.readFloat();

            _updateVolatileData(eid, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, r, -1, false);
        }

        public void Client_onUpdateData_xz(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float x = stream.readFloat();
            float z = stream.readFloat();

            _updateVolatileData(eid, x, KBEMath.KBE_FLT_MAX, z, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, 1, false);
        }

        public void Client_onUpdateData_xz_ypr(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float x = stream.readFloat();
            float z = stream.readFloat();

            float y = stream.readFloat();
            float p = stream.readFloat();
            float r = stream.readFloat();

            _updateVolatileData(eid, x, KBEMath.KBE_FLT_MAX, z, y, p, r, 1, false);
        }

        public void Client_onUpdateData_xz_yp(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float x = stream.readFloat();
            float z = stream.readFloat();

            float y = stream.readFloat();
            float p = stream.readFloat();

            _updateVolatileData(eid, x, KBEMath.KBE_FLT_MAX, z, y, p, KBEMath.KBE_FLT_MAX, 1, false);
        }

        public void Client_onUpdateData_xz_yr(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float x = stream.readFloat();
            float z = stream.readFloat();

            float y = stream.readFloat();
            float r = stream.readFloat();

            _updateVolatileData(eid, x, KBEMath.KBE_FLT_MAX, z, y, KBEMath.KBE_FLT_MAX, r, 1, false);
        }

        public void Client_onUpdateData_xz_pr(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float x = stream.readFloat();
            float z = stream.readFloat();

            float p = stream.readFloat();
            float r = stream.readFloat();

            _updateVolatileData(eid, x, KBEMath.KBE_FLT_MAX, z, KBEMath.KBE_FLT_MAX, p, r, 1, false);
        }

        public void Client_onUpdateData_xz_y(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float x = stream.readFloat();
            float z = stream.readFloat();

            float yaw = stream.readFloat();

            _updateVolatileData(eid, x, KBEMath.KBE_FLT_MAX, z, yaw, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, 1, false);
        }

        public void Client_onUpdateData_xz_p(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float x = stream.readFloat();
            float z = stream.readFloat();

            float p = stream.readFloat();

            _updateVolatileData(eid, x, KBEMath.KBE_FLT_MAX, z, KBEMath.KBE_FLT_MAX, p, KBEMath.KBE_FLT_MAX, 1, false);
        }

        public void Client_onUpdateData_xz_r(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float x = stream.readFloat();
            float z = stream.readFloat();

            float r = stream.readFloat();

            _updateVolatileData(eid, x, KBEMath.KBE_FLT_MAX, z, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, r, 1, false);
        }

        public void Client_onUpdateData_xyz(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float x = stream.readFloat();
            float y = stream.readFloat();
            float z = stream.readFloat();

            _updateVolatileData(eid, x, y, z, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, 0, false);
        }

        public void Client_onUpdateData_xyz_ypr(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float x = stream.readFloat();
            float y = stream.readFloat();
            float z = stream.readFloat();

            float yaw = stream.readFloat();
            float p = stream.readFloat();
            float r = stream.readFloat();

            _updateVolatileData(eid, x, y, z, yaw, p, r, 0, false);
        }

        public void Client_onUpdateData_xyz_yp(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float x = stream.readFloat();
            float y = stream.readFloat();
            float z = stream.readFloat();

            float yaw = stream.readFloat();
            float p = stream.readFloat();

            _updateVolatileData(eid, x, y, z, yaw, p, KBEMath.KBE_FLT_MAX, 0, false);
        }

        public void Client_onUpdateData_xyz_yr(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float x = stream.readFloat();
            float y = stream.readFloat();
            float z = stream.readFloat();

            float yaw = stream.readFloat();
            float r = stream.readFloat();

            _updateVolatileData(eid, x, y, z, yaw, KBEMath.KBE_FLT_MAX, r, 0, false);
        }

        public void Client_onUpdateData_xyz_pr(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float x = stream.readFloat();
            float y = stream.readFloat();
            float z = stream.readFloat();

            float p = stream.readFloat();
            float r = stream.readFloat();

            _updateVolatileData(eid, x, y, z, KBEMath.KBE_FLT_MAX, p, r, 0, false);
        }

        public void Client_onUpdateData_xyz_y(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float x = stream.readFloat();
            float y = stream.readFloat();
            float z = stream.readFloat();

            float yaw = stream.readFloat();

            _updateVolatileData(eid, x, y, z, yaw, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, 0, false);
        }

        public void Client_onUpdateData_xyz_p(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float x = stream.readFloat();
            float y = stream.readFloat();
            float z = stream.readFloat();

            float p = stream.readFloat();

            _updateVolatileData(eid, x, y, z, KBEMath.KBE_FLT_MAX, p, KBEMath.KBE_FLT_MAX, 0, false);
        }

        public void Client_onUpdateData_xyz_r(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            float x = stream.readFloat();
            float y = stream.readFloat();
            float z = stream.readFloat();

            float r = stream.readFloat();

            _updateVolatileData(eid, x, y, z, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, r, 0, false);
        }

        public void Client_onUpdateData_ypr_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            SByte y = stream.readInt8();
            SByte p = stream.readInt8();
            SByte r = stream.readInt8();

            _updateVolatileData(eid, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, y, p, r, -1, true);
        }

        public void Client_onUpdateData_yp_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            SByte y = stream.readInt8();
            SByte p = stream.readInt8();

            _updateVolatileData(eid, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, y, p, KBEMath.KBE_FLT_MAX, -1, true);
        }

        public void Client_onUpdateData_yr_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            SByte y = stream.readInt8();
            SByte r = stream.readInt8();

            _updateVolatileData(eid, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, y, KBEMath.KBE_FLT_MAX, r, -1, true);
        }

        public void Client_onUpdateData_pr_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            SByte p = stream.readInt8();
            SByte r = stream.readInt8();

            _updateVolatileData(eid, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, p, r, -1, true);
        }

        public void Client_onUpdateData_y_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            SByte y = stream.readInt8();

            _updateVolatileData(eid, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, y, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, -1, true);
        }

        public void Client_onUpdateData_p_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            SByte p = stream.readInt8();

            _updateVolatileData(eid, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, p, KBEMath.KBE_FLT_MAX, -1, true);
        }

        public void Client_onUpdateData_r_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            SByte r = stream.readInt8();

            _updateVolatileData(eid, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, r, -1, true);
        }

        public void Client_onUpdateData_xz_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            Vector2 xz = stream.readPackXZ();

            _updateVolatileData(eid, xz[0], KBEMath.KBE_FLT_MAX, xz[1], KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, 1, true);
        }

        public void Client_onUpdateData_xz_ypr_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            Vector2 xz = stream.readPackXZ();

            SByte y = stream.readInt8();
            SByte p = stream.readInt8();
            SByte r = stream.readInt8();

            _updateVolatileData(eid, xz[0], KBEMath.KBE_FLT_MAX, xz[1], y, p, r, 1, true);
        }

        public void Client_onUpdateData_xz_yp_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            Vector2 xz = stream.readPackXZ();

            SByte y = stream.readInt8();
            SByte p = stream.readInt8();

            _updateVolatileData(eid, xz[0], KBEMath.KBE_FLT_MAX, xz[1], y, p, KBEMath.KBE_FLT_MAX, 1, true);
        }

        public void Client_onUpdateData_xz_yr_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            Vector2 xz = stream.readPackXZ();

            SByte y = stream.readInt8();
            SByte r = stream.readInt8();

            _updateVolatileData(eid, xz[0], KBEMath.KBE_FLT_MAX, xz[1], y, KBEMath.KBE_FLT_MAX, r, 1, true);
        }

        public void Client_onUpdateData_xz_pr_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            Vector2 xz = stream.readPackXZ();

            SByte p = stream.readInt8();
            SByte r = stream.readInt8();

            _updateVolatileData(eid, xz[0], KBEMath.KBE_FLT_MAX, xz[1], KBEMath.KBE_FLT_MAX, p, r, 1, true);
        }

        public void Client_onUpdateData_xz_y_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);
            Vector2 xz = stream.readPackXZ();
            SByte yaw = stream.readInt8();
            _updateVolatileData(eid, xz[0], KBEMath.KBE_FLT_MAX, xz[1], yaw, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, 1, true);
        }

        public void Client_onUpdateData_xz_p_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            Vector2 xz = stream.readPackXZ();

            SByte p = stream.readInt8();

            _updateVolatileData(eid, xz[0], KBEMath.KBE_FLT_MAX, xz[1], KBEMath.KBE_FLT_MAX, p, KBEMath.KBE_FLT_MAX, 1, true);
        }

        public void Client_onUpdateData_xz_r_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            Vector2 xz = stream.readPackXZ();

            SByte r = stream.readInt8();

            _updateVolatileData(eid, xz[0], KBEMath.KBE_FLT_MAX, xz[1], KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, r, 1, true);
        }

        public void Client_onUpdateData_xyz_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            Vector2 xz = stream.readPackXZ();
            float y = stream.readPackY();

            _updateVolatileData(eid, xz[0], y, xz[1], KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, 0, true);
        }

        public void Client_onUpdateData_xyz_ypr_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            Vector2 xz = stream.readPackXZ();
            float y = stream.readPackY();

            SByte yaw = stream.readInt8();
            SByte p = stream.readInt8();
            SByte r = stream.readInt8();

            _updateVolatileData(eid, xz[0], y, xz[1], yaw, p, r, 0, true);
        }

        public void Client_onUpdateData_xyz_yp_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            Vector2 xz = stream.readPackXZ();
            float y = stream.readPackY();

            SByte yaw = stream.readInt8();
            SByte p = stream.readInt8();

            _updateVolatileData(eid, xz[0], y, xz[1], yaw, p, KBEMath.KBE_FLT_MAX, 0, true);
        }

        public void Client_onUpdateData_xyz_yr_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            Vector2 xz = stream.readPackXZ();
            float y = stream.readPackY();

            SByte yaw = stream.readInt8();
            SByte r = stream.readInt8();

            _updateVolatileData(eid, xz[0], y, xz[1], yaw, KBEMath.KBE_FLT_MAX, r, 0, true);
        }

        public void Client_onUpdateData_xyz_pr_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            Vector2 xz = stream.readPackXZ();
            float y = stream.readPackY();

            SByte p = stream.readInt8();
            SByte r = stream.readInt8();

            _updateVolatileData(eid, xz[0], y, xz[1], KBEMath.KBE_FLT_MAX, p, r, 0, true);
        }

        public void Client_onUpdateData_xyz_y_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            Vector2 xz = stream.readPackXZ();
            float y = stream.readPackY();

            SByte yaw = stream.readInt8();
            _updateVolatileData(eid, xz[0], y, xz[1], yaw, KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, 0, true);
        }

        public void Client_onUpdateData_xyz_p_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            Vector2 xz = stream.readPackXZ();
            float y = stream.readPackY();

            SByte p = stream.readInt8();

            _updateVolatileData(eid, xz[0], y, xz[1], KBEMath.KBE_FLT_MAX, p, KBEMath.KBE_FLT_MAX, 0, true);
        }

        public void Client_onUpdateData_xyz_r_optimized(MemoryStream stream)
        {
            Int32 eid = getViewEntityIDFromStream(stream);

            Vector2 xz = stream.readPackXZ();
            float y = stream.readPackY();

            SByte r = stream.readInt8();

            _updateVolatileData(eid, xz[0], y, xz[1], KBEMath.KBE_FLT_MAX, KBEMath.KBE_FLT_MAX, r, 0, true);
        }

        private void _updateVolatileData(Int32 entityID, float x, float y, float z, float yaw, float pitch, float roll, sbyte isOnGround, bool isOptimized)
        {
            Entity entity = null;

            if (!entities.TryGetValue(entityID, out entity))
            {
                // 如果为0且客户端上一步是重登陆或者重连操作并且服务端entity在断线期间一直处于在线状态
                // 则可以忽略这个错误, 因为cellapp可能一直在向baseapp发送同步消息， 当客户端重连上时未等
                // 服务端初始化步骤开始则收到同步信息, 此时这里就会出错。
                Dbg.ERROR_MSG("KBEngine::_updateVolatileData: entity(" + entityID + ") not found!");
                return;
            }

            bool isOnGroundChanged = false;
            // 小于0不设置
            if (isOnGround >= 0)
            {
                bool curIsOnGround = (isOnGround > 0);
                isOnGroundChanged = entity.isOnGround != curIsOnGround;
                entity.isOnGround = curIsOnGround;
            }

            bool changeDirection = false;

            if (roll != KBEMath.KBE_FLT_MAX)
            {
                changeDirection = true;
                entity.direction.x = (isOptimized ? KBEMath.int82angle((SByte)roll, false) : roll) * 360 / ((float)System.Math.PI * 2);
            }

            if (pitch != KBEMath.KBE_FLT_MAX)
            {
                changeDirection = true;
                entity.direction.y = (isOptimized ? KBEMath.int82angle((SByte)pitch, false) : pitch) * 360 / ((float)System.Math.PI * 2);
            }

            if (yaw != KBEMath.KBE_FLT_MAX)
            {
                changeDirection = true;
                entity.direction.z = (isOptimized ? KBEMath.int82angle((SByte)yaw, false) : yaw) * 360 / ((float)System.Math.PI * 2);
            }

            bool done = false;
            if (changeDirection == true)
            {
                //TODO annotation by xfl
                //Event.fireOut(EventOutTypes.set_direction, entity);
                entity.onSetDirection();
                done = true;
            }

            bool positionChanged = x != KBEMath.KBE_FLT_MAX || y != KBEMath.KBE_FLT_MAX || z != KBEMath.KBE_FLT_MAX;
            if (x == KBEMath.KBE_FLT_MAX) x = isOptimized ? 0.0f : entity.position.x;
            if (y == KBEMath.KBE_FLT_MAX) y = isOptimized ? 0.0f : entity.position.y;
            if (z == KBEMath.KBE_FLT_MAX) z = isOptimized ? 0.0f : entity.position.z;

            if (positionChanged || isOnGroundChanged)
            {
                Vector3 pos = isOptimized ? new Vector3(x + _entityServerPos.x, y + _entityServerPos.y, z + _entityServerPos.z) : new Vector3(x, y, z);

                entity.position = pos;
                done = true;
                //Event.fireOut(EventOutTypes.updatePosition, entity);
                entity.onSetPosition();
            }

            if (done)
                entity.onUpdateVolatileData();
        }

        /*
			服务端通知流数据下载开始
			请参考API手册关于onStreamDataStarted
		*/
        public void Client_onStreamDataStarted(Int16 id, Int16 dataTypeId, UInt32 datasize, string descr, sbyte dataType)
        {
            BattleManager.Instance.OnHandleStartTransferStreamData(id, dataTypeId, datasize);
        }

        public void Client_onStreamDataRecv(MemoryStream stream)
        {
            BattleManager.Instance.OnHandleTransferStreamData(stream);
        }

        public void Client_onStreamDataCompleted(Int16 id)
        {
            BattleManager.Instance.OnHandleEndTransferStreamData(id);
        }

        /*
			TSS安全SDK网络数据收发接口
		*/
        public void SendTSSDataToServer(byte[] data)
        {
            if (currserver == "baseapp")
            {
                Dbg.DEBUG_MSG("KBEngine::SendTSSDataToServer Baseapp_tssSdkAntiDataFromClient");
                Bundle bundle = Bundle.createObject();
                bundle.newMessage(Messages.messages["Baseapp_tssSdkAntiDataFromClient"]);
                bundle.writeBlob(data);
                bundle.send(_networkInterface);
            }
        }

        public void Client_onUpdateSubPos_y(MemoryStream ms)
        {
            float x = ms.readFloat();
            float y = ms.readFloat();
            float z = ms.readFloat();
            float yawRad = ms.readFloat();

            var entity = player();
            if (entity != null)
            {
                entity.position.Set(x, y, z);
                float yaw = yawRad * 360 / ((float)System.Math.PI * 2);
                entity.direction.Set(entity.direction.x, entity.direction.y, yaw);
                Event.fireOut(EventOutTypes.updatePosition, entity);
                entity.onSetPosition();
                entity.onSetDirectionSmooth();
                entity.onUpdateVolatileData();
            }
        }
    }

    public class KBEngineAppThread : KBEngineApp
    {
        /*
			KBEngine处理线程
		*/
        public class KBEThread
        {

            KBEngineApp app_;
            public bool over = false;

            public KBEThread(KBEngineApp app)
            {
                this.app_ = app;
            }

            public void run()
            {
                Dbg.INFO_MSG("KBEThread::run()");
                over = false;

                try
                {
                    this.app_.process();
                }
                catch (Exception e)
                {
                    Dbg.ERROR_MSG(e.ToString());
                }

                over = true;
                Dbg.INFO_MSG("KBEThread::end()");
            }
        }

        private Thread _t = null;
        public KBEThread kbethread = null;

        // 主循环频率
        public static int threadUpdateHZ = 10;

        // 主循环周期ms 优化去掉循环中做除法
        private static float threadUpdatePeriod = 1000f / threadUpdateHZ;

        // 插件是否退出
        private bool _isbreak = false;

        private System.DateTime _lasttime = System.DateTime.Now;

        public KBEngineAppThread(KBEngineArgs args) :
            base(args)
        {
        }

        public override bool initialize(KBEngineArgs args)
        {
            base.initialize(args);

            KBEngineAppThread.threadUpdateHZ = args.threadUpdateHZ;
            threadUpdatePeriod = 1000f / threadUpdateHZ;

            kbethread = new KBEThread(this);
            _t = new Thread(new ThreadStart(kbethread.run));
            _t.Start();

            return true;
        }

        public override void reset()
        {
            _isbreak = false;
            _lasttime = System.DateTime.Now;

            base.reset();
        }

        /*
			插件退出处理
		*/
        public void breakProcess()
        {
            _isbreak = true;
        }

        public bool isbreak()
        {
            return _isbreak;
        }

        public override void process()
        {
            while (!isbreak())
            {
                base.process();
                _thread_wait();
            }

            Dbg.WARNING_MSG("KBEngineAppThread::process(): break!");
        }

        /*
			防止占满CPU, 需要让线程等待一会
		*/
        void _thread_wait()
        {
            TimeSpan span = DateTime.Now - _lasttime;

            int diff = (int)(threadUpdatePeriod - span.TotalMilliseconds);

            if (diff < 0)
                diff = 0;

            System.Threading.Thread.Sleep(diff);
            _lasttime = DateTime.Now;
        }

        public override void destroy()
        {
            Dbg.WARNING_MSG("KBEngineAppThread::destroy()");
            breakProcess();

            int i = 0;
            while (!kbethread.over && i < 50)
            {
                Thread.Sleep(100);
                i += 1;
            }

            if (_t != null)
                _t.Abort();

            _t = null;

            base.destroy();
        }
    }
}
