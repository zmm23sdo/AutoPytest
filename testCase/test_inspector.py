import redis
from common.TestInterface import Interface
from common.TestRedis import Redis
import pytest
import json
import time
import random
import hmac, base64, struct, hashlib, time
from common.TestCommon import GetHeaders, GetHeaders2, getVerifyCodeImage, getRedis, loginTrue, SetPhone, Unicode, \
    GBK2312, TimeNow, Today, Now
from datetime import datetime

inter = Interface()


# 1.创建检车单
def test_createInspection():
    createInspection = inter.createInspection(
        carYear=1990,
        carBrand="BMW",
        carModel="1",
        applyTel=TimeNow(),
        applyTelCode="+86",
        applyName="ApplyName" + TimeNow() + Unicode(),
        applyMail="Apply" + TimeNow() + "@inspect.apply",
        carType="2",
        cardUrl="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createInspection:", createInspection.json())
    print("-" * 100)
    assert str(createInspection.json()['success']) == "True"


# 2.获取关联系统客户
def test_relatedCustomer():
    #   #创建新的检车单:
    test_createInspection()
    #   #查询待处理检车任务:
    queryNoConfirmInspections = inter.queryNoConfirmInspections(
        current="1",
        pageSize="9999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("queryNoConfirmInspections:", queryNoConfirmInspections.json())
    print("-" * 100)
    inspection_id = str(queryNoConfirmInspections.json()['data'][0]['id'])
    apply_Tel = str(queryNoConfirmInspections.json()['data'][0]['applyTel'])
    apply_TelCode = str(queryNoConfirmInspections.json()['data'][0]['applyTelCode'])
    apply_Name = str(queryNoConfirmInspections.json()['data'][0]['applyName'])
    apply_Mail = str(queryNoConfirmInspections.json()['data'][0]['applyMail'])
    print("-" * 100)
    print("inspection_id:", inspection_id)
    print("apply_Tel:", apply_Tel)
    print("apply_TelCode:", apply_TelCode)
    print("apply_Name:", apply_Name)
    print("apply_Mail:", apply_Mail)
    print("-" * 100)
    #   #根据新建的检车单创建seller，新建corp seller：
    addCorpSeller = inter.addCorpSeller(
        phoneNumber=apply_Tel,
        phonePrefix=apply_TelCode,
        email=apply_Mail,
        name=apply_Name,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addCorpSeller:", addCorpSeller.json())
    print("-" * 100)
    #   #获取关联系统客户
    relatedCustomer = inter.relatedCustomer(
        no=inspection_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("relatedCustomer:", relatedCustomer.json())
    print("-" * 100)
    assert str(relatedCustomer.json()['success']) == "True"


# 3.取消检车单
def test_cancelInspection():
    #   #创建新的检车单:
    test_createInspection()
    #   #查询待处理检车任务:
    queryNoConfirmInspections = inter.queryNoConfirmInspections(
        current="1",
        pageSize="9999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("queryNoConfirmInspections:", queryNoConfirmInspections.json())
    print("-" * 100)
    inspection_id = str(queryNoConfirmInspections.json()['data'][0]['id'])
    print("-" * 100)
    print("inspection_id:", inspection_id)
    print("-" * 100)
    #   #取消检车单:
    cancelInspection = inter.cancelInspection(
        no=inspection_id,
        comment="取消检车单" + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("cancelInspection:", cancelInspection.json())
    print("-" * 100)
    assert str(cancelInspection.json()['success']) == "True"


# 4.查询待处理检车任务
def test_queryNoConfirmInspections():
    queryNoConfirmInspections = inter.queryNoConfirmInspections(
        current="1",
        pageSize="9999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("queryNoConfirmInspections:", queryNoConfirmInspections.json())
    print("-" * 100)
    assert str(queryNoConfirmInspections.json()['success']) == "True"


# 5.获取所有检车任务安排
def test_checkerTasks():
    #   #获取今天的起止时间:
    today_start_time, today_end_time = Today()
    print(today_start_time)
    print(today_end_time)
    today_start = today_start_time.isoformat() + "Z"
    today_end = today_end_time.isoformat() + "Z"
    print("-" * 100)
    print("today_start:", today_start)
    print("today_end:", today_end)
    print("-" * 100)

    checkerTasks = inter.checkerTasks(
        checkDateA=str(today_start),
        checkDateB=str(today_end),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("checkerTasks:", checkerTasks.json())
    print("-" * 100)
    assert str(checkerTasks.json()['success']) == "True"


# 6.获取待确认检车单详情
def test_noConfirmInspectionInfo():
    #   #创建新的检车单:
    test_createInspection()
    #   #查询待处理检车任务:
    queryNoConfirmInspections = inter.queryNoConfirmInspections(
        current="1",
        pageSize="9999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("queryNoConfirmInspections:", queryNoConfirmInspections.json())
    print("-" * 100)
    inspection_id = str(queryNoConfirmInspections.json()['data'][0]['id'])
    print("-" * 100)
    print("inspection_id:", inspection_id)
    print("-" * 100)
    #   #获取待确认检车单详情:
    noConfirmInspectionInfo = inter.noConfirmInspectionInfo(
        id=inspection_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("noConfirmInspectionInfo:", noConfirmInspectionInfo.json())
    print("-" * 100)
    assert str(noConfirmInspectionInfo.json()['success']) == "True"


# 7、获取待分配检车员
def test_inspectorsWithTarget():
    inspectorsWithTarget = inter.inspectorsWithTarget(
        checkTime=Now(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("inspectorsWithTarget:", inspectorsWithTarget.json())
    print("-" * 100)
    assert str(inspectorsWithTarget.json()['success']) == "True"


# 8.确认检车单
def test_confirmInspection():
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
    assert str(confirmInspection.json()['success']) == "True"
    return inspection_id


# 9.关联seller
def test_associateSellerInspector():
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
    associateSellerInspector = inter.associateSellerInspector(
        id=inspection_id,
        customerId=customer_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("检车单关联seller:", associateSellerInspector.json())
    print("-" * 100)
    assert str(associateSellerInspector.json()['success']) == "True"


# 10.关联agent
def test_associateAgent():
    #   #创建新的检车单:
    test_createInspection()
    #   #查询待处理检车任务:
    queryNoConfirmInspections = inter.queryNoConfirmInspections(
        current="1",
        pageSize="9999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("queryNoConfirmInspections:", queryNoConfirmInspections.json())
    print("-" * 100)
    inspection_id = str(queryNoConfirmInspections.json()['data'][0]['id'])
    apply_Tel = str(queryNoConfirmInspections.json()['data'][0]['applyTel'])
    apply_TelCode = str(queryNoConfirmInspections.json()['data'][0]['applyTelCode'])
    apply_Name = str(queryNoConfirmInspections.json()['data'][0]['applyName'])
    apply_Mail = str(queryNoConfirmInspections.json()['data'][0]['applyMail'])
    print("-" * 100)
    print("inspection_id:", inspection_id)
    print("apply_Tel:", apply_Tel)
    print("apply_TelCode:", apply_TelCode)
    print("apply_Name:", apply_Name)
    print("apply_Mail:", apply_Mail)
    print("-" * 100)
    #   #根据新建的检车单创建agent，新建salesAgent：
    addSalesAgent = inter.addSalesAgent(
        phoneNumber=apply_Tel,
        phonePrefix=apply_TelCode,
        email=apply_Mail,
        name=apply_Name,
        type="NCD",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addSalesAgent:", addSalesAgent.json())
    print("-" * 100)
    #   #查询salesAgent,assignPending:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("agent_id:", agent_id)
    print("-" * 100)
    #   #获取可选分配人,mingvtest1
    getSalesAgentExecutive = inter.getSalesAgentExecutive(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getSalesAgentExecutive:", getSalesAgentExecutive.json())
    print("-" * 100)

    #   #循环取出，mingvtest1的id:
    def assignId():
        for x in getSalesAgentExecutive.json()["data"]:
            if str(x["name"]) == "mingvtest1":
                print(x["id"], x["name"], x["count"])
                assign_id = str(x["id"])
                return assign_id

    assign_id = str(assignId())
    assert str(assign_id) != None
    print("-" * 100)
    print("assign_id:", assign_id)
    print("-" * 100)
    #   #分配salesAgent,mingvtest1:
    assignSalesAgent = inter.assignSalesAgent(
        resourceId=agent_id,
        id=agent_id,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSalesAgent:", assignSalesAgent.json())
    print("-" * 100)
    #   #提交审核（除Individual broker）
    submitSalesAgentInfo = inter.submitSalesAgentInfo(
        resourceId=agent_id,
        id=agent_id,
        email=apply_Mail,
        name=apply_Name,
        companyName="Company" + GBK2312() + TimeNow(),
        city="City" + GBK2312() + TimeNow(),
        country="Country" + GBK2312() + TimeNow(),
        state=TimeNow(),
        companyAddress="CompanyAddress" + GBK2312() + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=apply_Tel,
        phonePrefix=apply_TelCode,
        corpCardname="截图20210316142730.png",
        corpCardphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        corpCardtype="png",
        remarks="Remarks" + TimeNow(),
        postcode=TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("submitSalesAgentInfo:", submitSalesAgentInfo.json())
    print("-" * 100)
    #   #审核成功:
    auditSuccessSa = inter.auditSuccessSa(
        resourceId=agent_id,
        id=agent_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditSuccessSa:", auditSuccessSa.json())
    print("-" * 100)
    #   #关联agent:
    associateAgent = inter.associateAgent(
        id=inspection_id,
        customerId=agent_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("associateAgent:", associateAgent.json())
    print("-" * 100)
    assert str(associateAgent.json()['success']) == "True"


# 11.查询审核未完成
def test_queryCheckedInspection():
    queryCheckedInspection = inter.queryCheckedInspection(
        current="1",
        pageSize="9999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("queryCheckedInspection:", queryCheckedInspection.json())
    print("-" * 100)
    assert str(queryCheckedInspection.json()['success']) == "True"


# 12.查询已完成
def test_queryFinishedInspection():
    queryFinishedInspection = inter.queryFinishedInspection(
        current="1",
        pageSize="9999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("queryFinishedInspection:", queryFinishedInspection.json())
    print("-" * 100)
    assert str(queryFinishedInspection.json()['success']) == "True"


# 13.审核详情
def test_auditInspectionInfo():
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
    assert str(auditInspectionInfo.json()['success']) == "True"
    return inspection_id


# 14.已完成检车单详情
def test_finishedInspectionInfo():
    #   #查询已完成的检车单:
    queryFinishedInspection = inter.queryFinishedInspection(
        current="1",
        pageSize="9999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("queryFinishedInspection:", queryFinishedInspection.json())
    print("-" * 100)
    finished_inspection_id = str(queryFinishedInspection.json()['data'][0]['id'])
    print("-" * 100)
    print("finished_inspection_id:", finished_inspection_id)
    print("-" * 100)
    #   #已完成检车单详情:
    finishedInspectionInfo = inter.finishedInspectionInfo(
        id=finished_inspection_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("finishedInspectionInfo:", finishedInspectionInfo.json())
    print("-" * 100)
    assert str(finishedInspectionInfo.json()['success']) == "True"


# 15.审核成功
def test_auditSuccessInspector():
    auditSuccessInspector = inter.auditSuccessInspector(
        no=test_auditInspectionInfo(),
        comment="审核成功" + TimeNow(),
        price="9999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditSuccessInspector:", auditSuccessInspector.json())
    print("-" * 100)
    assert str(auditSuccessInspector.json()['success']) == "True"
    return auditSuccessInspector.json()


# 16.审核失败
def test_auditFailInspector():
    auditFailInspector = inter.auditFailInspector(
        id=test_auditInspectionInfo(),
        comment="审核失败" + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditFailInspector:", auditFailInspector.json())
    print("-" * 100)
    assert str(auditFailInspector.json()['success']) == "True"


# 17.审核退回
def test_auditReviseInspector():
    auditReviseInspector = inter.auditReviseInspector(
        no=test_auditInspectionInfo(),
        comment="审核退回" + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditReviseInspector:", auditReviseInspector.json())
    print("-" * 100)
    assert str(auditReviseInspector.json()['success']) == "True"


# 18.上传结果
def test_uploadResultInspector():
    uploadResultInspector = inter.uploadResultInspector(
        photo="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("uploadResultInspector:", uploadResultInspector.json())
    print("-" * 100)
    assert str(uploadResultInspector.json()['success']) == "True"


# 19.取消关联
def test_disassociateInspector():
    #   #创建新的检车单：
    carYear = 1993
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

    #   #取消关联
    disassociateInspector = inter.disassociateInspector(
        id=inspection_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("disassociateInspector:", disassociateInspector.json())
    print("-" * 100)
    assert str(disassociateInspector.json()['success']) == "True"


# 20.获取已确认检车单列表
def test_queryConfirmedInspection():
    queryConfirmedInspection = inter.queryConfirmedInspection(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("queryConfirmedInspection:", queryConfirmedInspection.json())
    print("-" * 100)
    assert str(queryConfirmedInspection.json()['success']) == "True"


# 21.获取已确认检车单详情
def test_getConfirmedInspectionInfo():
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
    print("-" * 100)
    print("确认检车单返回：", confirmInspection.json())
    print("-" * 100)
    #   #获取已确认检车单详情:
    getConfirmedInspectionInfo = inter.getConfirmedInspectionInfo(
        id=inspection_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getConfirmedInspectionInfo:", getConfirmedInspectionInfo.json())
    print("-" * 100)
    assert str(getConfirmedInspectionInfo.json()['success']) == "True"
    reports_id = str(getConfirmedInspectionInfo.json()['data']['reports'][0]['id'])
    return inspection_id, reports_id


# 22.获取检车报告车辆信息
def test_getCarInfoInspector():
    #   #获取检车单id,检车报告id:
    inspection_id, reports_id = test_getConfirmedInspectionInfo()
    print("-" * 100)
    print("inspection_id", inspection_id)
    print("reports_id", reports_id)
    print("-" * 100)
    #   #获取检车报告车辆信息:
    getCarInfoInspector = inter.getCarInfoInspector(
        id=reports_id,
        resourceId=inspection_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getCarInfoInspector:", getCarInfoInspector.json())
    print("-" * 100)
    assert str(getCarInfoInspector.json()['success']) == "True"


# 23.获取检车报告车辆照片
def test_getCarPhotoInspector():
    #   #获取检车单id,检车报告id:
    inspection_id, reports_id = test_getConfirmedInspectionInfo()
    print("-" * 100)
    print("inspection_id", inspection_id)
    print("reports_id", reports_id)
    print("-" * 100)
    #   #获取检车报告车辆照片
    getCarPhotoInspector = inter.getCarPhotoInspector(
        id=reports_id,
        resourceId=inspection_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getCarPhotoInspector:", getCarPhotoInspector.json())
    print("-" * 100)
    assert str(getCarPhotoInspector.json()['success']) == "True"


# 24.获取检车报告车辆损伤照片
def test_getCarDamagePhotoInspector():
    #   #获取检车单id,检车报告id:
    inspection_id, reports_id = test_getConfirmedInspectionInfo()
    print("-" * 100)
    print("inspection_id", inspection_id)
    print("reports_id", reports_id)
    print("-" * 100)
    #   #获取检车报告车辆照片
    getCarDamagePhotoInspector = inter.getCarDamagePhotoInspector(
        id=reports_id,
        resourceId=inspection_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getCarDamagePhotoInspector:", getCarDamagePhotoInspector.json())
    print("-" * 100)
    assert str(getCarDamagePhotoInspector.json()['success']) == "True"


# 25.获取检车任务列表
def test_getCheckerTaskList():
    getCheckerTaskList = inter.getCheckerTaskList(
        startTime=Now(),
        endTime=Now(),
        headers=GetHeaders2()
    )
    print("-" * 100)
    print("getCheckerTaskList:", getCheckerTaskList.json())
    print("-" * 100)
    assert str(getCheckerTaskList.json()['success']) == "True"


# 26.编辑车辆损伤信息
def test_editCarDamageInfoInspector():
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
    editCarDamageInfoInspector = inter.editCarDamageInfoInspector(
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
    print("-" * 100)
    print("editCarDamageInfoInspector:", editCarDamageInfoInspector.json())
    print("-" * 100)
    assert str(editCarDamageInfoInspector.json()['success']) == "True"


# 27.提交检车任务
def test_submitCheckerTask():
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
    print("-" * 100)
    print("submitCheckerTask:", submitCheckerTask.json())
    print("-" * 100)
    assert str(submitCheckerTask.json()['success']) == "True"
    return inspection_id, appHeaders


# 28.取消检车任务
def test_cancelCheckerTask():
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
    #   #取消检车任务:
    cancelCheckerTask = inter.cancelCheckerTask(
        id=inspection_id,
        cancelReason="取消检车任务" + TimeNow(),
        remarks="Remark" + TimeNow(),
        headers=appHeaders
    )
    print("-" * 100)
    print("cancelCheckerTask:", cancelCheckerTask.json())
    print("-" * 100)
    assert str(cancelCheckerTask.json()['success']) == "True"


# 29。编辑车辆信息
def test_editCarInfoInspector():
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
    editCarInfoInspector = inter.editCarInfoInspector(
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
    print("-" * 100)
    print("editCarInfoInspector", editCarInfoInspector.json())
    print("-" * 100)
    assert str(editCarInfoInspector.json()['success']) == "True"
    return inspection_id, appHeaders


# 30.获取检车报告信息
def test_getInspectionReport():
    inspection_id, appHeaders = test_editCarInfoInspector()
    getInspectionReport = inter.getInspectionReport(
        id=inspection_id,
        headers=appHeaders
    )
    print("-" * 100)
    print("getInspectionReport", getInspectionReport.json())
    print("-" * 100)
    assert str(getInspectionReport.json()['success']) == "True"


# 31.退出审核
def test_quitAudit():
    inspection_id = test_auditInspectionInfo()
    print(inspection_id)
    quitAudit = inter.quitAudit(
        id=inspection_id,
        resourceId=inspection_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("quitAudit", quitAudit.json())
    print("-" * 100)
    assert str(quitAudit.json()['success']) == "True"


# 32.检查检车员时间
def test_checkInspectionTime():
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
    #   #检查检车员时间:
    checkInspectionTime = inter.checkInspectionTime(
        checkTime=Now(),
        checkerId=check_id,
        resourceId=check_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("checkInspectionTime", checkInspectionTime.json())
    print("-" * 100)
    assert str(checkInspectionTime.json()['success']) == "True"


# 33.回退检车单
def test_backInspection():
    backInspection = inter.backInspection(
        id=test_confirmInspection(),
        comment="回退检车单" + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("backInspection:", backInspection.json())
    print("-" * 100)
    assert str(backInspection.json()['success']) == "True"
