from py import code
from common.TestInterface import Interface
from common.TestRedis import Redis
import pytest
import json
import time
import random
import hmac, base64, struct, hashlib, time
from common.TestCommon import GetHeaders, GetHeaders2, calGoogleCode, getVerifyCodeImage, getRedis, loginTrue, SetPhone, \
    Unicode, GBK2312
from datetime import datetime

inter = Interface()


# 1.获取新增dealer
def test_getNewDealerCount():
    getNewDealerCount = inter.getNewDealerCount(
        startTime="2021-09-05T16:00:00.000Z",
        endTime="2021-09-12T15:59:59.999Z",
        interval="86400",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getNewDealerCount:", getNewDealerCount.json())
    print("-" * 100)
    assert str(getNewDealerCount.json()['success']) == "True"


# 2.获取dealer新增统计数据
def test_getNewDealerStatics():
    getNewDealerStatics = inter.getNewDealerStatics(
        dayStart="2021-09-09T16:00:00.000Z",
        dayEnd="2021-09-10T15:59:59.999Z",
        weekStart="2021-09-05T16:00:00.000Z",
        weekEnd="2021-09-12T15:59:59.999Z",
        monthStart="2021-08-31T16:00:00.000Z",
        monthEnd="2021-09-30T15:59:59.999Z",
        lastWeekStart="2021-08-29T16:00:00.000Z",
        lastWeekEnd="2021-09-05T15:59:59.999Z",
        lastMonthStart="2021-07-31T16:00:00.000Z",
        lastMonthEnd="2021-08-31T15:59:59.999Z",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getNewDealerStatics:", getNewDealerStatics.json())
    print("-" * 100)
    assert str(getNewDealerStatics.json()['success']) == "True"


# 3.获取新增seller
def test_getNewSellerCount():
    getNewSellerCount = inter.getNewSellerCount(
        startTime="2021-09-05T16:00:00.000Z",
        endTime="2021-09-12T15:59:59.999Z",
        interval="86400",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getNewSellerCount:", getNewSellerCount.json())
    print("-" * 100)
    assert str(getNewSellerCount.json()['success']) == "True"


# 4.获取seller新增统计数据
def test_getNewSellerStatics():
    getNewSellerStatics = inter.getNewSellerStatics(
        dayStart="2021-09-09T16:00:00.000Z",
        dayEnd="2021-09-10T15:59:59.999Z",
        weekStart="2021-09-05T16:00:00.000Z",
        weekEnd="2021-09-12T15:59:59.999Z",
        monthStart="2021-08-31T16:00:00.000Z",
        monthEnd="2021-09-30T15:59:59.999Z",
        lastWeekStart="2021-08-29T16:00:00.000Z",
        lastWeekEnd="2021-09-05T15:59:59.999Z",
        lastMonthStart="2021-07-31T16:00:00.000Z",
        lastMonthEnd="2021-08-31T15:59:59.999Z",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getNewSellerStatics:", getNewSellerStatics.json())
    print("-" * 100)
    assert str(getNewSellerStatics.json()['success']) == "True"


# 5.获取新增SalesAgent
def test_getNewSalesAgentCount():
    getNewSalesAgentCount = inter.getNewSalesAgentCount(
        startTime="2021-09-05T16:00:00.000Z",
        endTime="2021-09-12T15:59:59.999Z",
        interval="86400",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getNewSalesAgentCount:", getNewSalesAgentCount.json())
    print("-" * 100)
    assert str(getNewSalesAgentCount.json()['success']) == "True"


# 6.获取SalesAgent新增统计数据
def test_getNewSalesAgentStatics():
    getNewSalesAgentStatics = inter.getNewSalesAgentStatics(
        dayStart="2021-09-09T16:00:00.000Z",
        dayEnd="2021-09-10T15:59:59.999Z",
        weekStart="2021-09-05T16:00:00.000Z",
        weekEnd="2021-09-12T15:59:59.999Z",
        monthStart="2021-08-31T16:00:00.000Z",
        monthEnd="2021-09-30T15:59:59.999Z",
        lastWeekStart="2021-08-29T16:00:00.000Z",
        lastWeekEnd="2021-09-05T15:59:59.999Z",
        lastMonthStart="2021-07-31T16:00:00.000Z",
        lastMonthEnd="2021-08-31T15:59:59.999Z",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getNewSalesAgentStatics:", getNewSalesAgentStatics.json())
    print("-" * 100)
    assert str(getNewSalesAgentStatics.json()['success']) == "True"


# 7.获取统计数据
def test_getStatics():
    getStatics = inter.getStatics(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getStatics:", getStatics.json())
    print("-" * 100)
    assert str(getStatics.json()['success']) == "True"
