from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Product, Contact, Wishlist, Category, Subategory, Type, Benner
from login.models import Loginmaster
from mycart.models import Order
import os
from math import ceil
from django.http import JsonResponse
from django.conf import settings
from datetime import date, timedelta
from django.core.files.storage import default_storage, FileSystemStorage
from django.db.models import Sum, Count
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth import authenticate, login
import speech_recognition as sr
import webbrowser as web
import wikipedia


# Create your views here.
def sendMail(foo, sendemailadd):
    sender = "hardik249312@gmail.com"
    receiver = sendemailadd
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'order status'
    msg.attach(MIMEText('your order status is ' + foo, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, "hardik846090")
    text = msg.as_string()
    server.sendmail(sender, receiver, text)


def index(request):
    # try:
    #     if request.session.get('session_loginRole') == "user":
    allProds = []
    catprods = Product.objects.filter(status='active').values('type', 'id')
    cats = {item['type'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(type=cat, status='active')
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    """------------------for header category------------------"""
    allCategory = Type.objects.all().order_by('id')
    categoryData = {}

    for i in allCategory:
        if i.categoryId.status == 'active':
            if i.categoryId.category in categoryData:
                if i.subcategoryId.status == 'active':
                    if i.subcategoryId.subcategory in categoryData[i.categoryId.category]:
                        if i.status == 'active':
                            if i.type in categoryData[i.categoryId.category][i.subcategoryId.subcategory]:
                                categoryData[i.categoryId.category][i.subcategoryId.subcategory][i.type] = i.id
                            else:
                                if i.type not in categoryData[i.categoryId.category][i.subcategoryId.subcategory]:
                                    if i.status == 'active':
                                        categoryData[i.categoryId.category][i.subcategoryId.subcategory][i.type] = i.id
                    else:
                        if i.subcategoryId.subcategory not in categoryData[i.categoryId.category]:
                            categoryData[i.categoryId.category][i.subcategoryId.subcategory] = {}
                            if i.subcategoryId.status == 'active':
                                categoryData[i.categoryId.category][i.subcategoryId.subcategory][i.type] = i.id
            else:
                if i.categoryId.category not in categoryData:
                    categoryData[i.categoryId.category] = {}
                    if i.subcategoryId.status == 'active':
                        categoryData[i.categoryId.category][i.subcategoryId.subcategory] = {}
                        if i.status == 'active':
                            categoryData[i.categoryId.category][i.subcategoryId.subcategory][i.type] = i.id

    request.session['categoryData'] = categoryData
    print(">>>>>>>>>>>>", categoryData)

    """--------for benner-----------"""

    bennerList = Benner.objects.filter(status="active").order_by('rank')

    """--------for trendings --------"""

    trendingList = Product.objects.order_by('-totalsale')[:5]
    print("<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<,///", trendingList)

    """--------New Arrival --------"""

    newarrivalList = Product.objects.order_by('-pub_date')[:3]
    print("<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<,///", newarrivalList)

    return render(request, 'user/index.html',
                  {'bennerList': bennerList, 'allProds': allProds, 'trendingList': trendingList,
                   'newarrivalList': newarrivalList})
    #     else:
    #         return redirect("/loadLogin")
    # except Exception as e:
    #     print(e)


# def filterProduct(request):
#     typeId = request.GET['typeId']
#     print(">>>>>>>>>>>>>>", typeId)
#     filter = Type.objects.get(pk=typeId)
#
#     getProduct = Product.objects.filter(category=filter.categoryId.category,
#                                         subcategory=filter.subcategoryId.subcategory, type=filter.type).all()
#     print("{{{{{{{{{{",getProduct)
#     return render(request,'user/men.html',{'getProduct':getProduct})


def filterProductType(request):
    # try:
    #     if request.session.get('session_loginRole') == "user":
            getProduct = Product.objects.filter(status='active').all()
            dict = {}
            if 'category' in request.GET:
                category = request.GET['category']
                getProduct = getProduct.filter(category=category)
                # print("??????????????????????", getProduct, category)
                dict['category'] = category

            if 'subcategory' in request.GET:
                subcategory = request.GET['subcategory']

                getProduct = getProduct.filter(subcategory=subcategory)
                dict['subcategory'] = subcategory
            if 'type' in request.GET:
                # subcategory = request.GET['subcategory']
                # category = request.GET['category']
                type = request.GET['type']
                getProduct = getProduct.filter(type=type)
                dict['type'] = type
            print("{{{{{{{{{{", getProduct)
            dict['getProduct'] = getProduct
            return render(request, 'user/type.html', dict)
        # else:
        #     return redirect("/")
    # except Exception as e:
    #     print(e)


def search1(request):
    try:
        if request.session.get('session_loginRole') == "user":
            query1 = request.GET.get('search1')

            import speech_recognition as sr
            import webbrowser as web

            # path = "http://127.0.0.1:8000/"
            url = "http://127.0.0.1:8000/search1/?search1="

            r = sr.Recognizer()

            with sr.Microphone() as source:
                print("Speak....")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                # print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSpeackkkkkkkkkk.....")

            try:
                output = r.recognize_google(audio)
                print("You have said :", output.lower())
                web.get().open(url + output.lower(), new=0, autoraise=True)
            except sr.UnknownValueError:
                output = "Could not understand audio"
            except sr.RequestError as e:
                output = "Could not request results; {0}".format(e)
            data = output

            allProds = []
            catprods = Product.objects.values('category', 'id')
            cats = {item['category'] for item in catprods}
            for cat in cats:
                prodtemp = Product.objects.filter(category=cat)
                prod = [item for item in prodtemp if searchMatch1(query1, item)]
                n = len(prod)
                nSlides = n // 4 + ceil((n / 4) - (n // 4))
                if len(prod) != 0:
                    allProds.append([prod, range(1, nSlides), nSlides])

            params = {'allProds': allProds, "msg": "", 'data': data}
            if len(allProds) == 0 or len(query1) < 4:
                params = {'msg': "can't find products !!!"}
            return render(request, 'user/search1.html', params)
        else:
            return redirect("/")
    except Exception as e:
        print(e)


def searchMatch1(query1, item):
    '''return true only if query matches the item'''

    if query1 in item.desc.lower() or query1 in item.name.lower() or query1 in item.category.lower():
        return True
    else:
        return False


def search(request):
    try:
        if request.session.get('session_loginRole') == "user":
            query = request.GET.get('search')

            allProds = []
            catprods = Product.objects.values('category', 'id')
            cats = {item['category'] for item in catprods}
            for cat in cats:
                prodtemp = Product.objects.filter(category=cat)
                prod = [item for item in prodtemp if searchMatch(query, item)]
                n = len(prod)
                nSlides = n // 4 + ceil((n / 4) - (n // 4))
                if len(prod) != 0:
                    allProds.append([prod, range(1, nSlides), nSlides])

            params = {'allProds': allProds, "msg": ""}
            # print("DATA >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>,", data1)
            if len(allProds) == 0 or len(query) < 4:
                params = {'msg': "can't find products !!!"}
            return render(request, 'user/search.html', params)
        else:
            return redirect("/")
    except Exception as e:
        print(e)


def searchMatch(query, item):
    '''return true only if query matches the item'''

    if query in item.desc.lower() or query in item.name or query in item.category.lower():
        return True
    else:
        return False


def contact(request):
    try:
        if request.session.get('session_loginRole') == "user":
            thank = False
            if request.method == "POST":
                name = request.POST.get("name", "")
                email = request.POST.get("email", "")
                phone = request.POST.get("phone", "")
                desc = request.POST.get("desc", "")
                print(name, email, phone, desc)
                contact = Contact(name=name, email=email, phone=phone, desc=desc)
                contact.save()
                thank = True
            return render(request, 'user/contact.html', {'thank': thank})
        else:
            return redirect("/")
    except Exception as e:
        print(e)


def loadWishlist(request):
    try:
        if request.session.get('session_loginRole') == 'user':

            wishList = Wishlist.objects.filter(userId=request.session['login_Id'])
            return render(request, 'user/wishlist.html', {'wishList': wishList})
        else:
            return redirect('/loadLogin')
    except Exception as e:
        print(e)


def inserWishlist(request):
    try:
        if request.session.get('session_loginRole') == 'user':
            product_Id = request.GET['id']
            userId = request.session['login_Id']

            varify = Wishlist.objects.filter(userId=userId, wishProductId_id=product_Id)
            if len(varify) == 0:
                addOrder = Wishlist(wishProductId_id=product_Id, userId=userId)
                addOrder.save()

        else:
            return JsonResponse({'loginRequire': "loginRequire"})
    except Exception as e:
        print(e)


def deleteWishlist(request):
    try:
        if request.session.get('session_loginRole') == 'user':
            wishlistId = request.GET['id']

            deleteItem = Wishlist.objects.get(pk=wishlistId)
            deleteItem.delete()
            return JsonResponse({"deleteItemId": wishlistId})
        else:
            return redirect('/loadLogin')
    except Exception as e:
        print(e)


def loadProductdesc(request):
    try:
            id = request.GET['id']
            # productdescList = ProductDesc.objects.filter(userId=request.session['login_Id'])
            productdescList = Product.objects.get(pk=id)

            colors = []
            i = Product.objects.filter(color=colors)
            if i not in colors:
                colors.append(i)

            return render(request, 'user/productdesc.html', {'productdescList': productdescList, 'colors': colors})
    except Exception as e:
        print(e)


# def loadProductdesc(request):
#     productId = request.GET['productId']
#     productdescList = Product.objects.get(pk=productId)
#
#     return render(request, 'user/productdesc.html', {'productdescList': productdescList})


# def insertProductdesc(request):
#     if request.session.get('login_Role') == 'user':
#         # temp = {}
#
#         product_Id = request.GET['id']
#         userId = request.session['login_Id']
#         # name = request.GET['name']
#         # desc = request.GET['desc']
#         # color = request.GET['color']
#         # size = request.GET['size']
#         # price = request.GET['price']
#         print("$$$$$$$$$$$$$$$$$$$$$$$$$")
#         # getProduct = ProductDesc.objects.get(pk=product_Id)
#         varify = ProductDesc.objects.filter(userId=userId, productDescId_id=product_Id)
#                                         # ,name=name, desc=desc, color=color,
#                                         # size=size, price=price)
#         if len(varify) == 0:
#             addProductdesc = ProductDesc(productDescId_id=product_Id, userId=userId)
#                                      # , name=name, desc=desc,
#                                      # color=color, size=size, price=price)
#             addProductdesc.save()
#
#     else:
#         return JsonResponse({'loginRequire': "loginRequire"})


"""--------------   admin   ----------------"""


def adminLoadDashbord(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            revenue = Order.objects.filter(orderstatus='delivered')
            totalRevenue = revenue.aggregate(Sum('totalPrice'))

            users = Loginmaster.objects.filter(loginRole='user').all()
            admin = Loginmaster.objects.filter(loginRole='admin').all()

            product = Product.objects.all()

            orders = Order.objects.filter(orderstatus='delivered')

            return render(request, 'admin/index.html',
                          {'totalPrice__sum': totalRevenue['totalPrice__sum'], 'users': len(users), 'admin': len(admin),
                           'product': len(product), 'orders': len(orders)})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminLoadDatabase(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            return render(request, 'admin/datatable.html')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminLoadValidation(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            return render(request, 'admin/validation.html')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminViewUser(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            userList = Loginmaster.objects.filter(loginRole='user').all()
            return render(request, 'admin/viewUser.html', {'userList': userList})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def changeStatus(request, foo):
    try:
        if request.session.get('session_loginRole') == 'admin':
            if foo == 'login':
                loginId = request.GET['loginId']
                loginStatus = request.GET['loginStatus']
                print(">>>>>>>>>>>>>>>>>>>>>>>", loginStatus)
                changestatus = Loginmaster.objects.get(pk=loginId)
                if loginStatus == 'active':
                    changestatus.loginStatus = 'inactive'
                if loginStatus == 'inactive':
                    changestatus.loginStatus = 'active'
                changestatus.save()
                if changestatus.loginRole == 'admin':
                    return redirect('/admin/viewAdmin')
                if changestatus.loginRole == 'user':
                    return redirect('/admin/viewUser')

            if foo == 'category':
                id = request.GET['id']
                status = request.GET['status']
                changeStatus = Category.objects.get(pk=id)
                if status == 'active':
                    changeStatus.status = 'inactive'
                if status == 'inactive':
                    changeStatus.status = 'active'
                changeStatus.save()
                return redirect('/admin/viewCategory')

            if foo == 'subcategory':
                id = request.GET['id']
                status = request.GET['status']
                changeStatus = Subategory.objects.get(pk=id)
                if status == 'active':
                    changeStatus.status = 'inactive'
                if status == 'inactive':
                    changeStatus.status = 'active'
                changeStatus.save()
                return redirect('/admin/viewSubcategory')

            if foo == 'type':
                id = request.GET['id']
                status = request.GET['status']
                changeStatus = Type.objects.get(pk=id)
                if status == 'active':
                    changeStatus.status = 'inactive'
                if status == 'inactive':
                    changeStatus.status = 'active'
                changeStatus.save()
                return redirect('/admin/viewType')

            if foo == 'benner':
                id = request.GET['id']
                status = request.GET['status']
                changeStatus = Benner.objects.get(pk=id)
                if status == 'active':
                    changeStatus.status = 'inactive'
                if status == 'inactive':
                    changeStatus.status = 'active'
                changeStatus.save()
                return redirect('/admin/viewBenner')

            if foo == 'product':
                id = request.GET['id']
                status = request.GET['status']
                changeStatus = Product.objects.get(pk=id)
                if status == 'active':
                    changeStatus.status = 'inactive'
                if status == 'inactive':
                    changeStatus.status = 'active'
                changeStatus.save()
                return redirect('/admin/viewProduct')

            if foo == 'dataset':
                id = request.GET['id']
                status = request.GET['status']
                changeStatus = Product.objects.get(pk=id)
                if status == 'active':
                    changeStatus.status = 'inactive'
                if status == 'inactive':
                    changeStatus.status = 'active'
                changeStatus.save()
                return redirect('/admin/loadDataset')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminViewAdmin(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            adminList = Loginmaster.objects.filter(loginRole='admin').all()
            return render(request, 'admin/viewAdmin.html', {'adminList': adminList})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminEditAdmin(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            loginId = request.GET['loginId']
            adminInfo = Loginmaster.objects.get(pk=loginId)
            return render(request, 'admin/editAdmin.html', {'adminInfo': adminInfo})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminUpdateAdmin(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            loginId = request.POST['loginId']
            loginUserName = request.POST['loginUserName']
            loginEmail = request.POST['loginEmail']
            loginMobileNo = request.POST['loginMobileNo']
            loginPassword = request.POST['loginPassword']
            loginRole = request.POST['loginRole']

            adminInfo = Loginmaster.objects.get(pk=loginId)
            adminInfo.loginUserName = loginUserName
            adminInfo.loginPassword = loginPassword
            adminInfo.loginRole = loginRole

            varify = Loginmaster.objects.filter(loginEmail=loginEmail, loginRole='admin') | Loginmaster.objects.filter(
                loginMobileNo=loginMobileNo, loginRole='admin')
            if len(varify) == 0:
                adminInfo.loginEmail = loginEmail
                adminInfo.loginMobileNo = loginMobileNo
                adminInfo.save()
                return redirect('/admin/viewAdmin')
            else:
                adminInfo.save()
                return render(request, 'admin/editAdmin.html',
                              {'adminInfo': adminInfo,
                               'msg': 'this email or mobile NO. alredy exist. Othre data is change.'})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminLoadAdmin(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            return render(request, 'admin/addAdmin.html')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminInsertAdmin(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            loginUserName = request.POST['loginUserName']
            loginEmail = request.POST['loginEmail']
            loginPassword = request.POST['loginPassword']
            loginMobileNo = request.POST['loginMobileNo']
            loginStatus = request.POST['loginStatus']

            varify = Loginmaster.objects.filter(loginEmail=loginEmail, loginRole='admin') | Loginmaster.objects.filter(
                loginMobileNo=loginMobileNo, loginRole='admin')
            if len(varify) == 0:
                addAdmin = Loginmaster(loginUserName=loginUserName, loginEmail=loginEmail, loginPassword=loginPassword,
                                       loginMobileNo=loginMobileNo, loginStatus=loginStatus, loginRole='admin')
                addAdmin.save()
                return redirect('/admin/viewAdmin')
            else:
                dic = {'loginUserName': loginUserName, 'loginEmail': loginEmail, 'loginPassword': loginPassword,
                       'loginMobileNo': loginMobileNo, 'loginStatus': loginStatus}
                return render(request, 'admin/addAdmin.html',
                              {'msg': 'this email or mobile NO. alredy exist.', 'dic': dic})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminDeleteAdmin(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            id = request.GET['id']
            deleteAdmin = Loginmaster.objects.get(pk=id)
            deleteAdmin.delete()
            return redirect('/admin/viewAdmin')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminLoadProduct(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            return render(request, 'admin/addProduct.html')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminInsertProduct(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            code = request.POST['code']
            name = request.POST['name']
            image = request.FILES.getlist('image')
            category = request.POST['category']
            subcategory = request.POST['subcategory']
            type = request.POST['type']
            color = request.POST['color']
            desc = request.POST['desc']
            size = request.POST.getlist('size')
            price = request.POST['price']
            quantity = request.POST.getlist('quantity')
            promocode = request.POST['promocode']

            print("Size>>>>>>>>>>>>>.", size)

            imgStr = ""
            for i in image:
                fs = FileSystemStorage()  # defaults to   MEDIA_ROOT
                fs.save(i.name, i)
                if len(imgStr) == 0:
                    imgStr = i.name.rsplit(".")[0]
                else:
                    imgStr = imgStr + "," + i.name.rsplit(".")[0]

            sizeStr = ""
            for i in size:
                sizeStr = sizeStr + i + ","

            quantityStr = ""
            for i in quantity:
                quantityStr = quantityStr + i + ","
            print("Quantity >>>>>>>>>>>>>>>>>>>>>>>.........", quantityStr)

            colorStr = ""
            for i in color:
                colorStr = colorStr + i + ","
            print(">>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<", colorStr)

            varify = Product.objects.filter(code=code)
            if len(varify) == 0:
                addProduct = Product(code=code, name=name, image="[" + imgStr + "]", category=category,
                                     subcategory=subcategory,
                                     type=type, color=colorStr[0:len(colorStr) - 1], desc=desc, size=sizeStr[0:len(sizeStr) - 1],
                                     price=price,
                                     quantity=quantityStr[0:len(quantityStr) - 1], promocode=promocode, status='active')
                addProduct.save()

                varifyCategory = Category.objects.filter(category=category)
                if len(varifyCategory) == 0:
                    addCategory = Category(category=category, status='active')
                    addCategory.save()

                getCategory = Category.objects.get(category=category)
                varifySubcategory = Subategory.objects.filter(subcategory=subcategory, categoryId_id=getCategory.id)
                if len(varifySubcategory) == 0:
                    addSubcategory = Subategory(subcategory=subcategory, categoryId_id=getCategory.id, status='active')
                    addSubcategory.save()

                getCategory = Category.objects.get(category=category)
                getSubcategory = Subategory.objects.get(subcategory=subcategory, categoryId_id=getCategory.id)
                varifyType = Type.objects.filter(type=type, categoryId_id=getCategory.id,
                                                 subcategoryId_id=getCategory.id)
                if len(varifyType) == 0:
                    addType = Type(type=type, categoryId_id=getCategory.id, subcategoryId_id=getSubcategory.id,
                                   status='active')
                    addType.save()

            return render(request, 'admin/addProduct.html')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminViewProduct(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            productList = Product.objects.all().order_by('-id')
            return render(request, 'admin/viewProduct.html', {'productList': productList})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminDeleteProduct(request, foo):
    try:
        if request.session.get('session_loginRole') == 'admin':
            id = request.GET['id']

            deleteProduct = Product.objects.get(pk=id)
            for i in list(str(deleteProduct.image[1:len(deleteProduct.image) - 1]).split(",")):
                os.remove("../eshoppermodaz/media/" + i + ".jpeg")
            deleteProduct.delete()

            if foo == 'dataset':
                return redirect('/admin/loadDataset')
            else:
                return redirect('/admin/viewProduct')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminEditProduct(request, foo):
    try:
        if request.session.get('session_loginRole') == 'admin':
            navigate = foo
            id = request.GET['id']
            editProduct = Product.objects.get(pk=id)

            return render(request, 'admin/editProduct.html', {'editProduct': editProduct, 'navigate': navigate})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminDeleteImage(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            imageName = request.GET['imageName']
            productId = request.GET['productId']
            print(">>>>>>>>>>>>>>>>>", imageName, "<<<<<<<<<<<<<<<<", productId)
            deleteImage = Product.objects.get(pk=productId)
            images = list(str(deleteImage.image[1:len(deleteImage.image) - 1]).split(","))
            images.remove(imageName)
            os.remove('../eshoppermodaz/media/' + imageName + '.jpeg')

            imgStr = ""
            for i in images:
                if len(imgStr) == 0:
                    imgStr = i
                else:
                    imgStr = imgStr + "," + i

            deleteImage.image = "[" + imgStr + "]"
            deleteImage.save()
            return JsonResponse({'imageName': imageName})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminUpdateProduct(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            id = request.POST['id']
            navigate = request.POST['navigate']
            code = request.POST['code']
            name = request.POST['name']
            image = request.FILES.getlist('image')
            category = request.POST['category']
            subcategory = request.POST['subcategory']
            type = request.POST['type']
            color = request.POST.getlist('color')
            desc = request.POST['desc']
            size = request.POST.getlist('size')
            price = request.POST['price']
            quantity = request.POST['quantity']
            promocode = request.POST['promocode']

            imgStr = ""
            for i in image:
                fs = FileSystemStorage()  # defaults to   MEDIA_ROOT
                fs.save(i.name, i)
                if len(imgStr) == 0:
                    imgStr = i.name.rsplit(".")[0]
                else:
                    imgStr = imgStr + "," + i.name.rsplit(".")[0]

            sizeStr = ""
            for i in size:
                sizeStr = sizeStr + i + ","

            colorStr = ""
            for i in color:
                colorStr = colorStr + i + ","

            updateProduct = Product.objects.get(pk=id)
            if len(imgStr) > 0 and updateProduct.image != "[]":
                image = str(updateProduct.image)[1:len(str(updateProduct.image)) - 1] + "," + imgStr
            elif updateProduct.image == "[]":
                image = imgStr
            else:
                image = str(updateProduct.image)[1:len(str(updateProduct.image)) - 1]

            updateProduct.code = code
            updateProduct.name = name
            updateProduct.image = "[" + image + "]"
            updateProduct.category = category
            updateProduct.subcategory = subcategory
            updateProduct.type = type
            updateProduct.color = "[" + colorStr + "]"
            updateProduct.desc = desc
            updateProduct.size = size
            updateProduct.price = price
            updateProduct.quantity = quantity
            updateProduct.promocode = promocode
            updateProduct.save()

            varifyCategory = Category.objects.filter(category=category)
            if len(varifyCategory) == 0:
                addCategory = Category(category=category, status='active')
                addCategory.save()

            getCategory = Category.objects.get(category=category)
            varifySubcategory = Subategory.objects.filter(subcategory=subcategory, categoryId_id=getCategory.id)
            if len(varifySubcategory) == 0:
                addSubcategory = Subategory(subcategory=subcategory, categoryId_id=getCategory.id, status='active')
                addSubcategory.save()

            getCategory = Category.objects.get(category=category)
            getSubcategory = Subategory.objects.get(subcategory=subcategory, categoryId_id=getCategory.id)
            varifyType = Type.objects.filter(type=type, categoryId_id=getCategory.id, subcategoryId_id=getCategory.id)
            if len(varifyType) == 0:
                addType = Type(type=type, categoryId_id=getCategory.id, subcategoryId_id=getSubcategory.id,
                               status='active')
                addType.save()

            if navigate == 'dataset':
                return redirect('/admin/loadDataset')
            else:
                return redirect('/admin/viewProduct')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminLoadDataset(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            lastDataset = Product.objects.values('pub_date').distinct('pub_date')
            if len(lastDataset) != 0:
                pub_date = lastDataset[0]['pub_date']
                productList = Product.objects.filter(pub_date=pub_date).all().order_by('-id')

                return render(request, 'admin/addDataset.html', {'productList': productList})
            return render(request, 'admin/addDataset.html')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminInsertDataset(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            dataset = request.FILES.getlist('dataset')

            available = ""
            for i in dataset:
                fileName = str(i).rsplit(".")[0]
                data = fileName.split("-")

                if len(data) > 1:
                    code = data[0]
                    name = data[1]
                    category = data[2]
                    subcategory = data[3]
                    type = data[4]
                    color = data[5]
                    desc = data[6]
                    price = data[7]
                    size = data[8]
                    images = data[9]
                    quantity = data[10]

                    varifyCategory = Category.objects.filter(category=category)
                    if len(varifyCategory) == 0:
                        addCategory = Category(category=category, status='active')
                        addCategory.save()

                    getCategory = Category.objects.get(category=category)
                    varifySubcategory = Subategory.objects.filter(subcategory=subcategory, categoryId_id=getCategory.id)
                    if len(varifySubcategory) == 0:
                        addSubcategory = Subategory(subcategory=subcategory, categoryId_id=getCategory.id,
                                                    status='active')
                        addSubcategory.save()

                    getCategory = Category.objects.get(category=category)
                    getSubcategory = Subategory.objects.get(subcategory=subcategory, categoryId_id=getCategory.id)
                    varifyType = Type.objects.filter(type=type, categoryId_id=getCategory.id,
                                                     subcategoryId_id=getCategory.id)
                    if len(varifyType) == 0:
                        addType = Type(type=type, categoryId_id=getCategory.id, subcategoryId_id=getSubcategory.id,
                                       status='active')
                        addType.save()

                    varifyProduct = Product.objects.filter(code=code)

                    if len(varifyProduct) == 0:

                        addProduct = Product(code=code, name=name, image=images,
                                             category=category, subcategory=subcategory,
                                             type=type, color=color,
                                             desc=desc, price=price, size=size, quantity=quantity, status='active')
                        addProduct.save()

                        fs = FileSystemStorage()  # defaults to   MEDIA_ROOT
                        fs.save(i.name, i)

                        os.rename('../eshoppermodaz/media/' + i.name,
                                  '../eshoppermodaz/media/' + code + 'img1.' + str(i).rsplit(".")[1])

                    else:
                        available = available + " " + code

                else:
                    fs = FileSystemStorage()  # defaults to   MEDIA_ROOT
                    fs.save(i.name, i)

                if len(available) != 0:
                    messages.success(request, "this product already available : " + available)

            return redirect('/admin/loadDataset')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminViewCategory(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            categoryList = Category.objects.all().order_by('-id')
            return render(request, 'admin/viewCategory.html', {'categoryList': categoryList})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminInsertCategory(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            category = request.POST['category']
            varify = Category.objects.filter(category=category)
            if len(varify) == 0:
                addCategory = Category(category=category, status='active')
                addCategory.save()
                messages.success(request, 'category successfully saved.')
                return redirect('/admin/viewCategory')
            else:
                messages.success(request, 'Category already exist.')
                return redirect('/admin/viewCategory')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminDeleteCategory(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            id = request.GET['id']
            deleteCategory = Category.objects.get(pk=id)
            deleteCategory.delete()
            messages.success(request, 'category successfully deleted.')
            return redirect('/admin/viewCategory')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminEditCategory(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            id = request.GET['id']
            editCategory = Category.objects.get(pk=id)
            categoryList = Category.objects.all().order_by('-id')
            return render(request, 'admin/viewCategory.html',
                          {'editCategory': editCategory, 'categoryList': categoryList})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminUpdateCategory(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            id = request.POST['id']
            category = request.POST['category']
            varify = Category.objects.filter(category=category)
            if len(varify) == 0:
                updateCategory = Category.objects.get(pk=id)
                updateCategory.category = category
                updateCategory.save()
                messages.success(request, 'category successfully updated.')
                return redirect('/admin/viewCategory')
            else:
                messages.success(request, 'Category already exist.')
                return redirect('/admin/viewCategory')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminViewSubcategory(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            subcategoryList = Subategory.objects.all().order_by('-id')
            categoryList = Category.objects.all().order_by('-id')
            return render(request, 'admin/viewSubcategory.html',
                          {'subcategoryList': subcategoryList, 'categoryList': categoryList})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminInsertSubCategory(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            categoryId = request.POST['categoryId']
            subcategory = request.POST['subcategory']
            varify = Subategory.objects.filter(subcategory=subcategory, categoryId_id=categoryId)
            if len(varify) == 0:
                addCategory = Subategory(subcategory=subcategory, categoryId_id=categoryId, status='active')
                addCategory.save()
                messages.success(request, 'Subcategory successfully saved.')
                return redirect('/admin/viewSubcategory')
            else:
                messages.success(request, 'Subcategory alredy exist.')
                return redirect('/admin/viewSubcategory')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminDeleteSubcategory(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            id = request.GET['id']
            deleteSubcategory = Subategory.objects.get(pk=id)
            deleteSubcategory.delete()
            messages.success(request, 'Subcategory successfully deleted.')
            return redirect('/admin/viewSubcategory')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminEditSubcategory(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            id = request.GET['id']
            editSubcategory = Subategory.objects.get(pk=id)
            subcategoryList = Subategory.objects.all().order_by('-id')
            categoryList = Category.objects.all().order_by('-id')
            return render(request, 'admin/viewSubcategory.html',
                          {'editSubcategory': editSubcategory, 'subcategoryList': subcategoryList,
                           'categoryList': categoryList})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminUpdateSubcategory(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            id = request.POST['id']
            categoryId = request.POST['categoryId']
            subcategory = request.POST['subcategory']
            varify = Subategory.objects.filter(categoryId_id=categoryId, subcategory=subcategory)
            if len(varify) == 0:
                updateSubcategory = Subategory.objects.get(pk=id)
                updateSubcategory.categoryId_id = categoryId
                updateSubcategory.subcategory = subcategory
                updateSubcategory.save()
                messages.success(request, 'Subcategory successfully updated.')
                return redirect('/admin/viewSubcategory')
            else:
                messages.success(request, 'Subcategory already exist.')
                return redirect('/admin/viewSubcategory')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminViewType(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            typeList = Type.objects.all().order_by('-id')
            categoryList = Category.objects.all().order_by('-id')
            return render(request, 'admin/viewType.html', {'categoryList': categoryList, 'typeList': typeList})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminAjaxSubcategory(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            categoryId = request.GET['categoryId']
            subcategoryList = Subategory.objects.filter(categoryId=categoryId)
            ajaxSubcategoryJson = [i.as_dict() for i in subcategoryList]
            return JsonResponse(ajaxSubcategoryJson, safe=False)
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminInsertType(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            categoryId = request.POST['categoryId']
            subcategoryId = request.POST['subcategoryId']
            type = request.POST['type']

            varify = Type.objects.filter(type=type, categoryId_id=categoryId, subcategoryId_id=subcategoryId)
            if len(varify) == 0:
                addType = Type(type=type, subcategoryId_id=subcategoryId, categoryId_id=categoryId, status='active')
                addType.save()
                messages.success(request, 'Type successfuly saved.')
                return redirect('/admin/viewType')
            else:
                messages.success(request, 'Type alredy exist.')
                return redirect('/admin/viewType')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminDeleteType(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            id = request.GET['id']
            deleteType = Type.objects.get(pk=id)
            deleteType.delete()
            messages.success(request, 'Type successfully deleted.')
            return redirect('/admin/viewType')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminEditType(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            id = request.GET['id']
            editType = Type.objects.get(pk=id)
            typeList = Type.objects.all().order_by('-id')
            categoryList = Category.objects.all().order_by('-id')
            return render(request, 'admin/viewType.html',
                          {'typeList': typeList,
                           'categoryList': categoryList, 'editType': editType})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminUpdateType(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            id = request.POST['id']
            categoryId = request.POST['categoryId']
            subcategoryId = request.POST['subcategoryId']
            type = request.POST['type']

            varify = Type.objects.filter(type=type, categoryId_id=categoryId, subcategoryId_id=subcategoryId)
            if len(varify) == 0:
                updateType = Type.objects.get(pk=id)
                updateType.type = type
                updateType.categoryId_id = categoryId
                updateType.subcategoryId_id = subcategoryId
                updateType.save()
                messages.success(request, 'Type successfuly Updated.')
                return redirect('/admin/viewType')

            else:
                messages.success(request, 'Type alredy Exist.')
                return redirect('/admin/viewType')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminLoadBenner(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            return render(request, 'admin/addBenner.html')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminInsertBenner(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            image = request.FILES.get('image')
            link = request.POST['link']
            contact = request.POST['contact']
            rank = request.POST['rank']

            addBenner = Benner(image=image, link=link, contact=contact, rank=rank, status='active')
            addBenner.save()
            messages.success(request, 'Benner successfuly saved.')
            return redirect('/admin/viewBenner')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminViewBenner(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            bennerList = Benner.objects.all().order_by('rank')
            return render(request, 'admin/viewBenner.html', {'bennerList': bennerList})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminDeleteBenner(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            id = request.GET['id']
            deleteBenner = Benner.objects.get(pk=id)
            os.remove('../eshoppermodaz/media/' + str(deleteBenner.image))
            deleteBenner.delete()
            messages.success(request, 'Benner successfuly deleted')
            return redirect('/admin/viewBenner')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminEditBenner(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            id = request.GET['id']
            editBenner = Benner.objects.get(pk=id)
            return render(request, 'admin/addBenner.html', {'editBenner': editBenner})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminUpdateBenner(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            id = request.POST['id']
            image = request.FILES.get('image')
            print(">>>>>>>>>>>>>.", image)
            link = request.POST['link']
            contact = request.POST['contact']
            rank = request.POST['rank']

            updateBenner = Benner.objects.get(pk=id)
            if image != None:
                os.remove('../eshoppermodaz/media/' + str(updateBenner.image))
                updateBenner.image = image
            updateBenner.link = link
            updateBenner.contact = contact
            updateBenner.rank = rank
            updateBenner.save()
            messages.success(request, 'Benner successfuly updated.')
            return redirect('/admin/viewBenner')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminViewOrder(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            allOrder = Order.objects.exclude(orderstatus='addtocart').all().order_by('-id')
            return render(request, 'admin/viewOrder.html', {'allOrder': allOrder})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminOrderStatus(request, foo):
    try:
        if request.session.get('session_loginRole') == 'admin':
            if foo == 'ordered':
                orderId = request.GET['orderId']
                changestatus = Order.objects.get(pk=orderId)
                changestatus.orderstatus = 'ordered'
                product = eval(changestatus.product)
                for key, value in product.items():
                    value['orderstatus'] = 'ordered'
                changestatus.product = product
                changestatus.save()
                return redirect('/admin/viewOrder')

            if foo == 'packed':
                orderId = request.GET['orderId']
                changestatus = Order.objects.get(pk=orderId)
                changestatus.orderstatus = 'packed'
                product = eval(changestatus.product)
                for key, value in product.items():
                    value['orderstatus'] = 'packed'
                changestatus.product = product
                changestatus.save()

                ''' Order Email '''

                sendemailadd = changestatus.userId.loginEmail
                sendMail(foo, sendemailadd)

                return redirect('/admin/viewOrder')

            if foo == 'dispatched':
                orderId = request.GET['orderId']
                changestatus = Order.objects.get(pk=orderId)
                changestatus.orderstatus = 'dispatched'
                product = eval(changestatus.product)
                for key, value in product.items():
                    value['orderstatus'] = 'dispatched'
                changestatus.product = product
                changestatus.save()

                '''  Order Email'''

                sendemailadd = changestatus.userId.loginEmail
                sendMail(foo, sendemailadd)

                return redirect('/admin/viewOrder')

            if foo == 'delivered':
                orderId = request.GET['orderId']
                changestatus = Order.objects.get(pk=orderId)
                changestatus.orderstatus = 'delivered'
                product = eval(changestatus.product)
                for key, value in product.items():
                    value['orderstatus'] = 'delivered'
                changestatus.product = product
                changestatus.save()

                '''  Order Email'''

                sendemailadd = changestatus.userId.loginEmail
                sendMail(foo, sendemailadd)

                return redirect('/admin/viewOrder')

            if foo == 'return':
                orderId = request.GET['orderId']
                productId = request.GET['productId']
                changestatus = Order.objects.get(pk=orderId)
                product = eval(changestatus.product)
                product[productId]['orderstatus'] = 'return'
                today = date.today()
                product[productId]['returnDate'] = str(today)
                changestatus.product = product
                changestatus.save()

                '''  Order Email'''

                sendemailadd = changestatus.userId.loginEmail
                sendMail(foo, sendemailadd)

                if request.session.get('login_Role') == 'admin':
                    return redirect('/admin/viewOrder')
                elif request.session.get('login_Role') == 'user':
                    return redirect('/viewOrder')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)
