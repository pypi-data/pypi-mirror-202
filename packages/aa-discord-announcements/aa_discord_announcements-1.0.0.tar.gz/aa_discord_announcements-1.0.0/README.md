# AA Discord Announcements

[![Version](https://img.shields.io/pypi/v/aa-discord-announcements?label=release)](https://pypi.org/project/aa-discord-announcements/)
[![License](https://img.shields.io/github/license/ppfeufer/aa-discord-announcements)](https://github.com/ppfeufer/aa-discord-announcements/blob/master/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/aa-discord-announcements)](https://pypi.org/project/aa-discord-announcements/)
[![Django](https://img.shields.io/pypi/djversions/aa-discord-announcements?label=django)](https://pypi.org/project/aa-discord-announcements/)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](http://black.readthedocs.io/en/latest/)
[![Discord](https://img.shields.io/discord/790364535294132234?label=discord)](https://discord.gg/zmh52wnfvM)
[![Checks](https://github.com/ppfeufer/aa-discord-announcements/actions/workflows/automated-checks.yml/badge.svg)](https://github.com/ppfeufer/aa-discord-announcements/actions/workflows/automated-checks.yml)
[![codecov](https://codecov.io/gh/ppfeufer/aa-discord-announcements/branch/master/graph/badge.svg?token=9I6HQB6W6J)](https://codecov.io/gh/ppfeufer/aa-discord-announcements)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](https://github.com/ppfeufer/aa-discord-announcements/blob/master/CODE_OF_CONDUCT.md)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/N4N8CL1BY)

Discord Announcements via [Alliance Auth](https://gitlab.com/allianceauth/allianceauth)

Write announcements and manage who can write announcements on your corporation or
alliance Discord through Alliance Auth.


## Contents

- [Installation](#installation)
- [Change Log](https://github.com/ppfeufer/aa-discord-announcements/blob/master/CHANGELOG.md)
- [Code of Conduct](https://github.com/ppfeufer/aa-discord-announcements/blob/master/CODE_OF_CONDUCT.md)
- [Contribute](https://github.com/ppfeufer/aa-discord-announcements/blob/master/CONTRIBUTING.md)


## Installation

### ⚠️ Important ⚠️

This app is a plugin for Alliance Auth. If you don't have Alliance Auth running already,
please install it first before proceeding.
(see the official
[AA installation guide](https://allianceauth.readthedocs.io/en/latest/installation/allianceauth.html)
for details)

**⚠️ You also want to make sure that you have the
[Discord service](https://allianceauth.readthedocs.io/en/latest/features/services/discord.html)
installed, configured and activated before installing this app. ⚠️**

### Step 1 - Install the app

Make sure you are in the virtual environment (venv) of your Alliance Auth installation.
Then install the latest version:

```bash
pip install aa-discord-announcements
```

### Step 2 - Update your AA settings

Configure your AA settings (`local.py`) as follows:

- Add `'aa_discord_announcements',` to `INSTALLED_APPS`


### Step 3 - Finalize the installation

Copy static files and run migrations

```bash
python manage.py collectstatic
python manage.py migrate
```

Restart your supervisor services for AA

### Step 4 - Setup permission

Now you can setup permissions in Alliance Auth for your users.
Add `aa_discord_announcements | general | Can access this app` to the states and/or
groups you would like to have access.

### Step 5 - Setup the app

In your admin backend you'll find a new section called `Discord Announcements`.
This is where you set all your stuff up, like the webhooks you want to ping and who
can ping them. It's pretty straight forward, so you shouldn't have any issues. Go nuts!
