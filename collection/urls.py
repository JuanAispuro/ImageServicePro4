from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("artworks/search", views.search_view, name="search_artworks"),
    path("accounts/profile/artworks/", views.getArtworksAll, name="artworks"),
    path("accounts/profile/", views.SavedArtworks, name="index"),
    path("accounts/register/", views.register, name="register"),
    path('save_artwork/', views.save_artwork, name='save_artwork'),
    path('favorite_artwork/<int:idArtwork>', views.getFavoriteArtwork, name="favorite_artwork"),
    path('allfavorite_artwork/', views.getFavoriteArtworkAll, name="allfavorite_artwork")
]
