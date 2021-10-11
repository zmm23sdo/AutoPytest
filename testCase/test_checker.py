import redis
from common.TestInterface import Interface
from common.TestRedis import Redis
import pytest
import json
import time
import random
import hmac, base64, struct, hashlib, time
from common.TestCommon import GetHeaders, GetHeaders2, getVerifyCodeImage,\
    getRedis, loginTrue, SetPhone, Unicode, GBK2312, TimeNow, Today, NowDate
from datetime import datetime

inter = Interface()


# 1.获取检车员业绩统计
def test_performanceInfo():
    performanceInfo = inter.performanceInfo(
        type="week",
        date=NowDate(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("performanceInfo", performanceInfo.json())
    print("-" * 100)

    assert str(performanceInfo.json()['success']) == "True"
    user_id = str(performanceInfo.json()['data'][0]['user']['id'])
    print("-" * 100)
    print("user_id", user_id)
    print("-" * 100)
    return user_id


# 2.更改检车员目标
def test_changeInspectorTarget():
    changeInspectorTarget = inter.changeInspectorTarget(
        id=test_performanceInfo(),
        dayTarget="2",
        monthTarget="10",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("changeInspectorTarget", changeInspectorTarget.json())
    print("-" * 100)
    assert str(changeInspectorTarget.json()['success']) == "True"


# 3.更改检车员工作区域
def test_changeInspectorRegion():
    changeInspectorRegion = inter.changeInspectorRegion(
        id=test_performanceInfo(),
        region="Johor,Kuala Lumpur",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("changeInspectorRegion", changeInspectorRegion.json())
    print("-" * 100)
    assert str(changeInspectorRegion.json()['success']) == "True"


# 4.获取检车员工作状态表
def test_userBreakMonthDetailChecker():
    userBreakMonthDetailChecker = inter.userBreakMonthDetailChecker(
        year="2021",
        month="9",
        id=test_performanceInfo(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("userBreakMonthDetailChecker", userBreakMonthDetailChecker.json())
    print("-" * 100)
    assert str(userBreakMonthDetailChecker.json()['success']) == "True"


# 5.更改检车员工作状态
def test_changeUserWorkStateChecker():
    changeUserWorkStateChecker = inter.changeUserWorkStateChecker(
        date=NowDate(),
        userId=test_performanceInfo(),
        isBreak="true",
        remark="Remark" + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("changeUserWorkStateChecker", changeUserWorkStateChecker.json())
    print("-" * 100)
    assert str(changeUserWorkStateChecker.json()['success']) == "True"


# 6.获取检车员信息变更历史
def test_userChangeHistoryChecker():
    userChangeHistoryChecker = inter.userChangeHistoryChecker(
        id=test_performanceInfo(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("userChangeHistoryChecker", userChangeHistoryChecker.json())
    print("-" * 100)
    assert str(userChangeHistoryChecker.json()['success']) == "True"


# 7.获取客服业绩统计
def test_getCustomerServicePerformanceInfo():
    getCustomerServicePerformanceInfo = inter.getCustomerServicePerformanceInfo(
        date=NowDate(),
        type="week",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getCustomerServicePerformanceInfo", getCustomerServicePerformanceInfo.json())
    print("-" * 100)
    assert str(getCustomerServicePerformanceInfo.json()['success']) == "True"
    customer_id = str(getCustomerServicePerformanceInfo.json()['data'][0]['user']['id'])
    print("-" * 100)
    print("customer_id", customer_id)
    print("-" * 100)
    return customer_id


# 8.更改客服目标
def test_changeCustomerServiceTarget():
    changeCustomerServiceTarget = inter.changeCustomerServiceTarget(
        id=test_getCustomerServicePerformanceInfo(),
        dayTarget="2",
        monthTarget="10",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("changeCustomerServiceTarget", changeCustomerServiceTarget.json())
    print("-" * 100)
    assert str(changeCustomerServiceTarget.json()['success']) == "True"


# 9.获取客服工作状态表
def test_userBreakMonthDetailUser():
    userBreakMonthDetailUser = inter.userBreakMonthDetailUser(
        year="2021",
        month="9",
        id=test_getCustomerServicePerformanceInfo(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("userBreakMonthDetailUser", userBreakMonthDetailUser.json())
    print("-" * 100)
    assert str(userBreakMonthDetailUser.json()['success']) == "True"


# 10.更改客服工作状态
def test_changeUserWorkStateUser():
    changeUserWorkStateUser = inter.changeUserWorkStateUser(
        date=NowDate(),
        userId=test_getCustomerServicePerformanceInfo(),
        isBreak="true",
        remark="Remark" + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("changeUserWorkStateUser", changeUserWorkStateUser.json())
    print("-" * 100)
    assert str(changeUserWorkStateUser.json()['success']) == "True"


# 11.客服信息变更历史
def test_userChangeHistoryUser():
    userChangeHistoryUser = inter.userChangeHistoryUser(
        id=test_getCustomerServicePerformanceInfo(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("userChangeHistoryUser", userChangeHistoryUser.json())
    print("-" * 100)
    assert str(userChangeHistoryUser.json()['success']) == "True"