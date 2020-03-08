from django.urls import path
from . import views
urlpatterns = [
	path('',views.showchapter, name='home'),
	path('<slug:title>/<int:chapter>/', views.showchapter, name='showchapter'),
]