import click, sh
#from Naked.toolshed.shell import execute_js, muterun_js
#from parselighthouse import parselighthouse

import json, csv
# import os.path
from pathlib import Path

@click.command()
#@click.option('--headless', '-hl', default=True, is_flag=True, 
#		help='Run in headless mode')
@click.option('--count', default=1, help='Number of tests to run')
@click.option('--output-file', default='output', help='Name of output file with extension')
#@click.option('--overwrite', is_flag=True, help='Replace file if it already exists')
@click.argument('link')

def cli(link, count, output_file):
	"""This script runs Lighthouse using the command line interface."""
	output = 'output.csv'

	click.echo("******** Start Point Loma ********")
	click.echo("Running lighthouse on '{0}'".format(link))
	
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
	fmp_avg = 0
	si_avg = 0
	eil_avg = 0
	tti_avg = 0

	for x in range(count):
		y = x+1
		click.echo("Running Test #{0}...".format(x+1))
		
		filename = "./results{0}.json".format(y)
		sh.lighthouse(link, "--output", "json", "--output-path", filename)

	# click.echo("******** Finish Point Loma ********")

	#for x in range(count):
	#	y = x + 1
	#	filename = "./results{0}.json".format(y)

		with open(filename) as json_data:
			d = json.load(json_data)

			timestamp = d["generatedTime"]
			firstMeaningfulPaint = d["audits"]["first-meaningful-paint"]["rawValue"]
			speedIndex = d["audits"]["speed-index-metric"]["rawValue"]
			estimatedInputLatency = d["audits"]["estimated-input-latency"]["rawValue"]
			timeToInteractive = d["audits"]["time-to-interactive"]["rawValue"]

			fmp_avg = fmp_avg + firstMeaningfulPaint
			si_avg = si_avg + speedIndex
			eil_avg = eil_avg + estimatedInputLatency
			tti_avg = tti_avg + timeToInteractive

			header = ["********* Test {0} *********".format(y), ""]
			data1 =	["Timestamp", timestamp]
			data2 =	["First Meaningful Paint", firstMeaningfulPaint]
			data3 =	["Speed Index", speedIndex]
			data4 =	["Estimated Input Latency", estimatedInputLatency]
			data5 =	["Time to Interactive", timeToInteractive]
			newLine = ["", ""]

			# if output file is specified, set it
			if output_file != output:
				output = output_file

			read_mode = 'w'
			# outputPath = Path(output)
			# if outputPath.is_file():
			# 	read_mode = 'a'
			# else:
			# 	read_mode = 'w'

			# if overwrite:
			# 	read_mode = 'w'
			# else:
			# 	if outputPath.is_file():
			# 		read_mode = 'a'
			# 	else:
			# 		read_mode = 'w'

			with open(output, read_mode) as csvfile:
				wr = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
				
				wr.writerow(header)
				wr.writerow(data1)
				wr.writerow(data2)
				wr.writerow(data3)
				wr.writerow(data4)
				wr.writerow(data5)
				wr.writerow(newLine)

	read_mode = 'a'

	with open(output, read_mode) as csvfile:
		wr = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
		
		fmp_avg = fmp_avg/count
		si_avg = si_avg/count
		eil_avg = eil_avg/count
		tti_avg = tti_avg/count

		header = ["********* Average {0} Tests *********".format(y), ""]
		#data1 =	["Timestamp", timestamp]
		data2 =	["First Meaningful Paint", fmp_avg]
		data3 =	["Speed Index", si_avg]
		data4 =	["Estimated Input Latency", eil_avg]
		data5 =	["Time to Interactive", tti_avg]
		newLine = ["", ""]

		wr.writerow(header)
		#wr.writerow(data1)
		wr.writerow(data2)
		wr.writerow(data3)
		wr.writerow(data4)
		wr.writerow(data5)
		wr.writerow(newLine)

	click.echo("******** Finish Point Loma ********")