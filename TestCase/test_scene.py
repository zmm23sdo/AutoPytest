import redis
from common.TestInterface import Interface
from common.TestRedis import Redis
import pytest
import json
import time
import random
import hmac, base64, struct, hashlib, time
from common.TestCommon import GetHeaders, Now, getVerifyCodeImage, getRedis, loginTrue, SetPhone, Unicode, GBK2312, \
    TimeNow, Today
from datetime import datetime

inter = Interface()


def test_Seller():
    ##  设置Seller基础信息:
    seller_name = "Seller" + TimeNow()
    seller_email = seller_name + "@qacehi.to"
    seller_phonePrefix = "+86"
    seller_phoneNumber = TimeNow()
    ##  addCorpSeller
    addCorpSeller = inter.addCorpSeller(
        phoneNumber=seller_phoneNumber,
        phonePrefix=seller_phonePrefix,
        email=seller_email,
        name="Seller" + TimeNow(),
        headers=GetHeaders()
    )
    print("addCorpSeller", addCorpSeller.json())
    ##  querySellerAccount
    querySellerAccount = inter.querySellerAccount(
        pageSize="999",
        current="1",
        status="assignPending",
        headers=GetHeaders()
    )
    # print("querySellerAccount",querySellerAccount.json())
    seller_id = str(querySellerAccount.json()['data'][0]['id'])
    seller_name = str(querySellerAccount.json()['data'][0]['name'])
    seller_email = str(querySellerAccount.json()['data'][0]['email'])
    seller_phoneNumber = str(querySellerAccount.json()['data'][0]['phoneNumber'])
    seller_phonePrefix = str(querySellerAccount.json()['data'][0]['phonePrefix'])
    seller_status = str(querySellerAccount.json()['data'][0]['status'])
    print("seller_id", seller_id)
    print("seller_name", seller_name)
    print("seller_email", seller_email)
    print("seller_phoneNumber", seller_phoneNumber)
    print("seller_phonePrefix", seller_phonePrefix)
    print("seller_status", seller_status)
    ##  getSellerExecutive
    getSellerExecutiveId = inter.getSellerExecutiveId(
        id=seller_id,
        headers=GetHeaders()
    )

    # print("getSellerExecutiveId",getSellerExecutiveId.json())
    ##  循环
    def getFrom():
        for x in getSellerExecutiveId.json()['data']:
            if str(x['name']) == "mingvtest1":
                print(x['id'], x['name'], x['count'])
                exe_id = str(x['id'])
                exe_name = str(x['name'])
                exe_count = str(x['count'])
                return exe_id, exe_name, exe_count

    exe_id, exe_name, exe_count = getFrom()
    print("exe_id", exe_id)
    print("exe_name", exe_name)
    print("exe_count", exe_count)

    ##  assignSeller
    assignSeller = inter.assignSeller(
        id=seller_id,
        assignId=exe_id,
        resourceId=seller_id,
        headers=GetHeaders()
    )
    print("assignSeller", assignSeller.json())
    ##  uploadResultSeller
    photo = "car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png"
    uploadResultSeller = inter.uploadResultSeller(
        photo=photo,
        headers=GetHeaders()
    )
    print("uploadResultSeller", uploadResultSeller.json())
    ##  submitCorpSellerInfo
    submitCorpSellerInfo = inter.submitCorpSellerInfo(
        id=seller_id,
        email=seller_email,
        name=seller_name,
        companyName="Company" + seller_name,
        city="City" + TimeNow(),
        country="Country" + TimeNow(),
        state="21315",
        companyAddress="companyAddress" + TimeNow(),
        registrationNumber="0123" + TimeNow(),
        phoneNumber=seller_phoneNumber,
        phonePrefix=seller_phonePrefix,
        corpSsmname="截图20210316142730.png",
        corpSsmphoto=photo,
        corpCardname="截图20210316142730.png",
        corpCardphoto=photo,
        corpDocname="截图20210316142730.png",
        corpDocphoto=photo,
        remarks="Remark",
        postcode="21312d",
        resourceId=seller_id,
        headers=GetHeaders()
    )
    print("submitCorpSellerInfo", submitCorpSellerInfo.json())
    ##  auditSuccessSeller
    auditSuccessSeller = inter.auditSuccessSeller(
        resourceId=seller_id,
        id=seller_id,
        headers=GetHeaders()
    )
    print("auditSuccessSeller", auditSuccessSeller.json())

    ## 验证账户激活
    ##  querySellerAccount
    querySellerAccount = inter.querySellerAccount(
        pageSize="999",
        current="1",
        status="",
        headers=GetHeaders()
    )
    # print("querySellerAccount",querySellerAccount.json())
    ## 循环

    for x in querySellerAccount.json()['data']:
        if str(x['id']) == str(seller_id):
            print(x['id'], x['name'], x['email'], x['phoneNumber'], x['phoneNumber'], x['status'])
            seller_id = str(x['id'])
            seller_name = str(x['name'])
            seller_email = str(x['email'])
            seller_phoneNumber = str(x['phoneNumber'])
            seller_phonePrefix = str(x['phonePrefix'])
            seller_status = str(x['status'])

    print("seller_id", seller_id)
    print("seller_name", seller_name)
    print("seller_email", seller_email)
    print("seller_phoneNumber", seller_phoneNumber)
    print("seller_phonePrefix", seller_phonePrefix)
    print("seller_status", seller_status)
    assert str(seller_status) == "active"


def test_Agent():
    ##  addSalesAgent
    agent_phoneNumber = TimeNow()
    agent_phonePrefix = "+86"
    agent_name = "Ag" + TimeNow()
    agent_email = agent_name + "@agent.fo"
    agent_type = "NCD"
    addSalesAgent = inter.addSalesAgent(
        phoneNumber=agent_phoneNumber,
        phonePrefix=agent_phonePrefix,
        email=agent_email,
        name=agent_name,
        type=agent_type,
        headers=GetHeaders()
    )
    print("addSalesAgent", addSalesAgent.json())
    ##  querySalesAgent
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="999",
        status="assignPending",
        headers=GetHeaders()
    )
    # print("querySalesAgent",querySalesAgent.json())
    agent_id = str(querySalesAgent.json()['data'][0]['id'])
    agent_name = str(querySalesAgent.json()['data'][0]['name'])
    agent_phoneNumber = str(querySalesAgent.json()['data'][0]['phoneNumber'])
    agent_status = str(querySalesAgent.json()['data'][0]['status'])
    agent_email = str(querySalesAgent.json()['data'][0]['email'])
    print("agent_id", agent_id)
    print("agent_name", agent_name)
    print("agent_phoneNumber", agent_phoneNumber)
    print("agent_status", agent_status)
    print("agent_email", agent_email)

    ##  getSalesAgentExecutive

    ##  循环
    def getFrom():
        getSalesAgentExecutive = inter.getSalesAgentExecutive(
            headers=GetHeaders()
        )
        # print("getSalesAgentExecutive",getSalesAgentExecutive.json())
        for x in getSalesAgentExecutive.json()['data']:
            if str(x['name']) == "mingvtest1":
                print(x['id'], x['name'], x['count'])
                exe_id = str(x['id'])
                exe_name = str(x['name'])
                return exe_id, exe_name

    exe_id, exe_name = getFrom()
    print("exe_id", exe_id)
    print("exe_name", exe_name)
    ##  assignSalesAgent
    assignSalesAgent = inter.assignSalesAgent(
        resourceId=agent_id,
        id=agent_id,
        assignId=exe_id,
        headers=GetHeaders()
    )
    print("assignSalesAgent", assignSalesAgent.json())
    ##  uploadResultSeller
    photo = "car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png"
    uploadResultSa = inter.uploadResultSa(
        photo=photo,
        headers=GetHeaders()
    )
    print("uploadResultSa", uploadResultSa.json())
    ##  submitSalesAgentInfo
    submitSalesAgentInfo = inter.submitSalesAgentInfo(
        id=agent_id,
        email=agent_email,
        name=agent_name,
        companyName="Company" + agent_name,
        city="City" + TimeNow(),
        country="Country" + TimeNow(),
        state=TimeNow(),
        companyAddress="companyAddress" + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=agent_phoneNumber,
        phonePrefix=agent_phonePrefix,
        corpCardname="截图20210316142730.png",
        corpCardphoto=photo,
        corpCardtype=agent_type,
        remarks="Remark" + TimeNow(),
        postcode=TimeNow(),
        resourceId=agent_id,
        headers=GetHeaders()
    )
    print("submitSalesAgentInfo", submitSalesAgentInfo.json())
    ##  auditSuccessSa
    auditSuccessSa = inter.auditSuccessSa(
        resourceId=agent_id,
        id=agent_id,
        headers=GetHeaders()
    )
    print("auditSuccessSa", auditSuccessSa.json())
    ### salesAgentInfo
    salesAgentInfo = inter.salesAgentInfo(
        resourceId=agent_id,
        id=agent_id,
        headers=GetHeaders()
    )
    # print("salesAgentInfo",salesAgentInfo.json())
    agent_status_new = salesAgentInfo.json()['data']['salesAgent']['status']
    print("agent_status_new", agent_status_new)
    assert str(agent_status_new) == "active"


def test_Dealer():
    ##  createCorporateDealer
    dealer_email = "Dealer" + TimeNow() + "@qaceshi.co"
    dealer_contactPerson = "Dealer" + TimeNow() + GBK2312()
    dealer_phonePrefix = "+86"
    dealer_phoneNumber = TimeNow()
    createCorporateDealer = inter.createCorporateDealer(
        email=dealer_email,
        contactPerson=dealer_contactPerson,
        phonePrefix=dealer_phonePrefix,
        phoneNumber=dealer_phoneNumber,
        headers=GetHeaders()
    )
    print("createCorporateDealer", createCorporateDealer.json())
    ##  getDealerList
    getDealerList = inter.getDealerList(
        status="assignPending",
        headers=GetHeaders()
    )
    # print("getDealerList",getDealerList.json())
    dealer_id = str(getDealerList.json()['data'][0]['id'])
    dealer_email = str(getDealerList.json()['data'][0]['email'])
    dealer_contactPerson = str(getDealerList.json()['data'][0]['contactPerson'])
    dealer_phonePrefix = str(getDealerList.json()['data'][0]['phonePrefix'])
    dealer_phoneNumber = str(getDealerList.json()['data'][0]['phoneNumber'])
    dealer_status = str(getDealerList.json()['data'][0]['status'])
    print("dealer_id", dealer_id)
    print("dealer_email", dealer_email)
    print("dealer_contactPerson", dealer_contactPerson)
    print("dealer_phonePrefix", dealer_phonePrefix)
    print("dealer_phoneNumber", dealer_phoneNumber)
    print("dealer_status", dealer_status)
    ##  getDealerExecutiveId
    getDealerExecutiveId = inter.getDealerExecutiveId(
        resourceId=dealer_id,
        id=dealer_id,
        headers=GetHeaders()
    )

    # print("getDealerExecutiveId",getDealerExecutiveId.json())
    def getFrom():
        for x in getDealerExecutiveId.json()['data']:
            if str(x['name']) == 'mingvtest1':
                print(x['id'], x['name'])
                exe_id = str(x['id'])
                exe_name = str(x['name'])
                return exe_id, exe_name

    exe_id, exe_name = getFrom()
    print("exe_id", exe_id)
    print("exe_name", exe_name)
    ##  assignDealer
    assignDealer = inter.assignDealer(
        resourceId=dealer_id,
        id=dealer_id,
        assignId=exe_id,
        headers=GetHeaders()
    )
    print("assignDealer", assignDealer.json())
    ##  uploadResultDealer
    photo = "car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png"
    uploadResultDealer = inter.uploadResultDealer(
        photo=photo,
        headers=GetHeaders()
    )
    print("uploadResultDealer", uploadResultDealer.json())
    ##  submitDealerInfo
    submitDealerInfo = inter.submitDealerInfo(
        resourceId=dealer_id,
        id=dealer_id,
        email=dealer_email,
        contactPerson=dealer_contactPerson,
        companyName="Company" + Unicode(),
        city="City" + TimeNow(),
        country="Country" + TimeNow(),
        state=TimeNow(),
        companyAddress="companyAddress" + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=dealer_phoneNumber,
        phonePrefix=dealer_phonePrefix,
        corpSsmname="截图20210316142730.png",
        corpSsmphoto=photo,
        corpCardname="截图20210316142730.png",
        corpCardphoto=photo,
        filename="截图20210316142730.png",
        filephoto=photo,
        remarks="Remark",
        companyPic=Unicode() + GBK2312(),
        picIDCardname="截图20210316142730.png",
        picIDCardphoto=photo,
        marginPaid="true",
        marginFilename="截图20210316142730.png",
        marginFilephoto=photo,
        type="deposit",
        postcode=TimeNow(),
        headers=GetHeaders()
    )
    print("submitDealerInfo", submitDealerInfo.json())
    ##  auditSuccessDealer
    auditSuccessDealer = inter.auditSuccessDealer(
        resourceId=dealer_id,
        id=dealer_id,
        headers=GetHeaders()
    )
    print("auditSuccessDealer", auditSuccessDealer.json())
    ##  getDealerInfo
    getDealerInfo = inter.getDealerInfo(
        resourceId=dealer_id,
        id=dealer_id,
        headers=GetHeaders()
    )
    print("getDealerInfo", getDealerInfo.json())
    dealer_status = getDealerInfo.json()['data']['dealer']['status']
    print("dealer_status", dealer_status)
    assert str(dealer_status) == "active"


def test_Lead():
    ##  newLead
    applyName = "App" + TimeNow()
    applyTel = TimeNow()
    applyTelCode = "+86"
    applyMail = applyName + "@apply.ro"
    carType = "2"
    cardUrl = "car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png"
    newLead = inter.newLead(
        carYear="1992",
        carBrand="ALFA ROMEO",
        carType=carType,
        carModel="145",
        applyName=applyName,
        applyTel=applyTel,
        applyTelCode="+86",
        applyMail=applyMail,
        checkTime=Now(),
        checkDetailAddress="Address" + TimeNow(),
        checkCity="City" + TimeNow(),
        checkRegion=TimeNow(),
        checkPostcode="Postcode" + TimeNow(),
        headers=GetHeaders()
    )
    print("newLead", newLead.json())
    ##  unchecked
    unchecked = inter.unchecked(
        current="1",
        pageSize="999",
        headers=GetHeaders()
    )

    # print("unchecked",unchecked.json())
    def getForm():
        for x in unchecked.json()["data"]:
            if str(x["applyName"]) == applyName:
                print(x["id"], x["leadNo"], x["applyName"])
                newLead_leadNo = str(x["leadNo"])
                return newLead_leadNo

    newLead_leadNo = getForm()
    print("newLead_leadNo", newLead_leadNo)
    ##  corporateMembers
    corporateMembers = inter.corporateMembers(
        headers=GetHeaders()
    )
    print("corporateMembers", corporateMembers.json())

    def getForm():
        for x in corporateMembers.json()['data']:
            if str(x['name']) == "mingvtest1":
                print(x['id'], x['name'])
                corMem_id = str(x['id'])
                return corMem_id

    corMem_id = getForm()
    print("corMem_id", corMem_id)
    ##  assignCorporate
    assignCorporate = inter.assignCorporate(
        leadNo=newLead_leadNo,
        assignId=corMem_id,
        resourceId=newLead_leadNo,
        headers=GetHeaders()
    )
    print("assignCorporate", assignCorporate.json())
    ##  changeCarCard
    changeCarCard = inter.changeCarCard(
        carType=carType,
        cardUrl=cardUrl,
        leadNo=newLead_leadNo,
        resourceId=newLead_leadNo,
        headers=GetHeaders()
    )
    print("changeCarCard", changeCarCard.json())
    ##lead创建seller
    print("#lead创建seller", "=" * 120)
    leadNewSeller = inter.leadNewSeller(
        phoneNumber=applyTel,
        phonePrefix=applyTelCode,
        type=carType,
        email=applyMail,
        name=applyName,
        headers=GetHeaders()
    )
    print("leadNewSeller", leadNewSeller.json())
    ##激活seller
    print("激活seller:", "=" * 100, "START")
    querySellerAccount = inter.querySellerAccount(
        pageSize="999",
        current="1",
        status="assignPending",
        headers=GetHeaders()
    )

    def getSellerId():
        for x in querySellerAccount.json()['data']:
            if str(x['phoneNumber']) == str(applyTel):
                print(x['id'], x['name'], x['phoneNumber'])
                new_seller_id = str(x['id'])
                return new_seller_id

    new_seller_id = getSellerId()
    print("new_seller_id", new_seller_id)
    ##  getSellerExecutiveId
    getSellerExecutiveId = inter.getSellerExecutiveId(
        id=new_seller_id,
        headers=GetHeaders()
    )

    # print("getSellerExecutiveId",getSellerExecutiveId.json())
    ##  循环
    def getFrom():
        for x in getSellerExecutiveId.json()['data']:
            if str(x['name']) == "mingvtest1":
                print(x['id'], x['name'], x['count'])
                exe_id = str(x['id'])
                exe_name = str(x['name'])
                return exe_id, exe_name

    exe_id, exe_name = getFrom()
    print("exe_id", exe_id)
    print("exe_name", exe_name)
    ##  assignSeller
    assignSeller = inter.assignSeller(
        id=new_seller_id,
        assignId=exe_id,
        resourceId=new_seller_id,
        headers=GetHeaders()
    )
    print("assignSeller", assignSeller.json())
    ##  uploadResultSeller
    photo = "car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png"
    uploadResultSeller = inter.uploadResultSeller(
        photo=photo,
        headers=GetHeaders()
    )
    print("uploadResultSeller", uploadResultSeller.json())
    ##  submitCorpSellerInfo
    submitCorpSellerInfo = inter.submitCorpSellerInfo(
        id=new_seller_id,
        email=applyMail,
        name=applyName,
        companyName="Company" + applyName,
        city="City" + TimeNow(),
        country="Country" + TimeNow(),
        state=TimeNow(),
        companyAddress="companyAddress" + TimeNow(),
        registrationNumber=TimeNow(),
        phoneNumber=applyTel,
        phonePrefix=applyTelCode,
        corpSsmname="截图20210316142730.png",
        corpSsmphoto=photo,
        corpCardname="截图20210316142730.png",
        corpCardphoto=photo,
        corpDocname="截图20210316142730.png",
        corpDocphoto=photo,
        remarks="Remark" + TimeNow(),
        postcode=TimeNow(),
        resourceId=new_seller_id,
        headers=GetHeaders()
    )
    print("submitCorpSellerInfo", submitCorpSellerInfo.json())
    ##  auditSuccessSeller
    auditSuccessSeller = inter.auditSuccessSeller(
        resourceId=new_seller_id,
        id=new_seller_id,
        headers=GetHeaders()
    )
    print("auditSuccessSeller", auditSuccessSeller.json())
    ##  infoLead
    infoLead = inter.infoLead(
        id=newLead_leadNo,
        resourceId=newLead_leadNo,
        headers=GetHeaders()
    )
    # print("infoLead",infoLead.json())
    customer_seller_id = infoLead.json()["data"]["seller"]['id']
    print("customer_seller_id", customer_seller_id)

    ##  associateSellerLead
    associateSellerLead = inter.associateSellerLead(
        leadNo=newLead_leadNo,
        customerId=customer_seller_id,
        resourceId=newLead_leadNo,
        headers=GetHeaders()
    )
    print("associateSellerLead", associateSellerLead.json())
    ##  checkLead
    checkLead = inter.checkLead(
        leadNo=newLead_leadNo,
        resourceId=newLead_leadNo,
        headers=GetHeaders()
    )
    print("checkLead", checkLead.json())
    ##  queryNoConfirmInspections
    queryNoConfirmInspections = inter.queryNoConfirmInspections(
        current="1",
        pageSize="999",
        headers=GetHeaders()
    )
    # print("queryNoConfirmInspections",queryNoConfirmInspections.json())
    app_Name = str(queryNoConfirmInspections.json()['data'][0]['applyName'])
    print("applyName", applyName)
    print("app_Name", app_Name)
    assert str(app_Name) == str(applyName)
