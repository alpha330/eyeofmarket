from django.urls import path
from shop import views
# FROM WEBSITE URLS CONFIG core.urls<---->webiste.urs

app_name = "shop"

urlpatterns = [
    path("product/grid/", views.ShopProductGridView.as_view(), name="product-grid"),
]
