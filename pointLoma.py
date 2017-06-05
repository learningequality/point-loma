import click, sh
#from Naked.toolshed.shell import execute_js, muterun_js

@click.command()
@click.option('--headless', '-hl', multiple=True, default=True, is_flag=True, 
		help='Run in headless mode')
@click.argument('link')

def cli(link, headless):
	"""This script runs Lighthouse using the command line interface."""
	click.echo("Runing lighthouse on {0}".format(link))
	if headless:
		sh.lighthouse(link, "--output-path", "./myfile.json", "output", "html", "--chrome-flags=", "--headless")
	else:
		sh.lighthouse(link, "--output-path", "./myfile.json", "output", "html")
