from django.http import HttpResponse, HttpResponseForbidden
from servers.models import Host, Team, Bios, Cpu, Mem, Network,Change
from django.views.decorators.csrf import csrf_exempt
from auto.models import Auto
from IPpool.models import IPDetail


@csrf_exempt
def autoreport(request, uuid):
    import json
    if request.method == "POST":
        data = json.loads(request.body)
        data = data[uuid]
        if len(uuid) != 32:
            h = Host.objects.filter(ip=uuid)
            if not h:
                u = uuid.split('.')
                try:
                    subnet = [a for a in Auto.objects.filter(ippool__subnet='{}.0'.format('.'.join(u[0:3]))) if int(u[-1]) in range(int(a.start_ip), int(a.end_ip))][0]
                    if subnet:
                        Host.objects.get_or_create(status=subnet.status, asset_type=subnet.asset_type, team=subnet.team,
                                                   floor=None, ip=uuid, **(data['system']))
                        Change.objects.create(ip=uuid, note='新增', event=4)
                        ippool = IPDetail.objects.get(ip=uuid)
                        ippool.status = False
                        ippool.save()
                        h = Host.objects.filter(ip=uuid)
                except Exception as e:
                    # print(e)
                    return HttpResponse(json.dumps({"msg": "no ip_pool {}.0".format('.'.join(u[0:3])),
                                                        "code": "1"}),content_type="application/json")
        else:
            # uuid==UUID,更新信息
            h = Host.objects.filter(uuid=uuid)
            if not h:
                return HttpResponse(json.dumps({"msg": "no host named uuid {}".format(uuid), "code": "1"}),
                                    content_type="application/json")
            
            h = Host.objects.filter(uuid=uuid)
            # 更新system相关信息
            h.update(**(data['system']))
        # 此处可以考虑使用Model._meta.get_field(name).one_to_many排除一对多情况
        
        h = h[0]

        # 修复,ip改变情况
        update_ip = True
        for net in data['network']['child']:
            if h.ip == net['ipv4']:
                update_ip = False
                break
        if update_ip:
            h.ip = data['network']['child'][0]['ipv4']
            h.save()
            h = Host.objects.get(uuid=uuid)
            
        ippool = IPDetail.objects.get(ip=h.ip)
        if ippool.status:
            ippool.status = False
            ippool.save()

        # 更新cpu
        Cpu.objects.get_or_create(**(data['cpu']), host=h)
        
        # 更新mem
        ori_mem_sn_set = set([mobj.sn for mobj in Mem.objects.filter(host=h)])
        cur_mem_list = data['mem']['child']
        cur_mem_sn_set = set([m['sn'] for m in cur_mem_list])
        removed_sn_list = list(ori_mem_sn_set - cur_mem_sn_set)
        added_sn_list = list(cur_mem_sn_set - ori_mem_sn_set)
        # 第一次上报时，添加数据
        if len(ori_mem_sn_set) == 0:
            _ = [Mem.objects.get_or_create(**m, host=h) for m in cur_mem_list]

        elif len(added_sn_list) == 0 and len(removed_sn_list) == 0:
            # mem数据未发生变化
            pass
        elif len(added_sn_list) > 0 or len(removed_sn_list) > 0:
            # 新增内存入库
            for m in cur_mem_list:
                if m['sn'] in added_sn_list:
                    Mem.objects.get_or_create(**m, host=h)
                    Change.objects.create(ip=uuid, note='新增内存，sn地址为{}'.format(m['sn']), event=1)
            # 对减少的内存进行记录,标记
            if removed_sn_list:
                for rm in removed_sn_list:
                    Change.objects.create(ip=uuid, note='减少内存，sn地址为{}'.format(rm), event=1)
                    Mem.objects.filter(sn=rm).delete()
        
        # 更新network
        ori_net_sn_set = set([mobj.mac for mobj in Network.objects.filter(host=h)])
        cur_net_list = data['network']['child']
        cur_net_sn_set = set([m['mac'] for m in cur_net_list])
        removed_net_sn_list = list(ori_net_sn_set - cur_net_sn_set)
        added_net_sn_list = list(cur_net_sn_set - ori_net_sn_set)
        # 第一次上报时，添加数据
        if len(ori_net_sn_set) == 0:
            _ = [Network.objects.get_or_create(**m, host=h) for m in cur_net_list]

        elif len(removed_net_sn_list) == 0 and len(added_net_sn_list) == 0:
            # mem数据未发生变化
            pass
        elif len(removed_net_sn_list) > 0 or len(added_net_sn_list) > 0:
            # 新增内存入库
            for m in cur_net_list:
                if m['mac'] in added_net_sn_list:
                    Network.objects.get_or_create(**m, host=h)
                    Change.objects.create(ip=uuid, note='新增网卡，mac为{}'.format(m['mac']), event=1)
            # 对减少的内存进行记录,标记
            if removed_net_sn_list:
                for rm in removed_net_sn_list:
                    Change.objects.create(ip=uuid, note='减少网卡，mac为{}'.format(rm), event=1)
                    Network.objects.filter(mac=rm).delete()

        # 更新bios
        Bios.objects.get_or_create(**(data['bios']), host=h)
        return HttpResponse(json.dumps({"msg": "ok", "uuid": h.uuid.hex, "code": "0"}), content_type="application/json")
