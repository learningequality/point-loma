import csv
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile

from datetime import datetime as dt

import utils


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class PointLoma:
    def __init__(self):
        """
        Simple flow based call order: Prepare to run -> Run -> Clean
        """
        self.prepare()
        self.run()
        self.clean()

    """
    Core methods
    """

    def prepare(self):
        """
        Prepares environment and information we will need to run the tests
        """
        self.opts = utils.parse_cli_opts()
        self.logger = logging.getLogger('pointloma')
        self.workdir = self._create_workdir()

    def run(self):
        """
        Runs the actual Lighthouse tests and extracts the results into the
        csv output file
        """
        url = self.opts.url
        runs = self.opts.runs
        output_path = self._get_output_path()

        # Check if we have a live URL
        if not utils.check_url(url):
            self._log('error', 'No response from url {url}'.format(url=url))
            return

        #  Run Lighthouse tests
        self._log('info', 'Running {runs} Lighthouse tests'.format(runs=runs))
        for r in range(runs):
            results_path = self._get_lighthouse_results_path(run=r)

            # Run Lighthouse tests
            self._log('info', 'Running test #{run}'.format(run=r + 1))
            cmd = self._get_lighthouse_cmd(url=url, results_path=results_path)
            self._run_cmd(cmd)

            # Extract results data
            self._log('info', 'Getting results for test #{run}'.format(run=r))
            write_header = self._should_write_header(run=r)
            self._extract_results(results_path=results_path,
                                  output_path=output_path,
                                  write_header=write_header)

    def clean(self):
        """
        Cleans and reverts and environment changes we might have done during
        the prepare stage
        """
        self._remove_workdir()

    """
    Helper methods
    """

    def _log(self, log_type, msg):
        """
        At the moment logs info messages only if verbose cli option is set
        Always logs error messages
        """
        if not log_type:
            raise ValueError('Log type is required')
        if log_type not in ['info', 'error']:
            raise ValueError('Log type not supported')

        msg = ' ' + msg

        if log_type == 'info' and self.opts.verbose:
            self.logger.info(msg)
        elif log_type == 'error':
            self.logger.error(msg)

    def _create_workdir(self):
        """
        Creates temporary directory to be used to gather the Lighthouse json
        result files before we extract the data from those to a single csv file
        """
        workdir = tempfile.mkdtemp()
        self._log('info', 'Created temp directory: {dir}'.format(dir=workdir))
        return workdir

    def _remove_workdir(self):
        """
        Removes the temporary directory created to gather json results files
        """
        self._log('info', 'Deleting temp directory: {dir}'.format(
            dir=self.workdir))
        shutil.rmtree(self.workdir)

    def _run_cmd(self, cmd):
        """
        Runs the specified subprocess command synchronously, i.e. waits for it
        to finish executing
        """
        subprocess.Popen(cmd).wait()

    def _get_lighthouse_cmd(self, url, results_path):
        """
        Returns list of command line arguments needed to run a Lighthouse test
        """
        return ['lighthouse',
                url,
                '--output', 'json',
                '--output-path', results_path,
                '--perf',
                '--chrome-flags="--headless"']

    def _get_lighthouse_results_path(self, run):
        """
        Returns the path to the location where the Lighthouse results json file
        should be saved.
        It is quite simple; based on the current run number and json extension
        """
        return os.path.join(self.workdir, '{run}.json'.format(run=run))

    def _get_output_path(self):
        """
        Returns the path to which should the final csv file be saved to
        If the path has been passed as a CLI option, will use that, otherwise
        save to the root of the pointloma codebase
        """
        if self.opts.output_path:
            return self.opts.output_path
        else:
            directory = 'output'
            if not os.path.exists(directory):
                os.makedirs(directory)

            ts = dt.now().strftime('%Y_%m_%d__%H_%M_%S__%f')
            filename = 'output_{ts}.csv'.format(ts=ts)

            return os.path.join(directory, filename)

    def _should_write_header(self, run):
        """
        Returns boolean on whether we should write header of the csv or not
        We should write header if:
            - the current run is the first run in the series
            - the output path has been passed via CLI, so user may want to
              append results to the same csv file
        """
        if run == 0:
            if not self.opts.output_path:
                return True
            else:
                try:
                    with open(self.opts.output_path, 'r') as csvfile:
                        sniffer = csv.Sniffer()
                        if not sniffer.has_header(csvfile.read(2048)):
                            return True
                except FileNotFoundError:
                    return True
        return False

    def _extract_results(self, results_path, output_path, write_header):
        """
        Extracts results from the json file generated with a single  Lighthouse
        test run and appends it to the csv file in output_path location
        """
        with open(results_path) as json_data:
            data = json.load(json_data)
            metrics = self._get_metrics_definitions()
            write_mode = 'w' if write_header else 'a'

            data_row = [data['generatedTime']] + \
                       [data['audits'][i['key']]['rawValue'] for i in metrics]

            with open(output_path, write_mode) as csvfile:
                writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                if write_header:
                    header_row = ['Timestamp'] + [i['header'] for i in metrics]
                    writer.writerow(header_row)
                writer.writerow(data_row)

    def _get_metrics_definitions(self):
        """
        Returns the list of dictionaries describing the audit metrics keys
        and their respective header labels
        Used to simplify metrics retrieval code and make it more easy to add
        new metrics in the future
        """
        return [
            {'key': 'first-meaningful-paint',
             'header': 'First Meaningful Paint'},
            {'key': 'first-interactive',
             'header': 'First Interactive'},
            {'key': 'consistently-interactive',
             'header': 'Consistently Interactive'},
            {'key': 'speed-index-metric',
             'header': 'Speed Index'},
            {'key': 'estimated-input-latency',
             'header': 'Estimated Input Latency'}]
