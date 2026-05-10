from django.core.management.base import BaseCommand
from cities.models import City
from activities.models import Activity


class Command(BaseCommand):
    help = 'Seed activities for all seeded cities'

    def handle(self, *args, **options):
        activities_map = {
            'Paris': [
                {'name': 'Eiffel Tower Visit', 'category': 'sightseeing', 'estimated_cost': 26, 'duration_hours': 2.5, 'description': 'Ascend the iconic iron tower for panoramic views of Paris.', 'is_popular': True},
                {'name': 'Louvre Museum', 'category': 'culture', 'estimated_cost': 17, 'duration_hours': 4.0, 'description': 'Explore the world\'s largest art museum, home to the Mona Lisa.', 'is_popular': True},
                {'name': 'Seine River Cruise', 'category': 'sightseeing', 'estimated_cost': 15, 'duration_hours': 1.5, 'description': 'Scenic boat cruise along the Seine passing major landmarks.'},
                {'name': 'French Cooking Class', 'category': 'food', 'estimated_cost': 120, 'duration_hours': 3.0, 'description': 'Learn to make classic French dishes with a professional chef.'},
                {'name': 'Montmartre Walking Tour', 'category': 'culture', 'estimated_cost': 25, 'duration_hours': 2.0, 'description': 'Explore the artistic hilltop neighborhood and Sacré-Cœur.'},
                {'name': 'Paris Metro Day Pass', 'category': 'transport', 'estimated_cost': 13, 'duration_hours': 0.5, 'description': 'Unlimited daily travel on Paris metro and bus network.'},
            ],
            'Tokyo': [
                {'name': 'Senso-ji Temple', 'category': 'culture', 'estimated_cost': 0, 'duration_hours': 1.5, 'description': 'Tokyo\'s oldest Buddhist temple in the heart of Asakusa.', 'is_popular': True},
                {'name': 'Tsukiji Outer Market Food Tour', 'category': 'food', 'estimated_cost': 60, 'duration_hours': 3.0, 'description': 'Sample fresh sushi, wagyu, and street food at the famous market.', 'is_popular': True},
                {'name': 'Shibuya Crossing Experience', 'category': 'sightseeing', 'estimated_cost': 0, 'duration_hours': 1.0, 'description': 'Walk the world\'s busiest pedestrian crossing.'},
                {'name': 'TeamLab Borderless', 'category': 'culture', 'estimated_cost': 32, 'duration_hours': 2.5, 'description': 'Immersive digital art museum with stunning light installations.'},
                {'name': 'Shinkansen to Kyoto', 'category': 'transport', 'estimated_cost': 130, 'duration_hours': 2.5, 'description': 'Ride the bullet train from Tokyo to Kyoto.'},
                {'name': 'Robot Restaurant Show', 'category': 'culture', 'estimated_cost': 80, 'duration_hours': 1.5, 'description': 'Neon-lit cabaret show with robots and dancers in Shinjuku.'},
            ],
            'Bali': [
                {'name': 'Ubud Rice Terrace Trek', 'category': 'adventure', 'estimated_cost': 15, 'duration_hours': 3.0, 'description': 'Walk through stunning Tegallalang rice terraces.', 'is_popular': True},
                {'name': 'Uluwatu Temple Sunset', 'category': 'sightseeing', 'estimated_cost': 5, 'duration_hours': 2.0, 'description': 'Watch the Kecak dance at sunset overlooking the Indian Ocean.', 'is_popular': True},
                {'name': 'Balinese Spa Treatment', 'category': 'relaxation', 'estimated_cost': 30, 'duration_hours': 2.0, 'description': 'Traditional Balinese massage and flower bath ritual.'},
                {'name': 'Surf Lesson at Kuta', 'category': 'adventure', 'estimated_cost': 25, 'duration_hours': 2.0, 'description': 'Beginner-friendly surfing lesson on Kuta Beach.'},
                {'name': 'Cooking Class with Market Visit', 'category': 'food', 'estimated_cost': 35, 'duration_hours': 4.0, 'description': 'Visit a local market then cook traditional Balinese dishes.'},
                {'name': 'Mount Batur Sunrise Hike', 'category': 'adventure', 'estimated_cost': 45, 'duration_hours': 6.0, 'description': 'Pre-dawn hike to the summit of an active volcano.'},
            ],
            'New York': [
                {'name': 'Statue of Liberty & Ellis Island', 'category': 'sightseeing', 'estimated_cost': 24, 'duration_hours': 4.0, 'description': 'Ferry ride and tour of America\'s most iconic monument.', 'is_popular': True},
                {'name': 'Broadway Show', 'category': 'culture', 'estimated_cost': 120, 'duration_hours': 2.5, 'description': 'See a world-class musical or play on Broadway.', 'is_popular': True},
                {'name': 'Central Park Bike Tour', 'category': 'adventure', 'estimated_cost': 40, 'duration_hours': 2.0, 'description': 'Cycle through 843 acres of Manhattan\'s green heart.'},
                {'name': 'Metropolitan Museum of Art', 'category': 'culture', 'estimated_cost': 25, 'duration_hours': 3.0, 'description': 'One of the world\'s greatest art museums.'},
                {'name': 'Pizza Walking Tour', 'category': 'food', 'estimated_cost': 55, 'duration_hours': 2.5, 'description': 'Sample NYC\'s best pizza across multiple iconic pizzerias.'},
                {'name': 'NYC Subway Pass', 'category': 'transport', 'estimated_cost': 33, 'duration_hours': 0.5, 'description': '7-day unlimited MetroCard for subway and bus.'},
            ],
            'Bangkok': [
                {'name': 'Grand Palace & Wat Phra Kaew', 'category': 'sightseeing', 'estimated_cost': 15, 'duration_hours': 2.5, 'description': 'Thailand\'s most sacred temple and former royal residence.', 'is_popular': True},
                {'name': 'Street Food Tour in Chinatown', 'category': 'food', 'estimated_cost': 20, 'duration_hours': 3.0, 'description': 'Taste the best of Bangkok\'s legendary street food scene.', 'is_popular': True},
                {'name': 'Floating Market Visit', 'category': 'shopping', 'estimated_cost': 25, 'duration_hours': 4.0, 'description': 'Explore colorful canal-side markets by longtail boat.'},
                {'name': 'Thai Boxing (Muay Thai) Show', 'category': 'culture', 'estimated_cost': 30, 'duration_hours': 2.0, 'description': 'Watch live Muay Thai fights at a local stadium.'},
                {'name': 'Thai Massage', 'category': 'relaxation', 'estimated_cost': 10, 'duration_hours': 1.5, 'description': 'Traditional Thai massage at a local spa.'},
                {'name': 'Tuk Tuk Night Tour', 'category': 'transport', 'estimated_cost': 35, 'duration_hours': 3.0, 'description': 'See Bangkok\'s illuminated temples by tuk tuk.'},
            ],
            'Rome': [
                {'name': 'Colosseum & Roman Forum', 'category': 'sightseeing', 'estimated_cost': 18, 'duration_hours': 3.0, 'description': 'Explore the iconic amphitheater and ancient ruins.', 'is_popular': True},
                {'name': 'Vatican Museums & Sistine Chapel', 'category': 'culture', 'estimated_cost': 22, 'duration_hours': 3.5, 'description': 'Marvel at Michelangelo\'s masterpiece and priceless art collections.', 'is_popular': True},
                {'name': 'Pasta Making Class', 'category': 'food', 'estimated_cost': 65, 'duration_hours': 2.5, 'description': 'Learn to make fresh pasta from a Roman nonna.'},
                {'name': 'Trastevere Food Tour', 'category': 'food', 'estimated_cost': 50, 'duration_hours': 3.0, 'description': 'Sample Roman specialties in the charming Trastevere neighborhood.'},
                {'name': 'Pantheon Visit', 'category': 'sightseeing', 'estimated_cost': 5, 'duration_hours': 1.0, 'description': 'Visit the best-preserved ancient Roman building.'},
            ],
            'Barcelona': [
                {'name': 'Sagrada Família Tour', 'category': 'sightseeing', 'estimated_cost': 26, 'duration_hours': 2.0, 'description': 'Gaudí\'s unfinished masterpiece basilica.', 'is_popular': True},
                {'name': 'Park Güell', 'category': 'sightseeing', 'estimated_cost': 10, 'duration_hours': 1.5, 'description': 'Colorful mosaic park with panoramic city views.'},
                {'name': 'La Boqueria Market Tour', 'category': 'food', 'estimated_cost': 30, 'duration_hours': 2.0, 'description': 'Explore one of Europe\'s best food markets on Las Ramblas.'},
                {'name': 'Flamenco Show', 'category': 'culture', 'estimated_cost': 40, 'duration_hours': 1.5, 'description': 'Passionate flamenco performance in an intimate venue.'},
                {'name': 'Barceloneta Beach', 'category': 'relaxation', 'estimated_cost': 0, 'duration_hours': 3.0, 'description': 'Relax on Barcelona\'s most popular beach.'},
            ],
            'Dubai': [
                {'name': 'Burj Khalifa Observation Deck', 'category': 'sightseeing', 'estimated_cost': 40, 'duration_hours': 1.5, 'description': 'Visit the observation deck of the world\'s tallest building.', 'is_popular': True},
                {'name': 'Desert Safari', 'category': 'adventure', 'estimated_cost': 65, 'duration_hours': 6.0, 'description': 'Dune bashing, camel riding, and BBQ dinner under the stars.', 'is_popular': True},
                {'name': 'Dubai Mall Shopping', 'category': 'shopping', 'estimated_cost': 0, 'duration_hours': 4.0, 'description': 'Explore the world\'s largest shopping mall with aquarium.'},
                {'name': 'Dhow Dinner Cruise', 'category': 'food', 'estimated_cost': 55, 'duration_hours': 2.0, 'description': 'Traditional boat dinner cruise along Dubai Creek.'},
                {'name': 'Palm Jumeirah Monorail', 'category': 'transport', 'estimated_cost': 8, 'duration_hours': 0.5, 'description': 'Scenic monorail ride across the palm-shaped island.'},
            ],
            'London': [
                {'name': 'Tower of London', 'category': 'culture', 'estimated_cost': 30, 'duration_hours': 3.0, 'description': 'Historic castle housing the Crown Jewels.', 'is_popular': True},
                {'name': 'British Museum', 'category': 'culture', 'estimated_cost': 0, 'duration_hours': 3.0, 'description': 'World-famous museum with the Rosetta Stone and Egyptian mummies.', 'is_popular': True},
                {'name': 'West End Theatre Show', 'category': 'culture', 'estimated_cost': 80, 'duration_hours': 2.5, 'description': 'See a world-class musical or play in London\'s theatre district.'},
                {'name': 'Borough Market Food Tour', 'category': 'food', 'estimated_cost': 45, 'duration_hours': 2.0, 'description': 'Sample artisan foods at London\'s oldest food market.'},
                {'name': 'Oyster Card (Weekly)', 'category': 'transport', 'estimated_cost': 40, 'duration_hours': 0.5, 'description': 'Unlimited tube and bus travel across London zones.'},
                {'name': 'Afternoon Tea Experience', 'category': 'food', 'estimated_cost': 55, 'duration_hours': 2.0, 'description': 'Traditional English afternoon tea at a luxury hotel.'},
            ],
            'Sydney': [
                {'name': 'Opera House Tour', 'category': 'culture', 'estimated_cost': 32, 'duration_hours': 1.5, 'description': 'Behind-the-scenes tour of the iconic Sydney Opera House.', 'is_popular': True},
                {'name': 'Bondi to Coogee Coastal Walk', 'category': 'adventure', 'estimated_cost': 0, 'duration_hours': 2.5, 'description': 'Scenic cliff-top walk between two famous beaches.'},
                {'name': 'Harbour Bridge Climb', 'category': 'adventure', 'estimated_cost': 200, 'duration_hours': 3.0, 'description': 'Climb to the summit of the Sydney Harbour Bridge.'},
                {'name': 'Taronga Zoo', 'category': 'sightseeing', 'estimated_cost': 45, 'duration_hours': 4.0, 'description': 'See native Australian wildlife with harbour views.'},
                {'name': 'Fish & Chips at Sydney Fish Market', 'category': 'food', 'estimated_cost': 20, 'duration_hours': 1.5, 'description': 'Fresh seafood at the Southern Hemisphere\'s largest fish market.'},
            ],
            'Singapore': [
                {'name': 'Gardens by the Bay', 'category': 'sightseeing', 'estimated_cost': 20, 'duration_hours': 2.5, 'description': 'Futuristic park with Supertree Grove and Cloud Forest.', 'is_popular': True},
                {'name': 'Hawker Centre Food Tour', 'category': 'food', 'estimated_cost': 15, 'duration_hours': 2.5, 'description': 'Taste Michelin-starred street food and local favorites.', 'is_popular': True},
                {'name': 'Sentosa Island', 'category': 'relaxation', 'estimated_cost': 30, 'duration_hours': 5.0, 'description': 'Resort island with beaches, Universal Studios, and attractions.'},
                {'name': 'Marina Bay Sands SkyPark', 'category': 'sightseeing', 'estimated_cost': 23, 'duration_hours': 1.0, 'description': 'Observation deck with 360-degree views of the city.'},
                {'name': 'Night Safari', 'category': 'adventure', 'estimated_cost': 42, 'duration_hours': 3.0, 'description': 'World\'s first nocturnal wildlife park.'},
            ],
            'Istanbul': [
                {'name': 'Hagia Sophia', 'category': 'culture', 'estimated_cost': 12, 'duration_hours': 1.5, 'description': 'Byzantine masterpiece turned mosque, a symbol of Istanbul.', 'is_popular': True},
                {'name': 'Grand Bazaar Shopping', 'category': 'shopping', 'estimated_cost': 0, 'duration_hours': 3.0, 'description': 'Explore one of the world\'s oldest and largest covered markets.'},
                {'name': 'Bosphorus Cruise', 'category': 'sightseeing', 'estimated_cost': 10, 'duration_hours': 2.0, 'description': 'Cruise between Europe and Asia along the Bosphorus strait.'},
                {'name': 'Turkish Bath (Hamam)', 'category': 'relaxation', 'estimated_cost': 35, 'duration_hours': 1.5, 'description': 'Traditional Ottoman bathing experience.'},
                {'name': 'Turkish Breakfast Feast', 'category': 'food', 'estimated_cost': 15, 'duration_hours': 1.5, 'description': 'Lavish traditional Turkish breakfast spread.'},
            ],
            'Santorini': [
                {'name': 'Oia Sunset Viewing', 'category': 'sightseeing', 'estimated_cost': 0, 'duration_hours': 2.0, 'description': 'Watch the world-famous sunset from Oia\'s clifftop.', 'is_popular': True},
                {'name': 'Catamaran Cruise', 'category': 'adventure', 'estimated_cost': 120, 'duration_hours': 5.0, 'description': 'Sail around the caldera with swimming and BBQ lunch.'},
                {'name': 'Wine Tasting Tour', 'category': 'food', 'estimated_cost': 50, 'duration_hours': 3.0, 'description': 'Sample volcanic wines at traditional wineries.'},
                {'name': 'Red Beach Visit', 'category': 'relaxation', 'estimated_cost': 0, 'duration_hours': 2.0, 'description': 'Unique volcanic red sand beach near Akrotiri.'},
                {'name': 'Akrotiri Archaeological Site', 'category': 'culture', 'estimated_cost': 12, 'duration_hours': 1.5, 'description': 'Ancient Minoan city preserved in volcanic ash.'},
            ],
            'Kyoto': [
                {'name': 'Fushimi Inari Shrine', 'category': 'culture', 'estimated_cost': 0, 'duration_hours': 2.0, 'description': 'Walk through thousands of vermilion torii gates.', 'is_popular': True},
                {'name': 'Arashiyama Bamboo Grove', 'category': 'sightseeing', 'estimated_cost': 0, 'duration_hours': 1.5, 'description': 'Stroll through the magical bamboo forest.'},
                {'name': 'Tea Ceremony Experience', 'category': 'culture', 'estimated_cost': 40, 'duration_hours': 1.5, 'description': 'Traditional Japanese tea ceremony with a tea master.'},
                {'name': 'Geisha District Walking Tour', 'category': 'culture', 'estimated_cost': 30, 'duration_hours': 2.0, 'description': 'Explore Gion and spot geiko and maiko.'},
                {'name': 'Kaiseki Dinner', 'category': 'food', 'estimated_cost': 100, 'duration_hours': 2.0, 'description': 'Multi-course traditional Japanese haute cuisine.'},
            ],
            'Cape Town': [
                {'name': 'Table Mountain Cable Car', 'category': 'sightseeing', 'estimated_cost': 18, 'duration_hours': 2.5, 'description': 'Ride to the top of the iconic flat-topped mountain.', 'is_popular': True},
                {'name': 'Cape Peninsula Tour', 'category': 'sightseeing', 'estimated_cost': 60, 'duration_hours': 8.0, 'description': 'Day trip to Cape Point, penguins at Boulders Beach.'},
                {'name': 'Wine Tasting in Stellenbosch', 'category': 'food', 'estimated_cost': 40, 'duration_hours': 5.0, 'description': 'Sample world-class wines in the Cape Winelands.'},
                {'name': 'Shark Cage Diving', 'category': 'adventure', 'estimated_cost': 120, 'duration_hours': 6.0, 'description': 'Get up close with great white sharks.'},
                {'name': 'V&A Waterfront', 'category': 'shopping', 'estimated_cost': 0, 'duration_hours': 3.0, 'description': 'Shopping, dining, and entertainment at the harbour.'},
            ],
            'Marrakech': [
                {'name': 'Jardin Majorelle', 'category': 'sightseeing', 'estimated_cost': 10, 'duration_hours': 1.5, 'description': 'Stunning blue garden once owned by Yves Saint Laurent.', 'is_popular': True},
                {'name': 'Medina Souk Tour', 'category': 'shopping', 'estimated_cost': 15, 'duration_hours': 3.0, 'description': 'Navigate the labyrinthine market with a local guide.'},
                {'name': 'Moroccan Cooking Class', 'category': 'food', 'estimated_cost': 30, 'duration_hours': 3.0, 'description': 'Learn to make tagine and couscous with a local chef.'},
                {'name': 'Hammam Spa Experience', 'category': 'relaxation', 'estimated_cost': 25, 'duration_hours': 2.0, 'description': 'Traditional Moroccan steam bath and scrub.'},
                {'name': 'Sahara Desert Day Trip', 'category': 'adventure', 'estimated_cost': 80, 'duration_hours': 10.0, 'description': 'Camel ride and sunset in the Agafay Desert.'},
            ],
        }

        created_count = 0
        for city_name, activities in activities_map.items():
            try:
                city = City.objects.get(name=city_name)
            except City.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'City not found: {city_name}. Skipping.'))
                continue

            for act_data in activities:
                defaults = act_data.copy()
                is_popular = defaults.pop('is_popular', False)
                defaults.update({
                    'is_popular': is_popular,
                    'cost': defaults['estimated_cost'],
                    'duration_minutes': int(float(defaults['duration_hours']) * 60),
                })
                _, created = Activity.objects.update_or_create(
                    city=city,
                    name=act_data['name'],
                    defaults=defaults,
                )
                if created:
                    created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully seeded {created_count} activities')
        )
