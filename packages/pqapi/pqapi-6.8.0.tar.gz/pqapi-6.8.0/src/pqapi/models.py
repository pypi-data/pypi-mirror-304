import re
from enum import Enum
from typing import Any

import paperqa
from paperqa.types import PromptCollection
from pydantic import BaseModel, Field, ValidationInfo, field_validator, validator


def _extract_doi(citation: str) -> str | None:
    doi = re.findall(r"10\.\d{4}/\S+", citation, re.IGNORECASE)
    return doi[-1] if doi else None


class UploadMetadata(BaseModel):
    filename: str
    citation: str
    key: str | None = None


class Doc(paperqa.Doc):
    doi: str | None = None

    @validator("doi", pre=True)
    def citation_to_doi(cls, v: str | None, values: dict) -> str | None:  # noqa: N805
        if v is None and "citation" in values:
            return _extract_doi(values["citation"])
        return v


class DocsStatus(BaseModel):
    name: str
    llm: str
    summary_llm: str
    docs: list[Doc]
    doc_count: int
    writeable: bool = False


class QueryRequestMinimal(BaseModel):
    """A subset of the fields in the QueryRequest model."""

    query: str = Field(description="The query to be answered")
    group: str | None = Field(None, description="A way to group queries together")
    named_template: str | None = Field(
        None,
        description="The template to be applied (if any) to the query for settings things like models, chunksize, etc.",
    )


# COPIED FROM paperqa-server!
class ParsingOptions(str, Enum):
    S2ORC = "s2orc"
    PAPERQA_DEFAULT = "paperqa_default"
    GROBID = "grobid"


class ChunkingOptions(str, Enum):
    SIMPLE_OVERLAP = "simple_overlap"
    SECTIONS = "sections"


class AgentStatus(str, Enum):
    # FAIL - no answer could be generated
    FAIL = "fail"
    # SUCCESS - answer was generated
    SUCCESS = "success"
    # TIMEOUT - agent took too long, but an answer was generated
    TIMEOUT = "timeout"
    # UNSURE - the agent was unsure, but an answer is present
    UNSURE = "unsure"
    # INITIALIZED - the agent has started, but no answer is present
    INITIALIZED = "initialized"
    # IN_PROGRESS - the agent has provided an incomplete answer, still processing to the final result
    IN_PROGRESS = "in progress"


class AgentPromptCollection(BaseModel):
    agent_system_prompt: str | None = "You are a helpful AI assistant."
    agent_prompt: str = (
        "Use the tools to answer the question: {question}"
        "\n\nThe {gen_answer_tool_name} tool output is visible to the user, "
        "so you do not need to restate the answer and can simply terminate if the answer looks sufficient. "
        "The current status of evidence/papers/cost is {status}"
    )
    search_count: int = 8
    search_min_year: int | None = None
    search_max_year: int | None = None
    wipe_context_on_answer_failure: bool = True
    timeout: float = 500
    should_pre_search: bool = False
    papers_from_evidence_citations_config: dict[str, Any] | None = None
    agent_config: dict[str, Any] | None = None
    tool_names: set[str] | list[str] | None = None
    websockets_to_gcs_config: dict[str, str | bool] | None = None


class ParsingConfiguration(BaseModel):
    ordered_parser_preferences: list[ParsingOptions] = [
        ParsingOptions.S2ORC,
        ParsingOptions.PAPERQA_DEFAULT,
    ]
    chunksize: int = 6000
    overlap: int = 100
    chunking_algorithm: ChunkingOptions = ChunkingOptions.SIMPLE_OVERLAP
    gcs_parsing_prefix: str = "parsings"
    gcs_raw_prefix: str = "raw_files"


class QueryRequest(BaseModel):
    query: str = ""
    group: str | None = None
    named_template: str | None = None
    agent_llm: str = "gpt-4o-2024-08-06"
    llm: str = "gpt-4-turbo-2024-04-09"
    summary_llm: str = "gpt-4-turbo-2024-04-09"
    length: str = "about 200 words, but can be longer if necessary"
    summary_length: str = "about 100 words"
    max_sources: int = 10
    consider_sources: int = 16
    # if you change this to something other than default
    # modify code below in update_prompts
    prompts: PromptCollection = Field(default_factory=PromptCollection)
    agent_tools: AgentPromptCollection = Field(default_factory=AgentPromptCollection)
    texts_index_mmr_lambda: float = 1.0
    texts_index_embedding_config: dict[str, Any] | None = None
    docs_index_mmr_lambda: float = 0.5
    docs_index_embedding_config: dict[str, Any] | None = None
    parsing_configuration: ParsingConfiguration = Field(
        default_factory=ParsingConfiguration
    )
    embedding: str = "hybrid-text-embedding-3-small"
    max_concurrent: int = 20
    temperature: float = 0.0
    summary_temperature: float = 0.0
    adoc_match_threshold: int = 500
    filter_extra_background: bool = True

    @field_validator("prompts")
    def treat_summary_llm_none(
        cls,  # noqa: N805
        v: PromptCollection,
        info: ValidationInfo,
    ) -> PromptCollection:
        values = info.data
        if values["summary_llm"] == "none":
            v.skip_summary = True
            # for simplicity (it is not used anywhere)
            # so that Docs doesn't break when we don't have a summary_llm
            values["summary_llm"] = "gpt-3.5-turbo"
        return v


class UserModel(BaseModel):
    email: str
    full_name: str
    disabled: bool = False
    verified: bool = False
    roles: str = Field(
        default="user",
        description="roles delimied with ':', valid roles include 'user', 'admin', and 'api'.",
    )


class ScrapeStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    BLOCKLIST = "blocklist"
    IN_PROGRESS = "none"
    DUPLICATE = "duplicate"
    PARSED = "parsed"
    PENDING = "pending"


class PaperDetails(BaseModel):
    """A subset of the fields in the PaperDetails model."""

    citation: str | None = None
    year: int | None = None
    url: str | None = Field(
        default=None,
        description=(
            "Optional URL to the paper, which can lead to a Semantic Scholar page,"
            " arXiv abstract, etc. As of version 0.67 on 5/10/2024, we don't use this"
            " URL anywhere in the source code."
        ),
    )
    title: str | None = None
    doi: str | None = None
    paperId: str | None = None  # noqa: N815
    other: dict[str, Any] = Field(
        default_factory=dict,
        description="Other metadata besides the above standardized fields.",
    )

    def __getitem__(self, item: str):
        """Allow for dictionary-like access, falling back on other."""
        try:
            return getattr(self, item)
        except AttributeError:
            return self.other[item]
