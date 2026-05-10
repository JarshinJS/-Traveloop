from django.core.management.base import BaseCommand
from cities.models import City


class Command(BaseCommand):
    help = 'Seed the database with popular cities'

    def handle(self, *args, **options):
        cities_data = [
            {'name': 'Paris', 'country': 'France', 'region': 'Europe', 'description': 'The City of Light, famous for the Eiffel Tower, world-class museums, and exquisite cuisine.', 'cost_index': 180.00, 'popularity_score': 98, 'latitude': 48.856614, 'longitude': 2.352222},
            {'name': 'Tokyo', 'country': 'Japan', 'region': 'Asia', 'description': 'A dazzling blend of ultramodern and traditional, from neon-lit skyscrapers to historic temples.', 'cost_index': 150.00, 'popularity_score': 95, 'latitude': 35.689487, 'longitude': 139.691711},
            {'name': 'Bali', 'country': 'Indonesia', 'region': 'Asia', 'description': 'Tropical paradise known for lush rice terraces, ancient temples, and stunning beaches.', 'cost_index': 55.00, 'popularity_score': 92, 'latitude': -8.340539, 'longitude': 115.091949},
            {'name': 'New York', 'country': 'United States', 'region': 'Americas', 'description': 'The Big Apple — iconic skyline, Broadway shows, Central Park, and incredible diversity.', 'cost_index': 220.00, 'popularity_score': 97, 'latitude': 40.712776, 'longitude': -74.005974},
            {'name': 'Bangkok', 'country': 'Thailand', 'region': 'Asia', 'description': 'Vibrant street life, ornate temples, and legendary street food scene.', 'cost_index': 45.00, 'popularity_score': 90, 'latitude': 13.756331, 'longitude': 100.501765},
            {'name': 'Rome', 'country': 'Italy', 'region': 'Europe', 'description': 'The Eternal City, home to the Colosseum, Vatican, and unmatched Italian cuisine.', 'cost_index': 140.00, 'popularity_score': 94, 'latitude': 41.902782, 'longitude': 12.496366},
            {'name': 'Barcelona', 'country': 'Spain', 'region': 'Europe', 'description': 'Gaudí architecture, Mediterranean beaches, and vibrant nightlife.', 'cost_index': 130.00, 'popularity_score': 91, 'latitude': 41.385064, 'longitude': 2.173404},
            {'name': 'Dubai', 'country': 'UAE', 'region': 'Middle East', 'description': 'Futuristic skyline, luxury shopping, and desert adventures.', 'cost_index': 200.00, 'popularity_score': 88, 'latitude': 25.204849, 'longitude': 55.270783},
            {'name': 'Sydney', 'country': 'Australia', 'region': 'Oceania', 'description': 'Iconic Opera House, stunning harbour, and beautiful beaches.', 'cost_index': 170.00, 'popularity_score': 87, 'latitude': -33.868820, 'longitude': 151.209296},
            {'name': 'Singapore', 'country': 'Singapore', 'region': 'Asia', 'description': 'Garden city with futuristic architecture, incredible food, and cultural diversity.', 'cost_index': 160.00, 'popularity_score': 89, 'latitude': 1.352083, 'longitude': 103.819836},
            {'name': 'Istanbul', 'country': 'Turkey', 'region': 'Europe', 'description': 'Where East meets West — ancient bazaars, stunning mosques, and Bosphorus views.', 'cost_index': 60.00, 'popularity_score': 86, 'latitude': 41.008238, 'longitude': 28.978359},
            {'name': 'London', 'country': 'United Kingdom', 'region': 'Europe', 'description': 'Royal palaces, world-class museums, West End theatre, and iconic landmarks.', 'cost_index': 190.00, 'popularity_score': 96, 'latitude': 51.507351, 'longitude': -0.127758},
            {'name': 'Prague', 'country': 'Czech Republic', 'region': 'Europe', 'description': 'Fairy-tale architecture, historic Old Town, and legendary beer culture.', 'cost_index': 75.00, 'popularity_score': 82, 'latitude': 50.075538, 'longitude': 14.437800},
            {'name': 'Amsterdam', 'country': 'Netherlands', 'region': 'Europe', 'description': 'Charming canals, world-famous museums, and vibrant cultural scene.', 'cost_index': 150.00, 'popularity_score': 85, 'latitude': 52.366697, 'longitude': 4.894540},
            {'name': 'Lisbon', 'country': 'Portugal', 'region': 'Europe', 'description': 'Hilltop city with pastel buildings, historic trams, and delicious pastéis de nata.', 'cost_index': 90.00, 'popularity_score': 84, 'latitude': 38.722252, 'longitude': -9.139337},
            {'name': 'Kyoto', 'country': 'Japan', 'region': 'Asia', 'description': 'Ancient capital with thousands of temples, bamboo forests, and traditional geisha districts.', 'cost_index': 130.00, 'popularity_score': 88, 'latitude': 35.011636, 'longitude': 135.768029},
            {'name': 'Cape Town', 'country': 'South Africa', 'region': 'Africa', 'description': 'Table Mountain, stunning coastline, vibrant culture, and world-class wine regions.', 'cost_index': 65.00, 'popularity_score': 83, 'latitude': -33.924869, 'longitude': 18.424055},
            {'name': 'Maldives', 'country': 'Maldives', 'region': 'Asia', 'description': 'Overwater bungalows, crystal-clear lagoons, and pristine coral reefs.', 'cost_index': 300.00, 'popularity_score': 85, 'latitude': 3.202778, 'longitude': 73.220680},
            {'name': 'Santorini', 'country': 'Greece', 'region': 'Europe', 'description': 'Iconic white-washed buildings, breathtaking sunsets, and volcanic beaches.', 'cost_index': 160.00, 'popularity_score': 90, 'latitude': 36.393154, 'longitude': 25.461510},
            {'name': 'Marrakech', 'country': 'Morocco', 'region': 'Africa', 'description': 'Colorful souks, stunning palaces, and enchanting Jardin Majorelle.', 'cost_index': 50.00, 'popularity_score': 81, 'latitude': 31.629472, 'longitude': -7.981084},
            {'name': 'Rio de Janeiro', 'country': 'Brazil', 'region': 'Americas', 'description': 'Christ the Redeemer, Copacabana beach, samba rhythms, and Carnival celebrations.', 'cost_index': 80.00, 'popularity_score': 86, 'latitude': -22.906847, 'longitude': -43.172897},
            {'name': 'Mexico City', 'country': 'Mexico', 'region': 'Americas', 'description': 'Rich history, incredible street food, vibrant art scene, and ancient ruins.', 'cost_index': 55.00, 'popularity_score': 82, 'latitude': 19.432608, 'longitude': -99.133209},
            {'name': 'Vienna', 'country': 'Austria', 'region': 'Europe', 'description': 'Imperial palaces, classical music heritage, and legendary coffee houses.', 'cost_index': 140.00, 'popularity_score': 80, 'latitude': 48.208174, 'longitude': 16.373819},
            {'name': 'Seoul', 'country': 'South Korea', 'region': 'Asia', 'description': 'K-pop culture, ancient palaces, futuristic technology, and amazing street food.', 'cost_index': 100.00, 'popularity_score': 84, 'latitude': 37.566535, 'longitude': 126.977969},
            {'name': 'Buenos Aires', 'country': 'Argentina', 'region': 'Americas', 'description': 'Tango, incredible steaks, colorful La Boca, and European-style architecture.', 'cost_index': 50.00, 'popularity_score': 79, 'latitude': -34.603684, 'longitude': -58.381559},
            {'name': 'Petra', 'country': 'Jordan', 'region': 'Middle East', 'description': 'Ancient rose-red city carved into cliffs, one of the New Seven Wonders.', 'cost_index': 70.00, 'popularity_score': 78, 'latitude': 30.328460, 'longitude': 35.441394},
            {'name': 'Hanoi', 'country': 'Vietnam', 'region': 'Asia', 'description': 'Centuries-old architecture, bustling Old Quarter, and legendary pho.', 'cost_index': 35.00, 'popularity_score': 80, 'latitude': 21.028511, 'longitude': 105.804817},
            {'name': 'Reykjavik', 'country': 'Iceland', 'region': 'Europe', 'description': 'Gateway to Northern Lights, geysers, glaciers, and the Blue Lagoon.', 'cost_index': 200.00, 'popularity_score': 77, 'latitude': 64.146582, 'longitude': -21.942635},
            {'name': 'Cusco', 'country': 'Peru', 'region': 'Americas', 'description': 'Gateway to Machu Picchu, Inca heritage, and stunning Andean landscapes.', 'cost_index': 45.00, 'popularity_score': 81, 'latitude': -13.531950, 'longitude': -71.967461},
            {'name': 'Dubrovnik', 'country': 'Croatia', 'region': 'Europe', 'description': 'Pearl of the Adriatic — medieval walls, terracotta rooftops, and crystal seas.', 'cost_index': 110.00, 'popularity_score': 79, 'latitude': 42.650661, 'longitude': 18.094424},
        ]

        created_count = 0
        for city_data in cities_data:
            defaults = {
                **city_data,
                'popularity_rating': city_data['popularity_score'],
            }
            _, created = City.objects.update_or_create(
                name=city_data['name'],
                country=city_data['country'],
                defaults=defaults,
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully seeded {created_count} cities ({len(cities_data)} total)')
        )
