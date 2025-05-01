# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Product
from .serializers import ProductSerializer

@api_view(['GET'])
def product_list(request):
    queryset = Product.objects.all()
    
    # Filtering
    category = request.query_params.get('category')
    search = request.query_params.get('search')
    
    if category:
        queryset = queryset.filter(category__iexact=category)
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(brand__icontains=search)
        )
    
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
def checkout(request):
    product_id = request.data.get('product_id')
    product_name = request.data.get('product_name')
    
    if not (product_id or product_name):
        return Response(
            {"error": "Provide either product_id or product_name"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Dummy validation
    if product_id and not Product.objects.filter(id=product_id).exists():
        return Response(
            {"error": "Invalid product ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if product_name and not Product.objects.filter(name__iexact=product_name).exists():
        return Response(
            {"error": "Invalid product name"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response({"message": "Your order has been placed successfully!"})