from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.decorators import  permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView #Login
from .models import Order,OrderItem,Product

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import Order, OrderItem, Product

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')

    data = []

    for order in orders:
        items = []
        for item in order.items.all():
            items.append({
                "product_id": item.product.id if item.product else None,
                "product_name": item.product.desc if item.product else None,
                "quantity": item.quantity,
                "price": str(item.price),
                "subtotal": str(item.price * item.quantity),
            })

        data.append({
            "order_id": order.id,
            "created_at": order.created_at,
            "is_paid": order.is_paid,
            "items": items,
        })

    return Response(data)





@api_view(['POST'])
@permission_classes([IsAuthenticated]) # token required
def buy(request):
    items = request.data.get("items")

    # Validate request data
    if not items or not isinstance(items, list):
        return Response(
            {"error": "items must be a list"},
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():
        # ✅ CREATE ORDER
        order = Order.objects.create(user=request.user)

        for item in items:
            product_id = item.get("product_id")
            quantity = item.get("quantity", 1)

            if not product_id:
                return Response(
                    {"error": "product_id is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"error": f"Product with id {product_id} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            if quantity <= 0:
                return Response(
                    {"error": "quantity must be greater than 0"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ✅ CREATE ORDER ITEM
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price  # snapshot price
            )

    return Response(
        {
            "message": "Order placed successfully",
            "order_id": order.id,
            "items_count": len(items)
        },
        status=status.HTTP_201_CREATED
    )




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom colummns 
        token['username'] = user.username
        token['email'] = user.email
        token['waga'] = "baga"
        # ...


        return token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def only_mem(req):
    user = req.user
    print({'Welcome':user.email})
    return Response({'Welcome':user.email})


@api_view(['GET'])
def index(req):
    return Response('index')

@api_view(['GET'])
def hello(req):
    return Response('bla bla')

@api_view(['GET'])
def test(req):
    return Response({'user_name':'waga'})





@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)

    return Response({"success": f"user {user.username} created"}, status=status.HTTP_201_CREATED)
