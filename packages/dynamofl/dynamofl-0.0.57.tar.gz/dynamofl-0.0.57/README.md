# Run the samples
Try the samples to see the DynamoFL SDK in action.

## Generate API key from UI

## Setup the environment
1. Create a venv and activate
2. `cd` into the `client-py/samples` directory
3. Run `cp .env.template .env` to create a `.env` file and set the `API_HOST` and `API_KEY` (generated from the UI)
4. Run `pip install -r requirements.txt` to install the dependencies to the venv
5. Run `python sample.py`

# Development

## Install requirements
1. Create a venv and activate
2. `cd` into the `client-py` directory
3. Run `pip install -r requirements.txt` to install the dependencies to the venv

## Tired of copy-pasting your latest changes into `site-packages` ?

Follow the steps below to run the `samples` against your latest code

1. Open `<venv>/bin/activate` 
2. Paste the below code snippet to the end of file and set `CLIENT_PY_DIR` 
```
CLIENT_PY_DIR=<absolute path to client-py repo>
SYSPATHS=$($VIRTUAL_ENV/bin/python -c "import sys; print(':'.join(x for x in sys.path if x))")
export PYTHONPATH=$SYSPATHS":"$CLIENT_PY_DIR
```
3. Run `pip uninstall dynamofl` to delete the `dynamofl` package from `site-packages`

<br>

> To test against a published `dynamofl` SDK, run `pip install dynamofl` before running the samples


# Build and publish the package

NOTE: Building the package would delete the `dist` directory and `dynamofl.egg-info` file at the root of `client-py`

1. Ensure the libraries listed in `client-py/requirements.txt` is installed in the venv
2. Activate the venv
3. Run `./build.sh`