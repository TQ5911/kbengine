namespace KBEngine
{
    using UnityEngine;
    using System;
    using System.Collections;
    using System.Collections.Generic;
    using System.Reflection;

    /*
		KBEngine逻辑层的实体基础类
		所有扩展出的游戏实体都应该继承于该模块
	*/
    public class Entity
    {
        // 当前玩家最后一次同步到服务端的位置与朝向
        // 这两个属性是给引擎KBEngine.cs用的，别的地方不要修改
        public Vector3 _entityLastLocalPos = new Vector3(0f, 0f, 0f);
        public Vector3 _entityLastLocalDir = new Vector3(0f, 0f, 0f);
        public bool _entityLastLocalIsOnGround = true;

        public Int32 id = 0;
        public string className { get { return _className; } set { _className = value; classType = MyUtils.GetClassType(value); } }
        private string _className = "";
        public int classType = 0;
        public Vector3 position = new Vector3(0.0f, 0.0f, 0.0f);
        public Vector3 direction = new Vector3(0.0f, 0.0f, 0.0f);
        public float velocity = 0.0f;

        public bool isOnGround = true;

        public object renderObj = null;

        ///<summary>是否已有客户端View部分</summary>
        public bool hasView => view != null;
        public EntityCall entityCallBase = null;
        public EntityCall entityCallCell = null;

        // enterworld之后设置为true
        public bool _inWorld = false;

        /// <summary>
        /// 对于玩家自身来说，它表示是否自己被其它玩家控制了；
        /// 对于其它entity来说，表示我本机是否控制了这个entity
        /// </summary>
        public bool isControlled = false;

        // __init__调用之后设置为true
        public bool _inited = false;

        /// <summary>
        /// True 说明当前entity上的position是否是服务器设置的，当ViewEntity到达这个位置之后，
        /// 这个标记会被置为False
        /// 有些情况会直接将位置设成服务器位置，这个值要记得清掉
        /// 只有等待条件完成才设服务器位置的情况才要需要计算条件然后重置
        /// </summary>
        public bool ServerSetPosition { get; set; }

        /// <summary>
        /// 是否正在技能位移中
        /// true：客户端自己移动到目标位置，中间不同步服务器位置，也不上行客户端位置
        /// </summary>
        public bool isShifting = false;


        // private LuaEntityInterface luaInterface;
        // public LuaTable luaEntity;

        public ViewEntity view;

        public bool inWorld
        {
            get { return _inWorld; }
            set
            {
                _inWorld = value;
                // luaInterface.setBoolProp(luaEntity, "inWorld", value);
            }
        }

        public bool inited
        {
            get { return _inited; }
            set
            {
                _inited = value;
                // luaInterface.setBoolProp(luaEntity, "inited", value);
            }
        }

        // public void initLuaEnt()
        // {
        //     luaInterface = LuaEntityDef.getluaInterface(className);
        //     luaEntity = LuaEntityDef.newLuaEntity(className, id);
        // }

        public static void clear()
        {
        }

        public Entity()
        {


        }

        public void destroy()
        {
            detachComponents();
            onDestroy();
        }

        public virtual void onDestroy()
        {
        }

        public bool isPlayer()
        {
            return id == KBEngineApp.app.entity_id;
        }

        public virtual void onRemoteMethodCall(MemoryStream stream)
        {
            // 动态生成
        }

        public virtual void onUpdatePropertys(MemoryStream stream)
        {
            // 动态生成
        }

        public virtual void onGetBase()
        {
            // 动态生成
        }

        public virtual void onGetCell()
        {
            // 动态生成
        }

        public virtual void onLoseCell()
        {
            // 动态生成
        }

        public virtual void onComponentsEnterworld()
        {
            // 动态生成， 通知组件onEnterworld
        }

        public virtual void onComponentsLeaveworld()
        {
            // 动态生成， 通知组件onLeaveworld
        }

        public virtual EntityCall getBaseEntityCall()
        {
            // 动态生成
            return null;
        }

        public virtual EntityCall getCellEntityCall()
        {
            // 动态生成
            return null;
        }

        /*
			KBEngine的实体构造函数，与服务器脚本对应。
			存在于这样的构造函数是因为KBE需要创建好实体并将属性等数据填充好才能告诉脚本层初始化
		*/
        public virtual void __init__()
        {
        }

        public virtual void callPropertysSetMethods()
        {
            // 动态生成
        }

        public virtual void attachComponents()
        {
            // 动态生成
        }

        public virtual void detachComponents()
        {
            // 动态生成
        }

        public virtual void onSetPosition()
        {
            if (isShifting)
            {
                return;
            }

            if (isPlayer())
            {
                ServerSetPosition = true;
            }
            //如果不是玩家，或者是玩家但没有场景切换，统一走投影设位置，否则在OnEnterWorld里处理
            if (inWorld || !isPlayer())
            {
                if (hasView)
                    view.OnSetPosition(position, false, 0);
                //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SET_POSITION, id, position);
            }
        }

        public virtual void onSetDirection()
        {
            if (isShifting)
            {
                return;
            }

            if (hasView)
                view.OnSetDirection(direction);
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_SET_DIRECTION, id, direction);
        }

        public void baseCall(string methodname, params object[] arguments)
        {
            if (KBEngineApp.app.currserver == "loginapp")
            {
                Dbg.ERROR_MSG(className + "::baseCall(" + methodname + "), currserver=!" + KBEngineApp.app.currserver);
                return;
            }

            ScriptModule module = null;
            if (!EntityDef.moduledefs.TryGetValue(className, out module))
            {
                Dbg.ERROR_MSG("entity::baseCall:  entity-module(" + className + ") error, can not find from EntityDef.moduledefs");
                return;
            }

            Method method = null;
            if (!module.base_methods.TryGetValue(methodname, out method))
            {
                Dbg.ERROR_MSG(className + "::baseCall(" + methodname + "), not found method!");
                return;
            }

            UInt16 methodID = method.methodUtype;

            if (arguments.Length != method.args.Count)
            {
                Dbg.ERROR_MSG(className + "::baseCall(" + methodname + "): args(" + (arguments.Length) + "!= " + method.args.Count + ") size is error!");
                return;
            }

            EntityCall baseEntityCall = getBaseEntityCall();

            baseEntityCall.newCall();
            baseEntityCall.bundle.writeUint16(0);
            baseEntityCall.bundle.writeUint16(methodID);

            try
            {
                for (var i = 0; i < method.args.Count; i++)
                {
                    if (method.args[i].isSameType(arguments[i]))
                    {
                        method.args[i].addToStream(baseEntityCall.bundle, arguments[i]);
                    }
                    else
                    {
                        throw new Exception("arg" + i + ": " + method.args[i].ToString());
                    }
                }
            }
            catch (Exception e)
            {
                Dbg.ERROR_MSG(className + "::baseCall(method=" + methodname + "): args is error(" + e.Message + ")!");
                baseEntityCall.bundle = null;
                return;
            }

            baseEntityCall.sendCall(null);
        }

        public void cellCall(string methodname, params object[] arguments)
        {
            if (KBEngineApp.app.currserver == "loginapp")
            {
                Dbg.ERROR_MSG(className + "::cellCall(" + methodname + "), currserver=!" + KBEngineApp.app.currserver);
                return;
            }

            ScriptModule module = null;
            if (!EntityDef.moduledefs.TryGetValue(className, out module))
            {
                Dbg.ERROR_MSG("entity::cellCall:  entity-module(" + className + ") error, can not find from EntityDef.moduledefs!");
                return;
            }

            Method method = null;
            if (!module.cell_methods.TryGetValue(methodname, out method))
            {
                Dbg.ERROR_MSG(className + "::cellCall(" + methodname + "), not found method!");
                return;
            }

            UInt16 methodID = method.methodUtype;

            if (arguments.Length != method.args.Count)
            {
                Dbg.ERROR_MSG(className + "::cellCall(" + methodname + "): args(" + (arguments.Length) + "!= " + method.args.Count + ") size is error!");
                return;
            }

            EntityCall cellEntityCall = getCellEntityCall();

            if (cellEntityCall == null)
            {
                Dbg.ERROR_MSG(className + "::cellCall(" + methodname + "): no cell!");
                return;
            }

            cellEntityCall.newCall();
            cellEntityCall.bundle.writeUint16(0);
            cellEntityCall.bundle.writeUint16(methodID);

            try
            {
                for (var i = 0; i < method.args.Count; i++)
                {
                    if (method.args[i].isSameType(arguments[i]))
                    {
                        method.args[i].addToStream(cellEntityCall.bundle, arguments[i]);
                    }
                    else
                    {
                        throw new Exception("arg" + i + ": " + method.args[i].ToString());
                    }
                }
            }
            catch (Exception e)
            {
                Dbg.ERROR_MSG(className + "::cellCall(" + methodname + "): args is error(" + e.Message + ")!");
                cellEntityCall.bundle = null;
                return;
            }

            cellEntityCall.sendCall(null);
        }

        public void enterWorld()
        {
            // Dbg.DEBUG_MSG(className + "::enterWorld(" + getDefinedProperty("uid") + "): " + id); 
            inWorld = true;

			try{
				onEnterWorld();
				onComponentsEnterworld();
			}
			catch (Exception e)
			{
				Dbg.ERROR_MSG(className + "::onEnterWorld: error=" + e.ToString());
			}

			//Event.fireOut(EventOutTypes.onEnterWorld, this);
		}
		
		public virtual void onEnterWorld()
		{
		}

		public void leaveWorld()
		{
			// Dbg.DEBUG_MSG(className + "::leaveWorld: " + id); 
			inWorld = false;
			
			try{
				onLeaveWorld();
				onComponentsLeaveworld();
			}
			catch (Exception e)
			{
				Dbg.ERROR_MSG(className + "::onLeaveWorld: error=" + e.ToString());
			}

			//Event.fireOut(EventOutTypes.onLeaveWorld, this);
		}
		
		public virtual void onLeaveWorld()
		{
		}

		public virtual void enterSpace()
		{
			// Dbg.DEBUG_MSG(className + "::enterSpace(" + getDefinedProperty("uid") + "): " + id); 
			inWorld = true;
			
			try{
				onEnterSpace();
			}
			catch (Exception e)
			{
				Dbg.ERROR_MSG(className + "::onEnterSpace: error=" + e.ToString());
			}
			
			//Event.fireOut(EventOutTypes.onEnterSpace, this);
			
			// 要立即刷新表现层对象的位置
			//Event.fireOut(EventOutTypes.set_position, this);
			//Event.fireOut(EventOutTypes.set_direction, this);
		}
		
		public virtual void onEnterSpace()
		{
		}
		
		public virtual void leaveSpace()
		{
			// Dbg.DEBUG_MSG(className + "::leaveSpace: " + id); 
			inWorld = false;
			
			try{
				onLeaveSpace();
			}
            catch (Exception e)
            {
                Dbg.ERROR_MSG(className + "::onLeaveSpace: error=" + e.ToString());
            }

            //Event.fireOut(EventOutTypes.onLeaveSpace, this);
        }

        public virtual void onLeaveSpace()
        {
        }

        //不判断inWorld，无条件接受服务器的数据，跨场景传送时会在inWorld前通过onSetEntityPosAndDir设置面向和位置
        public virtual void onPositionChanged(Vector3 oldValue)
        {
            //Dbg.DEBUG_MSG(className + "::set_position: " + oldValue + " => " + v); 
            //if (isPlayer())
            //    KBEngineApp.app.entityServerPos(position);

            //onSetPosition();
        }

        public virtual void onUpdateVolatileData()
        {
        }

        //不判断inWorld，无条件接受服务器的数据，跨场景传送时会在inWorld前通过onSetEntityPosAndDir设置面向和位置
        public virtual void onDirectionChanged(Vector3 oldValue)
        {
            //Dbg.DEBUG_MSG(className + "::set_direction: " + oldValue + " => " + v); 
            //direction.x = direction.x * 360 / ((float)System.Math.PI * 2);
            //direction.y = direction.y * 360 / ((float)System.Math.PI * 2);
            //direction.z = direction.z * 360 / ((float)System.Math.PI * 2);
            //Event.fireOut(EventOutTypes.set_direction, this);
            //onSetDirection();
        }

        /// <summary>
        /// This callback method is called when the local entity control by the client has been enabled or disabled. 
        /// See the Entity.controlledBy() method in the CellApp server code for more infomation.
        /// </summary>
        /// <param name="isControlled">
        /// 对于玩家自身来说，它表示是否自己被其它玩家控制了；
        /// 对于其它entity来说，表示我本机是否控制了这个entity
        /// </param>
        public virtual void onControlled(bool isControlled_)
        {
            isControlled = isControlled_;
            //EventMgr.Instance.SendEvent(EventDef.EVENT_NET_ON_CONTROLLED, id, isControlled);
        }

        public virtual void updatePlayer(UInt32 currSpaceID, float x, float y, float z, float yaw)
        {
            // 更加安全的更新位置，避免将上一个场景的坐标更新到当前场景中的玩家
            if (currSpaceID > 0 && currSpaceID != KBEngineApp.app.spaceID)
            {
                return;
            }

            position.x = x;
            position.y = y;
            position.z = z;

            direction.z = yaw;
        }

        public virtual List<EntityComponent> getComponents(string componentName, bool all)
        {
            List<EntityComponent> founds = new List<EntityComponent>();
            return founds;
        }

        public virtual void ToAngleOfDirection()
        {
            direction.x = direction.x * 360 / ((float)System.Math.PI * 2);
            direction.y = direction.y * 360 / ((float)System.Math.PI * 2);
            direction.z = direction.z * 360 / ((float)System.Math.PI * 2);
        }

        #region 小工具函数
        //public FieldInfo info = null;
        //public object getDefinedProperty(string valName)
        //{
        //    if (string.IsNullOrEmpty(valName))
        //        return null;

        //    Type tt = this.GetType();
        //    info = tt.GetField(valName);

        //    if (info == null)
        //        return null;

        //    return info.GetValue(this);
        //}
        #endregion 小工具函数
    }

}
