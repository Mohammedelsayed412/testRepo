from django.urls import path

from products.views import home, productsView, productDetails, editProduct, deleteProduct, addProduct \
     , logsView, login_user, logout_user, deactivateUser

from rest_framework.authtoken import views

urlpatterns = [
    path('home', home, name='home'),
    path('login', login_user, name='login'),
    path('logout', logout_user, name='logout'),
    path('deactivate', deactivateUser, name='deactivate'),
    path('products', productsView, name='products'),
    path('<int:id>', productDetails, name='productDetials'),
    path('editProduct/<int:id>', editProduct, name='editProduct'),
    path('deleteProduct/<int:id>', deleteProduct, name='deleteProduct'),
    path('addProduct', addProduct, name='addProduct'),
    path('logs', logsView, name='logs'),
    path('api-token-auth', views.obtain_auth_token, name='api-token-auth'),
]