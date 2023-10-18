from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from analytics.model.inference import get_inference, user_processing


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_movie_recommendations(request):
    user = request.user
    inference = get_inference(user_processing(user.id))
    return Response(inference)
