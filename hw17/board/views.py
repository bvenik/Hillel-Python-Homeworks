from django.views.generic import ListView, DetailView
from .models import Ad

class AdListView(ListView):
    """
    Renders a list of all active advertisements.
    """
    model = Ad
    template_name = 'board/ad_list.html'
    context_object_name = 'ads'

    def get_queryset(self):
        """
        Filters the default queryset to include active ads only.

        :return: QuerySet of active advertisements.
        """
        return Ad.objects.filter(is_active=True)

class AdDetailView(DetailView):
    """
    Renders detailed information about a single advertisement.
    """
    model = Ad
    template_name = 'board/ad_detail.html'
    context_object_name = 'ad'