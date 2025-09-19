import requests
import time
import pandas as pd


def fetch_all_data(api_url: str, params: dict):
    """
    Fetches all data from a paginated API.

    Args:
        api_url (str): The base URL of the API endpoint.
        params (dict): The initial query parameters for the first request.

    Returns:
        list: A list containing all the fetched results.
    """
    all_results = []
    params = params.copy()
    session = requests.Session()
    # You might need to add authentication headers to the session
    # session.headers.update({'Authorization': 'Bearer YOUR_API_KEY'})
    print("Starting data fetch...")

    while True:
        try:
            print(f"Requesting data with parameters: {params}")
            response = session.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()
            results_on_page = data.get('features', [])

            if not results_on_page:
                print("No more results found on this page.")
                break  # Exit if the results list is empty

            all_results.extend(results_on_page)
            print(f"Fetched {len(results_on_page)} results. Total so far: {len(all_results)}")

            # --- Pagination check ---
            # Check the flag that indicates if there is more data
            if data.get("exceededTransferLimit"):
                print("Transfer limit exceeded, preparing for next page...")

                # --- This is the key logic for the next page ---
                # Increment the offset to get the next batch of results.
                # Your API might call the offset parameter 'start' or something else.
                # Your API might also not use an offset but a page number.
                params['resultOffset'] = params.get('resultOffset', 0) + len(results_on_page)

                # Be a good API citizen: wait a little before the next request
                time.sleep(1)
            else:
                # If the flag is false or not present, we're done.
                print("Last page reached. Finalizing fetch.")
                break

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break  # Exit the loop on error

    print(f"\nFinished! Total results fetched: {len(all_results)}")
    return all_results


# --- How to use the function ---
if __name__ == "__main__":
    API_ENDPOINT = 'https://sigel.aneel.gov.br/arcgis/rest/services/PORTAL/WFS/MapServer/0/query'
    parameters = {'where': '1=1', 'outFields': '*', 'f': 'pjson'}
    response = requests.post(API_ENDPOINT, data=parameters)
    data = response.json()
    data = pd.DataFrame(data['features'])

    # The initial parameters for your first query.
    # The 'limit' parameter is often called 'resultRecordCount' or 'num'.
    # The 'offset' parameter is often called 'resultOffset' or 'start'.
    # You MUST check your API's documentation for the correct names.
    initial_query_params = {
        'where': '1=1',  # Example query condition
        'outFields': '*',
        'returnGeometry': 'false',
        'f': 'json',
        'resultRecordCount': 1000,  # This is our 'limit'
        'resultOffset': 0  # This is our starting 'offset'
    }

    all_my_data = fetch_all_data(API_ENDPOINT, initial_query_params)

    # Now you can work with all_my_data
    # For example, print the first 5 results
    # print("\nFirst 5 results:")
    # for item in all_my_data[:5]:
    #    print(item)

