from django.shortcuts import render, get_object_or_404
from .models import City


def city_search_view(request):
    cities = City.objects.all()
    query = request.GET.get('q', '')
    region = request.GET.get('region', '')

    if query:
        cities = cities.filter(
            models.Q(name__icontains=query) |
            models.Q(country__icontains=query) |
            models.Q(region__icontains=query)
        )

    if region:
        cities = cities.filter(region__iexact=region)

    regions = City.objects.values_list('region', flat=True).distinct().order_by('region')
    regions = [r for r in regions if r]  # filter out blanks

    context = {
        'cities': cities,
        'query': query,
        'selected_region': region,
        'regions': regions,
    }
    return render(request, 'cities/search.html', context)


def city_detail_view(request, pk):
    city = get_object_or_404(City, pk=pk)
    activities = city.activities.all()

    context = {
        'city': city,
        'activities': activities,
    }
    return render(request, 'cities/city_detail.html', context)
