from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/profile/artworks/", views.getArtworksAll, name="artworks"),
#    que te mande directo a nuestras piezas guardadas
    path("accounts/profile/", views.SavedArtworks, name="index"),
    path("accounts/register/", views.register, name="register"),
    path('save_artwork/', views.save_artwork, name='save_artwork'),

]
