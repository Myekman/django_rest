from django.urls import path
from profiles import views 

# .as_view isbeacuse it is an classbased view
urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
    path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
]