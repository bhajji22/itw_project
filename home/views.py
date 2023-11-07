from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.conf import settings
from .forms import Fileform
from datetime import date
from .models import filedata
from django.contrib.auth.decorators import login_required
import mimetypes
import os
from django.db.models.functions import Lower

# Create your views here.
all_files = filedata.objects.all()
all_users = User.objects.all()

def index(request):
    #print("Hello there")
    if request.user.is_authenticated:
        return redirect('/data_manager/')
    return render(request,'home/index.html')

def about(request):
    return render(request,"home/about.html")

def register(request):
    #print("Hello there")
    if request.user.is_authenticated:
        messages.error(request,"please logout before registering")
        return redirect('/data_manager/')
    return render(request,"home/register.html")

def signup(request):
    if request.method == "POST":
        uname = request.POST['Uname']
        mail = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['passwd1']
        pass2 = request.POST['passwd2']
        if len(uname)>15:
            return HttpResponse("Username length should not exceed than 15 characters")
        elif pass1 != pass2:
            return HttpResponse("Passwords do not match")
        else :
            us = User.objects.create_user(uname,mail,pass1)
            us.first_name = fname
            us.last_name = lname
            us.save()
            return HttpResponse("Account created")
    else:
        return HttpResponse("Page not found")

def logging(request):
    #print("in views")
    if request.user.is_authenticated:
        return redirect("/data_manager/")
    if request.GET.get('next',None):
        return HttpResponseRedirect(request.GET['next'])
    if request.method == "POST":
        uname = request.POST['logusername']
        passwd = request.POST['logpassword']
        user = authenticate(username=uname,password=passwd)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully logged in")
            request.session['userinfo'] = [uname,passwd]
            param = {"userinfo":[uname,passwd]}
            return redirect('/data_manager/',param)
        else:
            return HttpResponse("Invalid credentials, Please try again")
    else:
        return HttpResponse("You cannot access this page")

@login_required(login_url='/')
def manage(request):
    if request.method == 'POST':
        form = Fileform(request.POST,request.FILES)
        if form.is_valid():
            #print("form validated")
            userinfo = request.session.get('userinfo')
            data = filedata(
                Title = form.cleaned_data["Title"],
                File = form.cleaned_data["File"],
                File_type = form.cleaned_data["File_type"],
                File_description = form.cleaned_data["File_description"],
                date_added = date.today(),
                file_owner = request.user
            )
            file_exists = filedata.objects.filter(Title=form.cleaned_data["Title"]).exists()
            if not file_exists:
                data.save()
                file_added = filedata.objects.get(Title=form.cleaned_data["Title"])
                file_added.file_access.add(request.user)
                messages.success(request,"File Uploaded Successfully")
            else:
                messages.error(request,"A file with same name already exists")
                userinfo = request.session.get('userinfo')
                param = {'form':form,'user':userinfo,'files':filedata.objects.all()}
                return render(request,'home/data_manager.html',param)
        else:
            #print(form.errors)
            userinfo = request.session.get('userinfo')
            param = {'form':form,'user':userinfo,'files':filedata.objects.all()}
            return render(request,'home/data_manager.html',param)
    userinfo = request.session.get('userinfo')
    param = {'user':userinfo,'form':Fileform(),'files':filedata.objects.all()}
    return render(request,'home/data_manager.html',param)

def handlelogout(request):
    logout(request)
    messages.success(request,"Successfully logged out")
    return redirect('/')
    
def protected_media(request, file_id):
    uploaded_file = get_object_or_404(filedata, pk=file_id)
    # print(uploaded_file.file_owner)
    # print(request.user)
    if not uploaded_file.file_access.filter(pk=request.user.id).exists():
        return HttpResponse("You don't have permission to access this file.", status=403)

    file_path = uploaded_file.File.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type=mimetypes.guess_type(file_path)[0])
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    return HttpResponse("File not found", status=404)

@login_required(login_url='/')
def downloader(request, op = ""):
    all_file = filedata.objects.all().order_by(Lower("Title"))
    return render(request,"home/downloader.html",{'files':all_file})

@login_required(login_url='/')
def permissions(request):
    param = {"files":filedata.objects.all(),"users":User.objects.all()}
    return render(request,'home/permissions.html',param)

def change_permissions(request):
    all_file = filedata.objects.all()
    if request.method == "POST":
        for file in all_file:
            if file.file_owner == request.user:
                for user in all_users:
                    if user.username != request.user.username:
                        key = file.Title+"+"+user.username
                        checkbox = request.POST.get(key)
                        #print(checkbox)
                        #print(user.username)
                        if checkbox=="on" and (not file.file_access.filter(pk=user.id).exists()):
                            file.file_access.add(user)
                        #print("giving "+user.username+" permission to access "+file.Title)
                        elif checkbox!="on" and file.file_access.filter(pk=user.id).exists():
                        #print("removing user")
                            file.file_access.remove(user)
        messages.success(request,"Changes saved")
        return redirect("/permissions/")
    else:
        return HttpResponse("Why you here?")
    
def contact(request):
    return render(request,"home/contact.html")

@login_required(login_url="/")
def delete(request):
    return render(request,"home/delete.html",{"files":filedata.objects.filter(file_owner=request.user)})

def deleter(request):
    if request.method == "POST":
        to_delete = []
        for file in filedata.objects.filter(file_owner = request.user):
            key = file.Title
            if request.POST.get(key)=="on":
                to_delete.append(file)
        for files in to_delete:
            path = files.File.path
            if os.path.exists(path):
                os.remove(path)
            files.delete()
        return redirect("/delete_files/")
    else:
        return HttpResponse("Why you here? Here Nothing")

@login_required(login_url="/")
def downloader1(request):
    all_file = filedata.objects.all().order_by("date_added")
    return render(request,"home/downloader.html",{"files":all_file})

@login_required(login_url="/")
def downloader2(request):
    all_file = filedata.objects.all().order_by("File_description")
    return render(request,"home/downloader.html",{"files":all_file})

@login_required(login_url="/")
def downloader3(request):
    all_file = filedata.objects.all().order_by("file_owner")
    return render(request,"home/downloader.html",{"files":all_file})
