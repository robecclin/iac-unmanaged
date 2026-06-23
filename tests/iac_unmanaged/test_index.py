from unittest.mock import patch

from iac_index.aws import NoAggregatorIndexFoundError
from iac_index.resource import Resource, ResourceType
from tests.conftest import RunCli


def test_main_index(run_cli: RunCli) -> None:
    resources = [
        Resource(
            account="123456789012",
            region="us-east-1",
            type=ResourceType("aws", "s3", "bucket"),
            identifier="my-bucket",
        ),
    ]
    with patch("iac_unmanaged.command.index.index_aws", return_value=iter(resources)):
        result = run_cli("index")
        assert result.exit_code == 0
        assert "aws:s3:bucket" in result.stdout
        assert "my-bucket" in result.stdout


def test_index_no_aggregator_region(run_cli: RunCli) -> None:
    with patch("iac_unmanaged.command.index.index_aws", side_effect=NoAggregatorIndexFoundError()):
        result = run_cli("index")
        assert result.exit_code == 1
        assert "No aggregator index found" in result.stderr


def test_main_index_zero_resources(run_cli: RunCli) -> None:
    with patch("iac_unmanaged.command.index.index_aws", return_value=iter([])):
        result = run_cli("index")
        assert result.exit_code == 0
        assert "No resources found" in result.stdout
