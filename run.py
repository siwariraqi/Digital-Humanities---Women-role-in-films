import time
import requests
import json


def start():
    years = ['19801990', '19912000', '20012006', '20072010', '20112014', '20152018', '20192022']
    for year in years:
        json_dict = {}
        movies = []
        for i in range(0, 2):
            query = 'https://imdb-api.com/API/AdvancedSearch/k_sej8mhp2?title_type=feature,tv_movie,short,tv_short&release_date=%s-01-01,%s-12-31&countries=us&languages=en&count=250&start=%d' % (
                year[0:4], year[4:8], i)
            response = requests.get(query)
            response_json = response.json()
            movies.append(response_json['results'])
        flat_movies = [movie for sublist in movies for movie in sublist]

        filtered_movies = []
        for_now = []
        movies_type = []
        for movie in flat_movies:
            movie_type = movie['genreList']
            for x in movie_type:
                if x['key'] not in for_now:
                    for_now.append(x['key'])
                    movies_type.append({'type': x['key'], 'males_number': 0, 'women_number': 0})
            response = requests.get(
                'https://api.themoviedb.org/3/movie/%s/credits?api_key=87eb3c17f3d088bc8b3a5ccb6fb36c2b' % movie['id'])
            response_json = response.json()
            if not response.ok:
                break
            cast = response_json['cast']
            members = []
            for member in cast:
                if member is None:
                    continue
                if (not ('known_for_department' in member.keys())) or member['known_for_department'] != 'Acting':
                    gender = None
                else:
                    gender = member['gender']
                if gender is None:
                    continue
                if gender == 2:
                    for typ in movie_type:
                        for t in movies_type:
                            if typ['key'] == t['type']:
                                t['males_number'] = t['males_number'] + 1
                                continue
                if gender == 1:
                    for typ in movie_type:
                        for t in movies_type:
                            if typ['key'] == t['type']:
                                t['women_number'] = t['women_number'] + 1
                    members.append({'name': member['name'], 'character': member['character']})
            filtered_movies.append({'id': movie['id'],
                                    'title': movie['title'],
                                    'release_year': movie['description'][1:-1],
                                    'plot': movie['plot'], 'members': members,
                                    'cast_total_number': len(cast)})
        json_dict.update({year: filtered_movies, 'movies_type': movies_type})
        path = './{}.json'.format(year)
        with open(path, 'w') as outfile:
            json.dump(json_dict, outfile, indent=4)
