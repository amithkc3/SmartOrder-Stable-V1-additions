import operator
from datetime import datetime,timedelta
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import *

def loginpage(request):
	#implement if doesnot exists
	# try:
	token = Token.objects.create(timetokenPlaced=datetime.datetime.now())
	context={'tokenNum':token.tokenNum}
	print(context)
	return render(request,"login.html",context)
	# except:
		# return HttpResponse("try again")

def menu(request,tokenNum,category):
	#print("orderId=",orderId,"category=",category)
	# try:
	#for already added items
	try:
		intTokenNum = int(tokenNum)
		token = Token.objects.get(tokenNum = intTokenNum)			#got the token object

		addedItems = TokenItem.objects.filter(tokens = token)

		if(category == 'VEGONLY'):
			MenuItems = Menu.objects.filter(isVeg = True,isEnabled=True)
			addedMenuItems =[]
			#print("\n\n\n\n\n\n")
			for a in addedItems:
				addedMenuItems.append({'itemNum':a.menu.itemNum,'quantity':a.quantity})
			#print(addedMenuItems)
			context={'isVeg':True,'MenuItems':MenuItems,'tokenNum':tokenNum,'addedMenuItems':addedMenuItems}
			return render(request,"menu.html",context)

		elif(category == 'ALL'):
			MenuItems = Menu.objects.filter(isEnabled=True)
			addedMenuItems =[]
			#print("\n\n\n\n\n\n")
			for a in addedItems:
				addedMenuItems.append({'itemNum':a.menu.itemNum,'quantity':a.quantity})
			#print(addedMenuItems)
			context={'isVeg':False,'MenuItems':MenuItems,'tokenNum':tokenNum,'addedMenuItems':addedMenuItems}
			return render(request,"menu.html",context)
	except:
		context = {'tokenNum':intTokenNum}
		return render(request,"UCannotGoThere.html",context)

	# except:
		# return HttpResponse("Unable to load menu try again")

@csrf_exempt
def menuConfirmation(request,tokenNum):											# need to give me orderId
	# print(request,orderId)
	intTokenNum = int(tokenNum)
	token = Token.objects.get(tokenNum = intTokenNum)			#got the token object

	confirmationItems = TokenItem.objects.filter(tokens = token)

	confirmedList = []
	for c in confirmationItems:
		d = {
		'itemNum':c.menu.itemNum,
		'itemName':c.menu.itemName,
		'quantity':c.quantity,
		'price':c.menu.itemUnitPrice,
		'image':c.menu.itemImageName}
		confirmedList.append(d)

	confirmedList.sort(key=operator.itemgetter('itemNum'))
	# print('confirmationList: -------\n\n\n')
	# print(confirmationList[0].quantity,confirmationList[0].price )			# list of the order items with given orderId
	context={'confirmationList':confirmedList}
	# return render(request,"confirm.html",context)
	return JsonResponse(confirmedList,safe=False)

@csrf_exempt
def ack(request):
	tokenNum = request.POST['tokenNum']
	itemNo = request.POST['itemNum']
	qty = request.POST['quantity']
#	Updating OrderItem object
	intTokenNum = int(tokenNum)
	token = Token.objects.get(tokenNum = intTokenNum)

	itemObj = Menu.objects.get(itemNum = itemNo)

	tokenItem,create = TokenItem.objects.get_or_create(
		tokens = token,
		menu = itemObj, 
		)
	
	tokenItem.quantity = int(qty)
	tokenItem.save()
	
	#x =  Menu.objects.get(itemNum = itemNo)
	print(tokenNum,itemNo,qty)

	if(qty==str(0)):
		tokenItem.delete()
		print("deleted")

	token=updateTokenListAmount(intTokenNum)   #OR TOKEN LIST AMOUNT
 	# orderItem.price = int(qty) * int(x.itemUnitPrice)
	# orderItem.save()
	# to update orderList.totalAmount
	# if(qty==str(0)):
	# 	orderItem.delete()
	#	# Updating OrderList object
	# o = OrderItem.objects.filter(orderList = orderListObj)
	# total=0
	# for item in o:
	# 	total += item.price
	# orderListObj.totalAmount = total
	# orderListObj.save()
	return HttpResponse(token.totalAmount)


#call this to update orders total amount 
def updateTokenListAmount(tokenNum):
	token = Token.objects.get(tokenNum = tokenNum)

	confirmationItems = TokenItem.objects.filter(tokens = token)		#get all orderItems
	totalAmount = 0

	for c in confirmationItems:
		totalAmount += (c.menu.itemUnitPrice * c.quantity)

	token.totalAmount = totalAmount
	token.save()

	print(token.totalAmount)
	return token


def placeOrder(request):
	tokenNum = request.POST['tokenNum']
	intTokenNum = int(tokenNum)
	try:
		t=updateTokenListAmount(intTokenNum)				#final update to token totalAmount

		token = Token.objects.get(tokenNum = intTokenNum)
		tokenItem = TokenItem.objects.filter(tokens = token)
	
		orderList = OrderList.objects.create(tokenNum = token.tokenNum,totalAmount = token.totalAmount,timeOrderPlaced = datetime.datetime.now())
		for item in tokenItem : 
			OrderedItem.objects.create(orderList=orderList,menu=item.menu,quantity=item.quantity)	#,price=item.price)
		token.delete()

	except:
		orderList = OrderList.objects.get(tokenNum = intTokenNum)
	finally:
		confirmationItems = OrderedItem.objects.filter(orderList = orderList)

		confirmedList = []
		for c in confirmationItems:
			d = {
			'itemNum':c.menu.itemNum,
			'itemName':c.menu.itemName,
			'quantity':c.quantity,
			'price':c.menu.itemUnitPrice * c.quantity,
			'image':c.menu.itemImageName}
			confirmedList.append(d)
		
		confirmedList.sort(key=operator.itemgetter('itemNum'))
		# print('confirmationList: -------\n\n\n')
		# print(confirmationList[0].quantity,confirmationList[0].price )			# list of the order items with given orderId
		estimatedTimeOfDelivery = orderList.timeOrderPlaced+timedelta(minutes=5)
		context={'confirmationList':confirmedList,'orderId':orderList.orderNum,'isEmpty':False,
		'timeOrderPlaced':str(orderList.timeOrderPlaced),'estimatedTimeOfDelivery':str(estimatedTimeOfDelivery),'total':orderList.totalAmount}

		if len(confirmationItems) == 0 :
			context['isEmpty'] = True

		#print("placeOrdercontext",context)
		# return render(request,"confirm.html",context)
		return render(request,"orderAck.html",context)

@csrf_exempt
def orderCompleted(request,orderId):
	try:
		o = OrderList.objects.get(orderNum = int(orderId))
		return HttpResponse(200)
	except:
		return HttpResponse(201)


#=========================================================================================================
#=========================================================================================================


# import operator
# from datetime import datetime,timedelta
# from django.shortcuts import render
# from django.http import HttpResponse,JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import *
#  # Create your views here.
# def loginpage(request,tableKeyScanned):
# 	#implement if doesnot exists
# 	# try:
# 	tableId = TableNum.objects.get(tableKey=tableKeyScanned)
# 	orderId,boo = OrderList.objects.get_or_create(tableNum = tableId,totalAmount=0)
# 	context={'tableId':tableId.tableNum,'tableKey':tableId.tableKey,'orderId':orderId.orderNum}
# 	#print(context)
# 	return render(request,"login.html",context)
# 	# except:
# 		# return HttpResponse("try again")

# def menu(request,orderId,category):
# 	#print("orderId=",orderId,"category=",category)
# 	# try:
# 	#for already added items
# 	intOrderId = int(orderId)
# 	orderListObj = OrderList.objects.get(orderNum = intOrderId)
# 	addedItems = OrderItem.objects.filter(orderList = orderListObj)
# 	if(category == 'VEGONLY'):
# 		MenuItems = Menu.objects.filter(isVeg = True,isEnabled=True)
# 		addedMenuItems =[]
# 		#print("\n\n\n\n\n\n")
# 		for a in addedItems:
# 			addedMenuItems.append({'itemNum':a.menu.itemNum,'quantity':a.quantity})
# 		#print(addedMenuItems)
# 		context={'isVeg':True,'MenuItems':MenuItems,'orderId':orderId,'addedMenuItems':addedMenuItems}
# 		return render(request,"menu.html",context)
# 	elif(category == 'ALL'):
# 		MenuItems = Menu.objects.filter(isEnabled=True)
# 		addedMenuItems =[]
# 		#print("\n\n\n\n\n\n")
# 		for a in addedItems:
# 			addedMenuItems.append({'itemNum':a.menu.itemNum,'quantity':a.quantity})
# 		#print(addedMenuItems)
# 		context={'isVeg':False,'MenuItems':MenuItems,'orderId':orderId,'addedMenuItems':addedMenuItems}
# 		return render(request,"menu.html",context)
# 	# except:
# 		# return HttpResponse("Unable to load menu try again")
# @csrf_exempt
# def menuConfirmation(request,orderId):											# need to give me orderId
# 	# print(request,orderId)
# 	intOrderId = int(orderId)
# 	orderListObj = OrderList.objects.get(orderNum = intOrderId)
# 	confirmationItems = OrderItem.objects.filter(orderList = orderListObj) 
# 	confirmedList = []
# 	for c in confirmationItems:
# 		d = {
# 		'itemNum':c.menu.itemNum,
# 		'itemName':c.menu.itemName,
# 		'quantity':c.quantity,
# 		'price':c.menu.itemUnitPrice * c.quantity,
# 		'image':c.menu.itemImageName}
# 		confirmedList.append(d)

# 	confirmedList.sort(key=operator.itemgetter('itemNum'))
# 	# print('confirmationList: -------\n\n\n')
# 	# print(confirmationList[0].quantity,confirmationList[0].price )			# list of the order items with given orderId
# 	context={'confirmationList':confirmedList}
# 	# return render(request,"confirm.html",context)
# 	return JsonResponse(confirmedList,safe=False)

# @csrf_exempt
# def ack(request):
# 	orderNo = request.POST['orderNum']
# 	itemNo = request.POST['itemNum']
# 	qty = request.POST['quantity']
# #	Updating OrderItem object
# 	orderListObj = OrderList.objects.get(orderNum = orderNo)
# 	itemObj = Menu.objects.get(itemNum = itemNo)
# 	orderItem,create = OrderItem.objects.get_or_create(
# 		orderList =	orderListObj,
# 		menu = itemObj, 
# 		)
	
# 	orderItem.quantity = int(qty)
# 	orderItem.save()
	
# 	#x =  Menu.objects.get(itemNum = itemNo)
# 	print(orderNo,itemNo,qty)
# 	if(qty==str(0)):
# 		orderItem.delete()
# 		print("deleted")
# 	orderListObj = updateOrderListAmount(orderNo)
# 	# orderItem.price = int(qty) * int(x.itemUnitPrice)
# 	# orderItem.save()
# 	# to update orderList.totalAmount
# 	# if(qty==str(0)):
# 	# 	orderItem.delete()
# 	#	# Updating OrderList object
# 	# o = OrderItem.objects.filter(orderList = orderListObj)
# 	# total=0
# 	# for item in o:
# 	# 	total += item.price
# 	# orderListObj.totalAmount = total
# 	# orderListObj.save()
# 	return HttpResponse(orderListObj.totalAmount)


# #call this to update orders total amount 
# def updateOrderListAmount(orderNo):
# 	orderListObj = OrderList.objects.get(orderNum = orderNo)
# 	confirmationItems = OrderItem.objects.filter(orderList = orderListObj)		#get all orderItems
# 	totalAmount = 0

# 	for c in confirmationItems:
# 		totalAmount += (c.menu.itemUnitPrice * c.quantity)

# 	orderListObj.totalAmount = totalAmount
# 	orderListObj.save()
# 	print(orderListObj.totalAmount)
# 	return orderListObj

# def placeOrder(request):
# 	orderId = request.POST['orderNum']
# 	intOrderId = int(orderId)
# 	orderListObj = OrderList.objects.get(orderNum = intOrderId)
# 	orderListObj.isFinished = True
# 	#print(orderListObj.timeOrderPlaced)
# 	if(orderListObj.timeOrderPlaced == None):
# 		orderListObj.timeOrderPlaced = datetime.datetime.now()+timedelta(minutes=5)
# 		orderListObj.save()
# 	confirmationItems = OrderItem.objects.filter(orderList = orderListObj)
# 	# Total = 0
# 	# for c in confirmationItems:
# 	# 	Total += c.price
# 	# orderListObj.totalAmount = Total
# 	# orderListObj.save()
# 	updateOrderListAmount(orderId)


# 	#now to render acknowledgement page
# 	confirmedList = []
# 	for c in confirmationItems:
# 		d = {
# 		'itemNum':c.menu.itemNum,
# 		'itemName':c.menu.itemName,
# 		'quantity':c.quantity,
# 		'price':c.menu.itemUnitPrice * c.quantity,
# 		'image':c.menu.itemImageName}
# 		confirmedList.append(d)
	
# 	confirmedList.sort(key=operator.itemgetter('itemNum'))
# 	# print('confirmationList: -------\n\n\n')
# 	# print(confirmationList[0].quantity,confirmationList[0].price )			# list of the order items with given orderId
# 	context={'confirmationList':confirmedList,'orderId':orderId,'isEmpty':False,
# 	'timeOrderPlaced':str(orderListObj.timeOrderPlaced),'total':orderListObj.totalAmount}

# 	if len(confirmationItems) == 0 :
# 		context['isEmpty'] = True

# 	#print("placeOrdercontext",context)
# 	# return render(request,"confirm.html",context)
# 	return render(request,"orderAck.html",context)

# @csrf_exempt
# def orderCompleted(request,orderId):
# 	try:
# 		o = OrderList.objects.get(orderNum = int(orderId))
# 		return HttpResponse(200)
# 	except:
# 		return HttpResponse(201)