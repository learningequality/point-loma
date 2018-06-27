import logging
import shutil
import subprocess
import sys
import tempfile

from urllib.request import urlopen
from urllib.error import URLError

from utils import parse_cli_opts

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class PointLoma:
    def __init__(self):
        self.setup()
        self.run()
        self.clean()

    """
    Core methods
    """

    def setup(self):
        self.opts = parse_cli_opts()
        self.logger = logging.getLogger('pointloma')
        self.workdir = self._get_workdir()

    def run(self):
        url = self.opts.url

        if not self._check_url(url):
            self._log('error', 'No response from the url: {url}'.format(
                url=url))
            return

        for i in range(self.opts.runs):
            self._run_cmd(
                self._get_lighthouse_cmd(url))

    def clean(self):
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

    def _get_workdir(self):
        workdir = tempfile.mkdtemp()
        self._log('info', 'Created temporary directory: {dir}'.format(
            dir=workdir))
        return workdir

    def _remove_workdir(self):
        self._log('info', 'Deleting temporary directory: {dir}'.format(
            dir=self.workdir))
        shutil.rmtree(self.workdir)

    def _run_cmd(self, cmd):
        subprocess.Popen(cmd).wait()

    def _get_lighthouse_cmd(self, url):
        return ['lighthouse',
                url,
                '--output', 'json',
                '--output-path', '/tmp/pl',
                '--chrome-flags="--headless"']

    def _check_url(self, url):
        try:
            urlopen(url)
            return True
        except ValueError:
            return False  # URL not well formatted
        except URLError:
            return False  # URL doesn't seem to be reachable
