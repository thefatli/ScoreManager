from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import User
from .serializers import UserImageSerializer

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
        # return User.objects.get(username='te')
    
    def get(self, request, *args, **kwargs):
      user = self.get_object()
      serializer = self.get_serializer(user)
      return Response(serializer.data)
