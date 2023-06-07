from typing import Any, Collection, Optional, Type
from django.db import models
from adress.models import Adress
from user.models import User
# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=25)
    inn = models.IntegerField()
    adress = models.ForeignKey(Adress, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete= models.PROTECT)

    @classmethod
    def from_db(cls, db: str | None, field_names: Collection[str], values: Collection[Any]):
        print(db, field_names, values)
        return super().from_db(db, field_names, values)

    


