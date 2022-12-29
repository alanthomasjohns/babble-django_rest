from rest_framework.permissions import (IsAuthenticated, IsAuthenticatedOrReadOnly)
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from .permissions import *
from .serializers import *
from rest_framework.response import Response
from .emails import send_otp_via_email
from .models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import views, generics
# from notifications.models import Notification
from rest_framework import status, mixins, viewsets, filters
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView
from django.http import Http404
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter


# Create your views here.


class RegisterAPI(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data['email'])
                return Response({
                    'status' : 200,
                    'message' : 'Registration successful, check email',
                    'data' : serializer.data
                })

            return Response(serializer.errors)

        except Exception as e:
            print(e)



class VerifyOTP(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data = data)

            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = Account.objects.filter(email = email)
                if not user.exists():
                    return Response({
                        'status' : 400,
                        'message' : 'something went wrong',
                        'data' : 'invalid email'
                    })

                if not user[0].otp == otp:
                    return Response({
                        'status' : 400,
                        'message' : 'something went wrong',
                        'data' : 'wrong otp'
                    })

                user = user.first()
                user.is_verified = True
                refresh = RefreshToken.for_user(user)
                print(user)
                print(refresh)
                user.save()

                return Response({
                    'status' : 200,
                    'message' : 'account verified',
                    'refresh' : str(refresh),
                    'access' : str(refresh.access_token),
                    'data' : {}
                })

            return Response({
                'status' : 400,
                'message' : 'something went wrong',
                'data' : serializer.errors
            })

        except Exception as e:
            print(e)




class LoginAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            print("++++++++++++++++++++++++++++++++")
            print(data)
            print("+++++++++++++++++++++++++++++++++++")
            serializer = LoginSerializer(data = data)
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']
                 
                user = authenticate(username=email, password=password)
                print("___________")
                print(user)
                print("___________")
                if email is None:
                    return Response({
                        'status' : 400,
                        'message' : 'something went wrong',
                    })

                print("******************************")
                print(email)
                print("*******************")

            

                if email is not None:
                    return Response({
                        'status' : 200,
                        'message' : 'Login successful'
                    })

            return Response({
                'status' : 400,
                'message' : 'Something went wrong',
                'data' : serializer.errors
            })
        except Exception as e:
            print(e)



    


class UserProfileView(views.APIView):
    serializer_class = UserProfileSerializer
    
    def get(self, request, profile_id):
        try:
            user = UserProfile.objects.get(id=profile_id)
        except:
            raise Http404
        serializer = UserProfileSerializer(user, context={'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)

  







# class LoginAPI(APIView):
#     def post(self, request):
#         try:
#             data = request.data 
#             serializer = LoginSerializer(data=request.data)
#             if serializer.is_valid():
#                 user = serializer.data['email']
#                 password = serializer.data['password']

#                 user = authenticate(email=email, password=password)
#                 refresh = RefreshToken.for_user(user)
#                 print(refresh)

#                 if user is None:
#                     return Response({
#                         'status' : 400,
#                         'message' : 'Invalid credentials',
#                         'data' : serializer.errors
#                     })

#                 if user.is_verified() is True:
#                     return Response({
#                         'status' : 200,
#                         'refresh' : str(refresh),
#                         'access' : str(refresh.access_token),
#                         'data' : {}
#                     })


#                 # return Response({
#                 #     'status' : 200,
#                 #     'refresh' : str(refresh),
#                 #     'access' : str(refresh.access_token)
#                 # })

#             return Response({
#                 'status' : 400,
#                 'message' : 'Something went wrong',
#                 'data' : serializer.errors
#             })
#         except Exception as e:
#             print(e)


class UserDetails(APIView):
    def get_object(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except:
            return Http404

    def get(self, request, pk, format=None):
        userData=self.get_object(pk)
        serializer = UserDataSerializer(userData)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        userData = self.get_object(pk)
        serializer = UserDataSerializer(userData, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({
            'status' : 400,
            'data'  : serializer.errors
        })

    def delete(self, request, pk, format=None):
        userData = self.get_object(pk)
        userData.delete()
        return Response({
            'status' : 200,
            'message' : "Your account has been permanently deactivated"
        })


class setPagination(PageNumberPagination):
    page_size = 2



class SearchAPI(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = UserDataSerializer
    pagination_class = setPagination
    filter_backends = (SearchFilter,)
    search_fields = ('first_name', 'last_name')
            