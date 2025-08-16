from django.db import models



class Participant(models.Model):
    name= models.CharField(max_length=100)
    email= models.EmailField(unique=True)
    password= models.CharField(max_length=150)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
    ])
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name



class Category(models.Model):
    name= models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Categories"


class Event(models.Model):
    name= models.CharField(max_length=150)
    description= models.TextField()
    date= models.DateField()
    time= models.TimeField()
    location =models.CharField(max_length=150)
    category= models.ForeignKey(Category, on_delete=models.CASCADE)
    host = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='hosted_events')
    participants = models.ManyToManyField(Participant, related_name='events', blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
