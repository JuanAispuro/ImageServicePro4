from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Item
from django.contrib import messages

# from .forms import UploadImageForm

# Register method
def register(request):
    if request.method == "POST":
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            username = f.cleaned_data.get("username")
            raw_password = f.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            print("User registered and logged in.")

            # Redirect the user to the "artworks" page after successful registration and login
            return redirect("/home")

    else:
        f = UserCreationForm()

    return render(request, "registration/registration_form.html", {"form": f})


def index(request):
    return render(request, "collection/index.html", {"data": "Not"})

def UploadImage(request):
    if request.method == "POST":
        prod = Item()
        if len(request.FILES) != 0:
            prod.image = request.FILES['image']

        prod.save()
        messages.success(request, "Product Added Successfully")
        return redirect('uploadImages/uploadImage.html')
    return render(request, 'uploadImages/uploadImage.html')
