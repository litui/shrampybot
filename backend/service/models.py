from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedTextField

class Service(models.Model):
    name = models.CharField(max_length=255, null=False)
    website_url = models.TextField(null=True)
    broad_scope = models.TextField(null=False)
    oauth_login_url = models.TextField(null=True)
    oauth_endpoint_url = models.TextField(null=True)
    oauth_revoke_url = models.TextField(null=True)
    api_client_id = models.TextField(null=True)
    api_secret_key = EncryptedTextField(null=True)
    api_token = EncryptedTextField(null=True)
    api_refresh_token = EncryptedTextField(null=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserService(models.Model):
    identity = models.CharField(max_length=255, null=True)
    service = models.ForeignKey(Service, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scope = models.TextField(null=False, default='read')
    user_token = EncryptedTextField(null=False)
    user_refresh_token = EncryptedTextField(null=True)

    def __str__(self):
        return "{} - {}".format(self.user.get_full_name(), self.service.name)