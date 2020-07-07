from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, views
from users.models import User 
from cards.models import Card
from cards.serializers import UserSerializer, CardSerializer, UserFollowsSerializer, AuthorSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS or (request.user and request.user.is_authenticated))

    def has_object_permission(self, request, view, obj):
        return bool(request.method in permissions.SAFE_METHODS or (request.user and request.user.is_authenticated and obj.author == request.user))


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def my_cards(self, request):
        cards = request.user.cards.all()
        
        page = self.paginate_queryset(cards)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def followed_users_cards(self, request):
        cards = Card.objects.filter(author__fans=self.request.user)
        page = self.paginate_queryset(cards)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)


class UserFollowsView(views.APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request, format=None):
        user_follows = request.user.followed_users.all()
        serializer = AuthorSerializer(user_follows, many=True, context={'request': request})
        return Response(serializer.data)
        
    def post(self, request, format=None):
        username = request.data["user"]
        user = User.objects.get(username=username)
        request.user.followed_users.add(user)
        serializer = AuthorSerializer(user, context={"request": request})
        return Response(serializer.data)


class UnfollowView(views.APIView):
    def get(self, request, followed_user_username, format=None):
        usernames = [user.username for user in request.user.followed_users.all()]
        return Response(usernames)

    def delete(self, request, followed_user_username, format=None):
        user_to_unfollow = get_object_or_404(request.user.followed_users,username=followed_user_username)
        request.user.followed_users.remove(user_to_unfollow)
        return Response(request.data)