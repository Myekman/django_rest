from django.urls import path
from profiles import views 

# .as_view isbeacuse it is an classbased view
urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
]