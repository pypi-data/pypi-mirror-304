# kaziro.MarketApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_market_endpoint_v1_exchange_market_create_post**](MarketApi.md#create_market_endpoint_v1_exchange_market_create_post) | **POST** /v1/exchange/market/create | Create Market Endpoint
[**retrieve_markets_endpoint_v1_exchange_market_retrieve_get**](MarketApi.md#retrieve_markets_endpoint_v1_exchange_market_retrieve_get) | **GET** /v1/exchange/market/retrieve | Retrieve Markets Endpoint


# **create_market_endpoint_v1_exchange_market_create_post**
> MarketCreationResponse create_market_endpoint_v1_exchange_market_create_post(market_detail)

Create Market Endpoint

Create multiple markets via API.  This endpoint allows users to create multiple conditional markets simultaneously.  Parameters: - market_details (List[MarketDetail]): A list of market details, each containing:     - detail (str): The description of the market     - ref_id (str): A reference identifier for the market  Returns: - MarketCreationResponse:     A dictionary containing the created markets or an error message.  Raises: - HTTPException(400): If there's a validation error or insufficient balance - HTTPException(401): If the API key is invalid - HTTPException(500): For any other unexpected errors  Note: - This endpoint requires a valid Kaziro API Key to be provided in the header. - A market creation fee will be charged for each market created. - Markets are automatically CLOSED after 10 minutes if no request accepts a reply.

### Example

* Api Key Authentication (APIKeyHeader):

```python
import kaziro
from kaziro.models.market_creation_response import MarketCreationResponse
from kaziro.models.market_detail import MarketDetail
from kaziro.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = kaziro.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyHeader
configuration.api_key['APIKeyHeader'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyHeader'] = 'Bearer'

# Enter a context with an instance of the API client
with kaziro.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = kaziro.MarketApi(api_client)
    market_detail = [kaziro.MarketDetail()] # List[MarketDetail] | 

    try:
        # Create Market Endpoint
        api_response = api_instance.create_market_endpoint_v1_exchange_market_create_post(market_detail)
        print("The response of MarketApi->create_market_endpoint_v1_exchange_market_create_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MarketApi->create_market_endpoint_v1_exchange_market_create_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **market_detail** | [**List[MarketDetail]**](MarketDetail.md)|  | 

### Return type

[**MarketCreationResponse**](MarketCreationResponse.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**400** | Bad Request |  -  |
**500** | Internal Server Error |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_markets_endpoint_v1_exchange_market_retrieve_get**
> MarketRetrievalResponse retrieve_markets_endpoint_v1_exchange_market_retrieve_get(market_ids=market_ids, status=status)

Retrieve Markets Endpoint

Retrieve markets based on optional market IDs and status.  This endpoint allows users to retrieve markets based on specific market IDs or statuses.  Parameters: - market_ids (Optional[List[str]]): A list of market IDs to filter by. If None, all markets are considered. - status (Optional[str]): The status to filter markets by. If None, markets of all statuses are returned.  Returns: - List[MarketDetail]: A list of market details based on the provided filters.  Raises: - HTTPException(401): If the API key is invalid - HTTPException(500): For any other unexpected errors  Note: - This endpoint requires a valid Kaziro API Key to be provided in the header. - A market creation fee will be charged for each market created.

### Example

* Api Key Authentication (APIKeyHeader):

```python
import kaziro
from kaziro.models.market_retrieval_response import MarketRetrievalResponse
from kaziro.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = kaziro.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyHeader
configuration.api_key['APIKeyHeader'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyHeader'] = 'Bearer'

# Enter a context with an instance of the API client
with kaziro.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = kaziro.MarketApi(api_client)
    market_ids = ['market_ids_example'] # List[str] |  (optional)
    status = 'status_example' # str |  (optional)

    try:
        # Retrieve Markets Endpoint
        api_response = api_instance.retrieve_markets_endpoint_v1_exchange_market_retrieve_get(market_ids=market_ids, status=status)
        print("The response of MarketApi->retrieve_markets_endpoint_v1_exchange_market_retrieve_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MarketApi->retrieve_markets_endpoint_v1_exchange_market_retrieve_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **market_ids** | [**List[str]**](str.md)|  | [optional] 
 **status** | **str**|  | [optional] 

### Return type

[**MarketRetrievalResponse**](MarketRetrievalResponse.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**400** | Bad Request |  -  |
**500** | Internal Server Error |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

