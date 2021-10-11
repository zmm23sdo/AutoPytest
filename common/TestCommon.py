import redis
from common.TestInterface import Interface
from common.TestRedis import Redis
import pytest
import json
import time
import random
import hmac, base64, struct, hashlib, time
import random
import datetime
import oss2
import os

inter = Interface()
redis = Redis()


# 生成随机手机号
def SetPhone():
    random_phone = ''.join(random.sample('0123456789', 10))
    print(random_phone)
    return random_phone


# 随机单个汉字
def Unicode():  # 第一种方法:Unicode码
    val = random.randint(0x4e00, 0x9fbf)
    return chr(val)


def GBK2312():  # 第二种方法:GBK2312
    head = random.randint(0xb0, 0xf7)
    body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
    val = f'{head:x}{body:x}'
    str = bytes.fromhex(val).decode('gb2312')
    return str


def getVerifyCodeImage():  # 获取验证码id
    code = inter.getVerifyCodeImage()
    # print("获取验证码ID:",code)
    return code


def getRedis():  # 获取验证码从Redis
    code = getVerifyCodeImage()
    rdis = Redis()
    value = "verify_code_id_" + code
    verify = eval(rdis.client.get(value))
    # print("获取验证码从Redis:",verify)
    return code, verify


def loginTrue():  # 登录正则提交
    code, verify = getRedis()  # 取出验证码id和验证码
    Response = inter.loginUser("mingvtest1", "qwer`123", code, verify)
    # print("^^^^^^^",Response.json())
    token = Response.json()['data']['token']
    # print("token:",Response.json()['data']['token'])
    return token


def GetHeaders():
    token = redis.activateToken(loginTrue())
    headers = {'Authorization': 'Bearer ' + token}
    print("=" * 100)
    print(headers)
    print("=" * 100)
    return headers


def loginApp():
    checkerLogin = inter.checkerLogin(
        username="Mvchecker4251",
        password="qwer`123"
    )
    print("=" * 100)
    token = checkerLogin.json()['data']['token']
    print("checkerLogin:", checkerLogin.json())
    print("=" * 100)
    return token


def GetHeaders2():
    token = redis.activateToken(loginApp())
    headers = {'Authorization': 'Bearer ' + token}
    print("=" * 100)
    print(headers)
    print("=" * 100)
    return headers


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


def TimeNow():
    time_now = int(time.time())
    Random = str(time_now)
    return Random


def Today():
    # 获取当前时间
    now = datetime.datetime.now()
    # 获取今天零点
    zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute,
                                         seconds=now.second,
                                         microseconds=now.microsecond)
    # 获取23:59:59
    lastToday = zeroToday + datetime.timedelta(hours=23, minutes=59, seconds=59)
    # 获取前一天的当前时间
    yesterdayNow = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
    # 获取明天的当前时间
    tomorrowNow = now + datetime.timedelta(hours=23, minutes=59, seconds=59)

    print('时间差', datetime.timedelta(hours=23, minutes=59, seconds=59))
    print('当前时间', now)
    print('今天零点', zeroToday)
    print('获取23:59:59', lastToday)
    print('昨天当前时间', yesterdayNow)
    print('明天当前时间', tomorrowNow)
    return zeroToday, lastToday


def Now():
    now = datetime.datetime.now().isoformat() + "Z"
    print(now)
    return now


def NowDate():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    now_time = str(now_time)
    print(now_time)
    return now_time


def UpLoad(car_no):
    #   获取STS:
    getSTS = inter.getSTS(
        headers=GetHeaders()
    )
    print("-" * 100)
    print("getSTS:", getSTS.json())
    print("-" * 100)
    accessKeyId = str(getSTS.json()['data']['accessKeyId'])
    accessKeySecret = str(getSTS.json()['data']['accessKeySecret'])
    security_token = str(getSTS.json()['data']['securityToken'])
    region = str(getSTS.json()['data']['region'])
    bucket_name = str(getSTS.json()['data']['bucket'])
    endpoint = str(getSTS.json()['data']['endpoint'])
    expiredTime = str(getSTS.json()['data']['expiredTime'])
    publicBucket = str(getSTS.json()['data']['publicBucket'])
    print("-" * 100)
    print("accessKeyId:", accessKeyId)
    print("accessKeySecret:", accessKeySecret)
    print("security_token:", security_token)
    print("region:", region)
    print("bucket_name:", bucket_name)
    print("endpoint:", endpoint)
    print("expiredTime:", expiredTime)
    print("publicBucket:", publicBucket)
    print("-" * 100)

    # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。

    auth = oss2.StsAuth(accessKeyId, accessKeySecret, security_token)

    print("-" * 100)
    print("auth", auth)
    print("-" * 100)
    # 填写Bucket名称。
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    print("-" * 100)
    print("bucket", bucket)
    print("-" * 100)
    # 必须以二进制的方式打开文件。
    # 填写本地文件的完整路径。如果未指定本地路径，则默认从示例程序所属项目对应本地路径中上传文件。
    with open('/Users/admin/Desktop/WechatIMG11643.jpg', 'rb') as fileobj:
        # Seek方法用于指定从第1000个字节位置开始读写。上传时会从您指定的第1000个字节位置开始上传，直到文件结束。
        fileobj.seek(1000, os.SEEK_SET)
        # Tell方法用于返回当前位置。
        current = fileobj.tell()
        # 填写Object完整路径。Object完整路径中不能包含Bucket名称。
        result = bucket.put_object('car/' + car_no + '/vehicle/car/front_right/hash', fileobj)

        # result = bucket.put_object_from_file("WechatIMG11643.jpeg", "/Users/hfy/Desktop/WechatIMG11643.jpeg")
    # HTTP返回码。
    print('http status: {0}'.format(result.status))
    # 请求ID。请求ID是本次请求的唯一标识，强烈建议在程序日志中添加此参数。
    print('request_id: {0}'.format(result.request_id))
    # ETag是put_object方法返回值特有的属性，用于标识一个Object的内容。
    print('ETag: {0}'.format(result.etag))
    # HTTP响应头部。
    print('date: {0}'.format(result.headers['date']))
    return1 = 'http status: {0}'.format(result.status)
    return2 = 'request_id: {0}'.format(result.request_id)
    return3 = 'ETag: {0}'.format(result.etag)
    return return1, return2, return3


def NDay(day, hour):
    ndays = datetime.datetime.now() + datetime.timedelta(days=day, hours=hour)
    ndays = str(ndays.isoformat() + "Z")
    print("-" * 100)
    print("ndays", ndays)
    print("-" * 100)
    return ndays

