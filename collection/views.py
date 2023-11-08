from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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

            # Debug: Print a message to check if this block is executed
            print("User registered and logged in.")

            # Redirect the user to the "artworks" page after successful registration and login
            return redirect("artworks")

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
    
    return render(request, "artwork/allArtworks.html", {"artworks": page})

@login_required
def SavedArtworks(request):
    # Get all saved artworks for the current user
    saved_artwork_entries = savedArtworks.objects.filter(userfK=request.user, favorited=False)

    # Retrieve the actual artworks associated with the saved entries
    saved_artworks = [entry.artworkfK for entry in saved_artwork_entries]

    # Create a paginator with a specified number of items per page (e.g., 5 items per page)
    paginator = Paginator(saved_artworks, 5)  # Change 5 to the desired number of items per page

    # Get the current page number from the request's query parameters (default to 1)
    page_number = request.GET.get('page', 1)

    # Get the Page object for the current page
    page = paginator.get_page(page_number)

    return render(request, "artwork/savedArtworks.html", {"artworks": page})

def save_artwork(request):
    if request.method == 'POST' and request.user.is_authenticated:
        artwork_id = request.POST.get('artwork_id')
        print(artwork_id)
        try:
            artwork = Artwork.objects.get(pk=artwork_id)
            # Create or update a savedArtworks entry for the user and artwork
            saved, created = savedArtworks.objects.get_or_create(userfK=request.user, artworkfK=artwork)
            if not created:
                saved.favorited = not saved.favorited
                saved.save()
            return JsonResponse({'success': True, 'message': 'Artwork saved successfully.'})
        except Artwork.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Artwork not found.'})

    return JsonResponse({'success': False, 'message': 'Authentication required.'})