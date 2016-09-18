import datetime
from django.db import models
from django.contrib.auth.models import User
import json
# Create your models here.
class Company(models.Model):

    name = models.CharField(max_length=50, default="")
    user= models.ForeignKey(User)

    def __unicode__(self):
        return self.name

def productImagePath(instance , filename):
    return 'images/' + str(instance.company) + '/' + str(instance)

class Product(models.Model):
    company = models.ForeignKey(Company)
    title = models.CharField(max_length=50, default="")
    image = models.ImageField(upload_to=productImagePath , null = True, blank=False)
    startAge = models.IntegerField(default = 0)
    endAge = models.IntegerField(default = 100)
    targetGender = models.IntegerField()
    targetIncome = models.IntegerField(default = 0)
    targetCountry = models.CharField(max_length = 50 , default = "")
    interestTypes = models.CharField(max_length = 200 , default = '[]')

    hidden = models.IntegerField()

    def __unicode__(self):
        return str(self.company) + ' ' + self.title

    def getData(self):
        data = {'id' : self.pk ,'title' : self.title , 'image' : self.image.url}

        return  data

class UserProfile(models.Model):
    email = models.CharField(max_length = 200 , default = "")

    age = models.IntegerField(default = 20)

    MALE = 1
    FEMALE = 0

    gender = models.IntegerField(default = MALE)

    # Interest represents
    GAMING = 1
    MOVIE = 2
    FASHION = 3
    SHOPPING = 4
    SPORTS = 5
    ANIMATION = 6

    # interests is stored as a json list
    interests = models.CharField(max_length=200 , default="[]")

    LESS1000 = 1
    B1000_2000 = 2
    B2000_2500 = 3
    B2500_3000 = 4
    B3000_3500 = 5
    B3500_4000 = 6
    Above4000 = 7

    income = models.IntegerField(default = 5)

    def getInterests(self):
        return json.loads(self.interests)

    country = models.CharField(max_length = 50 , default = "")

    # bonus points for user
    points = models.IntegerField(default = 0)

    def __unicode__(self):
        return str(self.user)   

class Record(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(UserProfile)
    like = models.CharField(max_length = 1 , default = "Y")
    datetime = models.DateTimeField(default = datetime.datetime.now())

