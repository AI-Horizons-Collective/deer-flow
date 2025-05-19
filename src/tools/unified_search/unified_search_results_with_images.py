import json
from typing import Any, Dict, List, Optional, Tuple, Union

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from pydantic import Field

from .unified_search_api_wrapper import UnifiedSearchAPIWrapper


class UnifiedSearchResultsWithImages(TavilySearchResults):  # type: ignore[override, override]
    """
    联网查询工具，返回标准结构化数据，支持图片和网页结果。
    """

    name: str = "unified_search_results_with_images"
    description: str = (
        "联网查询工具，返回结构化数据，支持图片、原始内容、图片描述等参数。"
    )

    # 配置参数，实例化时传递
    query: str = Field("", description="搜索问题，1~100字符")
    max_results: int = Field(default=10, description="最大返回结果数")
    include_raw_content: bool = Field(default=False, description="是否返回长正文")
    include_images: bool = Field(default=False, description="是否返回图片")
    include_image_descriptions: bool = Field(default=False, description="是否返回图片描述")
    include_answer: bool = Field(default=False, description="是否返回答案（无实际作用，仅为兼容性）")
    timeRange: str = Field(
        default="NoLimit",
        description="查询的时间范围，可选：OneDay, OneWeek, OneMonth, OneYear, NoLimit"
    )
    category: Optional[str] = Field(
        default=None,
        description="查询分类，多个行业用逗号分隔，可选：finance,law,medical,internet,tax,news_province,news_center"
    )
    engineType: str = Field(
        default="Generic",
        description="搜索引擎类型，可选：Generic, GenericAdvanced"
    )
    api_wrapper: UnifiedSearchAPIWrapper = Field(default_factory=UnifiedSearchAPIWrapper)

    def clean_results_with_images(self, raw: Dict) -> List[Dict]:
        """
        清洗 unified search 原始结果为标准结构化检索结果（严格对齐 tavily_search 结构）
        """
        results = []
        # 网页结果
        for item in raw.get("pageItems", []):
            page = {
                "type": "page",
                "title": item.get("title"),
                "url": item.get("link"),
                "content": item.get("snippet"),
                "score": item.get("rerankScore"),
            }
            # tavily_search 结构中 raw_content 对应 mainText
            if item.get("mainText"):
                page["raw_content"] = item.get("mainText")
            results.append(page)
            # images 字段单独拆分为 type=image
            if item.get("images"):
                for img_url in item["images"]:
                    results.append({
                        "type": "image",
                        "image_url": img_url,
                        "image_description": item.get("title") or "",
                    })
        # 场景化结构化结果不返回（tavily_search 不包含 scene 类型）
        return results

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Tuple[Union[List[Dict[str, Any]], str], Dict]:
        if not query or not str(query).strip():
            import logging
            logging.error(f"UnifiedSearchResultsWithImages: query 字段缺失, query={query}")
            raise ValueError("query 字段不能为空")
        contents = {
            "mainText": self.include_raw_content,
            "markdownText": False,
            "summary": True,
            "rerankScore": True,
        }
        try:
            raw_result = self.api_wrapper.search(
                query=query,
                timeRange=self.timeRange,
                category=self.category,
                engineType=self.engineType,
                contents=contents,
            )
        except Exception as e:
            raise
        cleaned = self.clean_results_with_images(raw_result)
        cleaned = cleaned[: self.max_results]
        print("sync", json.dumps(cleaned, indent=2, ensure_ascii=False))
        return cleaned, raw_result

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Tuple[Union[List[Dict[str, Any]], str], Dict]:
        if not query or not str(query).strip():
            raise ValueError("query 字段不能为空")
        contents = {
            "mainText": self.include_raw_content,
            "markdownText": False,
            "summary": True,
            "rerankScore": True,
        }
        try:
            raw_result = await self.api_wrapper.search_async(
                query=query,
                timeRange=self.timeRange,
                category=self.category,
                engineType=self.engineType,
                contents=contents,
            )
        except Exception as e:
            raise
        cleaned = self.clean_results_with_images(raw_result)
        cleaned = cleaned[: self.max_results]
        return cleaned, raw_result
