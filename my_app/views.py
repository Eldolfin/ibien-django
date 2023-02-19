from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Sell, UserProfile
from .forms import SellForm

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'my_app/index.html'
    context_object_name = 'latest_posts_list'

    def get_queryset(self):
        """Return the last ten published items."""
        return Sell.objects.order_by('-pub_date')[:10]


class SellView(generic.CreateView, LoginRequiredMixin):
    model = Sell
    form_class = SellForm
    template_name = 'my_app/sell.html'

    def form_valid(self, form):
        candidate = form.save(commit=False)
        profile = UserProfile.objects.get(user=self.request.user)
        candidate.seller = profile
        candidate.location = profile.location
        candidate.save()
        return super(SellView, self).form_valid(form)

    def get_success_url(self):
        return '/'


class MySellsView(generic.ListView, LoginRequiredMixin):
    template_name = 'my_app/my_sells.html'
    context_object_name = 'my_sells_list'

    def get_queryset(self):
        """Return the list of all the sells of the user."""
        return (Sell.objects
                .filter(seller__user=self.request.user)
                .order_by('-pub_date')
                )


class EditSellView(generic.UpdateView, LoginRequiredMixin):
    model = Sell
    form_class = SellForm
    template_name = 'my_app/edit_item.html'

    def get_success_url(self):
        return '/my_sells/'


class DeleteSellView(generic.DeleteView, LoginRequiredMixin):
    model = Sell
    template_name = 'my_app/delete_item.html'
    success_url = '/my_sells/'
