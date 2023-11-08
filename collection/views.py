from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator

from .models import (
    Artist,
    Genre,
    Style,
    Period,
    Artwork,
    savedArtworks,
)

def register(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            username = f.cleaned_data.get('username')
            raw_password = f.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return HttpResponseRedirect('/artworks/')

    else:
        f = UserCreationForm()

    return render(request, 'registration/registration_form.html', {'form': f})


def index(request):
    return render(request, 'collection/index.html', {'data': 'Not'})

#  id = models.AutoField(primary_key=True)
#     author = models.ForeignKey(Artist, on_delete=models.RESTRICT)
#     path = models.CharField(max_length=500)
#     title = models.CharField(max_length=500)
#     date = models.CharField(max_length=200, null=True)
#     style = models.ForeignKey(Style, null=True, on_delete=models.RESTRICT)
#     period = models.ForeignKey(Period, null=True, on_delete=models.RESTRICT)
#     genre = models.ForeignKey(Genre, null=True, on_delete=models.RESTRICT)
#     image_url = models.URLField()
def getArtworksAll(request):
    # Get all artworks
    all_artworks = Artwork.objects.all()

    # Create a paginator with a specified number of items per page (e.g., 5 items per page)
    paginator = Paginator(all_artworks, 5)  # Change 5 to the desired number of items per page

    # Get the current page number from the request's query parameters (default to 1)
    page_number = request.GET.get('page', 1)

    # Get the Page object for the current page
    page = paginator.get_page(page_number)

    return render(request, "artwork/favArtwork.html", {"artworks": page})