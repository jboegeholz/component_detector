import json
import time
import urllib.error
import urllib.parse
import urllib.request


class NexarApiError(Exception):
    pass


class NexarApi:
    TOKEN_URL = "https://identity.nexar.com/connect/token"
    GRAPHQL_URL = "https://api.nexar.com/graphql"

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires_at = 0

    def search_mpn(self, mpn):
        query = """
        query SearchMpn($mpn: String!) {
          supSearchMpn(q: $mpn) {
            hits
            results {
              part {
                mpn
                octopartUrl
                manufacturer {
                  name
                  homepageUrl
                }
                sellers {
                  company {
                    name
                  }
                  offers {
                    prices {
                      quantity
                      price
                    }
                  }
                }
              }
            }
          }
        }
        """

        data = self._graphql(query, {"mpn": mpn})
        return data["data"]["supSearchMpn"]

    def _graphql(self, query, variables=None):
        token = self._get_access_token()
        body = json.dumps({
            "query": query,
            "variables": variables or {},
        }).encode("utf-8")

        request = urllib.request.Request(
            self.GRAPHQL_URL,
            data=body,
            headers={
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json",
            },
            method="POST",
        )

        response = self._request_json(request)

        if "errors" in response:
            raise NexarApiError(response["errors"])

        return response

    def _get_access_token(self):
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token

        form = urllib.parse.urlencode({
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }).encode("utf-8")

        request = urllib.request.Request(
            self.TOKEN_URL,
            data=form,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )

        response = self._request_json(request)

        if "access_token" not in response:
            raise NexarApiError("Nexar token response did not contain access_token.")

        expires_in = int(response.get("expires_in", 3600))
        self.access_token = response["access_token"]
        self.token_expires_at = time.time() + expires_in - 60
        return self.access_token

    def _request_json(self, request):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = response.read().decode("utf-8")
        except urllib.error.HTTPError as error:
            details = error.read().decode("utf-8")
            raise NexarApiError(f"Nexar HTTP {error.code}: {details}") from error
        except urllib.error.URLError as error:
            raise NexarApiError(f"Nexar request failed: {error.reason}") from error

        return json.loads(payload)
