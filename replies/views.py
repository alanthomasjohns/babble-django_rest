from rest_framework import permissions
from user.permissions import IsOwnerOrReadOnly
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Reply
from . serializers import ReplySerializer


# Create your views here.
class ReplyViewSet(viewsets.ModelViewSet):
    """Comments"""
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
