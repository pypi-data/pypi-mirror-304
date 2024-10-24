# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from datetime import datetime

import httpx

from ..types import (
    appointment_bulk_params,
    appointment_list_params,
    appointment_create_params,
    appointment_update_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.appointment_read import AppointmentRead
from ..types.appointment_bulk_response import AppointmentBulkResponse
from ..types.appointment_list_response import AppointmentListResponse

__all__ = ["AppointmentsResource", "AsyncAppointmentsResource"]


class AppointmentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AppointmentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#accessing-raw-response-data-eg-headers
        """
        return AppointmentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AppointmentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#with_streaming_response
        """
        return AppointmentsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        date: Union[str, datetime],
        patient_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AppointmentRead:
        """
        Create Appointment

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/appointments",
            body=maybe_transform(
                {
                    "date": date,
                    "patient_id": patient_id,
                },
                appointment_create_params.AppointmentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AppointmentRead,
        )

    def retrieve(
        self,
        appointment_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AppointmentRead:
        """
        Get Appointment

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/appointments/{appointment_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AppointmentRead,
        )

    def update(
        self,
        appointment_id: int,
        *,
        date: Union[str, datetime],
        patient_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AppointmentRead:
        """
        Update Appointment

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._put(
            f"/appointments/{appointment_id}",
            body=maybe_transform(
                {
                    "date": date,
                    "patient_id": patient_id,
                },
                appointment_update_params.AppointmentUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AppointmentRead,
        )

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AppointmentListResponse:
        """
        Get Appointments

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/appointments",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"limit": limit}, appointment_list_params.AppointmentListParams),
            ),
            cast_to=AppointmentListResponse,
        )

    def delete(
        self,
        appointment_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Appointment

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/appointments/{appointment_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def bulk(
        self,
        *,
        body: Iterable[appointment_bulk_params.Body],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AppointmentBulkResponse:
        """
        Create Appointments Bulk

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/appointments/bulk",
            body=maybe_transform(body, Iterable[appointment_bulk_params.Body]),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AppointmentBulkResponse,
        )


class AsyncAppointmentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAppointmentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncAppointmentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAppointmentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#with_streaming_response
        """
        return AsyncAppointmentsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        date: Union[str, datetime],
        patient_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AppointmentRead:
        """
        Create Appointment

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/appointments",
            body=await async_maybe_transform(
                {
                    "date": date,
                    "patient_id": patient_id,
                },
                appointment_create_params.AppointmentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AppointmentRead,
        )

    async def retrieve(
        self,
        appointment_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AppointmentRead:
        """
        Get Appointment

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/appointments/{appointment_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AppointmentRead,
        )

    async def update(
        self,
        appointment_id: int,
        *,
        date: Union[str, datetime],
        patient_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AppointmentRead:
        """
        Update Appointment

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._put(
            f"/appointments/{appointment_id}",
            body=await async_maybe_transform(
                {
                    "date": date,
                    "patient_id": patient_id,
                },
                appointment_update_params.AppointmentUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AppointmentRead,
        )

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AppointmentListResponse:
        """
        Get Appointments

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/appointments",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"limit": limit}, appointment_list_params.AppointmentListParams),
            ),
            cast_to=AppointmentListResponse,
        )

    async def delete(
        self,
        appointment_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Appointment

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/appointments/{appointment_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def bulk(
        self,
        *,
        body: Iterable[appointment_bulk_params.Body],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AppointmentBulkResponse:
        """
        Create Appointments Bulk

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/appointments/bulk",
            body=await async_maybe_transform(body, Iterable[appointment_bulk_params.Body]),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AppointmentBulkResponse,
        )


class AppointmentsResourceWithRawResponse:
    def __init__(self, appointments: AppointmentsResource) -> None:
        self._appointments = appointments

        self.create = to_raw_response_wrapper(
            appointments.create,
        )
        self.retrieve = to_raw_response_wrapper(
            appointments.retrieve,
        )
        self.update = to_raw_response_wrapper(
            appointments.update,
        )
        self.list = to_raw_response_wrapper(
            appointments.list,
        )
        self.delete = to_raw_response_wrapper(
            appointments.delete,
        )
        self.bulk = to_raw_response_wrapper(
            appointments.bulk,
        )


class AsyncAppointmentsResourceWithRawResponse:
    def __init__(self, appointments: AsyncAppointmentsResource) -> None:
        self._appointments = appointments

        self.create = async_to_raw_response_wrapper(
            appointments.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            appointments.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            appointments.update,
        )
        self.list = async_to_raw_response_wrapper(
            appointments.list,
        )
        self.delete = async_to_raw_response_wrapper(
            appointments.delete,
        )
        self.bulk = async_to_raw_response_wrapper(
            appointments.bulk,
        )


class AppointmentsResourceWithStreamingResponse:
    def __init__(self, appointments: AppointmentsResource) -> None:
        self._appointments = appointments

        self.create = to_streamed_response_wrapper(
            appointments.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            appointments.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            appointments.update,
        )
        self.list = to_streamed_response_wrapper(
            appointments.list,
        )
        self.delete = to_streamed_response_wrapper(
            appointments.delete,
        )
        self.bulk = to_streamed_response_wrapper(
            appointments.bulk,
        )


class AsyncAppointmentsResourceWithStreamingResponse:
    def __init__(self, appointments: AsyncAppointmentsResource) -> None:
        self._appointments = appointments

        self.create = async_to_streamed_response_wrapper(
            appointments.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            appointments.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            appointments.update,
        )
        self.list = async_to_streamed_response_wrapper(
            appointments.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            appointments.delete,
        )
        self.bulk = async_to_streamed_response_wrapper(
            appointments.bulk,
        )
