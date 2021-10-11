import redis
import json


class Redis:
    def __init__(self):  # 初始化Redis
        self.client = redis.Redis(host='192.168.102.252', port=6379, decode_responses=True, password="qwer1234", db=0)

    def activateToken(self, token):  # 在Redis中激活token
        R = redis.Redis(host='192.168.102.252', port=6379, decode_responses=True, password="qwer1234", db=0)
        redis_token = R.get(token)
        verified = json.loads(redis_token);
        verified['verified'] = True
        R.set(token, json.dumps(verified))
        # print(R.get(token))
        # print("Token:",token)
        return token

    def redisCode(key):
        R = redis.Redis(host='192.168.102.252', port=6379, decode_responses=True, password="qwer1234", db=0)
        code_redis = str(R.get(key))
        new_code = code_redis.replace('"', '')
        print("key:", key)
        print("code_redis:", new_code)
        return new_code

    def verifyCode(code_id):
        R = redis.Redis(host='192.168.102.252', port=6379, decode_responses=True, password="qwer1234", db=0)
        code_redis = str(R.get(code_id))
        code = code_redis.replace('"', '')
        print("code_redis:", code_redis)
        print("code:", code)
        return code
