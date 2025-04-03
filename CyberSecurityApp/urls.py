from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('Login', views.Login, name='Login'),
    path('AVLogin', views.AVLogin, name='AVLogin'),
    path('Register', views.Register, name='Register'),
    path('UserLogin', views.UserLogin, name='UserLogin'),
    path('AVLoginAction', views.AVLoginAction, name='AVLoginAction'),
    path('RegisterAction', views.RegisterAction, name='RegisterAction'),
    path('Upload', views.Upload, name='Upload'),
    path('UploadAction', views.UploadAction, name='UploadAction'),
    path('DownloadFile', views.DownloadFile, name='DownloadFile'),
    path('DownloadFileAction', views.DownloadFileAction, name='DownloadFileAction'),
    path('ViewStatus', views.ViewStatus, name='ViewStatus'),
    path('ViewReceived', views.ViewReceived, name='ViewReceived'),
]



'''
from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path("UserLogin", views.UserLogin, name="UserLogin"),
	       path("Login.html", views.Login, name="Login"),
	       path("Register.html", views.Register, name="Register"),
	       path("RegisterAction", views.RegisterAction, name="RegisterAction"),		
	       path("AVLogin.html", views.AVLogin, name="AVLogin"),
	       path("AVLoginAction", views.AVLoginAction, name="AVLoginAction"),	
	       path("Upload.html", views.Upload, name="Upload"),
	       path("UploadAction", views.UploadAction, name="UploadAction"),
	       path("DownloadFile", views.DownloadFile, name="DownloadFile"),
	       path("DownloadFileAction", views.DownloadFileAction, name="DownloadFileAction"),
	       path("ViewReceived", views.ViewReceived, name="ViewReceived"),
	       path("ViewStatus", views.ViewStatus, name="ViewStatus"),
]

'''