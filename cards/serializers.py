from users.models import User
from cards.models import Card, Friend
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username'
        ]

class CardSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Card
        fields = [
            'url',
            'color',
            'font',
            'border',
            'message',
            'posted_at'
        ]