# sectoralarm/cache.py

import json
import os
import logging
from .endpoints import get_data_endpoints
from .utils import extract_structure

logger = logging.getLogger("SectorAlarmAPI")


class CacheManager:
    def __init__(self, api):
        self.api = api  # Reference to the SectorAlarmAPI instance
        self.cache = {}

    def build_cache(self):
        """Build the cache of categories, sections, and modules."""
        endpoints = get_data_endpoints(self.api.panel_id)

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api.auth_token,
            "API-Version": "5"
        }
        payload = {"panelId": self.api.panel_id}

        for name, (method, url) in endpoints.items():
            if method == "POST":
                response = self.api.session.post(url, headers=headers, json=payload, timeout=30)
            else:
                response = self.api.session.get(url, headers=headers, timeout=30)

            if response.status_code == 200:
                data = response.json()
                structure = extract_structure(data)
                self.cache[name] = structure
            else:
                logger.error(f"Failed to retrieve data from {name}. Status code: {response.status_code}")

    def save_cache(self, filename='cache.json'):
        """Save the cache to a file."""
        with open(filename, 'w', encoding='utf-8') as cache_file:
            json.dump(self.cache, cache_file, indent=4, ensure_ascii=False)

    def load_cache(self, filename='cache.json'):
        """Load the cache from a file, or build it if it doesn't exist."""
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as cache_file:
                self.cache = json.load(cache_file)
            logger.info(f"Cache loaded from {filename}")
        else:
            logger.info("Cache file not found. Building cache...")
            self.build_cache()
            self.save_cache(filename)

    def rebuild_cache(self, filename='cache.json'):
        """Rebuild the cache by fetching data from the API."""
        logger.info("Rebuilding cache...")
        self.build_cache()
        self.save_cache(filename)
