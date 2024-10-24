from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404
from django.views import View

from utilities.permissions import get_permission_for_model
from utilities.views import register_model_view, ViewTab
from netbox.constants import DEFAULT_ACTION_PERMISSIONS
from netbox.views import generic
from dcim.models import Site

from .models import *
from .forms import *
from .table import *


__all__ = (
    'SopInfraTabView',
    'SopInfraListView',
    'SopInfraDeleteView',
    'SopInfraEditView',
    'SopInfraAddView',
    'SopInfraDetailView',
    'SopInfraMerakiAddView',
    'SopInfraMerakiEditView',
    'SopInfraSizingAddView',
    'SopInfraSizingEditView',
    'SopInfraClassificationAddView',
    'SopInfraClassificationEditView',
)


@register_model_view(Site, name='infra')
class SopInfraTabView(View):
    '''
    creates an "infrastructure" tab on the site page
    '''
    tab = ViewTab(label=_('Infrastructure'), permission=get_permission_for_model(SopInfra, 'view'))
    template_name: str = 'sop_infra/tab/tab.html'

    def get_extra_context(self, request, pk) -> dict:
        context: dict = {}
        
        site = get_object_or_404(Site, pk=pk)
        if SopInfra.objects.filter(site=site).exists():
            context['sop_infra'] = SopInfra.objects.get(site=site)
        else:
            context['sop_infra'] = SopInfra
        context['actions'] = DEFAULT_ACTION_PERMISSIONS
        return {'object': site, 'context': context}

    def get(self, request, pk):
        if not request.user.has_perm(get_permission_for_model(SopInfra, 'view')):
            return self.handle_no_permission()
        return render(request, self.template_name, self.get_extra_context(request, pk))


class SopInfraDeleteView(generic.ObjectDeleteView):
    '''
    deletes an existing SopInfra instance
    '''
    queryset = SopInfra.objects.all()


class SopInfraEditView(generic.ObjectEditView):
    '''
    edits an existing SopInfra instance
    '''
    queryset = SopInfra.objects.all()
    form = SopInfraForm

    def get_return_url(self, request, obj):
        if obj.site:
            return f'/dcim/sites/{obj.site.id}/infra'


class SopInfraAddView(generic.ObjectEditView):
    '''
    adds a new SopInfra instance
    if the request is from the site page,
    -> the site id is passed as an argument (pk)
    '''
    queryset = SopInfra.objects.all()
    form = SopInfraForm

    def get_object(self, **kwargs):
        '''        
        '''
        if 'pk' in kwargs:
            site= get_object_or_404(Site, pk=kwargs['pk'])
            obj = self.queryset.model
            return obj(site=site)
        return super().get_object(**kwargs)

    def alter_object(self, obj, request, args, kwargs):
        '''
        '''
        if 'pk' in kwargs:
            site = get_object_or_404(Site, pk=kwargs['pk'])
            obj = self.queryset.model
            return obj(site=site)
        return super().alter_object(obj, request, args, kwargs)

    def get_return_url(self, request, obj):
        try:
            return f'/dcim/sites/{obj.site.id}/infra'
        except:
            return f'/plugins/sop_infra/list'


class SopInfraClassificationAddView(generic.ObjectEditView):
    '''
    only adds classification objects in a SopInfra instance
    '''
    template_name:str = 'sop_infra/tools/forms.html'
    queryset = SopInfra.objects.all()
    form = SopInfraClassificationForm

    def get_object(self, **kwargs):
        '''        
        '''
        if 'pk' in kwargs:
            site= get_object_or_404(Site, pk=kwargs['pk'])
            obj = self.queryset.model
            return obj(site=site)
        return super().get_object(**kwargs)

    def alter_object(self, obj, request, args, kwargs):
        '''
        '''
        if 'pk' in kwargs:
            site = get_object_or_404(Site, pk=kwargs['pk'])
            obj = self.queryset.model
            return obj(site=site)
        return super().alter_object(obj, request, args, kwargs)

    def get_return_url(self, request, obj):
        if obj.site:
            return f'/dcim/sites/{obj.site.id}/infra'

    def get_extra_context(self, request, obj) -> dict:
        context = super().get_extra_context(request, obj)
        context['object_type'] = 'Classification'
        if obj and obj.site:
            context['site'] = obj.site
        return context


class SopInfraClassificationEditView(generic.ObjectEditView):
    '''
    only edits classification objects in a sopinfra instance
    '''
    template_name:str = 'sop_infra/tools/forms.html'
    queryset = SopInfra.objects.all()
    form = SopInfraClassificationForm

    def get_return_url(self, request, obj):
        if obj.site:
            return f'/dcim/sites/{obj.site.id}/infra'

    def get_extra_context(self, request, obj) -> dict:
        context = super().get_extra_context(request, obj)
        context['object_type'] = 'Classification'
        if obj and obj.site:
            context['site'] = obj.site
        return context


class SopInfraMerakiAddView(generic.ObjectEditView):
    '''
    only adds meraki sdwan objects in a sopinfra instance
    '''
    template_name:str = 'sop_infra/tools/forms.html'
    queryset = SopInfra.objects.all()
    form = SopInfraMerakiForm

    def get_object(self, **kwargs):
        '''
        '''
        if 'pk' in kwargs:
            site = get_object_or_404(Site, pk=kwargs['pk'])
            obj = self.queryset.model
            return obj(site=site)
        return super().get_object(**kwargs)

    def get_return_url(self, request, obj):
        if obj.site:
            return f'/dcim/sites/{obj.site.id}/infra'

    def get_extra_context(self, request, obj) -> dict:
        context = super().get_extra_context(request, obj)
        context['object_type'] = 'Meraki SDWAN'
        if obj and obj.site:
            context['site'] = obj.site
        return context


class SopInfraMerakiEditView(generic.ObjectEditView):
    '''
    only edits meraki sdwan objects in a sopinfra instance
    '''
    template_name:str = 'sop_infra/tools/forms.html'
    queryset = SopInfra.objects.all()
    form = SopInfraMerakiForm
    
    def get_return_url(self, request, obj):
        if obj.site:
            return f'/dcim/sites/{obj.site.id}/infra'

    def get_extra_context(self, request, obj) -> dict:
        context = super().get_extra_context(request, obj)
        context['object_type'] = 'Meraki SDWAN'
        if obj and obj.site:
            context['site'] = obj.site
        return context


class SopInfraSizingAddView(generic.ObjectEditView):
    '''
    only adds sizing objects in a sopinfra instance
    '''
    template_name:str = 'sop_infra/tools/forms.html'
    queryset = SopInfra.objects.all()
    form = SopInfraSizingForm

    def get_object(self, **kwargs):
        '''
        '''
        if 'pk' in kwargs:
            site = get_object_or_404(Site, pk=kwargs['pk'])
            obj = self.queryset.model
            return obj(site=site)
        return super().get_object(**kwargs)

    def get_return_url(self, request, obj):
        if obj.site:
            return f'/dcim/sites/{obj.site.id}/infra'

    def get_extra_context(self, request, obj) -> dict:
        context = super().get_extra_context(request, obj)
        context['object_type'] = 'Sizing'
        if obj and obj.site:
            context['site'] = obj.site
        return context


class SopInfraSizingEditView(generic.ObjectEditView):
    '''
    only edits sizing objects in a sopinfra instance
    '''
    template_name:str = 'sop_infra/tools/forms.html'
    queryset = SopInfra.objects.all()
    form = SopInfraSizingForm

    def get_return_url(self, request, obj):
        if obj.site:
            return f'/dcim/sites/{obj.site.id}/infra'

    def get_extra_context(self, request, obj) -> dict:
        context = super().get_extra_context(request, obj)
        context['object_type'] = 'Sizing'
        if obj and obj.site:
            context['site'] = obj.site
        return context


class SopInfraDetailView(generic.ObjectView):
    '''
    detail view with changelog and journal
    '''
    queryset = SopInfra.objects.all()


class SopInfraListView(generic.ObjectListView):
    '''
    list view of all sopinfra instances
    '''
    queryset = SopInfra.objects.all()
    table = SopInfraTable

