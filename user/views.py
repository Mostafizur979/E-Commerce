import base64
import io
from django.shortcuts import render,redirect
import mysql.connector as sql

from PIL import Image
import datetime
from datetime import datetime
from num2words import num2words
import math

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required


from django.http import Http404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt



def database():

    mydb = sql.connect(
      host="localhost",
      user="root",
      password="",
      database="premiumfoods"
      )
           
    cursor=mydb.cursor()
    return cursor,mydb


def user_home(request):
    data=dict()
    cursor,mydb=database()
    c="select Image from banner where ID='Desktop'"
    cursor.execute(c)
    result=cursor.fetchall()
    desktop_banner=[]
    for img in result:
        image_bytes = base64.b64decode(img[0])
        image = Image.open(io.BytesIO(image_bytes))
        resized_image = image.resize((1200, 500))
        resized_image_bytes = io.BytesIO()
        resized_image.save(resized_image_bytes, format='PNG')
        bn={
          'img' : base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8')
       }
        desktop_banner.append(bn)

    data['desktop_banners']=desktop_banner  

    c="select Image from banner where ID='Mobile'"
    cursor.execute(c)
    result=cursor.fetchall()
    mobile_banner=[]
    for img in result:
        image_bytes = base64.b64decode(img[0])
        image = Image.open(io.BytesIO(image_bytes))
        resized_image = image.resize((1200, 500))
        resized_image_bytes = io.BytesIO()
        resized_image.save(resized_image_bytes, format='PNG')
        bn={
          'img' : base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8')
       }
        mobile_banner.append(bn)

    data['mobile_banners']=mobile_banner 
    c="select Product_Code,Product_Name,Image,Sales_Price,Discount from products"
    cursor.execute(c)
    result=cursor.fetchall()

    products=[]
    for x in result:
        image_bytes = base64.b64decode(x[2])
        image = Image.open(io.BytesIO(image_bytes))
            
        # Resize the image to 200x200
        resized_image = image.resize((190, 190))
        resized_image_bytes = io.BytesIO()
        resized_image.save(resized_image_bytes, format='PNG')
        price=float(x[3])
        dis_price=price-price*int(x[4])/100
        name=x[1]
       
        if len(name) > 22:
           name=str(name[:22])+'...'
        product={
            'pcode': x[0],
            'pname': name,
            'price': price,
            'dis_price': dis_price,
            'image': base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8'),
            'discount': int(x[4])
        }
        products.append(product)
    data['products']=products    
    return render(request,"user_home.html",data)
