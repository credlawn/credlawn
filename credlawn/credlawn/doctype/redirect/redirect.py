import frappe
from frappe.model.document import Document
import requests
from user_agents import parse

class Redirect(Document):
    def before_insert(self):
        self.click_count = 1
        self.device, self.browser = self.get_device_browser_info(self.user_agent or "Mozilla/5.0")
        self.city = self.get_ip_info(self.ip_address)
        self.set_click_type(self.ip_address, self.source)

    def get_ip_info(self, ip_address):
        access_token = self.get_ipinfo_access_token()
        if access_token:
            ip_info = requests.get(f"https://ipinfo.io/{ip_address}/json?token={access_token}").json()
            city = ip_info.get("city", "Unknown")
            region = ip_info.get("region", "Unknown")
            # Combine city and region in the desired format "City - Region"
            return f"{city} - {region}" if city != "Unknown" and region != "Unknown" else "Unknown"
        return "Unknown"

    def get_ipinfo_access_token(self):
        access_token_record = frappe.get_doc('Access Tokens', 'ipinfo.io')
        access_token = access_token_record.get_password("access_token")
        return access_token if access_token else None

    def get_device_browser_info(self, user_agent_string):
        user_agent = parse(user_agent_string)
        os = user_agent.os.family
        device = "Android" if "Android" in os else "iOS" if "iOS" in os else "Mac OS" if "Mac" in os else "Windows" if "Windows" in os else "Android" if "Linux" in os else "Unknown"
        return device, user_agent.browser.family

    def set_click_type(self, ip_address, source):
        self.click_type = "Repeat" if frappe.db.exists("Redirect", {"ip_address": ip_address, "source": source}) else "New"
