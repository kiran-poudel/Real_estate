from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions,status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User= get_user_model()
from .serializers import UserSerializer




# Create your views here.

class RegisterView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        try:
            data = request.data 

            name = data['name']
            email = data['email']
            password = data['password']
            re_password = data['re_password']
            is_agent = data['is_agent']

            if is_agent == 'True':
                is_agent = True

            else:
                is_agent = False

            if password == re_password:
                if len(password)>=8:
                    if not User.objects.filter(email = email).exists():
                        if not is_agent:
                            User.objects.create_user(name = name ,email = email ,password=password)

                            return Response('User created successfully',status=status.HTTP_201_CREATED)   
                        else:
                            User.objects.create_agent(name = name,email = email,password=password)  

                            return Response('Agent created successfully',status=status.HTTP_201_CREATED)                   
                    else:
                        return Response('User with this email already exists',status=status.HTTP_400_BAD_REQUEST)                     
                else:
                    return Response('Password must be atleast 8 character',status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response('Password doesnot match',status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response("Something went wrong when registering an account",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RetrieveUserView(APIView):

    def get(self, request, format = None):
        try:
           users = request.user
           users = UserSerializer(users)
           return Response(users.data,status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong during retrieving data',status=status.HTTP_500_INTERNAL_SERVER_ERROR)


