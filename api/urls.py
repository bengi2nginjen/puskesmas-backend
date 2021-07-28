from api.controller.UserController import UserController
from django.urls import path,include
from api.controller.FormController import FormController
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from userauth.serializer import CustomTokenObtainPairView
from . import views

router = routers.SimpleRouter()
router.register(r'Form', FormController,basename='Form')
router.register(r'User', UserController,basename='User')
# urlpatterns = router.urls
urlpatterns = [
    # path('Form/', FormController.as_view()),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('',views.index, name="index")
]
urlpatterns += router.urls
# urlpatterns = format_suffix_patterns(urlpatterns)