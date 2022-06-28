# Freshdesk import module

## Packages
- `commands` - abstractions of end-to-end processes available to be invoked
- `converters` - unitities for converting data from one source to another
- `library/freshdesk` - library implementation for consuming the Freshdesk REST API (v2)
- `library/github` - library implementation for consuming the GitHub REST API (v3)
- `library/rest` - provides reusable definitions for consuming REST API services

## Configuration
A couple of environment variables are required:
- `GITHUB_TOKEN` - GitHub personal access token, generated on demand, more details are available in the [official docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).
- `FRESHDESK_TOKEN` - Freshdesk API token - generated automatically, available in the administrative interface, more details are available in the [official docs](https://support.freshdesk.com/en/support/solutions/articles/215517-how-to-find-your-api-key).

## Prerequisites:
- Python 3 is installed (tested with 3.9.13).
- PyPi available
- GitHub user target is available
- GitHub personal access token is available
- Freshdesk service is available
- Freshdesk subdomain is available

## Setup
Dependencies need to be installed - this is possible via executing `pip3 install -r requirements.txt` in a terminal with python 3 available.

## Usage
Running the cli script is as simple as running `python import-freshdesk-contact.py {github-username} {freshdesk-subdomain}`.  
Prerequisites for running the script is having the following environment variables available - check the (Configuration)[#configuration] section.

## Testing
- Unit tests are available for most modules.
  - Running all tests can be done via executing `python -m unittest`
  - Specific tests can be done via executing `python -m unittest {path-to-test}/{test-file}`
- End-to-end tests are available for the commands
