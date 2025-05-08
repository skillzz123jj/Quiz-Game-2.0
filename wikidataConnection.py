import requests
import random

WIKIDATA_URL = 'https://query.wikidata.org/sparql'
HEADERS = {
    'Accept': 'application/sparql-results+json',
    'User-Agent': 'QuizGame/1.0 (myemail@example.com)'
}

info_type_mapping = {
    'P1082': 'What is the population?',
    'P36': 'What is the capital?',
    'P38': 'What is the currency?',
    'P37': 'What is the official language?',
    'P1056': 'What is the national animal?',
    'P1451': 'What is the national anthem?',

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



def get_country_info(country_name, question_id):
    query = build_query(country_name, question_id)
    results = execute_sparql_query(query)

    if results:
        entry = results[0]
        country = entry.get('countryLabel', {}).get('value')
        result = entry.get('valueLabel', {}).get('value', 'Unknown')
        question = info_type_mapping[question_id]

        if country:
            return {
                'country': country,
                'result': result,
                'question': question,
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

def get_question_pair(target_country):
    max_question_attempts = 5  # prevent infinite loops
    for _ in range(max_question_attempts):
        question_id = random.choice(list(info_type_mapping.keys()))
        correct = get_country_info(target_country, question_id)
        if not correct:
            continue  # try another question if data isn't found

        country_list = get_random_country_list()
        if not country_list or len(country_list) < 2:
            return {'error': 'Not enough countries to generate incorrect answer'}

        other_countries = [c for c in country_list if c != target_country]
        if not other_countries:
            return {'error': 'No other countries available for comparison'}

        max_incorrect_attempts = 10
        attempts = 0
        incorrect = None

        while attempts < max_incorrect_attempts:
            incorrect_country = random.choice(other_countries)
            data = get_country_info(incorrect_country, question_id)
            if data and data['result'] != 'Unknown' and data['result'] != correct['result']:
                incorrect = {**data, 'correct': False}
                break
            attempts += 1

        if incorrect:
            return {
                'question': correct['question'],
                'correct': {**correct, 'correct': True},
                'incorrect': incorrect
            }

    return {'error': 'Failed to generate distinct answers after multiple attempts'}





