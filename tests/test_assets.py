"""Unit tests for AssetsExt class."""
from cpmf.uipath_ext import AssetsExt


class TestAssetsExt:
    """Tests for AssetsExt extension."""

    def test_list_assets(self, mock_sdk, mock_response):
        """Test list_assets returns asset list."""
        mock_sdk.api_client.request.return_value = mock_response({
            "value": [
                {"Name": "Asset1", "ValueType": "Text", "Value": "test"},
                {"Name": "Asset2", "ValueType": "Integer", "Value": 42},
            ]
        })

        assets = AssetsExt(mock_sdk)
        result = assets.list_assets(folder_key="test-folder-key")

        assert len(result) == 2
        assert result[0]["Name"] == "Asset1"
        mock_sdk.api_client.request.assert_called_once_with(
            "GET",
            "/odata/Assets",
            params={},
            headers={"x-uipath-folderkey": "test-folder-key"},
        )

    def test_list_assets_with_filter(self, mock_sdk, mock_response):
        """Test list_assets with OData filter."""
        mock_sdk.api_client.request.return_value = mock_response({"value": []})

        assets = AssetsExt(mock_sdk)
        assets.list_assets(
            folder_key="test-folder",
            filter_query="ValueType eq 'Credential'",
            top=10,
        )

        mock_sdk.api_client.request.assert_called_once()
        call_args = mock_sdk.api_client.request.call_args
        assert call_args[1]["params"]["$filter"] == "ValueType eq 'Credential'"
        assert call_args[1]["params"]["$top"] == 10

    def test_list_assets_without_folder_key(self, mock_sdk, mock_response):
        """Test list_assets without folder_key uses default."""
        mock_sdk.api_client.request.return_value = mock_response({"value": []})

        assets = AssetsExt(mock_sdk)
        assets.list_assets()

        mock_sdk.api_client.request.assert_called_once_with(
            "GET",
            "/odata/Assets",
            params={},
            headers={},
        )

    def test_get_asset_by_name_found(self, mock_sdk, mock_response):
        """Test get_asset_by_name when asset exists."""
        mock_sdk.api_client.request.return_value = mock_response({
            "value": [{"Name": "MyAsset", "ValueType": "Text", "Value": "hello"}]
        })

        assets = AssetsExt(mock_sdk)
        result = assets.get_asset_by_name("MyAsset", folder_key="test-folder")

        assert result is not None
        assert result["Name"] == "MyAsset"

    def test_get_asset_by_name_not_found(self, mock_sdk, mock_response):
        """Test get_asset_by_name when asset doesn't exist."""
        mock_sdk.api_client.request.return_value = mock_response({"value": []})

        assets = AssetsExt(mock_sdk)
        result = assets.get_asset_by_name("NonExistent")

        assert result is None

    def test_create_asset(self, mock_sdk, mock_response):
        """Test create_asset sends correct payload."""
        mock_sdk.api_client.request.return_value = mock_response({
            "Name": "NewAsset",
            "ValueType": "Text",
            "Value": "test-value",
        })

        assets = AssetsExt(mock_sdk)
        result = assets.create_asset(
            name="NewAsset",
            value_type="Text",
            value="test-value",
            folder_key="test-folder",
            description="Test asset",
        )

        assert result["Name"] == "NewAsset"
        call_args = mock_sdk.api_client.request.call_args
        assert call_args[0] == ("POST", "/odata/Assets")
        assert call_args[1]["json"]["Name"] == "NewAsset"
        assert call_args[1]["json"]["Description"] == "Test asset"

    def test_create_asset_minimal(self, mock_sdk, mock_response):
        """Test create_asset with minimal parameters."""
        mock_sdk.api_client.request.return_value = mock_response({
            "Name": "MinimalAsset",
            "ValueType": "Bool",
            "Value": True,
        })

        assets = AssetsExt(mock_sdk)
        result = assets.create_asset(
            name="MinimalAsset",
            value_type="Bool",
            value=True,
        )

        assert result["Name"] == "MinimalAsset"
        call_args = mock_sdk.api_client.request.call_args
        assert "Description" not in call_args[1]["json"]

    def test_delete_asset(self, mock_sdk, mock_response):
        """Test delete_asset calls correct endpoint."""
        mock_sdk.api_client.request.return_value = mock_response({})

        assets = AssetsExt(mock_sdk)
        assets.delete_asset(asset_key="asset-123", folder_key="test-folder")

        mock_sdk.api_client.request.assert_called_once_with(
            "DELETE",
            "/odata/Assets(asset-123)",
            headers={"x-uipath-folderkey": "test-folder"},
        )

    def test_get_assets_across_folders(self, mock_sdk, mock_response):
        """Test get_assets_across_folders returns cross-folder assets."""
        mock_sdk.api_client.request.return_value = mock_response({
            "value": [
                {"Name": "SharedAsset", "FolderPath": "/Folder1"},
                {"Name": "SharedAsset", "FolderPath": "/Folder2"},
            ]
        })

        assets = AssetsExt(mock_sdk)
        result = assets.get_assets_across_folders(asset_name="SharedAsset")

        assert len(result) == 2
        mock_sdk.api_client.request.assert_called_once()
        call_args = mock_sdk.api_client.request.call_args
        assert call_args[1]["params"]["assetName"] == "SharedAsset"

    def test_share_asset_to_folders(self, mock_sdk, mock_response):
        """Test share_asset_to_folders sends correct payload."""
        mock_sdk.api_client.request.return_value = mock_response({})

        assets = AssetsExt(mock_sdk)
        assets.share_asset_to_folders(
            asset_key="asset-123",
            folder_ids=[100, 200, 300],
            source_folder_key="source-folder",
        )

        call_args = mock_sdk.api_client.request.call_args
        assert call_args[0] == (
            "POST",
            "/odata/Assets/UiPath.Server.Configuration.OData.ShareToFolders",
        )
        assert call_args[1]["json"]["assetId"] == "asset-123"
        assert call_args[1]["json"]["folderIds"] == [100, 200, 300]

    def test_get_folders_for_asset(self, mock_sdk, mock_response):
        """Test get_folders_for_asset returns folder list."""
        mock_sdk.api_client.request.return_value = mock_response({
            "value": [
                {"DisplayName": "Folder1", "Id": 100},
                {"DisplayName": "Folder2", "Id": 200},
            ]
        })

        assets = AssetsExt(mock_sdk)
        result = assets.get_folders_for_asset(
            asset_key="asset-123",
            source_folder_key="source-folder",
        )

        assert len(result) == 2
        assert result[0]["DisplayName"] == "Folder1"
