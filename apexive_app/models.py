# Code 1

from django.db import models

class Author(models.Model):
    # Author model representing the information about the authors
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Post(models.Model):
    # Post model representing individual blog posts
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title

class Tag(models.Model):
    # Tag model representing tags associated with blog posts
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name




# Code 2

from django.db import models

class Manufacturer(models.Model):
    # Model for representing manufacturers of products
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Category(models.Model):
    # Model for representing product categories
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    # Model for representing individual products
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

