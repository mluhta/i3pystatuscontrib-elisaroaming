from i3pystatus import IntervalModule, formatp
from i3pystatus.core.util import require, internet
import requests
import urllib

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
API_BASE = "https://verkkoasiointi.elisa.fi/rest"

class ElisaRoaming(IntervalModule):
    """
    Fetches used roaming quota information from OmaElisa.

    Requires PyPI package `requests`.

    .. rubric:: Available formatters

    * {used} amount of quota used in gigabytes
    * {total} amount of total quota in gigabytes
    * {free} amount of data left in gigabytes
    * {used_percentage} percentage of data used

    """
    interval = 60

    settings = (
        "format",
        "color",
        ("color_warning", "color when data usage over warning_percentage threshold"),
        ("warning_percentage", "percentage threshold for data usage, 0.0 - 1"),
        ("email", "OmaElisa email/username"),
        ("password", "OmaElisa password"),
        ("number", "target phone number")
    )

    format = "ROAM: {used}Gb/{total}Gb"
    color = "#FFFFFF"
    color_warning = "#ff0000"

    warning_percentage = 0.8

    @require(internet)
    def get_roaming_info(self):
        try:
            session = requests.Session()
            session.headers.update({"User-Agent": USER_AGENT})
            session.headers.update({"Referer": "https://verkkoasiointi.elisa.fi/"})

            # Get auth code for login
            res = session.get("{api}/public/login/password-auth-code/{email}".format(
                api=API_BASE, email=urllib.parse.quote(self.email)))
            res.raise_for_status() 
            auth_code = res.json()["code"]

            # Login, get SSO token
            res = session.post(
                    "https://id.elisa.fi/sso/login?client_id=ipa&language=fi",
                    json={
                        "accountId": self.email,
                        "authCode": auth_code,
                        "password": self.password
                    })
            res.raise_for_status()
            token = res.json()["token"]

            # Login with the token
            res = session.post(
                    "{api}/public/login".format(api=API_BASE),
                    json={"token": token})
            res.raise_for_status()

            # Get roaming usage
            res = session.get(
                    "{api}/mobile/{number}/roaming-package-usage".format(
                        api=API_BASE, number=self.number))
            res.raise_for_status()
            data = res.json()

            # TODO: calc data left
            return {
                "used": data["usedInGb"],
                "total": data["totalInGb"]
            }

        except ConnectionResetError:
            return None
        except requests.exceptions.ConnectionError:
            return None

    def disable(self):
        self.output = None

    def run(self):
        # Check that we have credentials
        # TODO: use keyring
        if not self.email or not self.password or not self.number:
            self.output = {
                    "full_text": "ROAM: FAIL!",
                    "color": "#ff0000",
            }
            return 
        usage = self.get_roaming_info()
        if not usage:
            return self.disable()

        used_percentage = float(usage["used"])/float(usage["total"])
        free = float(usage["total"]) - float(usage["used"])

        output_color = self.color
        if used_percentage > self.warning_percentage:
            output_color = self.color_warning

        formatting = {
            "used": usage["used"],
            "total": usage["total"],
            "free": free,
            "used_percentage": used_percentage
        }

        self.output = {
            "full_text": formatp(self.format, **formatting).strip(),
            "color": output_color
        }

