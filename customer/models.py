from django.db import models
from django.db.models.signals import pre_delete
import datetime

class Menu(models.Model):
	itemNum = models.AutoField(primary_key=True)
	itemName = models.CharField(max_length=30,unique=True)
	itemDesc = models.TextField(default="description")
	itemUnitPrice = models.FloatField(default=0)
	itemImageName = models.CharField(max_length=50)
	isEnabled = models.BooleanField(default=True)
	isVeg = models.BooleanField(default=True)
	
	def __str__(self):
		return str(self.itemNum)+" - "+self.itemName+" Price : "+str(self.itemUnitPrice)

	def unitprice(self):
		return self.itemUnitPrice

	def retSelf(self):
		return self


class Token(models.Model):
	tokenNum = models.AutoField(primary_key=True)
	totalAmount = models.FloatField(null=False,default=0)
	timetokenPlaced = models.DateTimeField(null=True)


class TokenItem(models.Model):
	tokens = models.ForeignKey(Token,on_delete=models.CASCADE)
	menu = models.ForeignKey(Menu,on_delete=models.CASCADE)
	quantity = models.IntegerField(default=0)
	price = models.FloatField(default=0)


class OrderList(models.Model):								#order is a keyword in sql so used OrderList as tablename
	tokenNum = models.IntegerField(unique=True)         #there is also unique_for_date and unique_for_month is token numbers are reset everyday or everymonth
	orderNum = models.AutoField(primary_key=True)
	totalAmount = models.FloatField(null=False,default=0)
	timeOrderPlaced = models.DateTimeField(null=True)

class OrderedItem(models.Model):
	orderList = models.ForeignKey(OrderList,on_delete=models.CASCADE)
	menu = models.ForeignKey(Menu,on_delete=models.CASCADE)
	quantity = models.IntegerField(default=0)
	price = models.FloatField(default=0)

class History(models.Model):
	orderNum = models.IntegerField()
	timeStamp = models.DateTimeField()
	itemNum = models.IntegerField()
	itemName = models.CharField(max_length=30,default="NA")
	quantity = models.IntegerField(default=0)
	price = models.FloatField()


def add_to_history(sender,**kwargs):
	x = kwargs['instance']
	y = OrderedItem.objects.filter(orderList = x)

	for i in y:
		h = History(orderNum = x.orderNum)
		h.itemNum = i.menu.itemNum
		h.itemName = i.menu.itemName
		h.price = i.menu.itemUnitPrice * i.quantity
		h.quantity = i.quantity
		h.timeStamp = datetime.datetime.now()
		h.save()
		print("Backed up : " + str(h.orderNum)+" "+str(h.timeStamp)+" "+str(h.itemNum)+" "+str(h.price))

pre_delete.connect(add_to_history,sender = OrderList)


























# -------------------------------------------------------------------------------------------------------------
# class OrderList(models.Model):
# 	tableNum = models.ForeignKey(TableNum,on_delete=models.CASCADE)
# 	orderNum = models.AutoField(primary_key=True)
	# totalAmount = models.FloatField(null=False,default=0)
	# timeOrderPlaced = models.DateTimeField(null=True)
# ####################################################
# 	isFinished = models.BooleanField(default=False)    #if true the customer has placed order else he/she is still placing
# ####################################################

# 	def __str__(self):
# 		return "totalAmount : "+str(self.totalAmount)


# class OrderItem(models.Model):
# 	orderList = models.ForeignKey(OrderList,on_delete=models.CASCADE)
# 	menu = models.ForeignKey(Menu,on_delete=models.CASCADE)
# 	quantity = models.IntegerField(default=0)
# 	#price = models.FloatField(default=0)

# 	def __str__(self):
# 		return "orderNum = "+str(self.orderList.orderNum)+" itemNum = "+str(self.menu.itemNum)+" Qty :"+str(self.quantity)


# class Backup(models.Model):
# 	orderNum = models.IntegerField()
# 	timeStamp = models.DateTimeField()
# 	itemNum = models.IntegerField()
# 	itemName = models.CharField(max_length=30,default="NA")
# 	quantity = models.IntegerField(default=0)
# 	price = models.FloatField()

# 	def __str__(self):
# 		return "Order No. - "+str(self.orderNum)+" TimeStamp - "+str(self.timeStamp)+" Item no. - "+str(self.itemNum)+" Bill - "+str(self.price)

# def create_Backup(sender,**kwargs):
# 	x = kwargs['instance']
# 	y = OrderItem.objects.filter(orderList = x)

# 	for i in y:
# 		b = Backup(orderNum = x.orderNum)
# 		b.itemNum = i.menu.itemNum
# 		b.itemName = i.menu.itemName
# 		b.price = i.menu.itemUnitPrice * i.quantity
# 		b.quantity = i.quantity
# 		b.timeStamp = datetime.datetime.now()
# 		b.save()
# 		print("Backed up : " + str(b.orderNum)+" "+str(b.timeStamp)+" "+str(b.itemNum)+" "+str(b.price))

# pre_delete.connect(create_Backup,sender = OrderList)
# ---------------------------------------------------------------------------------------------------------