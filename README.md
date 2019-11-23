# briefer
Send personalized briefing email daily. Collect repetitive checklists and
see them in your single email message.

## Development

### Setting up environment

Prerequisites: git, bash

Download repo.

    git clone https://github.com/bebaek/briefer.git

Run setup script.

    bash ci/setup-devenv.sh

### Running the app

Prerequisites: sender/receiver email accounts for SMTP use, API key from
[NewsAPI](https://newsapi.org)

Activate the dev environment:

    edm shell -e briefer

Check the usage and also if it runs:

    briefer -h

First, set up the configs:

    briefer config

Then, run send out an email:

    briefer send
