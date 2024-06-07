from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from easy_pdf.views import PDFTemplateResponseMixin

from utils.decorators import LoginRequiredMixin,  StaffRequiredMixin, SecretariaRequiredMixin
from .forms import BuscaAtaForm
from .models import Ata


class AtaListView(LoginRequiredMixin, ListView):
    model = Ata
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
			#quando ja tem dado filtrando
            context['form'] = BuscaAtaForm(data=self.request.GET)
        else:
			#quando acessa sem dado filtrando
            context['form'] = BuscaAtaForm()
        return context

    def get_queryset(self):
        qs = Ata.objects.all()
        
        if self.request.GET:
            #quando ja tem dado filtrando
            form = BuscaAtaForm(data=self.request.GET)
        else:
            #quando acessa sem dado filtrando
            form = BuscaAtaForm()

        if form.is_valid():
            data = form.cleaned_data.get('data')
            curso = form.cleaned_data.get('curso')
            conteudo = form.cleaned_data.get('conteudo')
            
            if data:
                qs = qs.filter(data__icontains=data)
                
            if curso:
                qs = qs.filter(curso=curso)
                
            if conteudo:
                qs = qs.filter(Q(pauta__icontains=conteudo) | Q(texto__icontains=conteudo))
                
        if self.request.user.tipo != "ADMINISTRADOR":
            qs = qs.filter(curso__in=self.request.user.curso.all())
        
        return qs


class AtaCreateView(LoginRequiredMixin,  SecretariaRequiredMixin, CreateView):
    model = Ata
    fields = ['curso','codigo', 'data', 'hora', 'local', 'pauta', 'redator', 'texto', 'integrantes', 'arquivo_anexo1']
    success_url = 'ata_list'
    
    def form_valid(self, form):
        limite_mb = 100 * 1024 * 1024
        ata = form.instance
        
        if (not ata.arquivo_anexo1 or (ata.arquivo_anexo1 and ata.arquivo_anexo1.file.size <= limite_mb)):
            form.save()
            return super(AtaCreateView, self).form_valid(form)
        else:
            messages.warning(self.request, 'Sistema somente suporta 100 Mb no anexo!')
            return super(AtaCreateView, self).form_invalid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Ata cadastrada com sucesso na plataforma!')
        return reverse(self.success_url)
        

class AtaUpdateView(LoginRequiredMixin,  SecretariaRequiredMixin, UpdateView):
    model = Ata
    fields = ['curso','codigo', 'data', 'hora', 'local', 'pauta', 'redator', 'texto', 'integrantes', 'arquivo_anexo1']
    success_url = 'ata_list'
    
    def form_valid(self, form):
        limite_mb = 100 * 1024 * 1024
        ata = form.instance
        
        if (not ata.arquivo_anexo1 or (ata.arquivo_anexo1 and ata.arquivo_anexo1.file.size <= limite_mb)):
            form.save()
            return super(AtaUpdateView, self).form_valid(form)
        else:
            messages.warning(self.request, 'Sistema somente suporta 100 Mb no anexo!')
            return super(AtaUpdateView, self).form_invalid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Dados da ata atualizados com sucesso na plataforma!')
        return reverse(self.success_url)


class AtaDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Ata
    success_url = 'ata_list'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à essa ata, permissão negada!')
        return redirect(self.success_url)
    
    
class AtaDetailView(LoginRequiredMixin, DetailView):
    model = Ata
    template_name = 'atas/ata_detail.html'


class AtaRelatorioView(LoginRequiredMixin, PDFTemplateResponseMixin, DetailView):
    model = Ata
    template_name = 'atas/relatorios/ata.html'