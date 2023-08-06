from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.token_holder import TokenHolder


T = TypeVar("T", bound="TokenHoldersHistoricalItem")


@attr.s(auto_attribs=True)
class TokenHoldersHistoricalItem:
    """
    Attributes:
        block_number (float): Block number. Example: 15490034.
        block_timestamp (float): Block timestamp. Number of seconds since January 1, 1970. Example: 1662550007.
        data (List['TokenHolder']): List of holders from the top
        total (float): Total number of holders Example: 10.
    """

    block_number: float
    block_timestamp: float
    data: List["TokenHolder"]
    total: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        block_number = self.block_number
        block_timestamp = self.block_timestamp
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()

            data.append(data_item)

        total = self.total

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "blockNumber": block_number,
                "blockTimestamp": block_timestamp,
                "data": data,
                "total": total,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.token_holder import TokenHolder

        d = src_dict.copy()
        block_number = d.pop("blockNumber")

        block_timestamp = d.pop("blockTimestamp")

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = TokenHolder.from_dict(data_item_data)

            data.append(data_item)

        total = d.pop("total")

        token_holders_historical_item = cls(
            block_number=block_number,
            block_timestamp=block_timestamp,
            data=data,
            total=total,
        )

        token_holders_historical_item.additional_properties = d
        return token_holders_historical_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
