from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapi.urls')),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
