import os
import json
from typing import Any, Dict, Optional

import requests
import aiohttp

UNIFIED_SEARCH_API_URL = "https://cloud-iqs.aliyuncs.com/search/unified"
UNIFIED_API_KEY = os.getenv("UNIFIED_API_KEY", "")


class UnifiedSearchAPIWrapper:
    """
    阿里云 IQS unified search API 封装
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or UNIFIED_API_KEY
        if not self.api_key:
            raise ValueError("UNIFIED_API_KEY 环境变量未设置")

    def search(
        self,
        query: str,
        timeRange: str = "NoLimit",
        category: Optional[str] = None,
        engineType: str = "Generic",
        contents: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        """
        同步请求 unified search
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "query": query,
            "engineType": engineType,
            "timeRange": timeRange,
        }
        if category:
            payload["category"] = category
        if contents:
            payload["contents"] = contents

        resp = requests.post(UNIFIED_SEARCH_API_URL, headers=headers, json=payload)
        resp.raise_for_status()
        return resp.json()

    async def search_async(
        self,
        query: str,
        timeRange: str = "NoLimit",
        category: Optional[str] = None,
        engineType: str = "Generic",
        contents: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        """
        异步请求 unified search
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "query": query,
            "engineType": engineType,
            "timeRange": timeRange,
        }
        if category:
            payload["category"] = category
        if contents:
            payload["contents"] = contents

        async with aiohttp.ClientSession() as session:
            async with session.post(UNIFIED_SEARCH_API_URL, headers=headers, json=payload) as resp:
                if resp.status == 200:
                    data = await resp.text()
                    return json.loads(data)
                else:
                    raise Exception(f"Error {resp.status}: {resp.reason}")
