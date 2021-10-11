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
Random = str(random.randint(0, 100))  # 随机数


# 1.清空
def test_setEmpty():
    setEmpty = inter.setEmpty(
        tag="business",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("setEmpty:", setEmpty.json())
    print("-" * 100)
    assert str(setEmpty.json()['success']) == "True"


# 2.sendNotification
def test_sendUserNotification():
    sendUserNotification = inter.sendUserNotification(
        type="business",
        userId="231",
        data="sendNotification" + Random,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("sendUserNotification:", sendUserNotification.json())
    print("-" * 100)
    assert str(sendUserNotification.json()['success']) == "True"


# 3.获取通知列表
def test_getNotificationList():
    getNotificationList = inter.getNotificationList(
        tag="business",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getNotificationList:", getNotificationList.json())
    print("-" * 100)
    assert str(getNotificationList.json()['success']) == "True"
