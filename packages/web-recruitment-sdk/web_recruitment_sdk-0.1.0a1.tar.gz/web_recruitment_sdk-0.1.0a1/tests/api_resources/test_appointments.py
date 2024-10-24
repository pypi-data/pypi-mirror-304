# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from web_recruitment_sdk import WebRecruitmentSDK, AsyncWebRecruitmentSDK
from web_recruitment_sdk.types import (
    AppointmentRead,
    AppointmentBulkResponse,
    AppointmentListResponse,
)
from web_recruitment_sdk._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAppointments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: WebRecruitmentSDK) -> None:
        appointment = client.appointments.create(
            date=parse_datetime("2019-12-27T18:11:19.117Z"),
            patient_id=0,
        )
        assert_matches_type(AppointmentRead, appointment, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: WebRecruitmentSDK) -> None:
        response = client.appointments.with_raw_response.create(
            date=parse_datetime("2019-12-27T18:11:19.117Z"),
            patient_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        appointment = response.parse()
        assert_matches_type(AppointmentRead, appointment, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: WebRecruitmentSDK) -> None:
        with client.appointments.with_streaming_response.create(
            date=parse_datetime("2019-12-27T18:11:19.117Z"),
            patient_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            appointment = response.parse()
            assert_matches_type(AppointmentRead, appointment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: WebRecruitmentSDK) -> None:
        appointment = client.appointments.retrieve(
            0,
        )
        assert_matches_type(AppointmentRead, appointment, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: WebRecruitmentSDK) -> None:
        response = client.appointments.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        appointment = response.parse()
        assert_matches_type(AppointmentRead, appointment, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: WebRecruitmentSDK) -> None:
        with client.appointments.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            appointment = response.parse()
            assert_matches_type(AppointmentRead, appointment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update(self, client: WebRecruitmentSDK) -> None:
        appointment = client.appointments.update(
            appointment_id=0,
            date=parse_datetime("2019-12-27T18:11:19.117Z"),
            patient_id=0,
        )
        assert_matches_type(AppointmentRead, appointment, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: WebRecruitmentSDK) -> None:
        response = client.appointments.with_raw_response.update(
            appointment_id=0,
            date=parse_datetime("2019-12-27T18:11:19.117Z"),
            patient_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        appointment = response.parse()
        assert_matches_type(AppointmentRead, appointment, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: WebRecruitmentSDK) -> None:
        with client.appointments.with_streaming_response.update(
            appointment_id=0,
            date=parse_datetime("2019-12-27T18:11:19.117Z"),
            patient_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            appointment = response.parse()
            assert_matches_type(AppointmentRead, appointment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: WebRecruitmentSDK) -> None:
        appointment = client.appointments.list()
        assert_matches_type(AppointmentListResponse, appointment, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: WebRecruitmentSDK) -> None:
        appointment = client.appointments.list(
            limit=0,
        )
        assert_matches_type(AppointmentListResponse, appointment, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: WebRecruitmentSDK) -> None:
        response = client.appointments.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        appointment = response.parse()
        assert_matches_type(AppointmentListResponse, appointment, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: WebRecruitmentSDK) -> None:
        with client.appointments.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            appointment = response.parse()
            assert_matches_type(AppointmentListResponse, appointment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: WebRecruitmentSDK) -> None:
        appointment = client.appointments.delete(
            0,
        )
        assert appointment is None

    @parametrize
    def test_raw_response_delete(self, client: WebRecruitmentSDK) -> None:
        response = client.appointments.with_raw_response.delete(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        appointment = response.parse()
        assert appointment is None

    @parametrize
    def test_streaming_response_delete(self, client: WebRecruitmentSDK) -> None:
        with client.appointments.with_streaming_response.delete(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            appointment = response.parse()
            assert appointment is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_bulk(self, client: WebRecruitmentSDK) -> None:
        appointment = client.appointments.bulk(
            body=[
                {
                    "date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "patient_id": 0,
                },
                {
                    "date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "patient_id": 0,
                },
                {
                    "date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "patient_id": 0,
                },
            ],
        )
        assert_matches_type(AppointmentBulkResponse, appointment, path=["response"])

    @parametrize
    def test_raw_response_bulk(self, client: WebRecruitmentSDK) -> None:
        response = client.appointments.with_raw_response.bulk(
            body=[
                {
                    "date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "patient_id": 0,
                },
                {
                    "date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "patient_id": 0,
                },
                {
                    "date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "patient_id": 0,
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        appointment = response.parse()
        assert_matches_type(AppointmentBulkResponse, appointment, path=["response"])

    @parametrize
    def test_streaming_response_bulk(self, client: WebRecruitmentSDK) -> None:
        with client.appointments.with_streaming_response.bulk(
            body=[
                {
                    "date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "patient_id": 0,
                },
                {
                    "date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "patient_id": 0,
                },
                {
                    "date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "patient_id": 0,
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            appointment = response.parse()
            assert_matches_type(AppointmentBulkResponse, appointment, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAppointments:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncWebRecruitmentSDK) -> None:
        appointment = await async_client.appointments.create(
            date=parse_datetime("2019-12-27T18:11:19.117Z"),
            patient_id=0,
        )
        assert_matches_type(AppointmentRead, appointment, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncWebRecruitmentSDK) -> None:
        response = await async_client.appointments.with_raw_response.create(
            date=parse_datetime("2019-12-27T18:11:19.117Z"),
            patient_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        appointment = await response.parse()
        assert_matches_type(AppointmentRead, appointment, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncWebRecruitmentSDK) -> None:
        async with async_client.appointments.with_streaming_response.create(
            date=parse_datetime("2019-12-27T18:11:19.117Z"),
            patient_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            appointment = await response.parse()
            assert_matches_type(AppointmentRead, appointment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncWebRecruitmentSDK) -> None:
        appointment = await async_client.appointments.retrieve(
            0,
        )
        assert_matches_type(AppointmentRead, appointment, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncWebRecruitmentSDK) -> None:
        response = await async_client.appointments.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        appointment = await response.parse()
        assert_matches_type(AppointmentRead, appointment, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncWebRecruitmentSDK) -> None:
        async with async_client.appointments.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            appointment = await response.parse()
            assert_matches_type(AppointmentRead, appointment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update(self, async_client: AsyncWebRecruitmentSDK) -> None:
        appointment = await async_client.appointments.update(
            appointment_id=0,
            date=parse_datetime("2019-12-27T18:11:19.117Z"),
            patient_id=0,
        )
        assert_matches_type(AppointmentRead, appointment, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncWebRecruitmentSDK) -> None:
        response = await async_client.appointments.with_raw_response.update(
            appointment_id=0,
            date=parse_datetime("2019-12-27T18:11:19.117Z"),
            patient_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        appointment = await response.parse()
        assert_matches_type(AppointmentRead, appointment, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncWebRecruitmentSDK) -> None:
        async with async_client.appointments.with_streaming_response.update(
            appointment_id=0,
            date=parse_datetime("2019-12-27T18:11:19.117Z"),
            patient_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            appointment = await response.parse()
            assert_matches_type(AppointmentRead, appointment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncWebRecruitmentSDK) -> None:
        appointment = await async_client.appointments.list()
        assert_matches_type(AppointmentListResponse, appointment, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncWebRecruitmentSDK) -> None:
        appointment = await async_client.appointments.list(
            limit=0,
        )
        assert_matches_type(AppointmentListResponse, appointment, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncWebRecruitmentSDK) -> None:
        response = await async_client.appointments.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        appointment = await response.parse()
        assert_matches_type(AppointmentListResponse, appointment, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncWebRecruitmentSDK) -> None:
        async with async_client.appointments.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            appointment = await response.parse()
            assert_matches_type(AppointmentListResponse, appointment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncWebRecruitmentSDK) -> None:
        appointment = await async_client.appointments.delete(
            0,
        )
        assert appointment is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncWebRecruitmentSDK) -> None:
        response = await async_client.appointments.with_raw_response.delete(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        appointment = await response.parse()
        assert appointment is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncWebRecruitmentSDK) -> None:
        async with async_client.appointments.with_streaming_response.delete(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            appointment = await response.parse()
            assert appointment is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_bulk(self, async_client: AsyncWebRecruitmentSDK) -> None:
        appointment = await async_client.appointments.bulk(
            body=[
                {
                    "date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "patient_id": 0,
                },
                {
                    "date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "patient_id": 0,
                },
                {
                    "date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "patient_id": 0,
                },
            ],
        )
        assert_matches_type(AppointmentBulkResponse, appointment, path=["response"])

    @parametrize
    async def test_raw_response_bulk(self, async_client: AsyncWebRecruitmentSDK) -> None:
        response = await async_client.appointments.with_raw_response.bulk(
            body=[
                {
                    "date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "patient_id": 0,
                },
                {
                    "date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "patient_id": 0,
                },
                {
                    "date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "patient_id": 0,
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        appointment = await response.parse()
        assert_matches_type(AppointmentBulkResponse, appointment, path=["response"])

    @parametrize
    async def test_streaming_response_bulk(self, async_client: AsyncWebRecruitmentSDK) -> None:
        async with async_client.appointments.with_streaming_response.bulk(
            body=[
                {
                    "date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "patient_id": 0,
                },
                {
                    "date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "patient_id": 0,
                },
                {
                    "date": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "patient_id": 0,
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            appointment = await response.parse()
            assert_matches_type(AppointmentBulkResponse, appointment, path=["response"])

        assert cast(Any, response.is_closed) is True
