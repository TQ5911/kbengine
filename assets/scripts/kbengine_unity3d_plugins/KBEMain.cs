using UnityEngine;
using System;
using System.Collections;
using KBEngine;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json.Linq;
using AOT;
using UnityEngine.Profiling;
// using GCloud.TGPA;

/*
	可以理解为插件的入口模块
	在这个入口中安装了需要监听的事件(installEvents)，同时初始化KBEngine(initKBEngine)
*/

public class KBEMain : MonoBehaviour 
{
	public KBEngineApp gameapp = null;
	
	// 在unity3d界面中可见选项
	public DEBUGLEVEL debugLevel = DEBUGLEVEL.DEBUG;
	public bool isMultiThreads = false;
	public string ip = "127.0.0.1";
	public int port = 20013;
	public KBEngineApp.CLIENT_TYPE clientType = KBEngineApp.CLIENT_TYPE.CLIENT_TYPE_MINI;
	public KBEngineApp.NETWORK_ENCRYPT_TYPE networkEncryptType = KBEngineApp.NETWORK_ENCRYPT_TYPE.ENCRYPT_TYPE_BLOWFISH;
	public int syncPlayerMS = 1000 / 10;

	public int threadUpdateHZ = 10 * 2;
	public int serverHeartbeatTick = 60;
	public int TCP_SEND_BUFFER_MAX = (int)KBEngine.NetworkInterfaceBase.TCP_PACKET_MAX;
	public int TCP_RECV_BUFFER_MAX = (int)KBEngine.NetworkInterfaceBase.TCP_PACKET_MAX;
	public int UDP_SEND_BUFFER_MAX = (int)KBEngine.NetworkInterfaceBase.UDP_PACKET_MAX;
	public int UDP_RECV_BUFFER_MAX = (int)KBEngine.NetworkInterfaceBase.UDP_PACKET_MAX;
	public bool useAliasEntityID = false;
	public bool isOnInitCallPropertysSetMethods = true;
	public bool forceDisableUDP = false;

	public bool automaticallyUpdateSDK = true;

	protected virtual void Awake() 
	 {
        useAliasEntityID = false;
		DontDestroyOnLoad(transform.gameObject);
	 }
 
	// Use this for initialization
	protected virtual void Start () 
	{
		MonoBehaviour.print("clientapp::start()");
		installEvents();
		//initKBEngine();
	}
	
	public virtual void installEvents()
	{
      EventMgr.Instance.RegistListener(EventDef.EVENT_NET_ON_CLICK_LOGIN, OnLoginBtnClick);
  }

  public void OnLoginBtnClick(params object[] pSender)
  {
      //重新输入IP登录，清空上次连接操作，出现错有优先排查这里
      if (gameapp != null && ip != (string)pSender[2])
      {
          gameapp.destroy();
          gameapp = null;
      }

        int accountType = int.Parse(pSender[0].ToString());
        string userName = pSender[1].ToString();
        string password = pSender[2].ToString();

        string newIp = (string)pSender[3];
        string[] ipArry = newIp.Split(':');
        ip = ipArry[0];
        if (ipArry.Length > 1)
        {
            port = int.Parse(ipArry[1]);
        }

        Dictionary<string, object> paramDic = pSender[4] as Dictionary<string, object>;

        if (gameapp == null)
        {
            initKBEngine();
            GLog.Log("-------------------------InitKBEngine End!!!!!!!!!!!!!!!!!!!!!");
        }

    //-----------上行设备信息------------------------------------------
    string deviceModel = "";
    if (SystemInfo.deviceType == DeviceType.Handheld)
    {
        deviceModel = SystemInfo.deviceModel;
    }
    else
    {
        deviceModel = SystemInfo.deviceType.ToString();
    }

#if UNITY_ANDROID
    int devicePlatId = (int)PlatformType.ANDROID;
#elif UNITY_IOS
    int devicePlatId = (int)PlatformType.IOS;
#elif UNITY_STANDALONE_OSX
    int devicePlatId = (int)PlatformType.OSX;
#else
    int devicePlatId = (int)PlatformType.PC;
#endif

        paramDic.Add("deviceModel", deviceModel);
        paramDic.Add("deviceId", SystemInfo.deviceUniqueIdentifier);
        paramDic.Add("deviceUniqueIdentifier", GetDeviceUniqueIdentifier());
        paramDic.Add("devicePlatId", devicePlatId);
        paramDic.Add("appVersion", MainStart.GetAppVersion());
        paramDic.Add("patch", MainStart.GetPatchVersion());
        paramDic.Add("vClientIPv6", "");
        paramDic.Add("UA", "");
        paramDic.Add("imei", "");
        string url_args = "";
        foreach (KeyValuePair<string, string> keyValuePair in SDKManager.Instance.CommandLineArgs)
        {
            if (string.IsNullOrEmpty(url_args))
            {
                url_args = string.Format("{0}:{1}", keyValuePair.Key, keyValuePair.Value);
            }
            else
            {
                url_args = string.Format("{0},{1}:{2}", url_args, keyValuePair.Key, keyValuePair.Value);
            }
        }
        paramDic.Add("url_args", url_args);

#if (UNITY_IOS || UNITY_ANDROID) && !UNITY_EDITOR
		paramDic.Add("operatingSystem", SystemInfo.operatingSystem);
		//paramDic.Add("operator", "");
		paramDic.Add("networkState",MyUtils.NetworkState());
		//paramDic.Add("loginChannel", SDKManager.Channel);
#else
        //paramDic.Add("loginChannel", "");
        paramDic.Add("operatingSystem", SystemInfo.operatingSystem);
        //paramDic.Add("operator", "");
        paramDic.Add("networkState", "");
#endif
        paramDic.Add("packageSource", MainStart.Instance.PackageSource);

        //add 数数访客id
        paramDic["distinct_id"] = MyUtils.GetThinkDistinctId();
    
        string oaidStr = "";
#if UNITY_ANDROID && !UNITY_EDITOR

        paramDic["imei"] = MyUtils.GetAndroidDeviceIMEI();
#endif
        paramDic.Add("oaid", oaidStr);

        string iosCaid = "";
#if UNITY_IOS && !UNITY_EDITOR
        //调用tdm接口，获取CAID信息
        // if (TDM.TDataMaster.Instance != null)
        // {
        //     iosCaid = TDM.TDataMaster.Instance.GetStringDeviceInfo("CAID");
        //     if (string.IsNullOrEmpty(iosCaid))
        //     {
        //         iosCaid = "";
        //     }
        //     else
        //     {
        //         GLog.Log("[TDM] get IOS CAID:{0}", iosCaid);
        //     }
        // }
        // paramDic["vClientIPv6"] = MyUtils.GetFirstIpv6Address();
        // paramDic["UA"] = MyUtils.GetIosUserAgentString();
#endif
        paramDic.Add("caid", iosCaid);

        var jsonStr = PlayerPrefs.GetString("LoginDataJson");
        if (!string.IsNullOrEmpty(jsonStr))
        {
	        JObject obj = JObject.Parse(jsonStr);
	        string phoneNumber = obj.Properties().First().Name;
	        paramDic.Add("phoneNumber",phoneNumber);
        }

        //----------------------------------------------------

        string json = MiniJSON.Json.Serialize(paramDic);
      //string param = string.Format("{\"token\":{0}, \"loginServerId\":{1}}", token, serverId);
      GLog.Log("@KBEMain  OnLoginBtnClick accountType={0}  username={1}, password={2}, json={3}", accountType, userName, password, json);
      KBEngine.Event.fireIn("login", accountType, userName, password, System.Text.Encoding.UTF8.GetBytes(json));
   }

    /// <summary>
    /// 获取设备的deviceUniqueIdentifier
    /// </summary>
    private string GetDeviceUniqueIdentifier()
    {
        //腾讯规则说明：
        //针对安卓10以下系统上报IMEI，IOS上报IDFA，此字段不要进行任何加密，记录原始信息即可。
        //目前iOS系统主流的IDFA广告获取设备标识符方式，用户可开启、关闭，每次切换会改变为新的取值。 10以下的版本关闭时也能取到唯一值, >= 10的iOS版本关闭时取到的值为00000000000 ；系统大版本升级（如11 到 12） IDFA也会发生变化
#if UNITY_IOS && !UNITY_EDITOR
        return UnityEngine.iOS.Device.advertisingIdentifier;
#elif UNITY_ANDROID && !UNITY_EDITOR
        if (MyUtils.GetSystemVersionOfYourPhone() < 10)
        {
            return MyUtils.GetAndroidDeviceIMEI();
        }
#elif UNITY_EDITOR || UNITY_STANDALONE
        return SystemInfo.deviceUniqueIdentifier;
#endif
        return "";
    }


    public void onVersionNotMatch(string verInfo, string serVerInfo)
	{
#if UNITY_EDITOR
		if(automaticallyUpdateSDK)
			gameObject.AddComponent<ClientSDKUpdater>();
#endif
	}

	public void onScriptVersionNotMatch(string verInfo, string serVerInfo)
	{
#if UNITY_EDITOR
		if(automaticallyUpdateSDK)
			gameObject.AddComponent<ClientSDKUpdater>();
#endif
	}

	public virtual void initKBEngine()
	{
		// 如果此处发生错误，请查看 Assets\Scripts\kbe_scripts\if_Entity_error_use______git_submodule_update_____kbengine_plugins_______open_this_file_and_I_will_tell_you.cs

		Dbg.debugLevel = debugLevel;

		KBEngineArgs args = new KBEngineArgs();
		
		args.ip = ip;
		args.port = port;
		args.clientType = clientType;
        args.networkEncryptType = networkEncryptType;
        args.syncPlayerMS = syncPlayerMS;
		args.threadUpdateHZ = threadUpdateHZ;
		args.serverHeartbeatTick = serverHeartbeatTick / 2;
		args.useAliasEntityID = useAliasEntityID;
		args.isOnInitCallPropertysSetMethods = isOnInitCallPropertysSetMethods;
#if UNITY_IOS && !UNITY_EDITOR
        args.forceDisableUDP = forceDisableUDP || VersionUtils.IsInAudit();
#else
        args.forceDisableUDP = forceDisableUDP;
#endif

        args.TCP_SEND_BUFFER_MAX = (UInt32)TCP_SEND_BUFFER_MAX;
		args.TCP_RECV_BUFFER_MAX = (UInt32)TCP_RECV_BUFFER_MAX;
		args.UDP_SEND_BUFFER_MAX = (UInt32)UDP_SEND_BUFFER_MAX;
		args.UDP_RECV_BUFFER_MAX = (UInt32)UDP_RECV_BUFFER_MAX;

		args.isMultiThreads = isMultiThreads;
		
		if(isMultiThreads)
			gameapp = new KBEngineAppThread(args);
		else
			gameapp = new KBEngineApp(args);
	}
	
	protected virtual void OnDestroy()
	{
		MonoBehaviour.print("clientapp::OnDestroy(): begin");
        EventMgr.Instance.UnRegistListener(EventDef.EVENT_NET_ON_CLICK_LOGIN, OnLoginBtnClick);
        if (KBEngineApp.app != null)
        {
            KBEngineApp.app.destroy();
            KBEngineApp.app = null;
        }
		KBEngine.Event.clear();
		MonoBehaviour.print("clientapp::OnDestroy(): end");
	}

    protected virtual void FixedUpdate() 
	{

        KBEUpdate();

	}
    private static readonly CustomSampler _testSampler = CustomSampler.Create("KBEUpdate.gameapp.process");
    private static readonly CustomSampler _processOutSampler = CustomSampler.Create("KBEUpdate.processOutEvents");

#if GM
    private float _lastProcessTime = 0;
#endif
    public virtual void KBEUpdate()
	{
#if GM
        ///GM面板中设置了网络处理延迟时间时，才会启用这个逻辑
        if (UIGMPanel.Instance != null && UIGMPanel.Instance.NetworkProcessDelayTime.HasValue)
        {
            if (_lastProcessTime == 0)
            {
                _lastProcessTime = Time.realtimeSinceStartup;
            }
            if (Time.realtimeSinceStartup - _lastProcessTime < UIGMPanel.Instance.NetworkProcessDelayTime.Value)
            {
                return;
            }
            UIGMPanel.Instance.NetworkProcessDelayTime = null;
            _lastProcessTime = 0;
        }
#endif

        if (gameapp == null)
            return;
		// 单线程模式必须自己调用
		if(!isMultiThreads)
        {
            _testSampler.Begin();
            gameapp.process();
            _testSampler.End();
        }
        _processOutSampler.Begin();
        KBEngine.Event.processOutEvents();
        _processOutSampler.End();
	}
}
