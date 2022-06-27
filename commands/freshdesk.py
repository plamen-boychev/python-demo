from library.github.githubclient import GitHubClient
from library.freshdesk.freshdeskclient import FreshdeskClient
from converters.freshdesk import GitHubUserToFreshdeskContact

class ImportGitHubUserInFreshdesk():
    """Implements the end-to-end mechanism of importing a GitHub user as Freshdesk contact."""

    github_username = None
    freshdesk_subdomain = None
    github_token = None
    freshdesk_token = None

    def __init__(self, github_username: str, freshdesk_subdomain: str, github_token: str, freshdesk_token: str):
        """Constructor."""
        # Validating parameters
        if not github_username:
            raise Exception('No GitHub user login was provided!')
        if not freshdesk_subdomain:
            raise Exception('No Freshdesk subdomain login was provided!')
        if not github_token:
            raise Exception('No GitHub token was provided!')
        if not freshdesk_token:
            raise Exception('No Freshdesk token was provided!')

        self.github_username = github_username
        self.freshdesk_subdomain = freshdesk_subdomain
        self.github_token = github_token
        self.freshdesk_token = freshdesk_token

    def execute(self):
        print("Running import command execute!")

        # Fetching user details
        github_client = GitHubClient(token=self.github_token)
        github_user = github_client.fet_user_details(self.github_username)

        # Converting to contact structure
        converter = GitHubUserToFreshdeskContact()
        contact = converter.convert(github_user)

        # Persist contact details
        freshdesk_client = FreshdeskClient(subdomain=self.freshdesk_subdomain, api_key=self.freshdesk_token)
        freshdesk_client.persist_contact(self.github_username, contact)
