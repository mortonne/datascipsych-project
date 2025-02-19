from pkg_resources import resource_filename


def get_data_file():
    data_file = resource_filename("project", "data/exp1.csv")
