from users.models import User
from cards.models import Card, Follower
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username'
        ]

class CardSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Card
        fields = [
            'user',
            'url',
            'color',
            'font',
            'border',
            'outer_message',
            'inner_message',
            'posted_at'
        ]