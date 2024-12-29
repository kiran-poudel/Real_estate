from django.shortcuts import render,redirect
from rest_framework.views import APIView
from .models import properties,Client,Inquiry,Interaction,Appointment,Contract
from rest_framework.response import Response
from rest_framework import status,permissions,viewsets
from .serializers import PropertySerializer,ClientSerializer,InquirySerializer,InteractionSerializer,AppointmentSerializer,ContractSerializer
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action,api_view
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from django.contrib.auth import get_user_model
User= get_user_model()
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse




# Create your views here.

class ManagePropertyView(APIView):
    def get(self,request,format = None):
        try:
            user = request.user

            if not user.is_agent:
                return Response({'error':'User doesnot have necessary permissions for getting property data.'},status=status.HTTP_403_FORBIDDEN)

            slug = request.query_params.get('slug')
            if not slug:
                propertyy =properties.objects.order_by('-date_created').filter(
                    agent = user.email
                )

                propertyy = PropertySerializer(propertyy,many= True)
                return Response(propertyy.data,status=status.HTTP_200_OK)
            

            if not properties.objects.filter(
                agent = user.email,
                slug = slug
            ).exists():
                return Response({'error':'Property does not exist'},status=status.HTTP_404_NOT_FOUND)
            
            propertyy = properties.objects.get(agent = user.email,slug = slug)
            propertyy = PropertySerializer(propertyy)
            return Response(
                {'propertyy':propertyy.data},status=status.HTTP_200_OK
            )
                

        except:
            return Response({"error": "Something went wrong when retrieving property details.  "}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve_values(self,data):
        title = data['title']
        slug = data['slug']
        address = data['address']
        city = data['city']
        state = data['state']
        zipcode = data['zipcode']
        description = data['description']

        price = data['price']
        try:
            price = int(price)
        except:
            return Response({'error':'Price must be an integer'},status=status.HTTP_400_BAD_REQUEST)
            
        bedrooms = data['bedrooms']
        try:
            bedrooms = int(bedrooms)
        except:
            return Response({'error':'bedrooms must be an integer'},status=status.HTTP_400_BAD_REQUEST)

        bathrooms = data['bathrooms']
        try:
            bathrooms = float(bathrooms)
        except:
            return Response({'error':'Price must be a floating point value'},status=status.HTTP_400_BAD_REQUEST)
            
        if bathrooms <=0 or bathrooms >= 10:
            bathrooms =1.0

        bathrooms = round(bathrooms,1)

        sale_type = data['sale_type']

        if sale_type == 'FOR_RENT':
            sale_type = 'For_Rent'
        elif sale_type == 'FOR_SALE':
            sale_type = 'For_Sale'
        else:
            sale_type = 'For_Lease'

        home_type = data['home_type']

        if home_type == 'APARTMENT':
            home_type = 'Apartment'
        elif home_type == 'HOUSE':
            home_type = 'House'
        elif home_type == 'TOWNHOUSE':
            home_type = 'Townhouse'
        else:
            home_type = 'Condo'
            
        main_image = data['main_image']
        image_1 = data['image_1']
        image_2 = data['image_2']
        image_3 = data['image_3']

        is_published = data['is_published']
        if is_published == 'True':
            is_published = True
        else:
            is_published = False

        data={
            'title':title,
            'slug' :slug,
            'address' :address,
            'city' :city,
            'state' :state,
            'zipcode' :zipcode,
            'description' :description,
            'price':price,
            'bedrooms' :bedrooms,
            'bathrooms': bathrooms,
            'sale_type': sale_type,
            'home_type': home_type,
            'main_image': main_image,
            'image_1': image_1,
            'image_2':image_2,
            'image_3':image_3,
            'is_published' :is_published
        }
        return data

    def post(self,request):
        try:
            user = request.user

            if not user.is_agent:
                return Response({'error':'User doesnot have necessary permissions for creating property data.'},status=status.HTTP_403_FORBIDDEN)
            
            data = request.data
            data = self.retrieve_values(data)

            title= data['title']
            slug = data['slug']
            address = data['address']
            city = data['city']
            state = data['state']
            zipcode = data['zipcode']
            description = data['description']
            price= data['price']
            bedrooms = data['bedrooms']
            bathrooms= data['bathrooms']
            sale_type= data['sale_type']
            home_type= data['home_type']
            main_image= data['main_image']
            image_1= data['image_1']
            image_2= data['image_2']
            image_3= data['image_3']
            is_published = data['is_published']

            if properties.objects.filter(slug=slug).exists():
             return Response({'error':'Property with this slug already exists.'},status=status.HTTP_400_BAD_REQUEST)


            properties.objects.create(
                agent = user.email,
                title = title,
                slug = slug,
                address = address, 
                city = city,
                state = state,
                zipcode = zipcode,
                description = description,
                price = price,
                bedrooms = bedrooms,
                bathrooms = bathrooms,
                sale_type = sale_type,
                home_type = home_type,
                main_image = main_image,
                image_1 = image_1,
                image_2 = image_2,
                image_3= image_3,
                is_published = is_published
            )
            return Response(
                {'success':'Property created successfully'},status=status.HTTP_201_CREATED
            )

        except:
            return Response({"error": "Something went wrong while creating property"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self,request):
        try:
            user = request.user

            if not user.is_agent:
             return Response({'error':'User doesnot have necessary permissions for updating property data.'},status=status.HTTP_403_FORBIDDEN)
             
            data = request.data
            data = self.retrieve_values(data)

            title= data['title']
            slug = data['slug']
            address = data['address']
            city = data['city']
            state = data['state']
            zipcode = data['zipcode']
            description = data['description']
            price= data['price']
            bedrooms = data['bedrooms']
            bathrooms= data['bathrooms']
            sale_type= data['sale_type']
            home_type= data['home_type']
            main_image= data['main_image']
            image_1= data['image_1']
            image_2= data['image_2']
            image_3= data['image_3']
            is_published = data['is_published']

            if not properties.objects.filter(agent=user.email, slug=slug).exists():
                return Response({'error':'Property does not exist'},status=status.HTTP_404_NOT_FOUND)
            
            properties.objects.filter(agent=user.email,slug=slug).update(
                title = title,
                slug = slug,
                address = address, 
                city = city,
                state = state,
                zipcode = zipcode,
                description = description,
                price = price,
                bedrooms = bedrooms,
                bathrooms = bathrooms,
                sale_type = sale_type,
                home_type = home_type,
                main_image = main_image,
                image_1 = image_1,
                image_2 = image_2,
                image_3= image_3,
                is_published = is_published
            )
            return Response({'message':'Property updated successfully'},status=status.HTTP_200_OK)

        except:
            return Response(
                {"error":"something went wrong while updating property"},status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def patch(self,request):
        try:
            user = request.user

            if not user.is_agent:
             return Response({'error':'User doesnot have necessary permissions for updating property data.'},status=status.HTTP_403_FORBIDDEN)
            
            data = request.data
            slug = data['slug']
            is_published = data['is_published']

            if is_published == 'True':
                is_published = True
            else:
                is_published = False

            if not properties.objects.filter(agent=user.email, slug=slug).exists():
                return Response({'error':'Property does not exist'},status=status.HTTP_404_NOT_FOUND)
            
            properties.objects.filter(agent=user.email,slug=slug).update(
                is_published = is_published
            )

            return Response({'message':'Property status updated successfully'},status=status.HTTP_200_OK)


        except:
            return Response({"error":"something went wrong while updating property"},status=status.HTTP_401_UNAUTHORIZED)
        
    def delete(self,request):
        try:
            user = request.user

            if not user.is_agent:
             return Response({'error':'User doesnot have necessary permissions for deleting property data.'},status=status.HTTP_403_FORBIDDEN)
            
            data = request.data
            try:
                slug = data['slug']
            except:
                return Response({'error':'Property slug is required'},status=status.HTTP_400_BAD_REQUEST)
            


            if not properties.objects.filter(agent=user.email, slug=slug).exists():
                return Response({'error':'property you are trying to delete doesnot exist.'},status=status.HTTP_404_NOT_FOUND)

            properties.objects.filter(agent=user.email, slug=slug).delete()
            if not properties.objects.filter(agent=user.email, slug=slug).exists():
              return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error':'Failed to delete property.'},status=status.HTTP_400_BAD_REQUEST)



        except:
            return Response({"error":"something went wrong while deleting property"},status=status.HTTP_401_UNAUTHORIZED)



class PropertyDetailView(APIView):
    def get(self, request, format= None):
        try:
            slug = request.query_params.get('slug')

            if not slug:
                return Response({"error": "Please provide slug"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not properties.objects.filter(slug=slug,is_published=True).exists():
                return Response({
                    "error": " Published Property with this slug doesnot exist."}, status=status.HTTP_404_NOT_FOUND)
            
            propertyy= properties.objects.get(slug=slug,is_published=True)
            propertyy = PropertySerializer(propertyy)

            return Response(
                {
                    "property": propertyy.data
                },status=status.HTTP_200_OK
            )        
        except:
            return Response({'error':'Error while fetching property details'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class PropertyView(APIView):
     permission_classes = (permissions.AllowAny, )
     def get(self,request, format=None):
        try:
            if not properties.objects.filter(is_published =True).exists():
                return Response({"error": "No published properties found"}, status=status.HTTP_404_NOT_FOUND)
                
            propertyy = properties.objects.order_by('-date_created').filter(is_published = True)
            propertyy = PropertySerializer(propertyy, many=True)

            return Response(
                {
                    'propertyy':propertyy.data 
                },status=status.HTTP_200_OK
            )


        except:
            return Response({'error':'Error while fetching property details'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SearchPropertyView(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self, request, format=None):
        try:
            city= request.query_params.get('city')
            state= request.query_params.get('state')
            max_price= request.query_params.get('max_price')
            try:
                max_price = int(max_price)
            except:
                return Response({'error':'Invalid max price'},status=status.HTTP_400_BAD_REQUEST)
            
            
            bedrooms= request.query_params.get('bedrooms')
            try:
                bedrooms = int(bedrooms)
            except:
                return Response({'error':'bedrooms must be an integer'},status=status.HTTP_400_BAD_REQUEST)
            
            bathrooms= request.query_params.get('bathrooms')
            try:
                bathrooms = float(bathrooms)
            except:
                return Response({'error':'bathrooms must be an float'},status=status.HTTP_400_BAD_REQUEST)
            
            if bathrooms < 0 or bathrooms >=10:
                bathrooms = 1.0
            bathrooms = round(bathrooms,1)

            sale_type= request.query_params.get('sale_type')
            if sale_type == 'FOR_RENT':
             sale_type = 'For_Rent'
            elif sale_type == 'FOR_SALE':
             sale_type = 'For_Sale'
            else:
             sale_type = 'For_Lease'

            home_type= request.query_params.get('home_type')
            if home_type == 'APARTMENT':
                home_type = 'Apartment'
            elif home_type == 'HOUSE':
                home_type = 'House'
            elif home_type == 'TOWNHOUSE':
                home_type = 'Townhouse'
            else:
                home_type = 'Condo'
            
            search= request.query_params.get('search')
            if not search:
                return Response({'error':'Must pass search parameter'},status=status.HTTP_400_BAD_REQUEST)
            
            vector= SearchVector('title','description')
            query = SearchQuery(search)

            if not properties.objects.annotate(search = vector).filter(
                search=query,
                city = city,
                state = state,
                price__lte =max_price,
                bedrooms__gte = bedrooms,
                bathrooms__gte = bathrooms,
                sale_type = sale_type,
                home_type = home_type,
                is_published = True
            ).exists():
                return Response({'error':'No properties found'},status=status.HTTP_404_NOT_FOUND)
            
            propertyy = properties.objects.annotate(
                search = vector
            ).filter(
                search=query,
                city = city,
                state = state,
                price__lte =max_price,
                bedrooms__gte = bedrooms,
                bathrooms__gte = bathrooms,
                sale_type = sale_type,
                home_type = home_type,
                is_published = True
            )
            propertyy= PropertySerializer(propertyy,many=True)

            return Response({'propertyy':propertyy.data},status=status.HTTP_200_OK)
        except:
            return Response({'error':'Error while searching property.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ClientManagementViewSet(viewsets.ViewSet):



    def list(self, request):

        """List all clients."""
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)
    
    def list(self, request):

        """List all clients."""
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        """Retrieve a single client by ID."""
        client = get_object_or_404(Client, pk=pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_favorite(self, request, pk=None):
        """Add a property to the client's favorites."""
        client = get_object_or_404(Client, pk=pk)
        property_id = request.data.get('properties_id')
        property_obj = get_object_or_404(properties, pk=property_id)
        client.favorite_properties.add(property_obj)
        return Response({"status": "Property added to favorites"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def remove_favorite(self, request, pk=None):
        client = self.get_object()
        property_id = request.data.get('properties_id')
        try:
            property_obj = properties.objects.get(id=property_id)
            client.favorite_properties.remove(property_obj)
            return Response({"status": "property removed from favorites"})
        except properties.DoesNotExist:
            return Response({"error": "Property not found"}, status=404)
        
    
       # Handle inquiries
    @action(detail=True, methods=['post'])
    def make_inquiry(self, request, pk=None):
        """Create an inquiry for a property."""
        client = get_object_or_404(Client, pk=pk)
        property_id = request.data.get('property_id')
        message = request.data.get('message', '')
        property_obj = get_object_or_404(properties, pk=property_id)
        inquiry = Inquiry.objects.create(client=client, property=property_obj, message=message)
        serializer = InquirySerializer(inquiry)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Track interactions
    @action(detail=True, methods=['post'])
    def log_interaction(self, request, pk=None):
        """Log an interaction with a client."""
        client = get_object_or_404(Client, pk=pk)
        description = request.data.get('description')
        if not description:
            return Response({"error": "Description is required"}, status=status.HTTP_400_BAD_REQUEST)
        interaction = Interaction.objects.create(client=client, description=description)
        serializer = InteractionSerializer(interaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def interactions(self, request, pk=None):
        """Retrieve all interactions for a client."""
        client = get_object_or_404(Client, pk=pk)
        interactions = client.interactions.all()
        serializer = InteractionSerializer(interactions, many=True)
        return Response(serializer.data)
    

class PropertyListView(APIView):
    permission_classes = [AllowAny]  # No authentication required

    def get(self, request):
        propertyy = properties.objects.all()
        serializer = PropertySerializer(propertyy, many=True)
        return Response(serializer.data)


class AppointmentRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Appointment requested successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AppointmentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
        
    def put(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Appointment updated successfully!"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ContractManagementView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get(self, request):
        Contracts = Contract.objects.all()
        serializer = ContractSerializer(Contracts, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class ContractManagementDetailView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
        
    def put(self, request, pk):
        try:
            contracts = Contract.objects.get(pk=pk)
        except Contract.DoesNotExist:
            return Response({"error": "Contract not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContractSerializer(contracts, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Contract  updated successfully!"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)