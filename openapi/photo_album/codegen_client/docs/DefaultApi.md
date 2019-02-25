# openapi_client.DefaultApi

All URIs are relative to *http://localhost:8080*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_photo**](DefaultApi.md#add_photo) | **POST** /users/{user_id}/photos/ | 
[**batchget_photo**](DefaultApi.md#batchget_photo) | **GET** /users/{user_id}/photos:batchGet | 
[**create_user**](DefaultApi.md#create_user) | **POST** /users | 
[**delete_photo**](DefaultApi.md#delete_photo) | **DELETE** /users/{user_id}/photos/{photo_id} | 
[**get_photo**](DefaultApi.md#get_photo) | **GET** /users/{user_id}/photos/{photo_id} | 
[**get_user**](DefaultApi.md#get_user) | **GET** /users/{user_id} | 
[**list_photos**](DefaultApi.md#list_photos) | **GET** /users/{user_id}/photos/ | 
[**update_user**](DefaultApi.md#update_user) | **PATCH** /users/{user_id} | 


# **add_photo**
> Photo add_photo(user_id, data, name=name, created_at=created_at)



Adds a photo

### Example
```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = openapi_client.DefaultApi()
user_id = 'user_id_example' # str | ID of user
data = '/path/to/file' # file | 
name = 'name_example' # str |  (optional)
created_at = 56 # int |  (optional)

try:
    api_response = api_instance.add_photo(user_id, data, name=name, created_at=created_at)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->add_photo: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| ID of user | 
 **data** | **file**|  | 
 **name** | **str**|  | [optional] 
 **created_at** | **int**|  | [optional] 

### Return type

[**Photo**](Photo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **batchget_photo**
> list[Photo] batchget_photo(user_id, photo_ids)



Gets a list of photos

### Example
```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = openapi_client.DefaultApi()
user_id = 'user_id_example' # str | ID of user
photo_ids = ['photo_ids_example'] # list[str] | a collection of photo IDs

try:
    api_response = api_instance.batchget_photo(user_id, photo_ids)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->batchget_photo: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| ID of user | 
 **photo_ids** | [**list[str]**](str.md)| a collection of photo IDs | 

### Return type

[**list[Photo]**](Photo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user**
> User create_user(user=user)



Creates a new user

### Example
```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = openapi_client.DefaultApi()
user = openapi_client.User() # User | The user to create (optional)

try:
    api_response = api_instance.create_user(user=user)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->create_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | [**User**](User.md)| The user to create | [optional] 

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_photo**
> delete_photo(user_id, photo_id)



Deletes a photo

### Example
```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = openapi_client.DefaultApi()
user_id = 'user_id_example' # str | ID of user
photo_id = 'photo_id_example' # str | ID of photo

try:
    api_instance.delete_photo(user_id, photo_id)
except ApiException as e:
    print("Exception when calling DefaultApi->delete_photo: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| ID of user | 
 **photo_id** | **str**| ID of photo | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_photo**
> Photo get_photo(user_id, photo_id)



Gets a photo

### Example
```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = openapi_client.DefaultApi()
user_id = 'user_id_example' # str | ID of user
photo_id = 'photo_id_example' # str | ID of photo

try:
    api_response = api_instance.get_photo(user_id, photo_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->get_photo: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| ID of user | 
 **photo_id** | **str**| ID of photo | 

### Return type

[**Photo**](Photo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user**
> User get_user(user_id)



Gets a user

### Example
```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = openapi_client.DefaultApi()
user_id = 'user_id_example' # str | ID of user

try:
    api_response = api_instance.get_user(user_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->get_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| ID of user | 

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_photos**
> InlineResponse200 list_photos(user_id, order_by=order_by, page_token=page_token)



Lists all photos

### Example
```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = openapi_client.DefaultApi()
user_id = 'user_id_example' # str | ID of user
order_by = 'order_by_example' # str | Ordering for the results (optional)
page_token = 'page_token_example' # str | Token for the next page (optional)

try:
    api_response = api_instance.list_photos(user_id, order_by=order_by, page_token=page_token)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->list_photos: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| ID of user | 
 **order_by** | **str**| Ordering for the results | [optional] 
 **page_token** | **str**| Token for the next page | [optional] 

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user**
> User update_user(user_id, user=user)



Updates a user

### Example
```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = openapi_client.DefaultApi()
user_id = 'user_id_example' # str | ID of user
user = openapi_client.User() # User | The user to update (optional)

try:
    api_response = api_instance.update_user(user_id, user=user)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->update_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| ID of user | 
 **user** | [**User**](User.md)| The user to update | [optional] 

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

