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
    
    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def all(self, request):
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)




class UserFollowsView(views.APIView):
    def get(self, request, format=None):
        user = request.user
        serializer = UserFollowsSerializer(user, many=True, context={'request':request})
        return Response(serializer.data)
        
    def post(self, request, format=None):
        serializer = UserFollowsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        
