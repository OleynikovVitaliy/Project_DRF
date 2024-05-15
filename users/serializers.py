from rest_framework import serializers

from users.models import User, Payments


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели пользователя """

    class Meta:
        model = User
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели платежа """
    class Meta:
        model = Payments
        fields = '__all__'
