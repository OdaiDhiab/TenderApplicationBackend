from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField("User Phone Number", max_length=20, blank=True, null=True, unique=True)

    role = models.CharField(
        "User Role",
        choices=[("Admin", "admin"), ("Buyer", "buyer"), ("Seller", "seller")],
        max_length=10
    )

    verified = models.BooleanField("User Verfication Status", default=False)

class Tender(models.Model):
    title = models.CharField("Tender Title", max_length=20)
    description = models.TextField("Tender Description", max_length=500)
    budget_min = models.DecimalField("Tender Minimum Budget", max_digits=12, decimal_places=2)
    budget_max = models.DecimalField("Tender Maximum Budget", max_digits=12, decimal_places=2)
    deadline = models.DateField("Tender Deadline")
    status = models.CharField(
        "Tender Status",
        choices=[("Draft","draft"), ("Open", "open"), ("Closed", "closed")],
        max_length=10
    ) 
    created_at = models.DateTimeField(auto_now_add=True)
    
class TenderCategory(models.Model):
    name = models.CharField("Category Name", max_length=20)

class TenderCategoryJunction(models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, verbose_name="Tender ID")
    category = models.ForeignKey(TenderCategory, on_delete=models.CASCADE, verbose_name="Category ID")

    class Meta:
        unique_together = ('tender_id', 'category_id')


class Bid(models.Model):
    title = models.CharField("Bid Title", max_length=20)
    proposal = models.TextField("Bid Proposal", max_length=500)
    amount = models.DecimalField("Bid Amount", max_digits=12, decimal_places=2)
    status = models.CharField(
        "Bid Status",
        choices=[("Draft","draft"), ("Submitted", "submitted"), ("Rejected", "rejected")],
        max_length=10
    ) 
    submitted_at = models.DateTimeField(auto_now_add=True)
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, verbose_name="Bidded Tender ID")

class BidDocument(models.Model):
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE,verbose_name="Bid ID")
    file_name = models.CharField("Bid File Name", max_length=20)
    file_path = models.CharField("Bid File Path", max_length=500)

class Evaluation(models.Model):
    tender = models.ForeignKey( Tender, on_delete=models.CASCADE, verbose_name="Evaluated Tender")
    bid = models.ForeignKey( Bid, on_delete=models.CASCADE, verbose_name="Evaluated Bid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Evaluator ID")
    score = models.DecimalField("Evaluator Score", max_digits=5, decimal_places=2)
    comments = models.TextField("Evaluator Comments", max_length=2500)
    evaluated_at = models.DateTimeField(auto_now_add=True)

#messaging model:
class Thread(models.Model):
    thread_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sent_date = models.DateTimeField(auto_now_add=True)
    message_body = models.TextField("Message", max_length=5000)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

class Participant(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('thread', 'user')

class MessageReadState(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('message', 'user')

