from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.postgres import search
from django.contrib import messages

from .models import (
    Artwork,
    savedArtworks,
)


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
            return redirect("artworks")

    else:
        f = UserCreationForm()

    return render(request, "registration/registration_form.html", {"form": f})


def index(request):
    return render(request, "collection/index.html", {"data": "Not"})


# method for artworks page
def getArtworksAll(request):
    # Get all artworks
    all_artworks = Artwork.objects.all()
    paginator = Paginator(all_artworks, 5)
    page_number = request.GET.get("page", 1)
    # Get the Page object for the current page
    page = paginator.get_page(page_number)

    return render(request, "artwork/allArtworks.html", {"artworks": page})


# method for favoriting artworks
def getFavoriteArtwork(request, idArtwork):
    # movie = Movie.objects.get(tmdb_id=idDB)
    favArtwork = savedArtworks.objects.get(userfK=request.user, artworkfK=idArtwork)
    print("GetFavorite function")
    if favArtwork.favorited == True:
        favArtwork.favorited = False
        favArtwork.save()
        messages.success(request, "The artwork has been removed successfully!")
        return redirect(to="favorite_artwork")

    elif favArtwork.favorited == False:
        favArtwork.favorited = True
        favArtwork.save()
        messages.success(request, "The artwork has been favorited successfully!")
        return redirect(to="favorite_artwork")

    return render(request, "artwork/favoriteArtworks.html", {"artworks": favArtwork})


# method for favorite artworks page
def getFavoriteArtworkAll(request):
    saved_artwork_entries = savedArtworks.objects.filter(
        userfK=request.user, favorited=True
    )
    # Retrieve the actual artworks associated with the saved entries
    saved_artworks = [entry.artworkfK for entry in saved_artwork_entries]

    # adds pagination
    paginator = Paginator(saved_artworks, 5)

    # Get the current page number from the request's query parameters
    page_number = request.GET.get("page", 1)

    # Get the Page object for the current page
    page = paginator.get_page(page_number)
    print(page.paginator.num_pages)
    print("Esta aqui ")
    return render(request, "artwork/favoriteArtworks.html", {"favArtworks": page})


# This is for when the user is logged in, it sends the user to his saved artworks page
@login_required
def SavedArtworks(request):
    # Get all saved artworks for the current user
    saved_artwork_entries = savedArtworks.objects.filter(
        userfK=request.user,
        favorited=False,
    )

    # Retrieve the actual artworks associated with the saved entries
    saved_artworks = [entry.artworkfK for entry in saved_artwork_entries]

    paginator = Paginator(saved_artworks, 5)

    # Get the current page number from the request's query parameters
    page_number = request.GET.get("page", 1)

    # Get the Page object for the current page
    page = paginator.get_page(page_number)

    return render(request, "artwork/savedArtworks.html", {"artworks": page})


# This is the method for saving artworks
def save_artwork(request):
    if request.method == "POST" and request.user.is_authenticated:
        artwork_id = request.POST.get("artwork_id")
        print(artwork_id)
        try:
            artwork = Artwork.objects.get(pk=artwork_id)
            # Create or update a savedArtworks entry for the user and artwork
            saved, created = savedArtworks.objects.get_or_create(
                userfK=request.user, artworkfK=artwork
            )

            if not created:
                saved.favorited = not saved.favorited
                saved.save()
                messages.success(request, "The artwork has been saved successfully!")
                return redirect(to="save_artwork")
            else:
                saved.delete()
                messages.success(request, "The artwork has been removed successfully!")
                return redirect(to="save_artwork")

        except Artwork.DoesNotExist:
            messages.success(request, "The artwork has been removed successfully!")
            return redirect(to="save_artwork")

    return JsonResponse({"success": False, "message": "Authentication required."})


# This is the search page method
def search_view(request):
    value = request.GET["search"]
    IndiArtworks = filterArwork(value)
    paginator = Paginator(IndiArtworks, 5)
    page_number = request.GET.get("page", 1)
    page = paginator.get_page(page_number)
    return render(
        request,
        "artwork/artwork_search.html",
        {"artworks": IndiArtworks, "valorbuscado": value, "page_obj": page},
    )


# this is the method for the search bar
def filterArwork(value):
    vector = (
        search.SearchVector("title", weight="A")
        + search.SearchVector("author__name", weight="B")
        + search.SearchVector("style__name", weight="C")
        + search.SearchVector("genre__name", weight="C")
    )
    query = search.SearchQuery(value, search_type="websearch")
    return (
        Artwork.objects.annotate(
            search=vector,
            rank=search.SearchRank(vector, query),
        )
        .filter(search=query)
        .order_by("-rank")
    )
