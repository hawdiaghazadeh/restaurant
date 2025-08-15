from rest_framework.response import Response
from rest_framework import generics, status, permissions, views
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

# Create your views here.
class register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, req):
        serializer = self.get_serializer(data=req.data) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class login(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class change_password(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RegisterSerializer  

    def get_object(self):
        return self.request.user
    
    def update(self, request):
        user = self.get_object()
        password = request.data.get("password")
        if not password:
            return Response({"message":"password required"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return Response({"message":"password changed"}, status=status.HTTP_200_OK)
    
