import requests
import json

url = "https://json.freeastrologyapi.com/planets"
headers = {
        'Content-Type': 'application/json',
        'x-api-key': 'e1KIctvC5C8f5OjgqTcNK1445DPIP0YWaDtbTSnQ'
    }

# Helper Functions
def compute_planetary_score(planet_data):
    """Compute a score for a single planet based on position, retrograde, and sign."""
    score = 0

    # Base score based on sign placement
    sign = planet_data["current_sign"]
    retrograde = planet_data["isRetro"] == "true"
    norm_degree = planet_data["normDegree"]

    if retrograde:
        score -= 10  # Penalty for retrograde
    if sign in [1, 4, 7, 10]:  # Angular houses (Kendra)
        score += 20
    elif sign in [5, 9]:  # Trine houses (Trikona)
        score += 15
    elif sign in [6, 8, 12]:  # Challenging houses
        score -= 5

    # Degree-based modifiers (e.g., near Gandanta zones)
    if 27 < norm_degree <= 30 or 0 <= norm_degree < 3:
        score -= 5

    return score


def compute_parameter_scores(planets):
    """Compute scores for different life parameters."""
    mood_score = 0
    work_score = 0
    relationship_score = 0

    for planet in planets.values():
        if planet["name"] == "Moon":
            mood_score += compute_planetary_score(planet)
        elif planet["name"] in ["Sun", "Mars", "Saturn"]:
            work_score += compute_planetary_score(planet)
        elif planet["name"] in ["Venus", "Mercury"]:
            relationship_score += compute_planetary_score(planet)

    # Normalize scores to percentages
    mood_score = max(0, min(100, mood_score + 50))
    work_score = max(0, min(100, work_score + 50))
    relationship_score = max(0, min(100, relationship_score + 50))

    return {
        "Mood and Energy": mood_score,
        "Work and Career": work_score,
        "Relationships": relationship_score,
    }

def calculate_dashboard(payload):
    """Main function to parse the input payload and generate scores."""

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    data = response.json()
    json_data = {
    "output": [
        {
            key: {
                "name": value.get("name", "Unknown"),
                "current_sign": value.get("current_sign", "N/A"),
                "normDegree": round(value.get("normDegree", 0), 2),
                "isRetro": value.get("isRetro", "false")
            }
            for key, value in data["output"][0].items()  # Use data instead of response here
            if key.isdigit()
        }
    ]
}
    planets = {k: v for k, v in json_data["output"][0].items() if isinstance(v, dict) and "name" in v}

    # Compute scores
    scores = compute_parameter_scores(planets)
    return scores


