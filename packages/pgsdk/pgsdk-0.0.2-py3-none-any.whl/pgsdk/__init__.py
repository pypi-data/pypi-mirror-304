import requests
import pyotp
from pprint import pprint


def parse_response(response: requests.Response):
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    if response.status_code == 200:
        pprint(response.json())
    else:
        print(response.text)
        raise Exception(f"Error: {response.status_code}")


class pgsdk:
    def __init__(
        self,
        base_uri: str = "https://api.paralegalgenius.com",
        api_key: str = None,
        verbose: bool = True,
    ):
        if not base_uri:
            base_uri = "https://api.paralegalgenius.com"
        self.base_uri = base_uri
        self.verbose = verbose
        if not api_key:
            self.headers = {"Content-Type": "application/json"}
        else:
            api_key = api_key.replace("Bearer ", "").replace("bearer ", "")
            self.headers = {
                "Authorization": f"{api_key}",
                "Content-Type": "application/json",
            }
        if self.base_uri[-1] == "/":
            self.base_uri = self.base_uri[:-1]
        self.failures = 0

    def handle_error(self, error) -> str:
        print(f"Error: {error}")
        raise Exception(f"Unable to retrieve data. {error}")

    def login(self, email, otp):
        response = requests.post(
            f"{self.base_uri}/v1/login",
            json={"email": email, "token": otp},
        )
        if self.verbose:
            parse_response(response)
        response = response.json()
        if "detail" in response:
            detail = response["detail"]
            if "?token=" in detail:
                token = detail.split("token=")[1]
                self.headers = {"Authorization": token}
                print(f"Log in at {detail}")
                return token

    def register_user(self, email, first_name, last_name):
        login_response = requests.post(
            f"{self.base_uri}/v1/user",
            json={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
            },
        )
        if self.verbose:
            parse_response(login_response)
        response = login_response.json()
        if "otp_uri" in response:
            mfa_token = str(response["otp_uri"]).split("secret=")[1].split("&")[0]
            totp = pyotp.TOTP(mfa_token)
            self.login(email=email, otp=totp.now())
            return response["otp_uri"]
        else:
            return response

    def user_exists(self, email):
        response = requests.get(f"{self.base_uri}/v1/user/exists?email={email}")
        if self.verbose:
            parse_response(response)
        return response.json()

    def update_user(self, **kwargs):
        response = requests.put(
            f"{self.base_uri}/v1/user", headers=self.headers, json=kwargs
        )
        if self.verbose:
            parse_response(response)
        return response.json()

    def get_user(self):
        response = requests.get(f"{self.base_uri}/v1/user", headers=self.headers)
        if self.verbose:
            parse_response(response)
        return response.json()

    def create_case(self, case_name, case_number, case_description="", company_id=None):
        response = requests.post(
            f"{self.base_uri}/v1/cases",
            headers=self.headers,
            json={
                "case_name": case_name,
                "case_number": case_number,
                "case_description": case_description,
                "company_id": company_id,
            },
        )
        return parse_response(response)

    def get_cases(self):
        response = requests.get(f"{self.base_uri}/v1/cases", headers=self.headers)
        return parse_response(response)

    def get_case(self, case_id):
        response = requests.get(
            f"{self.base_uri}/v1/cases/{case_id}", headers=self.headers
        )
        return parse_response(response)

    def update_case(self, case_id, **kwargs):
        # Convert camelCase to snake_case for API compatibility
        data = {}
        for key, value in kwargs.items():
            if "case" in key:
                new_key = key.replace("case", "").lower()
            else:
                new_key = "".join(
                    ["_" + c.lower() if c.isupper() else c for c in key]
                ).lstrip("_")
            data[new_key] = value

        response = requests.put(
            f"{self.base_uri}/v1/cases/{case_id}", headers=self.headers, json=data
        )
        return parse_response(response)

    def archive_case(self, case_id):
        response = requests.delete(
            f"{self.base_uri}/v1/cases/{case_id}", headers=self.headers
        )
        return parse_response(response)

    def upload_document(self, case_id, file_path):
        with open(file_path, "rb") as file:
            files = {"file": (file_path, file)}
            headers = {
                key: value
                for key, value in self.headers.items()
                if key != "Content-Type"
            }
            response = requests.post(
                f"{self.base_uri}/v1/cases/{case_id}/documents",
                headers=headers,
                files=files,
            )
        return parse_response(response)

    def get_case_documents(self, case_id):
        response = requests.get(
            f"{self.base_uri}/v1/cases/{case_id}/documents", headers=self.headers
        )
        return parse_response(response)

    def delete_document(self, document_id):
        response = requests.delete(
            f"{self.base_uri}/v1/documents/{document_id}", headers=self.headers
        )
        return parse_response(response)

    def query_case(self, case_id, query):
        response = requests.post(
            f"{self.base_uri}/v1/cases/{case_id}/query",
            headers=self.headers,
            json={"query": query},
        )
        return parse_response(response)
