"""Types for extraction requests and responses."""

__all__ = [
    "CreateExtractionRequest",
    "CreateJsonSchemaExtractionRequest",
    "CreateQuestionAnswerRecordExtractionRequest",
    "JsonSchemaExtraction",
    "JsonSchemaExtractionTask",
    "QuestionAnswerRecordExtraction",
    "QuestionAnswerRecordExtractionTask",
]

from typing import Optional, Union, Literal, Dict, Any, List

from openai.types.completion_usage import CompletionUsage
from pydantic import BaseModel, Field

from fixpoint_common.completions import ChatCompletionMessageParam
from .citations import Citation
from .research import ResearchRecord
from .sources import TextSource, WebpageSource, CrawlUrlSource, BatchTextSource
from .workflow import WorkflowId, WorkflowRunId


class JsonSchemaExtractionTask(BaseModel):
    """Extract data according to a plain JSON schema"""

    kind: Literal["json_schema"] = Field(
        description="The type of extraction task.", default="json_schema"
    )
    # we can't name this "schema" because that's a reserved by Pydantic
    extraction_schema: Dict[str, Any] = Field(
        description="The JSON schema for the extraction results",
        min_length=1,
    )
    extra_instructions: Optional[List[ChatCompletionMessageParam]] = Field(
        description="Additional instruction messages to prepend to the prompt",
        default=None,
    )


class QuestionAnswerRecordExtractionTask(BaseModel):
    """Extract data in a tabular format as a research record"""

    questions: List[str] = Field(description="The questions to answer.")


class CreateExtractionRequest(BaseModel):
    """Request to create an extraction from a data source."""

    source: Union[TextSource, WebpageSource] = Field(
        description="The source of the data to extract."
    )
    extraction_task: Union[
        JsonSchemaExtractionTask, QuestionAnswerRecordExtractionTask
    ] = Field(description="The extraction task to perform on the data source.")

    workflow_id: WorkflowId
    run_id: WorkflowRunId


class CreateJsonSchemaExtractionRequest(BaseModel):
    """Request to create a JSON schema extraction."""

    source: Union[TextSource, WebpageSource] = Field(
        description="The source of the data to extract."
    )
    extraction_task: JsonSchemaExtractionTask = Field(
        description="The extraction task to perform on the data source."
    )

    workflow_id: WorkflowId
    run_id: WorkflowRunId


class CreateQuestionAnswerRecordExtractionRequest(BaseModel):
    """Request to create Record Q&A extraction."""

    workflow_id: WorkflowId
    run_id: WorkflowRunId

    source: Union[
        CrawlUrlSource,
        WebpageSource,
        TextSource,
        BatchTextSource,
    ] = Field(description="The source of the data to extract.")

    extraction_task: QuestionAnswerRecordExtractionTask = Field(
        description="The extraction task to perform on the data source."
    )


class JsonSchemaExtraction(BaseModel):
    """Extraction result from a JSON schema extraction."""

    result: Dict[str, Any] = Field(description="The extraction result.")
    citations: List[Citation] = Field(
        description="The citations for the extraction result."
    )
    completion_usage: Optional[CompletionUsage] = Field(
        description="The completion usage for the extraction.",
        default=None,
    )


class QuestionAnswerRecordExtraction(BaseModel):
    """Extraction result from a question and answer record extraction."""

    result_record: ResearchRecord = Field(
        description="The research record containing the extracted data."
    )
    citations: List[Citation] = Field(
        description="The citations for the extraction result."
    )
    sub_json_extractions: List[JsonSchemaExtraction] = Field(
        description="The sub-extractions that resulted in this extraction."
    )
