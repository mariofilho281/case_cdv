import requests
import logging
import time

logging.basicConfig(level=logging.INFO)


def fetch_all_data(api_url: str, params: dict, seconds_to_wait: int = 1) -> list:
    """
    Fetches all data from a paginated API by handling pagination automatically.

    This function makes repeated requests to a paginated API endpoint, collecting
    all results across multiple pages. It handles pagination by detecting when
    the API indicates more data is available and adjusting the offset parameter
    accordingly.

    Args:
        api_url (str): The URL of the API endpoint.
        params (dict): The initial query parameters for the first request.
        seconds_to_wait (int, optional): Number of seconds to wait between
            consecutive requests to avoid rate limiting. Defaults to 1 second.

    Returns:
        list: A list containing all the fetched results from all pages.

    Raises:
        requests.exceptions.RequestException: If any network-related error occurs
            during the API request.

    Notes:
        - The API is expected to return JSON responses with a 'features' field
          containing the results and an 'exceededTransferLimit' boolean field
          indicating whether more pages are available.
        - Pagination is handled using the 'resultOffset' parameter which is
          automatically incremented by the number of results fetched per page.
        - The function includes built-in rate limiting with configurable wait time.
    """
    all_results = []
    params = params.copy()
    session = requests.Session()
    logging.info('Starting data fetch...')

    while True:
        try:
            logging.info(f'Requesting data with parameters: {params}')
            response = session.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()
            results_on_page = data.get('features', [])

            if not results_on_page:
                logging.info('No results found on this page.')
                break

            all_results.extend(results_on_page)
            logging.info(f'Fetched {len(results_on_page)} results. '
                         f'Total so far: {len(all_results)}')

            if data.get('exceededTransferLimit'):
                logging.info('Transfer limit exceeded, '
                             'preparing for next page...')
                params['resultOffset'] = (params.get('resultOffset', 0)
                                          + len(results_on_page))
                time.sleep(seconds_to_wait)
            else:
                logging.info('Last page reached. Finalizing fetch.')
                break

        except requests.exceptions.RequestException as request_error:
            logging.error(f'An error occurred: {request_error}')
            break

    logging.info(f'Finished! Total results fetched: {len(all_results)}')
    return all_results


if __name__ == '__main__':
    url = ('https://sigel.aneel.gov.br'
           '/arcgis/rest/services/PORTAL/WFS/MapServer/0/query')
    parameters = {'where': '1=1',
                  'outFields': '*',
                  'f': 'geojson',
                  'resultOffset': 0,
                  'resultRecordCount': 1000}
    results = fetch_all_data(url, parameters)
