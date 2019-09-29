from rest_framework.serializers import HyperlinkedIdentityField, ModelSerializer, SerializerMethodField
from posts.models import Post
from comments.api.serializers import CommentSerializer
from comments.models import Comment
from accounts.api.serializers import UserDetailSerializer

class PostCreateUpdateSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
			'title',
			'content',
			'draft',
			'publish'
		]

DETAIL_URL = HyperlinkedIdentityField(
		view_name = 'detail_api',
		lookup_field = 'slug'
	)

class PostDetailSerializer(ModelSerializer):
	url = DETAIL_URL
	user = UserDetailSerializer(read_only=True)
	image = SerializerMethodField()
	html = SerializerMethodField()
	comments = SerializerMethodField()
	class Meta:
		model = Post
		fields = [
			'url',
			'id',
			'title',
			'slug',
			'content',
			'html',
			'image',
			'user',
			'draft',
			'publish',
			'comments'
		]

	def get_html(self, obj):
		return obj.get_markdown()

	def get_image(self, obj):
		try:
			image = obj.image.url
		except:
			image = None
		return image

	def get_comments(self, obj):
		qs = Comment.objects.filter_by_instance(obj)
		comments = CommentSerializer(qs, many=True).data
		return comments

class PostListSerializer(ModelSerializer):
	url = DETAIL_URL
	class Meta:
		model = Post
		fields = [
			'url',
			'title',
			'content',
		]


"""
data = {
... 'title':"New data",
... 'content':"New data",
... 'draft':False,
... 'publish':"2019-9-12"
... }

new = PostSerializer(data=data)
if new.is_valid():
	new.save()
else:
	print(new.errors)


"""