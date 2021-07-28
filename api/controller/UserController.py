from inspect import isabstract
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import IsAuthenticated
from api.models.Response import Response
from userauth.serializer import UserSerializer
from api.models.User import CreateUserRequest, EditUserRequest, UserModelView
from rest_framework.generics import RetrieveAPIView
from userauth.models import CustomUserManager, UserModel
from django.http.response import HttpResponse, HttpResponseForbidden, JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view,action, permission_classes
from rest_framework import viewsets
import jsons

class UserController(viewsets.ViewSet):
    # permission_classes_by_action = {'CreateUser': [IsAuthenticated]}

    # def get_permissions(self):
    #     try:
    #         # return permission_classes depending on `action` 
    #         return [permission() for permission in self.permission_classes_by_action[self.action]]
    #     except KeyError: 
    #         # action is not set return default permission_classes
    #         return [permission() for permission in self.permission_classes]

    # @action(detail=False, methods=['post'])
    # def Login(self,request):
    #     if(request.POST is not None):
    #         print(request.POST)
    #         return HttpResponse("OK")
    
    
    @action(detail=False,methods=['post'])
    def CreateUser(self,request):
        if request.POST is not None:
            if not isinstance(request.user,AnonymousUser):
                userRequest = jsons.load(request.data,CreateUserRequest)
                nama = userRequest.nama
                username = userRequest.username
                jabatan = userRequest.jabatan
                password = userRequest.password
                isAdmin = userRequest.isAdmin
                try:
                    if(isAdmin):
                        # admin = UserSerializer(data=request.data)
                        # if admin.is_valid():
                        #     admin.isAdmin = True
                        #     admin.save()
                            admin = CustomUserManager.create_admin(UserModel.objects,username, nama, jabatan, password)
                            response = Response()
                            response.ResponseCode = "0"
                            response.ResponseMessage = "User berhasil dibuat"
                            returnModel = jsons.dump(response)
                            return JsonResponse(returnModel,safe=False)
                    else:
                        userBiasa = CustomUserManager.create_staffuser(UserModel.objects,username, nama, jabatan, password)
                        response = Response()
                        response.ResponseCode = "0"
                        response.ResponseMessage = "User berhasil dibuat"
                        returnModel = jsons.dump(response)
                        return JsonResponse(returnModel,safe=False)
                except Exception as e:
                    response = Response()
                    response.ResponseCode = "9"
                    response.ResponseMessage = str(e)
                    returnModel = jsons.dump(response)
                    return JsonResponse(returnModel,safe=False)
            else:
                response = Response()
                response.ResponseCode = "9"
                response.ResponseMessage = "Must be admin"
                returnModel = jsons.dump(response)
                return JsonResponse(returnModel,safe=False)
        else:
            response = Response()
            response.ResponseCode = "9"
            response.ResponseMessage = "Tidak ada data diterima"
            returnModel = jsons.dump(response)
            return JsonResponse(returnModel,safe=False)
    
    @action(detail=False,methods=['post'])
    def EditUser(self,request):
        if request.POST is not None:
            if not isinstance(request.user,AnonymousUser):
                try:
                    userRequest = jsons.load(request.data,EditUserRequest)
                    nama = userRequest.nama
                    username = userRequest.username
                    jabatan = userRequest.jabatan
                    password = userRequest.password
                    isAdmin = userRequest.isAdmin
                    userid = userRequest.id
                    user = UserModel.objects.get(id=userid)
                    user.nama = nama if nama else user.nama
                    user.username = username if username else user.username
                    if password:
                        user.set_password(password)  
                    else:
                        user.password
                    user.jabatan = jabatan if jabatan else user.jabatan
                    user.isadmin = isAdmin
                    user.save()
                    response = Response()
                    response.ResponseCode = "0"
                    response.ResponseMessage = "User berhasil diubah"
                    returnModel = jsons.dump(response)
                    return JsonResponse(returnModel,safe=False)
                except Exception as e:
                    response = Response()
                    response.ResponseCode = "9"
                    response.ResponseMessage = str(e)
                    returnModel = jsons.dump(response)
                    return JsonResponse(returnModel,safe=False)
            else:
                response = Response()
                response.ResponseCode = "9"
                response.ResponseMessage = "Must be admin"
                returnModel = jsons.dump(response)
                return JsonResponse(returnModel,safe=False)
        else:
            response = Response()
            response.ResponseCode = "9"
            response.ResponseMessage = "Tidak ada data diterima"
            returnModel = jsons.dump(response)
            return JsonResponse(returnModel,safe=False)
    
    @action(detail=False,methods=['post'])
    def DeleteUser(self,request):
        if request.POST is not None:
            if not isinstance(request.user,AnonymousUser):
                try:
                    userid = request.data['userid']
                    user = UserModel.objects.get(id=userid)
                    user.delete()
                    response = Response()
                    response.ResponseCode = "0"
                    response.ResponseMessage = "User berhasil dihapus"
                    returnModel = jsons.dump(response)
                    return JsonResponse(returnModel,safe=False)
                except Exception as e:
                    response = Response()
                    response.ResponseCode = "9"
                    response.ResponseMessage = str(e)
                    returnModel = jsons.dump(response)
                    return JsonResponse(returnModel,safe=False)
            else:
                response = Response()
                response.ResponseCode = "9"
                response.ResponseMessage = "Must be admin"
                returnModel = jsons.dump(response)
                return JsonResponse(returnModel,safe=False)
        else:
            response = Response()
            response.ResponseCode = "9"
            response.ResponseMessage = "Tidak ada data diterima"
            returnModel = jsons.dump(response)
            return JsonResponse(returnModel,safe=False)

    @action(methods=['get'],detail=False)
    @permission_classes([IsAuthenticated])
    def GetUserForEdit(self, request):
        self.permission_classes = IsAuthenticated
        try:
            if not isinstance(request.user,AnonymousUser):
                userid = request.GET['userid']
                user = UserModel.objects.get(id=userid)
                model = UserModelView()
                model.id = user.id
                model.nama = user.nama
                model.username = user.username
                model.jabatan = user.jabatan
                model.isAdmin = user.isadmin
                response = Response()
                response.ResponseCode = "0"
                response.ResponseMessage = "success"
                response.ResponseObject = model
                returnModel = jsons.dump(response)
                return JsonResponse(returnModel,safe=False)
            else:
                response = Response()
                response.ResponseCode = "9"
                response.ResponseMessage = "Must be admin"
                returnModel = jsons.dump(response)
                return JsonResponse(returnModel,safe=False)
        except Exception as e:
            response = Response()
            response.ResponseCode = "9"
            response.ResponseMessage = str(e)
            returnModel = jsons.dump(response)
            return JsonResponse(returnModel,safe=False)

    @action(methods=['get'],detail=False)
    @permission_classes([IsAuthenticated])
    def GetAllUsers(self, request):
        self.permission_classes = IsAuthenticated
        try:
            if not isinstance(request.user,AnonymousUser):
                user = UserModel.objects.all()
                users = []
                for u in user:
                    model = UserModelView()
                    model.id = u.id
                    model.nama = u.nama
                    model.username = u.username
                    model.jabatan = u.jabatan
                    model.isAdmin = u.isadmin
                    users.append(model)
                response = Response()
                response.ResponseCode = "0"
                response.ResponseMessage = "success"
                response.ResponseObject = users
                returnModel = jsons.dump(response)
                return JsonResponse(returnModel,safe=False)
            else:
                response = Response()
                response.ResponseCode = "9"
                response.ResponseMessage = "Must be admin"
                returnModel = jsons.dump(response)
                return JsonResponse(returnModel,safe=False)
        except Exception as e:
            response = Response()
            response.ResponseCode = "9"
            response.ResponseMessage = str(e)
            returnModel = jsons.dump(response)
            return JsonResponse(returnModel,safe=False)