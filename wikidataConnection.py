import requests
import random

WIKIDATA_URL = 'https://query.wikidata.org/sparql'
HEADERS = {
    'Accept': 'application/sparql-results+json',
    'User-Agent': 'QuizGameBot/1.0 (your.email@example.com)'
}

info_type_mapping = {
    'population': 'P1082',
    'area': 'P2046',
    'capital': 'P36',
    'currency': 'P38',
    'official_language': 'P37'
}

def build_query(country_name, property_id):
    return f"""
    SELECT ?country ?countryLabel ?value ?valueLabel
    WHERE {{
      ?country rdfs:label "{country_name}"@en.
      ?country wdt:P31 wd:Q6256.
      OPTIONAL {{
        ?country wdt:{property_id} ?value.
        ?value rdfs:label ?valueLabel.
        FILTER (lang(?valueLabel) = "en")
      }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT 1
    """

def execute_sparql_query(query):
    try:
        response = requests.get(WIKIDATA_URL, params={'query': query}, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        bindings = data.get('results', {}).get('bindings', [])
        if not bindings:
            print("[WARN] SPARQL returned no results")
        return bindings
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] SPARQL request failed: {e}")
        return []



def get_country_info(country_name, property_id):
    query = build_query(country_name, property_id)
    results = execute_sparql_query(query)

    if results:
        entry = results[0]
        country = entry.get('countryLabel', {}).get('value')
        result = entry.get('valueLabel', {}).get('value', 'Unknown')

        if country:
            return {
                'country': country,
                'result': result
            }

    return None


def get_random_country_list(limit=500):
    query = f"""
    SELECT ?countryLabel WHERE {{
      ?country wdt:P31 wd:Q6256.
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT {limit}
    """
    results = execute_sparql_query(query)
    return [item['countryLabel']['value'] for item in results if 'countryLabel' in item]

def get_question_pair(target_country, question_type, country_list=None):
    property_id = info_type_mapping.get(question_type)
    if not property_id:
        return {'error': 'Unknown question type'}

    correct = get_country_info(target_country, property_id)
    if not correct:
        return {'error': f'No data found for {target_country}'}

    if not country_list:
        country_list = get_random_country_list()

    if not country_list or len(country_list) < 2:
        return {'error': 'Not enough countries to generate incorrect answer'}

    other_countries = [c for c in country_list if c != target_country]
    if not other_countries:
        return {'error': 'No other countries available for comparison'}

    max_attempts = 10
    attempts = 0
    incorrect = None

    while attempts < max_attempts:
        incorrect_country = random.choice(other_countries)
        data = get_country_info(incorrect_country, property_id)
        if data and data['result'] != 'Unknown':
            incorrect = {**data, 'correct': False}
            break
        attempts += 1

    if not incorrect:
        incorrect = {'country': incorrect_country, 'result': 'Unknown', 'correct': False}

    return {
        'correct': {**correct, 'correct': True},
        'incorrect': incorrect
    }




