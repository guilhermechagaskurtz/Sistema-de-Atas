from __future__ import unicode_literals

import os

from django.conf import settings
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from utils.gerador_hash import gerar_hash
    
class Ata(models.Model):
    codigo = models.CharField(_('Código *'), unique=True, max_length=20, help_text='Fique atento ao último código de memória informado')
    data = models.DateField(_('Data *'), max_length=11, help_text='Use: dd/mm/aaaa')
    hora = models.CharField(_('Hora *'), max_length=5, help_text='Use: hh:mm')
    local = models.CharField(_('Local *'), max_length=50)
    pauta = models.TextField(_('Pauta'), max_length=200)
    redator = models.ForeignKey('usuario.Usuario', null=True, blank=True, verbose_name= 'Redator *', on_delete=models.PROTECT,related_name='redator')
    texto = models.TextField(_('Texto'), null=True, blank=True, max_length=50000)
    validada = models.BooleanField(_('Ata validada? '), default=False, null=True, blank=True)
    integrantes = models.ManyToManyField('usuario.Usuario', verbose_name='Integrantes', null=True, blank=True, related_name='integrantes',help_text='Para selecionar mais de um integrante, use a tecla CTRL ou CMD')
    curso = models.ForeignKey('curso.Curso', verbose_name= 'Curso *', on_delete=models.PROTECT, related_name='curso')
    arquivo_anexo1 = models.FileField(_('Anexo à reunião'), null=True, blank=True, upload_to='midias', help_text='Se houver mais de um arquivo, sugere-se enviar o compactado')
    
    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)
    
    objects = models.Manager()
    
    class Meta:
        ordering            =   ['-codigo','-data','-hora']
        verbose_name        =   ('ata')
        verbose_name_plural =   ('atas')
        unique_together     =   ['codigo', 'data', 'hora'] #criando chave primária composta no BD

    def __str__(self):
        return "Memória: %s. Data: %s." % (self.codigo, self.data)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        self.codigo = self.codigo.upper()
        super(Ata, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('ata_update', args=[str(self.id)])

    @property
    def get_delete_url(self):
        return reverse('ata_delete', args=[str(self.id)])
    
    @property
    def get_visualiza_url(self):
        return reverse('ata_detail', args=[str(self.id)])

    @property
    def get_relatorio_url(self):
        return reverse('ata_report', args=[str(self.id)])
    
    @property
    def get_linhas_texto(self):
        texto_tmp = self.texto
        tamanho_linha=94 
        return [texto_tmp[y-tamanho_linha:y] for y in range(tamanho_linha, len(texto_tmp)+tamanho_linha,tamanho_linha)]
        
        
    

#triggers para limpeza dos arquivos apagados ou alterados. No Django é chamado de signals
#deleta o arquivo fisico ao excluir o item da pasta midias
@receiver(models.signals.post_delete, sender=Ata)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.arquivo_anexo1:
        if os.path.isfile(instance.arquivo_anexo1.path):
            os.remove(instance.arquivo_anexo1.path)

#deleta o arquivo fisico ao alterar o arquivo da pasta midia
@receiver(models.signals.pre_save, sender=Ata)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        obj = Ata.objects.get(pk=instance.pk)

        if not obj.arquivo_anexo1:
            return False

        old_file = obj.arquivo_anexo1
    except Ata.DoesNotExist:
        return False

    new_file = instance.arquivo_anexo1
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
