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


# 1.admin新建lead
def test_newLead():
    newLead = inter.newLead(
        carYear="1992",
        carBrand="ALFA ROMEO",
        carType="2",
        carModel="145",
        applyName="Apply" + Unicode() + GBK2312() + TimeNow(),
        applyTel=TimeNow(),
        applyTelCode="+86",
        applyMail="Lead" + TimeNow() + "@qaceshi.ro",
        checkTime="2021-08-23T04:00:00Z",
        checkDetailAddress="Address" + TimeNow(),
        checkCity="City" + TimeNow(),
        checkRegion=TimeNow(),
        checkPostcode="Postcode" + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("newLead:", newLead.json())
    print("-" * 100)
    assert str(newLead.json()['success']) == "True"


# 2.查询等待预检的lead
def test_unchecked():
    unchecked = inter.unchecked(
        current="1",
        pageSize="9999",
        headers=GetHeaders()
    )
    print("-" * 100)
    # print("unchecked:",unchecked.json())
    print("-" * 100)
    assert str(unchecked.json()['success']) == "True"
    lead_no = str(unchecked.json()['data'][0]['leadNo'])
    print("-" * 100)
    print("lead_no:", lead_no)
    print("-" * 100)
    return lead_no


# 3.获取customerService成员
def test_customerServiceMembers():
    customerServiceMembers = inter.customerServiceMembers(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("customerServiceMembers:", customerServiceMembers.json())
    print("-" * 100)
    assert str(customerServiceMembers.json()['success']) == "True"
    customer_id = str(customerServiceMembers.json()['data'][-1]['id'])
    print("-" * 100)
    print("customer_id:", customer_id)
    print("-" * 100)
    return customer_id


# 4.获取corporate成员
def test_corporateMembers():
    corporateMembers = inter.corporateMembers(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("corporateMembers:", corporateMembers.json())
    print("-" * 100)
    assert str(corporateMembers.json()['success']) == "True"


# 5.获取lead详情
def test_infoLead():
    infoLead = inter.infoLead(
        id=test_unchecked(),
        resourceId=test_unchecked(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("infoLead:", infoLead.json())
    print("-" * 100)
    assert str(infoLead.json()['success']) == "True"


# 6.指派经办人(customer service)
def test_assignCustomerService():
    test_newLead()
    assignCustomerService = inter.assignCustomerService(
        leadNo=test_unchecked(),
        assignId=test_customerServiceMembers(),
        resourceId=test_unchecked(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("assignCustomerService:", assignCustomerService.json())
    print("-" * 100)
    assert str(assignCustomerService.json()['success']) == "True"


# 7.关联seller
def test_associateSeller():
    test_newLead()
    get_seller = inter.querySellerAccount(
        pageSize="9999",
        current="1",
        status="active",
        headers=GetHeaders()
    )
    seller_id = str(get_seller.json()['data'][0]['id'])
    print("get_seller:", get_seller.json())
    print("seller_id:", seller_id)

    associateSeller = inter.associateSellerLead(
        leadNo=test_unchecked(),
        customerId=seller_id,
        resourceId=test_unchecked(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("associateSeller:", associateSeller.json())
    print("-" * 100)
    assert str(associateSeller.json()['success']) == "True"


# 8.编辑lead基础信息
def test_editLead():
    editLead = inter.editLead(
        carYear="1992",
        carBrand="ALFA ROMEO",
        carType="2",
        carModel="145",
        applyName="Apply" + Unicode() + GBK2312() + TimeNow(),
        applyTel=TimeNow(),
        applyTelCode="+86",
        applyMail="Mv" + TimeNow() + "@qaceshi.ro",
        checkTime="2021-08-23T04:00:00Z",
        checkDetailAddress="Address" + TimeNow(),
        checkCity="City" + TimeNow(),
        checkRegion="y",
        checkPostcode="Postcode" + TimeNow(),
        leadNo=test_unchecked(),
        remark="editLead" + TimeNow(),
        resourceId=test_unchecked(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("editLead:", editLead.json())
    print("-" * 100)
    assert str(editLead.json()['success']) == "True"


# 9.终止lead
def test_finishLead():
    finishLead = inter.finishLead(
        leadNo=test_unchecked(),
        comment="终止lead " + TimeNow(),
        resourceId=test_unchecked(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("finishLead:", finishLead.json())
    print("-" * 100)
    assert str(finishLead.json()['success']) == "True"


# 10.查询完成的lead
def test_checkedLead():
    checkedLead = inter.checkedLead(
        current="1",
        pageSize="9999",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("checkedLead:", checkedLead.json())
    print("-" * 100)
    assert str(checkedLead.json()['success']) == "True"


# 11.编辑车辆户口
def test_changeCarCard():
    changeCarCard = inter.changeCarCard(
        carType="2",
        cardUrl="car/seller/corpSsm/252/9f328e8c5c3a41e1bd8dc9b4bd39bf84.png",
        leadNo=test_unchecked(),
        resourceId=test_unchecked(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("changeCarCard:", changeCarCard.json())
    print("-" * 100)
    assert str(changeCarCard.json()['success']) == "True"


# 12.lead异常
def test_exceptionLead():
    exceptionLead = inter.exception(
        leadNo=test_unchecked(),
        comment="lead异常 " + TimeNow(),
        resourceId=test_unchecked(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("exceptionLead:", exceptionLead.json())
    print("-" * 100)
    assert str(exceptionLead.json()['success']) == "True"


# 13.lead申请确认
def test_checkLead():
    test_associateSeller()
    checkLead = inter.checkLead(
        leadNo=test_unchecked(),
        resourceId=test_unchecked(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("checkLead:", checkLead.json())
    print("-" * 100)
    assert str(checkLead.json()['success']) == "True"


# 14.获取corporate成员
def test_corporateMembers():
    corporateMembers = inter.corporateMembers(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("corporateMembers:", corporateMembers.json())
    print("-" * 100)
    assert str(corporateMembers.json()['success']) == "True"
    corporate_id = str(corporateMembers.json()['data'][-1]['id'])
    print("-" * 100)
    print("corporate_id:", corporate_id)
    print("-" * 100)
    return corporate_id


# 15.查询异常lead
def test_abnormal():
    abnormal = inter.abnormal(
        carBrand="BMW",
        current="1",
        pageSize="999",
        search="",
        carYear="1990",
        createdTime="2021-09-08T16:00:00.000Z",
        sorter={},
        headers=GetHeaders()
    )
    print("-" * 100)
    print("abnormal:", abnormal.json())
    print("-" * 100)
    assert str(abnormal.json()['success']) == "True"


# 16.指派经办人（Corporate）
def test_assignCorporate():
    assignCorporate = inter.assignCorporate(
        leadNo=test_unchecked(),
        assignId=test_corporateMembers(),
        resourceId=test_unchecked(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("abnormal:", assignCorporate.json())
    print("-" * 100)
    assert str(assignCorporate.json()['success']) == "True"


# 17.取消关联系统用户
def test_disassociateLead():
    disassociateLead = inter.disassociateLead(
        leadNo=test_unchecked(),
        resourceId=test_unchecked(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("disassociateLead:", disassociateLead.json())
    print("-" * 100)
    assert str(disassociateLead.json()['success']) == "True"


# 18.lead创建seller
def test_leadNewSeller():
    leadNewSeller = inter.leadNewSeller(
        phoneNumber=TimeNow(),
        phonePrefix="+86",
        type="Individual",
        email="leadNewSeller" + TimeNow() + "@seller.com",
        name="leadNewSeller" + Unicode() + TimeNow(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("leadNewSeller:", leadNewSeller.json())
    print("-" * 100)
    assert str(leadNewSeller.json()['success']) == "True"


# 19.lead创建agent
def test_leadNewSalesAgent():
    leadNewSalesAgent = inter.leadNewSalesAgent(
        phoneNumber=TimeNow(),
        name="LSA" + Unicode() + TimeNow(),
        phonePrefix="+86",
        type="NCD",
        email="LSA" + TimeNow() + "@agent.com",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("leadNewSalesAgent:", leadNewSalesAgent.json())
    print("-" * 100)
    assert str(leadNewSalesAgent.json()['success']) == "True"


# 20.关联agent
def test_associateSalesAgent():
    querySalesAgent = inter.querySalesAgent(
        current="1",
        pageSize="999",
        status="active",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("querySalesAgent:", querySalesAgent.json())
    print("-" * 100)
    agent_id = str(querySalesAgent.json()['data'][0]['id'])
    print("-" * 100)
    print("agent_id:", agent_id)
    print("-" * 100)
    associateSalesAgent = inter.associateSalesAgent(
        leadNo=test_unchecked(),
        customerId=agent_id,
        resourceId=test_unchecked(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("associateSalesAgent:", associateSalesAgent.json())
    print("-" * 100)
    assert str(associateSalesAgent.json()['success']) == "True"


# 21.主页获取验证码
def test_sendVerifyCode():
    applyTel = "123123"
    applyTelCode = "123123"
    sendVerifyCode = inter.sendVerifyCode(
        phonePrefix=applyTelCode,
        phoneNumber=applyTel,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("applyTel:", applyTel)
    print("applyTelCode:", applyTelCode)
    print("sendVerifyCode:", sendVerifyCode.json())
    print("-" * 100)
    assert str(sendVerifyCode.json()['success']) == "True"
    return applyTel, applyTelCode


# 22.主页创建订单
def test_createLeadLead():
    applyTel, applyTelCode = test_sendVerifyCode()
    key = str("Homepage_" + applyTel + "_" + applyTelCode)

    createLeadLead = inter.createLeadLead(
        carYear="1990",
        carBrand="BMW",
        carType="1",
        carModel="2",
        applyName="applyName" + TimeNow() + Unicode() + GBK2312(),
        phonePrefix=applyTel,
        phoneNumber=applyTelCode,
        remark="主页创建订单" + TimeNow(),
        checkTime="2021-09-09T02:41:07.614Z",
        checkDetailAddress="checkDetailAddress" + TimeNow(),
        checkCity="checkCity" + TimeNow(),
        checkRegion="checkRegion" + TimeNow(),
        checkPostcode="checkPostcode" + TimeNow(),
        verifyCode=str(Redis.redisCode(key=key)),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createLeadLead:", createLeadLead.json())
    print("-" * 100)
    assert str(createLeadLead.json()['success']) == "True"


# 23.获取车牌信息
def test_carBrands():
    carBrands = inter.carBrands(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("carBrands:", carBrands.json())
    print("-" * 100)
    assert str(carBrands.json()['success']) == "True"

# GetHeaders()