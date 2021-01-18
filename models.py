from django.db import models

# Create your models here.
class Car(models.Model):
    """ 登録車
    """
    existence = models.BooleanField("廃車済",default=False)

    region = models.CharField("ナンバー（地名）", max_length=5,default='例：品川')
    bunruinum = models.CharField("ナンバー（分類番号）", max_length=3,default='例：５００')
    hiragana = models.CharField("ナンバー（ひらがな）", max_length=1,default='例：あ')
    number = models.CharField("ナンバー（４桁）", max_length=4,default='例：４６４９')
    price = models.PositiveIntegerField("取得価格",blank=True,null=True)
    distance = models.PositiveIntegerField("購入時走行距離",default='0')
    
    leaseorbuy = models.PositiveIntegerField("購入／リース", choices=((1,"購入"),(2,"リース")))

    def __str__(self):
        return self.region + self.bunruinum + self.hiragana + self.number

class Maintainance(models.Model):
    """ メンテナンス
    """
    car = models.ManyToManyField(Car,verbose_name="対象車",blank=True,null=True)
    maintain_name = models.PositiveIntegerField("メンテナンス種類", choices=((1,"定期点検"),(2,"バッテリー点検"),(3,"ライト点検")),blank=True,null=True)
    maintain_day = models.DateField("メンテナンス日",blank=True,null=True)
    maintain_memo = models.CharField("メンテナンス内容", max_length=100,blank=True,null=True)


class CarTest(models.Model):
    """車検
    """
    car = models.ManyToManyField(Car,verbose_name="対象車",blank=True,null=True)
    NextCarTestDay = models.DateField("次回車検日",blank=True,null=True)


class Cost(models.Model):
    """ 費用管理
    """


class Clash(models.Model):
    """ 事故管理
    """
    car = models.ManyToManyField(Car,verbose_name="対象車",blank=True,null=True)
    driver = models.CharField("運転手", max_length=10,default='',blank=True,null=True)
    detail = models.CharField("事故内容", max_length=100,default='',blank=True,null=True)
    clashday = models.DateField("事故日",blank=True,null=True)



class Scrap(models.Model):
    """ 廃車管理
    """
    car = models.ForeignKey(Car,verbose_name="対象車",on_delete=models.CASCADE,blank=True,null=True)
    scrap = models.BooleanField("廃車済",default=False)
    scrapday = models.DateField("廃車日",blank=True,null=True)





