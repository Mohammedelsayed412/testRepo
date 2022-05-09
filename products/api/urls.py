from django.urls import path
from products.api.views import AuditLogList


urlpatterns=[
    path("logList",AuditLogList,name="logList"),
]