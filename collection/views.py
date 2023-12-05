from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Item
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

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
            return redirect("UploadImage")

    else:
        f = UserCreationForm()

    return render(request, "registration/registration_form.html", {"form": f})


def index(request):
    return render(request, "collection/index.html", {"data": "Not"})


def test(request):
    return render(request, "ws.html")


def process_and_save_image(original_image):
    processed_image_1 = original_image.transpose(Image.FLIP_LEFT_RIGHT)
    processed_image_2 = original_image.rotate(90)
    processed_image_3 = original_image.rotate(180)
    processed_image_4 = original_image.rotate(270)

    original_image_identifier = hash(original_image.tobytes())

    try:
        item = Item.objects.get(original_image_identifier=original_image_identifier)
    except Item.DoesNotExist:
        item = Item(original_image_identifier=original_image_identifier)

    item.imageOriginal.save("original_image.jpg", process_and_get_image(original_image))
    item.imageProcessed1.save(
        "processed_image_1.jpg", process_and_get_image(processed_image_1)
    )
    item.imageProcessed2.save(
        "processed_image_2.jpg", process_and_get_image(processed_image_2)
    )
    item.imageProcessed3.save(
        "processed_image_3.jpg", process_and_get_image(processed_image_3)
    )
    item.imageProcessed4.save(
        "processed_image_4.jpg", process_and_get_image(processed_image_4)
    )


def process_and_get_image(image):
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    processed_image = InMemoryUploadedFile(
        buffer, None, "processed_image.jpg", "image/jpeg", buffer.tell(), None, None
    )

    return processed_image


def UploadImage(request):
    img= None
    if request.method == "POST":
        if "image" in request.FILES:
            image = request.FILES["image"]
            img = Image.open(image)
            process_and_save_image(img)
            print(img)
            print(" ------------ ")
            messages.success(request, "Images Added Successfully")
            return redirect("UploadImage")

    return render(request, "uploadImages/uploadImage.html")

    return render(request, 'uploadImages/uploadImage.html')