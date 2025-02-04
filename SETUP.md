# Tomaba

## Set up instructions

### 1. Get the environment variables

Create a file called `.env` at `tomaba/.env`. Get the required variables from Matt.

### 2. Install PyEnv and Python 3.13

Following assumes MacOS. See github for latest instructions (https://github.com/pyenv/pyenv?tab=readme-ov-file#b-set-up-your-shell-environment-for-pyenv).

```bash
brew update
brew install pyenv

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init - zsh)"' >> ~/.zshrc

exec "$SHELL"

pyenv install 3.13
pyenv global 3.13
```



### 3. Install poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Follow the output instructions to add the path to the poetry executable to your path
variable in your .zprofile.

```bash
export PATH="/Users/mattmahowald/.local/bin:$PATH"
```

Test poetry exists

```bash
poetry --version
```

### 4. Install packages

### 5. Test the app

```bash
poetry run python tomaba/test.py
```

# Tomaba Setup Instructions

## 1. Obtain Environment Variables

Create a .env file: Place this file in the tomaba/ directory.

Add the required variables: Contact Matt to obtain the necessary environment variables and add them to the .env file.

## 2. Install Poetry

Poetry is a tool for dependency management and packaging in Python. We'll install it using the official installer.

### a. Run the Installation Script

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### b. Add Poetry to Your PATH

After installation, ensure the poetry command is accessible from your terminal by adding Poetry's bin directory to your system's PATH.

Locate the bin directory: By default, Poetry is installed in $HOME/.local/bin.

Modify your shell configuration:

For Zsh users (common on macOS):

Open your .zprofile file located in your home directory.

Add the following line:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Save the file and exit.

Apply the changes by running:

```bash
source ~/.zprofile
```

### c. Verify the Installation

To confirm Poetry is installed correctly, run:

```bash
poetry --version
```

You should see the version number displayed.

## 3. Install Project Dependencies

With Poetry installed, navigate to the root directory of the project (where pyproject.toml is located) and run:

```bash
poetry install
```

This command will install all the dependencies specified in the pyproject.toml file.

## 4. Test the Application

To ensure everything is set up correctly, run the test script:

```bash
poetry run python tomaba/test.py
```

This will execute the test.py script located in the tomaba directory using Poetry's managed environment.

## 5. Setup GCloud

Once you are a part of the gcloud project, make sure to login to gcloud form your terminal:

If gcloud and/or homebrew are not installed:

```bash
# install homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# install gcloud command line interface
brew install --cask google-cloud-sdk

# sign into gcloud:
gcloud init
```

```bash
gcloud config set project tomaba
gcloud services enable run.googleapis.com cloudbuild.googleapis.com secretmanager.googleapis.com
gcloud auth login
gcloud auth application-default login
```

### 6. After making some changes, deploy to GCP using the following command

```bash
gcloud builds submit --tag gcr.io/tomaba/tomaba
gcloud run deploy tomaba-bot \
 --image gcr.io/tomaba/tomaba \
 --platform managed \
 --region us-central1 \
 --allow-unauthenticated \
 --set-secrets DISCORD_TOKEN=DISCORD_TOKEN:latest,MISTRAL_API_KEY=MISTRAL_API_KEY:latest

```
