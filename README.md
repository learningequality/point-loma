

# Point Loma
*A Python script to execute Lighthouse and export results of running performance tests against different URLs on different releases.Aims to track code quality and improve user experience.*

## Requirements
- Python 3 (not compatible with Python 2 at the moment)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse/)
- [Google Chrome](https://www.google.com/chrome/browser/desktop/)

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
Usage: `python pointloma [OPTIONS] url`

Options:

```
positional arguments:
  url                   Url to test against

optional arguments:
  -h, --help            show this help message and exit
  -hl HEADLESS, --headless HEADLESS
                        Run in headless mode
  -r RUNS, --runs RUNS  Number of test runs
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        Path to csv file output
  -v, --verbose         Increase output verbosity

```

Examples:
To specify the number of tests to run:
```
python pointloma -r 3 https://kolibridemo.learningequality.org
```
To specity the number of tests to run and the name of the csv file output
```
python pointloma -r 3 --output-path /tmp/example.csv http://localhost:8000/learn
```
## Output
TBD

## Coming Soon
TBD
