import redis
from common.TestInterface import Interface
from common.TestRedis import Redis
import pytest
import json
import time
import random
import hmac, base64, struct, hashlib, time
from common.TestCommon import GetHeaders, getVerifyCodeImage, getRedis, loginTrue, SetPhone, Unicode, GBK2312, TimeNow
from datetime import datetime

inter = Interface()


# 1.获取dealer列表
def test_getDealerList():
    getDealerList = inter.getDealerList(
        status="",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerList:", getDealerList.json())
    print("-" * 100)
    assert str(getDealerList.json()['success']) == "True"
    dealer_id = str(getDealerList.json()['data'][0]['id'])
    print("-" * 100)
    print("dealer_id:", dealer_id)
    print("-" * 100)
    return dealer_id


# 2.文件上传结果
def test_uploadResultDealer():
    uploadResultDealer = inter.uploadResultDealer(
        photo="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("uploadResultDealer:", uploadResultDealer.json())
    print("-" * 100)
    assert str(uploadResultDealer.json()['success']) == "True"


# 3.获取可选经办人列表
def test_getDealerExecutiveId():
    getDealerExecutiveId = inter.getDealerExecutiveId(
        resourceId=test_getDealerList(),
        id=test_getDealerList(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerExecutiveId:", getDealerExecutiveId.json())
    print("-" * 100)
    assert str(getDealerExecutiveId.json()['success']) == "True"


# 4.获取所有经办人列表
def test_getDealerExecutive():
    getDealerExecutive = inter.getDealerExecutive(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerExecutive:", getDealerExecutive.json())
    print("-" * 100)
    assert str(getDealerExecutive.json()['success']) == "True"


# 5.提交dealer审核
def test_submitDealerInfo():
    #   #创建corporate dealer:
    createCorporateDealer = inter.createCorporateDealer(
        email="CorporateDealer" + TimeNow() + "@corporate.dealer",
        contactPerson=Unicode() + GBK2312() + TimeNow(),
        phonePrefix="+86",
        phoneNumber=TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createCorporateDealer:", createCorporateDealer.json())
    print("-" * 100)
    #   #获取dealer列表,获取刚创建的dealer_id:
    getDealerList = inter.getDealerList(
        status="assignPending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerList:", getDealerList.json())
    print("-" * 100)
    assignPendingdealer_id = str(getDealerList.json()['data'][0]['id'])
    print("-" * 100)
    print("assignPendingdealer_id:", assignPendingdealer_id)
    print("-" * 100)
    #   #获取可选经办人列表:
    getDealerExecutiveId = inter.getDealerExecutiveId(
        resourceId=assignPendingdealer_id,
        id=assignPendingdealer_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerExecutiveId:", getDealerExecutiveId.json())
    print("-" * 100)

    def assignId():
        for x in getDealerExecutiveId.json()["data"]:
            if str(x["name"]) == "mingvtest1":
                print(x["id"], x["name"])
                assign_id = str(x["id"])
                return assign_id

    assign_id = str(assignId())
    assert str(assign_id) != None
    print("-" * 100)
    print("assign_id:", assign_id)
    print("-" * 100)
    #   #分配dealer:
    assignDealer = inter.assignDealer(
        resourceId=assignPendingdealer_id,
        id=assignPendingdealer_id,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignDealer:", assignDealer.json())
    print("-" * 100)
    #   #提交dealer审核:
    submitDealerInfo = inter.submitDealerInfo(
        resourceId=assignPendingdealer_id,
        id=assignPendingdealer_id,
        email="DealerInfo" + TimeNow() + "@submit.dealer",
        contactPerson=Unicode() + GBK2312() + TimeNow(),
        companyName="Company" + TimeNow(),
        city="City" + TimeNow(),
        country="Country" + TimeNow(),
        state=TimeNow(),
        companyAddress="CompanyAddress" + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        corpSsmname="截图20210316142730.png",
        corpSsmphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        corpCardname="截图20210316142730.png",
        corpCardphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        filename="截图20210316142730.png",
        filephoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        remarks="Remark" + TimeNow(),
        companyPic=GBK2312() + Unicode() + TimeNow(),
        picIDCardname="截图20210316142730.png",
        picIDCardphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        marginPaid="true",
        marginFilename="截图20210316142730.png",
        marginFilephoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        type="deposit",
        postcode=TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("submitDealerInfo:", submitDealerInfo.json())
    print("-" * 100)
    assert str(submitDealerInfo.json()['success']) == "True"


# 6.保存dealer修改信息
def test_saveEditInfoDealer():
    #   #创建corporate dealer:
    createCorporateDealer = inter.createCorporateDealer(
        email="CorporateDealer" + TimeNow() + "@corporate.dealer",
        contactPerson=Unicode() + GBK2312() + TimeNow(),
        phonePrefix="+86",
        phoneNumber=TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createCorporateDealer:", createCorporateDealer.json())
    print("-" * 100)
    #   #获取dealer列表,获取刚创建的dealer_id:
    getDealerList = inter.getDealerList(
        status="assignPending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerList:", getDealerList.json())
    print("-" * 100)
    assignPendingdealer_id = str(getDealerList.json()['data'][0]['id'])
    print("-" * 100)
    print("assignPendingdealer_id:", assignPendingdealer_id)
    print("-" * 100)
    #   #获取可选经办人列表:
    getDealerExecutiveId = inter.getDealerExecutiveId(
        resourceId=assignPendingdealer_id,
        id=assignPendingdealer_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerExecutiveId:", getDealerExecutiveId.json())
    print("-" * 100)

    def assignId():
        for x in getDealerExecutiveId.json()["data"]:
            if str(x["name"]) == "mingvtest1":
                print(x["id"], x["name"])
                assign_id = str(x["id"])
                return assign_id

    assign_id = str(assignId())
    assert str(assign_id) != None
    print("-" * 100)
    print("assign_id:", assign_id)
    print("-" * 100)
    #   #分配dealer:
    assignDealer = inter.assignDealer(
        resourceId=assignPendingdealer_id,
        id=assignPendingdealer_id,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignDealer:", assignDealer.json())
    print("-" * 100)
    #   #保存dealer修改信息
    saveEditInfoDealer = inter.saveEditInfoDealer(
        resourceId=assignPendingdealer_id,
        id=assignPendingdealer_id,
        email="DealerInfo" + TimeNow() + "@submit.dealer",
        contactPerson=Unicode() + GBK2312() + TimeNow(),
        companyName="Company" + TimeNow(),
        city="City" + TimeNow(),
        country="Country" + TimeNow(),
        state=TimeNow(),
        companyAddress="CompanyAddress" + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        corpSsmname="截图20210316142730.png",
        corpSsmphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        corpCardname="截图20210316142730.png",
        corpCardphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        filename="截图20210316142730.png",
        filephoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        remarks="Remark" + TimeNow(),
        companyPic=GBK2312() + Unicode() + TimeNow(),
        picIDCardname="截图20210316142730.png",
        picIDCardphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        marginPaid="true",
        marginFilename="截图20210316142730.png",
        marginFilephoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        type="deposit",
        postcode=TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("submitDealerInfo:", saveEditInfoDealer.json())
    print("-" * 100)
    assert str(saveEditInfoDealer.json()['success']) == "True"


# 7.审核通过
def test_auditSuccessDealer():
    test_submitDealerInfo()  # 创建新的审核用
    #   #获取approvePending（待审核）dealer列表:
    getDealerList = inter.getDealerList(
        status="approvePending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerList:", getDealerList.json())
    print("-" * 100)
    approvePendingdealer_id = str(getDealerList.json()['data'][0]['id'])
    print("-" * 100)
    print("approvePendingdealer_id:", approvePendingdealer_id)
    print("-" * 100)
    #   #获取可选经办人列表:
    getDealerExecutiveId = inter.getDealerExecutiveId(
        resourceId=approvePendingdealer_id,
        id=approvePendingdealer_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerExecutiveId:", getDealerExecutiveId.json())
    print("-" * 100)

    def assignId():
        for x in getDealerExecutiveId.json()["data"]:
            if str(x["name"]) == "mingvtest1":
                print(x["id"], x["name"])
                assign_id = str(x["id"])
                return assign_id

    assign_id = str(assignId())
    assert str(assign_id) != None
    print("-" * 100)
    print("assign_id:", assign_id)
    print("-" * 100)
    #   #审核通过
    auditSuccessDealer = inter.auditSuccessDealer(
        resourceId=assign_id,
        id=approvePendingdealer_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditSuccessDealer:", auditSuccessDealer.json())
    print("-" * 100)
    assert str(auditSuccessDealer.json()['success']) == "True"


# 8.审核失败
def test_auditFailDealer():
    test_submitDealerInfo()  # 创建新的审核用
    #   #获取approvePending（待审核）dealer列表:
    getDealerList = inter.getDealerList(
        status="approvePending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerList:", getDealerList.json())
    print("-" * 100)
    approvePendingdealer_id = str(getDealerList.json()['data'][0]['id'])
    print("-" * 100)
    print("approvePendingdealer_id:", approvePendingdealer_id)
    print("-" * 100)
    #   #获取可选经办人列表:
    getDealerExecutiveId = inter.getDealerExecutiveId(
        resourceId=approvePendingdealer_id,
        id=approvePendingdealer_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerExecutiveId:", getDealerExecutiveId.json())
    print("-" * 100)

    def assignId():
        for x in getDealerExecutiveId.json()["data"]:
            if str(x["name"]) == "mingvtest1":
                print(x["id"], x["name"])
                assign_id = str(x["id"])
                return assign_id

    assign_id = str(assignId())
    assert str(assign_id) != None
    print("-" * 100)
    print("assign_id:", assign_id)
    print("-" * 100)
    #   #审核失败
    auditFailDealer = inter.auditFailDealer(
        resourceId=assign_id,
        id=approvePendingdealer_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditFailDealer:", auditFailDealer.json())
    print("-" * 100)
    assert str(auditFailDealer.json()['success']) == "True"


# 9.审核退回
def test_auditReviseDealer():
    test_submitDealerInfo()  # 创建新的审核用
    #   #获取approvePending（待审核）dealer列表:
    getDealerList = inter.getDealerList(
        status="approvePending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerList:", getDealerList.json())
    print("-" * 100)
    approvePendingdealer_id = str(getDealerList.json()['data'][0]['id'])
    print("-" * 100)
    print("approvePendingdealer_id:", approvePendingdealer_id)
    print("-" * 100)
    #   #获取可选经办人列表:
    getDealerExecutiveId = inter.getDealerExecutiveId(
        resourceId=approvePendingdealer_id,
        id=approvePendingdealer_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerExecutiveId:", getDealerExecutiveId.json())
    print("-" * 100)

    def assignId():
        for x in getDealerExecutiveId.json()["data"]:
            if str(x["name"]) == "mingvtest1":
                print(x["id"], x["name"])
                assign_id = str(x["id"])
                return assign_id

    assign_id = str(assignId())
    assert str(assign_id) != None
    print("-" * 100)
    print("assign_id:", assign_id)
    print("-" * 100)
    #   #审核退回
    auditReviseDealer = inter.auditReviseDealer(
        resourceId=assign_id,
        id=approvePendingdealer_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditReviseDealer:", auditReviseDealer.json())
    print("-" * 100)
    assert str(auditReviseDealer.json()['success']) == "True"


# 10.获取审核dealer信息
def test_getAuditDealerInfo():
    getAuditDealerInfo = inter.getAuditDealerInfo(
        resourceId=test_getDealerList(),
        id=test_getDealerList(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getAuditDealerInfo:", getAuditDealerInfo.json())
    print("-" * 100)
    assert str(getAuditDealerInfo.json()['success']) == "True"


# 11.获取dealer账户历史
def test_getDealerHistory():
    getDealerHistory = inter.getDealerHistory(
        resourceId=test_getDealerList(),
        id=test_getDealerList(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerHistory:", getDealerHistory.json())
    print("-" * 100)
    assert str(getDealerHistory.json()['success']) == "True"


# 12.检查电话号码
def test_checkPhoneNumber():
    checkPhoneNumber = inter.checkPhoneNumber(
        phonePrefix="+86",
        phoneNumber=TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("checkPhoneNumber:", checkPhoneNumber.json())
    print("-" * 100)
    assert str(checkPhoneNumber.json()['success']) == "True"


# 13.检查公司注册码
def test_checkRegistrationNumber():
    checkRegistrationNumber = inter.checkRegistrationNumber(
        registrationNumber=TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("checkRegistrationNumber:", checkRegistrationNumber.json())
    print("-" * 100)
    assert str(checkRegistrationNumber.json()['success']) == "True"


# 14.检查邮箱
def test_checkEmailDealer():
    checkEmailDealer = inter.checkEmailDealer(
        email="EmailDealer" + TimeNow() + "@check.dealer",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("checkEmailDealer:", checkEmailDealer.json())
    print("-" * 100)
    assert str(checkEmailDealer.json()['success']) == "True"


# 15.创建corporate dealer
def test_createCorporateDealer():
    createCorporateDealer = inter.createCorporateDealer(
        email="CorporateDealer" + TimeNow() + "@corporate.dealer",
        contactPerson=Unicode() + GBK2312() + TimeNow(),
        phonePrefix="+86",
        phoneNumber=TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createCorporateDealer:", createCorporateDealer.json())
    print("-" * 100)
    assert str(createCorporateDealer.json()['success']) == "True"


# 16.创建dealer
def test_createDealer():
    createDealer = inter.createDealer(
        email="Dler" + TimeNow() + "@dealer.com",
        contactPerson=Unicode() + GBK2312() + TimeNow(),
        phonePrefix="+81",
        phoneNumber=TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createDealer:", createDealer.json())
    print("-" * 100)
    assert str(createDealer.json()['success']) == "True"


# 17.获取dealer信息
def test_getDealerInfo():
    getDealerInfo = inter.getDealerInfo(
        resourceId=test_getDealerList(),
        id=test_getDealerList(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerInfo:", getDealerInfo.json())
    print("-" * 100)
    assert str(getDealerInfo.json()['success']) == "True"


# 18.注销dealer
def test_closeDealer():
    test_createDealer()  # 创建Dealer
    closeDealer = inter.closeDealer(
        resourceId=test_getDealerList(),
        id=test_getDealerList(),
        comment="注销dealer" + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("closeDealer:", closeDealer.json())
    print("-" * 100)
    assert str(closeDealer.json()['success']) == "True"


# 19.冻结dealer
def test_freezeDealer():
    test_createDealer()  # 创建Dealer
    freezeDealer = inter.freezeDealer(
        resourceId=test_getDealerList(),
        id=test_getDealerList(),
        comment="冻结dealer" + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("freezeDealer:", freezeDealer.json())
    print("-" * 100)
    assert str(freezeDealer.json()['success']) == "True"


# 20.解冻dealer
def test_reactivateDealer():
    #   #获取（frozen） 冻结dealer列表:
    getDealerList = inter.getDealerList(
        status="frozen",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerList:", getDealerList.json())
    print("-" * 100)
    frozendealer_id = str(getDealerList.json()['data'][0]['id'])
    print("-" * 100)
    print("frozendealer_id:", frozendealer_id)
    print("-" * 100)
    reactivateDealer = inter.reactivateDealer(
        resourceId=frozendealer_id,
        id=frozendealer_id,
        comment="解冻dealer" + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("reactivateDealer:", reactivateDealer.json())
    print("-" * 100)
    assert str(reactivateDealer.json()['success']) == "True"


# 21.创建dealer子账号
def test_createSubsidiaryDealer():
    test_auditSuccessDealer()  # 审核新的dealer用
    getDealerList = inter.getDealerList(
        status="active",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerList:", getDealerList.json())
    print("-" * 100)
    activedealer_id = str(getDealerList.json()['data'][0]['id'])
    print("-" * 100)
    print("activedealer_id:", activedealer_id)
    print("-" * 100)
    createSubsidiaryDealer = inter.createSubsidiaryDealer(
        resourceId=activedealer_id,
        id=activedealer_id,
        phonePrefix="+86",
        phoneNumber=TimeNow(),
        email="Subsidiary" + TimeNow() + "@subsidiary.dealer",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createSubsidiaryDealer:", createSubsidiaryDealer.json())
    print("-" * 100)
    assert str(createSubsidiaryDealer.json()['success']) == "True"


# 22.注销dealer子账号
def test_closeSubsidiaryDealer():
    test_auditSuccessDealer()  # 审核新的dealer用
    #   #创建dealer子账号
    getDealerList = inter.getDealerList(
        status="active",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerList:", getDealerList.json())
    print("-" * 100)
    activedealer_id = str(getDealerList.json()['data'][0]['id'])
    print("-" * 100)
    print("activedealer_id:", activedealer_id)
    print("-" * 100)
    createSubsidiaryDealer = inter.createSubsidiaryDealer(
        resourceId=activedealer_id,
        id=activedealer_id,
        phonePrefix="+86",
        phoneNumber=TimeNow(),
        email="Subsidiary" + TimeNow() + "@subsidiary.dealer",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createSubsidiaryDealer:", createSubsidiaryDealer.json())
    print("-" * 100)
    #   #注销dealer子账号
    closeSubsidiaryDealer = inter.closeSubsidiaryDealer(
        resourceId=activedealer_id,
        id=activedealer_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("closeSubsidiaryDealer:", closeSubsidiaryDealer.json())
    print("-" * 100)
    assert str(closeSubsidiaryDealer.json()['success']) == "True"


# 23.获取dealer子账号列表
def test_getSubsidiaryDealer():
    test_auditSuccessDealer()  # 审核新的dealer用
    #   #创建dealer子账号
    getDealerList = inter.getDealerList(
        status="active",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerList:", getDealerList.json())
    print("-" * 100)
    activedealer_id = str(getDealerList.json()['data'][0]['id'])
    print("-" * 100)
    print("activedealer_id:", activedealer_id)
    print("-" * 100)
    createSubsidiaryDealer = inter.createSubsidiaryDealer(
        resourceId=activedealer_id,
        id=activedealer_id,
        phonePrefix="+86",
        phoneNumber=TimeNow(),
        email="Subsidiary" + TimeNow() + "@subsidiary.dealer",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createSubsidiaryDealer:", createSubsidiaryDealer.json())
    print("-" * 100)
    #   #获取dealer子账号列表
    getSubsidiaryDealer = inter.getSubsidiaryDealer(
        resourceId=activedealer_id,
        id=activedealer_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getSubsidiaryDealer:", getSubsidiaryDealer.json())
    print("-" * 100)
    assert str(getSubsidiaryDealer.json()['success']) == "True"


# 24.分配dealer
def test_assignDealer():
    #   #创建corporate dealer:
    createCorporateDealer = inter.createCorporateDealer(
        email="CorporateDealer" + TimeNow() + "@corporate.dealer",
        contactPerson=Unicode() + GBK2312() + TimeNow(),
        phonePrefix="+86",
        phoneNumber=TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createCorporateDealer:", createCorporateDealer.json())
    print("-" * 100)
    #   #获取dealer列表,获取刚创建的dealer_id:
    getDealerList = inter.getDealerList(
        status="assignPending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerList:", getDealerList.json())
    print("-" * 100)
    assignPendingdealer_id = str(getDealerList.json()['data'][0]['id'])
    print("-" * 100)
    print("assignPendingdealer_id:", assignPendingdealer_id)
    print("-" * 100)
    #   #获取可选经办人列表:
    getDealerExecutiveId = inter.getDealerExecutiveId(
        resourceId=assignPendingdealer_id,
        id=assignPendingdealer_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerExecutiveId:", getDealerExecutiveId.json())
    print("-" * 100)

    def assignId():
        for x in getDealerExecutiveId.json()["data"]:
            if str(x["name"]) == "mingvtest1":
                print(x["id"], x["name"])
                assign_id = str(x["id"])
                return assign_id

    assign_id = str(assignId())
    assert str(assign_id) != None
    print("-" * 100)
    print("assign_id:", assign_id)
    print("-" * 100)
    #   #分配dealer:
    assignDealer = inter.assignDealer(
        resourceId=assignPendingdealer_id,
        id=assignPendingdealer_id,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignDealer:", assignDealer.json())
    print("-" * 100)
    assert str(assignDealer.json()['success']) == "True"
