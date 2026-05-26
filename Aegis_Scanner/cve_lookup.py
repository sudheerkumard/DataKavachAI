import requests

class CVEIntegrator:
    def __init__(self, api_key=None):
        self.base_url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
        self.headers = {'apiKey': api_key} if api_key else {}

    def fetch_vulnerabilities(self, keyword):
        params = {'keywordSearch': keyword, 'resultsPerPage': 10}
        response = requests.get(self.base_url, params=params, headers=self.headers)
        return response.json().get('vulnerabilities', []) if response.status_code == 200 else []
