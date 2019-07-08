import datetime
import json
import os
import codecs
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse
from servers.models import Host, Team, Bios, Cpu, Mem, Network, Disk, Cabinet
from network.models import Network as NetDevice
from IPpool.models import IPpool
import servers.models as servers_models
from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import render
from django.http import StreamingHttpResponse
from .tool import deal_queryobject
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import DocumentForm
from .models import Document
from .tool import read_file
import IPy


def asset_export_machine(request):
    model = 'host'
    hosts = Host.objects
    download = request.GET.get('download', '')
    exclude = request.GET.get('exclude', '').split(',') or []
    hostname = request.GET.get('hostname', '')
    ip = request.GET.get('ip', '')
    team = request.GET.get('team', '')
    cabinet = request.GET.get('cabinet', '')
    responsible = request.GET.get('responsible')

    if hostname:
        hosts = hosts.filter(hostname__contains=hostname)
    if ip:
        hosts = hosts.filter(ip__contains=ip)
    if team:
        hosts = hosts.filter(team__name__icontains=team)
    if cabinet:
        hosts = hosts.filter(cabinet__name__icontains=cabinet)
    if responsible:
        hosts = hosts.filter(responsible__icontains=responsible)
    hosts = hosts.all()
    total_num=hosts.count()
    hosts=hosts[:20]

    form = DocumentForm()  # A empty, unbound form

    page_title = "资产批量导出导入"
    
    if download:
        timestamp = (datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d_%H:%M:%S")
        data = deal_queryobject(hosts, '{}_info_{}'.format(model, timestamp), exclude=exclude)
        response = StreamingHttpResponse(data)
        response['Content-Disposition'] = 'attachment;filename="{}_info_{}.csv"'.format(model, timestamp)
        return response
    
    return render(request, "report/report_machine.html", context={"page_title": page_title, 'hosts':hosts,
                                                                     "form": form,
                                                                     "num": total_num})
    
    
    
def asset_export_mem(request):
    hosts = Mem.objects.all()[:20]
    page_title = "资产批量导出"
    
    return HttpResponse('')

def asset_export_cpu(request):
    hosts = Cpu.objects.all()[:20]
    page_title = "资产批量导出"
    return HttpResponse('')
    
def asset_export_disk(request):
    hosts = Disk.objects.all()[:20]
    page_title = "资产批量导出"
    
    return HttpResponse('')

def asset_export_network(request):
    hosts = Network.objects.all()[:20]
    page_title = "资产批量导出导入"
    
    return HttpResponse('')
    
    
    
def asset_import(request):
    return render(request, "report/asset_import.html")






def export_csv(request, model):
    '''
    全量导出csv
    '''
    # 管理员有权限
    if not request.user.is_superuser:
        return HttpResponseForbidden(json.dumps({"msg":"禁止操作"}))
    
    # 定义除外的field, 默认的，model作为其它model(A)外键的情况下，a字段被排除
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    exclude = []
    Model = getattr(servers_models, model.capitalize())
    queryset = Model.objects.all()
    data = deal_queryobject(queryset, '{}_info_{}'.format(model, timestamp), exclude=exclude)
    response = StreamingHttpResponse(data)
    response['Content-Disposition'] = 'attachment;filename="{}_info_{}.csv"'.format(model, timestamp)
    return response


class FileView(LoginRequiredMixin, View):
    
    # def get(self, request):
    #     form = DocumentForm()  # A empty, unbound form
    #
    #     # Load documents for the list page
    #     documents = Document.objects.all()
    #
    #     # Render list page with the documents and the form
    #     return render(request, "report/upload.html", {"form": form, "documents":documents})
    
    
    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)
        response = {"msg":"", "code":"1", "data":[]}
        if form.is_valid():
            # print('valid')
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            try:
                # 更新数据到数据库
                from django.conf import settings
                path = os.path.join(getattr(settings, 'MEDIA_ROOT'), newdoc.docfile.name)
                with codecs.open(path, 'rb', 'gb2312') as csvfile:
                    objs_dict_list = []
                    keys = []

                    for index, line in enumerate(csvfile):
                        tmp_dict = {}
                        if index == 0:
                            keys = line.strip().split(',')
                        else:
                            for i, v in enumerate(line.strip().split(',')):
                                # 考虑多对-情况,team,cabinet..把name转化为ID,还要判断是否存在对应的team,和cabinet对象
                                error_msg = ''
                                if keys[i] == "team":
                                    v = Team.objects.filter(name__exact=v)
                                    # 判断是否存在team和cabiet,不存在直接抛出异常
                                    if not v:
                                        error_msg = "第{}行,的项目组{}在后台不存在,请检查".format(index, v)
                                        raise Exception(error_msg)
                                    else:
                                        v = v[0]

                                elif keys[i] == "cabinet":
                                    v = Cabinet.objects.filter(name__exact=v)
                                    # 判断是否存在team和cabiet,不存在直接抛出异常
                                    if not v:
                                        error_msg = "第{}行,的机柜{}在后台不存在,请检查".format(index, v)
                                        raise Exception(error_msg)
                                    else:
                                        v = v[0]
                                        
                                # 对有choices关键字的field进行值的转换
                                elif Host._meta.get_field(keys[i]).choices:
                                    print(keys[i])
                                    match = False
                                    for choice in Host._meta.get_field(keys[i]).choices:
                                        if choice[1] == v.strip():
                                            v = choice[0]
                                            match = True
                                    if not match:
                                        error_msg = "第{}行的{}值在后台没有匹配,检查".format(index, keys[i])
                                        raise Exception(error_msg)
                                # 生成和machine对象对应的字典
                                tmp_dict.update({keys[i]: v})
                            # 有效数据加入对象列表
                            objs_dict_list.append(tmp_dict)
                            
                    # print(objs_dict_list)
                    
                    # 判断是否是空表或只有一行
                    if len(objs_dict_list) <= 0:
                        raise Exception("请使用正确模板,并正确录入记录")


                    # 写入数据库
                    new_create_count = 0
                    create_machine_ip_list = []
                    for h_dict in objs_dict_list:
                        # 判断有没有该IP对应的网段池子,没有抛出异常
                        ip = h_dict['ip']
                        try:
                            # 生成IP对象,验证ip是否合法
                            ip_obj = IPy.IP(ip)
                            # 拿到该ip对应的ippool
                            subnet = str(ip_obj.make_net(24))[:-3]
                            ippool = IPpool.objects.filter(subnet=subnet)
                            if not ippool:
                                raise Exception("请先添加IP池:{}".format(subnet))
                        except:
                            raise Exception("IP:{} 格式错误".format(ip))
    
                        # 判断是否已经存在
                        if not Host.objects.filter(ip__exact=h_dict['ip']):
                            # 判定网络设备是否在这个floor上面
                            # 拿到机柜对象
                            cabinet = h_dict['cabinet']
                            # 判断 当前机柜的floor 有没有被网络设备占用
                            if NetDevice.objects.filter(floor=h_dict['floor'], cabinet=cabinet):
                                # 已经被占用
                                raise Exception("{}机柜的{}槽位已经被占用".format(cabinet.name, h_dict['floor']))
                            
                            create_result = Host.objects.get_or_create(**h_dict)
                            if create_result[1] == True:
                                #成功插入
                                new_create_count += 1
                                create_machine_ip_list.append(h_dict['ip'])
                        else:
                            print("已经存在,", h_dict)
                            
                    response["msg"] = "本次成功导入 {}条记录".format(new_create_count)
                    response["code"] = "0"
                    response["data"] = create_machine_ip_list
                    
            except Exception as e:
                # 导入失败
                print('读取文件失败',e)
                response["msg"] = "本次导入失败,{}".format(str(e))
                response["code"] = "1"
                
        else:
            # 文件验证失败
            print("数据验证失败,选择正确文件")
            response["msg"] = "上传校验失败"
            response["code"] = "1"
        return HttpResponse(json.dumps(response), content_type="application/json")
    

def down_demo(request, demo):
    # TODO:是否需要动态生成
    path = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(path, 'utils/csv_template/{}_demo.csv'.format(demo))
    data = read_file(file_path)
    response = StreamingHttpResponse(data)
    response['Content-Disposition'] = 'attachment;filename="{}_demo.csv"'.format(demo)
    return response