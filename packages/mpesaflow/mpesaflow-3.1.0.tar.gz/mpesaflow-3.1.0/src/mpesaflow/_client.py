# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Dict, Union, Mapping, cast
from typing_extensions import Self, Literal, override

import httpx

from . import resources, _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Headers,
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
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = [
    "ENVIRONMENTS",
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "resources",
    "Mpesaflow",
    "AsyncMpesaflow",
    "Client",
    "AsyncClient",
]

ENVIRONMENTS: Dict[str, str] = {
    "production": "https://api.mpesaflow.com",
    "sandbox": "https://sandbox-api.mpesaflow.com",
}


class Mpesaflow(SyncAPIClient):
    apps: resources.AppsResource
    transactions: resources.TransactionsResource
    with_raw_response: MpesaflowWithRawResponse
    with_streaming_response: MpesaflowWithStreamedResponse

    # client options
    app_api_key: str | None
    root_api_key: str | None

    _environment: Literal["production", "sandbox"] | NotGiven

    def __init__(
        self,
        *,
        app_api_key: str | None = None,
        root_api_key: str | None = None,
        environment: Literal["production", "sandbox"] | NotGiven = NOT_GIVEN,
        base_url: str | httpx.URL | None | NotGiven = NOT_GIVEN,
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
        """Construct a new synchronous mpesaflow client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `app_api_key` from `APP_API_KEY`
        - `root_api_key` from `ROOT_API_KEY`
        """
        if app_api_key is None:
            app_api_key = os.environ.get("APP_API_KEY")
        self.app_api_key = app_api_key

        if root_api_key is None:
            root_api_key = os.environ.get("ROOT_API_KEY")
        self.root_api_key = root_api_key

        self._environment = environment

        base_url_env = os.environ.get("MPESAFLOW_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `MPESAFLOW_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "production"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

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

        self.apps = resources.AppsResource(self)
        self.transactions = resources.TransactionsResource(self)
        self.with_raw_response = MpesaflowWithRawResponse(self)
        self.with_streaming_response = MpesaflowWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        if self._app_api_key:
            return self._app_api_key
        if self._root_api_key:
            return self._root_api_key
        return {}

    @property
    def _app_api_key(self) -> dict[str, str]:
        app_api_key = self.app_api_key
        if app_api_key is None:
            return {}
        return {"X-App-Api-Key": app_api_key}

    @property
    def _root_api_key(self) -> dict[str, str]:
        root_api_key = self.root_api_key
        if root_api_key is None:
            return {}
        return {"X-Root-Api-Key": root_api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.app_api_key and headers.get("X-App-Api-Key"):
            return
        if isinstance(custom_headers.get("X-App-Api-Key"), Omit):
            return

        if self.root_api_key and headers.get("X-Root-Api-Key"):
            return
        if isinstance(custom_headers.get("X-Root-Api-Key"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected either app_api_key or root_api_key to be set. Or for one of the `X-App-Api-Key` or `X-Root-Api-Key` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        app_api_key: str | None = None,
        root_api_key: str | None = None,
        environment: Literal["production", "sandbox"] | None = None,
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
            app_api_key=app_api_key or self.app_api_key,
            root_api_key=root_api_key or self.root_api_key,
            base_url=base_url or self.base_url,
            environment=environment or self._environment,
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


class AsyncMpesaflow(AsyncAPIClient):
    apps: resources.AsyncAppsResource
    transactions: resources.AsyncTransactionsResource
    with_raw_response: AsyncMpesaflowWithRawResponse
    with_streaming_response: AsyncMpesaflowWithStreamedResponse

    # client options
    app_api_key: str | None
    root_api_key: str | None

    _environment: Literal["production", "sandbox"] | NotGiven

    def __init__(
        self,
        *,
        app_api_key: str | None = None,
        root_api_key: str | None = None,
        environment: Literal["production", "sandbox"] | NotGiven = NOT_GIVEN,
        base_url: str | httpx.URL | None | NotGiven = NOT_GIVEN,
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
        """Construct a new async mpesaflow client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `app_api_key` from `APP_API_KEY`
        - `root_api_key` from `ROOT_API_KEY`
        """
        if app_api_key is None:
            app_api_key = os.environ.get("APP_API_KEY")
        self.app_api_key = app_api_key

        if root_api_key is None:
            root_api_key = os.environ.get("ROOT_API_KEY")
        self.root_api_key = root_api_key

        self._environment = environment

        base_url_env = os.environ.get("MPESAFLOW_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `MPESAFLOW_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "production"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

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

        self.apps = resources.AsyncAppsResource(self)
        self.transactions = resources.AsyncTransactionsResource(self)
        self.with_raw_response = AsyncMpesaflowWithRawResponse(self)
        self.with_streaming_response = AsyncMpesaflowWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        if self._app_api_key:
            return self._app_api_key
        if self._root_api_key:
            return self._root_api_key
        return {}

    @property
    def _app_api_key(self) -> dict[str, str]:
        app_api_key = self.app_api_key
        if app_api_key is None:
            return {}
        return {"X-App-Api-Key": app_api_key}

    @property
    def _root_api_key(self) -> dict[str, str]:
        root_api_key = self.root_api_key
        if root_api_key is None:
            return {}
        return {"X-Root-Api-Key": root_api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.app_api_key and headers.get("X-App-Api-Key"):
            return
        if isinstance(custom_headers.get("X-App-Api-Key"), Omit):
            return

        if self.root_api_key and headers.get("X-Root-Api-Key"):
            return
        if isinstance(custom_headers.get("X-Root-Api-Key"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected either app_api_key or root_api_key to be set. Or for one of the `X-App-Api-Key` or `X-Root-Api-Key` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        app_api_key: str | None = None,
        root_api_key: str | None = None,
        environment: Literal["production", "sandbox"] | None = None,
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
            app_api_key=app_api_key or self.app_api_key,
            root_api_key=root_api_key or self.root_api_key,
            base_url=base_url or self.base_url,
            environment=environment or self._environment,
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


class MpesaflowWithRawResponse:
    def __init__(self, client: Mpesaflow) -> None:
        self.apps = resources.AppsResourceWithRawResponse(client.apps)
        self.transactions = resources.TransactionsResourceWithRawResponse(client.transactions)


class AsyncMpesaflowWithRawResponse:
    def __init__(self, client: AsyncMpesaflow) -> None:
        self.apps = resources.AsyncAppsResourceWithRawResponse(client.apps)
        self.transactions = resources.AsyncTransactionsResourceWithRawResponse(client.transactions)


class MpesaflowWithStreamedResponse:
    def __init__(self, client: Mpesaflow) -> None:
        self.apps = resources.AppsResourceWithStreamingResponse(client.apps)
        self.transactions = resources.TransactionsResourceWithStreamingResponse(client.transactions)


class AsyncMpesaflowWithStreamedResponse:
    def __init__(self, client: AsyncMpesaflow) -> None:
        self.apps = resources.AsyncAppsResourceWithStreamingResponse(client.apps)
        self.transactions = resources.AsyncTransactionsResourceWithStreamingResponse(client.transactions)


Client = Mpesaflow

AsyncClient = AsyncMpesaflow
