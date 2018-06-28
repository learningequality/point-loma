
# Point Loma
*A Python library to execute [Lighthouse](https://developers.google.com/web/tools/lighthouse/) audits and export results of the running performance tests against different URL's. Aims to track code quality and improve user experience.*

## Requirements
- Python 3 (not compatible with Python 2 at the moment)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse/)
- [Google Chrome](https://www.google.com/chrome/browser/desktop/) (>= Chrome 59 for headless support)

## Installation
- Clone the repository or download the project as a zip file from this Github page
- Install Lighthouse as a Node command line tool:
```
    npm install -g lighthouse
    # or use yarn:
    yarn global add lighthouse
```
*Note:* Lighthouse requires Node 6 or later. It is [recommended](https://developers.google.com/web/tools/lighthouse/#cli) to install the current [Long-Term Support](https://github.com/nodejs/LTS) version of [Node](https://nodejs.org/).

## Setup (optional)
### Virtualenv
Create `virtualenv` to target the Python 3 interpreter, e.g.:

- `python3.6 -m venv ~/.venvs/pointloma3.6`
- `source ~/.venvs/pointloma3.6/bin/activate`

### Why is this step optional?

There are currently no requirements outside of the Python's standard library, so `pointloma` will work perfectly fine simply by substituing all calls to the `python` interpreter by directly targeting `python3` interpreter, e.g.:

Instead of running:

```python pointloma [url]```

You could run:

```python3 pointloma [url]```

## Usage
```python pointloma [-h] [-r RUNS] [-o OUTPUT_PATH] [-v] url```

### Options

```
positional arguments:
  url                   url to test against

optional arguments:
  -h, --help            show this help message and exit
  -r RUNS, --runs RUNS  number of test runs
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        path to csv file output
  -v, --verbose         increase output verbosity
```

### Examples

To specify the number of tests to run:
```
python pointloma -r 3 https://kolibridemo.learningequality.org
```
To specity the number of tests to run and the name of the csv file output
```
python pointloma -r 3 --output-path /tmp/example.csv http://localhost:8000/learn
```
To run the test a single time with verbose logging output:
```
python pointloma -v https://kolibridemo.learningequality.org
```

## Output
### Format
Resulting output is a comma delimited csv file with the following columns:
- Timestamp
- First Meaningful Paint [ms]
- First Interactive [ms]
- Consistently Interactive [ms]
- Speed Index [ms]
- Estimated Input Latency [ms]

### Location
The csv file with the results will be written to one of the two following locations:
- path specified by `-o` or `--output-path` CLI arguments
- to the `output` directory under the the `pointloma` codebase root directory, e.g.:
    - `output/results_1987_08_20__11_22_33__123456.csv`

### Appending to the output
The same output path can be used for multiple test runs (by using the `-o` or `--output-path` CLI options) as the results will simply be appended to the specified csv file.

This approach can be useful when testing a single URL with different code states or repository branches and wanting to gather the results in a single csv file for easier processing.


## Next steps
- Automatically generate graphs from the resulting csv
- Test multiple URL's by specifying file with the URL's listed
- Test URL's which require authentication
- Integrate with Health Inspector ([https://github.com/learningequality/auto-screenshots](https://github.com/learningequality/auto-screenshots))
