from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from main import views

urlpatterns = [
    # path('accounts/', views.UserAccountListView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)