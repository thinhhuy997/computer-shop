from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from .models import Product, Category, ImageURL
from rest_framework import status
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter


from api import serializers
# Create your views here.

@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'List':'/task-list/',
		'Detail View':'/task-detail/<str:pk>/',
		'Create':'/task-create/',
		'Update':'/task-update/<str:pk>/',
		'Delete':'/task-delete/<str:pk>/',
		}

	return Response(api_urls)

############################ CATEGORY VIEWS #####################################

@api_view(['GET', 'POST'])
def CategoryMultipleCreate(request):
	if request.method == "GET":
		return Response({"This API used to create multiple categories!"})
	if request.method == "POST":
		for item in request.data['items']:
			# create a product object
			try:
				category_obj = Category.objects.create(name=item['category_name'])
			except Exception as e:
				print(e)
				return Response({"An error occurred when creating multiple categories!"})
		return Response({"Created multiple categories successfully!"})

class CategoryListCreate(generics.ListCreateAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	filter_backends = [SearchFilter]
	search_fields = ['name']

@api_view(['GET','PUT','DELETE'])
def CategoryDetail(request, pk):
	try:
		category = Category.objects.get(id=pk)
	except Category.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "GET":
		serializers = CategorySerializer(category, many=False)
		return Response(serializers.data)


############################ END OF CATEGORY VIEWS ################################


############################ PRODUCT VIEWS #####################################

class ProductListCreate(generics.ListCreateAPIView):
	queryset = Product.objects.all().order_by('-created_at')
	serializer_class = ProductSerializer
	filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
	search_fields = ['name']
	# customized filter class
	filterset_class = ProductFilter

# class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
# 	queryset = Product.objects.all()
# 	lookup_url_kwarg = 'slug'
# 	serializer_class = ProductSerializer
# 	filter_backends = [SearchFilter]
# 	search_fields = ['name']

@api_view(['GET','PUT','DELETE'])
def ProductDetail(request, slug):
	try:
		product = Product.objects.get(slug__iexact = slug)
	except Product.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "GET":
		serializers = ProductSerializer(product, many=False)
		return Response(serializers.data)

@api_view(['GET', 'POST'])
def productMultipleCreate(request):
	if request.method == "GET":
		return Response({"This API used to create multiple products"})
	if request.method == "POST":
		for item in request.data['items']:

			# create a product object
			try:
				product_obj = Product.objects.create(name=str(item['product_name']).strip(), price=float(item["product_price"]), description_from_crawler = item["product_description"])
			except Exception as e:
				print(e)

			# connect image_url object to above product object through foreign key
			try:
				for piu in item["product_img_urls"].split():
					image_url_obj = ImageURL.objects.create(url = piu, product = product_obj)
			except Exception as e:
				print(e)

		return Response({"testing..."})

@api_view(['GET', 'POST'])
def ProudctMultipleCreateByCategory(request, categoryId):
	i = 1
	try:
		category = Category.objects.get(id=categoryId)
	except Category.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "GET":
		serializers = CategorySerializer(category, many=False)
		return Response(serializers.data)

	if request.method == "POST":
		for item in request.data['items']:
			# create a product object
			try:
				product_obj = Product.objects.create(name=str(item['product_name']).strip(), price=float(item["product_price"]), description_from_crawler = item["product_description"])
				product_obj.categories.add(category)
				print("Process in - " + str(i))
				i += 1
			except Exception as e:
				print(e)
				return Response({"An error occurred when creating multiple categories!"})
			# connect image_url object to above product object through foreign key
			try:
				for piu in item["product_img_urls"].split():
					image_url_obj = ImageURL.objects.create(url = piu, product = product_obj)
			except Exception as e:
				print(e)
		return Response({"Created multiple categories successfully!"})

############################ END OF PRODUCT VIEWS #####################################

