# Autumn8 CLI

Autumn8 CLI is a toolkit, which allows you to easily interact programatically
with the Autumn8's ML service, AutoDL.

## Usage

To use the CLI - as a prerequisite, you'll have to log in into
autodl.autumn8.ai and generate an API key for you CLI from your Profile page.

Follow the instructions on https://autodl.autumn8.ai/profile
to authenticate your CLI.

## Available commands

```
Usage: autumn8-cli [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  login
  submit-model
  test-connection
```

### Login

```
Usage: autumn8-cli login [OPTIONS]

  Store API credentials for the CLI to use in the future.

Options:
  -u, --user_id TEXT  The ID of the user that the CLI will authenticate as in
                      AutoDL.
  -a, --api_key TEXT  API Key to use when authenticating in AutoDL from now
                      on.
  --help              Show this message and exit.
```

### Submit model

```
Usage: autumn8-cli submit-model [OPTIONS] MODEL_FILE_PATH
                                [MODEL_SCRIPT_ARGS]...

  Submit a model to AutoDL.

Options:
  -n, --name TEXT                 Name of the model to be used in AutoDL.
  -q, --quantization, --quants [FP32|FP16|INT8]
                                  Quantization for the model.
  --input_dims TEXT               The model input dimensions, specified as a
                                  JSON array
  --input_file TEXT               The model input filepath
  -y, --yes                       Skip all confirmation input from the user.
  -o, --organization_id, --org_id INTEGER
                                  The ID of the Organization to submit the
                                  model to
  -g, --group_id TEXT             The ID of the group to submit the model to
  --help                          Show this message and exit.
```

### Test connection

```
Usage: autumn8-cli test-connection [OPTIONS]

  Test connection to the autumn8.ai service, using the configured API key.
  Displays the user's email address upon successful connection.

Options:
  --help  Show this message and exit.
```
