from common.TestInterface import Interface
from common.TestRedis import Redis
import pytest
import json
import time
import random
import hmac, base64, struct, hashlib, time
from common.TestCommon import getVerifyCodeImage, getRedis, loginTrue, SetPhone, \
                                Unicode, GBK2312, GetHeaders, TimeNow, Now

inter = Interface()
Random = TimeNow()


# 1.创建用户组
def get_roles():
    getGroupRoles = inter.getGroupRoles(
        id="1",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getGroupRoles:", getGroupRoles.json())
    print("-" * 100)
    role_names = list(map(lambda x: x['name'], getGroupRoles.json()['data']))
    print("role_names:", role_names)
    print("-" * 100)
    return role_names


def test_createGroup():
    createGroup = inter.createGroup(
        title="Group" + Random,
        roles=get_roles(),
        parentId="1",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createGroup:", createGroup.json())
    print("-" * 100)
    assert str(createGroup.json()['success']) == "True"
    group_id = str(createGroup.json()['data']['id'])
    return group_id


# 2.编辑用户组信息
def get_groupusers():
    group_info = inter.getGroupInfo(
        id=test_createGroup(),
        headers=GetHeaders()
    )
    group_users = list(map(lambda x: x['id'], group_info.json()['data']['groupUsers']))
    print("-" * 100)
    print("group_users:", group_users)
    print("-" * 100)
    return group_users


def get_rolesid():
    getGroupRoles = inter.getGroupRoles(
        id="1",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("1.获取用户组角色列表,返回:", getGroupRoles.json())
    print("-" * 100)
    role_ids = list(map(lambda x: x['id'], getGroupRoles.json()['data']))
    print("role_ids:", role_ids)
    print("-" * 100)
    return role_ids


def test_editGroupInfo():
    editGroupInfo = inter.editGroupInfo(
        groupId=test_createGroup(),
        title="Group" + Random,
        roles=get_rolesid(),
        groupUsers=get_groupusers(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("editGroupInfo:", editGroupInfo.json())
    print("-" * 100)
    assert str(editGroupInfo.json()['success']) == "True"


# 3.获取用户组树
def test_groupTree():
    groupTree = inter.groupTree(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("groupTree:", groupTree.json())
    print("-" * 100)
    assert str(groupTree.json()['success']) == "True"


# 4.删除用户组
def test_deleteGroup():
    deleteGroup = inter.deleteGroup(
        id=test_createGroup(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("deleteGroup:", deleteGroup.json())
    print("-" * 100)
    assert str(deleteGroup.json()['success']) == "True"


# 5.获取用户组角色列表
def test_getGroupRoles():
    getGroupRoles = inter.getGroupRoles(
        id=test_createGroup(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getGroupRoles:", getGroupRoles.json())
    print("-" * 100)
    assert str(getGroupRoles.json()['success']) == "True"


# 6.获取用户组信息
def test_getGroupInfo():
    getGroupInfo = inter.getGroupInfo(
        id=test_createGroup(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getGroupInfo:", getGroupInfo.json())
    print("-" * 100)
    assert str(getGroupInfo.json()['success']) == "True"


# 7.获取admin所有用户
def test_getUserList():
    getUserList = inter.allUsers(
        pageSize="9999",
        current="1",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getUserList:", getUserList.json())
    print("-" * 100)
    assert str(getUserList.json()['success']) == "True"
    user_id = str(getUserList.json()['data'][0]['id'])
    username = str(getUserList.json()['data'][0]['username'])
    print("-" * 100)
    print("user_id:", user_id, "username:", username)
    print("-" * 100)
    return user_id


# 8.获取admin用户列表
def test_getUsers():
    getUsers = inter.getUsers(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getUsers:", getUsers.json())
    print("-" * 100)
    assert str(getUsers.json()['success']) == "True"
    user_id = str(getUsers.json()['data'][-1]['id'])
    print("user_id:", user_id)
    return user_id


# 9.创建用户
def test_createUser():
    createUser = inter.createUser(
        username="User" + Random,
        password="qwer`123",
        email="User" + Random + "@user.com",
        name=Unicode() + GBK2312() + Random,
        enabled=True,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("createUser:", createUser.json())
    print("-" * 100)
    assert str(createUser.json()['success']) == "True"


# 10.修改admin用户邮箱
def get_userid():
    getUsers = inter.getUsers(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getUsers:", getUsers.json())
    print("-" * 100)
    user_id = str(getUsers.json()['data'][0]['id'])
    print("-" * 100)
    print("user_id:", user_id)
    print("-" * 100)
    return user_id


def test_editUserEmail():
    editUserEmail = inter.editUserEmail(
        id=get_userid(),
        email="MvUser" + Random + "@user.change",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("editUserEmail:", editUserEmail.json())
    print("-" * 100)
    assert str(editUserEmail.json()['success']) == "True"


# 11.修改admin用户姓名
def test_editUsername():
    editUsername = inter.editUsername(
        id=get_userid(),
        name=Unicode() + GBK2312() + "Changed",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("editUsername:", editUsername.json())
    print("-" * 100)
    assert str(editUsername.json()['success']) == "True"


# 12.修改admin用户密码
def test_resetpassword():
    resetpassword = inter.resetpassword(
        id=get_userid(),
        newPassword="qwer`123",
        setDisable=False,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("resetpassword:", resetpassword.json())
    print("-" * 100)
    assert str(resetpassword.json()['success']) == "True"


# 13.新建交易员
# 13.1 sellerTrader
def test_sellerTradernew():
    newsellerTrader = inter.newTrader(
        role="sellerTrader",
        username="ST" + Random,
        email="ST" + Random + "@st.com",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("newsellerTrader:", newsellerTrader.json())
    print("-" * 100)
    assert str(newsellerTrader.json()['success']) == "True"


# 13.2 dealerTrader
def test_dealerTradernew():
    newdealerTrader = inter.newTrader(
        role="dealerTrader",
        username="DT" + Random,
        email="DT" + Random + "@dt.com",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("newdealerTrader:", newdealerTrader.json())
    print("-" * 100)
    assert str(newdealerTrader.json()['success']) == "True"


# 14.交易员查询
def test_queryTrader():
    test_createUser()
    queryTrader = inter.queryTrader(
        pageSize="9999",
        current="1",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("queryTrader:", queryTrader.json())
    print("-" * 100)
    assert str(queryTrader.json()['success']) == "True"
    trader_id = queryTrader.json()['data'][0]['id']
    print("trader_id:", trader_id)
    return trader_id


# 15.修改交易员邮箱
def test_changeEmailTrader():
    changeEmailTrader = inter.changeEmailTrader(
        userId=test_queryTrader(),
        email="Trader" + Random + "@change.com",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("changeEmailTrader:", changeEmailTrader.json())
    print("-" * 100)
    assert str(changeEmailTrader.json()['success']) == "True"


# 16.新建检车员
def test_newChecker():
    newChecker = inter.newChecker(
        username="C" + Random,
        password="qwer`123",
        name="C" + Unicode() + GBK2312() + Random,
        email="C" + Random + "@checker.com",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("newChecker:", newChecker.json())
    print("-" * 100)
    assert str(newChecker.json()['success']) == "True"


# 17.查询检车员
def test_queryChecker():
    queryChecker = inter.queryChecker(
        pageSize="9999",
        current="1",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("queryChecker:", queryChecker.json())
    print("-" * 100)
    assert str(queryChecker.json()['success']) == "True"
    checker_id = queryChecker.json()['data'][0]['id']
    print("checker_id:", checker_id)
    return checker_id


# 18.重置检车员密码
def test_resetPasswordChecker():
    resetPasswordChecker = inter.resetPasswordChecker(
        id=test_queryChecker(),
        password="qwer`123",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("resetPasswordChecker:", resetPasswordChecker.json())
    print("-" * 100)
    assert str(resetPasswordChecker.json()['success']) == "True"


# 19.修改检车员邮箱
def test_changeEmailChecker():
    changeEmailChecker = inter.changeEmailChecker(
        id=test_queryChecker(),
        email="Checker" + Random + "@checker.change",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("changeEmailChecker:", changeEmailChecker.json())
    print("-" * 100)
    assert str(changeEmailChecker.json()['success']) == "True"


# 20.修改检车员姓名
def test_changeNameChecker():
    changeNameChecker = inter.changeNameChecker(
        id=test_queryChecker(),
        username="C" + Random,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("changeNameChecker:", changeNameChecker.json())
    print("-" * 100)
    assert str(changeNameChecker.json()['success']) == "True"


# 21.注销检车员
def test_logoffChecker():
    logoffChecker = inter.logoffChecker(
        id=test_queryChecker(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("logoffChecker:", logoffChecker.json())
    print("-" * 100)
    assert str(logoffChecker.json()['success']) == "True"


# 22.修改交易员姓名
def test_changeNameTrader():
    changeNameTrader = inter.changeNameTrader(
        userId=test_queryTrader(),
        name="Trader" + Random * 2,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("changeNameTrader:", changeNameTrader.json())
    print("-" * 100)
    assert str(changeNameTrader.json()['success']) == "True"


# 23.注销交易员
def test_logoffTrader():
    test_dealerTradernew()
    logoffTrader = inter.logoffTrader(
        userId=test_queryTrader(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("logoffTrader:", logoffTrader.json())
    print("-" * 100)
    assert str(logoffTrader.json()['success']) == "True"


# 24.验证邮箱是否可用
def test_checkEmailUser():
    checkEmailUser = inter.checkEmailUser(
        email=Random + "@check.email",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("checkEmailUser:", checkEmailUser.json())
    print("-" * 100)
    assert str(checkEmailUser.json()['success']) == "True"


# 25.获取二步验证二维码
def get_username():
    getUserList = inter.allUsers(
        pageSize="9999",
        current="1",
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getUserList:", getUserList.json())
    print("-" * 100)
    user_id = str(getUserList.json()['data'][0]['id'])
    username = str(getUserList.json()['data'][0]['username'])
    print("-" * 100)
    print("user_id:", user_id, "username:", username)
    print("-" * 100)
    return username


def test_getQRBarcode():
    getQRBarcode = inter.getQRBarcode(
        username=get_username(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getQRBarcode:", getQRBarcode.json())
    print("-" * 100)
    assert str(getQRBarcode.json()['success']) == "True"
    secret = str(getQRBarcode.json()['data']['secret'])
    print("-" * 100)
    print("secret:", secret)
    print("-" * 100)
    return secret


# 26.绑定二步验证
secretKey = test_getQRBarcode()


def calGoogleCode(secret_key):
    """
    基于时间的算法
    :param secret_key:
    :return:
    """
    # 密钥长度非8倍数，用'='补足
    # lens = len(secret_key)
    # lenx = 8 - (lens % 4 if lens % 4 else 4)
    # secret_key += lenx * '='
    # print(secret_key)
    decode_secret = base64.b32decode(secret_key, True)
    # 解码 Base32 编码过的 bytes-like object 或 ASCII 字符串 s 并返回解码过的 bytes。
    interval_number = int(time.time() // 30)
    message = struct.pack(">Q", interval_number)
    digest = hmac.new(decode_secret, message, hashlib.sha1).digest()
    index = ord(chr(digest[19])) % 16  # 注：网上材料有的没加chr，会报错
    google_code = (struct.unpack(">I", digest[index:index + 4])[0] & 0x7fffffff) % 1000000
    return "%06d" % google_code


# print("-"*100)
# googleCode = calGoogleCode(secretKey)
# print("googleCode:",googleCode)
# print("-"*100)
def test_bindTFA():
    bindTFA = inter.bindTFA(
        id=test_getUserList(),
        secret=secretKey,
        code=calGoogleCode(secretKey),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("bindTFA:", bindTFA.json())
    print("-" * 100)
    assert str(bindTFA.json()['success']) == "True"


# 27.解除二步验证
def test_clearTFA():
    clearTFA = inter.clearTFA(
        id=test_getUserList(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("clearTFA:", clearTFA.json())
    print("-" * 100)
    assert str(clearTFA.json()['success']) == "True"


# 28.检查用户名是否可用
def test_checkUsername():
    checkUsername = inter.checkUsername(
        username="M" + Random,
        headers=GetHeaders()
    )
    print("-" * 100)
    print("checkUsername:", checkUsername.json())
    print("-" * 100)
    assert str(checkUsername.json()['success']) == "True"


# 29.检验用户组内用户是否可以被删除
def test_checkGroupUser():
    checkGroupUser = inter.checkGroupUser(
        id=test_createGroup(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("checkGroupUser:", checkGroupUser.json())
    print("checkGroupUser:", checkGroupUser.status_code)
    print("-" * 100)
    assert str(checkGroupUser.status_code) == "200"


# 30.检查admin用户是否可以被注销
def test_checkUser():
    checkUser = inter.checkUser(
        id=get_userid(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("checkUser:", checkUser.json())
    print("checkUser:", checkUser.status_code)
    print("-" * 100)
    assert str(checkUser.status_code) == "200"


# 31.注销admin用户
def test_deleteUser():
    deleteUser = inter.deleteUser(
        id=test_getUserList(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("deleteUser:", deleteUser.json())
    print("-" * 100)
    assert str(deleteUser.json()['success']) == "True"


# 32.获取用户下级用户组用户信息
def test_getGroupUsers():
    getGroupUsers = inter.getGroupUsers(
        userId=test_getUserList(),
        roles=get_roles(),
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getGroupUsers:", getGroupUsers.json())
    print("-" * 100)
    assert str(getGroupUsers.json()['success']) == "True"
# #33.重置密码
# # def test_resetPassword():
# resetPassword = inter.resetPassword(
#         username = get_username(),
#         newPassword = "qwer`123",
#         setDisable = False,
#         headers = GetHeaders()
#     )
# print("-"*100)
# print("resetPassword:",resetPassword.json())
# print("-"*100)
#     # assert str(resetPassword.json()['success']) == "True"

# headers = GetHeaders()
# print("="*125)
# print(headers)
# print("="*125)
