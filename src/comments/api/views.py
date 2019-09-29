from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from django.db.models import Q
from comments.models import Comment
from .serializers import CommentListSerializer, CommentDetailSerializer, create_comment_serializer
from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination

class CommentCreateAPIView(CreateAPIView):
	queryset = Comment.objects.all()
	# serializer_class = PostCreateUpdateSerializer
	# lookup_field = "slug"
	# permission_classes = [IsAuthenticated]

	def get_serializer_class(self):
		model_type = self.request.GET.get('type')
		slug = self.request.GET.get('slug')
		parent_id = self.request.GET.get('parent_id')
		if self.request.user.is_authenticated:
			user = self.request.user
		else:
			user = None
		return create_comment_serializer(model_type, slug, parent_id, user)

	# def perform_create(self, serializer):
	# 	if self.request.user.is_authenticated:
	# 		serializer.save(user=self.request.user)

# class PostDeleteAPIView(DestroyAPIView):
# 	queryset = Post.objects.all()
# 	serializer_class = PostDetailSerializer
# 	lookup_field = "slug"
# 	permission_classes = [IsAuthenticated, IsAdminUser]

# class CommentDetailAPIView(RetrieveAPIView):
# 	queryset = Comment.objects.all()
# 	serializer_class = CommentDetailSerializer
# 	# lookup_field = "slug"
# 	# lookup_url_kwarg = "abc"


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
	queryset = Comment.objects.filter(id__gte=0)
	serializer_class = CommentDetailSerializer
	permission_classes = [IsOwnerOrReadOnly]

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


class CommentListAPIView(ListAPIView):
	serializer_class = CommentListSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['title', 'content', 'user__first_name', 'user__last_name']
	pagination_class = PostPageNumberPagination #PostLimitOffsetPagination
	permission_classes = [AllowAny]

	def get_queryset(self):
		queryset_list = Comment.objects.all()
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
					Q(content__icontains=query)|
					Q(user__first_name__icontains=query) |
					Q(user__last_name__icontains=query)
					).distinct()
		return queryset_list


# class PostUpdateAPIView(RetrieveUpdateAPIView):
# 	queryset = Post.objects.all()
# 	serializer_class = PostCreateUpdateSerializer
# 	lookup_field = "slug"
# 	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# 	def perform_update(self, serializer):
# 		if self.request.user.is_authenticated:
# 			serializer.save(user=self.request.user)