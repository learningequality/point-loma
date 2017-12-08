
import click, sh
import os
import sys
import json, csv
from pathlib import Path
import numbers
import subprocess
from distutils.dir_util import copy_tree
import shutil 
import time
import signal

#0.3.0 and 0.6.0
versionNumbers = ["0.3.1", "0.3.2", "0.4.0", "0.4.1", "0.4.2", "0.4.3", 
	"0.4.4", "0.4.5", "0.4.6", "0.4.7", "0.4.8", "0.4.9", "0.5.0",
	"0.5.1", "0.5.2", "0.5.3"]


#point-loma directory
pointlomaDir = os.path.dirname(os.path.abspath(__file__))

firstLoop = 1


def run_tests(link, headless, count, output_file, created, versionName):
	os.chdir(pointlomaDir) 
	testNum = 1
	"""This script runs Lighthouse using the command line interface."""
	output = 'output'

	click.echo("******** Start Point Loma ********")

	#Check if the cvs already exist
	outputPath = Path(output_file+'.csv')
	if outputPath.is_file() and not created:
		if output_file != output:
			confirmMessage = 'File {0} already exists. Proceeding will overwrite existing file. \nContinue?'.format(output_file+'.csv')
		else:
			confirmMessage = 'Default file already exists. Proceeding will overwrite existing file. \nContinue?'
		
		if (click.confirm(confirmMessage)) == False:
			click.echo("******** Quitting Point Loma ********")
			return;

	click.echo("Running lighthouse on '{0}'".format(link))

	fmp_avg = 0
	si_avg = 0
	eil_avg = 0
	fi_avg = 0
	ci_avg = 0
	
	#Runs the number times the user specified or default is 1 
	for numIteration in range(count):
		y = numIteration+1
		click.echo("---Test #{0}---".format(y))
		click.echo("Running lighthouse...")

		filename = "./results{0}.json".format(y)
		sh.lighthouse(link, "--output", "json", "--output-path", filename, '--chrome-flags="--headless"')

		click.echo("Exporting results for test {0} to csv file...".format(y))

		with open(filename) as json_data:
			d = json.load(json_data)

			# extract data from json files
			timestamp = d["generatedTime"]
			firstMeaningfulPaint = d["audits"]["first-meaningful-paint"]["rawValue"]
			firstInteractive = d["audits"]["first-interactive"]["rawValue"]
			consistentlyInteractive = d["audits"]["consistently-interactive"]["rawValue"]
			speedIndex = d["audits"]["speed-index-metric"]["rawValue"]
			estimatedInputLatency = d["audits"]["estimated-input-latency"]["rawValue"]
			

			# rows hardcoded for now
			if count == 1:
				header = ["********* Test {0} *********".format(y), "{0}".format(link)]
			else:
				header = ["********* Test {0} *********".format(y), ""]

			dataRow =	[timestamp,firstMeaningfulPaint, firstInteractive, consistentlyInteractive, speedIndex, estimatedInputLatency, versionName]
			newLine = [""]

			# if output file is specified, set it
			if output_file != output:
				output = output_file

			# convert to csv file
			output = output + '.csv'

			print("output: " + output)
			print numIteration
			# default is to overwrite existing files
			if numIteration == 0:
				read_mode = 'w'
			else:
				read_mode = 'a'
			
			headerRow = ["Timestamp", "First Meaningful Paint", "First Interactive", "Consistently Interactive", "Speed Index","Estimated Input Latency", "Version"]
			
			if not created:
				# add data to csv file
				with open(output, read_mode) as csvfile:
					wr = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
					if numIteration == 0:
						wr.writerow(headerRow)
					wr.writerow(dataRow)
					testNum = testNum+1
			else:
				with open(output, 'a') as csvfile:
					wr = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
					wr.writerow(dataRow)
					testNum = testNum+1


@click.command()
@click.option('--headless', '-hl', default=True, is_flag=True, help='Run in headless mode')
@click.option('--count', default=1, help='Number of tests to run. Default is 1.')
@click.option('--output-file', default='output', help='Name of csv file w/o extension. Default is "output".')
#@click.option('--html', default=False, is_flag=True, help='Generate full HTML reports')
@click.argument('link')
def cli(link, headless, count, output_file): #, versionNumber=None): #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	#print("THIS IS TO SEE IF IT enters", len(versionNumbers))
	global firstLoop
	for versionName in versionNumbers:
		print("THIS IS VERSION", versionName)
		#Get the directory of the right version of .kolibri 
		kolibriHome = os.path.join(
			os.path.dirname(__file__), 'kolibri-versions/',
			'kolibri-v.{version}/'.format(version=versionName),
			'.kolibri'
		)
		#Sets the location as the home directory
		os.environ["KOLIBRI_HOME"] = kolibriHome
		#Change to pex file folder
		os.chdir(os.path.join(pointlomaDir, 'kolibri-pex')) 
		file = 'kolibri-v{version}.pex'.format(version=versionName)
		#Run the pex file
		#sh.python(file, "start", "--foreground")
		commandPex = "python kolibri-v{version}.pex start --foreground".format(version=versionName)
		end = subprocess.Popen(commandPex, shell=True)
		time.sleep(5)
		#cli(versionNumber=versionName) 
		print('callling test function')
		if firstLoop == 1:
			run_tests(link, headless, count, output_file, False, versionName)
			firstLoop+=1
		else:
			run_tests(link, headless, count, output_file, True, versionName)
			firstLoop+=1
		end.terminate()
		click.echo("******** Finish Point Loma ********")

	return


if __name__ == '__main__':
    cli()

