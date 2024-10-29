"""Types for the Fixpoint client and its APIs."""

__all__ = [
    "AllResearchResultsPydantic",
    "BatchTextSource",
    "Citation",
    "CrawlUrlSource",
    "CreateHumanTaskEntryRequest",
    "CreateJsonSchemaExtractionRequest",
    "CreateQuestionAnswerRecordExtractionRequest",
    "CreateResearchRecordRequest",
    "CreateSimpleCrawlUrlParseRequest",
    "CreateSimpleWebpageParseRequest",
    "Document",
    "HumanTaskEntry",
    "JsonSchemaExtraction",
    "JsonSchemaExtractionTask",
    "ListDocumentsResponse",
    "ListHumanTaskEntriesResponse",
    "ListResearchRecordsResponse",
    "NodeStatus",
    "QuestionAnswerRecordExtraction",
    "QuestionAnswerRecordExtractionTask",
    "ResearchField",
    "ResearchFieldEditableConfig",
    "ResearchRecord",
    "SimpleCrawlUrlParseResult",
    "SimpleWebpageParseResult",
    "TaskEntryField",
    "TaskFieldEditableConfig",
    "TextCitation",
    "TextSource",
    "WebPageCitation",
    "WebpageSource",
]

from fixpoint_common.types import Document, ListDocumentsResponse, NodeStatus
from fixpoint_common.types.human import (
    HumanTaskEntry,
    CreateHumanTaskEntryRequest,
    EntryField as TaskEntryField,
    EditableConfig as TaskFieldEditableConfig,
    ListHumanTaskEntriesResponse,
)
from fixpoint_common.types.research import (
    ResearchRecord,
    ResearchField,
    CreateResearchRecordRequest,
    ListResearchRecordsResponse,
    EditableConfig as ResearchFieldEditableConfig,
)
from fixpoint_common.webresearcher.types import AllResearchResultsPydantic
from fixpoint_common.types.extraction import (
    CreateJsonSchemaExtractionRequest,
    CreateQuestionAnswerRecordExtractionRequest,
    JsonSchemaExtraction,
    JsonSchemaExtractionTask,
    QuestionAnswerRecordExtraction,
    QuestionAnswerRecordExtractionTask,
)
from fixpoint_common.types.parsing import (
    CreateSimpleCrawlUrlParseRequest,
    CreateSimpleWebpageParseRequest,
    SimpleCrawlUrlParseResult,
    SimpleWebpageParseResult,
)
from fixpoint_common.types.sources import (
    TextSource,
    WebpageSource,
    CrawlUrlSource,
    BatchTextSource,
)
from fixpoint_common.types.citations import Citation, TextCitation, WebPageCitation
