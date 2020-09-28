from django.shortcuts import render, redirect
from .models import Complain, Feedback
from mycart.models import Order
from datetime import datetime


# Create your views here.

# ------------- complain admin ------------------------------------------
def adminViewComplain(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            viewComplainList = Complain.objects.filter(complainStatus='pending')
            return render(request, 'admin/viewComplain.html', {'viewComplainList': viewComplainList})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminComplainreply(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            id = request.GET['id']
            getcomplain = Complain.objects.get(pk=id)
            return render(request, 'admin/reply.html', {'getcomplain': getcomplain})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def adminInsertreply(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            id = request.POST['id']
            replysub = request.POST['replysub']
            replymsg = request.POST['replymsg']

            reply = Complain.objects.get(pk=id)
            reply.replySubject = replysub
            reply.replyMessage = replymsg
            reply.replyDate = datetime.today().date()
            reply.replyTime = datetime.today().time()
            reply.complainStatus = "reply"
            reply.save()
            return redirect('/admin/viewComplain')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)

# ---------------------- comaplain user -------------------------------


def loadComplain(request):
    try:
        if request.session.get('session_loginRole') == 'user':
            return render(request, 'user/addComplain.html')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def insertComplain(request):
    try:
        if request.session.get('session_loginRole') == 'user':
            subject = request.POST['subject']
            description = request.POST['description']

            addComplain = Complain(complainSubject=subject, complainDescription=description,
                                   complainTo_LoginId_id=request.session['login_Id'], complainStatus='pending')
            addComplain.save()

            return redirect('/viewComplain')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def viewComplain(request):
    try:
        if request.session.get('session_loginRole') == 'user':
            viewComplainList = Complain.objects.filter(complainTo_LoginId=request.session['login_Id'])
            return render(request, 'user/viewComplain.html', {'viewComplainList': viewComplainList})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def deleteComplain(request):
    try:
        if request.session.get('session_loginRole') == 'user':
            id = request.GET['id']

            deleteComplain = Complain.objects.get(pk=id)
            deleteComplain.delete()
            return redirect('/viewComplain')
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


# -------------------------- feedback user ----------------------------------------------------

def loadFeedback(request):
    try:
        if request.session.get('session_loginRole') == 'user':
            productId = request.GET['productId']
            orderId = request.GET['orderId']
            return render(request, 'user/addFeedback.html', {'productId': productId,'orderId':orderId})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)


def insertFeedback(request):
    try:
         if request.session.get('session_loginRole') == 'user':
            rating = request.POST['feedbackRating']
            description = request.POST['description']
            productId = request.POST['productId']
            orderId = request.POST['orderId']

            getOrder = Order.objects.get(pk=orderId)
            product = eval(getOrder.product)
            product[productId]['feedback'] = 'yes'
            getOrder.product = product
            getOrder.save()

            addFeedback = Feedback(rating=rating, feedback=description, feedbackTo_LoginId_id=request.session['login_Id'],
                                   productId_id=productId)
            addFeedback.save()

            return redirect('/viewOrder')
         else:
             return redirect("/loadLogin")
    except Exception as e:
        print(e)

def viewFeedback(request):
    try:
        if request.session.get('session_loginRole') == 'user':
            getFeedbackList = Feedback.objects.filter(feedbackTo_LoginId_id=request.session['login_Id'])
            return render(request,'user/viewFeedback.html',{'getFeedbackList':getFeedbackList})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)

#----------------- feedback admin ------------------------

def adminViewFeedback(request):
    try:
        if request.session.get('session_loginRole') == 'admin':
            viewFeedbackList = Feedback.objects.all()

            return render(request,'admin/viewFeedback.html',{'viewFeedbackList':viewFeedbackList})
        else:
            return redirect("/loadLogin")
    except Exception as e:
        print(e)
