from iac_index.error import IacIndexError


class NoAggregatorIndexFoundError(IacIndexError):
    def __init__(self) -> None:
        super().__init__("No aggregator index found - enable cross-region search in AWS Resource Explorer")


class AwsAccessError(IacIndexError):
    pass
