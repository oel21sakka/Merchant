from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsStaff
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()

@api_view(['get'])
@permission_classes([IsStaff])
def add_staff(request):
    if not 'user_id' in request.query_params:
        return Response({"user_id": "this query param is required"}, status=status.HTTP_400_BAD_REQUEST)
    user_id = request.query_params['user_id']
    user = get_object_or_404(User, id=user_id)
    user.is_staff=True
    return Response({"message": f"user {user_id} is added to the staff"}, status=status.HTTP_200_OK)
