import requests
import json


class Interface:
    def __init__(self):
        self.url = "http://192.168.102.252:8081"
        """初始化host url"""

    '''【Seller 2.0】'''

    # 新建corp seller
    def addCorpSeller(self, phoneNumber, phonePrefix, email, name, headers):
        path = "/seller/admin/api/seller/addCorpSeller"
        res = requests.post(self.url + path, json={
            "phoneNumber": phoneNumber,
            "phonePrefix": phonePrefix,
            "email": email,
            "name": name
        }, headers=headers)
        return res

    # 查询seller
    def querySellerAccount(self, pageSize, current, status, headers):
        path = "/seller/admin/api/seller/querySellerAccount"
        if status == "":
            res = requests.get(self.url + path, params={
                "pageSize": pageSize,
                "current": current
            }, headers=headers)

        else:
            res = requests.get(self.url + path, params={
                "pageSize": pageSize,
                "current": current,
                "status": status
            }, headers=headers)
        return res

    # 查询个人seller
    def queryIndividualSellerAccount(self, pageSize, current, type, assignedName, headers):
        path = "/seller/admin/api/seller/querySellerAccount"
        if type == "":
            res = requests.get(self.url + path, params={
                "pageSize": pageSize,
                "current": current
            }, headers=headers)

        else:
            res = requests.get(self.url + path, params={
                "pageSize": pageSize,
                "current": current,
                "type": type,
                "assignedName": assignedName
            }, headers=headers)
        return res

    # 冻结seller
    def freezeSeller(self, id, comment, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/seller/admin/api/seller/freezeSeller"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        return res

    # 解冻seller
    def unfreezeSeller(self, id, comment, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/seller/admin/api/seller/unfreezeSeller"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        return res

    # 注销seller
    def closeSeller(self, id, comment, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/seller/admin/api/seller/closeSeller"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        return res

    # 获取可选经办人列表
    def getSellerExecutiveId(self, id, headers):
        path = "/seller/admin/api/seller/getSellerExecutive/"
        print('id', id)
        real_path = self.url + path + id
        res = requests.get(url=real_path, headers=headers)
        return res

    # 指定经办人
    def assignSeller(self, id, assignId, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/seller/admin/api/seller/assignSeller"
        res = requests.post(self.url + path, json={
            "id": id,
            "assignId": assignId
        }, headers=headers)
        print("id", id)
        print("assignId", assignId)
        print("resourceId", resourceId)
        return res

    # 获取子账号列表
    def getSellerSubsidiary(self, id, current, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/seller/admin/api/seller/getSellerSubsidiary/"
        res = requests.get(self.url + path, params={
            "id": id,
            "current": current
        }, headers=headers)
        return res

    # 创建Seller子账号
    def createSellerSubsidiary(self, id, email, phonePrefix, phoneNumber, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/seller/admin/api/seller/createSellerSubsidiary"
        res = requests.post(self.url + path, json={
            "id": id,
            "email": email,
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber
        }, headers=headers)
        return res

    # 注销Seller子账号
    def closeSellerSubsidiary(self, id, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/seller/admin/api/seller/closeSellerSubsidiary"
        res = requests.post(self.url + path, json={
            "id": id,
        }, headers=headers)
        print("id:", id)
        print("headers:", headers)
        return res

    # 新建个人seller
    def addIndividualSeller(self, name, email, phonePrefix, phoneNumber, headers):
        path = "/seller/admin/api/seller/addIndividualSeller"
        res = requests.post(self.url + path, json={
            "name": name,
            "email": email,
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber
        }, headers=headers)
        return res

    # 为dealer创建seller
    def addSellerForDealer(self, name, email, phonePrefix, phoneNumber, headers):
        path = "/seller/admin/api/seller/addSellerForDealer"
        res = requests.post(self.url + path, json={
            "name": name,
            "email": email,
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber
        }, headers=headers)
        return res

    # 获取分派的seller详情
    def sellerInfo(self, id, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/seller/admin/api/seller/sellerInfo/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 获取需要审核的seller详情
    def auditSellerInfo(self, id, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/seller/admin/api/seller/auditSellerInfo/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 提交公司seller审核
    def submitCorpSellerInfo(self, id, email, name, companyName, city, country, state, companyAddress,
                             registrationNumber, phoneNumber, phonePrefix, corpSsmname, corpSsmphoto,
                             corpCardname, corpCardphoto, corpDocname, corpDocphoto, remarks, postcode, resourceId,
                             headers):
        headers.update({'resourceId': resourceId})
        path = "/seller/admin/api/seller/submitCorpSellerInfo"
        res = requests.post(self.url + path, json={
            "id": id,
            "email": email,
            "name": name,
            "companyName": companyName,
            "city": city,
            "country": country,
            "state": state,
            "companyAddress": companyAddress,
            "registrationNumber": registrationNumber,
            "phoneNumber": phoneNumber,
            "phonePrefix": phonePrefix,
            "corpSsm": [{"name": corpSsmname,
                         "photo": corpSsmphoto}],
            "corpCard": [{"name": corpCardname,
                          "photo": corpCardphoto}],
            "corpDoc": [{"name": corpDocname,
                         "photo": corpDocphoto}],
            "remarks": remarks,
            "postcode": postcode
        }, headers=headers)
        return res

    # 提交个人seller信息修改
    def submitIndividualSellerInfo(self, name, email, id, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/seller/admin/api/seller/submitIndividualSellerInfo"
        res = requests.post(self.url + path, json={
            "name": name,
            "email": email,
            "id": id
        }, headers=headers)
        return res

    # 审核通过Seller
    def auditSuccessSeller(self, resourceId, id, headers):
        headers.update({'resourceId': resourceId})
        path = "/seller/admin/api/seller/auditSuccess"
        res = requests.post(self.url + path, json={
            "id": id
        }, headers=headers)
        return res

    # 获取seller history
    def sellerAccountHistory(self, id, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/seller/admin/api/seller/sellerAccountHistory/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 审核失败Seller
    def auditFailSeller(self, id, comment, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/seller/admin/api/seller/auditFail"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        return res

    # 审核退回Seller
    def auditReviseSeller(self, id, comment, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/seller/admin/api/seller/auditRevise"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        return res

    # 上传图片成功
    def uploadResultSeller(self, photo, headers):
        path = "/seller/admin/api/seller/uploadResult"
        # print(photo,headers)
        res = requests.post(self.url + path, data={
            "path": photo
        }, headers=headers)
        return res

    # 查询获取可查看审核人
    def getSellerExecutive(self, headers):
        path = "/seller/admin/api/seller/getSellerExecutive"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 保存修改信息
    def saveEditInfoSeller(self, id, createdTime, email, name, phoneNumber, type, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/seller/admin/api/seller/saveEditInfo"
        res = requests.post(self.url + path, json={
            "id": id,
            "info": [{
                "createdTime": createdTime,
                "email": email,
                "name": name,
                "phoneNumber": phoneNumber,
                "type": type
            }]
        }, headers=headers)
        return res

    '''【Dealer2.0】'''

    # 获取dealer列表
    def getDealerList(self, status, headers):
        path = "/dealer/admin/api/dealer/getDealerList"
        if status == "":
            res = requests.get(self.url + path, headers=headers)
        else:
            res = requests.get(self.url + path, params={
                "status": status
            }, headers=headers)

        return res

    # 文件上传结果
    def uploadResultDealer(self, photo, headers):
        path = "/dealer/admin/api/dealer/uploadResult"
        res = requests.post(self.url + path, data={
            "path": photo
        }, headers=headers)
        return res

    # 获取可选经办人列表
    def getDealerExecutiveId(self, resourceId, id, headers):
        headers.update({'resourceId': resourceId})
        path = "/dealer/admin/api/dealer/getDealerExecutive/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 获取所有经办人列表
    def getDealerExecutive(self, headers):
        path = "/dealer/admin/api/dealer/getDealerExecutive"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 提交dealer审核
    def submitDealerInfo(self, resourceId, id, email, contactPerson, companyName, city, country, state, companyAddress,
                         registrationNumber, phoneNumber, phonePrefix, corpSsmname, corpSsmphoto, corpCardname,
                         corpCardphoto, filename, filephoto, remarks, companyPic,
                         picIDCardname, picIDCardphoto, marginPaid, marginFilename, marginFilephoto, type, postcode,
                         headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/dealer/admin/api/dealer/submitDealerInfo"
        res = requests.post(self.url + path, json={
            "id": id,
            "email": email,
            "contactPerson": contactPerson,
            "companyName": companyName,
            "city": city,
            "country": country,
            "state": state,
            "companyAddress": companyAddress,
            "registrationNumber": registrationNumber,
            "phoneNumber": phoneNumber,
            "phonePrefix": phonePrefix,
            "corpSsm": [{"name": corpSsmname,
                         "photo": corpSsmphoto}],
            "corpCard": [{"name": corpCardname,
                          "photo": corpCardphoto}],
            "file": [{"name": filename,
                      "photo": filephoto}],
            "remarks": remarks,
            "companyPic": companyPic,
            "picIDCard": [{"name": picIDCardname,
                           "photo": picIDCardphoto}],
            "marginPaid": marginPaid,
            "marginFile": [{"name": marginFilename,
                            "photo": marginFilephoto,
                            "type": type}],
            "postcode": postcode
        }, headers=headers)
        return res

    # 保存dealer修改信息
    def saveEditInfoDealer(self, resourceId, id, email, contactPerson, companyName, city, country, state,
                           companyAddress,
                           registrationNumber, phoneNumber, phonePrefix, corpSsmname, corpSsmphoto, type, corpCardname,
                           corpCardphoto, filename, filephoto,
                           remarks, companyPic, picIDCardname, picIDCardphoto, marginPaid, marginFilename,
                           marginFilephoto, postcode, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/dealer/admin/api/dealer/saveEditInfo"
        res = requests.post(self.url + path, json={
            "id": id,
            "info": {
                "email": email,
                "contactPerson": contactPerson,
                "companyName": companyName,
                "city": city,
                "country": country,
                "state": state,
                "companyAddress": companyAddress,
                "registrationNumber": registrationNumber,
                "phoneNumber": phoneNumber,
                "phonePrefix": phonePrefix,
                "corpSsm": [{"name": corpSsmname,
                             "photo": corpSsmphoto}],
                "corpCard": [{"name": corpCardname,
                              "photo": corpCardphoto}],
                "file": [{"name": filename,
                          "photo": filephoto}],
                "remarks": remarks,
                "companyPic": companyPic,
                "picIDCard": [{"name": picIDCardname,
                               "photo": picIDCardphoto}],
                "marginPaid": marginPaid,
                "marginFile": [{"name": marginFilename,
                                "photo": marginFilephoto,
                                "type": type}],
                "postcode": postcode
            }

        }, headers=headers)
        return res

    # 审核通过Dealer
    def auditSuccessDealer(self, resourceId, id, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/dealer/admin/api/dealer/auditSuccess"
        res = requests.post(self.url + path, json={
            "id": id
        }, headers=headers)
        print("id=", id, "\nreresourceId=", resourceId)
        return res

    # 审核失败Dealer
    def auditFailDealer(self, resourceId, id, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/dealer/admin/api/dealer/auditFail"
        res = requests.post(self.url + path, json={
            "id": id
        }, headers=headers)
        return res

    # 审核退回Dealer
    def auditReviseDealer(self, resourceId, id, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/dealer/admin/api/dealer/auditRevise"
        res = requests.post(self.url + path, json={
            "id": id
        }, headers=headers)
        return res

    # 获取审核dealer信息
    def getAuditDealerInfo(self, resourceId, id, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/dealer/admin/api/dealer/getAuditDealerInfo/"
        res = requests.get(self.url + path + id, headers=headers)
        print(self.url + path + id, headers)
        print(resourceId, id, headers)
        return res

    # 获取dealer账户历史
    def getDealerHistory(self, resourceId, id, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/dealer/admin/api/dealer/getDealerHistory/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 检查电话号码
    def checkPhoneNumber(self, phonePrefix, phoneNumber, headers):
        path = "/dealer/admin/api/dealer/checkPhoneNumber"
        res = requests.post(self.url + path, json={
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber
        }, headers=headers)
        return res

    # 检查公司注册码
    def checkRegistrationNumber(self, registrationNumber, headers):
        path = "/dealer/admin/api/dealer/checkRegistrationNumber"
        res = requests.post(self.url + path, json={
            "registrationNumber": registrationNumber
        }, headers=headers)
        return res

    # 检查邮箱Dealer
    def checkEmailDealer(self, email, headers):
        path = "/dealer/admin/api/dealer/checkEmail"
        res = requests.post(self.url + path, json={
            "email": email
        }, headers=headers)
        return res

    # 创建corporate dealer
    def createCorporateDealer(self, email, contactPerson, phonePrefix, phoneNumber, headers):
        path = "/dealer/admin/api/dealer/createCorporateDealer"
        res = requests.post(self.url + path, json={
            "email": email,
            "contactPerson": contactPerson,
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber
        }, headers=headers)
        return res

    # 创建dealer
    def createDealer(self, email, contactPerson, phonePrefix, phoneNumber, headers):
        path = "/dealer/admin/api/dealer/createDealer"
        res = requests.post(self.url + path, json={
            "email": email,
            "contactPerson": contactPerson,
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber
        }, headers=headers)
        return res

    # 获取dealer信息
    def getDealerInfo(self, resourceId, id, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/dealer/admin/api/dealer/getDealerInfo/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 注销dealer
    def closeDealer(self, resourceId, id, comment, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/dealer/admin/api/dealer/closeDealer"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        print("id", id)
        print(headers)
        return res

    # 冻结dealer
    def freezeDealer(self, resourceId, id, comment, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/dealer/admin/api/dealer/freezeDealer"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        return res

    # 解冻dealer
    def reactivateDealer(self, resourceId, id, comment, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/dealer/admin/api/dealer/reactivateDealer"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        return res

    # 创建dealer子账号
    def createSubsidiaryDealer(self, resourceId, id, phonePrefix, phoneNumber, email, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/dealer/admin/api/dealer/createSubsidiaryDealer"
        res = requests.post(self.url + path, json={
            "id": id,
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber,
            "email": email
        }, headers=headers)
        # print(id)
        # print(phonePrefix)
        # print(phoneNumber)
        # print(email)
        return res

    # 注销dealer子账号
    def closeSubsidiaryDealer(self, resourceId, id, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/dealer/admin/api/dealer/closeSubsidiaryDealer"
        res = requests.post(self.url + path, json={
            "id": id
        }, headers=headers)
        return res

    # 获取dealer子账号列表
    def getSubsidiaryDealer(self, resourceId, id, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/dealer/admin/api/dealer/getSubsidiaryDealer"
        res = requests.get(self.url + path, params={
            "id": id
        }, headers=headers)
        # print(id,headers)
        return res

    # 分配dealer
    def assignDealer(self, resourceId, id, assignId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/dealer/admin/api/dealer/assignDealer"
        res = requests.post(self.url + path, json={
            "id": id,
            "assignId": assignId
        }, headers=headers)
        # print("id",id,"resourceId",resourceId,
        #     "assignId",assignId)
        return res

    '''【SalesAgent2.0】'''

    # 新建salesAgent
    def addSalesAgent(self, phoneNumber, phonePrefix, email, name, type, headers):
        '''
        type:
        New Car Dealership     ---NCD
        Recond Car Dealership  ---RCD
        Used Car Dealership    ---UCD
        Individual Broker.     ---INDIVIDUAL_BROKER
        '''
        path = "/sa/admin/api/sa/addSalesAgent"
        res = requests.post(self.url + path, json={
            "phoneNumber": phoneNumber,
            "phonePrefix": phonePrefix,
            "email": email,
            "name": name,
            "type": type
        }, headers=headers)
        return res

    # 查询salesAgent
    def querySalesAgent(self, current, pageSize, status, headers):
        path = "/sa/admin/api/sa/querySalesAgent"
        if status == "":
            res = requests.get(self.url + path, params={
                "current": current,
                "pageSize": pageSize
            }, headers=headers)
        else:
            res = requests.get(self.url + path, params={
                "current": current,
                "pageSize": pageSize,
                "status": status
            }, headers=headers)
        return res

    # 冻结salesAgent
    def freezeSalesAgent(self, resourceId, id, comment, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/sa/admin/api/sa/freezeSalesAgent"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        return res

    # 解冻salesAgent
    def unfreezeSalesAgent(self, resourceId, id, comment, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/sa/admin/api/sa/unfreezeSalesAgent"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        return res

    # 注销salesAgent
    def closeSalesAgent(self, resourceId, id, comment, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/sa/admin/api/sa/closeSalesAgent"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        return res

    # 获取可选分配人
    def getSalesAgentExecutive(self, headers):
        path = "/sa/admin/api/sa/getSalesAgentExecutive"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 分配salesAgent
    def assignSalesAgent(self, resourceId, id, assignId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/sa/admin/api/sa/assignSalesAgent"
        res = requests.post(self.url + path, json={
            "id": id,
            "assignId": assignId
        }, headers=headers)
        return res

    # 获取子账号列表
    def getSalesAgentSubsidiary(self, resourceId, id, pageSize, current, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/sa/admin/api/sa/getSalesAgentSubsidiary"
        res = requests.get(self.url + path, params={
            "id": id,
            "pageSize": pageSize,
            "current": current
        }, headers=headers)
        return res

    # 查看salesAgent信息
    def salesAgentInfo(self, resourceId, id, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/sa/admin/api/sa/salesAgentInfo/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 提交审核（除Individual broker）
    def submitSalesAgentInfo(self, resourceId, id, email, name, companyName, city, country, state, companyAddress,
                             registrationNumber, phoneNumber, phonePrefix, corpCardname, corpCardphoto, corpCardtype,
                             remarks, postcode, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/sa/admin/api/sa/submitSalesAgentInfo"
        res = requests.post(self.url + path, json={
            "id": id,
            "email": email,
            "name": name,
            "companyName": companyName,
            "city": city,
            "country": country,
            "state": state,
            "companyAddress": companyAddress,
            "registrationNumber": registrationNumber,
            "phoneNumber": phoneNumber,
            "phonePrefix": phonePrefix,
            "corpCard": [{"name": corpCardname,
                          "photo": corpCardphoto,
                          "type": corpCardtype}],
            "remarks": remarks,
            "postcode": postcode
        }, headers=headers)
        return res

    # 创建子账号
    def createSalesAgentSubsidiary(self, resourceId, id, email, phonePrefix, phoneNumber, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/sa/admin/api/sa/createSalesAgentSubsidiary"
        res = requests.post(self.url + path, json={
            "id": id,
            "email": email,
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber
        }, headers=headers)
        return res

    # 关闭子账号
    def closeSalesAgentSubsidiary(self, resourceId, id, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/sa/admin/api/sa/closeSalesAgentSubsidiary"
        res = requests.post(self.url + path, json={
            "id": id
        }, headers=headers)
        return res

    # 审核页面
    def auditAgentInfo(self, resourceId, id, pageSize, current, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/sa/admin/api/sa/auditAgentInfo/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 审核成功Sa
    def auditSuccessSa(self, resourceId, id, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/sa/admin/api/sa/auditSuccess"
        res = requests.post(self.url + path, json={
            "id": id
        }, headers=headers)
        return res

    # 审核失败Sa
    def auditFailSa(self, resourceId, id, comment, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/sa/admin/api/sa/auditFail"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        return res

    # 审核退回Sa
    def auditReviseSa(self, resourceId, id, comment, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/sa/admin/api/sa/auditRevise"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        return res

    # 账号历史
    def agentAccountHistory(self, resourceId, id, comment, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/sa/admin/api/sa/agentAccountHistory/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 提交individual broker审核
    def submitIndividualBrokerInfo(self, email, name, remarks, corpCardname, corpCardurl, id, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/sa/admin/api/sa/submitIndividualBrokerInfo"
        res = requests.post(self.url + path, json={
            "email": email,
            "name": name,
            "remarks": remarks,
            "corpCard": [{"name": corpCardname,
                          "url": corpCardurl}],
            "id": id
        }, headers=headers)
        return res

    # 保存editInfo
    def saveEditInfoSa(self, resourceId, id, email, name, companyName, city, country, state, companyAddress,
                       registrationNumber, phoneNumber, phonePrefix, corpSsmname, corpSsmphoto, corpCardname,
                       corpCardphoto,
                       corpDocname, corpDocphoto, remarks, postcode, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/sa/admin/api/sa/saveEditInfo"
        res = requests.post(self.url + path, json={
            "id": id,
            "info": {
                "email": email,
                "name": name,
                "companyName": companyName,
                "city": city,
                "country": country,
                "state": state,
                "companyAddress": companyAddress,
                "registrationNumber": registrationNumber,
                "phoneNumber": phoneNumber,
                "phonePrefix": phonePrefix,
                "corpSsm": [{"name": corpSsmname,
                             "photo": corpSsmphoto}],
                "corpCard": [{"name": corpCardname,
                              "photo": corpCardphoto}],
                "corpDoc": [{"name": corpDocname,
                             "photo": corpDocphoto}],
                "remarks": remarks,
                "postcode": postcode
            }
        }, headers=headers)
        return res

    # sa check email Sa
    def checkEmailSa(self, email, headers):
        path = "/sa/admin/api/sa/checkEmail"
        res = requests.post(self.url + path, json={
            "email": email
        }, headers=headers)
        return res

    # 上传图片成功Sa
    def uploadResultSa(self, photo, headers):
        path = "/sa/admin/api/sa/uploadResult"
        res = requests.post(self.url + path, data={
            "path": photo
        }, headers=headers)
        return res

    '''【检车2.0】'''

    # 创建检车单
    def createInspection(self, carYear, carBrand, carModel, applyTel, applyTelCode, applyName, applyMail, carType,
                         cardUrl, headers):
        path = "/inspector/admin/api/inspector/createInspection"
        res = requests.post(self.url + path, json={
            "carYear": carYear,
            "carBrand": carBrand,
            "carModel": carModel,
            "applyTel": applyTel,
            "applyTelCode": applyTelCode,
            "applyName": applyName,
            "applyMail": applyMail,
            "carType": carType,
            "cardUrl": cardUrl
        }, headers=headers)
        return res

    # 获取关联系统客户
    def relatedCustomer(self, no, headers):
        path = "/inspector/admin/api/inspector/relatedCustomer"
        res = requests.get(self.url + path, params={
            "no": no
        }, headers=headers)
        return res

    # 取消检车单
    def cancelInspection(self, no, comment, headers):
        path = "/inspector/admin/api/inspector/cancelInspection"
        res = requests.post(self.url + path, json={
            "no": no,
            "comment": comment
        }, headers=headers)
        return res

    # 查询待处理检车任务
    def queryNoConfirmInspections(self, current, pageSize, headers):
        path = "/inspector/admin/api/inspector/queryNoConfirmInspections"
        res = requests.get(self.url + path, params={
            "current": current,
            "pageSize": pageSize
        }, headers=headers)
        return res

    # 获取所有检车任务安排
    def checkerTasks(self, checkDateA, checkDateB, headers):
        path = "/inspector/admin/api/inspector/checkerTasks"
        res = requests.get(self.url + path, params={
            "checkDate": [checkDateA, checkDateB]
        }, headers=headers)
        return res

    # 获取待确认检车单详情
    def noConfirmInspectionInfo(self, id, headers):
        path = "/inspector/admin/api/inspector/noConfirmInspectionInfo"
        res = requests.get(self.url + path, params={
            "id": id
        }, headers=headers)
        return res

    # 获取待分配检车员
    def inspectorsWithTarget(self, checkTime, headers):
        path = "/inspector/admin/api/inspector/inspectorsWithTarget"
        res = requests.get(self.url + path, params={
            "checkTime": checkTime
        }, headers=headers)
        return res

    # 确认检车单
    def confirmInspection(self, id, checkTime, address, city, region, postCode, checkerName, checkerId, headers):
        path = "/inspector/admin/api/inspector/confirmInspection"
        res = requests.post(self.url + path, json={
            "id": id,
            "checkTime": checkTime,
            "address": address,
            "city": city,
            "region": region,
            "postCode": postCode,
            "checkerId": checkerId,
            "checkerName": checkerName
        }, headers=headers)
        return res

    # 关联seller
    def associateSellerInspector(self, id, customerId, headers):
        path = "/inspector/admin/api/inspector/associateSeller"
        res = requests.post(self.url + path, json={
            "id": id,
            "customerId": customerId
        }, headers=headers)
        return res

    # 关联agent
    def associateAgent(self, id, customerId, headers):
        path = "/inspector/admin/api/inspector/associateAgent"
        res = requests.post(self.url + path, json={
            "id": id,
            "customerId": customerId
        }, headers=headers)
        return res

    # 查询审核未完成
    def queryCheckedInspection(self, current, pageSize, headers):
        path = "/inspector/admin/api/inspector/queryCheckedInspection"
        res = requests.get(self.url + path, params={
            "current": current,
            "pageSize": pageSize
        }, headers=headers)
        return res

    # 查询已完成
    def queryFinishedInspection(self, current, pageSize, headers):
        path = "/inspector/admin/api/inspector/queryFinishedInspection"
        res = requests.get(self.url + path, params={
            "current": current,
            "pageSize": pageSize
        }, headers=headers)
        return res

    # 审核详情
    def auditInspectionInfo(self, id, headers):
        path = "/inspector/admin/api/inspector/auditInspectionInfo"
        res = requests.get(self.url + path, params={
            "id": id
        }, headers=headers)
        return res

    # 已完成检车单详情
    def finishedInspectionInfo(self, id, headers):
        path = "/inspector/admin/api/inspector/finishedInspectionInfo"
        res = requests.get(self.url + path, params={
            "id": id
        }, headers=headers)
        return res

    # 审核成功Inspector
    def auditSuccessInspector(self, no, comment, price, headers):
        path = "/inspector/admin/api/inspector/auditSuccess"
        res = requests.post(self.url + path, json={
            "no": no,
            "comment": comment,
            "price": price
        }, headers=headers)
        return res

    # 审核失败Inspector
    def auditFailInspector(self, id, comment, headers):
        path = "/inspector/admin/api/inspector/auditFail"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        return res

    # 审核退回Inspector
    def auditReviseInspector(self, no, comment, headers):
        path = "/inspector/admin/api/inspector/auditRevise"
        res = requests.post(self.url + path, json={
            "no": no,
            "comment": comment
        }, headers=headers)
        return res

    # 上传结果
    def uploadResultInspector(self, photo, headers):
        path = "/inspector/admin/api/inspector/uploadResult"
        res = requests.post(self.url + path, data={
            "path": photo
        }, headers=headers)
        return res

    # 取消关联
    def disassociateInspector(self, id, headers):
        path = "/inspector/admin/api/inspector/disassociate"
        res = requests.post(self.url + path, json={
            "id": id
        }, headers=headers)
        return res

    # 获取已确认检车单列表
    def queryConfirmedInspection(self, headers):
        path = "/inspector/admin/api/inspector/queryConfirmedInspection"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 获取已确认检车单详情
    def getConfirmedInspectionInfo(self, id, headers):
        path = "/inspector/admin/api/inspector/getConfirmedInspectionInfo"
        res = requests.get(self.url + path, params={
            "id": id
        }, headers=headers)
        print(id)
        return res

    # 获取检车报告车辆信息User
    def getCarInfoInspector(self, id, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/inspector/admin/api/inspector/getCarInfo/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 获取检车报告车辆照片Inspector
    def getCarPhotoInspector(self, id, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/inspector/admin/api/inspector/getCarPhoto/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 获取检车报告车辆损伤照片Inspector
    def getCarDamagePhotoInspector(self, id, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/inspector/admin/api/inspector/getCarDamagePhoto/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 获取检车任务列表
    def getCheckerTaskList(self, startTime, endTime, headers):
        path = "/inspector/api/inspector/getCheckerTaskList"
        res = requests.get(self.url + path, params={
            "startTime": startTime,
            "endTime": endTime
        }, headers=headers)
        return res

    # 编辑车辆损伤信息Inspector
    def editCarDamageInfoInspector(self, id, position1, photos1, position2, photos2, position3, photos3, position4,
                                   photos4, headers):
        path = "/inspector/api/inspector/editCarDamageInfo/"
        res = requests.post(self.url + path, json={
            "id": id,
            "damageInfo": {"Engine Acceleration": [
                {
                    "position": position1,
                    "photos": photos1
                },
                {
                    "position": position2,
                    "photos": photos2
                },
                {
                    "position": position3,
                    "photos": photos3
                },
                {
                    "position": position4,
                    "photos": photos4
                }]
            }},
                            headers=headers)
        return res

    # 提交检车任务
    def submitCheckerTask(self, id, expectPrice, inspectorDecision, remarks, headers):
        path = "/inspector/api/inspector/submitCheckerTask"
        res = requests.post(self.url + path, json={
            "id": id,
            "expectPrice": expectPrice,
            "inspectorDecision": inspectorDecision,
            "remarks": remarks
        }, headers=headers)
        return res

    # 取消检车任务
    def cancelCheckerTask(self, id, cancelReason, remarks, headers):
        path = "/inspector/api/inspector/cancelCheckerTask"
        res = requests.post(self.url + path, json={
            "id": id,
            "cancelReason": cancelReason,
            "remarks": remarks
        }, headers=headers)
        return res

    # 编辑车辆信息
    def editCarInfoInspector(self, id, brand, model, chassisNumber, currentColor, currentMileage, engineCapacity,
                             engineNumber, existingLoan,
                             fuelType, licensePlateNumber, manufacturedYear, originalColor, registrationDate,
                             registrationType, reservedPrice,
                             roadTaxExpiryDate, seat, soldWithLicensePlate, transmission, variant, inspectionNotes,
                             spareKey, b5, location, dealerIndicator, headers):
        # print(id,brand,model,chassisNumber,currentColor,currentMileage,engineCapacity,engineNumber,existingLoan,
        #             fuelType,licensePlateNumber,manufacturedYear,originalColor,registrationDate,registrationType,reservedPrice,
        #             roadTaxExpiryDate,seat,soldWithLicensePlate,transmission,variant,inspectionNotes,spareKey,b5,location,dealerIndicator)
        path = "/inspector/api/inspector/editCarInfo"
        res = requests.post(self.url + path, json={
            "id": id,
            "brand": brand,
            "model": model,
            "chassisNumber": chassisNumber,
            "currentColor": currentColor,
            "currentMileage": currentMileage,
            "engineCapacity": engineCapacity,
            "engineNumber": engineNumber,
            "existingLoan": existingLoan,
            "fuelType": fuelType,
            "licensePlateNumber": licensePlateNumber,
            "manufacturedYear": manufacturedYear,
            "originalColor": originalColor,
            "registrationDate": registrationDate,
            "registrationType": registrationType,
            "reservedPrice": reservedPrice,
            "roadTaxExpiryDate": roadTaxExpiryDate,
            "seat": seat,
            "soldWithLicensePlate": soldWithLicensePlate,
            "transmission": transmission,
            "variant": variant,
            "inspectionNotes": inspectionNotes,
            "spareKey": spareKey,
            "b5": b5,
            "location": location,
            "dealerIndicator": dealerIndicator
        }, headers=headers)
        return res

    # 获取检车报告信息
    def getInspectionReport(self, id, headers):
        path = "/inspector/api/inspector/getInspectionReport/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 退出审核
    def quitAudit(self, id, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/inspector/admin/api/inspector/quitAudit"
        res = requests.post(self.url + path, json={
            "id": id
        }, headers=headers)
        return res

    # 检查检车员时间
    def checkInspectionTime(self, checkTime, checkerId, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/inspector/admin/api/inspector/checkInspectionTime"
        res = requests.post(self.url + path, json={
            "checkTime": checkTime,
            "checkerId": checkerId
        }, headers=headers)
        return res

    # 回退检车单
    def backInspection(self, id, comment, headers):
        path = "/inspector/admin/api/inspector/backInspection"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        return res

    '''【业绩管理2.0】'''

    # 获取检车员业绩统计
    def performanceInfo(self, type, date, headers):
        path = "/user/admin/api/checker/performanceInfo"
        res = requests.get(self.url + path, params={
            "type": type,
            "date": date
        }, headers=headers)
        print("type", type)
        print("date", date)
        return res

    # 更改检车员目标
    def changeInspectorTarget(self, id, dayTarget, monthTarget, headers):
        path = "/user/admin/api/checker/changeInspectorTarget"
        res = requests.post(self.url + path, json={
            "id": id,
            "dayTarget": dayTarget,
            "monthTarget": monthTarget
        }, headers=headers)
        return res

    # 更改检车员工作区域
    def changeInspectorRegion(self, id, region, headers):
        path = "/user/admin/api/checker/changeInspectorRegion"
        res = requests.post(self.url + path, json={
            "id": id,
            "region": region
        }, headers=headers)
        return res

    # 获取检车员工作状态表
    def userBreakMonthDetailChecker(self, year, month, id, headers):
        path = "/user/admin/api/checker/userBreakMonthDetail"
        res = requests.get(self.url + path, params={
            "year": year,
            "month": month,
            "id": id
        }, headers=headers)
        return res

    # 更改检车员工作状态
    def changeUserWorkStateChecker(self, date, userId, isBreak, remark, headers):
        path = "/user/admin/api/checker/changeUserWorkState"
        res = requests.post(self.url + path, json={
            "date": date,
            "userId": userId,
            "isBreak": isBreak,
            "remark": remark
        }, headers=headers)
        return res

    # 获取检车员信息变更历史
    def userChangeHistoryChecker(self, id, headers):
        path = "/user/admin/api/checker/userChangeHistory"
        res = requests.get(self.url + path, params={
            "id": id
        }, headers=headers)
        return res

    # 获取客服业绩统计
    def getCustomerServicePerformanceInfo(self, date, type, headers):
        path = "/user/admin/api/user/getCustomerServicePerformanceInfo"
        res = requests.get(self.url + path, params={
            "date": date,
            "type": type
        }, headers=headers)
        return res

    # 更改客服目标
    def changeCustomerServiceTarget(self, id, dayTarget, monthTarget, headers):
        path = "/user/admin/api/user/changeCustomerServiceTarget"
        res = requests.post(self.url + path, json={
            "id": id,
            "dayTarget": dayTarget,
            "monthTarget": monthTarget
        }, headers=headers)
        return res

    # 获取客服工作状态表
    def userBreakMonthDetailUser(self, year, month, id, headers):
        path = "/user/admin/api/user/userBreakMonthDetail"
        res = requests.get(self.url + path, params={
            "year": year,
            "month": month,
            "id": id
        }, headers=headers)
        return res

    # 更改客服工作状态
    def changeUserWorkStateUser(self, date, userId, isBreak, remark, headers):
        path = "/user/admin/api/user/changeUserWorkState"
        res = requests.post(self.url + path, json={
            "date": date,
            "userId": userId,
            "isBreak": isBreak,
            "remark": remark
        }, headers=headers)
        return res

    # 客服信息变更历史
    def userChangeHistoryUser(self, id, headers):
        path = "/user/admin/api/user/userChangeHistory"
        res = requests.get(self.url + path, params={
            "id": id
        }, headers=headers)
        return res

    '''【车辆管理2.0】'''

    # 获取车辆列表
    def getCarListInspector(self, headers):
        path = "/inspector/admin/api/car/getCarList"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 获取关联卖家
    def getRelatedCustomer(self, phonePrefix, phoneNumber, headers):
        path = "/inspector/admin/api/car/getRelatedCustomer"
        res = requests.get(self.url + path, params={
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber
        }, headers=headers)
        return res

    # 添加车辆Car
    def createCar(self, brand, model, manufacturedYear, type, customerId, customerName, customerType, phonePrefix,
                  phoneNumber, headers):
        path = "/inspector/admin/api/car/createCar"
        res = requests.post(self.url + path, json={
            "brand": brand,
            "model": model,
            "manufacturedYear": manufacturedYear,
            "type": type,
            "customerId": customerId,
            "customerName": customerName,
            "customerType": customerType,
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber
        }, headers=headers)
        return res

    # 获取车辆检车报告列表
    def getCarInspectionReports(self, number, headers):
        path = "/inspector/admin/api/car/getCarInspectionReports/"
        res = requests.get(self.url + path + number, headers=headers)
        return res

    # 获取检车报告车辆信息Car
    def getCarInfoCar(self, id, headers):
        path = "/inspector/admin/api/car/getCarInfo/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 获取检车报告车辆照片Car
    def getCarPhotoCar(self, id, headers):
        path = "/inspector/admin/api/car/getCarPhoto/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 获取检车报告车辆损伤照片Car
    def getCarDamagePhotoCar(self, id, headers):
        path = "/inspector/admin/api/car/getCarDamagePhoto/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 确认检车报告
    def confirmInspectionReport(self, id, headers):
        path = "/inspector/admin/api/car/confirmInspectionReport"
        res = requests.post(self.url + path, json={
            "id": id
        }, headers=headers)
        return res

    # 删除检车报告
    def deleteInspectionReport(self, id, headers):
        path = "/inspector/admin/api/car/deleteInspectionReport"
        res = requests.post(self.url + path, json={
            "id": id
        }, headers=headers)
        return res

    # 修改检车报告到期时间
    def editInspectionReportExpiredTime(self, id, expiredTime, headers):
        path = "/inspector/admin/api/car/editInspectionReportExpiredTime"
        res = requests.post(self.url + path, json={
            "id": id,
            "expiredTime": expiredTime
        }, headers=headers)
        return res

    # 冻结车辆
    def freezeCar(self, number, days, reason, headers):
        path = "/inspector/admin/api/car/freezeCar"
        res = requests.post(self.url + path, json={
            "number": number,
            "days": days,
            "reason": reason
        }, headers=headers)
        return res

    # 解冻车辆
    def unfreezeCar(self, number, reason, headers):
        path = "/inspector/admin/api/car/unfreezeCar"
        res = requests.post(self.url + path, json={
            "number": number,
            "reason": reason
        }, headers=headers)
        return res

    # 注销车辆
    def deleteCar(self, number, reason, headers):
        path = "/inspector/admin/api/car/deleteCar"
        res = requests.post(self.url + path, json={
            "number": number,
            "reason": reason
        }, headers=headers)
        return res

    # 变更车辆起拍价
    def editReservedPrice(self, number, reservedPrice, headers):
        path = "/inspector/admin/api/car/editReservedPrice"
        res = requests.post(self.url + path, json={
            "number": number,
            "reservedPrice": reservedPrice
        }, headers=headers)
        return res

    # 获取车辆活动日志
    def getCarHistory(self, number, headers):
        path = "/inspector/admin/api/car/getCarHistory/"
        res = requests.get(self.url + path + number, headers=headers)
        return res

    # 获取检车报告活动日志
    def getInspectionReportHistory(self, id, headers):
        path = "/inspector/admin/api/car/getInspectionReportHistory/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 触发检车
    def createInspectionNumber(self, number, headers):
        path = "/inspector/admin/api/car/createInspection"
        res = requests.post(self.url + path, json={
            "number": number
        }, headers=headers)
        return res

    # 创建检车报告
    def createInspectionReport(self, number, headers):
        path = "/inspector/admin/api/car/createInspectionReport"
        res = requests.post(self.url + path, json={
            "number": number
        }, headers=headers)
        return res

    # 获取已完成车辆列表
    def getCompletedCarList(self, headers):
        path = "/inspector/admin/api/car/getCompletedCarList"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 编辑车辆信息
    def editCarInfoCar(self, id, brand, model, chassisNumber, currentColor, currentMileage, engineCapacity,
                       engineNumber, existingLoan,
                       fuelType, licensePlateNumber, manufacturedYear, originalColor, registrationDate,
                       registrationType, reservedPrice,
                       roadTaxExpiryDate, seat, soldWithLicensePlate, transmission, variant, inspectionNotes, spareKey,
                       b5, location, dealerIndicator,
                       headers):
        path = "/inspector/admin/api/car/editCarInfo"
        res = requests.post(self.url + path, json={
            "id": id,
            "brand": brand,
            "model": model,
            "chassisNumber": chassisNumber,
            "currentColor": currentColor,
            "currentMileage": currentMileage,
            "engineCapacity": engineCapacity,
            "engineNumber": engineNumber,
            "existingLoan": existingLoan,
            "fuelType": fuelType,
            "licensePlateNumber": licensePlateNumber,
            "manufacturedYear": manufacturedYear,
            "originalColor": originalColor,
            "registrationDate": registrationDate,
            "registrationType": registrationType,
            "reservedPrice": reservedPrice,
            "roadTaxExpiryDate": roadTaxExpiryDate,
            "seat": seat,
            "soldWithLicensePlate": soldWithLicensePlate,
            "transmission": transmission,
            "variant": variant,
            "inspectionNotes": inspectionNotes,
            "spareKey": spareKey,
            "b5": b5,
            "location": location,
            "dealerIndicator": dealerIndicator
        }, headers=headers)
        return res

    # 编辑车辆损伤信息Car
    def editCarDamageInfoCar(self, id, name, position, photo, headers):
        path = "/inspector/admin/api/car/editCarDamageInfo"
        res = requests.post(self.url + path, json={
            "id": id,
            "name": name,
            "position": position,
            "path": photo
        }, headers=headers)
        return res

    # 删除车辆损伤信息
    def deleteCarDamageInfo(self, id, name, position, headers):
        path = "/inspector/admin/api/car/deleteCarDamageInfo"
        res = requests.post(self.url + path, json={
            "id": id,
            "name": name,
            "position": position
        }, headers=headers)
        return res

    # 删除车辆照片
    def deleteCarPhoto(self, id, name, headers):
        path = "/inspector/admin/api/car/deleteCarPhoto"
        res = requests.post(self.url + path, json={
            "id": id,
            "name": name
        }, headers=headers)
        # print("id",id)
        # print("name",name)
        return res

    # 关联车辆
    def slotCar(self, number, id, headers):
        path = "/inspector/admin/api/car/slotCar"
        res = requests.post(self.url + path, json={
            "number": number,
            "id": id
        }, headers=headers)
        return res

    # 获取车辆竞标历史
    def getBiddingHistory(self, number, headers):
        path = "/inspector/admin/api/car/getBiddingHistory/"
        res = requests.get(self.url + path + number, headers=headers)
        return res

    # 编辑检车备注
    def editInspectionNotes(self, id, comment, headers):
        path = "/inspector/admin/api/car/editInspectionNotes"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        return res

    # 获取车辆检车报告完成情况
    def getReportRequiredInfo(self, id, headers):
        path = "/inspector/admin/api/car/getReportRequiredInfo/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    '''【竞标管理2.0】'''

    # 获取竞标场次列表
    def queryBiddingBlock(self, status, headers):
        path = "/bidding/admin/api/bidding/queryBiddingBlock"
        if status == "":
            res = requests.get(self.url + path, headers=headers)
        else:
            res = requests.get(self.url + path, params={
                "status": status
            }, headers=headers)

        return res

    # 批量关联车辆
    def slotCars(self, id, numbers, headers):
        # print(numbers)
        path = "/inspector/admin/api/car/slotCars"
        res = requests.post(self.url + path, json={
            "id": id,
            "numbers": numbers
        }, headers=headers)
        return res

    # 添加竞标场次
    def createBiddingBlock(self, startTime, endTime, maxCarCount, countDownTime, systemBidPrice,
                           bidPrice1, bidPrice2, bidPrice3, startNotified, noticeTime, headers):
        path = "/bidding/admin/api/bidding/createBiddingBlock"
        res = requests.post(self.url + path, json={
            "startTime": startTime,
            "endTime": endTime,
            "maxCarCount": maxCarCount,
            "countDownTime": countDownTime,
            "systemBidPrice": systemBidPrice,
            "bidPrice1": bidPrice1,
            "bidPrice2": bidPrice2,
            "bidPrice3": bidPrice3,
            "startNotified": startNotified,
            "noticeTime": noticeTime
        }, headers=headers)
        return res

    # 获取竞标场次详情
    def getBiddingBlockInfo(self, id, headers):
        path = "/bidding/admin/api/bidding/getBiddingBlockInfo/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 获取车辆出价明细
    def getBidList(self, biddingBlockId, carNumber, headers):
        path = "/bidding/admin/api/bidding/getBidList"
        res = requests.get(self.url + path, params={
            "biddingBlockId": biddingBlockId,
            "carNumber": carNumber
        }, headers=headers)
        return res

    # 批量添加竞标场次
    def createBiddingBlocks(self, maxCarCount, countDownTime, systemBidPrice, startNotified, startTime, endTime,
                            noticeTime, headers):
        path = "/bidding/admin/api/bidding/createBiddingBlocks"
        res = requests.post(self.url + path, json={
            "maxCarCount": maxCarCount,
            "countDownTime": countDownTime,
            "systemBidPrice": systemBidPrice,
            "startNotified": startNotified,
            "times": [{
                "startTime": startTime,
                "endTime": endTime,
                "noticeTime": noticeTime
            }]
        }, headers=headers)
        return res

    # 取消竞标场次
    def cancelBiddingBlock(self, id, comment, headers):
        path = "/bidding/admin/api/bidding/cancelBiddingBlock"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        return res

    # 批量取消车辆关联
    def cancelCars(self, ids, id, headers):
        path = "/bidding/admin/api/bidding/cancelCars"
        res = requests.post(self.url + path, json={
            "ids": ids,
            "id": id
        }, headers=headers)
        print("ids", ids)
        print("id", id)
        return res

    # 编辑Seller中标意见
    def editSellerComment(self, id, comment, headers):
        path = "/bidding/admin/api/bidding/editSellerComment"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        return res

    # 按时间段获取竞标场次
    def getBiddingBlocks(self, startTime, endTime, headers):
        path = "/bidding/admin/api/bidding/getBiddingBlocks"
        res = requests.get(self.url + path, params={
            "startTime": startTime,
            "endTime": endTime
        }, headers=headers)
        return res

    # 获取竞标场次关联车辆列表
    def getSlottedCars(self, id, pageSize, headers):
        path = "/bidding/admin/api/bidding/getSlottedCars"
        res = requests.get(self.url + path, params={
            "id": id,
            "pageSize": pageSize
        }, headers=headers)
        return res

    # 获取待关联车辆列表
    def getApprovedCars(self, id, headers):
        path = "/bidding/admin/api/bidding/getApprovedCars"
        res = requests.get(self.url + path, params={
            "id": id
        }, headers=headers)
        return res

    # 编辑竞标场次
    def editBiddingBlock(self, startTime, endTime, maxCarCount, countDownTime, systemBidPrice, startNotified,
                         noticeTime, id, headers):
        path = "/bidding/admin/api/bidding/editBiddingBlock"
        res = requests.post(self.url + path, json={
            "startTime": startTime,
            "endTime": endTime,
            "maxCarCount": maxCarCount,
            "countDownTime": countDownTime,
            "systemBidPrice": systemBidPrice,
            "startNotified": startNotified,
            "noticeTime": noticeTime,
            "id": id
        }, headers=headers)
        print("startTime", startTime)
        print("endTime", endTime)
        print("maxCarCount", maxCarCount)
        print("countDownTime", countDownTime)
        print("systemBidPrice", systemBidPrice)
        print("noticeTime", noticeTime)
        print("id", id)
        return res

    '''【交易2.0】'''

    # 查询交易
    def queryTransOrder(self, headers):
        path = "/trans/admin/api/transaction/queryTransOrder"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 获取operationAdmin以及sellerTransaction
    def executiveWithSeller(self, headers):
        path = "/trans/admin/api/transaction/executiveWithSeller"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 获取operationAdmin以及dealerExecutive
    def executiveWithDealer(self, headers):
        path = "/trans/admin/api/transaction/executiveWithDealer"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 获取seller交易员
    def sellerTraders(self, headers):
        path = "/trans/admin/api/transaction/sellerTraders"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 获取dealer交易员
    def dealerTraders(self, headers):
        path = "/trans/admin/api/transaction/dealerTraders"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 指定分配人
    def assignExecutive(self, assignId, id, headers):
        path = "/trans/admin/api/transaction/assignExecutive"
        res = requests.post(self.url + path, json={
            "assignId": assignId,
            "id": id
        }, headers=headers)
        return res

    # 查看预约信息
    def appointmentInfo(self, id, headers):
        path = "/trans/admin/api/transaction/appointmentInfo"
        res = requests.get(self.url + path, params={"id": id}
                           , headers=headers)
        return res

    # 提交预约信息
    def submitAppointmentInfo(self, bizId, appointmentDate, province, district, zipCode, detail, files, transAmount,
                              headers):
        path = "/trans/admin/api/transaction/submitAppointmentInfo"
        res = requests.post(self.url + path, json={
            "bizId": bizId,
            "appointmentDate": appointmentDate,
            "province": province,
            "district": district,
            "zipCode": zipCode,
            "detail": detail,
            "files": files,
            "transAmount": transAmount
        }, headers=headers)
        return res

    # 保存预约信息
    def saveAppointmentInfo(self, bizId, appointmentDate, province, district, zipCode, detail, files, transAmount,
                            headers):
        path = "/trans/admin/api/transaction/saveAppointmentInfo"
        res = requests.post(self.url + path, json={
            "bizId": bizId,
            "appointmentDate": appointmentDate,
            "province": province,
            "district": district,
            "zipCode": zipCode,
            "detail": detail,
            "files": files,
            "transAmount": transAmount
        }, headers=headers)
        return res

    # 获取sellerTX
    def sellerTransInfo(self, id, headers):
        # print(id)
        path = "/trans/admin/api/transaction/sellerTransInfo"
        res = requests.get(self.url + path, params={
            "id": id
        }, headers=headers)
        return res

    # 保存sellerTx
    def saveSellerTransInfo(self, transDate, carLocation, operatorId, operatorName, serviceFee, loanAmount, remark,
                            type_purchaseInvoice, photo_purchaseInvoice, name_purchaseInvoice,
                            type_odo, photo_odo, name_odo, type_vccl, photo_vccl, name_vccl,
                            type_partyLetter, photo_partyLetter, name_partyLetter, transId, headers):
        path = "/trans/admin/api/transaction/saveSellerTransInfo"
        res = requests.post(self.url + path, json={
            "transDate": transDate,
            "carLocation": carLocation,
            "operatorId": operatorId,
            "operatorName": operatorName,
            "serviceFee": serviceFee,
            "loanAmount": loanAmount,
            "remark": remark,
            "purchaseInvoice": [{
                "type": type_purchaseInvoice,
                "photo": photo_purchaseInvoice,
                "name": name_purchaseInvoice
            }],
            "odo": [{
                "type": type_odo,
                "photo": photo_odo,
                "name": name_odo
            }],
            "vccl": [{
                "type": type_vccl,
                "photo": photo_vccl,
                "name": name_vccl
            }],
            "partyLetter": [{
                "type": type_partyLetter,
                "photo": photo_partyLetter,
                "name": name_partyLetter
            }],
            "transId": transId
        }, headers=headers)
        return res

    # 提交sellerTX
    def submitSellerTransInfo(self, transDate, carLocation, operatorId, operatorName, serviceFee, loanAmount, remark,
                              type_purchaseInvoice, photo_purchaseInvoice, name_purchaseInvoice,
                              type_odo, photo_odo, name_odo, type_vccl, photo_vccl, name_vccl,
                              type_partyLetter, photo_partyLetter, name_partyLetter, transId, headers):
        path = "/trans/admin/api/transaction/submitSellerTransInfo"
        res = requests.post(self.url + path, json={
            "transDate": transDate,
            "carLocation": carLocation,
            "operatorId": operatorId,
            "operatorName": operatorName,
            "serviceFee": serviceFee,
            "loanAmount": loanAmount,
            "remark": remark,
            "purchaseInvoice": [{
                "type": type_purchaseInvoice,
                "photo": photo_purchaseInvoice,
                "name": name_purchaseInvoice
            }],
            "odo": [{
                "type": type_odo,
                "photo": photo_odo,
                "name": name_odo
            }],
            "vccl": [{
                "type": type_vccl,
                "photo": photo_vccl,
                "name": name_vccl
            }],
            "partyLetter": [{
                "type": type_partyLetter,
                "photo": photo_partyLetter,
                "name": name_partyLetter
            }],
            "transId": transId
        }, headers=headers)
        return res

    # 获取dealerInfo
    def dealerTransInfo(self, id, headers):
        path = "/trans/admin/api/transaction/dealerTransInfo"
        res = requests.get(self.url + path, params={
            "id": id
        }, headers=headers)
        return res

    # 保存dealeInfo
    def saveDealerTransInfo(self, transDate, registrationFee, interestAmount, payMethod, remark,
                            type_carSalesInvoice, photo_carSalesInvoice, name_carSalesInvoice,
                            type_pdo, photo_pdo, name_pdo, type_receipt, photo_receipt, name_receipt,
                            transId, headers):
        path = "/trans/admin/api/transaction/saveDealerTransInfo"
        res = requests.post(self.url + path, json={
            "transDate": transDate,
            "registrationFee": registrationFee,
            "interestAmount": interestAmount,
            "payMethod": payMethod,
            "remark": remark,
            "carSalesInvoice": [{
                "type": type_carSalesInvoice,
                "photo": photo_carSalesInvoice,
                "name": name_carSalesInvoice
            }],
            "pdo": [{
                "type": type_pdo,
                "photo": photo_pdo,
                "name": name_pdo
            }],
            "receipt": [{
                "type": type_receipt,
                "photo": photo_receipt,
                "name": name_receipt
            }],
            "transId": transId
        }, headers=headers)
        return res

    # 提交dealerInfo
    def submitDealerTransInfo(self, transDate, registrationFee, interestAmount, payMethod, remark,
                              type_carSalesInvoice, photo_carSalesInvoice, name_carSalesInvoice,
                              type_pdo, photo_pdo, name_pdo, type_receipt, photo_receipt, name_receipt,
                              transId, operatorId, operatorName, headers):
        path = "/trans/admin/api/transaction/submitDealerTransInfo"
        res = requests.post(self.url + path, json={
            "transDate": transDate,
            "registrationFee": registrationFee,
            "interestAmount": interestAmount,
            "payMethod": payMethod,
            "remark": remark,
            "carSalesInvoice": [{
                "type": type_carSalesInvoice,
                "photo": photo_carSalesInvoice,
                "name": name_carSalesInvoice
            }],
            "pdo": [{
                "type": type_pdo,
                "photo": photo_pdo,
                "name": name_pdo
            }],
            "receipt": [{
                "type": type_receipt,
                "photo": photo_receipt,
                "name": name_receipt
            }],
            "transId": transId,
            "operatorId": operatorId,
            "operatorName": operatorName
        }, headers=headers)
        return res

    # 取消订单
    def cancelTrans(self, id, comment, headers):
        path = "/trans/admin/api/transaction/cancel"
        res = requests.post(self.url + path, json={
            "id": id,
            "comment": comment
        }, headers=headers)
        return res

    # 订单详情
    def orderDetail(self, id, headers):
        path = "/trans/admin/api/transaction/orderDetail"
        res = requests.get(self.url + path, params={
            "id": id
        }, headers=headers)
        return res

    # 订单历史记录
    def historyTrans(self, id, headers):
        path = "/trans/admin/api/transaction/history"
        res = requests.get(self.url + path, params={
            "id": id
        }, headers=headers)
        return res

    # （服务调用接口） biding 成功生成订单
    def createBiddingOrder(self, dealerId, sellerId, isAgent, carNo, transAmount, isBuyBye, headers):
        path = "/trans/admin/api/transaction/createBiddingOrder"
        res = requests.post(self.url + path, json={
            "dealerId": dealerId,
            "sellerId": sellerId,
            "isAgent": isAgent,
            "carNo": carNo,
            "transAmount": transAmount,
            "isBuyBye": isBuyBye
        }, headers=headers)
        return res

    # (服务调用接口)买断订单
    def createBuyOutOrder(self, carId, carYear, carBrand, carNo, carModel, carLicence, customerType,
                          customerId, price, customerName, phonePrefix, phone, headers):
        path = "/trans/admin/api/transaction/createBuyOutOrder"
        res = requests.post(self.url + path, json={
            "carId": carId,
            "carYear": carYear,
            "carBrand": carBrand,
            "carModel": carModel,
            "carLicence": carLicence,
            "customerType": customerType,
            "customerId": customerId,
            "price": price,
            "customerName": customerName,
            "phonePrefix": phonePrefix,
            "phone": phone
        }, headers=headers)
        return res

    # 生成线下订单
    def createOfflineOrder(self, id, phoneNumber, phonePrefix, email, assignId, headers):
        path = "/trans/admin/api/transaction/createOfflineOrder"
        res = requests.post(self.url + path, json={
            "id": id,
            "phoneNumber": phoneNumber,
            "phonePrefix": phonePrefix,
            "email": email,
            "assignId": assignId
        }, headers=headers)
        print("fangfa=======")
        print("car_no:", id)
        print("dealer_phonePrefix:", phonePrefix)
        print("dealer_phoneNumber:", phoneNumber)
        print("dealer_email:", email)
        print("assign_id:", assignId)
        return res

    # 导出trans
    def exportTrans(self, headers):
        path = "/trans/admin/api/transaction/exportTrans"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 获取检车报告信息
    def reportViewInfo(self, id, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/trans/admin/api/transaction/reportViewInfo/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    '''【仪表盘2.0】'''

    # 获取新增dealer
    def getNewDealerCount(self, startTime, endTime, interval, headers):
        path = "/dealer/admin/api/dealer/getNewDealerCount"
        res = requests.get(self.url + path, params={
            "startTime": startTime,
            "endTime": endTime,
            "interval": interval
        }, headers=headers)
        return res

    # 获取dealer新增统计数据
    def getNewDealerStatics(self, dayStart, dayEnd, weekStart, weekEnd, monthStart, monthEnd, lastWeekStart,
                            lastWeekEnd, lastMonthStart, lastMonthEnd, headers):
        path = "/dealer/admin/api/dealer/getNewDealerStatics"
        res = requests.get(self.url + path, params={
            "dayStart": dayStart,
            "dayEnd": dayEnd,
            "weekStart": weekStart,
            "weekEnd": weekEnd,
            "monthStart": monthStart,
            "monthEnd": monthEnd,
            "lastWeekStart": lastWeekStart,
            "lastWeekEnd": lastWeekEnd,
            "lastMonthStart": lastMonthStart,
            "lastMonthEnd": lastMonthEnd
        }, headers=headers)
        return res

    # 获取新增seller
    def getNewSellerCount(self, startTime, endTime, interval, headers):
        path = "/seller/admin/api/seller/getNewSellerCount"
        res = requests.get(self.url + path, params={
            "startTime": startTime,
            "endTime": endTime,
            "interval": interval
        }, headers=headers)
        return res

    # 获取seller新增统计数据
    def getNewSellerStatics(self, dayStart, dayEnd, weekStart, weekEnd, monthStart, monthEnd, lastWeekStart,
                            lastWeekEnd, lastMonthStart, lastMonthEnd, headers):
        path = "/seller/admin/api/seller/getNewSellerStatics"
        res = requests.get(self.url + path, params={
            "dayStart": dayStart,
            "dayEnd": dayEnd,
            "weekStart": weekStart,
            "weekEnd": weekEnd,
            "monthStart": monthStart,
            "monthEnd": monthEnd,
            "lastWeekStart": lastWeekStart,
            "lastWeekEnd": lastWeekEnd,
            "lastMonthStart": lastMonthStart,
            "lastMonthEnd": lastMonthEnd
        }, headers=headers)
        return res

    # 获取新增SalesAgent
    def getNewSalesAgentCount(self, startTime, endTime, interval, headers):
        path = "/sa/admin/api/sa/getNewSalesAgentCount"
        res = requests.get(self.url + path, params={
            "startTime": startTime,
            "endTime": endTime,
            "interval": interval
        }, headers=headers)
        return res

    # 获取SalesAgent新增统计数据
    def getNewSalesAgentStatics(self, dayStart, dayEnd, weekStart, weekEnd, monthStart, monthEnd, lastWeekStart,
                                lastWeekEnd, lastMonthStart, lastMonthEnd, headers):
        path = "/sa/admin/api/sa/getNewSalesAgentStatics"
        res = requests.get(self.url + path, params={
            "dayStart": dayStart,
            "dayEnd": dayEnd,
            "weekStart": weekStart,
            "weekEnd": weekEnd,
            "monthStart": monthStart,
            "monthEnd": monthEnd,
            "lastWeekStart": lastWeekStart,
            "lastWeekEnd": lastWeekEnd,
            "lastMonthStart": lastMonthStart,
            "lastMonthEnd": lastMonthEnd
        }, headers=headers)
        return res

    # 获取统计数据
    def getStatics(self, headers):
        path = "/inspector/admin/api/inspector/getStatics"
        res = requests.get(self.url + path, headers=headers)
        return res

    '''【通知2.0】'''

    # 清空
    def setEmpty(self, tag, headers):
        path = "/user/admin/api/account/setEmpty"
        res = requests.post(self.url + path, json={
            "tag": tag
        }, headers=headers)
        return res

    # sendNotification
    def sendUserNotification(self, type, userId, data, headers):
        path = "/user/admin/api/account/sendUserNotification"
        res = requests.post(self.url + path, json={
            "type": type,
            "userId": userId,
            "content": {
                "data": data
            }
        }, headers=headers)
        return res

    # 获取通知列表
    def getNotificationList(self, tag, headers):
        path = "/user/admin/api/account/getNotificationList"
        res = requests.get(self.url + path, params={
            "tag": tag
        }, headers=headers)
        return res

    '''【Seller Crm】'''

    # seller手机号登录
    def loginByPhoneSeller(self, phonePrefix, phoneNumber, password, headers):
        path = "/seller/api/seller/loginByPhone"
        res = requests.post(self.url + path, json={
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber,
            "password": password
        }, headers=headers)
        return res

    # 获取大厅车辆列表
    def getCarListBidding(self, headers):
        path = "/bidding/api/bidding/getCarList"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 获取车辆竞标详细信息
    def getCarBiddingBlockInfo(self, carId, biddingBlockId, headers):
        path = "/bidding/api/bidding/getCarBiddingBlockInfo"
        res = requests.get(self.url + path, params={
            "carId": carId,
            "biddingBlockId": biddingBlockId
        }, headers=headers)
        return res

    # seller通过手机重置密码申请
    def resetPasswordApplyByPhone(self, phonePrefix, phoneNumber, headers):
        path = "/seller/api/seller/resetPasswordApplyByPhone"
        res = requests.post(self.url + path, json={
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber
        }, headers=headers)
        return res

    # seller通过邮箱重置密码申请
    def resetPasswordApplyByEmail(self, email, headers):
        path = "/seller/api/seller/resetPasswordApplyByEmail"
        res = requests.post(self.url + path, json={
            "email": email
        }, headers=headers)
        return res

    # seller邮箱登录
    def loginByEmail(self, email, password, headers):
        path = "/seller/api/seller/loginByEmail"
        res = requests.post(self.url + path, json={
            "email": email,
            "password": password
        }, headers=headers)
        return res

    # seller重置密码验证
    def resetPasswordVerifyByPhone(self, phonePrefix, phoneNumber, verifyCodeId, verifyCode, headers):
        path = "/seller/api/seller/resetPasswordVerifyByPhone"
        res = requests.post(self.url + path, json={
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber,
            "verifyCodeId": verifyCodeId,
            "verifyCode": verifyCode
        }, headers=headers)
        return res

    # seller通过手机重置密码
    def resetPasswordByPhone(self, password, verifyCodeId, verifyCode, headers):
        path = "/seller/api/seller/resetPasswordByPhone"
        res = requests.post(self.url + path, json={
            "password": password,
            "verifyCodeId": verifyCodeId,
            "verifyCode": verifyCode
        }, headers=headers)
        return res

    # seller通过邮箱重置密码
    def resetPasswordByEmail(self, password, token, headers):
        path = "/seller/api/seller/resetPasswordByEmail"
        res = requests.post(self.url + path, json={
            "password": password,
            "token": token
        }, headers=headers)
        return res

    # seller修改密码
    def changePasswordSeller(self, newPassword, oldPassword, headers):
        path = "/seller/api/seller/changePassword"
        res = requests.post(self.url + path, json={
            "newPassword": newPassword,
            "oldPassword": oldPassword
        }, headers=headers)
        return res

    # seller获取用户信息
    def getSellerInfo(self, headers):
        path = "/seller/api/seller/getSellerInfo"
        res = requests.get(self.url + path, headers=headers)
        return res

    # seller检查邮箱是否可用
    def checkEmailSeller(self, email, headers):
        path = "/seller/api/seller/checkEmail"
        res = requests.post(self.url + path, json={
            "email": email
        }, headers=headers)
        return res

    # seller登出
    def logoutSeller(self, email, headers):
        path = "/seller/api/seller/logout"
        res = requests.post(self.url + path, headers=headers)
        return res

    # 获取竞标历史列表
    def getCarBiddingBlockHistory(self, headers):
        path = "/bidding/api/bidding/getCarBiddingBlockHistory"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 获取车辆竞标历史详情
    def getCarBiddingBlockHistoryInfo(self, carId, biddingBlockId, headers):
        path = "/bidding/api/bidding/getCarBiddingBlockHistoryInfo"
        res = requests.get(self.url + path, params={
            "carId": carId,
            "biddingBlockId": biddingBlockId
        }, headers=headers)
        return res

    # seller检查手机号是否可用
    def checkPhoneNumber(self, phonePrefix, phoneNumber, headers):
        path = "/seller/api/seller/checkPhoneNumber"
        res = requests.post(self.url + path, json={
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber
        }, headers=headers)
        return res

    # 编辑中标意见
    def editSellerComment(self, carId, biddingBlockId, comment, headers):
        path = "/bidding/api/bidding/editSellerComment"
        res = requests.post(self.url + path, json={
            "carId": carId,
            "biddingBlockId": biddingBlockId,
            "comment": comment
        }, headers=headers)
        return res

    # seller修改用户信息
    def editSellerInfo(self, carId, biddingBlockId, comment, headers):
        path = "/bidding/api/bidding/editSellerComment"
        res = requests.post(self.url + path, json={
            "carId": carId,
            "biddingBlockId": biddingBlockId,
            "comment": comment
        }, headers=headers)
        return res

    '''【SA App】'''

    # 登陆Sa
    def loginSa(self, phonePrefix, phoneNumber, password, headers):
        path = "/sa/api/sa/login"
        res = requests.post(self.url + path, json={
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber,
            "password": password
        }, headers=headers)
        return res

    # 验证码登陆
    def loginVerifyCode(self, phonePrefix, phoneNumber, verifyCodeId, verifyCode, headers):
        path = "/sa/api/sa/loginVerifyCode"
        res = requests.post(self.url + path, json={
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber,
            "verifyCodeId": verifyCodeId,
            "verifyCode": verifyCode
        }, headers=headers)
        return res

    # 发送验证码
    def sendVerifyCode(self, phonePrefix, phoneNumber, headers):
        path = "/lead/api/sendVerifyCode"
        res = requests.post(self.url + path, json={
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber
        }, headers=headers)
        return res

    # 创建lead
    def createLeadSa(self, carYear, carBrand, carModel, customerName, customerPhonePrefix, customerPhone,
                     checkTime, checkDetailAddress, checkCity, checkRegion, checkPostcode, headers):
        path = "/sa/api/sa/createLead"
        res = requests.post(self.url + path, json={
            "carYear": carYear,
            "carBrand": carBrand,
            "carModel": carModel,
            "customerName": customerName,
            "customerPhonePrefix": customerPhonePrefix,
            "customerPhone": customerPhone,
            "checkTime": checkTime,
            "checkDetailAddress": checkDetailAddress,
            "checkCity": checkCity,
            "checkRegion": checkRegion,
            "checkPostcode": checkPostcode
        }, headers=headers)
        return res

    # 查询lead
    def leadList(self, type, current, pageSize, headers):
        path = "/sa/api/sa/leadList/"
        res = requests.get(self.url + path + type, params={
            "current": current,
            "pageSize": pageSize
        }, headers=headers)
        return res

    # 获取brand
    def getAllCarBrand(self, headers):
        path = "/sa/admin/api/sa/getAllCarBrand"
        res = requests.get(self.url + path, headers=headers)
        return res

    '''【SA Crm】'''

    # 登出Sa
    def logoutSa(self, headers):
        path = "/sa/api/sa/logout"
        res = requests.post(self.url + path, headers=headers)
        return res

    # 更换密码Sa
    def changePasswordSa(self, oldPassword, newPassword, headers):
        path = "/sa/api/sa/changePassword"
        res = requests.post(self.url + path, json={
            "oldPassword": oldPassword,
            "newPassword": newPassword
        }, headers=headers)
        return res

    # 通过手机重置密码Sa
    def resetPasswordSa(self, password, verifyCodeId, verifyCode, email, headers):
        path = "/sa/api/sa/resetPassword"
        res = requests.post(self.url + path, json={
            "password": password,
            "verifyCodeId": verifyCodeId,
            "verifyCode": verifyCode,
            "email": email
        }, headers=headers)
        return res

    # 重置密码验证Sa
    def resetPasswordVerifySa(self, phonePrefix, phoneNumber, verifyCodeId, verifyCode, headers):
        path = "/sa/api/sa/resetPasswordVerify"
        res = requests.post(self.url + path, json={
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber,
            "verifyCodeId": verifyCodeId,
            "verifyCode": verifyCode
        }, headers=headers)
        return res

    # agent通过手机重置密码申请
    def resetPasswordApplySa(self, phonePrefix, phoneNumber, headers):
        path = "/sa/api/sa/resetPasswordApply"
        res = requests.post(self.url + path, json={
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber
        }, headers=headers)
        return res

    # agent通过邮箱重置密码申请
    def resetPasswordApplyByEmailSa(self, email, headers):
        path = "/sa/api/sa/resetPasswordApplyByEmail"
        res = requests.post(self.url + path, json={
            "email": email
        }, headers=headers)
        return res

    # agent手机号登录
    def loginByPhoneSa(self, phonePrefix, phoneNumber, password, headers):
        path = "/sa/api/sa/loginByPhone"
        res = requests.post(self.url + path, json={
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber,
            "password": password
        }, headers=headers)
        return res

    # agent邮箱登录
    def loginByEmailSa(self, email, password, headers):
        path = "/sa/api/sa/loginByEmail"
        res = requests.post(self.url + path, json={
            "email": email,
            "password": password
        }, headers=headers)
        return res

    # agent通过邮箱重置密码
    def resetPasswordByEmailSa(self, password, token, headers):
        path = "/sa/api/sa/resetPasswordByEmail"
        res = requests.post(self.url + path, json={
            "password": password,
            "token": token
        }, headers=headers)
        return res

    # agent获取用户信息
    def getSalesAgentInfo(self, headers):
        path = "/sa/api/sa/getSalesAgentInfo"
        res = requests.get(self.url + path, headers=headers)
        return res

    # agent检查邮箱是否可用
    def checkEmailSa(self, email, headers):
        path = "/sa/api/sa/checkEmail"
        res = requests.post(self.url + path, json={
            "email": email
        }, headers=headers)
        return res

    # agent检查手机号是否可用
    def checkPhoneNumberSa(self, phonePrefix, phoneNumber, headers):
        path = "/sa/api/sa/checkPhoneNumber"
        res = requests.post(self.url + path, json={
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber
        }, headers=headers)
        return res

    # agent修改用户信息
    def editSalesAgentInfo(self, email, name, headers):
        path = "/sa/api/sa/editSalesAgentInfo"
        res = requests.post(self.url + path, json={
            "email": email,
            "name": name
        }, headers=headers)
        return res

    '''【Account账户管理2.0】'''

    # loginUser
    def loginUser(self, username, password, verifyCodeId, verifyCode, ):
        path = "/user/admin/api/account/login"
        res = requests.post(self.url + path, json={
            "username": username,
            "password": password,
            "verifyCodeId": verifyCodeId,
            "verifyCode": verifyCode
        })
        return res

    # logoutUser
    def logoutUser(self, headers):
        path = "/user/admin/api/account/logout"
        res = requests.post(self.url + path, headers=headers)
        return res

    # 获取所有车辆品牌
    def getAllCarBrandUser(self, headers):
        path = "/user/admin/api/account/getAllCarBrand"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 获取检车STS
    def getCheckerSTS(self, photo, headers):
        path = "/user/admin/api/account/getCheckerSTS"
        res = requests.get(self.url + path, params={
            "path": photo
        }, headers=headers)
        return res

    # 检车APP登录
    def checkerLogin(self, username, password):
        path = "/user/admin/api/account/checkerLogin"
        res = requests.post(self.url + path, json={
            "username": username,
            "password": password
        })
        return res

    # 获取用户信息
    def getUserInfo(self, headers):
        path = "/user/admin/api/account/getUserInfo"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 获取验证码图片
    def getVerifyCodeImage(self):
        """获取验证码图片"""
        path = "/user/admin/api/account/getVerifyCodeImage"
        res = requests.get(self.url + path)  # 拼接url
        verifyCodeId = res.json()['data']['verifyCodeId']
        return verifyCodeId

    # 验证二步验证
    def verifyTFA(self, code, headers):
        path = "/user/admin/api/account/verifyTFA"
        res = requests.post(self.url + path, json={
            "code": code
        }, headers=headers)
        print("code:", code)
        return res

    # 修改密码
    def changePasswordUser(self, newPassword, oldPassword, headers):
        path = "/user/admin/api/account/changePassword"
        res = requests.post(self.url + path, json={
            "newPassword": newPassword,
            "oldPassword": oldPassword
        }, headers=headers)
        return res

    # 获取任务
    def getTasks(self, headers):
        path = "/user/admin/api/account/getTasks"
        res = requests.get(self.url + path, headers=headers)
        return res

    '''【Lead 2.0】'''

    # admin新建lead
    def newLead(self, carYear, carBrand, carType, carModel, applyName, applyTel, applyTelCode, applyMail, checkTime,
                checkDetailAddress,
                checkCity, checkRegion, checkPostcode, headers):
        path = "/lead/admin/api/lead/new"
        # print("carYear",carYear,
        #     "carBrand",carBrand,
        #     "carType",carType,
        #     "carModel",carModel,
        #     "applyName",applyName,
        #     "applyTel",applyTel,
        #     "applyTelCode",applyTelCode,
        #     "applyMail",applyMail,
        #     "checkTime",checkTime,
        #     "checkDetailAddress",checkDetailAddress,
        #     "checkCity",checkCity,
        #     "checkRegion",checkRegion,
        #     "checkPostcode",checkPostcode)
        res = requests.post(self.url + path, json={
            "carYear": carYear,
            "carBrand": carBrand,
            "carType": carType,
            "carModel": carModel,
            "applyName": applyName,
            "applyTel": applyTel,
            "applyTelCode": applyTelCode,
            "applyMail": applyMail,
            "checkTime": checkTime,
            "checkDetailAddress": checkDetailAddress,
            "checkCity": checkCity,
            "checkRegion": checkRegion,
            "checkPostcode": checkPostcode
        }, headers=headers)

        return res

    # 查询等待预检的lead
    def unchecked(self, current, pageSize, headers):
        path = "/lead/admin/api/lead/query/unchecked"
        res = requests.get(self.url + path, params={
            "current": current,
            "pageSize": pageSize
        }, headers=headers)
        return res

    # 指派经办人(customer service)
    def assignCustomerService(self, leadNo, assignId, resourceId, headers):
        path = "/lead/admin/api/lead/assignCustomerService"
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        res = requests.post(self.url + path, json={
            "leadNo": leadNo,
            "assignId": assignId
        }, headers=headers)
        return res

    # 获取lead详情
    def infoLead(self, id, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/lead/admin/api/lead/info/"
        res = requests.get(self.url + path + id, headers=headers)

        return res

    # 关联seller
    def associateSellerLead(self, leadNo, customerId, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/lead/admin/api/lead/associateSeller"
        res = requests.post(self.url + path, json={
            "leadNo": leadNo,
            "customerId": customerId
        }, headers=headers)
        return res

    # 编辑lead基础信息
    def editLead(self, carYear, carBrand, carType, carModel, applyName, applyTel, applyTelCode, applyMail, checkTime,
                 checkDetailAddress, checkPostcode, checkRegion, checkCity, leadNo, remark, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/lead/admin/api/lead/edit"
        res = requests.post(self.url + path, json={
            "carYear": carYear,
            "carBrand": carBrand,
            "carType": carType,
            "carModel": carModel,
            "applyName": applyName,
            "applyTel": applyTel,
            "applyTelCode": applyTelCode,
            "applyMail": applyMail,
            "checkTime": checkTime,
            "checkDetailAddress": checkDetailAddress,
            "checkPostcode": checkPostcode,
            "checkRegion": checkRegion,
            "checkCity": checkCity,
            "leadNo": leadNo,
            "remark": remark
        }, headers=headers)
        return res

    # 终止lead
    def finishLead(self, leadNo, comment, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/lead/admin/api/lead/finish"
        res = requests.post(self.url + path, json={
            "leadNo": leadNo,
            "comment": comment
        }, headers=headers)
        return res

    # 查询完成的lead
    def checkedLead(self, current, pageSize, headers):
        path = "/lead/admin/api/lead/query/checked"
        res = requests.get(self.url + path, json={
            "current": current,
            "pageSize": pageSize
        }, headers=headers)
        return res

    # 编辑车辆户口
    def changeCarCard(self, carType, cardUrl, leadNo, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/lead/admin/api/lead/changeCarCard"
        res = requests.post(self.url + path, json={
            "carType": carType,
            "cardUrl": cardUrl,
            "leadNo": leadNo
        }, headers=headers)
        return res

    # lead异常
    def exception(self, leadNo, comment, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/lead/admin/api/lead/exception"
        res = requests.post(self.url + path, json={
            "leadNo": leadNo,
            "comment": comment
        }, headers=headers)
        return res

    # lead申请确认
    def checkLead(self, leadNo, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/lead/admin/api/lead/check"
        res = requests.post(self.url + path, json={
            "leadNo": leadNo
        }, headers=headers)
        print(leadNo)
        print(resourceId)
        print(headers)
        return res

    # 获取customerService成员
    def customerServiceMembers(self, headers):
        path = "/lead/admin/api/lead/customerServiceMembers"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 获取corporate成员
    def corporateMembers(self, headers):
        path = "/lead/admin/api/lead/corporateMembers"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 查询异常lead
    def abnormal(self, carBrand, current, pageSize, search, carYear, createdTime, sorter, headers):
        path = "/lead/admin/api/lead/query/abnormal"
        res = requests.get(self.url + path, params={
            "carBrand": carBrand,
            "current": current,
            "pageSize": pageSize,
            "search": search,
            "carYear": carYear,
            "createdTime": createdTime,
            "sorter": sorter
        }, headers=headers)

        return res

    # 指派经办人（Corporate）
    def assignCorporate(self, leadNo, assignId, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/lead/admin/api/lead/assignCorporate"
        res = requests.post(self.url + path, json={
            "leadNo": leadNo,
            "assignId": assignId
        }, headers=headers)
        return res

    # 取消关联系统用户
    def disassociateLead(self, leadNo, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/lead/admin/api/lead/disassociate"
        res = requests.post(self.url + path, json={
            "leadNo": leadNo
        }, headers=headers)
        return res

    # lead创建seller
    def leadNewSeller(self, phoneNumber, phonePrefix, type, email, name, headers):
        path = "/seller/admin/api/seller/leadNewSeller"
        res = requests.post(self.url + path, json={
            "phoneNumber": phoneNumber,
            "phonePrefix": phonePrefix,
            "type": type,
            "email": email,
            "name": name
        }, headers=headers)
        return res

    # lead创建agent
    def leadNewSalesAgent(self, phoneNumber, name, phonePrefix, type, email, headers):
        path = "/sa/admin/api/sa/leadNewSalesAgent"
        res = requests.post(self.url + path, json={
            "phoneNumber": phoneNumber,
            "name": name,
            "phonePrefix": phonePrefix,
            "type": type,
            "email": email
        }, headers=headers)
        return res

    # 关联agent
    def associateSalesAgent(self, leadNo, customerId, resourceId, headers):
        headers.update({'resourceId': resourceId})  # 更新headers，插入resourceId
        path = "/lead/admin/api/lead/associateSalesAgent"
        res = requests.post(self.url + path, json={
            "leadNo": leadNo,
            "customerId": customerId
        }, headers=headers)
        return res

    # 主页获取验证码
    def sendVerifyCodeLead(self, phoneNumber, phonePrefix, headers):
        path = "/lead/api/sendVerifyCode"
        res = requests.post(self.url + path, params={
            "phoneNumber": phoneNumber,
            "phonePrefix": phonePrefix
        }, headers=headers)
        return res

    # 主页创建订单
    def createLeadLead(self, carYear, carBrand, carType, carModel, applyName, phonePrefix, phoneNumber,
                       remark, checkTime, checkDetailAddress, checkCity, checkRegion, checkPostcode, verifyCode,
                       headers):
        path = "/lead/api/createLead"
        res = requests.post(self.url + path, json={
            "carYear": carYear,
            "carBrand": carBrand,
            "carType": carType,
            "carModel": carModel,
            "applyName": applyName,
            "phonePrefix": phonePrefix,
            "phoneNumber": phoneNumber,
            "remark": remark,
            "checkTime": checkTime,
            "checkDetailAddress": checkDetailAddress,
            "checkCity": checkCity,
            "checkRegion": checkRegion,
            "checkPostcode": checkPostcode,
            "verifyCode": verifyCode
        }, headers=headers)
        print(phonePrefix, phoneNumber, verifyCode)
        return res

    # 获取车牌信息
    def carBrands(self, headers):
        path = "/lead/api/carBrands"
        res = requests.get(self.url + path, headers=headers)
        return res

    '''【User用户管理模块2.0】'''

    # 创建用户组
    def createGroup(self, title, roles, parentId, headers):
        """创建用户组"""
        path = "/user/admin/api/user/createGroup"
        res = requests.post(self.url + path, json={
            "title": title,
            "roles": roles,
            "parentId": parentId
        }, headers=headers)
        # print("打印传参：",
        # {
        #     "title":title,
        #     "roles": [],
        #     "parentId":parentId
        # },headers)
        return res

    # 修改admin用户邮箱
    def editUserEmail(self, id, email, headers):
        """修改admin用户邮箱"""
        path = "/user/admin/api/user/editUserEmail"
        res = requests.post(self.url + path, json={
            "id": id,
            "email": email
        }, headers=headers)
        return res

    # 修改admin用户姓名
    def editUsername(self, id, name, headers):
        """修改admin用户姓名"""
        path = "/user/admin/api/user/editUsername"
        res = requests.post(self.url + path, json={
            "id": id,
            "name": name
        }, headers=headers)
        return res

    # 修改admin用户密码
    def resetpassword(self, id, newPassword, setDisable, headers):
        """修改admin用户密码"""
        path = "/user/admin/api/user/resetPassword"
        res = requests.post(self.url + path, json={
            "id": id,
            "newPassword": newPassword,
            "setDisable	": setDisable
        }, headers=headers)
        return res

    # 修改交易员姓名
    def changeNameTrader(self, userId, name, headers):
        """修改交易员姓名"""
        path = "/user/admin/api/trader/changeName"
        res = requests.post(self.url + path, json={
            "userId": userId,
            "name": name
        }, headers=headers)
        return res

    # 新建检车员
    def newChecker(self, username, password, name, email, headers):
        """新建检车员"""
        # print(username,password,name,email,headers)
        path = "/user/admin/api/checker/new"
        res = requests.post(self.url + path, json={
            "username": username,
            "password": password,
            "name": name,
            "email": email
        }, headers=headers)
        # print(username,password,name,email,headers)
        return res

    # 绑定二步验证
    def bindTFA(self, id, secret, code, headers):
        path = "/user/admin/api/user/bindTFA"
        res = requests.post(self.url + path, json={
            "id": id,
            "secret": secret,
            "code": code
        }, headers=headers)
        # print("id:",id)
        # print("secret:",secret)
        # print("code:",code)
        return res

    # 解除二步验证
    def clearTFA(self, id, headers):
        path = "/user/admin/api/user/clearTFA"
        res = requests.post(self.url + path, json={
            "id": id
        }, headers=headers)
        return res

    # 获取二步验证二维码
    def getQRBarcode(self, username, headers):
        path = "/user/admin/api/user/getQRBarcode"
        res = requests.get(self.url + path, params={"username": username}, headers=headers)
        return res

    # 验证邮箱是否可用User
    def checkEmailUser(self, email, headers):
        path = "/user/admin/api/user/checkEmail"
        res = requests.post(self.url + path, json={
            "email": email
        }, headers=headers)
        return res

    # 查询检车员
    def queryChecker(self, pageSize, current, headers):
        path = "/user/admin/api/checker/query"
        res = requests.get(self.url + path, params={
            "pageSize": pageSize,
            "current": current
        }, headers=headers)
        return res

    # 检查用户名是否可用
    def checkUsername(self, username, headers):
        path = "/user/admin/api/user/checkUsername"
        res = requests.post(self.url + path, json={
            "username": username
        }, headers=headers)
        return res

    # 重置检车员密码
    def resetPasswordChecker(self, id, password, headers):
        path = "/user/admin/api/checker/resetPassword"
        res = requests.post(self.url + path, json={
            "id": id,
            "password": password
        }, headers=headers)
        return res

    # 修改检车员邮箱
    def changeEmailChecker(self, id, email, headers):
        path = "/user/admin/api/checker/changeEmail"
        res = requests.post(self.url + path, json={
            "id": id,
            "email": email
        }, headers=headers)
        return res

    # 修改检车员姓名
    def changeNameChecker(self, id, username, headers):
        path = "/user/admin/api/checker/changeName"
        res = requests.post(self.url + path, json={
            "id": id,
            "username": username
        }, headers=headers)
        return res

    # 注销交易员
    def logoffTrader(self, userId, headers):
        path = "/user/admin/api/trader/logoff"
        res = requests.post(self.url + path, json={
            "userId": userId
        }, headers=headers)
        return res

    # 注销检车员
    def logoffChecker(self, id, headers):
        path = "/user/admin/api/checker/logoff"
        res = requests.post(self.url + path, json={
            "id": id
        }, headers=headers)
        return res

    # 检验用户组内用户是否可以被删除
    def checkGroupUser(self, id, headers):
        path = "/user/admin/api/user/checkGroupUser"
        res = requests.post(self.url + path, json={
            "id	": id
        }, headers=headers)
        return res

    # 检查admin用户是否可以被注销
    def checkUser(self, id, headers):
        path = "/user/admin/api/user/checkUser"
        res = requests.post(self.url + path, json={
            "id	": id
        }, headers=headers)
        return res

    # 注销admin用户
    def deleteUser(self, id, headers):
        path = "/user/admin/api/user/deleteUser"
        res = requests.post(self.url + path, json={
            "id": id
        }, headers=headers)
        print(id, headers)
        return res

    # 获取用户下级用户组用户信息
    def getGroupUsers(self, userId, roles, headers):
        path = "/user/admin/api/user/getGroupUsers"
        res = requests.get(self.url + path, params={
            "userId": userId,
            "roles": roles
        }, headers=headers)
        return res

    # 编辑用户组信息
    def editGroupInfo(self, groupId, title, roles, groupUsers, headers):
        path = "/user/admin/api/user/editGroupInfo"
        res = requests.post(self.url + path, json={
            "groupId": groupId,
            "title": title,
            "roles": roles,
            "groupUsers": groupUsers

        }, headers=headers)
        return res

    # 获取用户组角色列表
    def getGroupRoles(self, id, headers):
        path = "/user/admin/api/user/getGroupRoles/"
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 获取用户组信息
    def getGroupInfo(self, id, headers):
        path = "/user/admin/api/user/getGroupInfo/"
        # print("id:",id)#打印参数
        res = requests.get(self.url + path + id, headers=headers)
        return res

    # 获取admin所有用户
    def allUsers(self, pageSize, current, headers):
        """获取admin所有用户"""
        path = "/user/admin/api/user/getUserList"
        res = requests.get(self.url + path, params={
            "pageSize": pageSize,
            "current": current
        }, headers=headers)
        return res

    # 获取admin用户列表
    def getUsers(self, headers):
        """获取admin用户列表"""
        path = "/user/admin/api/user/getUsers"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 获取用户组树
    def groupTree(self, headers):
        path = "/user/admin/api/user/groupTree"
        res = requests.get(self.url + path, headers=headers)
        return res

    # 删除用户组
    def deleteGroup(self, id, headers):
        path = "/user/admin/api/user/deleteGroup"
        res = requests.post(self.url + path, json={
            "id": id
        }, headers=headers)
        return res

    # 创建用户
    def createUser(self, username, password, email, name, enabled, headers):
        path = "/user/admin/api/user/createUser"
        res = requests.post(self.url + path, json={
            "username": username,
            "password": password,
            "email": email,
            "name": name,
            "enabled": enabled
        }, headers=headers)
        # print(username)
        return res

    # 重置密码
    def resetPassword(self, username, newPassword, setDisable, headers):
        path = "/user/admin/api/user/resetPassword"
        res = requests.post(self.url + path, json={
            "username": username,
            "newPassword": newPassword,
            "setDisable": setDisable
        }, headers=headers)
        return res

    # 新建交易员
    def newTrader(self, role, username, email, headers):
        path = "/user/admin/api/trader/new"
        res = requests.post(self.url + path, json={
            "role": role,
            "username": username,
            "email": email
        }, headers=headers)
        return res

    # 交易员查询
    def queryTrader(self, pageSize, current, headers):
        path = "/user/admin/api/trader/query"
        res = requests.get(self.url + path, params={
            "pageSize": pageSize,
            "current": current
        }, headers=headers)
        return res

    # 修改交易员邮箱
    def changeEmailTrader(self, userId, email, headers):
        path = "/user/admin/api/trader/changeEmail"
        res = requests.post(self.url + path, json={
            "userId": userId,
            "email": email
        }, headers=headers)
        return res

    # 获取STS
    def getSTS(self, headers):
        path = "/user/admin/api/account/getSTS"
        res = requests.get(self.url + path, headers=headers)
        return res