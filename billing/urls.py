from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('',views.home,name="hm"),
    path('add/product', views.product_add, name='home'),
    path("register", views.register_request, name="register"),
    path("", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path("billing", views.billing, name= "billing"),
    path("billingpay", views.billingpay, name= "billingpay"),
    path("billpdf", views.bill_pdf, name= "billpdf"),
    path('generatepdf', views.generate_pdf, name='generatepdf'),
    path('dayreport', views.dat_report, name='dayreport')
    # More URL patterns if needed
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

