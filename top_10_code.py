from operator import itemgetter

import imdb
from SPARQLWrapper import SPARQLWrapper, JSON
import json


def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.queryAndConvert()


def get_actors_per_country():
    endpoint_url = "https://query.wikidata.org/sparql"
    query = """
            SELECT ?personLabel ?genderLabel
            WHERE
            {
                   ?person wdt:P31 wd:Q5 .
                   ?person wdt:P106 wd:Q33999 .
                   ?person wdt:P27 wd:Q30 .
                   ?person wdt:P21 ?gender .

                   SERVICE wikibase:label {bd:serviceParam wikibase:language "en" }
            }
    """

    actors_and_gender = []
    results = get_results(endpoint_url, query)
    for result in results["results"]["bindings"]:
        if not result["personLabel"]["value"][1:].isnumeric():
            actors_and_gender.append([result["personLabel"]["value"], result["genderLabel"]["value"]])
    return actors_and_gender


json_dict = []
imdbDB = imdb.IMDb()  # get instance of the class


def helper(female):
    search = imdbDB.search_person(female[0])
    splitted_name = female[0].split(" ")
    if len(splitted_name) != 2:
        return
    for t in search:
        if t.data['name'].lower() == "{last_name}, {first_name}".format(last_name=female[0].split(" ")[1].lower(),
                                                                        first_name=female[0].split(" ")[0].lower()):
            req = t.personID
            try:
                full_person = imdbDB.get_person(req, info=["filmography"])
            except:
                full_person = None
            if full_person is not None:
                try:
                    if "actress" in full_person["filmography"].keys() and len(full_person["actress"]) > 40:
                        json_dict.append({"actress": female[0], 'movies': len(full_person["actress"])})
                except:
                    break
            break


def run_top_5():
    data = get_actors_per_country()
    females = []
    for d in data:
        if d[1] == 'female':
            females.append(d)
    for female in females:
        helper(female)
        print(json_dict)
    with open('top_10/top_10.json', 'w') as outfile:
        json.dump(json_dict, outfile, indent=4)


def sort_top():
    with open("top_10/top_10.json") as json_file:
        actress = json.load(json_file)
    sorte = sorted(actress, key=itemgetter('movies'), reverse=True)
    with open('top_10/top_10_sorted.json', 'w') as outfile:
        json.dump(sorte, outfile, indent=4)

