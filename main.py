from Occupations import run_roles, jsons_jobs
from process_data import first_graph, second_graph
from run import start
from top_10_code import run_top_5, sort_top

if __name__ == '__main__':
    # collect data
    start()
    run_roles()
    jsons_jobs()

    # process data
    first_graph()
    second_graph()

    # top 5 code
    run_top_5()
    sort_top()
