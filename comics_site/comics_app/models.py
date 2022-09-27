# Create your models here.
from django.db import  models, connection

class COMICS(models.Model):
    path_image = models.TextField(db_column="path_image")
    comics_t = models.CharField(db_column="title",max_length=50)
    comics_amount = models.IntegerField(db_column="comics_amount")
    about_comics = models.CharField(db_column = "about", max_length=1000)
    comics_price = models.FloatField(db_column = "price")
    date_public = models.DateField(db_column="date_public")
    comics_id = models.IntegerField(db_column="comics_id", primary_key=True)

    class Meta:
        db_table = "comics"

class AUTHOR(models.Model):
    about = models.CharField(db_column="about_author", max_length=1000)
    author_name = models.CharField(db_column="author_name", max_length=50)
    author_lastname = models.CharField(db_column="author_lastname", max_length=50)
    author_birth = models.DateField(db_column="author_birth")
    author_id = models.IntegerField(db_column="author_id", primary_key=True)
    class Meta:
        db_table = "author"

    def __str__(self):
        return (self.author_name + " " + self.author_lastname)

class PUBLISHER(models.Model):
    publisher_id = models.IntegerField(db_column='publisher_id', primary_key=True)
    publisher_name = models.CharField(db_column="publisher_name", max_length=50)
    about_pub = models.CharField(db_column="about_pub", max_length=1000)
    class Meta:
        db_table = "publisher"

    def __str__(self):
        return self.publisher_name

    # def __unicode__(self):
    #     return self.publisher_name

class COMICS_PUBLISHER(models.Model):
    comics_id = models.ForeignKey(COMICS, db_column="comics_id", to_field="comics_id", on_delete=models.SET_NULL, null=True)
    publisher_id = models.ForeignKey(PUBLISHER, db_column="publisher_id", to_field="publisher_id", on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = "comics_publisher"

class USER(models.Model):
    user_id = models.IntegerField(primary_key=True, db_column="user_id")
    user_name = models.CharField(db_column = "user_name", max_length=50)
    user_lastname = models.CharField(db_column="user_lastname", max_length=50)
    password = models.CharField(db_column="user_password", max_length=224)
    user_login = models.CharField(db_column="login", max_length=50)
    user_email = models.CharField(db_column="email", max_length=320)
    user_mobile = models.CharField(db_column="user_mobile_phone", max_length=15)
    class Meta:
        db_table = "users"

class ROLE(models.Model):
    role_id = models.IntegerField(db_column="role_id", primary_key=True)
    role_name = models.CharField(db_column="role_name", max_length = 50)
    class  Meta:
        db_table = "roles"

class USER_ROLES(models.Model):
    user_role = models.ForeignKey(ROLE,db_column="role_id", to_field="role_id", on_delete=models.SET_NULL, null=True)
    user_id = models.ForeignKey(USER,db_column="user_id", to_field="user_id", on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = "user_role"

class ORDER(models.Model):
    order_id = models.IntegerField(primary_key = True, db_column="user_ord_id")
    order_date = models.DateField(db_column="order_date")
    user_id = models.ForeignKey(USER, db_column="user_id", to_field="user_id", on_delete=models.SET_NULL, null=True)
    address = models.CharField(db_column="user_address", max_length=500)
    comics_id = models.ForeignKey(COMICS, db_column="comics_id", to_field="comics_id", on_delete=models.SET_NULL, null=True)
    name = models.CharField(db_column="customer_name", max_length=50)
    lastname = models.CharField(db_column="customer_lastname", max_length=50)
    number = models.CharField(db_column="mobile_number", max_length=15)
    class Meta:
        db_table = "user_order"

class STATUS(models.Model):
    status_id = models.IntegerField(db_column="status_id", primary_key=True)
    status_name = models.CharField(db_column="_status_", max_length=255)
    class Meta:
        db_table="status_order"

    def __str__(self):
        return self.status_name

class ORDER_LINE(models.Model):
    line_id = models.IntegerField(db_column="line_id", primary_key=True)
    order_id = models.ForeignKey(ORDER, db_column="order_id", to_field="order_id", on_delete=models.SET_NULL, null=True)
    comics_id= models.ForeignKey(COMICS, to_field="comics_id", db_column="comics_id", on_delete=models.SET_NULL, null=True)
    status_id = models.ForeignKey(STATUS, to_field="status_id", db_column="status_id", on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = "order_line"


class ORDER_HISTORY(models.Model):
    history_id = models.IntegerField(db_column="history_id", primary_key=True)
    order_id = models.ForeignKey(ORDER,db_column="order_id", to_field="order_id", on_delete=models.SET_NULL, null=True )
    status_id = models.ForeignKey(STATUS,db_column="status_id", to_field="status_id", on_delete=models.SET_NULL, null=True)
    user_id = models.ForeignKey(USER, db_column="user_id", to_field="user_id", on_delete=models.SET_NULL, null=True)
    comment = models.CharField(db_column="coment", max_length=225)
    class Meta:
        db_table = "order_history"
