from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..messageservice.mailservice import *

import random as r
import copy


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER



############## FILE UPLOAD HANDLER IMPORTS #######################
from rest_framework.parsers import JSONParser,MultiPartParser
from django.conf import settings
from django.core.files.storage import FileSystemStorage

##################################################################
class UserLoginView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        # print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token': serializer.data['token'],
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class UserRegisterView(APIView):
    def post(self, request, format=None):
        try:
            phone_number = request.data.get('phone_number')
            password = request.data.get('password')
            user = CustomUser.objects.filter(phone_number=phone_number)

            if user.count() > 0:
                return Response({
                    "error": "Account with this phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)
            otp_qs = OTP.objects.filter(phone_number=phone_number)
            if(otp_qs.count() > 0 and otp_qs[0].is_verified):
                serializer = CreateUserSerializer(data=request.data)
                try:
                    if serializer.is_valid():
                        serializer.save()
                        user = authenticate(phone_number=phone_number, password=password)
                        payload = JWT_PAYLOAD_HANDLER(user)
                        jwt_token = JWT_ENCODE_HANDLER(payload)
                        update_last_login(None, user)
                        response = {
                            'success': 'True',
                            'status code': status.HTTP_201_CREATED,
                            'message': 'User created successfully',
                            'token': jwt_token,
                        }
                        return Response(response, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({
                        "error": "Invalid Input Data"}, status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "error": "Please verify this phone number with OTP"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # print(e)
            return Response({'error': "invalid input format"}, status=status.HTTP_400_BAD_REQUEST)


class SendOtp(APIView):
    def post(self, request, format=None):
        try:
            phone_number = request.data.get('phone_number')
            user = CustomUser.objects.filter(phone_number=phone_number)
            if user.count() > 0:
                return Response({
                    "error": "Account with this phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                qs = OTP.objects.filter(phone_number=phone_number)
                if(qs.count() > 0):
                    otp = qs[0].otp
                    messagestring = f" Your Otp is : {otp}\n"
                    mailIt(body=messagestring)
                    return Response({"phone_number": phone_number}, status=status.HTTP_200_OK)
                otp = otpgen()
                entry = OTP(phone_number=phone_number, otp=otp)
                entry.save()
                messagestring = f" Your Otp is : {otp}\n"
                mailIt(body=messagestring)
                return Response({"phone_number": phone_number}, status=status.HTTP_200_OK)
            except Exception as e:
                # print(e)
                return Response({'error': "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # print(e)
            return Response({"error": "not a valid input"}, status=status.HTTP_400_BAD_REQUEST)


class ValidateOtp(APIView):
    def post(self, request, format=None):
        try:
            phone_number = request.data.get("phone_number")
            otp = request.data.get('otp')
            otp_object = OTP.objects.get(phone_number=phone_number)
            if(otp_object.otp == otp):
                otp_object.is_verified = True
                otp_object.save()
                return Response({"message": "otp matched"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "otp didn't matched"}, status=status.HTTP_200_OK)
        except Exception as e:
            # print(e)
            return Response({"error": "invalid input"}, status=status.HTTP_400_BAD_REQUEST)


class CustomerProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerProfileSerializer

    def post(self, request, format=None):

        customer_dict = copy.deepcopy(request.data)
        customer_dict['user'] = request.user.id
        serializer = self.serializer_class(data=customer_dict)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'Customer Profile Updated',
        }
        
        try:
            cordinate_obj = Cordinates(user = request.user, lat = request.data.get('lat'), lon = request.data.get('lon'))
            cordinate_obj.save()
            status_code = status.HTTP_200_OK
            return Response(response, status=status_code)
        except Exception as e:
            return Response({'error':"problem in locations"},status=status.HTTP_400_BAD_REQUEST)


class PartnerProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    # parser_classes = [MultiPartParser, ]
    serializer_class = PartnerProfileSerializer
    def post(self, request, format=None):
        try:
            # myfile = request.FILES['file']
            # fs = FileSystemStorage()
            # filename = fs.save(myfile.name, myfile)
            # uploaded_file_url = fs.url(filename)
            
            # user = request.user
            # email = request.data.get('email')
            # fullname = request.data.get('fullname')
            # gender = request.data.get('gender')
            # qualification = request.data.get('qualification')
            # # qualification_doc = request.data.get()
            # place_of_work = request.data.get('place_of_work')
            # yex = request.data.get('yex')
            # profile_obj = PartnerProfile(user = user, email = email , fullname = fullname, gender = gender,
            # qualification = qualification, place_of_work = place_of_work, yex = yex)
            # profile_obj.save()
            
            # partner_dict = copy.deepcopy(request.data)
            partner_dict  = {}
            partner_dict['user'] = request.user.id 
            partner_dict['email'] = request.data.get('email')
            partner_dict['fullname'] = request.data.get('fullname') 
            partner_dict['gender'] = request.data.get('gender')
            partner_dict['qualification'] = request.data.get('qualification') 
            partner_dict['place_of_work'] = request.data.get('place_of_work')
            partner_dict['yex'] = request.data.get('yex')
            serializer = self.serializer_class(data=partner_dict)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            print(partner_dict) 

            try:
            #     profile_obj = PartnerProfile(user=request.user,email=request.data.get('email'),
            #     fullname=request.data.get('fullname'),gender=request.data.get('gender'),qualification=request.data.get('qualification'),
            #     place_of_work=request.data.get('place_of_work'),yex=request.data.get('yex'))
            #     profile_obj.qualification_doc.save(request.user.phone_number+"_qual_doc",request.data.get('qualification_doc'))
            #     #profile_obj.place_of_work_doc.save(request.user.phone_number+"_place_proof_doc",request.data.get('place_of_work_doc'))
            #     print(profile_obj)
            #     profile_obj.save()
                try:
                    cordinate_obj = Cordinates(user = request.user, lat = request.data.get('lat'), lon = request.data.get('lon'))
                    cordinate_obj.save()
                except Exception as e:
                    return Response({'error':"problem in locations"},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # print(e)
                return Response({"error":"file saving error"}, status = status.HTTP_400_BAD_REQUEST)
            return Response({"message":"done"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            # print(e)
            return Response({'error':"invalid input"} , status = status.HTTP_400_BAD_REQUEST)
# function for otp generation
def otpgen():
    otp = ""
    for i in range(4):
        otp += str(r.randint(1, 9))
    return otp
