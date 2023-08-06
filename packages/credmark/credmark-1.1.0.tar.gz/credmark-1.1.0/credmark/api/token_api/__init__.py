from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ...client import Credmark

from typing import Dict, Optional, Union, cast

from ...models.get_token_price_align import GetTokenPriceAlign
from ...models.get_token_price_historical_src import GetTokenPriceHistoricalSrc
from ...models.get_token_price_src import GetTokenPriceSrc
from ...models.token_abi_response import TokenAbiResponse
from ...models.token_balance_historical_response import TokenBalanceHistoricalResponse
from ...models.token_balance_response import TokenBalanceResponse
from ...models.token_creation_block_response import TokenCreationBlockResponse
from ...models.token_decimals_response import TokenDecimalsResponse
from ...models.token_error_response import TokenErrorResponse
from ...models.token_historical_holders_count_response import TokenHistoricalHoldersCountResponse
from ...models.token_holders_count_response import TokenHoldersCountResponse
from ...models.token_holders_historical_response import TokenHoldersHistoricalResponse
from ...models.token_holders_response import TokenHoldersResponse
from ...models.token_logo_response import TokenLogoResponse
from ...models.token_metadata_response import TokenMetadataResponse
from ...models.token_name_response import TokenNameResponse
from ...models.token_price_historical_response import TokenPriceHistoricalResponse
from ...models.token_price_response import TokenPriceResponse
from ...models.token_symbol_response import TokenSymbolResponse
from ...models.token_total_supply_historical_response import TokenTotalSupplyHistoricalResponse
from ...models.token_total_supply_response import TokenTotalSupplyResponse
from ...models.token_volume_historical_response import TokenVolumeHistoricalResponse
from ...models.token_volume_response import TokenVolumeResponse
from ...types import UNSET, Unset
from . import (
    get_token_abi,
    get_token_balance,
    get_token_balance_historical,
    get_token_creation_block,
    get_token_decimals,
    get_token_holders,
    get_token_holders_count,
    get_token_holders_count_historical,
    get_token_holders_historical,
    get_token_logo,
    get_token_metadata,
    get_token_name,
    get_token_price,
    get_token_price_historical,
    get_token_symbol,
    get_token_total_supply,
    get_token_total_supply_historical,
    get_token_volume,
    get_token_volume_historical,
)


class TokenApi:
    def __init__(self, client: "Credmark"):
        self.__client = client

    def get_token_metadata(
        self,
        chain_id: float,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenMetadataResponse]]:
        """Get token metadata

         Returns metadata for a token.

        Args:
            chain_id (float):
            token_address (str):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenMetadataResponse]]
        """

        return get_token_metadata.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_metadata_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenMetadataResponse]]:
        """Get token metadata

         Returns metadata for a token.

        Args:
            chain_id (float):
            token_address (str):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenMetadataResponse]]
        """

        return await get_token_metadata.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_name(
        self,
        chain_id: float,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenNameResponse]]:
        """Get token name

         Returns name of a token.

        Args:
            chain_id (float):
            token_address (str):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenNameResponse]]
        """

        return get_token_name.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_name_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenNameResponse]]:
        """Get token name

         Returns name of a token.

        Args:
            chain_id (float):
            token_address (str):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenNameResponse]]
        """

        return await get_token_name.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_symbol(
        self,
        chain_id: float,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenSymbolResponse]]:
        """Get token symbol

         Returns symbol of a token.

        Args:
            chain_id (float):
            token_address (str):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenSymbolResponse]]
        """

        return get_token_symbol.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_symbol_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenSymbolResponse]]:
        """Get token symbol

         Returns symbol of a token.

        Args:
            chain_id (float):
            token_address (str):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenSymbolResponse]]
        """

        return await get_token_symbol.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_decimals(
        self,
        chain_id: float,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenDecimalsResponse, TokenErrorResponse]]:
        """Get token decimals

         Returns decimals of a token.

        Args:
            chain_id (float):
            token_address (str):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenDecimalsResponse, TokenErrorResponse]]
        """

        return get_token_decimals.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_decimals_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenDecimalsResponse, TokenErrorResponse]]:
        """Get token decimals

         Returns decimals of a token.

        Args:
            chain_id (float):
            token_address (str):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenDecimalsResponse, TokenErrorResponse]]
        """

        return await get_token_decimals.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_total_supply(
        self,
        chain_id: float,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
        scaled: Union[Unset, None, bool] = True,
    ) -> Optional[Union[TokenErrorResponse, TokenTotalSupplyResponse]]:
        """Get token's total supply

         Returns total supply of a token.

        Args:
            chain_id (float):
            token_address (str):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):
            scaled (Union[Unset, None, bool]):  Default: True.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenTotalSupplyResponse]]
        """

        return get_token_total_supply.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
            scaled=scaled,
        )

    async def get_token_total_supply_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
        scaled: Union[Unset, None, bool] = True,
    ) -> Optional[Union[TokenErrorResponse, TokenTotalSupplyResponse]]:
        """Get token's total supply

         Returns total supply of a token.

        Args:
            chain_id (float):
            token_address (str):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):
            scaled (Union[Unset, None, bool]):  Default: True.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenTotalSupplyResponse]]
        """

        return await get_token_total_supply.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
            scaled=scaled,
        )

    def get_token_total_supply_historical(
        self,
        chain_id: float,
        token_address: str,
        *,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
        scaled: Union[Unset, None, bool] = True,
    ) -> Optional[Union[TokenErrorResponse, TokenTotalSupplyHistoricalResponse]]:
        """Get historical total supply

         Returns historical total supply for a token.

        Args:
            chain_id (float):
            token_address (str):
            start_block_number (Union[Unset, None, float]):
            end_block_number (Union[Unset, None, float]):
            block_interval (Union[Unset, None, float]):
            start_timestamp (Union[Unset, None, float]):
            end_timestamp (Union[Unset, None, float]):
            time_interval (Union[Unset, None, float]):
            scaled (Union[Unset, None, bool]):  Default: True.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenTotalSupplyHistoricalResponse]]
        """

        return get_token_total_supply_historical.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
            scaled=scaled,
        )

    async def get_token_total_supply_historical_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
        scaled: Union[Unset, None, bool] = True,
    ) -> Optional[Union[TokenErrorResponse, TokenTotalSupplyHistoricalResponse]]:
        """Get historical total supply

         Returns historical total supply for a token.

        Args:
            chain_id (float):
            token_address (str):
            start_block_number (Union[Unset, None, float]):
            end_block_number (Union[Unset, None, float]):
            block_interval (Union[Unset, None, float]):
            start_timestamp (Union[Unset, None, float]):
            end_timestamp (Union[Unset, None, float]):
            time_interval (Union[Unset, None, float]):
            scaled (Union[Unset, None, bool]):  Default: True.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenTotalSupplyHistoricalResponse]]
        """

        return await get_token_total_supply_historical.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
            scaled=scaled,
        )

    def get_token_logo(
        self,
        chain_id: float,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenLogoResponse]]:
        """Get token logo

         Returns logo of a token.

        Args:
            chain_id (float):
            token_address (str):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenLogoResponse]]
        """

        return get_token_logo.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_logo_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenLogoResponse]]:
        """Get token logo

         Returns logo of a token.

        Args:
            chain_id (float):
            token_address (str):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenLogoResponse]]
        """

        return await get_token_logo.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_creation_block(
        self,
        chain_id: float,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenCreationBlockResponse, TokenErrorResponse]]:
        """Get token creation block

         Returns creation block number of a token.

        Args:
            chain_id (float):
            token_address (str):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenCreationBlockResponse, TokenErrorResponse]]
        """

        return get_token_creation_block.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_creation_block_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenCreationBlockResponse, TokenErrorResponse]]:
        """Get token creation block

         Returns creation block number of a token.

        Args:
            chain_id (float):
            token_address (str):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenCreationBlockResponse, TokenErrorResponse]]
        """

        return await get_token_creation_block.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_abi(
        self,
        chain_id: float,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenAbiResponse, TokenErrorResponse]]:
        """Get token ABI

         Returns ABI of a token.

        Args:
            chain_id (float):
            token_address (str):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenAbiResponse, TokenErrorResponse]]
        """

        return get_token_abi.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_abi_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenAbiResponse, TokenErrorResponse]]:
        """Get token ABI

         Returns ABI of a token.

        Args:
            chain_id (float):
            token_address (str):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenAbiResponse, TokenErrorResponse]]
        """

        return await get_token_abi.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_price(
        self,
        chain_id: float,
        token_address: str,
        *,
        quote_address: Union[Unset, None, str] = UNSET,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
        src: Union[Unset, None, GetTokenPriceSrc] = GetTokenPriceSrc.DEX,
        align: Union[Unset, None, GetTokenPriceAlign] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenPriceResponse]]:
        """Get token price data

         Returns price data for a token.

        Args:
            chain_id (float):
            token_address (str):
            quote_address (Union[Unset, None, str]):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):
            src (Union[Unset, None, GetTokenPriceSrc]):  Default: GetTokenPriceSrc.DEX.
            align (Union[Unset, None, GetTokenPriceAlign]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenPriceResponse]]
        """

        return get_token_price.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            quote_address=quote_address,
            block_number=block_number,
            timestamp=timestamp,
            src=src,
            align=align,
        )

    async def get_token_price_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        quote_address: Union[Unset, None, str] = UNSET,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
        src: Union[Unset, None, GetTokenPriceSrc] = GetTokenPriceSrc.DEX,
        align: Union[Unset, None, GetTokenPriceAlign] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenPriceResponse]]:
        """Get token price data

         Returns price data for a token.

        Args:
            chain_id (float):
            token_address (str):
            quote_address (Union[Unset, None, str]):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):
            src (Union[Unset, None, GetTokenPriceSrc]):  Default: GetTokenPriceSrc.DEX.
            align (Union[Unset, None, GetTokenPriceAlign]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenPriceResponse]]
        """

        return await get_token_price.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            quote_address=quote_address,
            block_number=block_number,
            timestamp=timestamp,
            src=src,
            align=align,
        )

    def get_token_price_historical(
        self,
        chain_id: float,
        token_address: str,
        *,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
        quote_address: Union[Unset, None, str] = UNSET,
        src: Union[Unset, None, GetTokenPriceHistoricalSrc] = GetTokenPriceHistoricalSrc.DEX,
    ) -> Optional[Union[TokenErrorResponse, TokenPriceHistoricalResponse]]:
        """Get historical price

         Returns historical price data for a token.

        Args:
            chain_id (float):
            token_address (str):
            start_block_number (Union[Unset, None, float]):
            end_block_number (Union[Unset, None, float]):
            block_interval (Union[Unset, None, float]):
            start_timestamp (Union[Unset, None, float]):
            end_timestamp (Union[Unset, None, float]):
            time_interval (Union[Unset, None, float]):
            quote_address (Union[Unset, None, str]):
            src (Union[Unset, None, GetTokenPriceHistoricalSrc]):  Default:
                GetTokenPriceHistoricalSrc.DEX.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenPriceHistoricalResponse]]
        """

        return get_token_price_historical.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
            quote_address=quote_address,
            src=src,
        )

    async def get_token_price_historical_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
        quote_address: Union[Unset, None, str] = UNSET,
        src: Union[Unset, None, GetTokenPriceHistoricalSrc] = GetTokenPriceHistoricalSrc.DEX,
    ) -> Optional[Union[TokenErrorResponse, TokenPriceHistoricalResponse]]:
        """Get historical price

         Returns historical price data for a token.

        Args:
            chain_id (float):
            token_address (str):
            start_block_number (Union[Unset, None, float]):
            end_block_number (Union[Unset, None, float]):
            block_interval (Union[Unset, None, float]):
            start_timestamp (Union[Unset, None, float]):
            end_timestamp (Union[Unset, None, float]):
            time_interval (Union[Unset, None, float]):
            quote_address (Union[Unset, None, str]):
            src (Union[Unset, None, GetTokenPriceHistoricalSrc]):  Default:
                GetTokenPriceHistoricalSrc.DEX.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenPriceHistoricalResponse]]
        """

        return await get_token_price_historical.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
            quote_address=quote_address,
            src=src,
        )

    def get_token_balance(
        self,
        chain_id: float,
        token_address: str,
        *,
        account_address: str,
        quote_address: Union[Unset, None, str] = UNSET,
        scaled: Union[Unset, None, bool] = True,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenBalanceResponse, TokenErrorResponse]]:
        """Get token balance

         Returns token balance for an account.

        Args:
            chain_id (float):
            token_address (str):
            account_address (str):
            quote_address (Union[Unset, None, str]):
            scaled (Union[Unset, None, bool]):  Default: True.
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenBalanceResponse, TokenErrorResponse]]
        """

        return get_token_balance.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            account_address=account_address,
            quote_address=quote_address,
            scaled=scaled,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_balance_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        account_address: str,
        quote_address: Union[Unset, None, str] = UNSET,
        scaled: Union[Unset, None, bool] = True,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenBalanceResponse, TokenErrorResponse]]:
        """Get token balance

         Returns token balance for an account.

        Args:
            chain_id (float):
            token_address (str):
            account_address (str):
            quote_address (Union[Unset, None, str]):
            scaled (Union[Unset, None, bool]):  Default: True.
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenBalanceResponse, TokenErrorResponse]]
        """

        return await get_token_balance.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            account_address=account_address,
            quote_address=quote_address,
            scaled=scaled,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_balance_historical(
        self,
        chain_id: float,
        token_address: str,
        *,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
        account_address: str,
        quote_address: Union[Unset, None, str] = UNSET,
        scaled: Union[Unset, None, bool] = True,
    ) -> Optional[Union[TokenBalanceHistoricalResponse, TokenErrorResponse]]:
        """Get historical balance

         Returns historical token balance for an account.

        Args:
            chain_id (float):
            token_address (str):
            start_block_number (Union[Unset, None, float]):
            end_block_number (Union[Unset, None, float]):
            block_interval (Union[Unset, None, float]):
            start_timestamp (Union[Unset, None, float]):
            end_timestamp (Union[Unset, None, float]):
            time_interval (Union[Unset, None, float]):
            account_address (str):
            quote_address (Union[Unset, None, str]):
            scaled (Union[Unset, None, bool]):  Default: True.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenBalanceHistoricalResponse, TokenErrorResponse]]
        """

        return get_token_balance_historical.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
            account_address=account_address,
            quote_address=quote_address,
            scaled=scaled,
        )

    async def get_token_balance_historical_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
        account_address: str,
        quote_address: Union[Unset, None, str] = UNSET,
        scaled: Union[Unset, None, bool] = True,
    ) -> Optional[Union[TokenBalanceHistoricalResponse, TokenErrorResponse]]:
        """Get historical balance

         Returns historical token balance for an account.

        Args:
            chain_id (float):
            token_address (str):
            start_block_number (Union[Unset, None, float]):
            end_block_number (Union[Unset, None, float]):
            block_interval (Union[Unset, None, float]):
            start_timestamp (Union[Unset, None, float]):
            end_timestamp (Union[Unset, None, float]):
            time_interval (Union[Unset, None, float]):
            account_address (str):
            quote_address (Union[Unset, None, str]):
            scaled (Union[Unset, None, bool]):  Default: True.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenBalanceHistoricalResponse, TokenErrorResponse]]
        """

        return await get_token_balance_historical.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
            account_address=account_address,
            quote_address=quote_address,
            scaled=scaled,
        )

    def get_token_volume(
        self,
        chain_id: float,
        token_address: str,
        *,
        scaled: Union[Unset, None, bool] = True,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenVolumeResponse]]:
        """Get token volume

         Returns traded volume for a token over a period of blocks or time.

        Args:
            chain_id (float):
            token_address (str):
            scaled (Union[Unset, None, bool]):  Default: True.
            start_block_number (Union[Unset, None, float]):
            end_block_number (Union[Unset, None, float]):
            start_timestamp (Union[Unset, None, float]):
            end_timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenVolumeResponse]]
        """

        return get_token_volume.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            scaled=scaled,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
        )

    async def get_token_volume_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        scaled: Union[Unset, None, bool] = True,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenVolumeResponse]]:
        """Get token volume

         Returns traded volume for a token over a period of blocks or time.

        Args:
            chain_id (float):
            token_address (str):
            scaled (Union[Unset, None, bool]):  Default: True.
            start_block_number (Union[Unset, None, float]):
            end_block_number (Union[Unset, None, float]):
            start_timestamp (Union[Unset, None, float]):
            end_timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenVolumeResponse]]
        """

        return await get_token_volume.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            scaled=scaled,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
        )

    def get_token_volume_historical(
        self,
        chain_id: float,
        token_address: str,
        *,
        scaled: Union[Unset, None, bool] = True,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenVolumeHistoricalResponse]]:
        """Get historical volume

         Returns traded volume for a token over a period of blocks or time divided by intervals.

        Args:
            chain_id (float):
            token_address (str):
            scaled (Union[Unset, None, bool]):  Default: True.
            start_block_number (Union[Unset, None, float]):
            end_block_number (Union[Unset, None, float]):
            start_timestamp (Union[Unset, None, float]):
            end_timestamp (Union[Unset, None, float]):
            block_interval (Union[Unset, None, float]):
            time_interval (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenVolumeHistoricalResponse]]
        """

        return get_token_volume_historical.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            scaled=scaled,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            block_interval=block_interval,
            time_interval=time_interval,
        )

    async def get_token_volume_historical_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        scaled: Union[Unset, None, bool] = True,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenVolumeHistoricalResponse]]:
        """Get historical volume

         Returns traded volume for a token over a period of blocks or time divided by intervals.

        Args:
            chain_id (float):
            token_address (str):
            scaled (Union[Unset, None, bool]):  Default: True.
            start_block_number (Union[Unset, None, float]):
            end_block_number (Union[Unset, None, float]):
            start_timestamp (Union[Unset, None, float]):
            end_timestamp (Union[Unset, None, float]):
            block_interval (Union[Unset, None, float]):
            time_interval (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenVolumeHistoricalResponse]]
        """

        return await get_token_volume_historical.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            scaled=scaled,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            block_interval=block_interval,
            time_interval=time_interval,
        )

    def get_token_holders(
        self,
        chain_id: float,
        token_address: str,
        *,
        page_size: float = 100.0,
        cursor: Union[Unset, None, str] = UNSET,
        quote_address: Union[Unset, None, str] = UNSET,
        scaled: Union[Unset, None, bool] = True,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenHoldersResponse]]:
        """Get token holders

         Returns holders of a token at a block or time.

        Args:
            chain_id (float):
            token_address (str):
            page_size (float):  Default: 100.0.
            cursor (Union[Unset, None, str]):
            quote_address (Union[Unset, None, str]):
            scaled (Union[Unset, None, bool]):  Default: True.
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenHoldersResponse]]
        """

        return get_token_holders.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            page_size=page_size,
            cursor=cursor,
            quote_address=quote_address,
            scaled=scaled,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_holders_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        page_size: float = 100.0,
        cursor: Union[Unset, None, str] = UNSET,
        quote_address: Union[Unset, None, str] = UNSET,
        scaled: Union[Unset, None, bool] = True,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenHoldersResponse]]:
        """Get token holders

         Returns holders of a token at a block or time.

        Args:
            chain_id (float):
            token_address (str):
            page_size (float):  Default: 100.0.
            cursor (Union[Unset, None, str]):
            quote_address (Union[Unset, None, str]):
            scaled (Union[Unset, None, bool]):  Default: True.
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenHoldersResponse]]
        """

        return await get_token_holders.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            page_size=page_size,
            cursor=cursor,
            quote_address=quote_address,
            scaled=scaled,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_holders_historical(
        self,
        chain_id: float,
        token_address: str,
        *,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
        page_size: float = 100.0,
        quote_address: Union[Unset, None, str] = UNSET,
        scaled: Union[Unset, None, bool] = True,
    ) -> Optional[Union[TokenErrorResponse, TokenHoldersHistoricalResponse]]:
        """Get token historical holders

         Returns historical holders of a token at a block or time.

        Args:
            chain_id (float):
            token_address (str):
            start_block_number (Union[Unset, None, float]):
            end_block_number (Union[Unset, None, float]):
            block_interval (Union[Unset, None, float]):
            start_timestamp (Union[Unset, None, float]):
            end_timestamp (Union[Unset, None, float]):
            time_interval (Union[Unset, None, float]):
            page_size (float):  Default: 100.0.
            quote_address (Union[Unset, None, str]):
            scaled (Union[Unset, None, bool]):  Default: True.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenHoldersHistoricalResponse]]
        """

        return get_token_holders_historical.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
            page_size=page_size,
            quote_address=quote_address,
            scaled=scaled,
        )

    async def get_token_holders_historical_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
        page_size: float = 100.0,
        quote_address: Union[Unset, None, str] = UNSET,
        scaled: Union[Unset, None, bool] = True,
    ) -> Optional[Union[TokenErrorResponse, TokenHoldersHistoricalResponse]]:
        """Get token historical holders

         Returns historical holders of a token at a block or time.

        Args:
            chain_id (float):
            token_address (str):
            start_block_number (Union[Unset, None, float]):
            end_block_number (Union[Unset, None, float]):
            block_interval (Union[Unset, None, float]):
            start_timestamp (Union[Unset, None, float]):
            end_timestamp (Union[Unset, None, float]):
            time_interval (Union[Unset, None, float]):
            page_size (float):  Default: 100.0.
            quote_address (Union[Unset, None, str]):
            scaled (Union[Unset, None, bool]):  Default: True.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenHoldersHistoricalResponse]]
        """

        return await get_token_holders_historical.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
            page_size=page_size,
            quote_address=quote_address,
            scaled=scaled,
        )

    def get_token_holders_count(
        self,
        chain_id: float,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenHoldersCountResponse]]:
        """Get total number of token holders

         Returns total number of holders of a token at a block or time.

        Args:
            chain_id (float):
            token_address (str):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenHoldersCountResponse]]
        """

        return get_token_holders_count.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_holders_count_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenHoldersCountResponse]]:
        """Get total number of token holders

         Returns total number of holders of a token at a block or time.

        Args:
            chain_id (float):
            token_address (str):
            block_number (Union[Unset, None, float]):
            timestamp (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenHoldersCountResponse]]
        """

        return await get_token_holders_count.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_holders_count_historical(
        self,
        chain_id: float,
        token_address: str,
        *,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenHistoricalHoldersCountResponse]]:
        """Get historical total number of token holders

         Returns historical total number of holders of a token at a block or time.

        Args:
            chain_id (float):
            token_address (str):
            start_block_number (Union[Unset, None, float]):
            end_block_number (Union[Unset, None, float]):
            block_interval (Union[Unset, None, float]):
            start_timestamp (Union[Unset, None, float]):
            end_timestamp (Union[Unset, None, float]):
            time_interval (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenHistoricalHoldersCountResponse]]
        """

        return get_token_holders_count_historical.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
        )

    async def get_token_holders_count_historical_async(
        self,
        chain_id: float,
        token_address: str,
        *,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
    ) -> Optional[Union[TokenErrorResponse, TokenHistoricalHoldersCountResponse]]:
        """Get historical total number of token holders

         Returns historical total number of holders of a token at a block or time.

        Args:
            chain_id (float):
            token_address (str):
            start_block_number (Union[Unset, None, float]):
            end_block_number (Union[Unset, None, float]):
            block_interval (Union[Unset, None, float]):
            start_timestamp (Union[Unset, None, float]):
            end_timestamp (Union[Unset, None, float]):
            time_interval (Union[Unset, None, float]):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[Union[TokenErrorResponse, TokenHistoricalHoldersCountResponse]]
        """

        return await get_token_holders_count_historical.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
        )
