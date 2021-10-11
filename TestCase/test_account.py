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


# 1.login
def test_login():
    code, verify = getRedis()
    loginAccount = inter.loginUser(
        username="mingvtest1",
        password="qwer`123",
        verifyCodeId=code,
        verifyCode=verify
    )
    print("-" * 100)
    print("newLead:", loginAccount.json())
    print("-" * 100)
    assert str(loginAccount.json()['success']) == "True"


# 2.logout
def test_logout():
    logoutAccount = inter.logoutUser(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("logoutAccount:", logoutAccount.json())
    print("-" * 100)
    assert str(logoutAccount.json()['body']['success']) == "True"


# 3.获取所有车辆品牌
def test_getAllCarBrand():
    getAllCarBrand = inter.getAllCarBrand(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("logoutAccount:", getAllCarBrand.json())
    print("-" * 100)
    assert str(getAllCarBrand.json()['success']) == "True"


# 4.获取检车STS
def test_getCheckerSTS():
    getCheckerSTS = inter.getCheckerSTS(
        photo="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("logoutAccount:", getCheckerSTS.json())
    print("-" * 100)
    assert str(getCheckerSTS.json()['success']) == "True"


# 5.检车APP登录
def test_checkerLogin():
    checkerLogin = inter.checkerLogin(
        username="Mvchecker4251",
        password="qwer`123"
    )
    print("-" * 100)
    print("checkerLogin:", checkerLogin.json())
    print("-" * 100)
    assert str(checkerLogin.json()['success']) == "True"


# 6.获取用户信息
def test_getUserInfo():
    getUserInfo = inter.getUserInfo(
        headers=GetHeaders2()
    )
    print("-" * 100)
    print("getUserInfo:", getUserInfo.json())
    print("-" * 100)
    assert str(getUserInfo.json()['success']) == "True"


# 7.获取验证码图片
def test_getVerifyCodeImage():
    getVerifyCodeImage = inter.getVerifyCodeImage()
    print("-" * 100)
    print("getVerifyCodeImage:", getVerifyCodeImage)
    print("-" * 100)
    assert getVerifyCodeImage != None


# 8.验证二步验证
def test_verifyTFA():
    secretKey = "V6V4Y5J3EKAG3TGJ"  # 获取二步验证的密钥

    verifyTFA = inter.verifyTFA(
        code=calGoogleCode(secretKey),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("verifyTFA:", verifyTFA.json())
    print("-" * 100)
    assert str(verifyTFA.json()['success']) == "True"


# 9.修改密码
def test_changePassword():
    changePassword = inter.changePasswordUser(
        newPassword="qwer`123",
        oldPassword="qwer`123",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("changePassword:", changePassword.json())
    print("-" * 100)
    assert str(changePassword.json()['success']) == "True"


# 10.获取任务
def test_getTasks():
    getTasks = inter.getTasks(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getTasks:", getTasks.json())
    print("-" * 100)
    assert str(getTasks.json()['success']) == "True"
