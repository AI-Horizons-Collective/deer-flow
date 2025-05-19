import json
from typing import Any, Dict, List, Optional

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from .unified_search_results_with_images import UnifiedSearchResultsWithImages

class UnifiedSearchArgs(BaseModel):
    """联网查询工具参数"""
    query: str = Field(..., description="搜索问题，1~100字符")
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

@tool("unified_search", args_schema=UnifiedSearchArgs)
def unified_search_tool(args: UnifiedSearchArgs) -> List[Dict[str, Any]]:
    """
    联网查询工具，返回结构化数据，支持图片、原始内容、图片描述等参数。
    """
    tool = UnifiedSearchResultsWithImages(
        max_results=args.max_results,
        include_raw_content=args.include_raw_content,
        include_images=args.include_images,
        include_image_descriptions=args.include_image_descriptions,
        include_answer=args.include_answer,
        timeRange=args.timeRange,
        category=args.category,
        engineType=args.engineType,
    )
    results, _ = tool._run(args.query)
    return results
