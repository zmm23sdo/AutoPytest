import redis
from common.TestInterface import Interface
from common.TestRedis import Redis
import pytest
import json
import time
import random
import hmac, base64, struct, hashlib, time
from common.TestCommon import GetHeaders, NDay, getVerifyCodeImage, getRedis, loginTrue, SetPhone, Unicode, GBK2312, \
    Now, NowDate, TimeNow, Today, UpLoad
from datetime import datetime
from testCase.test_car import test_confirmInspectionReport

inter = Interface()


def CreateCars():
    #   #创建一个公司seller给车辆用：
    print("创建一个公司seller给车辆用：", "↓" * 120)
    #   #新建corp seller：
    phoneNumber = TimeNow()
    phonePrefix = "+86"
    email = "CorpSeller" + TimeNow() + "@seller.com"
    name = "CorpSeller" + Unicode() + GBK2312() + TimeNow()
    addCorpSeller = inter.addCorpSeller(
        phoneNumber=phoneNumber,
        phonePrefix=phonePrefix,
        email=email,
        name=name,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addCorpSeller:", addCorpSeller.json())
    print("-" * 100)
    #   #获取新创建的Seller ID:
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
    #   #获取可选经办人列表:
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
    #   #指定经办人:
    assignSeller = inter.assignSeller(
        id=seller_id,
        assignId=assign_id,
        resourceId=seller_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSeller:", assignSeller.json())
    print("-" * 100)
    #   #提交公司seller审核:
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
    #   #审核通过:
    auditSuccessSeller = inter.auditSuccessSeller(
        resourceId=seller_id,
        id=seller_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditSuccessSeller:", auditSuccessSeller.json())
    print("-" * 100)
    #   #激活新建的Seller:
    print("激活新建的Seller:", "↑" * 120)
    #   #添加车辆:
    createCar = inter.createCar(
        brand="BMW",
        model="1",
        manufacturedYear="1990",
        type="2",
        customerId=seller_id,
        customerName=name,
        customerType="seller",
        phonePrefix=phonePrefix,
        phoneNumber=phoneNumber,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createCar:", createCar.json())
    print("-" * 100)


# 1.获取竞标场次列表
def test_queryBiddingBlock():
    queryBiddingBlock = inter.queryBiddingBlock(
        status="",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("queryBiddingBlock:", queryBiddingBlock.json())
    print("-" * 100)
    assert str(queryBiddingBlock.json()['success']) == "True"
    bidding_id = str(queryBiddingBlock.json()['data'][0]['id'])
    car_no = str(queryBiddingBlock.json()['data'][0]['number'])
    print("-" * 100)
    print("bidding_id:", bidding_id)
    print("car_no:", car_no)
    print("-" * 100)
    return bidding_id, car_no


# 2.批量关联车辆
def test_slotCars():
    # 添加竞标场次:
    ran1 = random.randint(0, 10000)
    ran2 = random.uniform(0, 30)
    startTime = NDay(ran1 + 1, ran2)
    endTime = NDay(ran1 + 2, ran2)
    noticeTime = NDay(ran1, ran2)
    print("-" * 100)
    print("ran1:", ran1)
    print("ran2:", ran2)
    print("-" * 100)
    print("startTime:", startTime)
    print("endTime:", endTime)
    print("noticeTime:", noticeTime)
    print("-" * 100)
    createBiddingBlock = inter.createBiddingBlock(
        startTime=startTime,
        endTime=endTime,
        maxCarCount="100",
        countDownTime="60",
        systemBidPrice="999",
        bidPrice1="999",
        bidPrice2="999",
        bidPrice3="999",
        startNotified="true",
        noticeTime=noticeTime,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createBiddingBlock:", createBiddingBlock.json())
    print("-" * 100)
    #   #获取竞标场次列表:
    queryBiddingBlock = inter.queryBiddingBlock(
        status="pending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("queryBiddingBlock:", queryBiddingBlock.json())
    print("-" * 100)
    bidding_id = str(queryBiddingBlock.json()['data'][0]['id'])
    print("-" * 100)
    print("bidding_id:", bidding_id)
    print("-" * 100)
    #   #创建检车车辆
    reports_id, car_no1 = test_confirmInspectionReport()
    reports_id, car_no2 = test_confirmInspectionReport()
    reports_id, car_no3 = test_confirmInspectionReport()

    print("-" * 100)
    print("car_no1:", car_no1)
    print("car_no2:", car_no2)
    print("car_no3:", car_no3)
    print("-" * 100)
    #   #变更车辆起拍价:
    # car_no1
    editReservedPrice = inter.editReservedPrice(
        number=car_no1,
        reservedPrice="999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("editReservedPrice:", editReservedPrice.json())
    print("-" * 100)
    # car_no2
    editReservedPrice = inter.editReservedPrice(
        number=car_no2,
        reservedPrice="999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("editReservedPrice:", editReservedPrice.json())
    print("-" * 100)
    # car_no3
    editReservedPrice = inter.editReservedPrice(
        number=car_no3,
        reservedPrice="999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("editReservedPrice:", editReservedPrice.json())
    print("-" * 100)
    #   #批量关联车辆:
    slotCars = inter.slotCars(
        id=bidding_id,
        numbers=[car_no1, car_no2, car_no3],
        headers=GetHeaders()
    )
    print("-" * 100)
    print("slotCars:", slotCars.json())
    print("-" * 100)
    assert str(slotCars.json()['success']) == "True"
    return bidding_id, car_no1, car_no2, car_no3


# 3.添加竞标场次:
def test_createBiddingBlock():
    ran1 = random.randint(0, 100)
    ran2 = random.uniform(0, 30)
    startTime = NDay(ran1 + 1, ran2)
    endTime = NDay(ran1 + 2, ran2)
    noticeTime = NDay(ran1, ran2)
    print("-" * 100)
    print("ran1:", ran1)
    print("ran2:", ran2)
    print("-" * 100)
    print("startTime:", startTime)
    print("endTime:", endTime)
    print("noticeTime:", noticeTime)
    print("-" * 100)
    createBiddingBlock = inter.createBiddingBlock(
        startTime=startTime,
        endTime=endTime,
        maxCarCount="100",
        countDownTime="60",
        systemBidPrice="999",
        bidPrice1="999",
        bidPrice2="999",
        bidPrice3="999",
        startNotified="true",
        noticeTime=noticeTime,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createBiddingBlock:", createBiddingBlock.json())
    print("-" * 100)
    assert str(createBiddingBlock.json()['success']) == "True"


# 4.获取竞标场次详情
def test_getBiddingBlockInfo():
    bidding_id, car_no = test_queryBiddingBlock()
    getBiddingBlockInfo = inter.getBiddingBlockInfo(
        id=bidding_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getBiddingBlockInfo:", getBiddingBlockInfo.json())
    print("-" * 100)
    assert str(getBiddingBlockInfo.json()['success']) == "True"


# 5.获取车辆出价明细
def test_getBidList():
    bidding_id, car_no1, car_no2, car_no3 = test_slotCars()
    getBidList = inter.getBidList(
        biddingBlockId=bidding_id,
        carNumber=car_no1,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getBidList:", getBidList.json())
    print("-" * 100)
    assert str(getBidList.json()['success']) == "True"


# 6.批量添加竞标场次
def test_createBiddingBlocks():
    ran1 = random.randint(0, 1000)
    ran2 = random.uniform(0, 30)
    startTime = NDay(ran1 + 1, ran2)
    endTime = NDay(ran1 + 2, ran2)
    noticeTime = NDay(ran1, ran2)
    print("-" * 100)
    print("ran1:", ran1)
    print("ran2:", ran2)
    print("-" * 100)
    print("startTime:", startTime)
    print("endTime:", endTime)
    print("noticeTime:", noticeTime)
    print("-" * 100)
    createBiddingBlocks = inter.createBiddingBlocks(
        maxCarCount="100",
        countDownTime="60",
        systemBidPrice="999",
        startNotified="true",
        startTime=startTime,
        endTime=endTime,
        noticeTime=noticeTime,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createBiddingBlocks:", createBiddingBlocks.json())
    print("-" * 100)
    assert str(createBiddingBlocks.json()['success']) == "True"


# 7.取消竞标场次
def test_cancelBiddingBlock():
    bidding_id, car_no1, car_no2, car_no3 = test_slotCars()
    cancelBiddingBlock = inter.cancelBiddingBlock(
        id=bidding_id,
        comment="取消竞标场次" + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("cancelBiddingBlock:", cancelBiddingBlock.json())
    print("-" * 100)
    assert str(cancelBiddingBlock.json()['success']) == "True"


# 8.批量取消车辆关联
def test_cancelCars():
    bidding_id, car_no1, car_no2, car_no3 = test_slotCars()
    #   #获取竞标场次关联车辆列表：
    getSlottedCars = inter.getSlottedCars(
        id=bidding_id,
        pageSize="999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getSlottedCars:", getSlottedCars.json())
    print("-" * 100)
    car_id0 = str(getSlottedCars.json()['data'][0]['id'])
    car_id1 = str(getSlottedCars.json()['data'][1]['id'])
    car_id2 = str(getSlottedCars.json()['data'][2]['id'])
    print("-" * 100)
    print("car_id0:", car_id0)
    print("car_id1:", car_id1)
    print("car_id2:", car_id2)
    print("-" * 100)
    #   #批量取消车辆关联:
    cancelCars = inter.cancelCars(
        ids=[car_id0, car_id1, car_id2],
        id=bidding_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("cancelCars:", cancelCars.json())
    print("-" * 100)
    assert str(cancelCars.json()['success']) == "True"


# 9.编辑Seller中标意见


# 10.按时间段获取竞标场次
def test_getBiddingBlocks():
    startTime = NDay(0, 0)
    endTime = NDay(2, 2)
    print("-" * 100)
    print("startTime:", startTime)
    print("endTime:", endTime)
    print("-" * 100)
    getBiddingBlocks = inter.getBiddingBlocks(
        startTime=startTime,
        endTime=endTime,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getBiddingBlocks:", getBiddingBlocks.json())
    print("-" * 100)
    assert str(getBiddingBlocks.json()['success']) == "True"


# 11.获取竞标场次关联车辆列表
def test_getSlottedCars():
    bidding_id, car_no1, car_no2, car_no3 = test_slotCars()
    #   #获取竞标场次关联车辆列表：
    getSlottedCars = inter.getSlottedCars(
        id=bidding_id,
        pageSize="999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getSlottedCars:", getSlottedCars.json())
    print("-" * 100)
    assert str(getSlottedCars.json()['success']) == "True"


# 12.获取待关联车辆列表
def test_getApprovedCars():
    getApprovedCars = inter.getApprovedCars(
        id=test_queryBiddingBlock(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getApprovedCars:", getApprovedCars.json())
    print("-" * 100)
    assert str(getApprovedCars.json()['success']) == "True"


# 13.编辑竞标场次
def test_editBiddingBlock():
    bidding_id, car_no1, car_no2, car_no3 = test_slotCars()
    ran1 = random.randint(0, 1000)
    ran2 = random.uniform(0, 30)
    startTime = NDay(ran1 + 2, ran2)
    endTime = NDay(ran1 + 3, ran2)
    noticeTime = NDay(ran1 + 1, ran2)
    print("-" * 100)
    print("ran1:", ran1)
    print("ran2:", ran2)
    print("-" * 100)
    print("startTime:", startTime)
    print("endTime:", endTime)
    print("noticeTime:", noticeTime)
    print("-" * 100)
    editBiddingBlock = inter.editBiddingBlock(
        startTime=startTime,
        endTime=endTime,
        maxCarCount="100",
        countDownTime="60",
        systemBidPrice="999",
        startNotified="true",
        noticeTime=noticeTime,
        id=bidding_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("editBiddingBlock:", editBiddingBlock.json())
    print("-" * 100)
    assert str(editBiddingBlock.json()['success']) == "True"
