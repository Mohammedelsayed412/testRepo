from asyncio.windows_events import NULL
from products.models import AuditLog
from products.api.serializer import LogSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


# TODO ==> add filter with dynamics fields also 

@api_view(["GET", "POST"])
def AuditLogList(request):
    if request.method == 'POST':
        serialLog = LogSerializer(data=request.data)
        if serialLog.is_valid():
            serialLog.save()
            return Response(serialLog.data)
    if(len(request.query_params)==0):
        logs = AuditLog.objects.all()
        logSerailizer = LogSerializer(logs, many=True)
        
    else:
        logSerailizer =  filterByField(request, request.query_params) 
        
    for i in range(len(logSerailizer.data)) :
            for item in logSerailizer.data[i].items():
                if(item[0] == 'eventSpecificFields' and item[1]!= None):
                    for key, value in item[1].items():
                        logSerailizer.data[i][key] = value
    return Response(logSerailizer.data)


def filterByField(request, params):
    fieldsList = AuditLog.fieldsList()
    logs = AuditLog.objects.all()
    fieldsDict = {}

    for key in params.keys():
        if(key in fieldsList):
            fieldsDict[key] = params[key]
        
    logs = AuditLog.objects.filter(**fieldsDict)
    logSerailizer = LogSerializer(logs, many=True)
    return logSerailizer
