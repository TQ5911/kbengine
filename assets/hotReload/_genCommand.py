import gameglobal
import base64
if gameglobal.isBootstrap:
    import gmCommand
    import gmGroup
    import gmAdmin
    agent = gmCommand.GMAgent(gmAdmin.DUMMY_SU, None, None, gmGroup.MANAGER_GROUP_GOD)
    enc_str = 'TARGET'
    cmd_str = base64.b64decode(enc_str).decode('utf-8')
    gmCommand.doCommandInside(agent, cmd_str)
