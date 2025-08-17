from django.db import models
from django.contrib.auth.models import User
import uuid
from django_countries.fields import CountryField
class CertificateRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending DNS Validation'),
        ('valid', 'Validated'),
        ('rejected', 'Rejected'),
        ('issued', 'Certificate Issued'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    domain = models.CharField(max_length=255)
    csr = models.FileField(upload_to='csrs/')
    dns_token = models.CharField(max_length=64, default=uuid.uuid4().hex)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def dns_record_name(self):
        return f"_apnassl.{self.domain}"

    def dns_record_value(self):
        return self.dns_token

    def __str__(self):
        return f"{self.domain} - {self.status}"
