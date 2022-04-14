import argparse


def get_cmd_arguments():
    """
    Convert command line argument strings to objects and assign them as attributes of the namespace
    Returns:  the populated namespace
    """
    parser = argparse.ArgumentParser(allow_abbrev=True)

    parser.add_argument('--filepath', '-fp',
                        type=str, required=True, dest='file_path',
                        help="path to the .tsv metadata file")

    parser.add_argument('--filetype', '-ft',
                        type=str.lower, default="gisaid", choices=['gisaid', 'nextstrain'], dest='file_type',
                        help="type of the .tsv metadata file. Currently supported: gisaid or nextstrain")

    parser.add_argument('--countries', '--locations', '-loc',
                        type=custom_list, default="all", dest='filtered_countries',
                        help='''comma separated list of country names whose sequence data is to be imported 
                                in the tool. Use \"all\" to import the entire dataset''')

    parser.add_argument('--startdate', '-sd', '-s',
                        type=str.lower, default="beginning", dest='beginning_date',
                        help="start date to be considered when importing data. Use the format YYYY-mm-dd")

    parser.add_argument('--enddate', '-ed', '-e',
                        type=str.lower, default="end", dest='end_date',
                        help="end date to be considered when importing data. Use the format YYYY-mm-dd")

    parser.add_argument('--reload', '-r',
                        default=False, action='store_true', dest='reload',
                        help="boolean flag to overwrite the current database, if present")

    args = parser.parse_args()
    print(args)
    return args


def custom_list(str_list):
    """
    Converts a set of comma separated values into a set.
    If only one element is found and the element is 'all' then it returns and empty set
    Args:
        str_list:   string representing the set

    Returns:    a set that is the result of the conversion

    """
    values_set = set([x.lower().strip() for x in str_list.split(',') if x])
    if len(values_set) == 1 and 'all' in values_set:
        values_set.clear()
    return values_set
