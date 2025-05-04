import requests
import random

WIKIDATA_URL = 'https://query.wikidata.org/sparql'
HEADERS = {'Accept': 'application/sparql-results+json'}

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
    response = requests.get(WIKIDATA_URL, params={'query': query}, headers=HEADERS)
    response.raise_for_status()  # Raises an error for bad HTTP status codes
    return response.json().get('results', {}).get('bindings', [])

def get_country_info(country_name, property_id):
    query = build_query(country_name, property_id)
    results = execute_sparql_query(query)
    if results:
        entry = results[0]
        return {
            'country': entry['countryLabel']['value'],
            'result': entry.get('valueLabel', {}).get('value', 'Unknown')
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
    return [item['countryLabel']['value'] for item in results]

# Main function that fetches correct and incorrect answers
def get_question_pair(target_country, question_type, country_list=None):
    property_id = info_type_mapping.get(question_type)
    if not property_id:
        return {'error': 'Unknown question type'}

    correct = get_country_info(target_country, property_id)
    if not correct:
        return {'error': 'Country not found'}

    if not country_list:
        country_list = get_random_country_list()

    # Ensure incorrect country is not the same as correct one
    incorrect_country = random.choice([c for c in country_list if c != target_country])
    incorrect = get_country_info(incorrect_country, property_id) or {'country': incorrect_country, 'result': 'Unknown'}

    return {
        'correct': {**correct, 'correct': True},
        'incorrect': {**incorrect, 'correct': False}
    }




