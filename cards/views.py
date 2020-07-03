from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, views
from users.models import User 
from cards.models import Card
from cards.serializers import UserSerializer, CardSerializer, UserFollowsSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]



class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        cards = request.user.cards.all()
        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)



class UserFollowsView(views.APIView):
    def get(self, request, username, format=None):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user.follows.all(), many=True, context={'request':request})
        return Response(serializer.data)
        
    def post(self, request, username, format=None):
        user = get_object_or_404(User, username=username)
        serializer = UserFollowsSerializer(self.request.user.follows.all(), many=True, context={'request':request})
        return Response(serializer.data)
        
