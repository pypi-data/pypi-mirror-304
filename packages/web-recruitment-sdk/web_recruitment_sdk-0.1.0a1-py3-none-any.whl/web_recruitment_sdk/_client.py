# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import resources, _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import (
    is_given,
    get_async_library,
)
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError, WebRecruitmentSDKError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "resources",
    "WebRecruitmentSDK",
    "AsyncWebRecruitmentSDK",
    "Client",
    "AsyncClient",
]


class WebRecruitmentSDK(SyncAPIClient):
    admin: resources.AdminResource
    health: resources.HealthResource
    patients: resources.PatientsResource
    patients_by_external_id: resources.PatientsByExternalIDResource
    protocols: resources.ProtocolsResource
    criteria: resources.CriteriaResource
    criteria_instances: resources.CriteriaInstancesResource
    appointments: resources.AppointmentsResource
    sites: resources.SitesResource
    protocol_parsing: resources.ProtocolParsingResource
    with_raw_response: WebRecruitmentSDKWithRawResponse
    with_streaming_response: WebRecruitmentSDKWithStreamedResponse

    # client options
    api_key: str
    bearer_token: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous web-recruitment-sdk client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `X_API_KEY`
        - `bearer_token` from `AUTHORIZATION_TOKEN`
        """
        if api_key is None:
            api_key = os.environ.get("X_API_KEY")
        if api_key is None:
            raise WebRecruitmentSDKError(
                "The api_key client option must be set either by passing api_key to the client or by setting the X_API_KEY environment variable"
            )
        self.api_key = api_key

        if bearer_token is None:
            bearer_token = os.environ.get("AUTHORIZATION_TOKEN")
        if bearer_token is None:
            raise WebRecruitmentSDKError(
                "The bearer_token client option must be set either by passing bearer_token to the client or by setting the AUTHORIZATION_TOKEN environment variable"
            )
        self.bearer_token = bearer_token

        if base_url is None:
            base_url = os.environ.get("WEB_RECRUITMENT_SDK_BASE_URL")
        if base_url is None:
            base_url = f"https://localhost:8080/test-api"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.admin = resources.AdminResource(self)
        self.health = resources.HealthResource(self)
        self.patients = resources.PatientsResource(self)
        self.patients_by_external_id = resources.PatientsByExternalIDResource(self)
        self.protocols = resources.ProtocolsResource(self)
        self.criteria = resources.CriteriaResource(self)
        self.criteria_instances = resources.CriteriaInstancesResource(self)
        self.appointments = resources.AppointmentsResource(self)
        self.sites = resources.SitesResource(self)
        self.protocol_parsing = resources.ProtocolParsingResource(self)
        self.with_raw_response = WebRecruitmentSDKWithRawResponse(self)
        self.with_streaming_response = WebRecruitmentSDKWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        if self._api_key_header:
            return self._api_key_header
        if self._http_bearer:
            return self._http_bearer
        return {}

    @property
    def _api_key_header(self) -> dict[str, str]:
        api_key = self.api_key
        return {"x-api-key": api_key}

    @property
    def _http_bearer(self) -> dict[str, str]:
        bearer_token = self.bearer_token
        return {"Authorization": f"Bearer {bearer_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            bearer_token=bearer_token or self.bearer_token,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncWebRecruitmentSDK(AsyncAPIClient):
    admin: resources.AsyncAdminResource
    health: resources.AsyncHealthResource
    patients: resources.AsyncPatientsResource
    patients_by_external_id: resources.AsyncPatientsByExternalIDResource
    protocols: resources.AsyncProtocolsResource
    criteria: resources.AsyncCriteriaResource
    criteria_instances: resources.AsyncCriteriaInstancesResource
    appointments: resources.AsyncAppointmentsResource
    sites: resources.AsyncSitesResource
    protocol_parsing: resources.AsyncProtocolParsingResource
    with_raw_response: AsyncWebRecruitmentSDKWithRawResponse
    with_streaming_response: AsyncWebRecruitmentSDKWithStreamedResponse

    # client options
    api_key: str
    bearer_token: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async web-recruitment-sdk client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `X_API_KEY`
        - `bearer_token` from `AUTHORIZATION_TOKEN`
        """
        if api_key is None:
            api_key = os.environ.get("X_API_KEY")
        if api_key is None:
            raise WebRecruitmentSDKError(
                "The api_key client option must be set either by passing api_key to the client or by setting the X_API_KEY environment variable"
            )
        self.api_key = api_key

        if bearer_token is None:
            bearer_token = os.environ.get("AUTHORIZATION_TOKEN")
        if bearer_token is None:
            raise WebRecruitmentSDKError(
                "The bearer_token client option must be set either by passing bearer_token to the client or by setting the AUTHORIZATION_TOKEN environment variable"
            )
        self.bearer_token = bearer_token

        if base_url is None:
            base_url = os.environ.get("WEB_RECRUITMENT_SDK_BASE_URL")
        if base_url is None:
            base_url = f"https://localhost:8080/test-api"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.admin = resources.AsyncAdminResource(self)
        self.health = resources.AsyncHealthResource(self)
        self.patients = resources.AsyncPatientsResource(self)
        self.patients_by_external_id = resources.AsyncPatientsByExternalIDResource(self)
        self.protocols = resources.AsyncProtocolsResource(self)
        self.criteria = resources.AsyncCriteriaResource(self)
        self.criteria_instances = resources.AsyncCriteriaInstancesResource(self)
        self.appointments = resources.AsyncAppointmentsResource(self)
        self.sites = resources.AsyncSitesResource(self)
        self.protocol_parsing = resources.AsyncProtocolParsingResource(self)
        self.with_raw_response = AsyncWebRecruitmentSDKWithRawResponse(self)
        self.with_streaming_response = AsyncWebRecruitmentSDKWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        if self._api_key_header:
            return self._api_key_header
        if self._http_bearer:
            return self._http_bearer
        return {}

    @property
    def _api_key_header(self) -> dict[str, str]:
        api_key = self.api_key
        return {"x-api-key": api_key}

    @property
    def _http_bearer(self) -> dict[str, str]:
        bearer_token = self.bearer_token
        return {"Authorization": f"Bearer {bearer_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            bearer_token=bearer_token or self.bearer_token,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class WebRecruitmentSDKWithRawResponse:
    def __init__(self, client: WebRecruitmentSDK) -> None:
        self.admin = resources.AdminResourceWithRawResponse(client.admin)
        self.health = resources.HealthResourceWithRawResponse(client.health)
        self.patients = resources.PatientsResourceWithRawResponse(client.patients)
        self.patients_by_external_id = resources.PatientsByExternalIDResourceWithRawResponse(
            client.patients_by_external_id
        )
        self.protocols = resources.ProtocolsResourceWithRawResponse(client.protocols)
        self.criteria = resources.CriteriaResourceWithRawResponse(client.criteria)
        self.criteria_instances = resources.CriteriaInstancesResourceWithRawResponse(client.criteria_instances)
        self.appointments = resources.AppointmentsResourceWithRawResponse(client.appointments)
        self.sites = resources.SitesResourceWithRawResponse(client.sites)
        self.protocol_parsing = resources.ProtocolParsingResourceWithRawResponse(client.protocol_parsing)


class AsyncWebRecruitmentSDKWithRawResponse:
    def __init__(self, client: AsyncWebRecruitmentSDK) -> None:
        self.admin = resources.AsyncAdminResourceWithRawResponse(client.admin)
        self.health = resources.AsyncHealthResourceWithRawResponse(client.health)
        self.patients = resources.AsyncPatientsResourceWithRawResponse(client.patients)
        self.patients_by_external_id = resources.AsyncPatientsByExternalIDResourceWithRawResponse(
            client.patients_by_external_id
        )
        self.protocols = resources.AsyncProtocolsResourceWithRawResponse(client.protocols)
        self.criteria = resources.AsyncCriteriaResourceWithRawResponse(client.criteria)
        self.criteria_instances = resources.AsyncCriteriaInstancesResourceWithRawResponse(client.criteria_instances)
        self.appointments = resources.AsyncAppointmentsResourceWithRawResponse(client.appointments)
        self.sites = resources.AsyncSitesResourceWithRawResponse(client.sites)
        self.protocol_parsing = resources.AsyncProtocolParsingResourceWithRawResponse(client.protocol_parsing)


class WebRecruitmentSDKWithStreamedResponse:
    def __init__(self, client: WebRecruitmentSDK) -> None:
        self.admin = resources.AdminResourceWithStreamingResponse(client.admin)
        self.health = resources.HealthResourceWithStreamingResponse(client.health)
        self.patients = resources.PatientsResourceWithStreamingResponse(client.patients)
        self.patients_by_external_id = resources.PatientsByExternalIDResourceWithStreamingResponse(
            client.patients_by_external_id
        )
        self.protocols = resources.ProtocolsResourceWithStreamingResponse(client.protocols)
        self.criteria = resources.CriteriaResourceWithStreamingResponse(client.criteria)
        self.criteria_instances = resources.CriteriaInstancesResourceWithStreamingResponse(client.criteria_instances)
        self.appointments = resources.AppointmentsResourceWithStreamingResponse(client.appointments)
        self.sites = resources.SitesResourceWithStreamingResponse(client.sites)
        self.protocol_parsing = resources.ProtocolParsingResourceWithStreamingResponse(client.protocol_parsing)


class AsyncWebRecruitmentSDKWithStreamedResponse:
    def __init__(self, client: AsyncWebRecruitmentSDK) -> None:
        self.admin = resources.AsyncAdminResourceWithStreamingResponse(client.admin)
        self.health = resources.AsyncHealthResourceWithStreamingResponse(client.health)
        self.patients = resources.AsyncPatientsResourceWithStreamingResponse(client.patients)
        self.patients_by_external_id = resources.AsyncPatientsByExternalIDResourceWithStreamingResponse(
            client.patients_by_external_id
        )
        self.protocols = resources.AsyncProtocolsResourceWithStreamingResponse(client.protocols)
        self.criteria = resources.AsyncCriteriaResourceWithStreamingResponse(client.criteria)
        self.criteria_instances = resources.AsyncCriteriaInstancesResourceWithStreamingResponse(
            client.criteria_instances
        )
        self.appointments = resources.AsyncAppointmentsResourceWithStreamingResponse(client.appointments)
        self.sites = resources.AsyncSitesResourceWithStreamingResponse(client.sites)
        self.protocol_parsing = resources.AsyncProtocolParsingResourceWithStreamingResponse(client.protocol_parsing)


Client = WebRecruitmentSDK

AsyncClient = AsyncWebRecruitmentSDK
