from rest_framework.pagination import PageNumberPagination
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import MessageSerializer, ChatSerializer
from .models import Message, Chat

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_list(request):
    # Return a list of all the chats for the authenticated user
    chats = Message.objects.filter(recipient=request.user)
    serializer = MessageSerializer(chats, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_create(request):
    # Create a new chat message
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(sender=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = PageNumberPagination

