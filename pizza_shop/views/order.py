from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..models import Order
from ..serializers import OrderSerializer, OrderPacingSerializer
from datetime import datetime


class OrderList(APIView):
    permission_classes = [IsAuthenticated]
    """
    List all orders(filter), or create a new order.
    """

    #  GET root/shop/order/
    def get(self, request, format=None):
        try:
            self.validate_customer(request)
            query_set = self.get_query_set(request, request.user)
        except PermissionError as e:
            return Response({'err': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'err': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(query_set, many=True)
        orders = self.prepare_outgoing_order_data_list(serializer.data)
        return Response(orders, status=status.HTTP_200_OK)

    # POST root/shop/order/
    def post(self, request, format=None):
        print(request.data)
        serializer = OrderPacingSerializer(
            data=modify_incoming_data(request.data),
            context={
                "user": request.user
            }
        )

        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'OK'}, status=status.HTTP_200_OK)
        return Response({'err': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # Helper methods
    def get_query_set(self, request, user):
        order_state = request.query_params.get('order_state')
        date = request.query_params.get('date')
        user = request.query_params.get('user')

        query_set = Order.objects.filter(customer=user)

        if order_state in ['submitted', 'confirmed', 'cancelled', 'delivered']:
            query_set = query_set.filter(order_state=order_state)
            if order_state == 'delivered':
                try:
                    date = datetime.strptime(date, '%Y-%m-%d')
                    query_set = query_set.filter(
                        delivery_time__year=date.year,
                        delivery_time__month=date.month,
                        delivery_time__day=date.day
                    )
                except Exception as e:
                    print(e)
                    print('date format is invalid. It should be in format yyyy-mm-dd')
        return query_set

    def validate_customer(self, request):
        try:
            user_id = int(request.query_params.get('user'))
            if user_id != request.user.id:
                raise PermissionError('You do not have enough permission')
        except Exception as e:
            raise e

    def prepare_outgoing_order_data_list(self, orders):
        order_list = []
        for order in orders:
            modified_order = {
                'id': order['id'],
                'pizza_name': order['pizza']['name'],
                'customer_name': order['customer']['name'],
                'order_price': order['order_price'],
                'quantity': order['quantity'],
                'order_state': order['order_state']
            }
            order_list.append(modified_order)
        return order_list


class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]
    """
    Retrieve specified order details.
    """

    # GET root/shop/order/<id>/
    def get(self, request, pk, format=None):
        try:
            query_set = Order.objects.get(pk=pk)
            if query_set.customer != request.user:
                raise PermissionError('You do not have enough permission!')
        except Order.DoesNotExist as e:
            return Response({'err': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as e:
            return Response({'err': str(e)}, status=status.HTTP_403_FORBIDDEN)

        serializer = OrderSerializer(query_set)

        order = self.prepare_outgoing_order_data(serializer.data)
        return Response(order, status=status.HTTP_200_OK)

    # helper methods
    def prepare_outgoing_order_data(self, order):
        modified_order = {
            'id': order['id'],
            'pizza_details': {
                'name': order['pizza']['name'],
                'brand': order['pizza']['brand'],
                'image': order['pizza']['image']
            },
            'customer_details': {
                'name': order['customer']['name'],
                'phone': order['customer']['phone']
            },
            'order_price': order['order_price'],
            'quantity': order['quantity'],
            'address': order['address'],
            'location': modify_outgoing_data(order),
            'order_state': order['order_state'],
            'delivery_time': order['delivery_time']
        }
        return modified_order


def modify_incoming_data(data):
    if data.get('location'):
        data['lat'] = data['location']['lat']
        data['lng'] = data['location']['lng']
    return data


def modify_outgoing_data(data):
    new_data = {
        'lat': data.get('lat'),
        'lng': data.get('lng')
    }
    if data['lat']: del data['lat']
    if data['lng']: del data['lng']
    return new_data
