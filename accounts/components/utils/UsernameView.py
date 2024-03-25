from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

@method_decorator(authentication_classes([JWTAuthentication]), name='dispatch')
@method_decorator(permission_classes([IsAuthenticated]), name='dispatch')
class CurrentUserView(View):
    def get(self, request):
        # Текущий пользователь доступен через request.user благодаря JWTAuthentication
        user = request.user
        return JsonResponse({'username': user.username}, status=200)
