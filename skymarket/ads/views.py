from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from ads.filters import AdFilter
from ads.models import Ad, Comment
from ads.permissions import IsUser, IsAdmin
from ads.serializers import AdSerializer, AdDetailSerializer, CommentSerializer


class AdPagination(pagination.PageNumberPagination):
    page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    pagination_class = AdPagination
    default_permission = (AllowAny(), )
    default_serializer = AdSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter

    permissions = {
        'retrieve': (IsAuthenticated(),),
        'create': (IsAuthenticated(), IsUser() or IsAdmin()),
        'destroy': (IsAuthenticated(), IsUser() or IsAdmin()),
        'partial-update': (IsAuthenticated(), IsUser() or IsAdmin()),
        'update': (IsAuthenticated(), IsUser() or IsAdmin())
    }

    @action(detail=False)
    def me(self, request, *args, **kwargs):
        self.queryset = Ad.objects.filter(author=request.user)
        return super().list(self, request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in ["retrieve", "create", "update", "partial_update", "destroy"]:
            return AdDetailSerializer
        else:
            return AdSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        return self.permissions.get(self.action, self.default_permission)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    default_permission = (IsAuthenticated(), )

    permissions = {
        'create': (IsAuthenticated(), ),
        'update': (IsUser() or IsAdmin(), ),
        'partial_update': (IsUser() or IsAdmin(), ),
        'destroy': (IsUser() or IsAdmin(), ),
    }

    def get_permissions(self):
        return self.permissions.get(self.action, self.default_permission)

    def get_queryset(self):
        ad_id = self.kwargs.get('ad_pk')
        return Comment.objects.filter(ad_id=int(ad_id))

    def perform_create(self, serializer):
        ad_id = self.kwargs.get('ad_pk')
        ad_instance = get_object_or_404(Ad, pk=ad_id)
        serializer.save(ad=ad_instance, author=self.request.user)

