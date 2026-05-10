from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from cities.models import City
from .models import Activity


class ActivityViewTests(TestCase):
    def setUp(self):
        self.city = City.objects.create(
            name='Rome',
            country='Italy',
            region='Europe',
            cost_index='140.00',
            popularity_score=88,
        )
        self.food = Activity.objects.create(
            city=self.city,
            name='Pasta Walk',
            description='A guided food tour.',
            category='food',
            estimated_cost='45.00',
            duration_hours='2.5',
            is_popular=True,
        )
        self.museum = Activity.objects.create(
            city=self.city,
            name='Museum Morning',
            description='Culture and art.',
            category='culture',
            estimated_cost='75.00',
            duration_hours='3.0',
        )

    def test_activities_root_uses_search_view(self):
        response = self.client.get('/activities/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pasta Walk')

    def test_activity_search_filters_by_category_and_max_cost(self):
        response = self.client.get(reverse('activity_search'), {
            'category': 'food',
            'max_cost': '50',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pasta Walk')
        self.assertNotContains(response, 'Museum Morning')

    def test_activity_detail_renders_activity(self):
        response = self.client.get(reverse('activity_detail', args=[self.food.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pasta Walk')


class SeedActivitiesCommandTests(TestCase):
    def test_seed_activities_is_idempotent(self):
        out = StringIO()
        call_command('seed_cities', stdout=out)
        call_command('seed_activities', stdout=out)
        first_count = Activity.objects.count()
        call_command('seed_activities', stdout=out)

        self.assertGreater(first_count, 0)
        self.assertEqual(Activity.objects.count(), first_count)
        self.assertTrue(Activity.objects.filter(name='Eiffel Tower Visit', cost__gt=0).exists())
