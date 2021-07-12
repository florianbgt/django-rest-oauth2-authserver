from rest_framework import serializers      #new
from django.contrib.auth import get_user_model      #new
from django.contrib.auth.password_validation import validate_password       #new
from django.contrib.auth.models import Group        #new

User = get_user_model()     #new


class ProfileChangeSerializer(serializers.ModelSerializer):        #new
    groups = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')     #new

    class Meta:        #new
        model = User        #new
        depth = 1        #new
        fields = ('id', 'email', 'first_name', 'last_name', 'groups')        #new


class PasswordChangeSerializer(serializers.ModelSerializer):        #new
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])        #new
    password2 = serializers.CharField(write_only=True, required=True)       #new
    old_password = serializers.CharField(write_only=True, required=True)        #new

    class Meta:        #new
        model = User        #new
        fields = ('old_password', 'password', 'password2')        #new

    def validate_old_password(self, value):        #new
        user = self.context['request'].user        #new
        if not user.check_password(value):        #new
            raise serializers.ValidationError({'old_password': 'Old password is incorrect'})        #new
        return value        #new

    def validate(self, value):        #new
        if value['password'] != value['password2']:        #new
            raise serializers.ValidationError({'password2': 'Password fields did not match'})        #new
        return value        #new

    def update(self, instance, validated_data):        #new
        instance.set_password(validated_data['password'])        #new
        instance.save()        #new
        return instance        #new