import json

years = ['19801990', '19912000', '20012006', '20072010', '20112014', '20152018', '20192022']


def first_graph():
    first_graph_data = []
    for year in years:
        women = 0
        total_cast = 0
        with open("./not_relevant/{}.json".format(year), 'r') as json_file:
            movies_per_year = json.load(json_file)
        all_movies = movies_per_year[year]
        for movie in all_movies:
            women += len(movie['members'])
            total_cast += movie['cast_total_number']
        first_graph_data.append({"year": year, "women": women, "total_cast": total_cast})
    with open('./final_graphs/first_graph_data.json', 'w') as outfile:
        json.dump(first_graph_data, outfile, indent=4)


def second_graph():
    types = []  # {{"movie_type":"action", "males":number,"females":number}}
    for_now = []
    for year in years:
        with open("./{}.json".format(year), 'r') as json_file:
            movies_per_year = json.load(json_file)
        movies_type = movies_per_year["movies_type"]
        for item in types:
            if item['movie_type'] not in for_now:
                for_now.append(item['movie_type'])
        for t in movies_type:
            if t['type'] not in for_now:
                types.append({"movie_type": t['type'], "males": t['males_number'], "females": t['women_number']})
                for_now.append( t['type'])
            else:
                for item in types:
                    if item['movie_type'].lower() == t['type'].lower():
                        item['males'] += t['males_number']
                        item['females'] += t['women_number']

    with open('./final_graphs/second_graph_data_new.json', 'w') as outfile:
        json.dump(types, outfile, indent=4)