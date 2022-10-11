from django.urls import path
from . import views

urlpatterns = [
	path('', views.apiOverview, name="api-overview"),

	########################## Category #####################################
	path('category-list-create/', views.CategoryListCreate.as_view()),
	# category detail - function based views
	path('category-detail/<int:pk>', views.CategoryDetail),
	# used to create multiple categories
	path('category-multiple-create/', views.CategoryMultipleCreate),
	########################### End of Category #############################

	########################### Product #######################################
	path('product-list-create/', views.ProductListCreate.as_view()),
	path('product-detail/<slug:slug>/', views.ProductDetail),
	# used to create multiple products
	path('product-multiple-create/', views.productMultipleCreate),
	path('product-multiple-create-by-category/<int:categoryId>', views.ProudctMultipleCreateByCategory),
	########################### End of Product #############################
]