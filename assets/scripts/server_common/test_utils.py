# coding: utf-8
from KBEDebug import *
import utils


def test_inTimeTupleRange():
    now = utils.getNow()
    ERROR_MSG("test_inTimeTupleRange:: now", utils.getTimeStr(now))

    # import activityControl_activityData
    # ERROR_MSG("| test_inTimeTupleRange:: show act")
    # for v in activityControl_activityData.datas.values():
    #     s = utils.inTimeTuplesRange(v["openTimeCron"], v["endTimeCron"], now=now)
    #     ERROR_MSG(' \- test_inTimeTupleRange:: actID={}, actName={}, isOpen={}'.format(v["ID"], v["name"], s))
    #
    # import questionnaire_questionnaire
    # ERROR_MSG("| test_inTimeTupleRange:: show quest")
    # for v in questionnaire_questionnaire.datas.values():
    #     s = utils.inTimeTuplesRange(v["showTime"], v["hideTime"], now=now)
    #     ERROR_MSG('\- test_inTimeTupleRange:: questID={}, isOpen={}'.format(v["ID"], s))
