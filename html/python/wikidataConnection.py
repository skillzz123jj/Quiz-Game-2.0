import requests

#Creates the question for Wikidata-database
def build_query(country_name, info_type):
    base = f"""
    SELECT ?country ?countryLabel ?value
    WHERE {{
      ?country rdfs:label "{country_name}"@en.
      ?country wdt:P31 wd:Q6256.
      OPTIONAL {{
        ?country wdt:{info_type} ?value.
      }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT 1
    """
    return base

info_type_mapping = {
    'population': 'P1082',
    'area': 'P2046',
    'capital': 'P36',
    'currency': 'P38',
    'official_language': 'P37'
}

def get_country_info(country_name, question_type):
    property_id = info_type_mapping.get(question_type)
    if not property_id:
        return {'error': 'Unknown question type'}

    query = build_query(country_name, property_id)
    url = 'https://query.wikidata.org/sparql'
    headers = {'Accept': 'application/sparql-results+json'}
    response = requests.get(url, params={'query': query}, headers=headers)
    data = response.json()
    results = data['results']['bindings']

    if results:
        country_info = results[0]
        label = country_info['countryLabel']['value']
        value = country_info.get('value', {}).get('value', 'Unknown')
        return {'country': label, 'result': value, 'correct': True}
    else:
        return {'error': 'Country not found'}




