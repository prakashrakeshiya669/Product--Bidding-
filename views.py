from django.http import HttpResponse
from django.shortcuts import render,redirect
from . import emailAPI
from . import models
import time

#middleware to check session for mainapp routes
def sessioncheck_middleware(get_response):
	def middleware(request):
		if request.path=='/home/' or request.path=='/about/' or request.path=='/contact/' or request.path=='/login/' or request.path=='/service/' or request.path=='/register/':
			request.session['sesunm']=None
			request.session['sesrole']=None
			response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware
# create Views Here
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def service(request):
    return render(request, 'service.html')

def register(request):
    if request.method=="GET":
        return render(request, 'register.html',{"output":""})
    else:
        #to recive data from UI
        name=request.POST.get("name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        mobile=request.POST.get("mobile")
        address=request.POST.get("address")
        city=request.POST.get("city")
        gender=request.POST.get("gender")

        #to send verification email
        emailAPI.sendMail(email,password)

        #insert record in data base table
        r=models.Register(name=name, email=email, password=password, mobile=mobile,address=address, city=city, gender=gender,status=0,role="user",info=time.asctime())
        
        r.save()
        
        return render(request, 'register.html',{"output": "User Register Successfull.........!"})

def verify(request):
    vemail=request.GET.get("vemail")
    #print(vemail)
    #return HttpResponse("This is Verify email")
    models.Register.objects.filter(email=vemail).update(status=1)
    
    return redirect("/login/")

def login(request):
    cunm,cpass="",""
    if request.COOKIES.get("cunm")!=None:
        cunm=request.COOKIES.get("cunm")
        cpass=request.COOKIES.get("cpass")
    print(request.COOKIES.get("cunm"))
    if request.method=="GET":
     return render(request, 'login.html', {"cunm":cunm,"cpass":cpass,"output":" "})
    else:
      email=request.POST.get("email")
      password=request.POST.get("password")
      chk=request.POST.get("chk")
      #print(chk)

      userDetails=models.Register.objects.filter(email=email,password=password,status=1 )
        
      if len(userDetails)>0:
        #to store user Details in session
        request.session["sesunm"]=userDetails[0].email
        request.session["sesrole"]=userDetails[0].role

        if userDetails[0].role=="admin":
            response=redirect("/myadmin/")
             #return render(request,'login.html', {"output": " Login Success as a admin"})
        else:
            response= redirect("/user/")
            #return render(request,'login.html', {"output": " Login Success as a user"})
        #to store Cookies in response
        if chk!=None:
            response.set_cookie("cunm",userDetails[0].email,3600*24*365*100)
            response.set_cookie("cpass",userDetails[0].password,3600)
        return response
      else:
            return render(request,'login.html',{"cunm":cunm,"cpass":cpass,"output": "Invalid User or verify your Account"})
        
def ajaxresponse(request):
    return HttpResponse("<h1>This is Ajax code working Here</h1>")

def checkEmailAJAX(request):
    email=request.GET.get("email")
    userDetails=models.Register.objects.filter(email__startswith=email)
    flag=0
    if len(userDetails)>0:
        flag=1
    return HttpResponse(flag)

def vemail(request):
    if request.method=="GET":
     return render(request, 'vemail.html')
    else:
        email=request.POST.get("email")
        ems=models.Register.objects.filter(email=email)
        if len(ems)>0:
            return render(request,'forget.html',{"msg":"Your Email verify is successfulll"})
        else:
            return render(request, 'vemail.html',{"msg":"Incorrect Your email"})
def forget(request):
    if request.method=="GET":
        email=request.GET.get("email")
        user=models.Register.objects.filter(email=email)
        print(user)
        return render(request, 'forget.html',{"msg":""})
    else:
        #to recive the data from UI
        email=request.POST.get("email")
        npassword=request.POST.get("npassword")
        cnpassword=request.POST.get("cnpassword")
        models.Register.objects.filter(email=email)
        #password or Confirm Password are Matching 
    if npassword==cnpassword:
        models.Register.objects.filter(email=email).update(password=npassword)
        return render(request,'forget.html',{"msg":"password change Successfullly...."})
    else:
        return render(request, 'forget.html',{"msg":"New Password and Confirm Password Are Not Match"})
