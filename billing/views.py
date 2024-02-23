from django.shortcuts import render
from django.shortcuts import render, redirect
from .form import *
from django.contrib.auth import login, authenticate,logout #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from django.db.models import Count, Sum, Avg, Max, Min
from django.db.models import F, ExpressionWrapper
from datetime import date
from .models import *
import datetime
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.loader import get_template
# from html2pdf import HTMLToPDFConverter
from xhtml2pdf import pisa
import os

def home(request):
     return render(request,'billing/home.html')

def generate_pdf(request):
    sales = list(finalbill.objects.filter(status = False).values_list('name','count','mrp','discount','amount',"total"))
    bill_list = []
    grand_dict = {}
    grand_dict["Grand Total"] = {}
    grand_dict["Grand Total"]["count"] = 0
    grand_dict["Grand Total"]["mrp"] = "-"
    grand_dict["Grand Total"]["dis"] = "-"
    grand_dict["Grand Total"]["amount"] = "-"
    grand_dict["Grand Total"]["total"] = 0
    for pro in sales:
        bill_dic = {}
        bill_dic[pro[0]] = {}
        bill_dic[pro[0]]["count"] = pro[1]
        bill_dic[pro[0]]["mrp"] = pro[2]
        bill_dic[pro[0]]["dis"] = pro[3]
        bill_dic[pro[0]]["amount"] = pro[4]
        bill_dic[pro[0]]["total"] = pro[5]
        bill_list.append(bill_dic)

        
        grand_dict["Grand Total"]["count"] += pro[1]
        # grand_dict["Grand Total"]["amount"] += pro[5]
        grand_dict["Grand Total"]["total"] += pro[5]
    bill_list.append(grand_dict)
    print(bill_list)
    html_template = get_template('billing/bill_pdf.html')

    # Get the latest TotalSale object
    product = TotalSale.objects.latest('id')
    print("product",product)
    # Create context data (replace with your actual data)
    context = {'data': bill_list}

    # Render the HTML template with context
    html_content = html_template.render(context)

    # Create a Django HttpResponse with PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="bill.pdf"'

    # Use pisa.CreatePDF to generate PDF content
    pdf_content = pisa.CreatePDF(html_content, dest=response, encoding='utf-8', page_size=(200, 400))

    # Check if PDF generation was successful
    if pdf_content.err:
        return HttpResponse('Error during PDF generation.')

    # Get the actual PDF content from the pisaContext object
    pdf_bytes = pdf_content.dest.getvalue()

    # Save the PDF content to a file (optional)
    static_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')
    pdf_file_path = os.path.join(static_folder, 'bill.pdf')

    with open(pdf_file_path, 'wb') as pdf_file:
        pdf_file.write(pdf_bytes)

    # Return the PDF content as the response
    return response

    return HttpResponse("PDF generated and saved in the static folder.")


def product_add(request):
    print(request.POST)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            instance = form.save()
            print(instance.id)
            stackProduct(
                name = instance,
				count = instance.count,
				mrp = instance.mrp,
				discount = instance.discount,
				amount = instance.amount,			
            ).save()
            return render(request,'billing/product_id.html',{'product_id': instance.id,"product_name":instance.name,"size":instance.size})
    else:
        form = ProductForm()

    return render(request, 'billing/item.html', {'form': form})


def register_request(request):
	print(request.POST)
	if request.method == "POST":
		form = NewUserForm(request.POST)
		print(form)
		print("1")
		if form.is_valid():
			print("2")
			user = form.save()
			login(request, user)
			print("3")
			messages.success(request, "Registration successful." )
			return redirect("/login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
		print("4")
	form = NewUserForm()
	return render (request=request, template_name="billing/register.html", context={"register_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("main:homepage")


def login_request(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                user_type = Access.objects.get(user_map = user.id).user_type_map               

                if user_type.name=="accs":
                    form = IdNumber()
                    return render(request=request, template_name="billing/billing.html", context={"form":form})
            
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="billing/login.html", context={"login_form":form})

def billing(request):
    available = False
    sales =[]
    bill = finalbill.objects.filter(status = False)
    if bill.exists():
         for i in bill:
              final = finalbill.objects.get(id=i.id)
              final.status = True
              final.save()

    if request.method == 'POST':
        form = IdNumber(request.POST)
        print(request.POST["id"])
        if request.POST["id"] != 0:
            if form.is_valid():
                pro_id = request.POST["id"]
                if Product.objects.filter(id=pro_id).exists():
                    products = Product.objects.get(id=pro_id)
                    if products.count != 0:
                        SaleProduct(
                            product = products,
                            size = products.size,
                            count = request.POST["count"],
                            mrp = products.mrp,
                            discount = products.discount,
                            amount = products.amount,
                            status = False,			
                        ).save()
    sales = list(SaleProduct.objects.filter(status = False).values_list('product__name__name','size__name','count','mrp','discount','amount'))
    bill_list = []
    for pro in sales:
        bill_dic = {}
        bill_dic["name"] = pro[0]+"-"+pro[1]
        bill_dic["count"] = pro[2]
        bill_dic["mrp"] = pro[3]
        bill_dic["dis"] = pro[4]
        bill_dic["amount"] = pro[5]
        bill_dic["total"] = pro[2]*pro[5]
        bill_list.append(bill_dic)
    
    if len(sales)>0:
        available = True
    print(sales)
    form = IdNumber()
    return render(request=request, template_name="billing/billing.html", context={"form":form,"available":available,"bill":bill_list})


def billingpay(request):
    sales = list(SaleProduct.objects.filter(status = False).values_list('product__name__name','size__name','count','mrp','discount','amount'))
    bill_list = []
    grand_dict = {}
    grand_dict["name"] = "Grand Total"
    grand_dict["count"] = 0
    grand_dict["mrp"] = "-"
    grand_dict["dis"] = "-"
    grand_dict["amount"] = "-"
    grand_dict["total"] = 0
    for pro in sales:
        bill_dic = {}
        bill_dic["name"] = pro[0]+"-"+pro[1]
        bill_dic["count"] = pro[2]
        bill_dic["mrp"] = pro[3]
        bill_dic["dis"] = pro[4]
        bill_dic["amount"] = pro[5]
        bill_dic["total"] = pro[2]*pro[5]
        bill_list.append(bill_dic)
        
        grand_dict["count"] += pro[2]
        # grand_dict["amount"] += pro[5]
        grand_dict["total"] += pro[2]*pro[5]
    bill_list.append(grand_dict)

    form = PaymentForm()
    form2 = InfoForm()

    return render(request=request, template_name="billing/total.html", context={"form":form,"bill":bill_list,"form2":form2})

            
def bill_pdf(request):
    print("yes")
    print(request.POST)
    payments = Payment.objects.create(
         cash = int(request.POST["cash"]),
         upi = int(request.POST["upi"]),
    )
    sales = list(SaleProduct.objects.filter(status = False).values_list('product__name__name','size__name','count','mrp','discount','amount'))
    bill_list = []
    grand_dict = {}
    grand_dict["Grand Total"] = {}
    grand_dict["Grand Total"]["count"] = 0
    grand_dict["Grand Total"]["mrp"] = "-"
    grand_dict["Grand Total"]["dis"] = "-"
    grand_dict["Grand Total"]["amount"] = 0
    grand_dict["Grand Total"]["total"] = 0
    for pro in sales:
        bill_dic = {}
        bill_dic[pro[0]+"-"+pro[1]] = {}
        bill_dic[pro[0]+"-"+pro[1]]["count"] = pro[2]
        bill_dic[pro[0]+"-"+pro[1]]["mrp"] = pro[3]
        bill_dic[pro[0]+"-"+pro[1]]["dis"] = pro[4]
        bill_dic[pro[0]+"-"+pro[1]]["amount"] = pro[5]
        bill_dic[pro[0]+"-"+pro[1]]["total"] = pro[2]*pro[5]
        bill_list.append(bill_dic)

        
        grand_dict["Grand Total"]["count"] += pro[2]
        grand_dict["Grand Total"]["amount"] += pro[5]
        grand_dict["Grand Total"]["total"] += pro[2]*pro[5]
        finalbill(
             name = pro[0]+"-"+pro[1],
             count = pro[2],
             mrp = pro[3],
             discount = pro[4],
             amount = pro[5],
             total = pro[2]*pro[5]

        ).save()
    bill_list.append(grand_dict)
    products = SaleProduct.objects.filter(status = False)
    total_sale = TotalSale(
                            customer_name = request.POST["customer_name"],
                            ph_no = request.POST["ph_no"],
                            total_amount = grand_dict["Grand Total"]["total"],
                            payment = payments,
                        )
    total_sale.save()
    for i in products:
         total_sale.product.add(i)

    
    for data in SaleProduct.objects.filter(status = False):
        if data.status == False:
            data.status = True
            data.save()
        products_obj = Product.objects.get(id=data.product.id)
        products_obj.count =  int(products_obj.count)-data.count
        products_obj.save()
    print(bill_list)
    pdf = generate_pdf(bill_list)

            
        
    return render(request=request, template_name="billing/Success.html",context={"form":"okay","pdf":pdf})

def dat_report(request):
    print(datetime.date.today(),type(datetime.date.today()))
    sales = SaleProduct.objects.filter(date = str(datetime.date.today()))
    name = list(set(sales.values_list("product__name__name",flat=True)))
    sales = list(sales.filter(date = str(datetime.date.today())).values_list('product__name__name','count','mrp','discount','amount'))
    print(name)
    bill_list = []
    grand_dict = {}
    grand_dict["Grand Total"] = {}
    grand_dict["Grand Total"]["count"] = 0
    grand_dict["Grand Total"]["mrp"] = "-"
    grand_dict["Grand Total"]["dis"] = "-"
    grand_dict["Grand Total"]["amount"] = "-"
    grand_dict["Grand Total"]["total"] = 0

    for i in name:
        dicts = {}
        dicts[i] = {}
        dicts[i]["count"] = 0
        dicts[i]["mrp"] = 0
        dicts[i]["dis"] = 0
        dicts[i]["amount"] = 0
        dicts[i]["total"] = 0
        bill_list.append(dicts)
     
    for pro in sales:
        index = name.index(pro[0])
        bill_list[index][pro[0]]["count"] += pro[1]
        bill_list[index][pro[0]]["mrp"] = pro[2]
        bill_list[index][pro[0]]["dis"] = pro[3]
        bill_list[index][pro[0]]["amount"] = pro[4]
        total = pro[1] * pro[4]
        bill_list[index][pro[0]]["total"] += total

        
        grand_dict["Grand Total"]["count"] += pro[1]
        grand_dict["Grand Total"]["total"] += total
    bill_list.append(grand_dict)

    html_template = get_template('billing/daily_report.html')

    context = {'data': bill_list}

    # Render the HTML template with context
    html_content = html_template.render(context)

    # Create a Django HttpResponse with PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="today bill.pdf"'

    # Use pisa.CreatePDF to generate PDF content
    pdf_content = pisa.CreatePDF(html_content, dest=response, encoding='utf-8', page_size=(200, 400))

    # Check if PDF generation was successful
    if pdf_content.err:
        return HttpResponse('Error during PDF generation.')

    # Get the actual PDF content from the pisaContext object
    pdf_bytes = pdf_content.dest.getvalue()

    # Save the PDF content to a file (optional)
    static_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')
    pdf_file_path = os.path.join(static_folder, 'today bill.pdf')

    with open(pdf_file_path, 'wb') as pdf_file:
        pdf_file.write(pdf_bytes)

    # Return the PDF content as the response
    return response
     
    return render(request=request, template_name="billing/daily_report.html",context={"form":"okay","pdf":pdf})