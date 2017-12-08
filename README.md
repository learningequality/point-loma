# Point Loma
*A Python script to execute Lighthouse and export results of running performance tests against different URLs on different releases.Aims to track code quality and improve user experience.*

**December 8, 2017**

## Requirements
- sh (Python package)
- click (Python package)
- pathlib (Python package)
- lighthouse (Node package) 
- shutil (Python packaage)
  *Lighthouse requires Node 6 or later.*
- Google Chrome
- Chrome Canary (Only needed for headless)

**Installation:**  
- Use `git clone` or download the project as a zip from this Github page. There are two file main files inside:  
	- *setup.py*: used to install the three Python dependencies  
	- *pointLoma.py*: the main script file, executes lighthouse and exports  results  
- Install **lighthouse** using the following command:  
```
    npm install -g lighthouse
    # or use yarn:
    yarn global add lighthouse
```  
   *Note:* lighthouse requires Node 6 or later. Install the current [Long-Term Support](https://github.com/nodejs/LTS) version of [Node](https://nodejs.org/).  
- Google Chrome
	Link: https://www.google.com/chrome/browser/desktop/index.html
- Chrome Canary - Needed for only the headless mode, which still needs to be implemented for the python script.
	Link: https://www.google.com/chrome/browser/canary.html
- Download pex zip file:
	Link: https://drive.google.com/file/d/1FCBzRDr-17R8WMEirOlTdLu2bZUWf9Rx/view?usp=sharing
	Unzip the zip file in pointLoma directory
	Note: May need execute permission, use chmod +x file_name to add execute permission
- Download .kolibri zip file:
	Link: https://drive.google.com/file/d/1YMKA1b8H4kEo02_iYZcFIus27wtm8-hO/view?usp=sharing
	Unzip the zip file in pointLoma directory
## Setup
1. Copy over *setup.py* and *pointloma.py* into a location of your choice. The two files must be in the same directory.
2. Install all dependencies by using the following command:
```
    python setup.py
```
*Note:* Use *virutalenv* if you would like to test in a clean environment. It was used in testing and building of this script.

## Usage
Usage: `pointLoma [OPTIONS] LINK`

  This script runs lighthouse using the command line interface.

Options:

    --count=INTEGER  Number of tests to run. Default is 1.
	--output-file=TEXT  Name of csv file w/o extension. Default is "output".
	--help           Show this message and exit. 

Examples:
To specify the number of tests to run:
```
pointLoma --count=3 https://kolibridemo.learningequality.org
```
To specity the number of tests to run and the name csv file
```
pointLoma --count=3 --output-file=learningEquality https://kolibridemo.learningequality.org
```
## Output
Each test will output to a json file, *resultsN.report.json*, where *N*, is the test number. 
Unless specified, a csv file named 'output.csv' will contain the timestamp, the performance metrics, and the version we are testing.
All files will be in the directory where the script was run. 

## Coming Soon
- Testing multiple links automatically without using command line argument by using dictionary
- Automatically login for headless mode
- Integrate with Health Inspector (https://github.com/learningequality/auto-screenshots)
