from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from posts.models import Post
from .serializers import PostCreateUpdateSerializer, PostDetailSerializer, PostListSerializer
from .permissions import IsOwnerOrReadOnly
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination

class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	lookup_field = "slug"
	# permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		if self.request.user.is_authenticated:
			serializer.save(user=self.request.user)

class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = "slug"
	permission_classes = [IsOwnerOrReadOnly]

class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	permission_classes = [AllowAny]
	lookup_field = "slug"
	# lookup_url_kwarg = "abc"

class PostListAPIView(ListAPIView):
	serializer_class = PostListSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['title', 'content', 'user__first_name', 'user__last_name']
	pagination_class = PostPageNumberPagination #PostLimitOffsetPagination
	permission_classes = [AllowAny]

	def get_queryset(self):
		queryset_list = Post.objects.all()
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
					Q(title__icontains=query)|
					Q(content__icontains=query)|
					Q(user__first_name__icontains=query) |
					Q(user__last_name__icontains=query)
					).distinct()
		return queryset_list


class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	lookup_field = "slug"
	permission_classes = [IsOwnerOrReadOnly]

	def perform_update(self, serializer):
		if self.request.user.is_authenticated:
			serializer.save(user=self.request.user)