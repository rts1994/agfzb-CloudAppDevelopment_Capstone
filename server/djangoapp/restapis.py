import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#    
#                                  auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    try:
        # Call post method of requests library with URL and parameters
        payload = kwargs.pop("payload")
        response = requests.post(url, headers={'Content-Type': 'application/json'},
                                            params=kwargs, json=payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    
    #print("hi")
    if json_result:
        # Get the list of dealerships from JSON
        dealerships = json_result[0]["doc"]["dealerships"]
        #print(dealerships)
        # For each dealership object
        for dealership in dealerships:
            # Create a CarDealer object with values from the dealership dictionary
            dealer_obj = CarDealer(
                address=dealership["address"],
                city=dealership["city"],
                full_name=dealership["full_name"],
                id=dealership["id"],
                lat=dealership["lat"],
                long=dealership["long"],
                short_name=dealership["short_name"],
                st=dealership["st"],
                zip=dealership["zip"]
            )
            results.append(dealer_obj)
        
        # parse x:
        # y = json.loads(dealerships)

        # the result is a Python dictionary:
        # print(*y)
        
        return results



###### start og
    # if json_result:
    #     # Get the row list in JSON as dealers
    #     dealers = json_result
        
    #     # For each dealer object
    #     for dealer_doc in dealers:
    #         # Get its content in `doc` object
    #         # dealer_doc = dealer["doc"]
    #         # Create a CarDealer object with values in `doc` object
    #         dealer_obj = CarDealer(
    #             address=dealer_doc["address"],
    #             city=dealer_doc["city"],
    #             full_name=dealer_doc["full_name"],
    #             id=dealer_doc["id"],
    #             lat=dealer_doc["lat"],
    #             long=dealer_doc["long"],
    #             short_name=dealer_doc["short_name"],
    #             st=dealer_doc["st"],
    #             zip=dealer_doc["zip"]
    #         )
    #         results.append(dealer_obj)

    # return results
#### end og 

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)

    if json_result:
        reviews = json_result[0]["doc"]["reviews"]
        for review_doc in reviews:
            print("start")

            review_obj = DealerReview(
                dealership=review_doc.get("dealership"),
                name=review_doc.get("name"),
                purchase=review_doc.get("purchase"),
                review=review_doc.get("review"),
                purchase_date=review_doc.get("purchase_date"),
                car_make=review_doc.get("car_make"),
                car_model=review_doc.get("car_model"),
                car_year=review_doc.get("car_year"),
                # sentiment=analyze_review_sentiments(review_doc.get("review")),
                sentiment=review_doc.get("review"),
                id=review_doc.get("id")
            )
            results.append(review_obj)

        return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/73b09635-c5e3-4048-9d48-59b1788a7f09"
    api_key = "ZqQf7VC2jDWTFqnvvxoknZoUp2k-rUGHI2euoApnYtkP"
    params = {
        "text": text,
        "features": {
            "sentiment": {
            }
        },
        "language": "en"
    }
    # params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    response = requests.post(url, json=params, headers={'Content-Type': 'application/json'},
                                    auth=('apikey', api_key))
    return response.json()["sentiment"]["document"]["label"]


