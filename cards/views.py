from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, views
from users.models import User 
from cards.models import Card
from cards.serializers import UserSerializer, CardSerializer, UserFollowsSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]



class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(author__fans=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['GET', 'POST'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        cards = request.user.cards.all()
        
        page = self.paginate_queryset(cards)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET', 'POST'], permission_classes=[permissions.IsAuthenticated])
    def all(self, request):
        cards = Card.objects.all()
        page = self.paginate_queryset(cards)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)

class UserFollowsView(views.APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request, format=None):
        usernames = [user.username for user in request.user.followed_users.all()]
        return Response(usernames)
        
    def post(self, request, format=None):
        username = request.data["user"]
        user = User.objects.get(username=username)
        request.user.followed_users.add(user)
        return Response(request.data)

class UnfollowView(views.APIView):
    def get(self, request, followed_user_username, format=None):
        usernames = [user.username for user in request.user.followed_users.all()]
        return Response(usernames)

    def delete(self, request, followed_user_username, format=None):
        user_to_unfollow = get_object_or_404(request.user.followed_users,username=followed_user_username)
        request.user.followed_users.remove(user_to_unfollow)
        return Response(request.data)