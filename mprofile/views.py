from django.shortcuts import render, redirect
from login.models import Loginmaster
from .models import Address
from django.http import JsonResponse


# Create your views here.

def loadMyprofile(request):
    try:
        if request.session.get('session_loginRole') == 'user':
            viewAddress = Address.objects.filter(login_Id=request.session['login_Id']).order_by("id")

            return render(request, 'user/myprofile.html', {'viewAddress': viewAddress, 'default': 'default'})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def updatePassword(request):
    try:
        if request.session.get('session_loginRole') == 'user':
            currentPassword = request.POST['currentPassword']
            newPasssword = request.POST['newPasssword']
            cofirmPassword = request.POST['cofirmPassword']

            update = Loginmaster.objects.get(pk=request.session['login_Id'])

            if currentPassword == update.loginPassword:
                if newPasssword == cofirmPassword:
                    update.loginPassword = newPasssword
                    update.save()
                    return render(request, 'user/myprofile.html',
                                  {'sucess': 'your Password change successfully'})
                else:
                    return render(request, 'user/myprofile.html',
                                  {'matchError': 'New password and Confirmpasswor does not match'})

            else:
                return render(request, 'user/myprofile.html', {'c_passError': 'Please enter correct current password'})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def editAddress(request):
    try:
        if request.session.get('session_loginRole') == 'user':
            addressId = request.GET['addressId']
            viewAddress = Address.objects.filter(pk=addressId)
            return render(request, 'user/editAddress.html', {'addressId': addressId, 'viewAddress': viewAddress})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def updateAddress(request):
    try:
        if request.session.get('session_loginRole') == 'user':
            fullName = request.POST['fullName']
            mobileNo = request.POST['mobileNo']
            alternetMobileNo = request.POST['alternetMobileNo']
            PINCode = request.POST['PINCode']
            home = request.POST['home']
            address = request.POST['address']
            landmark = request.POST['landmark']
            town = request.POST['town']
            state = request.POST['state']
            country = request.POST['country']
            addressId = request.POST['addressId']

            updateAddress = Address.objects.get(pk=addressId)
            updateAddress.fullName = fullName
            updateAddress.mobileNo = mobileNo
            updateAddress.PINCode = PINCode
            updateAddress.home = home
            updateAddress.address = address
            updateAddress.town = town
            updateAddress.state = state
            updateAddress.country = country
            if alternetMobileNo != "":
                updateAddress.alternetMobileNo = alternetMobileNo
            if landmark == "":
                updateAddress.landmark = landmark
            updateAddress.save()

            return redirect('/loadMyprofile')
        else:
            return redirect('/loadLogin')
    except Exception as e:
        print(e)

def loadAddress(request):
    try:
        if request.session.get('session_loginRole') == 'user':
            return render(request, 'user/addAddress.html')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def insertAddress(request):
    try:
        if request.session.get('session_loginRole') == 'user':
            fullName = request.POST['fullName']
            mobileNo = request.POST['mobileNo']
            alternetMobileNo = request.POST['alternetMobileNo']
            PINCode = request.POST['PINCode']
            home = request.POST['home']
            address = request.POST['address']
            landmark = request.POST['landmark']
            town = request.POST['town']
            state = request.POST['state']
            country = request.POST['country']

            addAddress = Address(fullName=fullName, mobileNo=mobileNo, PINCode=PINCode,
                                 home=home, address=address, landmark=landmark, town=town, state=state, country=country,
                                 login_Id_id=request.session['login_Id'], action="no default")
            if alternetMobileNo != "":
                addAddress.alternetMobileNo = alternetMobileNo
            if landmark == "":
                addAddress.landmark = landmark
            addAddress.save()

            return redirect('/loadMyprofile')
        else:
            return redirect('/loadLogin')
    except Exception as e:
        print(e)

def deleteAddress(request):
    try:
        if request.session.get('session_loginRole') == 'user':
            addressId = request.GET['addressId']
            deleteAddress = Address.objects.get(pk=addressId)
            deleteAddress.delete()
            return JsonResponse({"addressId": addressId})
        else:
            return redirect('/loadLogin')
    except Exception as e:
        print(e)


def insertDefault(request):
    try:
        if request.session.get('session_loginRole') == 'user':
            addressId = request.GET['addressId']
            beforeDefault = addressId
            remove = Address.objects.filter(login_Id=request.session['login_Id'], action="default")
            if len(remove) != 0:
                remove[0].action = "no default"
                remove[0].save()
                beforeDefault = remove[0].id

            addDefault = Address.objects.get(pk=addressId)
            addDefault.action = 'default'
            addDefault.save()
            return JsonResponse({"addressId": addressId, "beforeDefault": beforeDefault})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)