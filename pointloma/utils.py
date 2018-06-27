import argparse


def parse_cli_opts():
    description = 'PointLoma - A Python library to execute Lighthouse and ' \
                  'export the results of running performance tests against ' \
                  'different Kolibri URLs'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('url', help='Url to test against')
    parser.add_argument('-hl', '--headless', help='Run in headless mode',
                        required=False, default=True)
    parser.add_argument('-r', '--runs', help='Number of test runs',
                        required=False, default=1, type=int)
    parser.add_argument('--output-path', help='Output csv file',
                        required=False)
    parser.add_argument('-v', '--verbose', help='Increase output verbosity',
                        action='store_true')
    return parser.parse_args()
