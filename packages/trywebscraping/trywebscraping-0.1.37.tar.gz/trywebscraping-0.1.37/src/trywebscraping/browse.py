from typing import List, Dict
import requests
import time
from .api_key import get_api_key

class Browse:
    def __init__(self, url):
        self.url = url
        self.html = None
        self.browser = None
        self.page = None
        self.headless_actions: List[Dict] = []
        self.session = requests.Session()
        self.api_url = "http://188.245.148.139:3000"
        self.api_key = get_api_key()

    def get_html(self) -> str:
        if self.html is None and self.api_key:
            self.html = self.headless_scrape()
        return self.html

    def headless_scrape(self) -> str:
        if not self.api_key:
            return ""
        
        try:
            # Check API health
            health_check = self.session.get(f"{self.api_url}/healthz")
            if health_check.status_code != 200:
                raise Exception(f"API endpoint not healthy: {health_check.status_code}")

            # Get page HTML
            print(f"Getting page HTML for {self.url}")
            response = self.session.get(
                f"{self.api_url}/pagehtml",
                params={"url": self.url, "api_key": self.api_key}
            )
            
            if response.status_code != 200:
                raise Exception(f"Failed to fetch page: {response.status_code}")

            # Process any queued actions
            for action in self.headless_actions:
                result = self.perform_action(action)
                if result:  # If action changes the page content
                    self.html = result
            
            return response.text

        except requests.RequestException as e:
            raise Exception(f"Failed to connect to API: {str(e)}")

    def perform_action(self, action: Dict) -> str | None:
        """Execute a queued action through the API"""
        if not self.api_key:
            return None
        
        try:
            response = self.session.post(
                f"{self.api_url}/action",
                json={
                    **action,
                    "url": self.url,
                    "api_key": self.api_key
                }
            )

            if response.status_code != 200:
                raise Exception(f"Action failed: {response.status_code}")

            # For actions that change the page, we need to get the new HTML
            if action["action"] in ["click", "typing"]:
                time.sleep(1)  # Wait for any page updates
                self.html = None  # Clear cached HTML
                return self.get_html()  # Get fresh HTML

            return None

        except requests.RequestException as e:
            raise Exception(f"Failed to perform action: {str(e)}")

    def entering(self, selector: str):
        if self.api_key:
            self.headless_actions.append({"action": "entering", "selector": selector})
        return self

    def typing(self, selector: str, text: str):
        if self.api_key:
            self.headless_actions.append({"action": "typing", "selector": selector, "text": text})
        return self

    def click(self, selector: str):
        if self.api_key:
            self.headless_actions.append({"action": "click", "selector": selector})
        return self

    def __del__(self):
        """Clean up the session when the object is destroyed"""
        if hasattr(self, 'session'):
            self.session.close()