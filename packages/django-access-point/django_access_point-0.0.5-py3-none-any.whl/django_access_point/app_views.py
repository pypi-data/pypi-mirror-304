from rest_framework import viewsets
from .models import UserBase
from .serializers import UserSerializer

# Platform User ViewSet
class PlatformUserViewSet(viewsets.ModelViewSet):
    queryset = UserBase.objects.filter(user_type='platform')  # Only platform users
    serializer_class = UserSerializer

