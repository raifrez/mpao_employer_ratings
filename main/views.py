from django.db.models import Q, F, Sum
from django.db.models.functions import Abs
from django.shortcuts import get_object_or_404
from rest_framework import pagination, generics, filters, status as http_status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from django.utils import timezone
from datetime import datetime

@api_view(['GET'])
def top_five(request):
    limit = request.query_params.get('limit', 5)
    queryset = Rating.objects.all()
    queryset = queryset.select_related('employer', 'star_rating')
    queryset = queryset.order_by('-points', '-star_rating__value')[:limit]
    serializer = RatingDetailSerializer(queryset, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def bottom_five(request):
    limit = request.query_params.get('limit', 5)
    queryset = Rating.objects.all()
    queryset = queryset.select_related('employer', 'star_rating')
    queryset = queryset.order_by('points', 'star_rating__value')[:limit]
    serializer = RatingDetailSerializer(queryset, many=True)

    return Response(serializer.data)

class EmployerListView(generics.ListAPIView):
    serializer_class = EmployerSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'name']
    ordering = ['id']

    def get_queryset(self):
        name = self.request.query_params.get('filter')
        queryset = Employer.objects.all()
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentDetailSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'due_date', 'paid_date']
    ordering = ['-paid_date']
    pagination_class = pagination.CursorPagination

    def get_queryset(self):
        employer = self.request.query_params.get('employer')
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        due = self.request.query_params.get('due')

        queryset = super().get_queryset()

        queryset = queryset.select_related('employer')

        if employer:
            queryset = queryset.filter(employer__name__icontains=employer)
        if month:
            queryset = queryset.filter(due_date__month=month)
        if year:
            queryset = queryset.filter(due_date__year=year)
        if due == 'true' or due == 1:
            queryset = queryset.filter(paid_date=None)

        return queryset

class PaymentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def update(self, request, pk=None):
        data = request.data
        obj = self.get_object()
        serializer = PaymentSerializer(obj, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=http_status.HTTP_200_OK)

class RatingListView(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingDetailSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'points', 'star_rating__value', 'last_paid_date']
    ordering = ['-points']
    pagination_class = pagination.CursorPagination

    def get_queryset(self):
        employer = self.request.query_params.get('employer')
        stars = self.request.query_params.get('stars')

        queryset = super().get_queryset()

        queryset = queryset.select_related('employer', 'star_rating')

        if employer:
            queryset = queryset.filter(employer__name__icontains=employer)
        if stars:
            queryset = queryset.filter(star_rating__value=stars)

        return queryset