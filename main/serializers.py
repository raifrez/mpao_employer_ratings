from rest_framework import serializers
from main.models import *

class StarSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StarSystem
        exclude = ['threshold_upper', 'threshold_lower']

class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        exclude = ['created_at', 'updated_at']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        read_only_fields = ['created_at', 'updated_at']
        fields = '__all__'

class PaymentDetailSerializer(serializers.ModelSerializer):
    employer_name = serializers.StringRelatedField(source='employer', read_only=True)

    class Meta:
        model = Payment
        read_only_fields = ['created_at', 'updated_at']
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    star_rating_details = StarSystemSerializer(field=star_rating)
    
    class Meta:
        model = Rating
        read_only_fields = ['updated_at']
        fields = '__all__'

class RatingDetailSerializer(serializers.ModelSerializer):
    employer_name = serializers.StringRelatedField(source='employer', read_only=True)

    class Meta:
        model = Rating
        read_only_fields = ['updated_at']
        fields = '__all__'

class RatingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingHistory
        read_only_fields = ['created_at']
        fields = '__all__'