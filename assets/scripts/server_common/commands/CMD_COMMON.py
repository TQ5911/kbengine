# -*- coding: utf-8 -*-
import utils
import gameglobal
import gameconst
import gmAdmin
import gmCommand
import random
from KBEDebug import *
import gametimer
import gameclass


BASE, CELL, ALL, INSIDE, ALLSIDE = gameconst.BASE, gameconst.CELL,\
    gameconst.ALL, gmAdmin.INSIDE, gmAdmin.ALLSIDE

gm_cmd, forwardGMCommand, callOnApps = gmCommand.gm_cmd, gmCommand.forwardGMCommand,\
    gmCommand._callApps

Int, Str, Float, Player, Entity, PlayerAccount = gmCommand.Int, gmCommand.Str,\
    gmCommand.Float, gmCommand.Player, gmCommand.Entity, gmCommand.PlayerAccount

RARG, RSU, RSTUB, RONE, SELF, RALL= gmCommand.RARG, gmCommand.RSU, gmCommand.RSTUB,\
    gmCommand.RONE, gmCommand.SELF, gmCommand.RALL

GOD_GROUPS = gmCommand.GOD_GROUPS
DEVE_GROUPS = gmCommand.DEVE_GROUPS
