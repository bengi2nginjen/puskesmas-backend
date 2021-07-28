from api.models.DataTable import DataTableColumn, ResponseDataTable
from api.models.FormResponseModel import FormResponseModel, ResponseAnswer
from api.models.Response import Response
import uuid
from api.model import Form, FormResponse
from api.models.FormModel import FormModel
from django.http.response import JsonResponse
import jsons
from rest_framework.decorators import api_view,action
from rest_framework import HTTP_HEADER_ENCODING, viewsets
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from userauth.models import UserModel

class FormController(viewsets.ViewSet):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=['post'])
    def SubmitForm(self,request):
        if(request.POST is not None):
            try:
                formRequestModel = jsons.load(request.data,FormModel)
                # retr = jsons.dumps(formModel)
                # print(request.POST)
                formModel = Form()
                formModel.id = uuid.uuid4()
                formRequestModel.id = formModel.id
                formModel.content = jsons.dumps(formRequestModel)
                formModel.user_id = request.user.id
                formModel.created_date = datetime.now()
                formModel.is_active = False
                formModel.save()
                response = Response()
                response.ResponseCode = "0"
                response.ResponseMessage = "Form berhasil dibuat"
                returnModel = jsons.dump(response)
                return JsonResponse(returnModel,safe=False)
            except Exception as e:
                    response = Response()
                    response.ResponseCode = "9"
                    response.ResponseMessage = str(e)
                    returnModel = jsons.dump(response)
                    return JsonResponse(returnModel,safe=False)

    @action(detail=False, methods=['get'])
    def GetAll(self,request):
        if(request.GET is not None):
            try:
                forms = Form.objects.all()
                # retr = jsons.dumps(formModel)
                # print(request.POST)
                formModels = []
                for form in forms:
                    if form.content is not None and form.content != "":
                        frm = jsons.loads(form.content,FormModel)
                        formModels.append(frm)
                response = Response()
                response.ResponseCode = "0"
                response.ResponseMessage = "success"
                response.ResponseObject = formModels
                returnModel = jsons.dump(response)
                return JsonResponse(returnModel,safe=False)
            except Exception as e:
                    response = Response()
                    response.ResponseCode = "9"
                    response.ResponseMessage = str(e)
                    returnModel = jsons.dump(response)
                    return JsonResponse(returnModel,safe=False)
    
    @action(detail=False, methods=['get'])
    def GetForm(self,request):
        if(request.GET is not None):
            try:
                form = Form.objects.get(id=request.GET['FormId'])
                # retr = jsons.dumps(formModel)
                # print(request.POST)
                formModel = jsons.loads(form.content,FormModel)
                response = Response()
                response.ResponseCode = "0"
                response.ResponseMessage = "success"
                response.ResponseObject = formModel
                returnModel = jsons.dump(response)
                return JsonResponse(returnModel,safe=False)
            except Exception as e:
                    response = Response()
                    response.ResponseCode = "9"
                    response.ResponseMessage = str(e)
                    returnModel = jsons.dump(response)
                    return JsonResponse(returnModel,safe=False)

    @action(detail=False, methods=['post'])
    def DeleteForm(self,request):
        if(request.POST is not None):
            try:
                form = Form.objects.get(id=request.data['FormId'])
                # retr = jsons.dumps(formModel)
                # print(request.POST)
                form.delete()
                response = Response()
                response.ResponseCode = "0"
                response.ResponseMessage = "Form dihapus"
                returnModel = jsons.dump(response)
                return JsonResponse(returnModel,safe=False)
            except Exception as e:
                    response = Response()
                    response.ResponseCode = "9"
                    response.ResponseMessage = str(e)
                    returnModel = jsons.dump(response)
                    return JsonResponse(returnModel,safe=False)
    
    @action(detail=False, methods=['post'])
    def EditForm(self,request):
        if(request.POST is not None):
            try:
                formRequestModel = jsons.load(request.data,FormModel)
                # retr = jsons.dumps(formModel)
                # print(request.POST)
                form = Form.objects.get(id=formRequestModel.id)
                form.content = jsons.dumps(formRequestModel)
                form.save()
                response = Response()
                response.ResponseCode = "0"
                response.ResponseMessage = "Form diubah"
                returnModel = jsons.dump(response)
                return JsonResponse(returnModel,safe=False)
            except Exception as e:
                    response = Response()
                    response.ResponseCode = "9"
                    response.ResponseMessage = str(e)
                    returnModel = jsons.dump(response)
                    return JsonResponse(returnModel,safe=False)

    @action(detail=False, methods=['post'])
    def SubmitResponse(self,request):
        if(request.POST is not None):
            try:
                formResponseModel = jsons.load(request.data,FormResponseModel)
                # retr = jsons.dumps(formModel)
                # print(request.POST)
                formResponse = FormResponse()
                formResponse.id = uuid.uuid4()
                formResponse.responses = jsons.dumps(formResponseModel)
                formResponse.user_id = request.user.id
                formResponse.form_id = formResponseModel.form_id
                formResponse.date_created = datetime.now()
                formResponse.save()
                response = Response()
                response.ResponseCode = "0"
                response.ResponseMessage = "Form berhasil dikirim"
                returnModel = jsons.dump(response)
                return JsonResponse(returnModel,safe=False)
            except Exception as e:
                    response = Response()
                    response.ResponseCode = "9"
                    response.ResponseMessage = str(e)
                    returnModel = jsons.dump(response)
                    return JsonResponse(returnModel,safe=False)

    @action(detail=False, methods=['get'])
    def GetFormResponsesDataTable(self,request):
        if(request.GET is not None):
            try:
                dataResponse = ResponseDataTable()
                form = Form.objects.get(id=request.GET['FormId'])
                # retr = jsons.dumps(formModel)
                # print(request.POST)
                if form is not None:
                    formModel = jsons.loads(form.content,FormModel)
                    #region populate column name
                    colNama = DataTableColumn()
                    colNama.name = "Nama"
                    colNama.data = "nama"
                    colTgl = DataTableColumn()
                    colTgl.name = "Tanggal Isi"
                    colTgl.data = "date"
                    dataResponse.columns.append(colNama)
                    dataResponse.columns.append(colTgl)
                    for question in formModel.questions:
                        colQuestion = DataTableColumn()
                        colQuestion.data = "question-"+str(question['id'])
                        colQuestion.name = question['question']
                        dataResponse.columns.append(colQuestion)
                    #endregion 
                    formResponses = FormResponse.objects.filter(form_id=form.id)
                    if formResponses is not None:
                        for resp in formResponses:
                            responseModel = jsons.loads(resp.responses,FormResponseModel)
                            user = None
                            try:
                                user = UserModel.objects.get(id=resp.user_id)
                            except Exception as e:
                                pass
                            dictData = {'nama':user.nama if user is not None else "",'date':resp.date_created.strftime("%d/%m/%Y, %H:%M:%S")}
                            for ans in responseModel.responses:
                                dictData['question-'+str(ans['question_id'])] = ans['response_value']
                            dataResponse.data.append(dictData)                                
                            # formModel = jsons.loads(form.content,FormModel)
                response = Response()
                response.ResponseCode = "0"
                response.ResponseMessage = "success"
                response.ResponseObject = dataResponse
                returnModel = jsons.dump(response)
                return JsonResponse(returnModel,safe=False)
            except Exception as e:
                    response = Response()
                    response.ResponseCode = "9"
                    response.ResponseMessage = str(e)
                    returnModel = jsons.dump(response)
                    return JsonResponse(returnModel,safe=False)

    # @action(detail=False,methods=['get'])
    # def Hello(self,request):
    #     return HttpResponse("HELLLO")
    