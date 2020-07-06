from users.models import User
from cards.models import Card
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):    
    follows = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'follows'
        ]

class UserFollowsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields =['username']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username'
        ]

class CardSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Card
        fields = [
            'id',
            'author',
            'url',
            'color',
            'font',
            'border',
            'outer_message',
            'inner_message',
            'posted_at'
        ]

