from django.shortcuts import render
from django.views.generic import ListView
from django.shortcuts import render, redirect
from .models import *
from django.views import View
import googlemaps
from django.conf import settings 
from .forms import*
from datetime import datetime

# Create your views here.

class HomeView(ListView):
    template_name = "home.html"
    context_object_name = 'mydata'
    model = Location
    success_url = "/"

class MapView(View):
    template_name = "map.html"

    def get(self, request):
        key = settings.GOOGLE_API_KEY
        eligable_location = Location.objects.filter(place_id__isnull = False)
        location = []

        for a in eligable_location:
            data = {
                'lat': float(a.lat),
                'lng': float(a.lng),
                'name': a.name
            }
            location.append(data)
        context = {
            "key":key,
            "location":location
        }   
        return render(request, self.template_name, context) 


class DistanceView(View):
    template_name = "distance.html"

    def get(self, request):
        form = DistanceForm
        distance = Distance.objects.all()

        context = {
            'form':form,
            'distance':distance
        }

        return render(request, self.template_name, context)
    
    def post(self, request):
        form = DistanceForm(request.POST)
        if form.is_valid():
            from_location = form.cleaned_data['from_location']
            from_location_info = Location.objects.get(name = from_location)
            from_address_string = str(from_location_info.address)+", "+str(from_location_info.zipcode)+", "+str(from_location_info.city)+", "+str(from_location_info.country)

            to_location = form.cleaned_data['to_location']
            to_location_info = Location.objects.get(name = to_location)
            to_address_string = str(to_location_info.address)+", "+str(to_location_info.zipcode)+", "+str(to_location_info.city)+", "+str(to_location_info.country)

            mode = form.cleaned_data['mode']
            now = datetime.now()

            gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
            calculate = gmaps.distance_matrix(
                from_address_string,
                to_address_string,
                mode = mode,
                departure_time = now
            )
            print(calculate)

            duration_seconds = calculate['rows'][0]['elements'][0]['duration']['value']
            duration_minutes = duration_seconds/60

            distance_meters = calculate['rows'][0]['elements'][0]['distance']['value']
            distance_kilometers = distance_meters/1000

            if 'duration_in_traffic' in calculate['rows'][0]['elements'][0]:
                duration_in_traffic_seconds = calculate['rows'][0]['elements'][0]['duration_in_traffic']['value']
                duration_in_traffic_minutes = duration_in_traffic_seconds/60

            else:
                duration_in_traffic_minutes = None

            obj = Distance(
                from_location = Location.objects.get(name=from_location),
                to_location = Location.objects.get(name=to_location),
                mode = mode,
                distance_km = distance_kilometers,
                duration_mins = duration_minutes,
                duration_traffic_mins = duration_in_traffic_minutes
            )      
            obj.save()

        else:
            print(form.errors)

        return redirect('distance')        
    

class GeocodingView(View):
    template_name = "geocoding.html"

    def get(self, request, pk):
        location = Location.objects.get(pk=pk)

        if location.lng and location.lat and location.place_id != None:
            lat = location.lat
            lng = location.lng
            place_id = location.place_id
            label = "from my database" 

        elif location.address and location.country and location.zipcode and location.city !=None:
            address__string = str(location.address)+", "+str(location.zipcode)+", "+str(location.city)+", "+str(location.country)

            gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
            result = gmaps.geocode(address__string)[0]
            lat =result.get('geometry', {}).get('location', {}).get('lat', None)
            lng =result.get('geometry', {}).get('location', {}).get('lng', None)
            place_id =result.get('place_id', {})
            label = "From my api call"

            location.lat = lat
            location.lng = lng
            location.place_id = place_id
            location.save()

        else:
            result = ""
            lat = ""
            lng =""
            place_id = ""
            label = "no call Made"


        context = {
            'location':location,
            'lat':lat,
            'lng':lng,
            'place_id':place_id,
            'label':label
        }
        return render(request, self.template_name, context)



