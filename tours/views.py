import random

from django.http import Http404, HttpResponseServerError
from django.shortcuts import render
from django.views import View
from django.views.defaults import server_error

from .data import title, departures, description, subtitle, tours


# Create your views here.
def custom_handler500(request):
    return HttpResponseServerError('Ой, что-то сервер потерялся! ')


class MainView(View):
    def get(self, request):
        view_lst = []
        i = 0
        while (i < 6):
            num_tour = random.randint(1, len(tours))
            if num_tour not in view_lst:
                view_lst.append(num_tour)
                i = len(view_lst)

        context = {
            'title': title,
            'subtitle': subtitle,
            'description': description,
            'departures': departures,
            'tours': tours,
            'view_lst': view_lst,
        }
        return render(request, 'index.html', context=context)


class DepartureView(View):
    def get(self, request, departure):
        if departure not in departures:
            raise Http404

        tours_dict = {}
        prices_lst = []
        nights_lst = []
        for tour in tours:
            if tours[tour]['departure'] == departure:
                prices_lst.append(tours[tour]['price'])
                nights_lst.append(tours[tour]['nights'])
                tours_dict[tour] = tours[tour]
        context = {
            'title': title,
            'subtitle': subtitle,
            'description': description,
            'departures': departures,
            'tours': tours_dict,
            'city_from': departures[departure],
            'count_tours': len(tours_dict),
            'max_price': max(prices_lst),
            'min_price': min(prices_lst),
            'min_nights': min(nights_lst),
            'max_nights': max(nights_lst),
        }
        return render(request, 'departure.html', context)


class TourView(View):
    def get(self, request, tour_id):
        if tour_id not in tours:
            raise Http404

        context = {
            'title': title,
            'subtitle': subtitle,
            'description': description,
            'departures': departures,
            'tours': tours,
            'id': tour_id,
            'city_from': departures[tours[tour_id]['departure']]
        }
        return render(request, 'tour.html', context)
