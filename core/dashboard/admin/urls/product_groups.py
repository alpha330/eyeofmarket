from django.urls import path, include
from .. import views


urlpatterns = [
    path("product-group/list/",views.AdminProductGroupListView.as_view(),name="product-group-list"),
    path("product-group/create/",views.AdminProductGroupCreateView.as_view(),name="product-group-create"),
    path("product-group/<int:pk>/edit/",views.AdminProductGroupEditView.as_view(),name="product-group-edit"),
    path("product-group/<int:pk>/delete/",views.AdminProductDeleteView.as_view(),name="product-group-delete"),
]
