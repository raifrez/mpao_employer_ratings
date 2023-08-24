from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from main import views

urlpatterns = [
    path('employers/', views.EmployerListView.as_view()),
    path('payments/', views.PaymentListView.as_view()),
    path('payments/<int:pk>/', views.PaymentDetailView.as_view()),
    path('ratings/', views.RatingListView.as_view()),
    path('ratings/top/', views.top_five),
    path('ratings/bottom/', views.bottom_five),
]

urlpatterns = format_suffix_patterns(urlpatterns)