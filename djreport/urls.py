# dj
from django.urls import path

# views
from . import views


urlpatterns = [path("<int:pk>", views.RenderView.as_view(), name="djreport_render")]
