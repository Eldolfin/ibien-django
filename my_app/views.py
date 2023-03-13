from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Sell, UserProfile
from .forms import SellForm


# I make heavy use of the generic views of Django
# to avoid writing as much code as possible.
# This avoids many bugs and makes the code more readable.
# I only need to provide the correct class parameters
# and the generic views will do the rest.

# IndexView is the view that shows the list of items.
# It is the home page of the website.
class IndexView(generic.ListView):
    template_name = 'my_app/index.html'
    context_object_name = 'latest_posts_list'

    def get_queryset(self):
        """Return the last ten published items."""
        return Sell.objects.order_by('-pub_date')[:10]


class SellView(generic.CreateView, LoginRequiredMixin):
    # SellView is the view that allows the user to sell an item.
    # It is the page where the user can fill the form to sell an item.
    # It fullfills the Create part of the CRUD.
    model = Sell
    form_class = SellForm
    template_name = 'my_app/sell.html'

    def form_valid(self, form):
        candidate = form.save(commit=False)
        # here we automatically set the seller and the location fields
        # of the item to the profile of the user and its location
        profile = UserProfile.objects.get(user=self.request.user)
        candidate.seller = profile
        candidate.location = profile.location
        candidate.save()
        return super(SellView, self).form_valid(form)

    def get_success_url(self):
        return '/'


class MySellsView(generic.ListView, LoginRequiredMixin):
    # MySellsView is the view that shows the list of items
    # that the user has sold.
    # It is there that users can edit their items.
    template_name = 'my_app/my_sells.html'
    context_object_name = 'my_sells_list'

    def get_queryset(self):
        """Return the list of all the sells of the user.
           ordered by date of publication (most recent first)."""
        return (Sell.objects
                .filter(seller__user=self.request.user)
                .order_by('-pub_date')
                )


class EditSellView(generic.UpdateView, LoginRequiredMixin):
    # EditSellView is the view that allows the user to edit an item.
    # It is also the view that allows the user to delete an item.
    # It fullfills the Update part of the CRUD.
    model = Sell
    form_class = SellForm
    template_name = 'my_app/edit_item.html'
    success_url = '/my_sells/'


class DeleteSellView(generic.DeleteView, LoginRequiredMixin):
    # DeleteSellView is the view that allows the user to delete an item.
    # It is the page where the user can confirm the deletion of an item.
    # It provides the user with a confirmation page.
    # It fullfills the Delete part of the CRUD.
    model = Sell
    template_name = 'my_app/delete_item.html'
    success_url = '/my_sells/'
