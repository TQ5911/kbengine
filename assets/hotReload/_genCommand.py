import gameglobal
if gameglobal.isBootstrap:
    import gmCommand
    import gmGroup
    import gmAdmin
    agent = gmCommand.GMAgent(gmAdmin.DUMMY_SU, None, None, gmGroup.MANAGER_GROUP_GOD)
    gmCommand.doCommandInside(agent, 'TARGET')
