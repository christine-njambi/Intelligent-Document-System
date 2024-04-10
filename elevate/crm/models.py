from django.db import models

# Create your models here.
class ClassModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    class_motto = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class StudentModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    class_attending = models.ForeignKey(ClassModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class TransactionModel(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    receipt_no = models.CharField(max_length=100)
    student_number = models.ForeignKey(StudentModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image uploaded at {self.uploaded_at}"