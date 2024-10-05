from rest_framework import serializers
from .models import User, Tip
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'pro_pic', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user:
            refresh = RefreshToken.for_user(user)
            return {'token': str(refresh.access_token), 'name': user.name}
        raise serializers.ValidationError("Invalid credentials")


class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = ['place', 'total_amount', 'tip_percentage', 'tip_amount', 'created_at']


    def create(self, validated_data):
        total_amount = validated_data['total_amount']
        tip_percentage = validated_data['tip_percentage']
        tip_amount = total_amount * (tip_percentage / 100)
        validated_data['tip_amount'] = tip_amount
        return super().create(validated_data)