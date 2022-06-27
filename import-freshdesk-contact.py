import os
import typer
from commands.freshdesk import ImportGitHubUserInFreshdesk

# TODO: Add documentation for input parameters
# TODO: Improve command description formatting and contents
def main(github_username: str, freshdesk_subdomain: str):
    """Importing GitHub user as a Freshdesk contact.
    Requires the following environment variables:\n
    - GITHUB_TOKEN: enables communication with GitHub REST API v3\n
    - FRESHDESK_TOKEN: enables communication with Freshdesk REST API v2\n
    """
    github_token = os.getenv('GITHUB_TOKEN')
    freshdesk_token = os.getenv('FRESHDESK_TOKEN')

    if not github_username:
        raise Exception('No GitHub user login was provided (param 1)!')
    if not freshdesk_subdomain:
        raise Exception('No Freshdesk subdomain login was provided (param 2)!')
    if not github_token:
        raise Exception('GitHub token not available as environment variable (GITHUB_TOKEN)!')
    if not freshdesk_token:
        raise Exception('Freshdesk token not available as environment variable (FRESHDESK_TOKEN)!')

    typer.echo(f"User login: {github_username}")
    typer.echo(f"Subdomain: {freshdesk_subdomain}")
    # TODO: Log loaded tokens masked with asterisks
    typer.echo(f"GitHub token: {github_token}")
    typer.echo(f"Freshdesk token: {freshdesk_token}")

    command = ImportGitHubUserInFreshdesk(
        github_username=github_username,
        freshdesk_subdomain=freshdesk_subdomain,
        github_token=github_token,
        freshdesk_token=freshdesk_token
    )
    command.execute()

if __name__ == "__main__":
    typer.run(main)
