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



def products(request):
    data=dict()
    cursor,mydb=database()
    try:
       pcode=request.GET.get('pcode')
       print(pcode)
       c="select * from products where Product_Code='{}'".format(pcode)
       cursor.execute(c)
       result=cursor.fetchall()
       image_bytes = base64.b64decode(result[0][8])
       image = Image.open(io.BytesIO(image_bytes))
            
        # Resize the image to 300x300
       resized_image = image.resize((334, 300))
       resized_image_bytes = io.BytesIO()
       resized_image.save(resized_image_bytes, format='PNG')
       data['pcode']=result[0][0]
       data['pname']=result[0][1]
       data['unit']=result[0][2]
       data['price']=result[0][4]
       data['size']=result[0][6]
       data['image']=base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8') 
       data['quality']=result[0][9]
       data['purity']=result[0][10]
       data['premium']=result[0][11]
       data['healthy']=result[0][12]
       data['purity_level']=result[0][13]
       data['experience']=result[0][14]
       data['safety']=result[0][15]
       data['packaging']=result[0][16]
       data['real_taste']=result[0][17]
       data['discount']=result[0][18]
       data['quality_head']=result[0][19]
       data['purity_head']=result[0][20]
       data['premium_head']=result[0][21]
       data['heading_1']=result[0][23]
       data['heading_2']=result[0][24]
       data['discount_price']=int(data['price'])-int(data['price'])*int(data['discount'])/100

       c="select * from product_variant where Product_Code='{}'".format(pcode)
       cursor.execute(c)
       result=cursor.fetchall()
       variant=[]
       var={
               'size': data['size'],
               'price': data['price']-int(data['price'])*int(data['discount'])/100
           }
       variant.append(var)
       for x in result:
           var={
               'size': x[1],
               'price': x[2]-int(x[2])*int(data['discount'])/100
           }
           variant.append(var)
       data['variant']=variant   
       c="select * from product_image where Product_ID='{}'".format(pcode)
       cursor.execute(c)
       result=cursor.fetchall()
       images=[]
       for x in result:
            image_bytes = base64.b64decode(x[1])
            image = Image.open(io.BytesIO(image_bytes))
                    
            # Resize the image to 300x300
            resized_image = image.resize((334, 300))
            resized_image_bytes = io.BytesIO()
            resized_image.save(resized_image_bytes, format='PNG')
            image={
                'image': base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8')
            }
            images.append(image)
       data['images']=images  
    except:
       1     
    
    return render(request,"products.html",data)
