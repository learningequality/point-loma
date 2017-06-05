# version 0.2

import json, csv
# import os.path
from pathlib import Path

#def parseLighthouse():
count = 3
for x in range(count):
	y = x + 1
	filename = "./results{0}.json".format(y)

	with open(filename) as json_data:
		d = json.load(json_data)

		timestamp = d["generatedTime"]
		firstMeaningfulPaint = d["audits"]["first-meaningful-paint"]["rawValue"]
		speedIndex = d["audits"]["speed-index-metric"]["rawValue"]
		estimatedInputLatency = d["audits"]["estimated-input-latency"]["rawValue"]
		timeToInteractive = d["audits"]["time-to-interactive"]["rawValue"]

		header = ["********* Test {0} *********".format(y), ""]
		data1 =	["Timestamp", timestamp]
		data2 =	["First Meaningful Paint", firstMeaningfulPaint]
		data3 =	["Speed Index", speedIndex]
		data4 =	["Estimated Input Latency", estimatedInputLatency]
		data5 =	["Time to Interactive", timeToInteractive]
		#footer = ["***************************", ""]
		newLine = ["", ""]

		#output = "./output{0}.csv".format(y)
		output = Path("output.csv")
		if output.is_file():
			read_mode = 'a'
		else:
			read_mode = 'w'

		with open("output.csv", read_mode) as csvfile:
			wr = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
			
			wr.writerow(header)
			wr.writerow(data1)
			wr.writerow(data2)
			wr.writerow(data3)
			wr.writerow(data4)
			wr.writerow(data5)
			#wr.writerow(footer)
			wr.writerow(newLine)