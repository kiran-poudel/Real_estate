from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager,Group

# Create your models here.

class UserAccountManager(BaseUserManager):
    def create_user(self,name,email,password = None):
        if not email:
            raise ValueError('User must have an email address')
                       
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            name = name,
        )
        

        user.set_password(password)
        user.save(using=self._db)


        return user
    
    def create_agent(self,name,email,password = None):

        user = self.create_user(name,email,password)
        
        user.is_agent = True
        user.save(using=self._db)

        return user
    

    
    def create_superuser(self,name,email,password = None):
        user = self.create_user(name,email,password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user
    

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    groups = models.ForeignKey(Group,on_delete=models.SET_NULL,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_agent = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

