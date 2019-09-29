from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rest_framework.serializers import HyperlinkedIdentityField, ModelSerializer, SerializerMethodField, ValidationError
from comments.models import Comment
from accounts.api.serializers import UserDetailSerializer

User = get_user_model()

DETAIL_URL = HyperlinkedIdentityField(view_name='thread_detail_api')

def create_comment_serializer(model_type='post', slug=None, parent_id=None, user=None):
	class CreateCommentSerializer(ModelSerializer):
		class Meta:
			model = Comment
			fields = [
				'id',
				'content',
				'timestamp'
			]

		def __init__(self, *args, **kwargs):
			self.model_type = model_type
			self.slug = slug
			self.parent_id = parent_id
			self.user = user
			self.parent_obj = None
			if self.parent_id:
				parent_qs = Comment.objects.filter(id=self.parent_id)
				if parent_qs.exists() and parent_qs.count() == 1:
					self.parent_obj = parent_qs.first()
			return super(CreateCommentSerializer, self).__init__(*args, **kwargs)

		def validate(self, data):
			model_type = self.model_type
			model_qs = ContentType.objects.filter(model=model_type)
			if not model_qs.exists() or model_qs.count() != 1:
				raise ValidationError("This is not a valid model type")
			SomeModel = model_qs.first().model_class()
			obj_qs = SomeModel.objects.filter(slug=self.slug)
			if not obj_qs.exists() or obj_qs.count() != 1:
				raise ValidationError("This slug is not valid for this model type")
			return data

		def create(self, validated_data):
			model_type = self.model_type
			slug = self.slug
			content = validated_data.get('content')
			if self.user is not None:
				user = self.user
			else:
				user = User.objects.first()
			parent_obj = self.parent_obj
			comment_obj = Comment.objects.create_by_model_type(model_type, slug, content, user, parent_obj=parent_obj)
			return comment_obj

	return CreateCommentSerializer

class CommentSerializer(ModelSerializer):
	user = UserDetailSerializer(read_only=True)
	reply_count = SerializerMethodField()
	class Meta:
		model = Comment
		fields = [
			'id',
			'user',
			'content_type',
			'object_id',
			'parent',
			'content',
			'reply_count',
			'timestamp'
		]

	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0

class CommentListSerializer(ModelSerializer):
	url = DETAIL_URL
	reply_count = SerializerMethodField()
	class Meta:
		model = Comment
		fields = [
			'id',
			'url',
			'content',
			'reply_count',
			'timestamp'
		]

	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0

class CommentChildrenSerializer(ModelSerializer):
	user = UserDetailSerializer(read_only=True)
	class Meta:
		model = Comment
		fields = [
			'id',
			'user',
			'content',
			'timestamp'
		]


class CommentDetailSerializer(ModelSerializer):
	url = DETAIL_URL
	user = UserDetailSerializer(read_only=True)
	replies = SerializerMethodField()
	reply_count = SerializerMethodField()
	post_object_slug = SerializerMethodField()
	class Meta:
		model = Comment
		fields = [
			'id',
			'url',
			'user',
			'content',
			'reply_count',
			'timestamp',
			'post_object_slug',
			'replies',
		]
		read_only_fields = [
			'reply_count',
			'replies'
		]

	def get_replies(self, obj):
		if obj.is_parent:
			return CommentChildrenSerializer(obj.children(), many=True).data
		return None

	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0

	def get_post_object_slug(self, obj):
		try:
			url = obj.content_object.get_api_url()
		except:
			url = None
		return url
