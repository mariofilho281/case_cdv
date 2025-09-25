from scripts.fetch_data import DataFetcher


class TestDataFetcher:
    """Test suite for DataFetcher class."""

    def test_initialization(self):
        """Test that DataFetcher initializes with correct attributes."""
        url = "https://api.example.com/data"
        params = {"where": "1=1", "outFields": "*"}
        fetcher = DataFetcher(url, params)

        assert fetcher.url == url
        assert fetcher.params == params
        assert fetcher.params is not params
        assert fetcher.finished is False
        assert fetcher.data == []
        assert fetcher.session is not None

        fetcher.session.close()

    def test_initialization_params_copy(self):
        """Test that parameters are properly copied to avoid mutation issues."""
        original_params = {"where": "1=1", "outFields": "*"}
        fetcher = DataFetcher("https://api.example.com", original_params)
        original_params["new_key"] = "new_value"

        assert "new_key" not in fetcher.params

        fetcher.session.close()

    def test_real_api_call(self):
        """Test with real API endpoint (use sparingly)."""
        url = "https://sigel.aneel.gov.br/arcgis/rest/services/PORTAL/WFS/MapServer/0/query"
        params = {"where": "1=1", "outFields": "*", "f": "geojson"}

        fetcher = DataFetcher(url, params)
        fetcher.fetch_all_pages(seconds_between_requests=1)

        assert len(fetcher.data) > 0
        assert isinstance(fetcher.data, list)
