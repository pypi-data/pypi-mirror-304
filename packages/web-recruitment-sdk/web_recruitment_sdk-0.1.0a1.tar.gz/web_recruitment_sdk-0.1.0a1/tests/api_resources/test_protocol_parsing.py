# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from web_recruitment_sdk import WebRecruitmentSDK, AsyncWebRecruitmentSDK
from web_recruitment_sdk.types import (
    ProtocolParsingListResponse,
)
from web_recruitment_sdk.types.shared import ProtocolRead

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestProtocolParsing:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: WebRecruitmentSDK) -> None:
        protocol_parsing = client.protocol_parsing.create(
            file=b"raw file contents",
        )
        assert_matches_type(ProtocolRead, protocol_parsing, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: WebRecruitmentSDK) -> None:
        protocol_parsing = client.protocol_parsing.create(
            file=b"raw file contents",
            site_ids=[0, 0, 0],
            title="title",
        )
        assert_matches_type(ProtocolRead, protocol_parsing, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: WebRecruitmentSDK) -> None:
        response = client.protocol_parsing.with_raw_response.create(
            file=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        protocol_parsing = response.parse()
        assert_matches_type(ProtocolRead, protocol_parsing, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: WebRecruitmentSDK) -> None:
        with client.protocol_parsing.with_streaming_response.create(
            file=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            protocol_parsing = response.parse()
            assert_matches_type(ProtocolRead, protocol_parsing, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: WebRecruitmentSDK) -> None:
        protocol_parsing = client.protocol_parsing.list()
        assert_matches_type(ProtocolParsingListResponse, protocol_parsing, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: WebRecruitmentSDK) -> None:
        protocol_parsing = client.protocol_parsing.list(
            limit=1,
            offset=0,
        )
        assert_matches_type(ProtocolParsingListResponse, protocol_parsing, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: WebRecruitmentSDK) -> None:
        response = client.protocol_parsing.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        protocol_parsing = response.parse()
        assert_matches_type(ProtocolParsingListResponse, protocol_parsing, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: WebRecruitmentSDK) -> None:
        with client.protocol_parsing.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            protocol_parsing = response.parse()
            assert_matches_type(ProtocolParsingListResponse, protocol_parsing, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_error(self, client: WebRecruitmentSDK) -> None:
        protocol_parsing = client.protocol_parsing.error(
            tenant="tenant",
            job_id="job_id",
        )
        assert_matches_type(object, protocol_parsing, path=["response"])

    @parametrize
    def test_method_error_with_all_params(self, client: WebRecruitmentSDK) -> None:
        protocol_parsing = client.protocol_parsing.error(
            tenant="tenant",
            job_id="job_id",
            status_message="status_message",
        )
        assert_matches_type(object, protocol_parsing, path=["response"])

    @parametrize
    def test_raw_response_error(self, client: WebRecruitmentSDK) -> None:
        response = client.protocol_parsing.with_raw_response.error(
            tenant="tenant",
            job_id="job_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        protocol_parsing = response.parse()
        assert_matches_type(object, protocol_parsing, path=["response"])

    @parametrize
    def test_streaming_response_error(self, client: WebRecruitmentSDK) -> None:
        with client.protocol_parsing.with_streaming_response.error(
            tenant="tenant",
            job_id="job_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            protocol_parsing = response.parse()
            assert_matches_type(object, protocol_parsing, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_error(self, client: WebRecruitmentSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            client.protocol_parsing.with_raw_response.error(
                tenant="tenant",
                job_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tenant` but received ''"):
            client.protocol_parsing.with_raw_response.error(
                tenant="",
                job_id="job_id",
            )

    @parametrize
    def test_method_success(self, client: WebRecruitmentSDK) -> None:
        protocol_parsing = client.protocol_parsing.success(
            tenant="tenant",
            job_id="job_id",
            body=[
                {
                    "protocol_id": 0,
                    "summary": "summary",
                    "type": "inclusion",
                },
                {
                    "protocol_id": 0,
                    "summary": "summary",
                    "type": "inclusion",
                },
                {
                    "protocol_id": 0,
                    "summary": "summary",
                    "type": "inclusion",
                },
            ],
        )
        assert_matches_type(object, protocol_parsing, path=["response"])

    @parametrize
    def test_raw_response_success(self, client: WebRecruitmentSDK) -> None:
        response = client.protocol_parsing.with_raw_response.success(
            tenant="tenant",
            job_id="job_id",
            body=[
                {
                    "protocol_id": 0,
                    "summary": "summary",
                    "type": "inclusion",
                },
                {
                    "protocol_id": 0,
                    "summary": "summary",
                    "type": "inclusion",
                },
                {
                    "protocol_id": 0,
                    "summary": "summary",
                    "type": "inclusion",
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        protocol_parsing = response.parse()
        assert_matches_type(object, protocol_parsing, path=["response"])

    @parametrize
    def test_streaming_response_success(self, client: WebRecruitmentSDK) -> None:
        with client.protocol_parsing.with_streaming_response.success(
            tenant="tenant",
            job_id="job_id",
            body=[
                {
                    "protocol_id": 0,
                    "summary": "summary",
                    "type": "inclusion",
                },
                {
                    "protocol_id": 0,
                    "summary": "summary",
                    "type": "inclusion",
                },
                {
                    "protocol_id": 0,
                    "summary": "summary",
                    "type": "inclusion",
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            protocol_parsing = response.parse()
            assert_matches_type(object, protocol_parsing, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_success(self, client: WebRecruitmentSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            client.protocol_parsing.with_raw_response.success(
                tenant="tenant",
                job_id="",
                body=[
                    {
                        "protocol_id": 0,
                        "summary": "summary",
                        "type": "inclusion",
                    },
                    {
                        "protocol_id": 0,
                        "summary": "summary",
                        "type": "inclusion",
                    },
                    {
                        "protocol_id": 0,
                        "summary": "summary",
                        "type": "inclusion",
                    },
                ],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tenant` but received ''"):
            client.protocol_parsing.with_raw_response.success(
                tenant="",
                job_id="job_id",
                body=[
                    {
                        "protocol_id": 0,
                        "summary": "summary",
                        "type": "inclusion",
                    },
                    {
                        "protocol_id": 0,
                        "summary": "summary",
                        "type": "inclusion",
                    },
                    {
                        "protocol_id": 0,
                        "summary": "summary",
                        "type": "inclusion",
                    },
                ],
            )


class TestAsyncProtocolParsing:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncWebRecruitmentSDK) -> None:
        protocol_parsing = await async_client.protocol_parsing.create(
            file=b"raw file contents",
        )
        assert_matches_type(ProtocolRead, protocol_parsing, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncWebRecruitmentSDK) -> None:
        protocol_parsing = await async_client.protocol_parsing.create(
            file=b"raw file contents",
            site_ids=[0, 0, 0],
            title="title",
        )
        assert_matches_type(ProtocolRead, protocol_parsing, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncWebRecruitmentSDK) -> None:
        response = await async_client.protocol_parsing.with_raw_response.create(
            file=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        protocol_parsing = await response.parse()
        assert_matches_type(ProtocolRead, protocol_parsing, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncWebRecruitmentSDK) -> None:
        async with async_client.protocol_parsing.with_streaming_response.create(
            file=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            protocol_parsing = await response.parse()
            assert_matches_type(ProtocolRead, protocol_parsing, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncWebRecruitmentSDK) -> None:
        protocol_parsing = await async_client.protocol_parsing.list()
        assert_matches_type(ProtocolParsingListResponse, protocol_parsing, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncWebRecruitmentSDK) -> None:
        protocol_parsing = await async_client.protocol_parsing.list(
            limit=1,
            offset=0,
        )
        assert_matches_type(ProtocolParsingListResponse, protocol_parsing, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncWebRecruitmentSDK) -> None:
        response = await async_client.protocol_parsing.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        protocol_parsing = await response.parse()
        assert_matches_type(ProtocolParsingListResponse, protocol_parsing, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncWebRecruitmentSDK) -> None:
        async with async_client.protocol_parsing.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            protocol_parsing = await response.parse()
            assert_matches_type(ProtocolParsingListResponse, protocol_parsing, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_error(self, async_client: AsyncWebRecruitmentSDK) -> None:
        protocol_parsing = await async_client.protocol_parsing.error(
            tenant="tenant",
            job_id="job_id",
        )
        assert_matches_type(object, protocol_parsing, path=["response"])

    @parametrize
    async def test_method_error_with_all_params(self, async_client: AsyncWebRecruitmentSDK) -> None:
        protocol_parsing = await async_client.protocol_parsing.error(
            tenant="tenant",
            job_id="job_id",
            status_message="status_message",
        )
        assert_matches_type(object, protocol_parsing, path=["response"])

    @parametrize
    async def test_raw_response_error(self, async_client: AsyncWebRecruitmentSDK) -> None:
        response = await async_client.protocol_parsing.with_raw_response.error(
            tenant="tenant",
            job_id="job_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        protocol_parsing = await response.parse()
        assert_matches_type(object, protocol_parsing, path=["response"])

    @parametrize
    async def test_streaming_response_error(self, async_client: AsyncWebRecruitmentSDK) -> None:
        async with async_client.protocol_parsing.with_streaming_response.error(
            tenant="tenant",
            job_id="job_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            protocol_parsing = await response.parse()
            assert_matches_type(object, protocol_parsing, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_error(self, async_client: AsyncWebRecruitmentSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            await async_client.protocol_parsing.with_raw_response.error(
                tenant="tenant",
                job_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tenant` but received ''"):
            await async_client.protocol_parsing.with_raw_response.error(
                tenant="",
                job_id="job_id",
            )

    @parametrize
    async def test_method_success(self, async_client: AsyncWebRecruitmentSDK) -> None:
        protocol_parsing = await async_client.protocol_parsing.success(
            tenant="tenant",
            job_id="job_id",
            body=[
                {
                    "protocol_id": 0,
                    "summary": "summary",
                    "type": "inclusion",
                },
                {
                    "protocol_id": 0,
                    "summary": "summary",
                    "type": "inclusion",
                },
                {
                    "protocol_id": 0,
                    "summary": "summary",
                    "type": "inclusion",
                },
            ],
        )
        assert_matches_type(object, protocol_parsing, path=["response"])

    @parametrize
    async def test_raw_response_success(self, async_client: AsyncWebRecruitmentSDK) -> None:
        response = await async_client.protocol_parsing.with_raw_response.success(
            tenant="tenant",
            job_id="job_id",
            body=[
                {
                    "protocol_id": 0,
                    "summary": "summary",
                    "type": "inclusion",
                },
                {
                    "protocol_id": 0,
                    "summary": "summary",
                    "type": "inclusion",
                },
                {
                    "protocol_id": 0,
                    "summary": "summary",
                    "type": "inclusion",
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        protocol_parsing = await response.parse()
        assert_matches_type(object, protocol_parsing, path=["response"])

    @parametrize
    async def test_streaming_response_success(self, async_client: AsyncWebRecruitmentSDK) -> None:
        async with async_client.protocol_parsing.with_streaming_response.success(
            tenant="tenant",
            job_id="job_id",
            body=[
                {
                    "protocol_id": 0,
                    "summary": "summary",
                    "type": "inclusion",
                },
                {
                    "protocol_id": 0,
                    "summary": "summary",
                    "type": "inclusion",
                },
                {
                    "protocol_id": 0,
                    "summary": "summary",
                    "type": "inclusion",
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            protocol_parsing = await response.parse()
            assert_matches_type(object, protocol_parsing, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_success(self, async_client: AsyncWebRecruitmentSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            await async_client.protocol_parsing.with_raw_response.success(
                tenant="tenant",
                job_id="",
                body=[
                    {
                        "protocol_id": 0,
                        "summary": "summary",
                        "type": "inclusion",
                    },
                    {
                        "protocol_id": 0,
                        "summary": "summary",
                        "type": "inclusion",
                    },
                    {
                        "protocol_id": 0,
                        "summary": "summary",
                        "type": "inclusion",
                    },
                ],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tenant` but received ''"):
            await async_client.protocol_parsing.with_raw_response.success(
                tenant="",
                job_id="job_id",
                body=[
                    {
                        "protocol_id": 0,
                        "summary": "summary",
                        "type": "inclusion",
                    },
                    {
                        "protocol_id": 0,
                        "summary": "summary",
                        "type": "inclusion",
                    },
                    {
                        "protocol_id": 0,
                        "summary": "summary",
                        "type": "inclusion",
                    },
                ],
            )
