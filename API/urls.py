from django.urls import path


from API import views

urlpatterns = [
   path('inbound/sms/', views.InboundSMS.as_view(),
         name='InboundSMS'),
path('outbound/sms/', views.OutboundSMS.as_view(),
      name='OutboundSMS')
]
