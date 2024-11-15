from django.urls import path
from . import views 

urlpatterns = [
path('signup',views.signup, name='signup'),
path('signin',views.signin, name='signin'),
path('signout',views.signout, name='signout'),
path('profile',views.profile, name='profile'),
path('update_profile',views.update_profile, name='update_profile'),
path('station/<slug:slug>/', views.station_detail, name='station_detail'),
path('station/<slug:slug>/paiements/', views.station_payments, name='station_payments'),
path('station/<slug:slug>/paiements/<str:payment_date>/', views.payments_by_date, name='payments_by_date'),
path('confirm-payment/<int:payment_id>/', views.confirm_payment, name='confirm_payment'),
path('user/checkout/<int:cart_id>/<slug:slug>/', views.checkout, name='checkout'),
path('payment-success/<int:payment_id>/', views.payment_success, name='payment_success'),
path('station/<slug:slug>/paiements/', views.payments_by_date, name='payments_by_date'),
path('station/<slug:slug>/paiements/<str:payment_date>/', views.payments_by_date, name='payments_by_date_with_date'),
path('verifier-identifiant/<slug:slug>/', views.verifier_identifiant, name='verifier_identifiant'),
path('paiements/<slug:slug>/generate_word/', views.generate_word, name='generate_word'),
]
