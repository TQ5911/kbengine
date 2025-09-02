namespace KBEngine
{
	using System; 
	using System.Net.Sockets; 
	using System.Net; 
	using System.Collections; 
	using System.Collections.Generic;
	using System.Text;
	using System.Text.RegularExpressions;
	using System.Threading;

	using MessageID = System.UInt16;
	using MessageLength = System.UInt16;
	
	/*
		包发送模块(与服务端网络部分的名称对应)
		处理网络数据的发送
	*/
    public class PacketSenderKCP : PacketSenderBase
    {
		Socket socket_;
		EndPoint remoteEndPint_;

        public PacketSenderKCP(NetworkInterfaceBase networkInterface) : base(networkInterface)
        {
			socket_ = _networkInterface.sock();
			remoteEndPint_ = ((NetworkInterfaceKCP)_networkInterface).remoteEndPint;
        }

		~PacketSenderKCP()
		{
			Dbg.DEBUG_MSG("PacketSenderKCP::~PacketSenderKCP(), destroyed!");
		}

		public override bool send(MemoryStream stream)
		{
			//MemoryStream udpPacket = MemoryStream.createObject();
			//udpPacket.swap(stream);
			return true;
		}

		public bool sendto(byte[] packet, int size)
		{
            string err = "";
            bool sendErr = false;
            try
            {
                socket_.SendTo(packet, size, SocketFlags.None, remoteEndPint_);
            }
            catch (SocketException se)
            {
                Event.fireIn("_closeNetwork", new object[] { _networkInterface });
                err = se.ToString();
                sendErr = true;
            }

            if (sendErr)
            {
                try
                {
                    Dbg.ERROR_MSG(string.Format("PacketSenderKCP::sendto(): send data error, disconnect from '{0}'! error = '{1}'", socket_.RemoteEndPoint, err));
                }
                catch (SocketException se)
                {
                    Dbg.ERROR_MSG(string.Format("PacketSenderKCP::sendto(): send data error, disconnect! error = '{0}'", se));
                }
                return false;
            }

            return true;
		}

		protected override void _asyncSend()
		{
			/* 
			if (_networkInterface == null || !_networkInterface.valid())
			{
				Dbg.WARNING_MSG("PacketSenderKCP::_asyncSend(): network interface invalid!");
				return;
			}

			var socket = _networkInterface.sock();
			EndPoint remoteEndPint = ((NetworkInterfaceKCP)_networkInterface).remoteEndPint;

			while (true)
			{
				socket.SendTo(data, size, SocketFlags.None, remoteEndPint);
			}
			*/
		}
	}
} 
