from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from credits_api.models import UserCredits
from rest_framework import status
import requests

@api_view(['GET'])
# connect to API 1
def retrieve_credits(request):
    try:
        token = request.query_params.get('token')
        user_token = UserCredits.objects.get(user_token = token)

        return Response({'credits':user_token.current_credits}, status=status.HTTP_200_OK)
    except:
        return Response({'error': "bad request"}, status=status.HTTP_400_BAD_REQUEST)
    
# connect to API 2
@api_view(['POST'])
def send_credits_information(request, endpoint):
    try:
        user_token = request.data.get('user_token')

        user_credits = UserCredits.objects.get(user_token=user_token)

        data = {
            'user_token': user_credits.user_token,
            'current_credits': user_credits.current_credits,
        }

        response = requests.post(endpoint, json=data)
        if response.status_code == 200:
            return Response({'message': 'Credits information sent successfully'}, status=200)
        else:
            return Response({'message': 'Failed to send credits information', 'error': response.text}, status=response.status_code)

    except UserCredits.DoesNotExist:
        return Response({'message': 'User token not found'}, status=404)
    except Exception as e:
        return Response({'message': f'An error occurred: {str(e)}'}, status=500)