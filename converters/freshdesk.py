class GitHubUserToFreshdeskContact():
    """Converts a GitHub user to a Freshdesk contact."""

    def __init__(self):
        """Constructor."""
        pass

    def convert(self, github_user_details:dict):
        # TODO: Convert details
        # TODO: Take declarative approach rather than imperative if possible, there
        #       might be portions that are dynamic and it might not be feasible.
        return {
            "name": github_user_details["name"],
            "email": github_user_details["email"],
            "unique_external_id": github_user_details["login"],
            "description": "Imported GitHub user, repositories URL: {}".format(github_user_details["repos_url"])
        }
