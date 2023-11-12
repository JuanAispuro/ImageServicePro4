from django_filters_facet import Facet, FacetedFilterSet
from .models import Artwork

class ArtworkFilter(FacetedFilterSet):
    class Meta:
        model = Artwork
        fields = ["title"]
    
    def configure_facets(self):
        self.filters["title"].facet = Facet()


# class ArtworkFilter(django_filters.FilterSet):

#     def filter_search(self, queryset, name, value):
#         vector = (
#             searchVector("title"))
#         return (
#             queryset.annotate(
#                 search=vector
#             )
#         )