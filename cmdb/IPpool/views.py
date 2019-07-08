# Create your views here.
from __future__ import absolute_import, unicode_literals
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.mixin import CommonMixin, JsonFormMixin, FieldClassMixin
from django.core.urlresolvers import reverse_lazy
from .models import IPpool,IPDetail
from .forms import PoolCreateForm, DetailCreateForm


class PoolList(LoginRequiredMixin, CommonMixin, ListView):
    module = IPpool
    template_name = 'ippool/pool_list.html'
    paginate_by = '30'
    context_object_name = 'pools'
    page_title = 'ip资源池列表'

    def get_queryset(self):
        name = self.request.GET.get('name')
        subnet = self.request.GET.get('subnet')
        pools = IPpool.objects
        if name:
            pools = pools.filter(name__contains=name)
        if subnet:
            pools = pools.filter(subnet__exact=subnet)
        return pools.all()


class PoolCreate(LoginRequiredMixin, CommonMixin, JsonFormMixin, CreateView):
    template_name = 'ippool/pool_create.html'
    page_title = 'ip资源池创建'
    form_class = PoolCreateForm
    success_url = reverse_lazy('pool:pool_list')


class PoolDetailView(LoginRequiredMixin, CommonMixin, DetailView):
    model = IPDetail
    template_name = 'ippool/pool_detail.html'
    page_title=''
    slug_field = 'pk'
    slug_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(PoolDetailView, self).get_context_data(**kwargs)
        context['unused'] = IPDetail.objects.filter(status=True, ippool_id=self.object.pk)
        context['used'] = IPDetail.objects.filter(status=False, ippool_id=self.object.pk)
        return context

class DetailCreate(LoginRequiredMixin, CommonMixin, JsonFormMixin, CreateView):
    template_name = 'ippool/detail_create.html'
    page_title = '资源池自定义规则'
    form_class = DetailCreateForm
    success_url = reverse_lazy('pool:pool_list')