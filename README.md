

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

## Setup
### Virtualenv
Create `virtualenv` to target the Python 3 interpreter, e.g.:

- `python3.6 -m venv ~/.venvs/pointloma3.6`
- `source ~/.venvs/pointloma3.6/bin/activate`

### Fetch package dependencies

```pip install -r requirements.txt```

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
  -a AUTH_MODULE, --auth-module AUTH_MODULE
                        authentication module to use
```

### Authentication

#### Overview
Point Loma supports testing URLs which are behind authentication with custom auth modules. Currently, a single auth module is supported, `kolibri`, but additional ones can be written for specific use cases.

`kolibri` auth module enables authentication to [Kolibri](https://github.com/learningequality/kolibri) instances and its code is extensively commented so it should be rather straightforward to use it to write your own custom authentication module.

#### Configure
To be able to use `kolibri` (or custom auth module) you should add the following environment variables with the user credentials, e.g. in your `~/.bashrc`:

- `POINTLOMA_USERNAME=yourusername`
- `POINTLOMA_PASSWORD=yourpassword`

You could also simply prepend environment variables to the `pointloma` CLI command, but of course, in that case you would have to type it every time you use it (adding it to your `~/.bashrc` or similiar script would persist it), e.g.:

```POINTLOMA_USERNAME=yourusername POINTLOMA_PASSWORD=yourpassword python pointloma --auth-module kolibri http://kolibridemo.learningequality.org/user```

### Examples
#### Specifying the number of tests to run
```
python pointloma -r 3 https://example.com
```

#### Specifying the number of tests to run and the name of the csv file output
```
python pointloma -r 3 --output-path /tmp/example.csv http://localhost:8000
```

#### Running the test once time with verbose logging output
```
python pointloma -v https://example.com
```

#### Running the test using authentication modules

Environment variables added to e.g. `~/.bashrc`:

```
python pointloma --auth-module kolibri http://kolibridemo.learningequality.org/user
```
Environment variables prepended to the command:

```
POINTLOMA_USERNAME=yourusername POINTLOMA_PASSWORD=yourpassword python pointloma --auth-module kolibri http://kolibridemo.learningequality.org/user
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
- Test multiple URLs by specifying file with the URLs listed
- Integrate with Health Inspector ([https://github.com/learningequality/auto-screenshots](https://github.com/learningequality/auto-screenshots))
