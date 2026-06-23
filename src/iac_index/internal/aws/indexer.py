from collections.abc import Generator

from boto3 import Session

from iac_index.resource import Resource

from .arn import parse_arn
from .client import get_resources
from .resource_type import parse_resource_type


def index(session: Session) -> Generator[Resource]:
    for resource in get_resources(session):
        arn = parse_arn(resource.arn)
        resource_type = parse_resource_type(resource.type)
        yield Resource(
            account=resource.account_id,
            region=resource.region,
            type=resource_type,
            identifier=arn.resource_id,
        )
