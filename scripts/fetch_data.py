import requests
import logging
import time

logging.basicConfig(level=logging.INFO)


class DataFetcher:
    """
    A client for fetching paginated data from a REST API endpoint.

    This class handles automatic pagination by making sequential requests
    to an API endpoint until all available data has been retrieved. It
    maintains state between requests to track progress and manage resources.

    Attributes:
        url (str): The base URL of the API endpoint to fetch data from.
        params (dict): Query parameters to pass to the API endpoint.
        session (requests.Session): HTTP session for making requests.
        finished (bool): Flag indicating whether all pages have been fetched.
        data (list): Accumulated data from all fetched pages.
    """

    def __init__(self, url: str, params: dict):
        """
        Initialize the DataFetcher with the target API endpoint.

        Args:
            url (str): The base URL of the API endpoint to fetch data from.
                       This should be the full endpoint URL without query parameters.
            params (dict): Query parameters for the API requests. Should include
                          any required parameters for the specific endpoint.
        """
        self.url = url
        self.params = params.copy()
        self.session = requests.Session()
        self.finished = False
        self.data = []

    def fetch_all_pages(self, seconds_between_requests: int = 1):
        """
        Fetch all available pages of data from the API endpoint.

        This method performs sequential requests to the API, automatically
        handling pagination until all data has been retrieved. It accumulates
        results in the `data` attribute and ensures proper resource cleanup.

        Args:
            seconds_between_requests (int, optional): Number of seconds to wait
                                                     between consecutive requests
                                                     to avoid rate limiting.
                                                     Defaults to 1.

        Notes:
            - Ensures the HTTP session is closed even if an exception occurs
        """
        try:
            while not self.finished:
                new_data = self.get_page_data()
                self.data.extend(new_data)
                logging.info(f'Fetched {len(new_data)} results. '
                             f'Total so far: {len(self.data)}')
                time.sleep(seconds_between_requests)
        finally:
            self.session.close()

    def get_page_data(self) -> list:
        """
        Fetch a single page of data from the API.

        This method makes a single HTTP request to the API endpoint with
        the current pagination state. It updates the internal state to
        track progress and determine when pagination is complete.

        Returns:
            list: The data from the current page (from 'features' field).

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returns an error status.
            requests.exceptions.RequestException: For network-related errors.

        Notes:
            - Automatically increments the 'resultOffset' based on records fetched
            - Sets the 'finished' flag when 'exceededTransferLimit' is False
            - Expects the API response to have a 'features' field with the data
              and an 'exceededTransferLimit' boolean field for pagination control
        """
        self.params['resultOffset'] = len(self.data)
        response = self.session.get(self.url, params=self.params)
        response.raise_for_status()
        json_data = response.json()
        page_data = json_data.get('features', [])
        if not json_data.get('exceededTransferLimit'):
            self.finished = True
        return page_data


if __name__ == '__main__':
    url = ('https://sigel.aneel.gov.br'
           '/arcgis/rest/services/PORTAL/WFS/MapServer/0/query')
    parameters = {'where': '1=1',
                  'outFields': '*',
                  'f': 'geojson'}
    fetcher = DataFetcher(url, parameters)
    fetcher.fetch_all_pages(seconds_between_requests=1)
