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

inter = Interface()
Random = TimeNow()
CheckTime = datetime.utcnow().isoformat() + "Z"


# 1.获取车辆列表
def test_getCarListInspector():
    getCarListInspector = inter.getCarListInspector(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getCarListInspector:", getCarListInspector.json())
    print("-" * 100)
    assert str(getCarListInspector.json()['success']) == "True"
    car_number = str(getCarListInspector.json()['data'][0]['number'])
    print("-" * 100)
    print("car_number:", car_number)
    print("-" * 100)
    return car_number


# 2.获取关联卖家
def test_getRelatedCustomer():
    getRelatedCustomer = inter.getRelatedCustomer(
        phonePrefix="+86",
        phoneNumber=Random * 4,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getRelatedCustomer:", getRelatedCustomer.json())
    print("-" * 100)
    assert str(getRelatedCustomer.json()['success']) == "True"


# 3.添加车辆
def test_createCar():
    #   #创建一个公司seller给车辆用：
    print("创建一个公司seller给车辆用：", "↓" * 120)
    #   #新建corp seller：
    phoneNumber = Random
    phonePrefix = "+86"
    email = "CorpSeller" + Random + "@seller.com"
    name = "CorpSeller" + Unicode() + GBK2312() + Random
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
        email="CorpSeller" + Random + "@submit.com",
        name="CorpSeller" + Random + Unicode(),
        companyName="CompanyName" + Random + Unicode(),
        city="City" + Random + Unicode(),
        country="Country" + Random + Unicode(),
        state=Random,
        companyAddress="CompanyAddress" + Random + Unicode(),
        registrationNumber=Random,
        phoneNumber=Random,
        phonePrefix="+86",
        corpSsmname="截图20210316142730.png",
        corpSsmphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        corpCardname="截图20210316142730.png",
        corpCardphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        corpDocname="截图20210316142730.png",
        corpDocphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        remarks="Remark" + Random + Unicode(),
        postcode=Random,
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
    assert str(createCar.json()['success']) == "True"


# 4.获取车辆检车报告列表
def test_getCarInspectionReports():
    getCarInspectionReports = inter.getCarInspectionReports(
        number=test_getCarListInspector(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getCarInspectionReports:", getCarInspectionReports.json())
    print("-" * 100)
    assert str(getCarInspectionReports.json()['success']) == "True"


# 5.获取检车报告车辆信息
def test_getCarInfoCar():
    #   #添加车辆:
    test_createCar()
    car_no = test_getCarListInspector()
    #   #创建检车报告:
    createInspectionReport = inter.createInspectionReport(
        number=car_no,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createInspectionReport:", createInspectionReport.json())
    print("-" * 100)
    #   #获取车辆检车报告列表:
    getCarInspectionReports = inter.getCarInspectionReports(
        number=test_getCarListInspector(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getCarInspectionReports:", getCarInspectionReports.json())
    print("-" * 100)
    report_id = str(getCarInspectionReports.json()['data']['reports'][0]['id'])
    print("-" * 100)
    print("report_id:", report_id)
    print("-" * 100)
    #   #获取检车报告车辆信息:
    getCarInfoCar = inter.getCarInfoCar(
        id=report_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getCarInfoCar:", getCarInfoCar.json())
    print("-" * 100)
    assert str(getCarInfoCar.json()['success']) == "True"
    return report_id, car_no


# 6.获取检车报告车辆照片
def test_getCarPhotoCar():
    report_id, car_no = test_getCarInfoCar()
    getCarPhotoCar = inter.getCarPhotoCar(
        id=report_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getCarPhotoCar:", getCarPhotoCar.json())
    print("-" * 100)
    assert str(getCarPhotoCar.json()['success']) == "True"


# 7.获取检车报告车辆损伤照片
def test_getCarDamagePhotoCar():
    report_id, car_no = test_getCarInfoCar()
    getCarDamagePhotoCar = inter.getCarDamagePhotoCar(
        id=report_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getCarDamagePhotoCar:", getCarDamagePhotoCar.json())
    print("-" * 100)
    assert str(getCarDamagePhotoCar.json()['success']) == "True"


# 8.确认检车报告
def test_confirmInspectionReport():
    #   #检车报告id:
    reports_id, car_no = test_getCarInfoCar()
    #   #编辑车辆信息:
    editCarInfoCar = inter.editCarInfoCar(
        id=reports_id,
        brand="BMW",
        model="1",
        chassisNumber=Random,
        currentColor=Random,
        currentMileage=Random,
        engineCapacity=Random,
        engineNumber=Random,
        existingLoan="false",
        fuelType="Electric",
        licensePlateNumber=Random,
        manufacturedYear="1993",
        originalColor=Random,
        registrationDate=Now(),
        registrationType="Company",
        reservedPrice="999",
        roadTaxExpiryDate=Now(),
        seat="10",
        soldWithLicensePlate="false",
        transmission="MT",
        variant="variant",
        inspectionNotes="a\nb",
        spareKey="Yes",
        b5="Yes",
        location="Segamat",
        dealerIndicator="false",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("editCarInfoCar:", editCarInfoCar.json())
    print("-" * 100)
    #   #编辑车辆损伤信息:
    editCarDamageInfoCar = inter.editCarDamageInfoCar(
        id=reports_id,
        name="Engine Acceleration",
        position="Jerking",
        photo="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("editCarDamageInfoCar:", editCarDamageInfoCar.json())
    print("-" * 100)
    #   #确认检车报告:
    confirmInspectionReport = inter.confirmInspectionReport(
        id=reports_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("confirmInspectionReport:", confirmInspectionReport.json())
    print("-" * 100)
    assert str(confirmInspectionReport.json()['success']) == "True"
    return reports_id, car_no


# 9.删除检车报告
def test_deleteInspectionReport():
    report_id, car_no = test_getCarInfoCar()
    deleteInspectionReport = inter.deleteInspectionReport(
        id=report_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("deleteInspectionReport:", deleteInspectionReport.json())
    print("-" * 100)
    assert str(deleteInspectionReport.json()['success']) == "True"


# 10。修改检车报告到期时间
def test_editInspectionReportExpiredTime():
    reports_id, car_no = test_confirmInspectionReport()
    editInspectionReportExpiredTime = inter.editInspectionReportExpiredTime(
        id=reports_id,
        expiredTime=Now(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("editInspectionReportExpiredTime:", editInspectionReportExpiredTime.json())
    print("-" * 100)
    assert str(editInspectionReportExpiredTime.json()['success']) == "True"


# 11.冻结车辆
def test_freezeCar():
    #   #添加车辆:
    test_createCar()
    car_no = test_getCarListInspector()
    #   #冻结车辆:
    freezeCar = inter.freezeCar(
        number=car_no,
        days="1",
        reason="冻结车辆" + Random,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("freezeCar:", freezeCar.json())
    print("-" * 100)
    assert str(freezeCar.json()['success']) == "True"
    return car_no


# 12.解冻车辆
def test_unfreezeCar():
    unfreezeCar = inter.unfreezeCar(
        number=test_freezeCar(),
        reason="解冻车辆" + Random,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("unfreezeCar:", unfreezeCar.json())
    print("-" * 100)
    assert str(unfreezeCar.json()['success']) == "True"


# 13.注销车辆
def test_deleteCar():
    #   #添加车辆:
    test_createCar()
    car_no = test_getCarListInspector()
    #   #注销车辆:
    deleteCar = inter.deleteCar(
        number=car_no,
        reason="注销车辆" + Random,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("deleteCar:", deleteCar.json())
    print("-" * 100)
    assert str(deleteCar.json()['success']) == "True"


# 14.变更车辆起拍价
def test_editReservedPrice():
    #   #添加车辆:
    test_createCar()
    car_no = test_getCarListInspector()
    #   #变更车辆起拍价:
    editReservedPrice = inter.editReservedPrice(
        number=car_no,
        reservedPrice="999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("editReservedPrice:", editReservedPrice.json())
    print("-" * 100)
    assert str(editReservedPrice.json()['success']) == "True"


# 15.获取车辆活动日志
def test_getCarHistory():
    getCarHistory = inter.getCarHistory(
        number=test_getCarListInspector(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getCarHistory:", getCarHistory.json())
    print("-" * 100)
    assert str(getCarHistory.json()['success']) == "True"


# 16.获取检车报告活动日志
def test_getInspectionReportHistory():
    reports_id, car_no = test_confirmInspectionReport()
    getInspectionReportHistory = inter.getInspectionReportHistory(
        id=reports_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getInspectionReportHistory:", getInspectionReportHistory.json())
    print("-" * 100)
    assert str(getInspectionReportHistory.json()['success']) == "True"


# 17.触发检车
def test_createInspectionNumber():
    #   #添加车辆:
    test_createCar()
    car_no = test_getCarListInspector()
    #   #触发检车:
    createInspectionNumber = inter.createInspectionNumber(
        number=car_no,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createInspectionNumber:", createInspectionNumber.json())
    print("-" * 100)
    assert str(createInspectionNumber.json()['success']) == "True"


# 18.创建检车报告
def test_createInspectionReport():
    #   #添加车辆:
    test_createCar()
    #   #创建检车报告:
    createInspectionReport = inter.createInspectionReport(
        number=test_getCarListInspector(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createInspectionReport:", createInspectionReport.json())
    print("-" * 100)
    assert str(createInspectionReport.json()['success']) == "True"


# 19.获取已完成车辆列表
def test_getCompletedCarList():
    getCompletedCarList = inter.getCompletedCarList(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getCompletedCarList:", getCompletedCarList.json())
    print("-" * 100)
    assert str(getCompletedCarList.json()['success']) == "True"


# 20.编辑车辆信息
def test_editCarInfoCar():
    reports_id, car_no = test_confirmInspectionReport()
    editCarInfoCar = inter.editCarInfoCar(
        id=reports_id,
        brand="BMW",
        model="1",
        chassisNumber=Random,
        currentColor=Random,
        currentMileage=Random,
        engineCapacity=Random,
        engineNumber=Random,
        existingLoan="false",
        fuelType="Electric",
        licensePlateNumber=Random,
        manufacturedYear="1993",
        originalColor=Random,
        registrationDate=Now(),
        registrationType="Company",
        reservedPrice="999",
        roadTaxExpiryDate=Now(),
        seat="10",
        soldWithLicensePlate="false",
        transmission="MT",
        variant="variant",
        inspectionNotes="a\nb",
        spareKey="Yes",
        b5="Yes",
        location="Segamat",
        dealerIndicator="false",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("editCarInfoCar:", editCarInfoCar.json())
    print("-" * 100)
    assert str(editCarInfoCar.json()['success']) == "True"
    return reports_id


# 21.编辑车辆损伤信息
def test_editCarDamageInfoCar():
    #   #检车报告id:
    reports_id, car_no = test_getCarInfoCar()
    #   #编辑车辆损伤信息:`
    editCarDamageInfoCar = inter.editCarDamageInfoCar(
        id=reports_id,
        name="Engine Acceleration",
        position="Jerking",
        photo="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("editCarDamageInfoCar:", editCarDamageInfoCar.json())
    print("-" * 100)
    assert str(editCarDamageInfoCar.json()['success']) == "True"
    return reports_id


# 22.删除车辆损伤信息
def test_deleteCarDamageInfo():
    deleteCarDamageInfo = inter.deleteCarDamageInfo(
        id=test_editCarDamageInfoCar(),
        name="Engine Acceleration",
        position="Jerking",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("deleteCarDamageInfo:", deleteCarDamageInfo.json())
    print("-" * 100)
    assert str(deleteCarDamageInfo.json()['success']) == "True"


# 23.删除车辆照片
def test_deleteCarPhoto():
    #   #获取检车id，车辆Number:
    report_id, car_no = test_getCarInfoCar()
    print("-" * 100)
    print("report_id", report_id)
    print("car_no", car_no)
    print("-" * 100)
    #   #上传车辆图片:
    UpLoad(car_no=car_no)
    #
    deleteCarPhoto = inter.deleteCarPhoto(
        id=report_id,
        name="front_right",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("deleteCarPhoto:", deleteCarPhoto.json())
    print("-" * 100)
    assert str(deleteCarPhoto.json()['success']) == "True"


# 23.关联车辆
def test_slotCar():
    #   #添加竞标场次:
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
    #   #关联车辆:
    reports_id, car_no = test_confirmInspectionReport()
    print("-" * 100)
    print("bidding_id:", bidding_id)
    print("reports_id:", reports_id)
    print("car_no:", car_no)
    print("-" * 100)
    #   #变更车辆起拍价:
    editReservedPrice = inter.editReservedPrice(
        number=car_no,
        reservedPrice="999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("editReservedPrice:", editReservedPrice.json())
    print("-" * 100)
    #   #关联车辆:
    slotCar = inter.slotCar(
        number=car_no,
        id=bidding_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("slotCar:", slotCar.json())
    print("-" * 100)
    assert str(slotCar.json()['success']) == "True"
    return reports_id, bidding_id, car_no


# 24.获取车辆竞标历史
def test_getBiddingHistory():
    reports_id, bidding_id, car_no = test_slotCar()
    getBiddingHistory = inter.getBiddingHistory(
        number=car_no,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getBiddingHistory:", getBiddingHistory.json())
    print("-" * 100)
    assert str(getBiddingHistory.json()['success']) == "True"


# 25.编辑检车备注
def test_editInspectionNotes():
    report_id, car_no = test_getCarInfoCar()
    editInspectionNotes = inter.editInspectionNotes(
        id=report_id,
        comment="编辑检车备注" + Random,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("editInspectionNotes:", editInspectionNotes.json())
    print("-" * 100)
    assert str(editInspectionNotes.json()['success']) == "True"


# 26.获取车辆检车报告完成情况
def test_getReportRequiredInfo():
    report_id, car_no = test_getCarInfoCar()
    getReportRequiredInfo = inter.getReportRequiredInfo(
        id=report_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getReportRequiredInfo:", getReportRequiredInfo.json())
    print("-" * 100)
    assert str(getReportRequiredInfo.json()['success']) == "True"
