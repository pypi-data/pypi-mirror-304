"""
Types for parsing web pages and other data sources into an LLM-ready format.
"""

__all__ = [
    "CreateSimpleWebpageParseRequest",
    "SimpleWebpageParseResult",
    "CreateSimpleCrawlUrlParseRequest",
    "SimpleCrawlUrlParseResult",
]


from typing import List, Optional

from pydantic import BaseModel, Field

from .sources import WebpageSource, CrawlUrlSource
from .workflow import WorkflowId, WorkflowRunId


class CreateSimpleWebpageParseRequest(BaseModel):
    """Request to parse a single webpage.

    Parses a webpage and returns the text (non-chunked) of the page.
    """

    source: WebpageSource
    workflow_id: WorkflowId
    run_id: Optional[WorkflowRunId]


# Parse results are called `...ParseResult` instead of `...Parse` because if we
# have a plain `CreateParseRequest`, returning a `Parse` object is confusing
# about whether that is a verb or a noun.


class SimpleWebpageParseResult(BaseModel):
    """A parse result from a single webpage.

    Contains the text (non-chunked) of the page.
    """

    source: WebpageSource
    content: str = Field(description="The parsed text, ready for LLM")


class CreateSimpleCrawlUrlParseRequest(BaseModel):
    """Request to start a simple crawl parse.

    Crawls webpages starting at a URL. Returns the text (non-chunked) per page.
    """

    source: CrawlUrlSource
    workflow_id: WorkflowId
    run_id: Optional[WorkflowRunId]


class SimpleCrawlUrlParseResult(BaseModel):
    """A parse result from crawling a URL.

    Contains the text (non-chunked) per page.
    """

    source: CrawlUrlSource
    page_contents: List[SimpleWebpageParseResult] = Field(
        description="The parsed contents of each page"
    )
