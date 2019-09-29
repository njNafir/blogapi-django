from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.serializers import HyperlinkedIdentityField, ModelSerializer, SerializerMethodField, EmailField, CharField, ValidationError

User = get_user_model()

class UserCreateSerializer(ModelSerializer):
	email = EmailField(label='Email Address')
	email2 = EmailField(label='Confirm Email')
	password2 = CharField(style={'input_type': 'password'}, label='Confirm Password', write_only=True)
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'email2',
			'password',
			'password2'
		]
		extra_kwargs = {
			'password': {
				'write_only': True
			}
		}

	def validate_email2(self, value):
		data = self.get_initial()
		email = data['email']
		email2 = value
		user_qs = User.objects.filter(email=email2)
		if user_qs.exists():
			raise ValidationError("User already registered with this email address.")
		if email2 != email:
			raise ValidationError("Email must match.")
		return value

	def validate_password2(self, value):
		data = self.get_initial()
		password = data['password']
		password2 = value
		if password2 != password:
			raise ValidationError("Password must match.")
		return value

	def create(self, validated_data):
		username = validated_data['username']
		email = validated_data['email']
		password = validated_data['password']
		user_obj = User(
				username = username,
				email = email
			)
		user_obj.set_password(password)
		user_obj.save()
		return validated_data

class UserLoginSerializer(ModelSerializer):
	username = CharField(required=False, allow_blank=True)
	email = EmailField(label='Email Address')
	password = CharField(style={'input_type': 'password'}, label='Password', write_only=True)
	token = CharField(allow_blank=True, read_only=True)
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password',
			'token'
		]
		extra_kwargs = {
			'password': {
				'write_only': True
			}
		}

	def validate(self, data):
		username = data.get('username', None)
		email = data.get('email', None)
		password = data['password']
		if not username and not email:
			raise ValidationError("A username or email must be needed to login")
		user_obj = User.objects.filter(
				Q(username=username) |
				Q(email=email)
			).distinct()
		print(user_obj)
		user_obj = user_obj.exclude(email__isnull=True).exclude(email__iexact="")
		if user_obj.exists() and user_obj.count() == 1:
			user = user_obj.first()
			if not user.check_password(password):
				raise ValidationError("Invalid credentials for typing the password please try again.")
			data['token'] = "SOME DATA TOKEN"
		else:
			raise ValidationError("User not found.")
		return data

class UserDetailSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'first_name',
			'last_name'
		]