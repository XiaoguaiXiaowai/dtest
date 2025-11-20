from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.db import IntegrityError, DataError, OperationalError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .models import Host
from .form import HostForm

# Create your views here.
@login_required
def index(request):
    host_list = Host.objects.all()
    return render(request, 'main.html', {'hosts': host_list})

def cmdb(request):
    return HttpResponse("You're at the cmdb.")

@login_required
def add(request):
    if request.method == "POST":
        form = HostForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('index')
            except (IntegrityError, DataError, OperationalError) as e:
                # 将数据库异常附加到表单的非字段错误，便于模板展示
                form.add_error(None, f"保存失败：{e}")
    else:
        form = HostForm()
    return render(request, 'add.html', {'form': form})

@login_required
def edit(request, pk):
    host = get_object_or_404(Host, pk=pk)
    if request.method == 'POST':
        form = HostForm(request.POST, instance=host)
        if form.is_valid():
            try:
                form.save()
                return redirect('index')
            except (IntegrityError, DataError, OperationalError) as e:
                form.add_error(None, f"保存失败：{e}")
    else:
        form = HostForm(instance=host)
    return render(request, 'edit.html', {'form': form, 'host': host})

@login_required
def delete(request, pk):
    host = get_object_or_404(Host, pk=pk)
    if request.method == 'POST':
        host.delete()
        return redirect('index')
    # 不允许 GET 直接删除，回到首页
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
