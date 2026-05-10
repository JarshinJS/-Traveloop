from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Activity
from cities.models import City


def activity_search_view(request):
    activities = Activity.objects.select_related('city').all()
    city_id = request.GET.get('city_id', '')
    category = request.GET.get('category', '')
    max_cost = request.GET.get('max_cost', '')
    query = request.GET.get('q', '')

    if city_id:
        activities = activities.filter(city_id=city_id)

    if category:
        activities = activities.filter(category=category)

    if max_cost:
        try:
            activities = activities.filter(estimated_cost__lte=float(max_cost))
        except ValueError:
            pass

    if query:
        activities = activities.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    categories = Activity.CATEGORY_CHOICES
    cities = City.objects.all().order_by('name')

    context = {
        'activities': activities,
        'categories': categories,
        'cities': cities,
        'selected_city_id': city_id,
        'selected_category': category,
        'max_cost': max_cost,
        'query': query,
    }
    return render(request, 'activities/search.html', context)


def activity_detail_view(request, pk):
    activity = get_object_or_404(Activity.objects.select_related('city'), pk=pk)
    context = {'activity': activity}
    return render(request, 'activities/activity_detail.html', context)
