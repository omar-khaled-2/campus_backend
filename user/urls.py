from django.urls import path
from .views import Register,UserDetail,UserPassword,StudentCourses,UserProfilePicture,TokenObtain,ForgotPassword,ChangeEmailGenerateOTP,ChangeEmail,GoogleLogin,LinkGoogle,LoginMethods,StudentGroup,DeviceTokenDetail

urlpatterns = [
    path('token/',TokenObtain.as_view()),
    path('google/',GoogleLogin.as_view()),
    path('register/', Register.as_view()),
    path('forgot-password/',ForgotPassword.as_view()),
    path('user/password',UserPassword.as_view()),
    path('user/',UserDetail.as_view()),
    path('user/profile-pic',UserProfilePicture.as_view()),
    path('user/device-token',DeviceTokenDetail.as_view()),
    path('student/courses',StudentCourses.as_view()),
    path('student/courses/<str:course_code>/group/',StudentGroup.as_view()),
    path('user/email/generate-otp/',ChangeEmailGenerateOTP.as_view()),
    path('user/email',ChangeEmail.as_view()),
    path("user/login-methods/google",LinkGoogle.as_view()),
    path("user/login-methods/",LoginMethods.as_view())
]

