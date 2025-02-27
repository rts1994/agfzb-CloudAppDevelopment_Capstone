from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarDealer, CarMake, CarModel, DealerReview
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .restapis import get_request, get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id_from_cf
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}

    if request.method == "GET":
        #url = "https://9aa2e73d-04a9-491c-9002-b01932eea12d-bluemix.cloudantnosqldb.appdomain.cloud/dealerships/dealer-get"
        #og
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/c0aa41f6-e40b-423d-aad3-bcbeebb7ab6b/default/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        
        #print (*dealerships)
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
        context['dealerships'] = dealerships
    return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/c0aa41f6-e40b-423d-aad3-bcbeebb7ab6b/default/get-reviews"
        # print("reviews")
        # print(url)
        reviews = get_dealer_reviews_from_cf(url)
        print(reviews)
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in reviews])
        # Return a list of dealer short name
        # return HttpResponse(dealer_names)
        context['reviews'] = filter(lambda x: x.id == dealer_id, reviews)
        print("context reviews")
        print(context)
        #context['dealer_id'] = dealer_id
        #context['dealer'] = get_dealer_detail_infos(dealer_id)
    return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
# def add_review(request, dealer_id):
#     print("********************add_review!!!!: ")
#     print(dealer_id)
#     print(request.method)
#     if request.method == "GET":
#         context = {}
#         context['dealer_id'] = dealer_id
#         context['dealer'] = get_dealer_detail_infos(dealer_id)
#         context['cars'] = CarModel.objects.all()
#         print("^^^^^^^^^^^^HELLO^^^^^^^^^^^^^")
#         print(context)
#         return render(request, 'djangoapp/add_review.html', context)
#     if request.method == "POST":
#         url = "https://5bde1960.us-south.apigw.appdomain.cloud/api/review-post"
#         payload = {}
#         payload['name'] = request.POST['username']
#         payload['dealership'] = dealer_id
#         payload['review'] = request.POST['review']
#         payload['purchase'] = request.POST['purchase']
#         payload['purchase_date'] = request.POST['purchase_date']
#         car = CarModel.objects.get(id = request.POST['car'])
#         if car:
#             payload['car_make'] = car.make.name
#             payload['car_model'] = car.name
#             payload['car_year'] = car.year.strftime("%Y")
#         store_review(url, payload)
#     return redirect('djangoapp:dealer_details', dealer_id = dealer_id)


def add_review(request, dealer_id):
    context = {}
    # dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/CD0201-xxx-nodesample123_Tyler/dealership-package/get-dealerships"
    dealer_url = "https://us-east.functions.appdomain.cloud/api/v1/web/c0aa41f6-e40b-423d-aad3-bcbeebb7ab6b/default/get-dealership"
    dealer = get_dealer_by_id_from_cf(dealer_url, dealer_id)
    context["dealer"] = dealer
    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars
        print("carsssssssssssssssssssss")
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            payload = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = id
            payload["id"] = id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchasedate"]           
            payload["car_model"] = car.name
            new_payload = {}
            new_payload["review"] = payload
            # review_post_url = "https://us-south.functions.appdomain.cloud/api/v1/web/CD0201-xxx-nodesample123_Tyler/dealership-package/post-review"
            review_post_url = "https://us-east.functions.appdomain.cloud/api/v1/web/c0aa41f6-e40b-423d-aad3-bcbeebb7ab6b/default/post-review"
            post_request(review_post_url, new_payload, dealer_id)
        return redirect("djangoapp:dealer_details", dealer_id)

def get_dealer_detail_infos(dealer_id):
    url = "https://us-east.functions.appdomain.cloud/api/v1/web/c0aa41f6-e40b-423d-aad3-bcbeebb7ab6b/default/get-dealership"
    dealerships = get_dealers_from_cf(url)
    print("delaerhsup")
    print(dealerships)
    return next(filter(lambda x: x.id == dealer_id, dealerships))
