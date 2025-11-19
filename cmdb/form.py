from django import forms
from django.forms.widgets import *
from .models import Host

class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        exclude = ("id",)
        labels = {
            'host': '名称',
            'ip': 'IP地址',
            'disk': '硬盘',
            'memory': '内存',
            'cpu': 'CPU',
            'desc': '描述',
        }
        error_messages = {
            'ip': {
                'invalid': '请输入合法的 IPv4 或 IPv6 地址',
                'required': 'IP地址为必填项',
            },
            'host': {
                'required': '名称为必填项',
            }
        }
        widgets = {
            'host': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),
            'ip': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),
            'cpu': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'可选项目'}),
            'memory': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'可选项目'}),
            'disk': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'可选项目'}),
            'desc': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'可选项目'}),
        }
