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


# 1.新建salesAgent
def test_addSalesAgent():
    addSalesAgent = inter.addSalesAgent(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        type="NCD",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addSalesAgent:", addSalesAgent.json())
    print("-" * 100)
    assert str(addSalesAgent.json()['success']) == "True"


# 2.查询salesAgent
def test_querySalesAgent():
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    assert str(querySalesAgent.json()['success']) == "True"


# 3.冻结salesAgent
def test_freezeSalesAgent():
    #   新建salesAgent
    addSalesAgent = inter.addSalesAgent(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        type="UCD",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addSalesAgent:", addSalesAgent.json())
    print("-" * 100)
    #   #查询salesAgent,assignPending:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="assignPending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    assignPending_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("assignPendingagent_id:", assignPending_agent_id)
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSalesAgent:", assignSalesAgent.json())
    print("-" * 100)
    #   #提交审核（除Individual broker）
    submitSalesAgentInfo = inter.submitSalesAgentInfo(
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        companyName="Company" + GBK2312() + TimeNow(),
        city="City" + GBK2312() + TimeNow(),
        country="Country" + GBK2312() + TimeNow(),
        state=TimeNow(),
        companyAddress="CompanyAddress" + GBK2312() + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=TimeNow(),
        phonePrefix="+86",
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditSuccessSa:", auditSuccessSa.json())
    print("-" * 100)
    #   #查询salesAgent,active:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="active",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    active_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("active_agent_id:", active_agent_id)
    print("-" * 100)
    #   #冻结salesAgent:
    freezeSalesAgent = inter.freezeSalesAgent(
        resourceId=active_agent_id,
        id=active_agent_id,
        comment="冻结salesAgent" + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("freezeSalesAgent:", freezeSalesAgent.json())
    print("-" * 100)
    assert str(freezeSalesAgent.json()['success']) == "True"


# 4.解冻salesAgent
def test_unfreezeSalesAgent():
    test_freezeSalesAgent()  # 冻结一个新的agent
    #   #查询salesAgent,frozen:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="frozen",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    frozen_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("frozen_agent_id:", frozen_agent_id)
    print("-" * 100)
    #   #解冻salesAgent
    unfreezeSalesAgent = inter.unfreezeSalesAgent(
        resourceId=frozen_agent_id,
        id=frozen_agent_id,
        comment="解冻salesAgent" + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("unfreezeSalesAgent:", unfreezeSalesAgent.json())
    print("-" * 100)
    assert str(unfreezeSalesAgent.json()['success']) == "True"


# 5.注销salesAgent
def test_closeSalesAgent():
    #   新建salesAgent
    addSalesAgent = inter.addSalesAgent(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        type="UCD",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addSalesAgent:", addSalesAgent.json())
    print("-" * 100)
    #   #查询salesAgent,assignPending:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="assignPending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    assignPending_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("assignPendingagent_id:", assignPending_agent_id)
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSalesAgent:", assignSalesAgent.json())
    print("-" * 100)
    #   #提交审核（除Individual broker）
    submitSalesAgentInfo = inter.submitSalesAgentInfo(
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        companyName="Company" + GBK2312() + TimeNow(),
        city="City" + GBK2312() + TimeNow(),
        country="Country" + GBK2312() + TimeNow(),
        state=TimeNow(),
        companyAddress="CompanyAddress" + GBK2312() + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=TimeNow(),
        phonePrefix="+86",
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditSuccessSa:", auditSuccessSa.json())
    print("-" * 100)
    #   #查询salesAgent,active:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="active",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    active_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("active_agent_id:", active_agent_id)
    print("-" * 100)
    #   #注销salesAgent
    closeSalesAgent = inter.closeSalesAgent(
        resourceId=active_agent_id,
        id=active_agent_id,
        comment="注销salesAgent" + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("closeSalesAgent:", closeSalesAgent.json())
    print("-" * 100)
    assert str(closeSalesAgent.json()['success']) == "True"


# 6.获取可选分配人
def test_getSalesAgentExecutive():
    getSalesAgentExecutive = inter.getSalesAgentExecutive(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getSalesAgentExecutive:", getSalesAgentExecutive.json())
    print("-" * 100)
    assert str(getSalesAgentExecutive.json()['success']) == "True"


# 7.分配salesAgent
def test_assignSalesAgent():
    #   新建salesAgent
    addSalesAgent = inter.addSalesAgent(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        type="UCD",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addSalesAgent:", addSalesAgent.json())
    print("-" * 100)
    #   #查询salesAgent,assignPending:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="assignPending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    assignPending_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("assignPendingagent_id:", assignPending_agent_id)
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSalesAgent:", assignSalesAgent.json())
    print("-" * 100)
    assert str(assignSalesAgent.json()['success']) == "True"


# 8.获取子账号列表
def test_getSalesAgentSubsidiary():
    #   #新建salesAgent
    addSalesAgent = inter.addSalesAgent(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        type="UCD",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addSalesAgent:", addSalesAgent.json())
    print("-" * 100)
    #   #查询salesAgent,assignPending:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="assignPending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    assignPending_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("assignPendingagent_id:", assignPending_agent_id)
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSalesAgent:", assignSalesAgent.json())
    print("-" * 100)
    #   #提交审核（除Individual broker）
    submitSalesAgentInfo = inter.submitSalesAgentInfo(
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        companyName="Company" + GBK2312() + TimeNow(),
        city="City" + GBK2312() + TimeNow(),
        country="Country" + GBK2312() + TimeNow(),
        state=TimeNow(),
        companyAddress="CompanyAddress" + GBK2312() + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=TimeNow(),
        phonePrefix="+86",
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditSuccessSa:", auditSuccessSa.json())
    print("-" * 100)
    #   #查询salesAgent,active:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="active",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    active_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("active_agent_id:", active_agent_id)
    print("-" * 100)
    #   #创建子账号:
    createSalesAgentSubsidiary = inter.createSalesAgentSubsidiary(
        resourceId=active_agent_id,
        id=active_agent_id,
        email="SalesAgentSubsidiary" + TimeNow() + "@susidiary.sales",
        phonePrefix="+60",
        phoneNumber=TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createSalesAgentSubsidiary:", createSalesAgentSubsidiary.json())
    print("-" * 100)
    #   #获取子账号列表:
    getSalesAgentSubsidiary = inter.getSalesAgentSubsidiary(
        resourceId=active_agent_id,
        id=active_agent_id,
        pageSize="9999",
        current="1",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getSalesAgentSubsidiary:", getSalesAgentSubsidiary.json())
    print("-" * 100)
    assert str(getSalesAgentSubsidiary.json()['success']) == "True"


# 10.查看salesAgent信息
def test_salesAgentInfo():
    #   #查询salesAgent,agent_id:
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
    salesAgentInfo = inter.salesAgentInfo(
        resourceId=agent_id,
        id=agent_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("salesAgentInfo:", salesAgentInfo.json())
    print("-" * 100)
    assert str(salesAgentInfo.json()['success']) == "True"


# 11.提交审核（除Individual broker）
def test_submitSalesAgentInfo():
    #   新建salesAgent:
    addSalesAgent = inter.addSalesAgent(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        type="UCD",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addSalesAgent:", addSalesAgent.json())
    print("-" * 100)
    #   #查询salesAgent,assignPending:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="assignPending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    assignPending_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("assignPendingagent_id:", assignPending_agent_id)
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSalesAgent:", assignSalesAgent.json())
    print("-" * 100)
    #   #提交审核（除Individual broker）
    submitSalesAgentInfo = inter.submitSalesAgentInfo(
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        companyName="Company" + GBK2312() + TimeNow(),
        city="City" + GBK2312() + TimeNow(),
        country="Country" + GBK2312() + TimeNow(),
        state=TimeNow(),
        companyAddress="CompanyAddress" + GBK2312() + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=TimeNow(),
        phonePrefix="+86",
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
    assert str(submitSalesAgentInfo.json()['success']) == "True"


# 12.创建子账号
def test_createSalesAgentSubsidiary():
    #   #新建salesAgent
    addSalesAgent = inter.addSalesAgent(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        type="UCD",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addSalesAgent:", addSalesAgent.json())
    print("-" * 100)
    #   #查询salesAgent,assignPending:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="assignPending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    assignPending_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("assignPendingagent_id:", assignPending_agent_id)
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSalesAgent:", assignSalesAgent.json())
    print("-" * 100)
    #   #提交审核（除Individual broker）
    submitSalesAgentInfo = inter.submitSalesAgentInfo(
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        companyName="Company" + GBK2312() + TimeNow(),
        city="City" + GBK2312() + TimeNow(),
        country="Country" + GBK2312() + TimeNow(),
        state=TimeNow(),
        companyAddress="CompanyAddress" + GBK2312() + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=TimeNow(),
        phonePrefix="+86",
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditSuccessSa:", auditSuccessSa.json())
    print("-" * 100)
    #   #查询salesAgent,active:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="active",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    active_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("active_agent_id:", active_agent_id)
    print("-" * 100)
    #   #创建子账号:
    createSalesAgentSubsidiary = inter.createSalesAgentSubsidiary(
        resourceId=active_agent_id,
        id=active_agent_id,
        email="SalesAgentSubsidiary" + TimeNow() + "@susidiary.sales",
        phonePrefix="+60",
        phoneNumber=TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createSalesAgentSubsidiary:", createSalesAgentSubsidiary.json())
    print("-" * 100)
    assert str(createSalesAgentSubsidiary.json()['success']) == "True"


# 13.关闭子账号
def test_closeSalesAgentSubsidiary():
    #   #新建salesAgent
    addSalesAgent = inter.addSalesAgent(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        type="UCD",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addSalesAgent:", addSalesAgent.json())
    print("-" * 100)
    #   #查询salesAgent,assignPending:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="assignPending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    assignPending_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("assignPendingagent_id:", assignPending_agent_id)
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSalesAgent:", assignSalesAgent.json())
    print("-" * 100)
    #   #提交审核（除Individual broker）
    submitSalesAgentInfo = inter.submitSalesAgentInfo(
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        companyName="Company" + GBK2312() + TimeNow(),
        city="City" + GBK2312() + TimeNow(),
        country="Country" + GBK2312() + TimeNow(),
        state=TimeNow(),
        companyAddress="CompanyAddress" + GBK2312() + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=TimeNow(),
        phonePrefix="+86",
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditSuccessSa:", auditSuccessSa.json())
    print("-" * 100)
    #   #查询salesAgent,active:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="active",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    active_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("active_agent_id:", active_agent_id)
    print("-" * 100)
    #   #创建子账号:
    createSalesAgentSubsidiary = inter.createSalesAgentSubsidiary(
        resourceId=active_agent_id,
        id=active_agent_id,
        email="SalesAgentSubsidiary" + TimeNow() + "@susidiary.sales",
        phonePrefix="+60",
        phoneNumber=TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createSalesAgentSubsidiary:", createSalesAgentSubsidiary.json())
    print("-" * 100)
    #   #获取子账号列表:
    getSalesAgentSubsidiary = inter.getSalesAgentSubsidiary(
        resourceId=active_agent_id,
        id=active_agent_id,
        pageSize="9999",
        current="1",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getSalesAgentSubsidiary:", getSalesAgentSubsidiary.json())
    print("-" * 100)
    subsidiary_agent_id = str(getSalesAgentSubsidiary.json()['data'][0]['id'])
    print("-" * 100)
    print("subsidiary_agent_id:", subsidiary_agent_id)
    print("-" * 100)
    #   #关闭子账号
    closeSalesAgentSubsidiary = inter.closeSalesAgentSubsidiary(
        resourceId=active_agent_id,
        id=subsidiary_agent_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("closeSalesAgentSubsidiary:", closeSalesAgentSubsidiary.json())
    print("-" * 100)
    assert str(closeSalesAgentSubsidiary.json()['success']) == "True"


# 14.审核页面
def test_auditAgentInfo():
    #   #新建salesAgent
    addSalesAgent = inter.addSalesAgent(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        type="UCD",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addSalesAgent:", addSalesAgent.json())
    print("-" * 100)
    #   #查询salesAgent,assignPending:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="assignPending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    assignPending_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("assignPendingagent_id:", assignPending_agent_id)
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSalesAgent:", assignSalesAgent.json())
    print("-" * 100)
    #   #提交审核（除Individual broker）
    submitSalesAgentInfo = inter.submitSalesAgentInfo(
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        companyName="Company" + GBK2312() + TimeNow(),
        city="City" + GBK2312() + TimeNow(),
        country="Country" + GBK2312() + TimeNow(),
        state=TimeNow(),
        companyAddress="CompanyAddress" + GBK2312() + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=TimeNow(),
        phonePrefix="+86",
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
    #   #审核页面:
    auditAgentInfo = inter.auditAgentInfo(
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        pageSize="9999",
        current="1",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditAgentInfo:", auditAgentInfo.json())
    print("-" * 100)
    assert str(auditAgentInfo.json()['success']) == "True"


# 15.审核成功
def test_auditSuccessSa():
    #   #新建salesAgent
    addSalesAgent = inter.addSalesAgent(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        type="UCD",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addSalesAgent:", addSalesAgent.json())
    print("-" * 100)
    #   #查询salesAgent,assignPending:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="assignPending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    assignPending_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("assignPendingagent_id:", assignPending_agent_id)
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSalesAgent:", assignSalesAgent.json())
    print("-" * 100)
    #   #提交审核（除Individual broker）
    submitSalesAgentInfo = inter.submitSalesAgentInfo(
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        companyName="Company" + GBK2312() + TimeNow(),
        city="City" + GBK2312() + TimeNow(),
        country="Country" + GBK2312() + TimeNow(),
        state=TimeNow(),
        companyAddress="CompanyAddress" + GBK2312() + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=TimeNow(),
        phonePrefix="+86",
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditSuccessSa:", auditSuccessSa.json())
    print("-" * 100)
    assert str(auditSuccessSa.json()['success']) == "True"


# 16.审核失败
def test_auditFailSa():
    #   #新建salesAgent
    addSalesAgent = inter.addSalesAgent(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        type="UCD",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addSalesAgent:", addSalesAgent.json())
    print("-" * 100)
    #   #查询salesAgent,assignPending:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="assignPending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    assignPending_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("assignPendingagent_id:", assignPending_agent_id)
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSalesAgent:", assignSalesAgent.json())
    print("-" * 100)
    #   #提交审核（除Individual broker）
    submitSalesAgentInfo = inter.submitSalesAgentInfo(
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        companyName="Company" + GBK2312() + TimeNow(),
        city="City" + GBK2312() + TimeNow(),
        country="Country" + GBK2312() + TimeNow(),
        state=TimeNow(),
        companyAddress="CompanyAddress" + GBK2312() + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=TimeNow(),
        phonePrefix="+86",
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
    #   #审核失败
    auditFailSa = inter.auditFailSa(
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        comment="审核失败" + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditFailSa:", auditFailSa.json())
    print("-" * 100)
    assert str(auditFailSa.json()['success']) == "True"


# 16.审核退回
def test_auditReviseSa():
    #   #新建salesAgent
    addSalesAgent = inter.addSalesAgent(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        type="UCD",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addSalesAgent:", addSalesAgent.json())
    print("-" * 100)
    #   #查询salesAgent,assignPending:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="assignPending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    assignPending_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("assignPendingagent_id:", assignPending_agent_id)
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSalesAgent:", assignSalesAgent.json())
    print("-" * 100)
    #   #提交审核（除Individual broker）
    submitSalesAgentInfo = inter.submitSalesAgentInfo(
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        companyName="Company" + GBK2312() + TimeNow(),
        city="City" + GBK2312() + TimeNow(),
        country="Country" + GBK2312() + TimeNow(),
        state=TimeNow(),
        companyAddress="CompanyAddress" + GBK2312() + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=TimeNow(),
        phonePrefix="+86",
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
    #   #审核退回
    auditReviseSa = inter.auditReviseSa(
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        comment="审核退回" + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("auditReviseSa:", auditReviseSa.json())
    print("-" * 100)
    assert str(auditReviseSa.json()['success']) == "True"


# 17.账号历史
def test_agentAccountHistory():
    #   #查询salesAgent:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    salesagent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("salesagent_id:", salesagent_id)
    print("-" * 100)
    #   #账号历史
    agentAccountHistory = inter.agentAccountHistory(
        resourceId=salesagent_id,
        id=salesagent_id,
        comment="账号历史" + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("agentAccountHistory:", agentAccountHistory.json())
    print("-" * 100)
    assert str(agentAccountHistory.json()['success']) == "True"


# 18.提交individual broker审核
def test_submitIndividualBrokerInfo():
    #   #新建salesAgent,individual broker:
    addSalesAgent = inter.addSalesAgent(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        type="INDIVIDUAL_BROKER",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addSalesAgent:", addSalesAgent.json())
    print("-" * 100)
    #   #查询salesAgent,assignPending:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="assignPending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    assignPending_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("assignPendingagent_id:", assignPending_agent_id)
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSalesAgent:", assignSalesAgent.json())
    print("-" * 100)
    #   #提交individual broker审核
    submitIndividualBrokerInfo = inter.submitIndividualBrokerInfo(
        email="IndividualBroker" + TimeNow() + "@individual.broker",
        name="IndividualBroker" + GBK2312() + TimeNow(),
        remarks="Remark" + TimeNow(),
        corpCardname="CorpCardname" + Unicode() + TimeNow(),
        corpCardurl="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        id=assignPending_agent_id,
        resourceId=assignPending_agent_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("submitIndividualBrokerInfo:", submitIndividualBrokerInfo.json())
    print("-" * 100)
    assert str(submitIndividualBrokerInfo.json()['success']) == "True"


# 19.保存editInfo
def test_saveEditInfoSa():
    #   #新建salesAgent
    addSalesAgent = inter.addSalesAgent(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        type="UCD",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("addSalesAgent:", addSalesAgent.json())
    print("-" * 100)
    #   #查询salesAgent,assignPending:
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="9999",
        status="assignPending",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    assignPending_agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("assignPendingagent_id:", assignPending_agent_id)
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
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        assignId=assign_id,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignSalesAgent:", assignSalesAgent.json())
    print("-" * 100)
    #   #保存editInfo:
    saveEditInfoSa = inter.saveEditInfoSa(
        resourceId=assignPending_agent_id,
        id=assignPending_agent_id,
        email="SalesAgent" + TimeNow() + "@sales.agent",
        name="SalesAgent" + Unicode() + TimeNow(),
        companyName="Company" + GBK2312() + TimeNow(),
        city="City" + GBK2312() + TimeNow(),
        country="Country" + GBK2312() + TimeNow(),
        state=TimeNow(),
        companyAddress="CompanyAddress" + GBK2312() + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        corpSsmname="截图20210316142730.png",
        corpSsmphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        corpCardname="截图20210316142730.png",
        corpCardphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        corpDocname="截图20210316142730.png",
        corpDocphoto="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        remarks="Remarks" + TimeNow(),
        postcode=TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("saveEditInfoSa:", saveEditInfoSa.json())
    print("-" * 100)
    assert str(saveEditInfoSa.json()['success']) == "True"


# 20.sa check email
def test_checkEmailSa():
    checkEmailSa = inter.checkEmailSa(
        email="checkEmailSa" + TimeNow() + "@sa.agent",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("checkEmailSa:", checkEmailSa.json())
    print("-" * 100)
    assert str(checkEmailSa.json()['success']) == "True"


# 21.上传图片成功
def test_uploadResultSa():
    uploadResultSa = inter.uploadResultSa(
        photo="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("uploadResultSa:", uploadResultSa.json())
    print("-" * 100)
    assert str(uploadResultSa.json()['success']) == "True"
