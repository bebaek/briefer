# briefer
Send personalized briefing email daily. Collect repetitive checklists and
see them in your single email message. Currently, the email contents are created
from news highlights and google calendar events.

## Installation

Prerequisites: git, bash, python3, pip3,
[external API keys](#Set-up-external-APIs)

Download the repo.

    git clone https://github.com/bebaek/briefer.git

In the cloned directory, run the CLI installation script. This installs this
package with pip3, creates a configuration file, and registers to the users
crontab. (Run `crontab -e` to further modify your crontab.)

    bash install.sh

See the usage of the main command:

    briefer -h

(Re-)configure:

    briefer config

Test-send an email:

    briefer send

## Set up external APIs

Set up the sender email account for SMTP use. Of course, have a receiver email
account too.

Get a NewsAPI key from [NewsAPI](https://newsapi.org).

(To be expanded.)
Get a google calendar account and authorize this app for the API access. Refer
to [reference 1](https://developers.google.com/calendar/auth) and
[reference 2](https://developers.google.com/identity/sign-in/devices).
Set the scope to `https://www.googleapis.com/auth/calendar.readonly`.
First, collect a bunch of keys: `client_id`, `client_secret`, device `code`.
Then get `refresh_token`.

## Development

### Setting up environment

Prerequisites: git, bash,
[edm](https://www.enthought.com/enthought-deployment-manager/)

Download repo.

    git clone https://github.com/bebaek/briefer.git

Run setup script.

    bash ci/setup-devenv.sh

### Running the app

Prerequisites: sender/receiver email accounts for SMTP use, API key from
[NewsAPI](https://newsapi.org), google calendar account and API access

Activate the dev environment:

    edm shell -e briefer

Check the usage and also if it runs:

    briefer -h

First, set up the configs:

    briefer config

Then, run send out an email:

    briefer send
