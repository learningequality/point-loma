import click, sh
#from Naked.toolshed.shell import execute_js, muterun_js
#from parselighthouse import parseLighthouse

@click.command()
#@click.option('--headless', '-hl', default=True, is_flag=True, 
#		help='Run in headless mode')
#@click.option('--verbose', is_flag=True, help='Verbose logging')
@click.option('--count', default=1, help='Number of tests to run')
@click.argument('link')

def cli(link, count):
	"""This script runs Lighthouse using the command line interface."""
	click.echo("Running lighthouse on '{0}' ...".format(link))
	
	#chromeHeadless = sh.Command("/Applications/Google\ Chrome\ Canary.app/Contents/MacOS/Google\ Chrome\ Canary")
	#chromeHeadless("--headless", "--remote-debugging-port=9222", "--disable-gpu")

	# if headless:
	# 	sh.lighthouse(link, "--output-path", "./myfile.json", "output", "html", "--chrome-flags=", "--headless")
	# else:
	# 	if verbose:
	# 		sh.lighthouse(link, "--output-path", "./myfile.json", "output", "json", "--verbose")
	# 	else:
	# 		sh.lighthouse(link,  "--output", "json", "--output", "html")

	#sh.lighthouse(link,  "--output", "json", "--output-path=", "./results.json")
	for x in range(count):
		y = x+1
		click.echo("Test #{0}...".format(x+1))
		
		filename = "./results{0}.json".format(y)
		sh.lighthouse(link, "--output", "json", "--output-path", filename)
