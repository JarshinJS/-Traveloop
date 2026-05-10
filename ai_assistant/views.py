"""
AI Assistant — Chatbot & Smart Suggestion engine for Traveloop.

Uses Google Gemini as the LLM backend.
Falls back gracefully if GEMINI_API_KEY is not set.
"""
import json
import logging
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.conf import settings

from cities.models import City
from activities.models import Activity
from trips.models import Trip, TripStop

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────
#  Gemini helper
# ─────────────────────────────────────────────────────────

def _get_gemini_model():
    """Return a configured Gemini GenerativeModel or None if key is missing."""
    api_key = getattr(settings, "GEMINI_API_KEY", None)
    if not api_key or api_key == "your-gemini-api-key-here":
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        logger.error("Gemini model init failed: %s", e)
        return None


SYSTEM_PROMPT = """
You are "Trave", a friendly and knowledgeable AI travel assistant built into the Traveloop web application.

## Your Personality
- Warm, enthusiastic, and helpful — like a well-travelled friend
- Concise but thorough — no unnecessary padding
- Always guide the user towards taking action in the app

## Traveloop Application Overview
Traveloop is a trip-planning Django web application. Here are the key features and their URLs:

| Feature | URL | Description |
|---|---|---|
| Dashboard | /dashboard/ | Overview of all trips, stats, upcoming events |
| My Trips | /trips/ | List all user trips with tabs for Active/Upcoming/Past |
| Create Trip | /trips/new/ | Multi-step form to create a new trip |
| Trip Detail | /trips/<id>/ | Overview, tabs for Itinerary, Budget, Packing, Notes |
| Itinerary Builder | /trips/<id>/itinerary/builder/ | Add/remove stops and activities with drag-and-drop |
| Itinerary View | /trips/<id>/itinerary/ | Read-only timeline or list view of the full itinerary |
| Budget Analysis | /trips/<id>/budget/ | Doughnut/bar charts, cost breakdown by city & category |
| Packing Checklist | /trips/<id>/packing/ | Categorized checklist with progress tracking |
| Notes / Journal | /trips/<id>/notes/ | Rich journal entries linked to specific stops |
| Explore Cities | /cities/ | Browse and filter all destination cities |
| City Detail | /cities/<id>/ | Info, cost index, popularity, curated activities for a city |
| Experiences | /activities/ | Filter activities by city, type, and max cost |
| Activity Detail | /activities/<id>/ | Full activity info with "Add to Journey" action |
| Profile | /accounts/profile/ | Edit name, email, avatar, and preferences |

## Your Capabilities
1. **Navigation help**: Guide users to the right page with clickable links formatted as: [Link Text](/url/)
2. **Feature explanations**: Explain how any feature works step-by-step
3. **Travel tips**: Offer general travel advice and best practices for planning
4. **App troubleshooting**: Help with common usage questions

## Important Rules
- NEVER make up data about specific trips, cities, or activities — these are from the user's database
- For specific data questions (e.g., "What did I plan for Paris?"), suggest the user check the relevant app page
- Always include an actionable link where appropriate
- Keep responses under 200 words unless the user asks for detail
- Respond in plain text with markdown formatting (bold, lists, links)
"""


# ─────────────────────────────────────────────────────────
#  1. Chat endpoint
# ─────────────────────────────────────────────────────────

@require_POST
def chat_api(request):
    """
    POST /api/ai/chat/
    Body: { "message": "...", "history": [{"role": "user|model", "parts": ["..."]}] }
    Returns: { "reply": "..." }
    """
    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
        history = data.get("history", [])  # [{role, parts:[text]}]
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({"error": "Invalid request body"}, status=400)

    if not user_message:
        return JsonResponse({"error": "Empty message"}, status=400)

    model = _get_gemini_model()

    if model is None:
        # Fallback rule-based responses when no API key is set
        reply, links = _rule_based_response(user_message)
        return JsonResponse({"reply": reply, "links": links})

    try:
        # Build chat with full history for context
        chat = model.start_chat(history=history)
        # Prepend system prompt to first message if history is empty
        if not history:
            full_message = f"{SYSTEM_PROMPT}\n\nUser: {user_message}"
        else:
            full_message = user_message

        response = chat.send_message(full_message)
        reply = response.text
    except Exception as e:
        logger.error("Gemini chat error: %s", e)
        reply, links = _rule_based_response(user_message)
        return JsonResponse({"reply": reply, "links": links})

    return JsonResponse({"reply": reply, "links": []})


def _rule_based_response(message: str) -> tuple[str, list[dict[str, str]]]:
    """Minimal rule-based fallback when Gemini is unavailable."""
    msg = message.lower()

    if any(w in msg for w in ["create trip", "new trip", "add trip", "plan trip"]):
        return (
            "To create a new trip, head to [Create Trip](/trips/create/) and enter your dates, budget, and sharing preference.",
            [{"label": "Create Trip", "url": "/trips/create/"}],
        )
    if any(w in msg for w in ["my trips", "trips", "journeys"]):
        return (
            "You can see every journey you own on [My Trips](/trips/).",
            [{"label": "My Trips", "url": "/trips/"}],
        )
    if any(w in msg for w in ["dashboard", "home", "overview"]):
        return (
            "Your [Dashboard](/dashboard/) gives you an overview of upcoming journeys and quick stats.",
            [{"label": "Dashboard", "url": "/dashboard/"}],
        )
    if any(w in msg for w in ["itinerary", "builder", "stop", "stops"]):
        return (
            "Open a trip from [My Trips](/trips/) and use the itinerary builder to add destinations and reorder stops.",
            [{"label": "My Trips", "url": "/trips/"}],
        )
    if any(w in msg for w in ["budget", "cost", "money", "spending"]):
        return (
            "Open a trip from [My Trips](/trips/) and choose Budget to track entries, charts, and over-budget alerts.",
            [{"label": "My Trips", "url": "/trips/"}],
        )
    if any(w in msg for w in ["pack", "packing", "checklist", "luggage"]):
        return (
            "Your packing checklist lives inside each trip and tracks progress as you check items off.",
            [{"label": "My Trips", "url": "/trips/"}],
        )
    if any(w in msg for w in ["note", "journal", "diary", "write"]):
        return (
            "The journey journal lets you save notes linked to a specific stop or the whole trip.",
            [{"label": "My Trips", "url": "/trips/"}],
        )
    if any(w in msg for w in ["city", "cities", "destination", "explore"]):
        return (
            "Browse destinations on [Explore Cities](/cities/), filter by region, and add cities to a journey.",
            [{"label": "Explore Cities", "url": "/cities/"}],
        )
    if any(w in msg for w in ["activity", "activities", "experience", "thing to do"]):
        return (
            "Check out [Experiences](/activities/) to browse activities by city, category, and budget.",
            [{"label": "Experiences", "url": "/activities/"}],
        )
    if any(w in msg for w in ["profile", "account", "settings"]):
        return (
            "Visit your [Profile](/accounts/profile/) to update your name, email, avatar, and preferences.",
            [{"label": "Profile", "url": "/accounts/profile/"}],
        )
    if any(w in msg for w in ["help", "what can you", "how do i", "what is"]):
        return (
            "I'm **Trave**, your Traveloop guide! I can help you create trips, explore cities, find activities, and manage packing, budget, and notes.",
            [
                {"label": "Create Trip", "url": "/trips/create/"},
                {"label": "Explore Cities", "url": "/cities/"},
                {"label": "Experiences", "url": "/activities/"},
            ],
        )

    return (
        "I'm here to help you plan your journey. Try asking about trips, cities, activities, budgets, packing, or notes.",
        [{"label": "My Trips", "url": "/trips/"}],
    )


# ─────────────────────────────────────────────────────────
#  2. Smart Suggestions endpoint
# ─────────────────────────────────────────────────────────

@login_required
def smart_suggestions_api(request, trip_id):
    """
    GET /api/ai/suggestions/<trip_id>/
    Returns smart city and activity suggestions based on the trip's current stops,
    budget, and existing activities — hybrid DB filtering + optional Gemini ranking.
    """
    try:
        trip = Trip.objects.get(pk=trip_id)
    except Trip.DoesNotExist:
        return JsonResponse({"error": "Trip not found"}, status=404)
    if trip.user_id != request.user.id:
        return JsonResponse({"error": "Forbidden"}, status=403)

    # ── Step 1: Gather trip context ──────────────────────────────────────────
    stops = TripStop.objects.filter(trip=trip).select_related("city").prefetch_related("trip_activities__activity")
    existing_city_ids = [s.city_id for s in stops if s.city_id]
    existing_activity_ids = []
    existing_categories = set()
    regions = set()
    total_budget = trip.total_budget or 0

    for stop in stops:
        if stop.city and stop.city.region:
            regions.add(stop.city.region)
        for ta in stop.trip_activities.all():
            existing_activity_ids.append(ta.activity_id)
            existing_categories.add(ta.activity.category)

    trip_duration = trip.duration_days if trip.start_date and trip.end_date else 7
    avg_daily_budget = total_budget / trip_duration if trip_duration > 0 else 100

    # ── Step 2: DB-driven city suggestions ──────────────────────────────────
    # Prioritize cities in the same region, not already in the trip, within budget
    city_qs = City.objects.exclude(id__in=existing_city_ids)
    if regions:
        # Mix: same region first, then others
        same_region_cities = list(
            city_qs.filter(region__in=regions)
            .filter(cost_index__lte=avg_daily_budget * Decimal('1.5'))
            .order_by("-popularity_score")[:6]
        )
        other_cities = list(
            city_qs.exclude(region__in=regions)
            .filter(cost_index__lte=avg_daily_budget * Decimal('1.5'))
            .order_by("-popularity_score")[:4]
        )
        suggested_cities = same_region_cities + other_cities
    else:
        suggested_cities = list(city_qs.order_by("-popularity_score")[:8])

    # ── Step 3: DB-driven activity suggestions ──────────────────────────────
    activity_qs = (
        Activity.objects.exclude(id__in=existing_activity_ids)
        .exclude(category__in=existing_categories)
        .select_related("city")
    )
    if existing_city_ids:
        # Prioritize activities in the cities already in the trip
        in_trip_activities = list(
            activity_qs.filter(city_id__in=existing_city_ids)
            .filter(cost__lte=avg_daily_budget)
            .order_by("-is_popular", "cost")[:8]
        )
        # Add varied-category suggestions
        other_activities = list(
            activity_qs.exclude(city_id__in=existing_city_ids)
            .filter(cost__lte=avg_daily_budget)
            .order_by("-is_popular", "cost")[:4]
        )
        suggested_activities = in_trip_activities + other_activities
    else:
        suggested_activities = list(
            activity_qs.filter(cost__lte=avg_daily_budget)
            .order_by("-is_popular", "cost")[:8]
        )

    # ── Step 4: Optional Gemini re-ranking of the selections ─────────────────
    ai_tip = "Start with one high-priority activity per day, then leave flexible time for meals, transit, and discoveries."
    model = _get_gemini_model()
    if model and stops.exists():
        try:
            city_names = ", ".join([s.city.name for s in stops if s.city])
            prompt = (
                f"A traveler is planning a trip. They are currently visiting: {city_names}. "
                f"Their trip lasts {trip_duration} days with a daily budget of approximately "
                f"${avg_daily_budget:.0f}. "
                f"Give ONE short, personalized travel tip (max 2 sentences) about what to do "
                f"or see in these cities. Be specific and enthusiastic. No markdown, plain text only."
            )
            response = model.generate_content(prompt)
            ai_tip = response.text.strip()
        except Exception as e:
            logger.error("Gemini suggestions error: %s", e)

    # ── Step 5: Serialize and return ─────────────────────────────────────────
    return JsonResponse({
        "cities": [
            {
                "id": c.id,
                "name": c.name,
                "country": c.country,
                "region": c.region,
                "cost_index": c.cost_index,
                "popularity_score": c.popularity_score,
                "url": f"/cities/{c.id}/",
            }
            for c in suggested_cities[:8]
        ],
        "activities": [
            {
                "id": a.id,
                "name": a.name,
                "city": a.city.name,
                "category": a.get_category_display(),
                "estimated_cost": float(a.cost),
                "duration_hours": round(a.duration_minutes / 60, 1),
                "is_popular": a.is_popular,
                "url": f"/activities/{a.id}/",
            }
            for a in suggested_activities[:8]
        ],
        "ai_tip": ai_tip,
        "context": {
            "trip_duration_days": trip_duration,
            "avg_daily_budget": round(avg_daily_budget, 2),
            "existing_cities": [{"id": c_id} for c_id in existing_city_ids],
        }
    })
