import os
import tempfile
from pathlib import Path

import pytest

from momics.config import AzureConfig, GCSConfig, LocalConfig, MomicsConfig, S3Config


@pytest.fixture
def temp_config_file():
    """Fixture to create a temporary config file for testing."""
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = Path(temp_file.name)
        yield temp_file_path
    temp_file_path.unlink()


@pytest.fixture
def local_config(temp_config_file):
    """Fixture to initialize LocalConfig with a temporary config file."""
    return LocalConfig(path=temp_config_file)


def test_local_config_set_and_get(local_config):
    """Test setting and getting values in LocalConfig."""
    local_config.set("s3", "region", "us-west-1")
    region = local_config.get("s3", "region")
    assert region == "us-west-1", "Failed to get the correct region value"


def test_s3config_validation():
    """Test S3Config validation."""
    valid_s3_config = S3Config(
        region="us-east-1", access_key_id="key", secret_access_key="secret"
    )
    assert valid_s3_config._is_valid(), "S3Config should be valid"

    with pytest.raises(ValueError):
        S3Config(region="us-east-1", access_key_id="key")  # Missing secret_access_key


def test_momicsconfig_with_s3():
    """Test MomicsConfig with manual S3Config."""
    s3_config = S3Config(
        region="us-east-1", access_key_id="key", secret_access_key="secret"
    )
    momics_config = MomicsConfig(s3=s3_config)
    assert momics_config.type == "s3"
    assert momics_config.cfg["vfs.s3.region"] == "us-east-1"


def test_momicsconfig_with_gcs():
    """Test MomicsConfig with manual GCSConfig."""
    gcs_config = GCSConfig(project_id="name", credentials="key")
    momics_config = MomicsConfig(gcs=gcs_config)
    assert momics_config.type == "gcs"
    assert momics_config.cfg["vfs.gcs.project_id"] == "name"


def test_momicsconfig_with_azure():
    """Test MomicsConfig with manual AzureConfig."""
    azure_config = AzureConfig(account_name="name", account_key="key")
    momics_config = MomicsConfig(azure=azure_config)
    assert momics_config.type == "azure"
    assert momics_config.cfg["vfs.azure.storage_account_name"] == "name"


def test_momicsconfig_with_local_config(local_config):
    """Test MomicsConfig with local config."""
    local_config.set("s3", "region", "eu-west-1")
    local_config.set("s3", "access_key_id", "local_key")
    momics_config = MomicsConfig(local_cfg=local_config.config_path)
    assert momics_config.type is None

    local_config.set("s3", "secret_access_key", "local_secret")
    momics_config = MomicsConfig(local_cfg=local_config.config_path)

    assert momics_config.type == "local", "MomicsConfig should use local config"
    assert (
        momics_config.cfg["vfs.s3.region"] == "eu-west-1"
    ), "Region mismatch in TileDB config"


def test_momicsconfig_without_valid_config():
    """Test MomicsConfig without valid configuration."""
    momics_config = MomicsConfig(local_cfg=Path("dasdcasdcasdcasdc"))
    assert momics_config.type is None
    os.unlink("dasdcasdcasdcasdc")
