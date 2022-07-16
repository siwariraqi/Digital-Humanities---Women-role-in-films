import json
import numpy as np
from SPARQLWrapper import SPARQLWrapper, JSON
import wikipedia

array_of_years = ["19801990", "19912000", "20012006", "20072010", "20112014", "20152018", "20192022"]
careers_and_roles = []


def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def all_roles():
    endpoint_url = "https://query.wikidata.org/sparql"

    query = """SELECT DISTINCT ?occLabel WHERE {
      ?occ wdt:P31 wd:Q28640.
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }

    """
    results = get_results(endpoint_url, query)

    for result in results["results"]["bindings"]:
        careers_and_roles.append(result["occLabel"]["value"])
    careers_and_roles.sort()
    careers_and_roles.sort(reverse=True, key=len)


def search_for_roles(name, plot):
    check = False
    if plot:
        chars = [s.lower().replace(',', '').split(' ') for s in plot.split('.') if
                 any(w in s for w in [name])]
    if chars:
        for job in careers_and_roles:
            for i in range(len(chars[0]) - len(job.split(' ')) + 1):
                if job.split(' ') == chars[0][i:i + len(job.split(' '))]:
                    check = True
                    break
            if check:
                occupation = job
                break
    if occupation:
        return occupation
    check2 = False
    for job in careers_and_roles:
        for i in range(len(name.lower().split(' ')) - len(job.lower().split(' ')) + 1):
            if job.lower().split(' ') == name.lower().split(' ')[i:i + len(job.lower().split(' '))]:
                check2 = True
                break
        if check2:
            occupation = job
            break
    return occupation


def get_plot(film_name):
    plot = np.NaN
    plot_options = ['Plot', 'Synopsis', 'Plot synopsis', 'Plot summary',
                    'Story', 'Plotline', 'The Beginning', 'Summary',
                    'Content', 'Premise', 'PlotEdit', 'SynopsisEdit', 'Plot synopsisEdit', 'Plot summaryEdit',
                    'StoryEdit', 'PlotlineEdit', 'The BeginningEdit', 'SummaryEdit',
                    'ContentEdit', 'PremiseEdit']
    try:
        wikipage = wikipedia.WikipediaPage(film_name)
    except:
        wikipage = np.NaN
    try:
        for j in plot_options:
            if wikipage.section(j) is not None:
                plot = wikipage.section(j).replace('\n', '').replace("\'", "")
    except:
        plot = np.NaN
    return plot


def run_roles():
    all_roles()
    all_movies = {}
    for years in array_of_years:
        path = './{}.json'.format(years)
        with open(path) as json_file:
            all_movies[years] = json.load(json_file)
    for years in all_movies:
        jobs_of_characters = {}
        for movie in all_movies[years][years]:
            plot = get_plot(movie['title'])
            if plot is np.NAN:
                plot = movie["plot"]
            for actor in movie['members']:
                if actor['character']:
                    occupation = search_for_roles(actor["character"], plot)
                    if occupation:
                        actor['occupation'] = occupation
                        if occupation in jobs_of_characters.keys():
                            jobs_of_characters[occupation]['numOfCharacters'] += 1
                            jobs_of_characters[occupation]['characters'].extend(
                                [{'movie name': movie['title'], 'actor name': actor["name"],
                                  'character name': actor["character"]}])
                        else:
                            jobs_of_characters.update({occupation: {'numOfCharacters': 1, 'characters': [
                                {'movie name': movie['title'], 'actor name': actor["name"],
                                 'character name': actor["character"]}]}})

        open("./Jobs" + years + ".json", "w").write(
            json.dumps(jobs_of_characters, indent=4))


def extended(dic, job, to_update):
    dic['title'] = job
    dic.update(to_update)
    return dic


def jsons_jobs():
    job_files = {}
    for years in array_of_years:
        path = "./occupationsByJob" + years + ".json"
        with open(path) as json_file:
            job_files[years] = json.load(json_file)
    merged = {}
    for year in job_files:
        new_file = []
        for job in job_files[year]:
            if job in merged.keys():
                merged[job]['numOfCharacters'] += job_files[year][job]['numOfCharacters']
                merged[job]['characters'].extend(job_files[year][job]['characters'])
            else:
                merged[job] = {}
                merged[job]['title'] = job
                merged[job].update(job_files[year][job])
            new_file.extend([extended({}, job, job_files[year][job])])
            path = "./occupationsByJob/Jobs" + year + "final.json"
            open(path, "w").write(json.dumps(new_file, indent=4))

    final = []
    for job in merged.values():
        final.extend([job])
    open("./occupationsByJob/final.json", "w").write(json.dumps(final, indent=4))
