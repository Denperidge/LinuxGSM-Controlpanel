from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class GameserverManager(BaseUserManager):
    # A normal user is expected to link towards a gameserver running on LGSM
    def create_user(self, linux_username, lgsm_servername, password):
        if not lgsm_servername or not linux_username or not password:
            raise ValueError('Gameserver must have all variables defined')

        gameserver = self.model(
            linux_username=linux_username,
            lgsm_servername=lgsm_servername,
            identifier=linux_username+"/"+lgsm_servername,
        )

        gameserver.is_staff = False  # Deny access to /admin

        gameserver.set_password(password)  # Hash & save password
        gameserver.save(using=self._db)
        return gameserver
    
    # The superusers only function is to add gameservers through /admin
    def create_superuser(self, identifier, linux_username, lgsm_servername, password):
        if not identifier or not password:
            raise ValueError('Superuser must have an identifier and a password')

        gameserver = self.model(
            linux_username="",  # No use for linux_username
            lgsm_servername="",  # No use for lgsm_servername 
            identifier=identifier,  # Identifier is the username set by the 
        )
        gameserver.is_staff = True  # Allow access to /admin

        gameserver.set_password(password)
        gameserver.save(using=self._db)
        return gameserver
    
        


class Gameserver(AbstractBaseUser):
    identifier = models.CharField(max_length=50, unique=True)
    lgsm_servername = models.CharField(max_length=50, default=None)
    linux_username = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)  # Default: set gameserver to active
    is_staff = models.BooleanField(default=False)  # Default: not allowed to access /admin

    objects = GameserverManager()

    USERNAME_FIELD = 'identifier'  # Unique id
    REQUIRED_FIELDS = ['lgsm_servername', 'linux_username', 'password']  # Fiels required to fill in

    # str() return identifier
    def __str__(self):
        return self.identifier

    # Currently defaulting to True
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    # Determine whether the user is allowed to open app_label
    def has_module_perms(self, app_label):
        if app_label != "admin":
            return True
        else:
            if self.is_staff:
                return True
            else:
                return False



