from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ...client import Credmark

from typing import Dict, List, Optional, Union, cast

from ...models.check_health_response_200 import CheckHealthResponse200
from ...models.check_health_response_503 import CheckHealthResponse503
from ...types import UNSET, Unset
from . import check_health, get_daily_model_usage, get_top_models, get_total_model_usage


class Utilities:
    def __init__(self, client: "Credmark"):
        self.__client = client

    def check_health(
        self,
    ) -> Optional[Union[CheckHealthResponse200, CheckHealthResponse503]]:
        """Healthcheck status

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[CheckHealthResponse200, CheckHealthResponse503]]
        """

        return check_health.sync(
            client=self.__client,
        )

    async def check_health_async(
        self,
    ) -> Optional[Union[CheckHealthResponse200, CheckHealthResponse503]]:
        """Healthcheck status

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[CheckHealthResponse200, CheckHealthResponse503]]
        """

        return await check_health.asyncio(
            client=self.__client,
        )

    def get_daily_model_usage(
        self,
        *,
        days: Union[Unset, None, float] = UNSET,
        group_by: Union[Unset, None, str] = UNSET,
        requester: Union[Unset, None, str] = UNSET,
    ) -> Optional[List[Dict[str, Any]]]:
        """Model Request statistics

         Returns a list of daily model request statistics, either for a specific requester or for everyone.

        Args:
            days (Union[Unset, None, float]):
            group_by (Union[Unset, None, str]):
            requester (Union[Unset, None, str]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[List[Dict[str, Any]]]
        """

        return get_daily_model_usage.sync(
            client=self.__client,
            days=days,
            group_by=group_by,
            requester=requester,
        )

    async def get_daily_model_usage_async(
        self,
        *,
        days: Union[Unset, None, float] = UNSET,
        group_by: Union[Unset, None, str] = UNSET,
        requester: Union[Unset, None, str] = UNSET,
    ) -> Optional[List[Dict[str, Any]]]:
        """Model Request statistics

         Returns a list of daily model request statistics, either for a specific requester or for everyone.

        Args:
            days (Union[Unset, None, float]):
            group_by (Union[Unset, None, str]):
            requester (Union[Unset, None, str]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[List[Dict[str, Any]]]
        """

        return await get_daily_model_usage.asyncio(
            client=self.__client,
            days=days,
            group_by=group_by,
            requester=requester,
        )

    def get_top_models(
        self,
    ) -> Optional[List[Dict[str, Any]]]:
        """Top Used Models

         Returns a list of the top used models.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[List[Dict[str, Any]]]
        """

        return get_top_models.sync(
            client=self.__client,
        )

    async def get_top_models_async(
        self,
    ) -> Optional[List[Dict[str, Any]]]:
        """Top Used Models

         Returns a list of the top used models.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[List[Dict[str, Any]]]
        """

        return await get_top_models.asyncio(
            client=self.__client,
        )

    def get_total_model_usage(
        self,
    ) -> Optional[List[Dict[str, Any]]]:
        """Total Model Usage

         Returns a count of model runs.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[List[Dict[str, Any]]]
        """

        return get_total_model_usage.sync(
            client=self.__client,
        )

    async def get_total_model_usage_async(
        self,
    ) -> Optional[List[Dict[str, Any]]]:
        """Total Model Usage

         Returns a count of model runs.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[List[Dict[str, Any]]]
        """

        return await get_total_model_usage.asyncio(
            client=self.__client,
        )
