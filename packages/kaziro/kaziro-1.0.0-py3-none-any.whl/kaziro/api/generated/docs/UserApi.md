# kaziro.UserApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**profile_endpoint_v1_user_retrieve_get**](UserApi.md#profile_endpoint_v1_user_retrieve_get) | **GET** /v1/user/retrieve | Profile Endpoint


# **profile_endpoint_v1_user_retrieve_get**
> UserProfileResponse profile_endpoint_v1_user_retrieve_get()

Profile Endpoint

### Example

* Api Key Authentication (APIKeyHeader):

```python
import kaziro
from kaziro.models.user_profile_response import UserProfileResponse
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
    api_instance = kaziro.UserApi(api_client)

    try:
        # Profile Endpoint
        api_response = api_instance.profile_endpoint_v1_user_retrieve_get()
        print("The response of UserApi->profile_endpoint_v1_user_retrieve_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->profile_endpoint_v1_user_retrieve_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**UserProfileResponse**](UserProfileResponse.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**401** | Unauthorized |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

