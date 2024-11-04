from django.http import HttpRequest, JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .models import CustomUser
from .serializers import UserRoleSerializer
import jwt
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import CustomUser
User = get_user_model()


class TelegramTokenViewSet(viewsets.ViewSet): 
    permission_classes = [permissions.IsAuthenticated]

    def generate_token(self, request):
        user = request.user
        user.generate_telegram_token()
        return Response({"telegram_token": user.telegram_token})

    def bind_telegram(self, request):
        telegram_id = request.data.get("telegram_id")
        telegram_token = request.data.get("telegram_token")

        user = CustomUser.objects.filter(telegram_token=telegram_token).first()

        if user:
            user.telegram_id = telegram_id
            user.save()
            return Response({"message": "Telegram привязан успешно!"})
        return Response({"error": "Неправильный токен"}, status=400)


class OAuthLoginViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], url_path='oauth-login')
    def oauth_login(self, request):
        token_str = request.data.get('token')
        if not token_str:
            return Response({'error': 'Token is required'}, status=400)

        try:
            token_data = jwt.decode(token_str, options={"verify_signature": False})  

            email = token_data.get('email')
            first_name = token_data.get('given_name', '')
            last_name = token_data.get('family_name', '')

            if not email:
                return Response({'error': 'Email is missing in the token'}, status=400)

            user, created = User.objects.get_or_create(email=email, defaults={
                'first_name': first_name,
                'last_name': last_name,
            })

            if created:
                user.role = 'worker'
                user.save()

            return Response({
                'status': 'logged in' if not created else 'registered',
                'email': user.email,
                'role': user.role,
            })
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired'}, status=401)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=400)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserRoleSerializer  

    @action(detail=False, methods=['post'], url_path='set-role')
    def set_role(self, request):
        user = request.user
        serializer = UserRoleSerializer(data=request.data)
        if serializer.is_valid():
            user.role = serializer.validated_data['role']
            user.save()
            return Response({'status': 'role updated'})
        return Response(serializer.errors, status=400)


# пример кода где на фронте не проверят подленость тогда надо будет разобраться болле потробнее с проверкой jwt  и 0auth
# Проверяем токен с помощью RequestToken
#
#from django.contrib.auth import get_user_model
#from rest_framework.response import Response
#from rest_framework.decorators import api_view, permission_classes
#from rest_framework import permissions
#from .authorization import RequestToken
#
#User = get_user_model()
#
#@api_view(['POST'])
#@permission_classes([permissions.AllowAny])  
#def oauth_login_view(request):
#    # Получаем JWT токен из запроса
#    token_str = request.data.get('token')
#    if not token_str:
#        return Response({'error': 'Token is required'}, status=400)
#
#    try:
#        token = RequestToken(token_str)
#        if not token.isAuthorized():
#            return Response({'error': 'Invalid token'}, status=401)
#    except Exception as e:
#        return Response({'error': str(e)}, status=400)
#
#    email = token._decoded.get('email')
#    first_name = token._decoded.get('given_name', '')
#    last_name = token._decoded.get('family_name', '')
#    role = request.data.get('role', 'worker')  
#
#    if not email:
#        return Response({'error': 'Email is missing in the token'}, status=400)
#
#    
#    user, created = User.objects.get_or_create(email=email, defaults={
#        'first_name': first_name,
#        'last_name': last_name,
#        'role': role  
#    })
#
#   
#    if created:
#        user.role = role
#        user.save()
#
#    
#    return Response({
#        'status': 'logged in' if not created else 'registered',
#        'email': user.email,
#        'role': user.role,
#    })

