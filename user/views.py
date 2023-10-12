from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer,SignUpSerilizer,ForgotPasswordSerializer,ResetPasswordSerializer,ChangePasswordSerializer,ChangeProfilePicSerializer,SignInSerilizer,NameSerilizer,EmailUniqueSerilizer,ChangeEmailSerializer,PasswordSerilizer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db.models import F
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import AllowAny
from academic.serializers import CourseSerializer
from academic.models import Course
from django.conf import settings
from django.core.mail import send_mail
from os import path
from PIL import Image
from django.contrib.auth.models import Group
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from rest_framework.exceptions import AuthenticationFailed,APIException,NotFound
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from jwt import encode,decode
import datetime
from .models import OTP,GoogleUser,Device,StudentGroupCourse,Student
from django.db import IntegrityError
import boto3


from rest_framework.generics import CreateAPIView,UpdateAPIView,DestroyAPIView,ListAPIView
def get_token(user):
    payload = {
        "id":user.id
    }
    token = encode(payload,settings.SECRET_KEY,algorithm=settings.JWT_ALGORITHM)
    return token


class EmailOrPasswordInvalid(AuthenticationFailed):
    default_detail = "Oops! Incorrect Email or password. Please verify and retry"

class EmailTaken(APIException):
    status_code = 409
    default_detail = "Uh-oh! The Email you're trying to use is already taken"


class PasswordInvalid(APIException):
    status_code = 400
    default_detail = "Password invalid"

class OTPInvalid(APIException):
    status_code = 400
    default_detail = "Invalid OTP"


class GoogleAccountNotFound(APIException):
    status_code = 404
    default_detail = "Account not found for this Google account. Please check your credentials"


class TokenObtain(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):

        serilizer = SignInSerilizer(data = request.data)
        serilizer.is_valid(raise_exception=True)
    
        try:
            user = get_user_model().objects.get(email = serilizer.validated_data['email'])

        except ObjectDoesNotExist:
            raise EmailOrPasswordInvalid()
        if not user.check_password(serilizer.validated_data['password']):
            raise EmailOrPasswordInvalid()
        token = get_token(user)
        response_data = {
            'token': token,
        }
        return Response(response_data,status= status.HTTP_200_OK)



class Register(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self,request):
        serilizer = SignUpSerilizer(data = request.data)
        serilizer.is_valid(raise_exception=True)

    
        first_name = serilizer.validated_data['first_name']
        last_name = serilizer.validated_data['last_name']
        email = serilizer.validated_data['email']
        password = serilizer.validated_data['password']

        academic_id = serilizer.validated_data['academic_id']



        user = get_user_model().objects.create_user(first_name = first_name,last_name = last_name,email = email,password = password)

        print(user)
    
        Student.objects.create(academic_id = academic_id,user = user)
        student_group = Group.objects.get(name='student')

        user.groups.add(student_group)
        token = get_token(user)
        response_data = {
            'token': token,
        }
        return Response(response_data,status= status.HTTP_201_CREATED)
    
class LinkGoogle(APIView):
    def post(self,request):
        google_id = request.data['google_id']
        user = request.user
        GoogleUser.objects.create(user = user,google_id = google_id)
        return Response(status= status.HTTP_201_CREATED)

    
    def delete(self,request):
  
        user = request.user

        GoogleUser.objects.get(user = user).delete()

        return Response(status= status.HTTP_204_NO_CONTENT)
        


class LoginMethods(APIView):
    def get(self,request):
        user = request.user
        is_google_linked = GoogleUser.objects.filter(user = user).exists()
        is_apple_linked = False

        return Response({
            "google" : is_google_linked,
            "apple" : is_apple_linked
        },status= status.HTTP_200_OK)
        


class GoogleLogin(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            google_id = request.data['google_id']
            print(GoogleUser.objects.filter(google_id = google_id))
            googleUser = GoogleUser.objects.get(google_id = google_id)
            token = get_token(googleUser.user);
            response_data = {
                'token': token,
            }
            return Response(response_data,status= status.HTTP_201_CREATED)
        except GoogleUser.DoesNotExist:
            raise GoogleAccountNotFound()
        
class UserDetail(APIView):
    def get(self,request):
        user = request.user
        permissions = user.get_all_permissions()
        serializer = UserSerializer(instance = request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request):
        serilizer = NameSerilizer(data=request.data)
        serilizer.is_valid(raise_exception=True)
        first_name = serilizer.validated_data['first_name']
        last_name = serilizer.validated_data['last_name']
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return Response(status=status.HTTP_201_CREATED)
    
    def delete(self,request):
        user = request.user
        serilizer = PasswordSerilizer(data = request.data)
        serilizer.is_valid(raise_exception=True)
        password = serilizer.validated_data['password']
        password_match = user.check_password(password)
        if not password_match:
            raise PasswordInvalid()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserPermissions(APIView):

    def get(self,request):
        user = request.user
        permissions = user.get_all_permissions()
        return Response(permissions,status=status.HTTP_200_OK)

    
       

class UserPassword(APIView):
    def put(self,request):
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        serilizer = ChangePasswordSerializer(data = request.data)
        serilizer.is_valid(raise_exception=True)
        user = request.user
        password_match = user.check_password(old_password)
        if not password_match:
            raise PasswordInvalid()
        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_200_OK)



class ValidateEmail(APIView):
    def post(self,request):
        print(request.data)
        serializer = EmailUniqueSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)



class ChangeEmail(APIView):
    
    def put(self,request):
        user = request.user
        serilizer = ChangeEmailSerializer(data = request.data)
        serilizer.is_valid(raise_exception=True)
        secret = serilizer.validated_data['otp']
        email = serilizer.validated_data['email']
        try:
            otp = OTP.objects.get(user = user)
            if otp.secret != secret:
                raise OTPInvalid()
            user.email = email
            user.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        except OTP.DoesNotExist:
            raise NotFound("OTP does not exist")

class GenerateOtp(APIView):
    def post(self,request):
        user = request.user
        otp = OTP.generate(user = user)
        return Response(otp.secret,status=status.HTTP_201_CREATED)


class StudentCourses(ListAPIView):
    serializer_class = CourseSerializer
    pagination_class = None
    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(studentgroupcourse__student__user=user)
    
    
class StudentGroup(APIView):
    def put(self,request,course_code):
        try:
            group_id = request.data['group_id']
            user = request.user
            course = Course.objects.get(code = course_code)
            group = course.group_set.get(pk = group_id)
            StudentGroupCourse.objects.update_or_create(
                course=course, student=user.student,
                defaults={'group': group},
            )
            return Response(status=status.HTTP_201_CREATED)
            
        except Course.DoesNotExist:
            raise NotFound("Course does not exist")
        
        except Group.DoesNotExist:
            raise NotFound("Group does not exist")
    
    def delete(self,request,course_code):
        try:
            user = request.user
            course = Course.objects.get(code = course_code)
            StudentGroupCourse.objects.filter(course=course, student=user.student).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            raise NotFound("Course does not exist")
        
    


    


    

class UserProfilePicture(APIView):
    def delete(self,request):
        user = request.user
        if user.profile_pic != settings.DEFAULT_PROFILE_PIC :
            user.profile_pic.delete(save = False)
            user.profile_pic = settings.DEFAULT_PROFILE_PIC
            user.save()
        serilizer = ChangeProfilePicSerializer(user)
   
        return Response(serilizer.data)

    def put(self,request):
        user = request.user
        serilizer = ChangeProfilePicSerializer(data=request.data)
        serilizer.is_valid(raise_exception=True)
        profile_pic = serilizer.validated_data['profile_pic']
        if user.profile_pic != settings.DEFAULT_PROFILE_PIC :
            user.profile_pic.delete(save = False)
        img = Image.open(profile_pic)
        width, height = img.size
        if width > height:
            left = (width - height) / 2
            top = 0
            right = width - left
            bottom = height
        else:
            top = (height - width) / 2
            left = 0
            right = width
            bottom = height - top
        img = img.crop((left, top, right, bottom))
        img.thumbnail((300, 300))
        buffer = io.BytesIO()
        img.save(fp=buffer, format='JPEG')
        user.profile_pic.save(profile_pic.name, 
            InMemoryUploadedFile(
                buffer,       
                None,          
                profile_pic.name,         
                'image/jpeg',     
                buffer.tell,
                None
            ),
            save = True
        )

        serilizer = ChangeProfilePicSerializer(user)

        return Response(serilizer.data,status=status.HTTP_202_ACCEPTED)
    





class ForgotPassword(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    

    def post(self,request):
        serilizer = ForgotPasswordSerializer(data= request.data)
        serilizer.is_valid(raise_exception=True)
        email = serilizer.validated_data['email']
        user = get_user_model().objects.get(email = email);
        from_email = settings.EMAIL_HOST_USER
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        token = encode({"id":user.id,"action":"reset-password","exp":expiration_time},"sphinx")
        subject = 'Reset Your Password'
        message = f"""
            Dear {user.first_name},

            We recently received a request to reset the password associated with your account. If you did not initiate this request, please ignore this email. If you did request a password reset, please follow the instructions below.

            To reset your password, click on the following link:
            [Password Reset Link]

            Please note that this link is valid for the next 24 hours. If you do not reset your password within this time frame, you may need to request another password reset.

            If you have any questions or need further assistance, please don't hesitate to contact our support team at {from_email}.

            Thank you for using our services.

            Best regards,
            Campus
            Support Team
        """
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)
        return Response(token,status=status.HTTP_200_OK)


class TokenExpired(APIException):
    default_code = "400"
    default_detail = "Password reset link has expired"

class ResetPassword(APIView):
    def post(self,request):
        token = request.data["token"]
        payload = decode(token, "sphinx")
        exp_time = payload['exp']
        current_time = datetime.datetime.utcnow()
        if current_time > datetime.datetime.fromtimestamp(exp_time):
            raise TokenExpired()
        serilizer = ResetPasswordSerializer(data=request.data)
        serilizer.is_valid(raise_exception=True)
        id = payload['id']
        password = serilizer.validated_data['password']
        user = get_user_model().objects.get(pk = id)
        user.set_password(password)
        return Response()
    

class DeviceDetail(APIView):
    def put(self,request):
        device_token = request.data['device_token']
        user = request.user
        platform = request.META["HTTP_PLATFORM"]
        
        Device.objects.get_or_create(token=device_token,user=user,platform=platform)
        return Response(status=status.HTTP_200_OK)
    
    def delete(self,request):
        device_token = request.data['device_token']
        Device.objects.get(token=device_token).delete()
        return Response(status=status.HTTP_200_OK)
