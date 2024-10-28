# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

import itertools
import os

import pytest
import pytest_asyncio

from pydantic import BaseModel, ValidationError

from llama_models.llama3.api.datatypes import *  # noqa: F403
from llama_stack.apis.inference import *  # noqa: F403

from llama_stack.distribution.datatypes import *  # noqa: F403
from llama_stack.providers.tests.resolver import resolve_impls_for_test

# How to run this test:
#
# 1. Ensure you have a conda with the right dependencies installed. This is a bit tricky
#    since it depends on the provider you are testing. On top of that you need
#    `pytest` and `pytest-asyncio` installed.
#
# 2. Copy and modify the provider_config_example.yaml depending on the provider you are testing.
#
# 3. Run:
#
# ```bash
# PROVIDER_ID=<your_provider> \
#   PROVIDER_CONFIG=provider_config.yaml \
#   pytest -s llama_stack/providers/tests/inference/test_inference.py \
#   --tb=short --disable-warnings
# ```


def group_chunks(response):
    return {
        event_type: list(group)
        for event_type, group in itertools.groupby(
            response, key=lambda chunk: chunk.event.event_type
        )
    }


Llama_8B = "Llama3.1-8B-Instruct"
Llama_3B = "Llama3.2-3B-Instruct"


def get_expected_stop_reason(model: str):
    return StopReason.end_of_message if "Llama3.1" in model else StopReason.end_of_turn


if "MODEL_IDS" not in os.environ:
    MODEL_IDS = [Llama_8B, Llama_3B]
else:
    MODEL_IDS = os.environ["MODEL_IDS"].split(",")


# This is going to create multiple Stack impls without tearing down the previous one
# Fix that!
@pytest_asyncio.fixture(
    scope="session",
    params=[{"model": m} for m in MODEL_IDS],
    ids=lambda d: d["model"],
)
async def inference_settings(request):
    model = request.param["model"]
    impls = await resolve_impls_for_test(
        Api.inference,
    )

    return {
        "impl": impls[Api.inference],
        "models_impl": impls[Api.models],
        "common_params": {
            "model": model,
            "tool_choice": ToolChoice.auto,
            "tool_prompt_format": (
                ToolPromptFormat.json
                if "Llama3.1" in model
                else ToolPromptFormat.python_list
            ),
        },
    }


@pytest.fixture
def sample_messages():
    return [
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="What's the weather like today?"),
    ]


@pytest.fixture
def sample_tool_definition():
    return ToolDefinition(
        tool_name="get_weather",
        description="Get the current weather",
        parameters={
            "location": ToolParamDefinition(
                param_type="string",
                description="The city and state, e.g. San Francisco, CA",
            ),
        },
    )


@pytest.mark.asyncio
async def test_model_list(inference_settings):
    params = inference_settings["common_params"]
    models_impl = inference_settings["models_impl"]
    response = await models_impl.list_models()
    assert isinstance(response, list)
    assert len(response) >= 1
    assert all(isinstance(model, ModelDefWithProvider) for model in response)

    model_def = None
    for model in response:
        if model.identifier == params["model"]:
            model_def = model
            break

    assert model_def is not None
    assert model_def.identifier == params["model"]


@pytest.mark.asyncio
async def test_completion(inference_settings):
    inference_impl = inference_settings["impl"]
    params = inference_settings["common_params"]

    provider = inference_impl.routing_table.get_provider_impl(params["model"])
    if provider.__provider_spec__.provider_type not in (
        "meta-reference",
        "remote::ollama",
        "remote::tgi",
    ):
        pytest.skip("Other inference providers don't support completion() yet")

    response = await inference_impl.completion(
        content="Roses are red,",
        stream=False,
        model=params["model"],
        sampling_params=SamplingParams(
            max_tokens=50,
        ),
    )

    assert isinstance(response, CompletionResponse)
    assert "violets are blue" in response.content

    chunks = [
        r
        async for r in await inference_impl.completion(
            content="Roses are red,",
            stream=True,
            model=params["model"],
            sampling_params=SamplingParams(
                max_tokens=50,
            ),
        )
    ]

    assert all(isinstance(chunk, CompletionResponseStreamChunk) for chunk in chunks)
    assert len(chunks) == 51
    last = chunks[-1]
    assert last.stop_reason == StopReason.out_of_tokens


@pytest.mark.asyncio
async def test_completions_structured_output(inference_settings):
    inference_impl = inference_settings["impl"]
    params = inference_settings["common_params"]

    provider = inference_impl.routing_table.get_provider_impl(params["model"])
    if provider.__provider_spec__.provider_type not in (
        "meta-reference",
        "remote::tgi",
    ):
        pytest.skip(
            "Other inference providers don't support structured output in completions yet"
        )

    class Output(BaseModel):
        name: str
        year_born: str
        year_retired: str

    user_input = "Michael Jordan was born in 1963. He played basketball for the Chicago Bulls. He retired in 2003."
    response = await inference_impl.completion(
        content=f"input: '{user_input}'. the schema for json: {Output.schema()}, the json is: ",
        stream=False,
        model=params["model"],
        sampling_params=SamplingParams(
            max_tokens=50,
        ),
        response_format=JsonResponseFormat(
            schema=Output.model_json_schema(),
        ),
    )
    assert isinstance(response, CompletionResponse)
    assert isinstance(response.content, str)

    answer = Output.parse_raw(response.content)
    assert answer.name == "Michael Jordan"
    assert answer.year_born == "1963"
    assert answer.year_retired == "2003"


@pytest.mark.asyncio
async def test_chat_completion_non_streaming(inference_settings, sample_messages):
    inference_impl = inference_settings["impl"]
    response = await inference_impl.chat_completion(
        messages=sample_messages,
        stream=False,
        **inference_settings["common_params"],
    )

    assert isinstance(response, ChatCompletionResponse)
    assert response.completion_message.role == "assistant"
    assert isinstance(response.completion_message.content, str)
    assert len(response.completion_message.content) > 0


@pytest.mark.asyncio
async def test_structured_output(inference_settings):
    inference_impl = inference_settings["impl"]
    params = inference_settings["common_params"]

    provider = inference_impl.routing_table.get_provider_impl(params["model"])
    if provider.__provider_spec__.provider_type not in (
        "meta-reference",
        "remote::fireworks",
        "remote::tgi",
        "remote::together",
    ):
        pytest.skip("Other inference providers don't support structured output yet")

    class AnswerFormat(BaseModel):
        first_name: str
        last_name: str
        year_of_birth: int
        num_seasons_in_nba: int

    response = await inference_impl.chat_completion(
        messages=[
            SystemMessage(content="You are a helpful assistant."),
            UserMessage(content="Please give me information about Michael Jordan."),
        ],
        stream=False,
        response_format=JsonResponseFormat(
            schema=AnswerFormat.model_json_schema(),
        ),
        **inference_settings["common_params"],
    )

    assert isinstance(response, ChatCompletionResponse)
    assert response.completion_message.role == "assistant"
    assert isinstance(response.completion_message.content, str)

    answer = AnswerFormat.parse_raw(response.completion_message.content)
    assert answer.first_name == "Michael"
    assert answer.last_name == "Jordan"
    assert answer.year_of_birth == 1963
    assert answer.num_seasons_in_nba == 15

    response = await inference_impl.chat_completion(
        messages=[
            SystemMessage(content="You are a helpful assistant."),
            UserMessage(content="Please give me information about Michael Jordan."),
        ],
        stream=False,
        **inference_settings["common_params"],
    )

    assert isinstance(response, ChatCompletionResponse)
    assert isinstance(response.completion_message.content, str)

    with pytest.raises(ValidationError):
        AnswerFormat.parse_raw(response.completion_message.content)


@pytest.mark.asyncio
async def test_chat_completion_streaming(inference_settings, sample_messages):
    inference_impl = inference_settings["impl"]
    response = [
        r
        async for r in await inference_impl.chat_completion(
            messages=sample_messages,
            stream=True,
            **inference_settings["common_params"],
        )
    ]

    assert len(response) > 0
    assert all(
        isinstance(chunk, ChatCompletionResponseStreamChunk) for chunk in response
    )
    grouped = group_chunks(response)
    assert len(grouped[ChatCompletionResponseEventType.start]) == 1
    assert len(grouped[ChatCompletionResponseEventType.progress]) > 0
    assert len(grouped[ChatCompletionResponseEventType.complete]) == 1

    end = grouped[ChatCompletionResponseEventType.complete][0]
    assert end.event.stop_reason == StopReason.end_of_turn


@pytest.mark.asyncio
async def test_chat_completion_with_tool_calling(
    inference_settings,
    sample_messages,
    sample_tool_definition,
):
    inference_impl = inference_settings["impl"]
    messages = sample_messages + [
        UserMessage(
            content="What's the weather like in San Francisco?",
        )
    ]

    response = await inference_impl.chat_completion(
        messages=messages,
        tools=[sample_tool_definition],
        stream=False,
        **inference_settings["common_params"],
    )

    assert isinstance(response, ChatCompletionResponse)

    message = response.completion_message

    # This is not supported in most providers :/ they don't return eom_id / eot_id
    # stop_reason = get_expected_stop_reason(inference_settings["common_params"]["model"])
    # assert message.stop_reason == stop_reason
    assert message.tool_calls is not None
    assert len(message.tool_calls) > 0

    call = message.tool_calls[0]
    assert call.tool_name == "get_weather"
    assert "location" in call.arguments
    assert "San Francisco" in call.arguments["location"]


@pytest.mark.asyncio
async def test_chat_completion_with_tool_calling_streaming(
    inference_settings,
    sample_messages,
    sample_tool_definition,
):
    inference_impl = inference_settings["impl"]
    messages = sample_messages + [
        UserMessage(
            content="What's the weather like in San Francisco?",
        )
    ]

    response = [
        r
        async for r in await inference_impl.chat_completion(
            messages=messages,
            tools=[sample_tool_definition],
            stream=True,
            **inference_settings["common_params"],
        )
    ]

    assert len(response) > 0
    assert all(
        isinstance(chunk, ChatCompletionResponseStreamChunk) for chunk in response
    )
    grouped = group_chunks(response)
    assert len(grouped[ChatCompletionResponseEventType.start]) == 1
    assert len(grouped[ChatCompletionResponseEventType.progress]) > 0
    assert len(grouped[ChatCompletionResponseEventType.complete]) == 1

    # This is not supported in most providers :/ they don't return eom_id / eot_id
    # expected_stop_reason = get_expected_stop_reason(
    #     inference_settings["common_params"]["model"]
    # )
    # end = grouped[ChatCompletionResponseEventType.complete][0]
    # assert end.event.stop_reason == expected_stop_reason

    model = inference_settings["common_params"]["model"]
    if "Llama3.1" in model:
        assert all(
            isinstance(chunk.event.delta, ToolCallDelta)
            for chunk in grouped[ChatCompletionResponseEventType.progress]
        )
        first = grouped[ChatCompletionResponseEventType.progress][0]
        assert first.event.delta.parse_status == ToolCallParseStatus.started

    last = grouped[ChatCompletionResponseEventType.progress][-1]
    # assert last.event.stop_reason == expected_stop_reason
    assert last.event.delta.parse_status == ToolCallParseStatus.success
    assert isinstance(last.event.delta.content, ToolCall)

    call = last.event.delta.content
    assert call.tool_name == "get_weather"
    assert "location" in call.arguments
    assert "San Francisco" in call.arguments["location"]
