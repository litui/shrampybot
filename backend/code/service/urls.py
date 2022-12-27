from django.urls import path
from service.views import (
    ServiceView,
    ServiceCreateView,
    ServiceIndividualView,
    ServiceDeleteView,
    ServiceUpdateView,
)

urlpatterns = [
    # path('', ServiceView.as_view()),
    # path('create', ServiceCreateView.as_view()),
    # path('<int:pk>', ServiceUpdateView.as_view()),
    path("<slug:name>", ServiceIndividualView.as_view()),
    # path('<int:pk>/delete', ServiceDeleteView.as_view())
]
