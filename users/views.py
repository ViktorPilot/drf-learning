from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from stripe import CardError, InvalidRequestError, RateLimitError, StripeError

from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserSerializer
from users.services import create_stripe_price, create_stripe_product, create_stripe_session


class UserUpdateAPIView(generics.UpdateAPIView):
    """Контроллер API редактирования существующего пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    """Контроллер API просмотра списка пользователей"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер API просмотра профиля пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """Контроллер API создания нового пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Метод устанавливает статус пользователя активным и хэширует пароль перед сохранением"""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserDestroyAPIView(generics.DestroyAPIView):
    """Контроллер API удаления пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentsListApiView(generics.ListAPIView):
    """Контроллер API просмотра всех платежей"""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ("date",)
    filterset_fields = (
        "type_payment",
        "bought_course",
        "bought_lesson",
    )


class PaymentsCreateAPIView(generics.CreateAPIView):
    """Контроллер API создания нового платежа"""

    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        """Метод выполняющий платеж через сервис Stripe"""
        payment = serializer.save(user=self.request.user)
        if payment.bought_course is None and payment.bought_lesson is None:
            raise ValidationError("Нужно выбрать или курс или урок")
        elif payment.bought_course is not None and payment.bought_lesson is not None:
            raise ValidationError("Нужно выбрать или курс или урок")
        else:
            try:
                product_stripe = create_stripe_product(payment.id)
                price_stripe = create_stripe_price(product_stripe, payment.payment)
                session_id, session_link = create_stripe_session(price_stripe)
                payment.session_id = session_id
                payment.link = session_link
                payment.save()
            except CardError as e:
                return Response({"error": str(e)})
            except RateLimitError as e:
                return Response({"error": str(e)})
            except InvalidRequestError as e:
                return Response({"error": str(e)})
            except StripeError as e:
                return Response({"error": str(e)})
            except Exception as e:
                return Response({"error": str(e)})
