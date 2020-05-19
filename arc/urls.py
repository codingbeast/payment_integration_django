from django.urls import path, include
from arc import views as arcviews
urlpatterns = [
	path("", arcviews.homepage.as_view(), name="homepage"),
	path("checkout/",arcviews.checkout.as_view(), name="checkout"),
	path("success/",arcviews.success.as_view(), name='success')
]