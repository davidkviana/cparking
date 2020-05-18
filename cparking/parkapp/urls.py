from django.urls import path, re_path
from parkapp import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('parking/<int:pk>/pay', views.VehiclePay.as_view()),
    path('parking/<int:pk>/out', views.VehicleOut.as_view()),
    path('parking', views.VehicleIn.as_view()),
    re_path('^parking/(?P<plate>[A-Z]{3}-[0-9]{4})$', views.VehicleHist.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
