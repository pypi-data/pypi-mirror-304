import os

import paperqa
import pytest
import requests

from pqapi import (
    AnswerResponse,
    QueryRequest,
    UploadMetadata,
    agent_query,
    async_agent_query,
    async_send_feedback,
    check_dois,
    delete_bibliography,
    get_bibliography,
    get_query_request,
    upload_file,
    upload_paper,
)


def test_bad_bibliography():
    with pytest.raises(requests.exceptions.HTTPError):
        get_bibliography("bad-bibliography")


@pytest.mark.parametrize(
    "query",
    [
        "How are bispecific antibodies engineered?",
        QueryRequest(query="How are bispecific antibodies engineered?"),
    ],
)
def test_agent_query(query: QueryRequest | str) -> None:
    response = agent_query(query, "default")
    assert isinstance(response, AnswerResponse)


def test_query_named_template():
    response = agent_query(
        "How are bispecific antibodies engineered?", named_template="hasanybodydone"
    )
    assert isinstance(response, AnswerResponse)


@pytest.mark.asyncio
async def test_get_query_request() -> None:
    assert isinstance(
        await get_query_request(name="better table parsing"), QueryRequest
    )


def test_query_obj():
    prompt_collection = paperqa.PromptCollection()
    prompt_collection.post = (
        "This answer below was generated for {cost}. "
        "Provide a critique of this answer that could be used to improve it.\n\n"
        "{question}\n\n{answer}"
    )
    request = QueryRequest(
        query="How are bispecific antibodies engineered?", group="foo"
    )
    agent_query(request)


def test_upload_file() -> None:
    script_dir = os.path.dirname(__file__)
    # pylint: disable-next=consider-using-with
    file = open(os.path.join(script_dir, "paper.pdf"), "rb")  # noqa: SIM115
    response = upload_file(
        "default",
        file,
        UploadMetadata(filename="paper.pdf", citation="Test Citation"),
    )
    assert response["success"], f"Expected success in response {response}."


@pytest.mark.skip(reason="This is no longer supported")
def test_upload_public() -> None:
    # create a public bibliography
    script_dir = os.path.dirname(__file__)
    # pylint: disable-next=consider-using-with
    file = open(os.path.join(script_dir, "paper.pdf"), "rb")  # noqa: SIM115
    response = upload_file(
        "api-test-public",
        file,
        UploadMetadata(filename="paper.pdf", citation="Test Citation"),
        public=True,
    )
    assert response["success"], f"Expected success in response {response}."

    # get status of public bibliography
    status = get_bibliography("api-test-public", public=True)

    assert status.writeable
    assert status.doc_count == 1

    # delete public bibliography
    delete_bibliography("api-test-public", public=True)


@pytest.mark.parametrize(
    "query",
    [
        "How are bispecific antibodies engineered?",
        QueryRequest(query="How are bispecific antibodies engineered?"),
    ],
)
@pytest.mark.asyncio
async def test_async_agent_query(query: QueryRequest | str) -> None:
    response = await async_agent_query(query, "default")
    assert isinstance(response, AnswerResponse)


@pytest.mark.asyncio
async def test_feedback_model() -> None:
    response = await async_agent_query(
        QueryRequest(query="How are bispecific antibodies engineered?"), "default"
    )
    assert isinstance(response, AnswerResponse)
    feedback = {"test_feedback": "great!"}
    assert (
        len(await async_send_feedback([response.answer.id], [feedback], "default")) == 1
    )


@pytest.mark.asyncio
async def test_async_tmp():
    response = await async_agent_query(
        QueryRequest(query="How are bispecific antibodies engineered?"),
    )
    assert isinstance(response, AnswerResponse)


def test_upload_paper() -> None:
    script_dir = os.path.dirname(__file__)
    # pylint: disable-next=consider-using-with
    file = open(os.path.join(script_dir, "paper.pdf"), "rb")  # noqa: SIM115
    upload_paper("10.1021/acs.jctc.2c01235", file)


def test_check_dois() -> None:
    response = check_dois(
        dois=[
            "10.1126/science.1240517",
            "10.1126/science.1240517",  # NOTE: duplicate input DOI
            "10.1016/j.febslet.2014.11.036",
        ]
    )
    assert response == {
        "10.1016/j.febslet.2014.11.036": ["c1433904691e17c2", "cached"],
        "10.1126/science.1240517": ["", "DOI not found"],
    }
