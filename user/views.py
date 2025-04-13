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

#from django.utils.text import force_bytes, force_text
# Create your views here.

# views.py


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

def about_company(request):
    return render(request,"about-company.html")

def terms_condition(request):
    return render(request,"terms-and-conditions.html")

def contact_us(request):
    return render(request,"contact-us.html")

def checkout(request):
    data=dict()
    cursor,mydb=database()
    if request.method=='POST':
        pcode=request.POST['pcode']
        try:
          price=request.POST['option']
        except:
           c="select Sales_Price,Discount from products where Product_Code='{}'".format(pcode)  
           cursor.execute(c)
           pp=cursor.fetchall()
           price=int(pp[0][0])-int(pp[0][0])*int(pp[0][1])/100
        qty=request.POST['numberInput']
        data['qty']=qty
        data['price']=price
        data['pcode']=pcode

        c="select Product_Name,Image,Product_Unit,Discount from products where Product_Code='{}'".format(pcode)
        cursor.execute(c)
        result=cursor.fetchall()

        products=[]
       
        image_bytes = base64.b64decode(result[0][1])
        image = Image.open(io.BytesIO(image_bytes))
                
            # Resize the image to 50x50
        resized_image = image.resize((50,50))
        resized_image_bytes = io.BytesIO()
        resized_image.save(resized_image_bytes, format='PNG')
      
    
        data['pname']= result[0][0]
        data['image']= base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8') 
        data['unit']=result[0][2]
        data['total']=float(price)*float(qty)
        try:
            c="select Product_Size,Product_Price from product_variant where Product_Code='{}' and Discount_Price='{}'".format(pcode,price)
            cursor.execute(c)
            result=cursor.fetchall()
            data['size']=result[0][0]
            data['org_price']=result[0][1]*int(qty)
        except:
            c="select Product_Size,Sales_Price from products where Product_code='{}'".format(pcode)
            cursor.execute(c)
            result=cursor.fetchall()
            data['size']=result[0][0]
            data['org_price']=result[0][1]*int(qty)
        product_size=int(data['qty'])*int(data['size'])  
        product_size=product_size-1  
        data['delivery_charge_inside_dhaka']=110+product_size*20
        data['delivery_charge_outside_dhaka']=130+product_size*20
  
    return render(request,"checkout.html",data)

def order_request(request):
    data=dict()
    cursor,mydb=database()
    if request.method=='POST':
        pcode=request.POST['pcode']
        size=request.POST['size']
        qty=request.POST['qty']
        org_price=request.POST['org_price']
        dis_price=request.POST['dis_price']
        product_price=request.POST['pprice']
        try:
          option=request.POST['option'] #delivery charge
        except:
          option=130
        try:  
          cod=request.POST['cod']
        except:
           1  
        #customer info
        name=request.POST['name']
        address=request.POST['address']
        district=request.POST['district']
        upazila=request.POST['upazila']
        mobile=request.POST['mobile']
        note=request.POST['note']
        if len(note) == 0:
           note="No Comment"
        customer_address=district+','+upazila
        phone=mobile[6:12]
        cid='C'+'-'+phone
        c="select Name from customer where Contact='{}'".format(mobile)
        cursor.execute(c)
        result=cursor.fetchall()
        
        data['zila']=district
        data['upazila']=upazila
        
        phone=mobile[6:12]
        cid='C'+'-'+phone
        if len(result) == 0:
            c="insert into customer values('{}','{}','{}','{}','{}')".format(cid,name,mobile,customer_address,'Null')
            cursor.execute(c)
            mydb.commit()
        discount=float(org_price)-float(dis_price)
        total=float(dis_price)+int(option)
        c="select max(Serial) from sales"
        cursor.execute(c)
        sale_list=cursor.fetchall()
        sale_list=sale_list[0][0]
        try:
          l=int(sale_list)
          l=l+1  
        except:
          l=1  
    
        current_date = datetime.now()
        current_month = current_date.month
        current_year = current_date.year
        current_day =current_date.day

        if int(current_month)<10:
          current_month='0'+str(current_month)
        if int(current_day)<10:
          current_day='0'+str(current_day)  
        date=str(current_year)+'-'+str(current_month)+'-'+str(current_day)
        date2=date
        date = str(date).replace('-', '')
        order_id='PF'+date[2:]+str(l)
        edited_by=''

        date_str = datetime.strptime(date2, "%Y-%m-%d")
        formatted_date = date_str.strftime("%d %B %Y")
        c="select Product_Name from products where Product_Code='{}'".format(pcode)
        cursor.execute(c)
        pname=cursor.fetchall()
        data['pname']=pname[0][0]
        data['oid']=order_id
        data['delivery_charge']=float(option)
      
        data['discount']=float(discount)
        data['qty']=qty
        data['total']=float(total)
        data['date']=formatted_date
 
        c="insert into sales values(sysdate(),'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',sysdate(),sysdate(),'{}','{}')".format(order_id,cid,"Pending",0,0,option,total,'Website',edited_by,address,'to be select',l,note)
        cursor.execute(c)
        mydb.commit()
        c="select Purchase_Price,Product_Unit,Product_Size from products where Product_Code='{}'".format(pcode)
        cursor.execute(c)
        result=cursor.fetchall()
        pprice=result[0][0]
        unit=result[0][1]
        purchase=int(pprice)/int(result[0][2])
        purchase=int(purchase)*int(size)*int(qty)
        product_price=float(org_price)
        data['product_price']=float(product_price)
        c="insert into sales_order values('{}','{}','{}','{}','{}','{}','{}','{}','none','{}')".format(order_id,pcode,discount,purchase,product_price,dis_price,qty,unit,size)
        cursor.execute(c)
        mydb.commit()
    return redirect('confirmation',oid=order_id)    


def add_products(request):
    return render(request,"add-products.html")

def confirmation(request, oid):
    data=dict()
    cursor,mydb=database()
    c="select Customer_id,Order_date,Delivery,Total,Destination from sales where Order_id='{}'".format(oid)
    cursor.execute(c)
    result=cursor.fetchall()
    data['total']=float(result[0][3])
    data['date']=result[0][1]
    data['oid']=oid
    data['delivery_charge']=float(result[0][2])
    data['destination']=result[0][4]
    print(oid) 
    c="select * from customer where ID='{}'".format(result[0][0])
    cursor.execute(c)
    result=cursor.fetchall()
    address = result[0][3].split(',')

    data['zila']=address[0]
    data['upazila']=address[1]
    
    c="select Product_code,Discount,Sales_price,Payable,Qty,Product_Size,unit from sales_order where Order_id='{}'".format(oid)
    cursor.execute(c)
    result=cursor.fetchall()
      
    data['discount']=float(result[0][1])
    data['qty']=result[0][4]
    data['product_price']=float(result[0][2])
    data['psize']=result[0][5]
    data['unit']=result[0][6]
    c="select Product_Name from products where Product_Code='{}'".format(result[0][0])
    cursor.execute(c)
    result=cursor.fetchall()
    data['pname'] = result[0][0]
    return render(request,'thank-you.html',data)