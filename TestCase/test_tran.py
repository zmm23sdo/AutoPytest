import redis
from common.TestInterface import Interface
from common.TestRedis import Redis
import pytest
import json
import time
import random
import hmac, base64, struct, hashlib, time
from common.TestCommon import GetHeaders, NDay, getVerifyCodeImage, getRedis, \
    loginTrue, SetPhone, Unicode, GBK2312, Now, NowDate, TimeNow, Today, UpLoad
from datetime import datetime

inter = Interface()


def auditInspection():
    #   #创建新的检车单：
    carYear = 1992
    carBrand = "BMW"
    carModel = "1"
    applyTel = TimeNow()
    applyTelCode = "+86"
    applyName = "ApplyName" + TimeNow() + Unicode()
    applyMail = "Apply" + TimeNow() + "@inspect.apply"
    carType = "2"
    cardUrl = "car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png"
    createInspection = inter.createInspection(
        carYear=carYear,
        carBrand=carBrand,
        carModel=carModel,
        applyTel=applyTel,
        applyTelCode=applyTelCode,
        applyName=applyName,
        applyMail=applyMail,
        carType=carType,
        cardUrl=cardUrl,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createInspection:", createInspection.json())
    print("-" * 100)
    #   #查询待处理检车任务：
    queryNoConfirmInspections = inter.queryNoConfirmInspections(
        current="1",
        pageSize="9999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("queryNoConfirmInspections:", queryNoConfirmInspections.json())
    print("-" * 100)

    #   #循环获取刚创建的检车单id:
    def getId():
        for x in queryNoConfirmInspections.json()['data']:
            if str(x['applyName']) == applyName:
                print(x['applyName'], x['id'])
                inspection_id = str(x['id'])
                return inspection_id

    inspection_id = str(getId())
    assert str(inspection_id) != None
    print("-" * 100)
    print("inspection_id:", inspection_id)
    print("-" * 100)
    #   #根据新建的检车单的手机号去创建seller
    addInspectorSeller = inter.addCorpSeller(
        phoneNumber=applyTel,
        phonePrefix=applyTelCode,
        email=applyMail,
        name=applyName,
        headers=GetHeaders()
    )
    print("根据新建的检车单的手机号去创建seller返回：", addInspectorSeller.json())
    #   #获取关联系统客户
    relatedCustomer = inter.relatedCustomer(
        no=inspection_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("获取关联系统客户返回：", relatedCustomer.json())
    print("-" * 100)
    customer_id = relatedCustomer.json()['data']['id']
    customer_id = str(customer_id)
    print("-" * 100)
    print("获取关联系统客户id返回：", customer_id)
    print("-" * 100)
    print("-" * 100)
    print("激活seller:", "↓" * 100)
    #   #获取Seller可选经办人列表
    getSellerExecutiveId = inter.getSellerExecutiveId(
        id=customer_id,
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
    #   #Seller指定经办人:
    assignSeller = inter.assignSeller(
        id=customer_id,
        assignId=assign_id,
        resourceId=customer_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSeller:", assignSeller.json())
    print("-" * 100)
    #   #Seller提交审核
    submitAdudit = inter.submitCorpSellerInfo(
        id=customer_id,
        email=applyMail,
        name=applyName,
        companyName="Company" + applyName,
        city="City" + TimeNow(),
        country="Country" + TimeNow(),
        state="21315",
        companyAddress="companyAddress" + TimeNow(),
        registrationNumber="0123" + TimeNow(),
        phoneNumber=applyTel,
        phonePrefix=applyTelCode,
        corpSsmname="截图20210316142730.png",
        corpSsmphoto=cardUrl,
        corpCardname="截图20210316142730.png",
        corpCardphoto=cardUrl,
        corpDocname="截图20210316142730.png",
        corpDocphoto=cardUrl,
        remarks="Remark",
        postcode="21312d",
        resourceId=customer_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("提交审核反馈：", submitAdudit.json())
    print("-" * 100)
    #   #Seller审核通过
    auditSuccess = inter.auditSuccessSeller(
        resourceId=assign_id,
        id=customer_id,
        headers=GetHeaders()
    )
    print("审核通过返回：", auditSuccess.json())
    print("激活seller:", "↑" * 100, "完毕")
    #   #检车单关联seller
    associateSeller = inter.associateSellerInspector(
        id=inspection_id,
        customerId=customer_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("检车单关联seller:", associateSeller.json())
    print("-" * 100)
    #   #新建检车员用于审核检车单：
    print("新建检车员:", "↓" * 100)
    checkName = "MC" + TimeNow()
    password = "qwer`123"
    newCheck = inter.newChecker(
        username=checkName,
        password=password,
        name=Unicode() + GBK2312() + TimeNow(),
        email=checkName + "@inspector.io",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("新建检车员返回：", newCheck.json())
    print("-" * 100)
    print("新建检车员:", "↑" * 100, "完毕")
    #   #检车单获取待分配检车员:
    inspectorsWithTarget = inter.inspectorsWithTarget(
        checkTime=Now(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("获取待分配检车员返回：", inspectorsWithTarget.json())
    print("-" * 100)

    #   #循环取出刚刚新建的检车员id给检车单用:
    def checkId():
        for x in inspectorsWithTarget.json()["data"]:
            if str(x["name"]) == checkName:
                print(x["id"], x["name"], x["count"])
                check_id = str(x["id"])
                return check_id

    check_id = str(checkId())
    assert str(check_id) != None
    print("-" * 100)
    print("check_id:", check_id)
    print("-" * 100)
    #   #确认检车单
    confirmInspection = inter.confirmInspection(
        id=inspection_id,
        checkTime=Now(),
        address="Address" + TimeNow(),
        city="City" + TimeNow(),
        region="Region" + TimeNow(),
        postCode="Postcode" + TimeNow(),
        checkerName=checkName,
        checkerId=check_id,
        headers=GetHeaders()
    )
    print("确认检车单返回：", confirmInspection.json())
    #   #App编辑提交检车:
    print("App编辑提交检车:", "~" * 120)
    #   #检车APP登录:
    checkerLogin = inter.checkerLogin(
        username=checkName,
        password=password,
    )
    print("检车APP登录返回：", checkerLogin.json())
    check_token = checkerLogin.json()['data']['token']
    print("*" * 100)
    print("获取检车APP登录token：", check_token)
    print("*" * 100)
    # 更新headers，检车员登录token
    appHeaders = {'Authorization': 'Bearer ' + check_token}
    print("*" * 100)
    print("更新headers，检车员登录token：", appHeaders)
    print("*" * 100)
    #   #编辑车辆信息
    editCarInfo = inter.editCarInfoInspector(
        id=inspection_id,
        brand=carBrand,
        model=carModel,
        chassisNumber=TimeNow(),
        currentColor=TimeNow(),
        currentMileage=TimeNow(),
        engineCapacity=TimeNow(),
        engineNumber=TimeNow(),
        existingLoan="false",
        fuelType="Electric",
        licensePlateNumber="lno",
        manufacturedYear="1993",
        originalColor="oc",
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
        headers=appHeaders
    )
    print("*" * 100)
    print("编辑车辆信息返回：", editCarInfo.json())
    print("*" * 100)
    #   #编辑车辆损伤信息
    position1 = "Jerking"
    photos1 = ["car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png"]
    position2 = "Misfire"
    photos2 = ["car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png"]
    position3 = "Lack of Power"
    photos3 = ["car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png"]
    position4 = "Stalling"
    photos4 = ["car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png"]
    editCarDamageInfo = inter.editCarDamageInfoInspector(
        id=inspection_id,
        position1=position1,
        photos1=photos1,
        position2=position2,
        photos2=photos2,
        position3=position3,
        photos3=photos3,
        position4=position4,
        photos4=photos4,
        headers=appHeaders
    )
    print("*" * 100)
    print("编辑车辆损伤信息返回：", editCarDamageInfo.json())
    print("*" * 100)

    #   #App提交检车任务
    submitCheckerTask = inter.submitCheckerTask(
        id=inspection_id,
        expectPrice="999",
        inspectorDecision="InspectorDecision" + TimeNow(),
        remarks="Remarks" + TimeNow(),
        headers=appHeaders
    )
    print("提交检车任务返回：", submitCheckerTask.json())
    print("App编辑提交检车", "~" * 120, "完毕")
    #   #审核详情:
    auditInspectionInfo = inter.auditInspectionInfo(
        id=inspection_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditInspectionInfo:", auditInspectionInfo.json())
    print("-" * 100)
    #   #检车审核成功
    auditSuccessInspector = inter.auditSuccessInspector(
        no=inspection_id,
        comment="buyout",
        price="9999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditSuccessInspector:", auditSuccessInspector.json())
    print("-" * 100)
    return inspection_id


# 1.查询交易
def test_queryTransOrder():
    queryTransOrder = inter.queryTransOrder(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("queryTransOrder:", queryTransOrder.json())
    print("-" * 100)
    assert str(queryTransOrder.json()['success']) == "True"
    tran_id = str(queryTransOrder.json()['data'][0]['id'])
    print("-" * 100)
    print("tran_id:", tran_id)
    print("-" * 100)
    return tran_id


# 2.获取operationAdmin以及sellerTransaction
def test_executiveWithSeller():
    executiveWithSeller = inter.executiveWithSeller(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("executiveWithSeller:", executiveWithSeller.json())
    print("-" * 100)
    assert str(executiveWithSeller.json()['success']) == "True"
    executiveWithSeller_id = str(executiveWithSeller.json()['data'][0]['id'])
    print("-" * 100)
    print("executiveWithSeller_id:", executiveWithSeller_id)
    print("-" * 100)
    return executiveWithSeller_id


# 3.获取operationAdmin以及dealerExecutive
def test_executiveWithDealer():
    executiveWithDealer = inter.executiveWithDealer(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("executiveWithDealer:", executiveWithDealer.json())
    print("-" * 100)
    assert str(executiveWithDealer.json()['success']) == "True"
    executiveWithDealer_id = str(executiveWithDealer.json()['data'][0]['id'])
    print("-" * 100)
    print("executiveWithDealer_id:", executiveWithDealer_id)
    print("-" * 100)
    return executiveWithDealer_id


# 4.获取seller交易员
def test_sellerTraders():
    sellerTraders = inter.sellerTraders(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("sellerTraders:", sellerTraders.json())
    print("-" * 100)
    assert str(sellerTraders.json()['success']) == "True"
    seller_trader_id = str(sellerTraders.json()['data'][0]['id'])
    seller_trader_name = str(sellerTraders.json()['data'][0]['name'])
    print("-" * 100)
    print("seller_trader_id:", seller_trader_id)
    print("seller_trader_name:", seller_trader_name)
    print("-" * 100)
    return seller_trader_id, seller_trader_name


# 5.获取dealer交易员
def test_dealerTraders():
    dealerTraders = inter.dealerTraders(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("dealerTraders:", dealerTraders.json())
    print("-" * 100)
    assert str(dealerTraders.json()['success']) == "True"


# 6.指定分配人
def test_assignExecutive():
    inspection_id = auditInspection()

    print("-" * 100)
    print("inspection_id", inspection_id)
    print("-" * 100)
    #   #trans_id：
    queryTransOrder = inter.queryTransOrder(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("queryTransOrder:", queryTransOrder.json())
    print("-" * 100)

    def getTransId():
        for x in queryTransOrder.json()['data']:
            if str(x['fromId']) == inspection_id:
                print(x["id"], x["sellerId"], x["carNo"])
                trans_id = str(x["id"])
                return trans_id

    trans_id = str(getTransId())
    assert str(trans_id) != None
    print("-" * 100)
    print("trans_id:", trans_id)
    print("-" * 100)
    #   #assign_id:
    executiveWithSeller = inter.executiveWithSeller(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("executiveWithSeller:", executiveWithSeller.json())
    print("-" * 100)

    def getAssignId():
        for x in executiveWithSeller.json()['data']:
            if str(x['name']) == "mingvtest1":
                print(x["id"], x["name"], x["count"])
                assign_id = str(x["id"])
                return assign_id

    assign_id = str(getAssignId())
    assert str(assign_id) != None
    print("-" * 100)
    print("assign_id:", assign_id)
    print("-" * 100)
    #   #指定分配人:
    assignExecutive = inter.assignExecutive(
        assignId=assign_id,
        id=trans_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignExecutive:", assignExecutive.json())
    print("-" * 100)
    assert str(assignExecutive.json()['success']) == "True"
    return trans_id


# 7.查看预约信息
def test_appointmentInfo():
    appointmentInfo = inter.appointmentInfo(
        id=test_assignExecutive(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("appointmentInfo:", appointmentInfo.json())
    print("-" * 100)
    assert str(appointmentInfo.json()['success']) == "True"


# 8.提交预约信息
def test_submitAppointmentInfo():
    trans_id = test_assignExecutive()
    submitAppointmentInfo = inter.submitAppointmentInfo(
        bizId=trans_id,
        appointmentDate=Now(),
        province="Province" + TimeNow(),
        district="District" + TimeNow(),
        zipCode="ZipCode" + TimeNow(),
        detail="Detail" + TimeNow(),
        files="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        transAmount="9999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("submitAppointmentInfo:", submitAppointmentInfo.json())
    print("-" * 100)
    assert str(submitAppointmentInfo.json()['success']) == "True"
    return trans_id


# 9.保存预约信息
def test_saveAppointmentInfo():
    saveAppointmentInfo = inter.saveAppointmentInfo(
        bizId=test_assignExecutive(),
        appointmentDate=Now(),
        province="Province" + TimeNow(),
        district="District" + TimeNow(),
        zipCode="ZipCode" + TimeNow(),
        detail="Detail" + TimeNow(),
        files="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        transAmount="9999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("saveAppointmentInfo:", saveAppointmentInfo.json())
    print("-" * 100)
    assert str(saveAppointmentInfo.json()['success']) == "True"


# 10.获取sellerTX
def test_sellerTransInfo():
    trans_id = test_submitAppointmentInfo()
    sellerTransInfo = inter.sellerTransInfo(
        id=trans_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("sellerTransInfo:", sellerTransInfo.json())
    print("-" * 100)
    assert str(sellerTransInfo.json()['success']) == "True"
    return trans_id


# 11.保存sellerTx
def test_saveSellerTransInfo():
    trans_id = test_sellerTransInfo()
    seller_trader_id, seller_trader_name = test_sellerTraders()
    photo = "car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png"
    type = "png"
    saveSellerTransInfo = inter.saveSellerTransInfo(
        transDate=Now(),
        carLocation="CarLocation" + TimeNow(),
        operatorId=seller_trader_id,
        operatorName=seller_trader_name,
        serviceFee="2",
        loanAmount="",
        remark="Remark" + TimeNow(),
        type_purchaseInvoice=type,
        photo_purchaseInvoice=photo,
        name_purchaseInvoice=Unicode() + GBK2312() + TimeNow(),
        type_odo=type,
        photo_odo=photo,
        name_odo=Unicode() + GBK2312() + TimeNow(),
        type_vccl=type,
        photo_vccl=photo,
        name_vccl=Unicode() + GBK2312() + TimeNow(),
        type_partyLetter=type,
        photo_partyLetter=photo,
        name_partyLetter=Unicode() + GBK2312() + TimeNow(),
        transId=trans_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("saveSellerTransInfo:", saveSellerTransInfo.json())
    print("-" * 100)
    assert str(saveSellerTransInfo.json()['success']) == "True"
    return trans_id, seller_trader_id, seller_trader_name


# 12.提交sellerTX
def test_submitSellerTransInfo():
    trans_id, seller_trader_id, seller_trader_name = test_saveSellerTransInfo()
    submitSellerTransInfo = inter.submitSellerTransInfo(
        transDate=Now(),
        carLocation="CarLocation" + TimeNow(),
        operatorId=seller_trader_id,
        operatorName=seller_trader_name,
        serviceFee="2",
        loanAmount="",
        remark="Remark" + TimeNow(),
        type_purchaseInvoice="png",
        photo_purchaseInvoice="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        name_purchaseInvoice=Unicode() + GBK2312() + TimeNow(),
        type_odo="png",
        photo_odo="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        name_odo=Unicode() + GBK2312() + TimeNow(),
        type_vccl="png",
        photo_vccl="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        name_vccl=Unicode() + GBK2312() + TimeNow(),
        type_partyLetter="png",
        photo_partyLetter="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        name_partyLetter=Unicode() + GBK2312() + TimeNow(),
        transId=trans_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("submitSellerTransInfo:", submitSellerTransInfo.json())
    print("-" * 100)
    assert str(submitSellerTransInfo.json()['success']) == "True"


# 13.获取dealerInfo
def test_dealerTransInfo():
    print("Car Number", "=" * 120)
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
    #   #获取car_Number:
    getCarListInspector = inter.getCarListInspector(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getCarListInspector:", getCarListInspector.json())
    print("-" * 100)
    car_number = str(getCarListInspector.json()['data'][0]['number'])
    print("-" * 100)
    print("car_number:", car_number)
    print("-" * 100)
    print("Car Number", "=" * 120)
    #   #创建可用dealer：
    print("Dealer", "=" * 120)
    #   #创建corporate dealer:
    email = "Dealer" + TimeNow() + "@corporate.dealer"
    contactPerson = Unicode() + GBK2312() + TimeNow()
    phonePrefix = "+86"
    phoneNumber = TimeNow()
    createCorporateDealer = inter.createCorporateDealer(
        email=email,
        contactPerson=contactPerson,
        phonePrefix=phonePrefix,
        phoneNumber=phoneNumber,
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
        email=email,
        contactPerson=contactPerson,
        companyName="Company" + TimeNow(),
        city="City" + TimeNow(),
        country="Country" + TimeNow(),
        state=TimeNow(),
        companyAddress="CompanyAddress" + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=phoneNumber,
        phonePrefix=phonePrefix,
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
    print("Dealer", "=" * 120)
    #   #获取operationAdmin以及dealerExecutive:
    executiveWithDealer = inter.executiveWithDealer(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("executiveWithDealer:", executiveWithDealer.json())
    print("-" * 100)

    def executiveWithDealerId():
        for x in executiveWithDealer.json()["data"]:
            if str(x["name"]) == "mingvtest1":
                print(x["id"], x["name"])
                executiveWithDealer_id = str(x["id"])
                return executiveWithDealer_id

    executiveWithDealer_id = str(executiveWithDealerId())
    assert str(executiveWithDealer_id) != None
    print("-" * 100)
    print("executiveWithDealer_id:", executiveWithDealer_id)
    print("-" * 100)
    #   #获取dealer列表:
    getDealerList = inter.getDealerList(
        status="active",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerList:", getDealerList.json())
    print("-" * 100)
    #   #取出参数:
    car_no = car_number
    dealer_phonePrefix = str(getDealerList.json()['data'][0]['phonePrefix'])
    dealer_phoneNumber = str(getDealerList.json()['data'][0]['phoneNumber'])
    dealer_email = str(getDealerList.json()['data'][0]['email'])
    assign_id = executiveWithDealer_id
    print("-" * 100)
    print("car_no:", car_no)
    print("dealer_phonePrefix:", dealer_phonePrefix)
    print("dealer_phoneNumber:", dealer_phoneNumber)
    print("dealer_email:", dealer_email)
    print("assign_id:", assign_id)
    print("-" * 100)
    #   #生成线下订单:
    createOfflineOrder = inter.createOfflineOrder(
        id=car_no,
        phoneNumber=dealer_phoneNumber,
        phonePrefix=dealer_phonePrefix,
        email=dealer_email,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createOfflineOrder:", createOfflineOrder.json())
    print("-" * 100)
    #   #查询刚刚添加的交易:
    queryTransOrder = inter.queryTransOrder(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("queryTransOrder:", queryTransOrder.json())
    print("-" * 100)
    tran_id = str(queryTransOrder.json()['data'][0]['id'])
    print("-" * 100)
    print("tran_id:", tran_id)
    print("-" * 100)
    #   #获取dealerInfo:
    dealerTransInfo = inter.dealerTransInfo(
        id=tran_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("dealerTransInfo:", dealerTransInfo.json())
    print("-" * 100)
    assert str(dealerTransInfo.json()['success']) == "True"
    return tran_id


# 14.保存dealeInfo
def test_saveDealerTransInfo():
    #   #获取operationAdmin以及dealerExecutive:
    executiveWithDealer = inter.executiveWithDealer(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("executiveWithDealer:", executiveWithDealer.json())
    print("-" * 100)
    executive_id = str(executiveWithDealer.json()['data'][0]['id'])
    executive_name = str(executiveWithDealer.json()['data'][0]['name'])
    trans_id = test_dealerTransInfo()
    print("-" * 100)
    print("trans_id", trans_id)
    print("executive_id", executive_id)
    print("executive_name", executive_name)
    print("-" * 100)
    #   #保存dealeInfo：
    photo = "car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png"
    type = "png"
    name = Unicode() + TimeNow() + GBK2312()
    saveDealerTransInfo = inter.saveDealerTransInfo(
        transDate=Now(),
        registrationFee="2",
        interestAmount="100",
        payMethod="cash",
        remark="Remark" + TimeNow(),
        type_carSalesInvoice=type,
        photo_carSalesInvoice=photo,
        name_carSalesInvoice=name,
        type_pdo=type,
        photo_pdo=photo,
        name_pdo=name,
        type_receipt=type,
        photo_receipt=photo,
        name_receipt=name,
        transId=trans_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("saveDealerTransInfo:", saveDealerTransInfo.json())
    print("-" * 100)
    assert str(saveDealerTransInfo.json()['success']) == "True"
    return trans_id, executive_id, executive_name, type, photo, name


# 15.提交dealerInfo
def test_submitDealerTransInfo():
    trans_id, executive_id, executive_name, type, photo, name = test_saveDealerTransInfo()
    submitDealerTransInfo = inter.submitDealerTransInfo(
        transDate=Now(),
        registrationFee="2",
        interestAmount="100",
        payMethod="cash",
        remark="Remark" + TimeNow(),
        type_carSalesInvoice=type,
        photo_carSalesInvoice=photo,
        name_carSalesInvoice=name,
        type_pdo=type,
        photo_pdo=photo,
        name_pdo=name,
        type_receipt=type,
        photo_receipt=photo,
        name_receipt=name,
        transId=trans_id,
        operatorId=executive_id,
        operatorName=executive_name,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("submitDealerTransInfo:", submitDealerTransInfo.json())
    print("-" * 100)
    assert str(submitDealerTransInfo.json()['success']) == "True"


# 16.取消订单
def test_cancelTrans():
    cancelTrans = inter.cancelTrans(
        id=test_assignExecutive(),
        comment="取消订单" + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("cancelTrans:", cancelTrans.json())
    print("-" * 100)
    assert str(cancelTrans.json()['success']) == "True"


# 17.订单详情
def test_orderDetail():
    orderDetail = inter.orderDetail(
        id=test_assignExecutive(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("orderDetail:", orderDetail.json())
    print("-" * 100)
    assert str(orderDetail.json()['success']) == "True"


# 18.订单历史记录
def test_historyTrans():
    historyTrans = inter.historyTrans(
        id=test_assignExecutive(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("historyTrans:", historyTrans.json())
    print("-" * 100)
    assert str(historyTrans.json()['success']) == "True"


# 19.生成线下订单
def test_createOfflineOrder():
    print("Car Number", "=" * 120)
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
    #   #获取car_Number:
    getCarListInspector = inter.getCarListInspector(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getCarListInspector:", getCarListInspector.json())
    print("-" * 100)
    car_number = str(getCarListInspector.json()['data'][0]['number'])
    print("-" * 100)
    print("car_number:", car_number)
    print("-" * 100)
    print("Car Number", "=" * 120)
    #   #创建可用dealer：
    print("Dealer", "=" * 120)
    #   #创建corporate dealer:
    email = "Dealer" + TimeNow() + "@corporate.dealer"
    contactPerson = Unicode() + GBK2312() + TimeNow()
    phonePrefix = "+86"
    phoneNumber = TimeNow()
    createCorporateDealer = inter.createCorporateDealer(
        email=email,
        contactPerson=contactPerson,
        phonePrefix=phonePrefix,
        phoneNumber=phoneNumber,
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
        email=email,
        contactPerson=contactPerson,
        companyName="Company" + TimeNow(),
        city="City" + TimeNow(),
        country="Country" + TimeNow(),
        state=TimeNow(),
        companyAddress="CompanyAddress" + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=phoneNumber,
        phonePrefix=phonePrefix,
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
    print("Dealer", "=" * 120)
    #   #获取operationAdmin以及dealerExecutive:
    executiveWithDealer = inter.executiveWithDealer(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("executiveWithDealer:", executiveWithDealer.json())
    print("-" * 100)

    def executiveWithDealerId():
        for x in executiveWithDealer.json()["data"]:
            if str(x["name"]) == "mingvtest1":
                print(x["id"], x["name"])
                executiveWithDealer_id = str(x["id"])
                return executiveWithDealer_id

    executiveWithDealer_id = str(executiveWithDealerId())
    assert str(executiveWithDealer_id) != None
    print("-" * 100)
    print("executiveWithDealer_id:", executiveWithDealer_id)
    print("-" * 100)
    #   #获取dealer列表:
    getDealerList = inter.getDealerList(
        status="active",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getDealerList:", getDealerList.json())
    print("-" * 100)
    #   #取出参数:
    car_no = car_number
    dealer_phonePrefix = str(getDealerList.json()['data'][0]['phonePrefix'])
    dealer_phoneNumber = str(getDealerList.json()['data'][0]['phoneNumber'])
    dealer_email = str(getDealerList.json()['data'][0]['email'])
    assign_id = executiveWithDealer_id
    print("-" * 100)
    print("car_no:", car_no)
    print("dealer_phonePrefix:", dealer_phonePrefix)
    print("dealer_phoneNumber:", dealer_phoneNumber)
    print("dealer_email:", dealer_email)
    print("assign_id:", assign_id)
    print("-" * 100)
    #   #生成线下订单:
    createOfflineOrder = inter.createOfflineOrder(
        id=car_no,
        phoneNumber=dealer_phoneNumber,
        phonePrefix=dealer_phonePrefix,
        email=dealer_email,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createOfflineOrder:", createOfflineOrder.json())
    print("-" * 100)
    assert str(createOfflineOrder.json()['success']) == "True"
    return car_no, assign_id


# 20.导出trans
def test_exportTrans():
    exportTrans = inter.exportTrans(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("exportTrans:", exportTrans.json())
    print("-" * 100)
    assert str(exportTrans.json()['success']) == "True"


# 21.获取检车报告信息
def test_reportViewInfo():
    car_no, assign_id = test_createOfflineOrder()
    reportViewInfo = inter.reportViewInfo(
        id=car_no,
        resourceId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("reportViewInfo:", reportViewInfo.json())
    print("-" * 100)
    assert str(reportViewInfo.json()['success']) == "True"
