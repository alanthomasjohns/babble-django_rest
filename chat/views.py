from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Conversation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import Account as User
from .serializers import ConversationListSerializer, ConversationSerializer, MessageSerializer
from django.db.models import Q
from django.shortcuts import redirect, reverse


# Create your views here.
@api_view(['POST'])
def start_convo(request):
    data = request.data
    print(f'data : {data}')
    email = data.pop('email')
    print(email)
    text = data.get('text')

    try:
        participant = User.objects.get(email=email)
        print(participant)
    except User.DoesNotExist:
        return Response({'message': 'You cannot chat with a non existent user',
        'email' : email})
    

    conversation = Conversation.objects.filter(Q(initiator=request.user, receiver=participant) |
                                               Q(initiator=participant, receiver=request.user))
    print(conversation)

    if conversation.exists():
        print('ddd',conversation[0].id)
        return redirect(reverse('get_conversation', args=(conversation[0].id,)))
    else:                                
        conversation = Conversation.objects.create(initiator=request.user, receiver=participant)
        return Response(ConversationSerializer(instance=conversation).data)


@api_view(['POST', 'GET'])
def get_conversation(request, convo_id):
    conversation = Conversation.objects.filter(id=convo_id)
    if not conversation.exists():
        return Response({'message': 'Conversation does not exist'})
    else:
        serializer = ConversationSerializer(instance=conversation[0])
        return Response(serializer.data)


@api_view(['POST','GET'])
def conversations(request):
    conversation_list = Conversation.objects.filter(Q(initiator=request.user) |
                                                    Q(receiver=request.user))
    serializer = ConversationListSerializer(instance=conversation_list, many=True)
    return Response(serializer.data)
