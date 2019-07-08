from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
# Create your views here.

def index(request, sship):
    
    return render(request, "ssh/terminal.html", context={"sship": sship})

def generate_gate_one_auth_obj(request):
    import time, hmac, hashlib, json
    user = request.user.username
    gateone_server = getattr(settings, "GATEONE_SERVER")  # 替换成对应的部署gateone的server的ip地址
    secret = bytes("{}".format(getattr(settings, "GATEONE_SECRET")), encoding="utf-8")  # 替换成对应的api secret ，该信息
    # 存放在gateone的配置文件30api.conf中
    api_key = "{}".format(settings, "GATEONE_API_KEY")  # 替换成对应的api key ，该信息 存放在gateone的配置文件30api.conf中

    authobj = {
        'api_key': api_key,
        'upn': user,
        'timestamp': str(int(time.time() * 1000)),
        'signature_method': 'HMAC-SHA1',
        'api_version': '1.0'
    }

    my_hash = hmac.new(secret, digestmod=hashlib.sha1)
    my_hash.update((authobj['api_key'] + authobj['upn'] + authobj['timestamp']).encode("utf-8"))
    authobj['signature'] = my_hash.hexdigest()
    auth_info_and_server = {"url": gateone_server, "auth": authobj}
    valid_json_auth_info = json.dumps(auth_info_and_server)
    return HttpResponse(valid_json_auth_info, content_type="application/json")