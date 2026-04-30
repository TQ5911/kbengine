# coding: utf-8
from KBEDebug import *
import utils


def test_inTimeTupleRange():
    now = utils.curTS()
    LOG_ERR("test_inTimeTupleRange:: now", utils.getCommonTimeStr(now))

