from django.db import models

from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User 
from django.forms import ModelForm
from django.db.models import Count, Sum, Avg 
# Create your models here.
 

class Category(MPTTModel):
    status = (
        ('True', 'True'),
        ('False', 'False'),
    ) 
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    title = models.CharField(max_length=200)
    keywords = models.CharField(max_length=100)
    image = models.ImageField(blank=True, upload_to='category/')
    status = models.CharField(max_length=20, choices=status)
    slug = models.SlugField(null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    
    class MPTTMeta:
        order_insertion_by = ['title']


    def __str__(self):
        return self.title
    
    

class Product(models.Model):
    status = (
        ('True', 'True'),
        ('False', 'False'),)
    
    VARTANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    keywords = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product', null=True, blank=True, default='')
    new_price = models.DecimalField(decimal_places=2, max_digits=15, default=0)
    old_price = models.DecimalField(decimal_places=2, max_digits=15)
    amount = models.IntegerField(default=0)
    min_amount = models.IntegerField(default=3)
    variant = models.CharField(max_length=10, choices=VARTANTS, default='None')
    detail = models.TextField()
    status = models.CharField(max_length=20, choices=status)
    slug = models.SlugField(null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
     
    def ImageUrl(self):
        if self.image:
            return self.image.url 
        else:
            return ""    

     
    def average_review(self):
        reviews = Comment.objects.filter(
            product=self, status=True).aggregate(average=Avg('rate'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
            return avg
        else:
            return avg
        
    def total_reviews(self):
        reviews = Comment.objects.filter(
            product=self, status=True).aggregate(count=Count('id'))
        cnt = 0    
        if reviews['count'] is not None:
            cnt = (reviews['count'])
            return cnt 



 

class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='product/images')


    def __str__(self):
        return self.title            
   



class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False')
       
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=300, blank=True)
    comment = models.CharField(max_length=300, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=40, choices=STATUS,  default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
    
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']




class Color(models.Model):
    name = models.CharField(max_length=200, blank=True)
    code = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.name
   

    def colortag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color</p>'.format(self.code))
        else:
            return ""     


class Size(models.Model):
    name = models.CharField(max_length=200, blank=True)
    code = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.name     



class Variants(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    image_id = models.IntegerField(blank=True, null=True, default=0)
    quantity = models.IntegerField(blank=True, null=True, default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)


    def __str__(self):
        return self.title


    def image(self):
        img - Images.objects.get(id=self.image_id)
        if img.id is not None:
            variant_image - img.image.url 
        else:
            variant_image = ""
        return variant_image

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""
