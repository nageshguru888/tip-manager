from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Tip
from .serializers import UserSerializer, LoginSerializer, TipSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.dateparse import parse_date



class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'name': user.username,
                'token': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response({"message": f"invalid field {serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class TipCalculateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"tip": serializer.validated_data['tip_amount']}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class TipListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('startDate')
        end_date = request.query_params.get('endDate')

        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            tips = Tip.objects.filter(user=request.user, created_at__range=[start_date, end_date])
        else:
            tips = Tip.objects.filter(user=request.user)

        serializer = TipSerializer(tips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
