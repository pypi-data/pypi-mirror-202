from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ...client import Credmark

from typing import Dict, List, Optional, Union, cast

from ...models.get_cached_model_results_order import GetCachedModelResultsOrder
from ...models.model_deployment import ModelDeployment
from ...models.model_metadata import ModelMetadata
from ...models.model_run_response import ModelRunResponse
from ...models.model_runtime_stats_response import ModelRuntimeStatsResponse
from ...models.run_model_dto import RunModelDto
from ...types import UNSET, Unset
from . import (
    get_cached_model_results,
    get_model_by_slug,
    get_model_deployments_by_slug,
    get_model_runtime_stats,
    list_models,
    run_model,
)


class DefiApi:
    def __init__(self, client: "Credmark"):
        self.__client = client

    def list_models(
        self,
    ) -> Optional[List["ModelMetadata"]]:
        """List metadata for available models

         Returns a list of metadata for available models.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[List['ModelMetadata']]
        """

        return list_models.sync(
            client=self.__client,
        )

    async def list_models_async(
        self,
    ) -> Optional[List["ModelMetadata"]]:
        """List metadata for available models

         Returns a list of metadata for available models.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[List['ModelMetadata']]
        """

        return await list_models.asyncio(
            client=self.__client,
        )

    def get_model_by_slug(
        self,
        slug: str,
    ) -> Optional[ModelMetadata]:
        """Get model metadata by slug

         Returns the metadata for the specified model.

        Args:
            slug (str):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[ModelMetadata]
        """

        return get_model_by_slug.sync(
            client=self.__client,
            slug=slug,
        )

    async def get_model_by_slug_async(
        self,
        slug: str,
    ) -> Optional[ModelMetadata]:
        """Get model metadata by slug

         Returns the metadata for the specified model.

        Args:
            slug (str):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[ModelMetadata]
        """

        return await get_model_by_slug.asyncio(
            client=self.__client,
            slug=slug,
        )

    def get_model_deployments_by_slug(
        self,
        slug: str,
    ) -> Optional[List["ModelDeployment"]]:
        """Get model deployments of a model by slug

         Returns the deployments for a model.

        Args:
            slug (str):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[List['ModelDeployment']]
        """

        return get_model_deployments_by_slug.sync(
            client=self.__client,
            slug=slug,
        )

    async def get_model_deployments_by_slug_async(
        self,
        slug: str,
    ) -> Optional[List["ModelDeployment"]]:
        """Get model deployments of a model by slug

         Returns the deployments for a model.

        Args:
            slug (str):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[List['ModelDeployment']]
        """

        return await get_model_deployments_by_slug.asyncio(
            client=self.__client,
            slug=slug,
        )

    def get_model_runtime_stats(
        self,
    ) -> Optional[ModelRuntimeStatsResponse]:
        """Model runtime stats

         Returns runtime stats for all models.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[ModelRuntimeStatsResponse]
        """

        return get_model_runtime_stats.sync(
            client=self.__client,
        )

    async def get_model_runtime_stats_async(
        self,
    ) -> Optional[ModelRuntimeStatsResponse]:
        """Model runtime stats

         Returns runtime stats for all models.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[ModelRuntimeStatsResponse]
        """

        return await get_model_runtime_stats.asyncio(
            client=self.__client,
        )

    def get_cached_model_results(
        self,
        *,
        slug: str,
        sort: Union[Unset, None, str] = UNSET,
        order: Union[Unset, None, GetCachedModelResultsOrder] = UNSET,
        limit: Union[Unset, None, float] = UNSET,
        offset: Union[Unset, None, float] = UNSET,
    ) -> Optional[ModelRuntimeStatsResponse]:
        """Cached model results

         Returns cached run results for a slug.<p>This endpoint is for analyzing model runs. To run a model
        and get results, use `POST /v1/model/run`.

        Args:
            slug (str):
            sort (Union[Unset, None, str]):
            order (Union[Unset, None, GetCachedModelResultsOrder]):
            limit (Union[Unset, None, float]):
            offset (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[ModelRuntimeStatsResponse]
        """

        return get_cached_model_results.sync(
            client=self.__client,
            slug=slug,
            sort=sort,
            order=order,
            limit=limit,
            offset=offset,
        )

    async def get_cached_model_results_async(
        self,
        *,
        slug: str,
        sort: Union[Unset, None, str] = UNSET,
        order: Union[Unset, None, GetCachedModelResultsOrder] = UNSET,
        limit: Union[Unset, None, float] = UNSET,
        offset: Union[Unset, None, float] = UNSET,
    ) -> Optional[ModelRuntimeStatsResponse]:
        """Cached model results

         Returns cached run results for a slug.<p>This endpoint is for analyzing model runs. To run a model
        and get results, use `POST /v1/model/run`.

        Args:
            slug (str):
            sort (Union[Unset, None, str]):
            order (Union[Unset, None, GetCachedModelResultsOrder]):
            limit (Union[Unset, None, float]):
            offset (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[ModelRuntimeStatsResponse]
        """

        return await get_cached_model_results.asyncio(
            client=self.__client,
            slug=slug,
            sort=sort,
            order=order,
            limit=limit,
            offset=offset,
        )

    def run_model(
        self,
        *,
        json_body: RunModelDto,
    ) -> Optional[ModelRunResponse]:
        """Run model

         Runs a model and returns result object.

        Args:
            json_body (RunModelDto):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[ModelRunResponse]
        """

        return run_model.sync(
            client=self.__client,
            json_body=json_body,
        )

    async def run_model_async(
        self,
        *,
        json_body: RunModelDto,
    ) -> Optional[ModelRunResponse]:
        """Run model

         Runs a model and returns result object.

        Args:
            json_body (RunModelDto):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[ModelRunResponse]
        """

        return await run_model.asyncio(
            client=self.__client,
            json_body=json_body,
        )
