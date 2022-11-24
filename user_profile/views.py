from django.shortcuts import render
from rest_framework import viewsets,permissions
from .permissions import IsOwnerOrReadOnly 
from user.models import UserProfile
from .serializers import profileSerializer
# Create your views here.
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = profileSerializer
    permission_classes =[permissions.IsAuthenticated,IsOwnerOrReadOnly]


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
        