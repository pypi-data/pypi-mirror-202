from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Dict, List, Optional, cast

import httpx

if TYPE_CHECKING:
    from ...client import Credmark

from typing import List, cast

from ... import errors
from ...types import Response


def _get_kwargs(client: "Credmark") -> Dict[str, Any]:
    url = "{}/v1/usage/top".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(*, client: "Credmark", response: httpx.Response) -> Optional[List[Dict[str, Any]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(List[Dict[str, Any]], response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: "Credmark", response: httpx.Response) -> Response[List[Dict[str, Any]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(client: "Credmark") -> Response[List[Dict[str, Any]]]:
    """Top Used Models

     Returns a list of the top used models.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[Dict[str, Any]]]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(client: "Credmark") -> Optional[List[Dict[str, Any]]]:
    """Top Used Models

     Returns a list of the top used models.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[Dict[str, Any]]]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(client: "Credmark") -> Response[List[Dict[str, Any]]]:
    """Top Used Models

     Returns a list of the top used models.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[Dict[str, Any]]]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(client: "Credmark") -> Optional[List[Dict[str, Any]]]:
    """Top Used Models

     Returns a list of the top used models.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[Dict[str, Any]]]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
