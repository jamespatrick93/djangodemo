from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django_demo.models import productmodel
from django.contrib import messages
from django_demo.forms import productforms
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

@login_required
def showproduct(request):
    showall = productmodel.objects.all().order_by('id')
    return render(request, "index.html", {"data" : showall})
@login_required
def insertproduct(request):
    if request.method == "POST":
        if request.POST.get('name') and request.POST.get('description') and request.POST.get('price'):
            insertdata = productmodel()
            insertdata.name =request.POST.get('name')
            insertdata.description = request.POST.get('description')
            insertdata.price = request.POST.get('price')
            insertdata.save()
            messages.success(request, "Product " + insertdata.name + ' is saved successfully')
            return render(request, 'insert.html')
    else:
            return render(request, 'insert.html')

@login_required
def editproduct(request,id):
    editproductobj = productmodel.objects.get(id= id)
    return render(request, 'edit.html', {"editdata" : editproductobj})

@login_required
def updateproduct(request,id):
    updateproductobj = productmodel.objects.get(id= id)
    form = productforms(request.POST, instance=updateproductobj)
    if form.is_valid():
        form.save()
        messages.success(request, "Updated data sucessfully")
        return render(request, 'edit.html', {"editdata" : updateproductobj})

@login_required
def deleteproduct(request,id):
    deleteproductobj = productmodel.objects.get(id= id)
    deleteproductobj.delete()
    showall = productmodel.objects.all().order_by('id')
    return render(request, "index.html", {"data" : showall})

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})
    
@login_required
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("login")