from phonenumber_field import serializerfields
from rest_framework import serializers
from ads.models import Ad, Comment


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ("pk", "image", "title", "price", "description")


class AdDetailSerializer(serializers.ModelSerializer):
    author_first_name = serializers.SerializerMethodField()
    author_last_name = serializers.SerializerMethodField()
    author_id = serializers.ReadOnlyField(source='author.id')
    phone = serializerfields.PhoneNumberField(source='author.phone', read_only=True)

    def get_author_first_name(self, ad):
        return ad.author.first_name

    def get_author_last_name(self, ad):
        return ad.author.last_name

    class Meta:
        model = Ad
        fields = ['pk', 'image', 'title', 'price', 'description',
                  'author_first_name', 'author_last_name', 'author_id', 'phone']


class CommentSerializer(serializers.ModelSerializer):
    author_id = serializers.ReadOnlyField(source="author.id")
    author_first_name = serializers.ReadOnlyField(source="author.first_name")
    author_last_name = serializers.ReadOnlyField(source="author.last_name")
    author_image = serializers.ImageField(source="author.image", read_only=True)

    class Meta:
        model = Comment
        fields = ['author_id', 'text', 'ad_id', 'created_at',
                  'pk', "author_first_name", "author_last_name", "author_image"]
