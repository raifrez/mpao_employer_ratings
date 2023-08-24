import sys

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

class RatingSerializer(serializers.ModelSerializer):
    employer_name = serializers.StringRelatedField(source='employer', read_only=True)
    star_rating_details = StarSystemSerializer(source='star_rating')

    class Meta:
        model = Rating
        read_only_fields = ['updated_at']
        fields = '__all__'

class RatingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingHistory
        read_only_fields = ['created_at']
        fields = '__all__'

class RatingDetailSerializer(serializers.ModelSerializer):
    employer_name = serializers.StringRelatedField(source='employer', read_only=True)
    star_rating_details = StarSystemSerializer(source='star_rating')
    rating_history = RatingHistorySerializer(source='history', many=True)

    class Meta:
        model = Rating
        read_only_fields = ['updated_at']
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        read_only_fields = ['created_at', 'updated_at']
        fields = '__all__'


    def update_rating(self, instance, paid_date):
        rating = instance.employer.rating
        due = paid_date - instance.due_date
        point_system = PointSystem.objects.filter(
                point_type='paid', 
                threshold_lower__lte=due.days, 
                threshold_upper__gte=due.days
            ).first()
        if not point_system:
            print("Relevant point system not found!", file=sys.stderr)
            return False

        updated_points = rating.points + point_system.value

        new_streak = rating.payment_streak + 1
        updated_stars = StarSystem.objects.filter(
                threshold_lower__lte=new_streak, 
                threshold_upper__gte=new_streak
            ).first()

        if not updated_stars:
            print("Relevant star system not found!", file=sys.stderr)
            return False

        data = {
            'points': updated_points,
            'star_rating': updated_stars,
            'last_paid_date': paid_date    
        }

        # remove suspension on payment
        if rating.is_suspended:
            data['is_suspended'] = False

        updated_rating = RatingSerializer(rating, data=data, partial=True)
        updated_rating.is_valid(raise_exception=True)
        updated_rating.save()

        history_record = RatingHistory.objects.create(
                rating = rating,
                stars = rating.star_rating.value,
                streak = rating.payment_streak,
                points = rating.points
            )
        
        return True

    def update(self, instance, validated_data):
        if instance.paid_date:
            raise serializers.ValidationError("Already paid")

        updated_rating = self.update_rating(paid_date=validated_data.get('paid_date'))
        if not updated_rating:
            raise serializers.ValidationError("Unable to update rating")

        instance.paid_date = datetime.now()
        instance.amount = validated_data.get('amount', instance.amount)
        instance.save()
        return instance

class PaymentDetailSerializer(serializers.ModelSerializer):
    employer_name = serializers.StringRelatedField(source='employer', read_only=True)

    class Meta:
        model = Payment
        read_only_fields = ['created_at', 'updated_at']
        fields = '__all__'

    
