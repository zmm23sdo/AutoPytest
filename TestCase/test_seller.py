import redis
from common.TestInterface import Interface
from common.TestRedis import Redis
import pytest
import json
import time
import random
import hmac, base64, struct, hashlib, time
from common.TestCommon import GetHeaders, getVerifyCodeImage, getRedis, loginTrue, SetPhone, Unicode, GBK2312, TimeNow, \
    Today
from datetime import datetime

inter = Interface()


# 1.新建corp seller
def test_addCorpSeller():
    addCorpSeller = inter.addCorpSeller(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        email="CorpSeller" + TimeNow() + "@seller.com",
        name="CorpSeller" + Unicode() + GBK2312() + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addCorpSeller:", addCorpSeller.json())
    print("-" * 100)
    assert str(addCorpSeller.json()['success']) == "True"


# 2.查询seller
def test_querySellerAccount():
    querySellerAccount = inter.querySellerAccount(
        pageSize="9999",
        current="1",
        status="",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addCorpSeller:", querySellerAccount.json())
    print("-" * 100)
    assert str(querySellerAccount.json()['success']) == "True"
    seller_id = str(querySellerAccount.json()['data'][0]['id'])
    print("-" * 100)
    print("seller_id:", seller_id)
    print("-" * 100)
    return seller_id


# 3.冻结seller
def test_freezeSeller():
    querySellerAccount = inter.querySellerAccount(
        pageSize="9999",
        current="1",
        status="active",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addCorpSeller:", querySellerAccount.json())
    print("-" * 100)
    # assert str(querySellerAccount.json()['success']) == "True"
    activeseller_id = str(querySellerAccount.json()['data'][0]['id'])
    print("-" * 100)
    print("activeseller_id:", activeseller_id)
    print("-" * 100)
    freezeSeller = inter.freezeSeller(
        id=activeseller_id,
        comment="冻结seller" + TimeNow(),
        resourceId=activeseller_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("freezeSeller:", freezeSeller.json())
    print("-" * 100)
    assert str(freezeSeller.json()['success']) == "True"


# 4.解冻seller
def test_unfreezeSeller():
    querySellerAccount = inter.querySellerAccount(
        pageSize="9999",
        current="1",
        status="frozen",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addCorpSeller:", querySellerAccount.json())
    print("-" * 100)
    # assert str(querySellerAccount.json()['success']) == "True"
    frozenseller_id = str(querySellerAccount.json()['data'][0]['id'])
    print("-" * 100)
    print("frozenseller_id:", frozenseller_id)
    print("-" * 100)
    unfreezeSeller = inter.unfreezeSeller(
        id=frozenseller_id,
        comment="解冻seller" + TimeNow(),
        resourceId=frozenseller_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("unfreezeSeller:", unfreezeSeller.json())
    print("-" * 100)
    assert str(unfreezeSeller.json()['success']) == "True"


# 5.注销seller
def test_closeSeller():
    querySellerAccount = inter.querySellerAccount(
        pageSize="9999",
        current="1",
        status="active",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addCorpSeller:", querySellerAccount.json())
    print("-" * 100)
    # assert str(querySellerAccount.json()['success']) == "True"
    activeseller_id = str(querySellerAccount.json()['data'][0]['id'])
    print("-" * 100)
    print("activeseller_id:", activeseller_id)
    print("-" * 100)
    closeSeller = inter.closeSeller(
        id=activeseller_id,
        comment="注销seller" + TimeNow(),
        resourceId=activeseller_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("closeSeller:", closeSeller.json())
    print("-" * 100)
    assert str(closeSeller.json()['success']) == "True"


# 6.获取可选经办人列表
def test_getSellerExecutiveId():
    getSellerExecutiveId = inter.getSellerExecutiveId(
        id=test_querySellerAccount(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getSellerExecutiveId:", getSellerExecutiveId.json())
    print("-" * 100)
    assert str(getSellerExecutiveId.json()['success']) == "True"
    SellerExecutive_Id = getSellerExecutiveId.json()['data'][0]['id']
    print("-" * 100)
    print("SellerExecutive_Id:", SellerExecutive_Id)
    print("-" * 100)
    return SellerExecutive_Id


# 7.指定经办人
def test_assignSeller():
    assignSeller = inter.assignSeller(
        id=test_querySellerAccount(),
        assignId=test_getSellerExecutiveId(),
        resourceId=test_querySellerAccount(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSeller:", assignSeller.json())
    print("-" * 100)
    assert str(assignSeller.json()['success']) == "True"


# 8.获取子账号列表
def test_getSellerSubsidiary():
    getSellerSubsidiary = inter.getSellerSubsidiary(
        id=test_querySellerAccount(),
        current="1",
        resourceId=test_querySellerAccount(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getSellerSubsidiary:", getSellerSubsidiary.json())
    print("-" * 100)
    assert str(getSellerSubsidiary.json()['success']) == "True"


# 9.创建Seller子账号
def test_createSellerSubsidiary():
    querySellerAccount = inter.querySellerAccount(
        pageSize="9999",
        current="1",
        status="active",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySellerAccount:", querySellerAccount.json())
    print("-" * 100)
    activeseller_id = str(querySellerAccount.json()['data'][0]['id'])
    createSellerSubsidiary = inter.createSellerSubsidiary(
        id=activeseller_id,
        email="SellerSubsidiary" + TimeNow() + "@subsidiary.com",
        phonePrefix="+86",
        phoneNumber=TimeNow(),
        resourceId=activeseller_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createSellerSubsidiary:", createSellerSubsidiary.json())
    print("-" * 100)
    assert str(createSellerSubsidiary.json()['success']) == "True"


# 10.注销Seller子账号
def test_closeSellerSubsidiary():
    querySellerAccount = inter.querySellerAccount(
        pageSize="9999",
        current="1",
        status="active",
        headers=GetHeaders()
    )
    activeseller_id = str(querySellerAccount.json()['data'][0]['id'])
    print("-" * 100)
    print("activeseller_id:", activeseller_id)
    print("-" * 100)
    getSellerSubsidiary = inter.getSellerSubsidiary(
        id=activeseller_id,
        current="1",
        resourceId=activeseller_id,
        headers=GetHeaders()
    )
    subsidiary_id = str(getSellerSubsidiary.json()['data'][0]['id'])
    print("-" * 100)
    print("subsidiary_id:", subsidiary_id)
    print("-" * 100)
    closeSellerSubsidiary = inter.closeSellerSubsidiary(
        id=subsidiary_id,
        resourceId=activeseller_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("closeSellerSubsidiary:", closeSellerSubsidiary.json())
    print("-" * 100)
    assert str(closeSellerSubsidiary.json()['success']) == "True"


# 11.新建个人seller
def test_addIndividualSeller():
    addIndividualSeller = inter.addIndividualSeller(
        name="IndividualSeller" + Unicode() + GBK2312() + TimeNow(),
        email="IndividualSeller" + TimeNow() + "@individual.seller",
        phonePrefix="+86",
        phoneNumber=TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addIndividualSeller:", addIndividualSeller.json())
    print("-" * 100)
    assert str(addIndividualSeller.json()['success']) == "True"


# 12.为dealer创建seller
def test_addSellerForDealer():
    addSellerForDealer = inter.addSellerForDealer(
        name="SellerForDealer" + TimeNow() + Unicode() + GBK2312(),
        email="SellerForDealer" + TimeNow() + "@SellerForDealer.dealer",
        phonePrefix="+86",
        phoneNumber=TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addSellerForDealer:", addSellerForDealer.json())
    print("-" * 100)
    assert str(addSellerForDealer.json()['success']) == "True"


# 13.获取分派的seller详情
def test_sellerInfo():
    sellerInfo = inter.sellerInfo(
        id=test_querySellerAccount(),
        resourceId=test_querySellerAccount(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("sellerInfo:", sellerInfo.json())
    print("-" * 100)
    assert str(sellerInfo.json()['success']) == "True"


# 14.获取需要审核的seller详情
def test_auditSellerInfo():
    querySellerAccount = inter.querySellerAccount(
        pageSize="9999",
        current="1",
        status="assignPending",
        headers=GetHeaders()
    )
    assignPending_id = str(querySellerAccount.json()['data'][0]['id'])
    print("-" * 100)
    print("assignPending_id:", assignPending_id)
    print("-" * 100)
    auditSellerInfo = inter.auditSellerInfo(
        id=assignPending_id,
        resourceId=assignPending_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditSellerInfo:", auditSellerInfo.json())
    print("-" * 100)
    assert str(auditSellerInfo.json()['success']) == "True"


# 15.提交公司seller审核
def test_submitCorpSellerInfo():
    # 创建一个公司Seller：
    addCorpSeller = inter.addCorpSeller(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        email="CorpSeller" + TimeNow() + "@seller.com",
        name="CorpSeller" + Unicode() + GBK2312() + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addCorpSeller:", addCorpSeller.json())
    print("-" * 100)
    # 获取新创建的Seller ID：
    querySellerAccount = inter.querySellerAccount(
        pageSize="9999",
        current="1",
        status="",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addCorpSeller:", querySellerAccount.json())
    print("-" * 100)
    seller_id = str(querySellerAccount.json()['data'][0]['id'])
    print("-" * 100)
    print("seller_id:", seller_id)
    print("-" * 100)
    # 获取可选经办人列表:
    getSellerExecutiveId = inter.getSellerExecutiveId(
        id=seller_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print(getSellerExecutiveId.json())
    print("-" * 100)

    def assignId():
        for x in getSellerExecutiveId.json()["data"]:
            if str(x["name"]) == "mingvtest1":
                print(x["id"], x["name"], x["count"])
                assign_id = str(x["id"])
                return assign_id

    assign_id = str(assignId())
    assert str(assign_id) != None
    print("-" * 100)
    print("assign_id:", assign_id)
    print("-" * 100)
    # 指定经办人:
    assignSeller = inter.assignSeller(
        id=seller_id,
        assignId=assign_id,
        resourceId=seller_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSeller:", assignSeller.json())
    print("-" * 100)
    # 提交公司seller审核:
    submitCorpSellerInfo = inter.submitCorpSellerInfo(
        id=seller_id,
        email="CorpSeller" + TimeNow() + "@submit.com",
        name="CorpSeller" + TimeNow() + Unicode(),
        companyName="CompanyName" + TimeNow() + Unicode(),
        city="City" + TimeNow() + Unicode(),
        country="Country" + TimeNow() + Unicode(),
        state=TimeNow(),
        companyAddress="CompanyAddress" + TimeNow() + Unicode(),
        registrationNumber=TimeNow(),
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        corpSsmname="截图20210316142730.png",
        corpSsmphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        corpCardname="截图20210316142730.png",
        corpCardphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        corpDocname="截图20210316142730.png",
        corpDocphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        remarks="Remark" + TimeNow() + Unicode(),
        postcode=TimeNow(),
        resourceId=seller_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("submitCorpSellerInfo:", submitCorpSellerInfo.json())
    print("-" * 100)
    assert str(submitCorpSellerInfo.json()['success']) == "True"


# 16.提交个人seller信息修改
def test_submitIndividualSellerInfo():
    # 查询个人seller
    queryIndividualSellerAccount = inter.queryIndividualSellerAccount(
        pageSize="999",
        current="1",
        type="Individual",
        assignedName="mingvtest1",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("queryIndividualSellerAccount:", queryIndividualSellerAccount.json())
    print("-" * 100)
    IndividualSelle_id = str(queryIndividualSellerAccount.json()['data'][0]['id'])
    print("-" * 100)
    print("IndividualSelle_id:", IndividualSelle_id)
    print("-" * 100)
    # 提交个人seller信息修改
    submitIndividualSellerInfo = inter.submitIndividualSellerInfo(
        name="IndividualSeller" + TimeNow() + Unicode(),
        email="IndividualSeller" + TimeNow() + "@seller.individaul",
        id=IndividualSelle_id,
        resourceId=IndividualSelle_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("submitIndividualSellerInfo:", submitIndividualSellerInfo.json())
    print("-" * 100)
    assert str(submitIndividualSellerInfo.json()['success']) == "True"


# 17.审核通过
def test_auditSuccessSeller():
    # 查询待审核seller
    querySellerAccount = inter.querySellerAccount(
        pageSize="9999",
        current="1",
        status="approvePending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySellerAccount:", querySellerAccount.json())
    print("-" * 100)
    approvePending_id = str(querySellerAccount.json()['data'][0]['id'])
    print("-" * 100)
    print("approvePending_id:", approvePending_id)
    print("-" * 100)
    # 审核通过
    auditSuccessSeller = inter.auditSuccessSeller(
        resourceId=approvePending_id,
        id=approvePending_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditSuccessSeller:", auditSuccessSeller.json())
    print("-" * 100)
    assert str(auditSuccessSeller.json()['success']) == "True"


# 18.获取seller history
def test_sellerAccountHistory():
    sellerAccountHistory = inter.sellerAccountHistory(
        id=test_querySellerAccount(),
        resourceId=test_querySellerAccount(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("sellerAccountHistory:", sellerAccountHistory.json())
    print("-" * 100)
    assert str(sellerAccountHistory.json()['success']) == "True"


# 19.审核失败
def test_auditFailSeller():
    # 创建一个公司Seller：
    addCorpSeller = inter.addCorpSeller(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        email="CorpSeller" + TimeNow() + "@seller.com",
        name="CorpSeller" + Unicode() + GBK2312() + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addCorpSeller:", addCorpSeller.json())
    print("-" * 100)
    # 获取新创建的Seller ID：
    querySellerAccount = inter.querySellerAccount(
        pageSize="9999",
        current="1",
        status="",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addCorpSeller:", querySellerAccount.json())
    print("-" * 100)
    seller_id = str(querySellerAccount.json()['data'][0]['id'])
    print("-" * 100)
    print("seller_id:", seller_id)
    print("-" * 100)
    # 获取可选经办人列表:
    getSellerExecutiveId = inter.getSellerExecutiveId(
        id=seller_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print(getSellerExecutiveId.json())
    print("-" * 100)

    def assignId():
        for x in getSellerExecutiveId.json()["data"]:
            if str(x["name"]) == "mingvtest1":
                print(x["id"], x["name"], x["count"])
                assign_id = str(x["id"])
                return assign_id

    assign_id = str(assignId())
    assert str(assign_id) != None
    print("-" * 100)
    print("assign_id:", assign_id)
    print("-" * 100)
    # 指定经办人:
    assignSeller = inter.assignSeller(
        id=seller_id,
        assignId=assign_id,
        resourceId=seller_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSeller:", assignSeller.json())
    print("-" * 100)
    # 提交公司seller审核:
    submitCorpSellerInfo = inter.submitCorpSellerInfo(
        id=seller_id,
        email="CorpSeller" + TimeNow() + "@submit.com",
        name="CorpSeller" + TimeNow() + Unicode(),
        companyName="CompanyName" + TimeNow() + Unicode(),
        city="City" + TimeNow() + Unicode(),
        country="Country" + TimeNow() + Unicode(),
        state=TimeNow(),
        companyAddress="CompanyAddress" + TimeNow() + Unicode(),
        registrationNumber=TimeNow(),
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        corpSsmname="截图20210316142730.png",
        corpSsmphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        corpCardname="截图20210316142730.png",
        corpCardphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        corpDocname="截图20210316142730.png",
        corpDocphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        remarks="Remark" + TimeNow() + Unicode(),
        postcode=TimeNow(),
        resourceId=seller_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("submitCorpSellerInfo:", submitCorpSellerInfo.json())
    print("-" * 100)
    # 查询待审核seller
    querySellerAccount = inter.querySellerAccount(
        pageSize="9999",
        current="1",
        status="approvePending",
        headers=GetHeaders()
    )
    print("*" * 120)
    print("-" * 100)
    print("querySellerAccount:", querySellerAccount.json())
    print("-" * 100)
    approvePending_id = str(querySellerAccount.json()['data'][0]['id'])
    print("-" * 100)
    print("approvePending_id:", approvePending_id)
    print("-" * 100)
    # 审核失败
    auditFailSeller = inter.auditFailSeller(
        resourceId=approvePending_id,
        comment="auditFailSeller" + TimeNow(),
        id=approvePending_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditFailSeller:", auditFailSeller.json())
    print("-" * 100)
    assert str(auditFailSeller.json()['success']) == "True"


# 20.审核退回
def test_auditReviseSeller():
    test_submitCorpSellerInfo()
    # 查询待审核seller
    querySellerAccount = inter.querySellerAccount(
        pageSize="9999",
        current="1",
        status="approvePending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySellerAccount:", querySellerAccount.json())
    print("-" * 100)
    approvePending_id = str(querySellerAccount.json()['data'][0]['id'])
    print("-" * 100)
    print("approvePending_id:", approvePending_id)
    print("-" * 100)
    # 审核失败
    auditReviseSeller = inter.auditReviseSeller(
        resourceId=approvePending_id,
        comment="auditReviseSeller" + TimeNow(),
        id=approvePending_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditReviseSeller:", auditReviseSeller.json())
    print("-" * 100)
    assert str(auditReviseSeller.json()['success']) == "True"


# 21.上传图片成功
def test_uploadResultSeller():
    uploadResultSeller = inter.uploadResultSeller(
        photo="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("uploadResultSeller:", uploadResultSeller.json())
    print("-" * 100)
    assert str(uploadResultSeller.json()['success']) == "True"


# 22.查询获取可查看审核人
def test_getSellerExecutive():
    getSellerExecutive = inter.getSellerExecutive(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getSellerExecutive:", getSellerExecutive.json())
    print("-" * 100)
    assert str(getSellerExecutive.json()['success']) == "True"


# 23.保存修改信息
def test_saveEditInfoSeller():
    # 创建一个公司Seller：
    addCorpSeller = inter.addCorpSeller(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        email="CorpSeller" + TimeNow() + "@seller.com",
        name="CorpSeller" + Unicode() + GBK2312() + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addCorpSeller:", addCorpSeller.json())
    print("-" * 100)
    # 获取新创建的Seller ID：
    querySellerAccount = inter.querySellerAccount(
        pageSize="9999",
        current="1",
        status="",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addCorpSeller:", querySellerAccount.json())
    print("-" * 100)
    seller_id = str(querySellerAccount.json()['data'][0]['id'])
    print("-" * 100)
    print("seller_id:", seller_id)
    print("-" * 100)
    # 获取可选经办人列表:
    getSellerExecutiveId = inter.getSellerExecutiveId(
        id=seller_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print(getSellerExecutiveId.json())
    print("-" * 100)

    def assignId():
        for x in getSellerExecutiveId.json()["data"]:
            if str(x["name"]) == "mingvtest1":
                print(x["id"], x["name"], x["count"])
                assign_id = str(x["id"])
                return assign_id

    assign_id = str(assignId())
    assert str(assign_id) != None
    print("-" * 100)
    print("assign_id:", assign_id)
    print("-" * 100)
    # 指定经办人:
    assignSeller = inter.assignSeller(
        id=seller_id,
        assignId=assign_id,
        resourceId=seller_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSeller:", assignSeller.json())
    print("-" * 100)
    timenow = datetime.utcnow().isoformat()
    checkTime = timenow + "Z"
    saveEditInfoSeller = inter.saveEditInfoSeller(
        id=seller_id,
        createdTime=checkTime,
        email="EditInfoSeller" + TimeNow() + "@edit.seller",
        name="EditInfoSeller" + TimeNow() + GBK2312(),
        phoneNumber=TimeNow(),
        type="Corporate",
        resourceId=seller_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("saveEditInfoSeller:", saveEditInfoSeller.json())
    print("-" * 100)
    assert str(saveEditInfoSeller.json()['success']) == "True"
