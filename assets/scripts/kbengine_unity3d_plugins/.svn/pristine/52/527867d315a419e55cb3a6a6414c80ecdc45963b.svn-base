using UnityEngine;
using KBEngine;
using System; 
using System.Collections;
using System.Collections.Generic;

namespace KBEngine
{
    public class EntityTypes 
    {
        public static Dictionary<UInt16, string> entitiesNames = new Dictionary<UInt16, string>();
        public static Dictionary<string, Type> entityTypes = new Dictionary<string, Type>();

        private static void initEntityType(UInt16 typeUid, string typeName)
        {
            entitiesNames[typeUid] = typeName;
            foreach (System.Reflection.Assembly ass in AppDomain.CurrentDomain.GetAssemblies())
            {
                Type entityScript = ass.GetType("KBEngine." + typeName);
                if (entityScript == null)
                {
                    entityScript = ass.GetType(typeName);
                }

                if (entityScript != null)
                {
                    entityTypes[typeName] = entityScript;
                    break;
                }
            }
        }

        public static Type getEntityType(string entityTypeName)
        {
            if (entityTypes.ContainsKey(entityTypeName))
                return entityTypes[entityTypeName];
            return null;
        }
    }
}
