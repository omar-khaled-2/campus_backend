from django.urls import path
from .views import Register,UserDetail,UserPassword,StudentCourses,UserProfilePicture,TokenObtain,ForgotPassword,ChangeEmail,GoogleLogin,LinkGoogle,LoginMethods,StudentGroup,DeviceDetail,UserPermissions,ValidateEmail,GenerateOtp

urlpatterns = [
    path('token/',TokenObtain.as_view()),
    path('google/',GoogleLogin.as_view()),
    path('register/', Register.as_view()),
    path('forgot-password/',ForgotPassword.as_view()),
    path('user/password/',UserPassword.as_view()),
    path('user/',UserDetail.as_view()),
    path('user/permissions/',UserPermissions.as_view()),
    path('user/profile-pic/',UserProfilePicture.as_view()),
    path('user/device-token/',DeviceDetail.as_view()),
    path('student/courses',StudentCourses.as_view()),
    path('student/courses/<str:course_code>/group/',StudentGroup.as_view()),
    path('generate-otp/',GenerateOtp.as_view()),
    path('user/email/',ChangeEmail.as_view()),
    path("user/login-methods/google",LinkGoogle.as_view()),
    path("user/login-methods/",LoginMethods.as_view()),
    path("validate-email/",ValidateEmail.as_view()),

]

