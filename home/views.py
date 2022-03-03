from types import coroutine
from typing import ItemsView
from django.core.checks import messages
from django.http.response import HttpResponse
from django.shortcuts import render
from django.utils.translation import deactivate_all
from .models import Salesbill, Salesbillitems, Stock,Sales,Credit,Purchasebill,Purchasebillitems,Expenses,Saving
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger


# Create your views here.
def index(request):
    # for total sale,expenses
    obj_sales=Sales.objects.all()
    totalsale=0.0
    for data in obj_sales:
        totalsale=round(totalsale+float(data.Total),2)
    obj_sales=Salesbillitems.objects.all()
    totalsaleb=0.0
    totalsalec=0.0
    for data in obj_sales:
        totalsaleb=round(totalsaleb+float(data.Total),2)
        totalsalec=round(totalsalec+float(data.Total),2)
    obj_salesbil=Salesbill.objects.all()
    totalsalebil=0.0
    for data in obj_salesbil:
        totalsalebil=round(totalsalebil+float(data.Paid),2)

    obj_purchase=Purchasebillitems.objects.all()
    obj_expense=Credit.objects.all()
    obj_save=Saving.objects.all()
    totalpurchase=0.0
    for data in obj_purchase:
        totalpurchase=round(totalpurchase+float(data.Total),2)
    totalexpense=0.0
    for data in obj_expense:
        totalexpense=round(totalexpense+float(data.Due_left),2)
    #for credit on salesbill
    
    totalsave=0.0
    for data in obj_save:
        totalsave=round(totalsave+float(data.Amount),2)
# for recently sold products
    obj_sales=Sales.objects.all().order_by('-Date')[:5]
    
    #for total or highest creditors
    obj_credit=Credit.objects.all().order_by('-Due_left')[:5]
    context={
        'totalsale':totalsale+totalsaleb,
        'totalpurchase':totalpurchase,
        'totalexpense':totalexpense + totalsalec-totalsalebil,
        'totalsave':totalsave,
        'data':obj_sales,
        'creditt':obj_credit,
    }
    return render(request,'dashboard.html',context)
def sales(request):
    count=0
    objec=Sales.objects.all()
    for data in objec:
        count+=1
    p=Paginator(objec,5)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    #for totoal sale and total credit
    total_sale=0.0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
        

    if request.method=='POST':
        date=request.POST['date2']
        customer=request.POST['cname']
        phone=request.POST['cphone']
        address=request.POST['caddress']
        product=request.POST['product']
        quantity=request.POST['quantity']
        rate=request.POST['rate']
        dis=request.POST['discount']
        total=request.POST['total']
        paid=request.POST['paid']
        rem=request.POST['dueleft']
        #for discount
        discount=round((float(dis)/100)*float(total),2)
        # for checking the stock
        stock_quan=Stock.objects.filter(Product=product)
        for datas in stock_quan:
            left_quan=datas.Left
        if int(left_quan)<int(quantity):
            return render(request,'sales.html',{'data':data,'message':"OUT OF STOCK"})

        elif len(product)!=0:
            objec=Sales.objects.create(Date=date,Customer_name=customer,
            Customer_phone=phone,Customer_address=address,Product=product,
            Quantity=quantity,Rate=rate,Discount=discount,
            Total=total,Paid=paid,Due_left=rem)
            objec.save()
            #for credt
            if int(rem)>0:
                objec=Credit.objects.create(Date=date,Customer_name=customer,
                Customer_phone=phone,Customer_address=address,Product=product,
                Quantity=quantity,Rate=rate,Discount=discount,
                Total=total,Paid=paid,Due_left=rem)
                objec.save()
                print("Credit saves")

            objec=Sales.objects.all()
            p=Paginator(objec,5)
            page=request.GET.get('page')
            data=p.get_page(page)
            #for decraesing sdtock 
            stock_obj=Stock.objects.filter(Product=product)
            for obj in stock_obj:
                remain=int(obj.Left)-int(quantity)
                stock_obj.update(Left=remain)
            #for total sale and total credit
            objec=Sales.objects.all()
            total_sale=0
            for datass in objec:
                total_sale=round(float(datass.Total)+total_sale,2)
            total_credit=0
            for datass in objec:
                total_credit=round(float(datass.Due_left)+total_credit,2)
            return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit})

    stk=Stock.objects.all()
    return render(request,'sales.html',{'data':data,'obj':stk,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})
def searchsale(request):
    if request.method=='POST':
        date=request.POST['findtext']
        factor=request.POST['searchtype']

        if factor=='Date':
            count=0
            objec=Sales.objects.filter(Date__icontains=date)
            for data in objec:
                count+=1
            p=Paginator(objec,5)
            page=request.GET.get('page')
            data=p.get_page(page)
            start=data.start_index()
            end=data.end_index()
            #for totoal sale and total credit
            total_sale=0.0
            for datass in objec:
                total_sale=round(float(datass.Total)+total_sale,2)
                
                
            total_credit=0
            for datass in objec:
                total_credit=round(float(datass.Due_left)+total_credit,2)
            return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'start':start,'end':end,'count':count})
        if factor=='Customer Name':
            count=0
            objec=Sales.objects.filter(Customer_name__icontains=date)
            for data in objec:
                count+=1
            p=Paginator(objec,5)
            page=request.GET.get('page')
            data=p.get_page(page)
            start=data.start_index()
            end=data.end_index()
            #for totoal sale and total credit
            total_sale=0.0
            for datass in objec:
                total_sale=round(float(datass.Total)+total_sale,2)
                
                
            total_credit=0
            for datass in objec:
                total_credit=round(float(datass.Due_left)+total_credit,2)
            return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'start':start,'end':end,'count':count})
        if factor=='Product':
            count=0
            objec=Sales.objects.filter(Product__icontains=date)
            for data in objec:
                count+=1
            p=Paginator(objec,5)
            page=request.GET.get('page')
            data=p.get_page(page)
            start=data.start_index()
            end=data.end_index()
            #for totoal sale and total credit
            total_sale=0.0
            for datass in objec:
                total_sale=round(float(datass.Total)+total_sale,2)
                
                
            total_credit=0
            for datass in objec:
                total_credit=round(float(datass.Due_left)+total_credit,2)
            return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'start':start,'end':end,'count':count})
        
# for searchsale
def searchsales(request,product):
    count=0
    objec=Sales.objects.filter(Product__icontains=product).order_by('-Date')[:1]
    for data in objec:
        count+=1
    p=Paginator(objec,5)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    
        
    #for totoal sale and total credit
    total_sale=0.0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'start':start,'end':end,'count':count})
#for ordering of sales
def saledd(request):
    objec=Sales.objects.all().order_by('-Date')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_sale=0.0
    count=0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        count+=1
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})
def saledi(request):
    objec=Sales.objects.all().order_by('Date')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_sale=0.0
    count=0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        count+=1
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})
def salecd(request):
    objec=Sales.objects.all().order_by('-Customer_name')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_sale=0.0
    count=0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        count+=1
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})
def saleci(request):
    objec=Sales.objects.all().order_by('Customer_name')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_sale=0.0
    count=0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        count+=1

        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})
def salepi(request):
    objec=Sales.objects.all().order_by('Product')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_sale=0.0
    count=0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        count+=1
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})
def salepd(request):
    objec=Sales.objects.all().order_by('-Product')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_sale=0.0
    count=0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        count+=1
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})
def saleqd(request):
    objec=Sales.objects.all().order_by('-Quantity')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_sale=0.0
    count=0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        count+=1
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})
def saleqi(request):
    objec=Sales.objects.all().order_by('Quantity')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_sale=0.0
    count=0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        count+=1
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})
def salerd(request):
    objec=Sales.objects.all().order_by('-Rate')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_sale=0.0
    count=0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        count+=1
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})
def saleri(request):
    objec=Sales.objects.all().order_by('Rate')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_sale=0.0
    count=0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        count+=1
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})
def saledid(request):
    objec=Sales.objects.all().order_by('-Discount')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_sale=0.0
    count=0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        count+=1
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})
def saledii(request):
    objec=Sales.objects.all().order_by('Discount')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_sale=0.0
    count=0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        count+=1
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})
def saletd(request):
    objec=Sales.objects.all().order_by('-Total')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_sale=0.0
    count=0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        count+=1
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})
def saleti(request):
    objec=Sales.objects.all().order_by('Total')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_sale=0.0
    count=0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        count+=1
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})
def salepad(request):
    objec=Sales.objects.all().order_by('-Paid')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_sale=0.0
    count=0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        count+=1
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})
def salepai(request):
    objec=Sales.objects.all().order_by('Paid')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_sale=0.0
    count=0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        count+=1
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})
def salered(request):
    objec=Sales.objects.all().order_by('-Due_left')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_sale=0.0
    count=0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        count+=1
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})
def salerei(request):
    objec=Sales.objects.all().order_by('Due_left')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_sale=0.0
    count=0
    for datass in objec:
        total_sale=round(float(datass.Total)+total_sale,2)
        count+=1
        
    total_credit=0
    for datass in objec:
        total_credit=round(float(datass.Due_left)+total_credit,2)
    return render(request,'sales.html',{'data':data,'totalsale':total_sale,'totalcredit':total_credit,'count':count,'start':start,'end':end})


def stock(request):
    objec=Stock.objects.all().order_by('Product')
    count=0
    for data in objec:
        count+=1
    p=Paginator(objec,8)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    
    
    #for total quantity
    total_quantity=0
    for datass in objec:
        total_quantity+=int(datass.Total)
    left_quantity=0
    for datass in objec:
        left_quantity+=int(datass.Left)

    
    if request.method=='POST':
        product=request.POST['product']
        total=request.POST['totquan']
        left=request.POST['leftquan']
        cp=request.POST['cp']
        sp=request.POST['sp']
        obj=Stock.objects.filter(Product=product)
        if len(obj)==0 and len(product)!=0:
            user=Stock.objects.create(Product=product,Total=total,Left=left,Cost=cp,Sold=sp)
            user.save()
            objec=Stock.objects.all().order_by('Product')
            total_quantity=0
            for datass in objec:
                total_quantity+=int(datass.Total)
            left_quantity=0
            for datass in objec:
                left_quantity+=int(datass.Left)
            p=Paginator(objec,8)
            for data in objec:
                count+=1
            page=request.GET.get('page')
            data=p.get_page(page)
    
            
            start=data.start_index()
            end=data.end_index()
            return render(request,'stock.html',{'data':data,'count':count,'start':start,'end':end,'total_quantity':total_quantity,'Left_quantity':left_quantity})
        if len(obj)!=0:
            for ob in obj:
                obj.update(Product=product,Total=int(ob.Total)+int(total),Left=int(ob.Left)+int(left),Cost=cp,Sold=sp)
                objec=Stock.objects.all().order_by('Product')
                total_quantity=0
                for datass in objec:
                    total_quantity+=int(datass.Total)
                left_quantity=0
                for datass in objec:
                    left_quantity+=int(datass.Left)
                p=Paginator(objec,8)
                count=0
                for data in objec:
                    count+=1
                page=request.GET.get('page')
                data=p.get_page(page)
                
                start=data.start_index()
                end=data.end_index()
            return render(request,'stock.html',{'data':data,'count':count,'start':start,'end':end,'total_quantity':total_quantity,'Left_quantity':left_quantity})
       
    return render(request,'stock.html',{'data':data,'count':count,'start':start,'end':end,'total_quantity':total_quantity,'Left_quantity':left_quantity})     
#for excel of stock
def stockexcel(request):
    from openpyxl import Workbook
    from openpyxl.worksheet.table import Table
    from openpyxl.worksheet.table import Table, TableStyleInfo
    wb=Workbook()
    ws=wb.active# ws means worksheet
    ws.title="Stock Sheet" #for title
    datas=("Product","Total","Left","Cost Price","Selling Price")
    obj=Stock.objects.all()
    count=1
    for data in obj:
        count+=1
    for row in range(1):
        ws.append(datas)
    
    tab=Table(displayName="StockDetails")
    style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                        showLastColumn=False, showRowStripes=True, showColumnStripes=True)
    tab.tableStyleInfo = style    
    ws.add_table(tab)
    wb.save('stock.xlsx')
    context={
        'message':"Excel file Created Successfully."
    }
    return render(request,'stock.html',context)
#for ordeirng of stock
def stockpd(request):
    objec=Stock.objects.all().order_by('-Product')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_quantity=0
    count=0
    for datass in objec:
        total_quantity+=int(datass.Total)
        count+=1
    left_quantity=0
    for datass in objec:
        left_quantity+=int(datass.Left)
    return render(request,'stock.html',{'data':data,'total_quantity':total_quantity,'Left_quantity':left_quantity,'count':count,'start':start,'end':end})  
def stockpi(request):
    objec=Stock.objects.all().order_by('Product')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_quantity=0
    count=0
    for datass in objec:
        total_quantity+=int(datass.Total)
        count+=1
    left_quantity=0
    for datass in objec:
        left_quantity+=int(datass.Left)
    return render(request,'stock.html',{'data':data,'total_quantity':total_quantity,'Left_quantity':left_quantity,'count':count,'start':start,'end':end})  
def stockqi(request):
    objec=Stock.objects.all().order_by('Total')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    count=0
    total_quantity=0
    for datass in objec:
        total_quantity+=int(datass.Total)
        count+=1
    left_quantity=0
    for datass in objec:
        left_quantity+=int(datass.Left)
    return render(request,'stock.html',{'data':data,'total_quantity':total_quantity,'Left_quantity':left_quantity,'count':count,'start':start,'end':end})  
def stockqd(request):
    objec=Stock.objects.all().order_by('-Total')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_quantity=0
    count=0
    for datass in objec:
        total_quantity+=int(datass.Total)
        count+=1
    left_quantity=0
    for datass in objec:
        left_quantity+=int(datass.Left)
    return render(request,'stock.html',{'data':data,'total_quantity':total_quantity,'Left_quantity':left_quantity,'count':count,'start':start,'end':end})  
def stocklqi(request):
    objec=Stock.objects.all().order_by('Left')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_quantity=0
    count=0
    for datass in objec:
        total_quantity+=int(datass.Total)
        count+=1
    left_quantity=0
    for datass in objec:
        left_quantity+=int(datass.Left)
    return render(request,'stock.html',{'data':data,'total_quantity':total_quantity,'Left_quantity':left_quantity,'count':count,'start':start,'end':end})  
def stocklqd(request):
    objec=Stock.objects.all().order_by('-Left')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_quantity=0
    count=0
    for datass in objec:
        total_quantity+=int(datass.Total)
        count+=1
    left_quantity=0
    for datass in objec:
        left_quantity+=int(datass.Left)
    return render(request,'stock.html',{'data':data,'total_quantity':total_quantity,'Left_quantity':left_quantity,'count':count,'start':start,'end':end})  
def stockcpi(request):
    objec=Stock.objects.all().order_by('Cost')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_quantity=0
    count=0
    for datass in objec:
        total_quantity+=int(datass.Total)
        count+=1
    left_quantity=0
    for datass in objec:
        left_quantity+=int(datass.Left)
    return render(request,'stock.html',{'data':data,'total_quantity':total_quantity,'Left_quantity':left_quantity,'count':count,'start':start,'end':end})  
def stockcpd(request):
    objec=Stock.objects.all().order_by('-Cost')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    total_quantity=0
    start=data.start_index()
    end=data.end_index()
    count=0
    for datass in objec:
        total_quantity+=int(datass.Total)
        count+=1
    left_quantity=0
    for datass in objec:
        left_quantity+=int(datass.Left)
    return render(request,'stock.html',{'data':data,'total_quantity':total_quantity,'Left_quantity':left_quantity,'count':count,'start':start,'end':end})  
def stockspi(request):
    objec=Stock.objects.all().order_by('Sold')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_quantity=0
    count=0
    for datass in objec:
        total_quantity+=int(datass.Total)
        count+=1
    left_quantity=0
    for datass in objec:
        left_quantity+=int(datass.Left)
    return render(request,'stock.html',{'data':data,'total_quantity':total_quantity,'Left_quantity':left_quantity,'count':count,'start':start,'end':end})  
def stockspd(request):
    objec=Stock.objects.all().order_by('-Sold')
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    count=0
    total_quantity=0
    for datass in objec:
        total_quantity+=int(datass.Total)
        count+=1
    left_quantity=0
    for datass in objec:
        left_quantity+=int(datass.Left)
    return render(request,'stock.html',{'data':data,'total_quantity':total_quantity,'Left_quantity':left_quantity,'count':count,'start':start,'end':end})  
def search(request):
    objec=Stock.objects.all().order_by('Product')
   
    p=Paginator(objec,1)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    total_quantity=0
    for datass in objec:
        total_quantity+=int(datass.Total)
    left_quantity=0
    for datass in objec:
        left_quantity+=int(datass.Left)
    if request.method=='POST':
        total_quantity=0
        for datass in objec:
            total_quantity+=int(datass.Total)
        left_quantity=0
        for datass in objec:
            left_quantity+=int(datass.Left)
        text=request.POST['findtext']
        obj=Stock.objects.filter(Product__icontains=text)
        count=0
        for data in obj:
            count+=1
        if len(obj)!=0:
            objec=Stock.objects.filter(Product__icontains=text)

            total_quantity=0
            for datass in objec:
                total_quantity+=int(datass.Total)

            left_quantity=0
            for datass in objec:
                left_quantity+=int(datass.Left)

            p=Paginator(objec,5)
            page=request.GET.get('page')
            data=p.get_page(page)
            context={
                'data':data,
                'total_quantity':total_quantity,
                'Left_quantity':left_quantity,
                'count':count,
                'start':start,
                'end':end
            }
            return render(request,'stock.html',context)
        if len(obj)==0:
            objec=Stock.objects.all()
            return render(request,'stock.html',{'data':data})
    return render(request,'stock.html',{'data':data,'total_quantity':total_quantity,'Left_quantity':left_quantity})
    #
def salesbill(request):
    objec=Salesbill.objects.all()
    count=0
    for dara in objec:
        count+=1
    p=Paginator(objec,8)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'salesbill.html',{'data':data,'count':count,'start':start,'end':end})
#for ordering of salesbill
def ddsb(request):
    objec=Salesbill.objects.all().order_by('-Date')
    count=0
    for data in objec:
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'salesbill.html',{'data':data,'count':count,'start':start,'end':end})
def idsb(request):
    objec=Salesbill.objects.all().order_by('Date')
    count=0
    for data in objec:
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'salesbill.html',{'data':data,'count':count,'start':start,'end':end})
def dcsb(request):
    objec=Salesbill.objects.all().order_by('-Customer_name')
    count=0
    for data in objec:
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'salesbill.html',{'data':data,'count':count,'start':start,'end':end})
def icsb(request):
    objec=Salesbill.objects.all().order_by('Customer_name')
    count=0
    for data in objec:
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'salesbill.html',{'data':data,'count':count,'start':start,'end':end})
def dpsb(request):
    objec=Salesbill.objects.all().order_by('-Paid')
    count=0
    for data in objec:
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'salesbill.html',{'data':data,'count':count,'start':start,'end':end})
def ipsb(request): 
    objec=Salesbill.objects.all().order_by('Paid')
    count=0
    for data in objec:
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'salesbill.html',{'data':data,'count':count,'start':start,'end':end})

#for creating of salesbill
def searchsb(request):
    if request.method=='POST':
        serch=request.POST['findtext']
        objec=Salesbill.objects.filter(Customer_name__icontains=serch)
        count=0
        for data in objec:
            count+=1
        p=Paginator(objec,7)
        page=request.GET.get('page')
        data=p.get_page(page)
        start=data.start_index()
        end=data.end_index()
        return render(request,'salesbill.html',{'data':data,'count':count,'start':start,'end':end})
#for search of purchasebill
def searchpb(request):
    if request.method=='POST':
        serch=request.POST['findtext']
        objec=Purchasebill.objects.filter(Company_name__icontains=serch)
        p=Paginator(objec,7)
        page=request.GET.get('page')
        data=p.get_page(page)
        return render(request,'purchasebill.html',{'data':data})
    return render(request,'purchasebill.html')

def purchasebill(request):
    objec=Purchasebill.objects.all()
    count=0
    for data in objec:
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'purchasebill.html',{'data':data,'count':count,'start':start,'end':end})
#for ordering o
def purchasebilldate(request):
    objec=Purchasebill.objects.all().order_by('-Date')
    count=0
    for data in objec:
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'purchasebill.html',{'data':data,'count':count,'start':start,'end':end})
def purchasebilldated(request):
    objec=Purchasebill.objects.all().order_by('Date')
    count=0
    for data in objec:
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'purchasebill.html',{'data':data,'count':count,'start':start,'end':end})
def purchasebillci(request):
    objec=Purchasebill.objects.all().order_by('Company_name')
    count=0
    for data in objec:
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'purchasebill.html',{'data':data,'count':count,'start':start,'end':end})
def purchasebillcd(request):
    objec=Purchasebill.objects.all().order_by('-Company_name')
    count=0
    for data in objec:
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'purchasebill.html',{'data':data,'count':count,'start':start,'end':end})
def purchasebillp(request):
    objec=Purchasebill.objects.all().order_by('Paid')
    count=0
    for data in objec:
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'purchasebill.html',{'data':data,'count':count,'start':start,'end':end})
def purchasebilld(request):
    objec=Purchasebill.objects.all().order_by('-Paid')
    count=0
    for data in objec:
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'purchasebill.html',{'data':data,'count':count,'start':start,'end':end})
def purchase(request):
    return render(request,'saving.html')
def credit(request):
    count=0
    objec=Credit.objects.all()
    for data in objec:
        count+=1
    total=0.0
    remain=0.0
    for data in objec:
        total=float(data.Total)+total
    for data in objec:
        remain=float(data.Due_left)+remain
    p=Paginator(objec,10)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'credit.html',{'data':data,'total':total,'remain':remain,'count':count,'start':start,'end':end})
#for credit order:
def creditincrease(request,factor):
    objec=Credit.objects.all().order_by(factor)
    total=0.0
    remain=0.0
    count=0
    
    for data in objec:
        total=float(data.Total)+total
        count+=1
    for data in objec:
        remain=float(data.Due_left)+remain
    p=Paginator(objec,8)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'credit.html',{'data':data,'total':total,'remain':remain,'count':count,'start':start,'end':end})
def creditdecrease(request,factors):
    objec=Credit.objects.all().order_by("-"+factors)
    total=0.0
    remain=0.0
    count=0
    for data in objec:
        total=float(data.Total)+total
        count+=1
    for data in objec:
        remain=float(data.Due_left)+remain
    p=Paginator(objec,8)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'credit.html',{'data':data,'total':total,'remain':remain,'count':count,'start':start,'end':end})
def saving(request):
    global length
    length=0
    objec=Saving.objects.all()
    total=0.0
    count=0
    for data in objec:
        tot=data.Amount
        total=round(total+float(tot),2)
        count+=1
    
    if request.method == 'POST':
        date=request.POST['date']
        purpose=request.POST['purpose']
        amount=request.POST['amount']
        obj=Saving.objects.create(Date=date,Bank=purpose,Amount=amount)
        obj.save()
        objec=Saving.objects.all()
        count=0
        for data in objec:
            count+=1
        total=0.0
        for data in objec:
            tot=data.Amount
            total=round(total+float(tot),2)
        p=Paginator(objec,5)
        page=request.GET.get('page')
        data=p.get_page(page)
        lenth=len(data)
        start=data.start_index()
        end=data.end_index()

        return render(request,'saving.html',{'data':data,'total':total,'count':count,'datas':lenth,'start':start,'end':end})
    p=Paginator(objec,3)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()

    return render(request,'saving.html',{'data':data,'total':total,'count':count,'start':start,'end':end})
    # for saving order
def savedd(request):

    objec=Saving.objects.all().order_by('-Date')
    total=0.0
    count=0
    for data in objec:
        tot=data.Amount
        total=round(total+float(tot),2)
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'saving.html',{'data':data,'total':total,'count':count,'start':start,'end':end})
def saveid(request):
    
    objec=Saving.objects.all().order_by('Date')
    total=0.0
    count=0
    for data in objec:
        tot=data.Amount
        total=round(total+float(tot),2)
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'saving.html',{'data':data,'total':total,'count':count,'start':start,'end':end})
def savedf(request):
    objec=Saving.objects.all().order_by('-Bank')
    total=0.0
    count=0
    for data in objec:
        tot=data.Amount
        total=round(total+float(tot),2)
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    lenth=int(len(data))
    return render(request,'saving.html',{'data':data,'total':total,'count':count,'start':start,'end':end})
def savefi(request):
    objec=Saving.objects.all().order_by('Bank')
    total=0.0
    count=0
    for data in objec:
        tot=data.Amount
        total=round(total+float(tot),2)
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'saving.html',{'data':data,'total':total,'count':count,'start':start,'end':end})
def saveda(request):
    objec=Saving.objects.all().order_by('-Amount')
    total=0.0
    count=0
    for data in objec:
        tot=data.Amount
        total=round(total+float(tot),2)
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    lenth=int(len(data))
    start=data.start_index()
    end=data.end_index()
    return render(request,'saving.html',{'data':data,'total':total,'count':count,'start':start,'end':end})
def saveia(request):
    objec=Saving.objects.all().order_by('Amount')
    total=0.0
    count=0
    for data in objec:
        tot=data.Amount
        total=round(total+float(tot),2)
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    lenth=int(len(data))
    start=data.start_index()
    end=data.end_index()
    return render(request,'saving.html',{'data':data,'total':total,'count':count,'start':start,'end':end})
def expense(request):

    objec=Expenses.objects.all()
    total=0.0
    count=0
    for data in objec:
        tot=data.Amount
        count+=1
        total=round(total+float(tot),2)
    p=Paginator(objec,5)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    if request.method == 'POST':
        date=request.POST['date']
        purpose=request.POST['purpose']
        amount=request.POST['amount']
        obj=Expenses.objects.create(Date=date,Purpose=purpose,Amount=amount)
        obj.save()
        objec=Expenses.objects.all()
        total=0.0
        count=0
        for data in objec:
            tot=data.Amount
            total=round(total+float(tot),2)
            count+=1
        p=Paginator(objec,5)
        page=request.GET.get('page')
        data=p.get_page(page)
        start=data.start_index()
        end=data.end_index()
        return render(request,'expense.html',{'data':data,'total':total,'count':count,'start':start,'end':end})

    return render(request,'expense.html',{'data':data,'total':total,'count':count,'start':start,'end':end})
#for expenses
def edd(request):

    objec=Expenses.objects.all().order_by('-Date')
    total=0.0
    count=0
    for data in objec:
        tot=data.Amount
        total=round(total+float(tot),2)
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    
    return render(request,'expense.html',{'data':data,'total':total,'count':count,'start':start,'end':end})
def eid(request):
    
    objec=Expenses.objects.all().order_by('Date')
    total=0.0
    count=0
    for data in objec:
        tot=data.Amount
        total=round(total+float(tot),2)
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'expense.html',{'data':data,'total':total,'count':count,'start':start,'end':end})
def edf(request):
    objec=Expenses.objects.all().order_by('-Purpose')
    total=0.0
    count=0
    for data in objec:
        tot=data.Amount
        total=round(total+float(tot),2)
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'expense.html',{'data':data,'total':total,'count':count,'start':start,'end':end})
def efi(request):
    objec=Expenses.objects.all().order_by('Purpose')
    total=0.0
    count=0
    for data in objec:
        tot=data.Amount
        total=round(total+float(tot),2)
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'expense.html',{'data':data,'total':total,'count':count,'start':start,'end':end})
def eda(request):
    objec=Expenses.objects.all().order_by('-Amount')
    total=0.0
    count=0
    for data in objec:
        tot=data.Amount
        total=round(total+float(tot),2)
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'expense.html',{'data':data,'total':total,'count':count,'start':start,'end':end})
def eia(request):
    objec=Expenses.objects.all().order_by('Amount')
    total=0.0
    count=0
    for data in objec:
        tot=data.Amount
        total=round(total+float(tot),2)
        count+=1
    p=Paginator(objec,7)
    page=request.GET.get('page')
    data=p.get_page(page)
    start=data.start_index()
    end=data.end_index()
    return render(request,'expense.html',{'data':data,'total':total,'count':count,'start':start,'end':end})

def searchsaving(request):
    if request.method=="POST":
        dat=request.POST['findtext']
        factor=request.POST['searchtype']
        if factor=="Date":
            obj=Saving.objects.filter(Date__icontains=dat)
            if len(obj)==0:
                return render(request,'saving.html')
            else:
                total=0.0
                for data in obj:
                    tot=data.Amount
                    total=round(total+float(tot),2)
                p=Paginator(obj,5)
                page=request.GET.get('page')
                data=p.get_page(page)
                return render(request,'saving.html',{'data':data,'total':total})
        if factor=="Bank":
            obj=Saving.objects.filter(Bank__icontains=dat)
            if len(obj)==0:
                return render(request,'saving.html')
            else:
                total=0.0
                for data in obj:
                    tot=data.Amount
                    total=round(total+float(tot),2)
                p=Paginator(obj,5)
                page=request.GET.get('page')
                data=p.get_page(page)
                return render(request,'saving.html',{'data':data,'total':total})



    return render(request,'saving.html')
def searchexpense(request):
    if request.method=="POST":
        dat=request.POST['findtext']
        factor=request.POST['searchtype']
        if factor=="Date":
            obj=Expenses.objects.filter(Date__icontains=dat)
            if len(obj)==0:
                return render(request,'expense.html')
            else:
                total=0.0
                for data in obj:
                    tot=data.Amount
                    total=round(total+float(tot),2)
                p=Paginator(obj,5)
                page=request.GET.get('page')
                data=p.get_page(page)
                return render(request,'expense.html',{'data':data,'total':total})
        if factor=="Purpose":
            obj=Expenses.objects.filter(Purpose__icontains=dat)
            if len(obj)==0:
                return render(request,'expense.html')
            else:
                total=0.0
                for data in obj:
                    tot=data.Amount
                    total=round(total+float(tot),2)
                p=Paginator(obj,5)
                page=request.GET.get('page')
                data=p.get_page(page)
                return render(request,'expense.html',{'data':data,'total':total})



    return render(request,'expense.html')
def transportbill(request):
    return render(request,'transportationbill.html')
def report(request):
    obj=Sales.objects.all()
    p=Paginator(obj,9)
    page=request.GET.get('page')
    data=p.get_page(page)
    return render(request,'report.html',{'sales':"sales",'data':data})
def searchreport(request):
    objec=Sales.objects.all()
    p=Paginator(objec,9)
    page=request.GET.get('page')
    data=p.get_page(page)
    
    if request.method=='POST':
        search=request.POST['searchtype']
        count=request.POST['num']
        start=request.POST['start']
        end=request.POST['end']
        if search=="Sales":
            if len(start)==0 and len(end)==0:
                objec=Sales.objects.all()
                p=Paginator(objec,count)
                
                page=request.GET.get('page')
                data=p.get_page(page)
                return render(request,'report.html',{'data':data,'sales':"Sales"})
            else:
                objec=Sales.objects.filter(Date__range=(start,end))
                p=Paginator(objec,count)
                page=request.GET.get('page')
                data=p.get_page(page)
                return render(request,'report.html',{'data':data,'sales':"Sales"})
                
        if search=="Purchase":
            if len(start)==0 and len(end)==0:
                objec=Purchasebill.objects.all()
                p=Paginator(objec,count)
                page=request.GET.get('page')
                data=p.get_page(page)
                return render(request,'report.html',{'data':data,'purchase':"Purchase"})
            else:
                objec=Purchasebill.objects.filter(Date__range=(start,end))
                p=Paginator(objec,count)
                page=request.GET.get('page')
                data=p.get_page(page)
                return render(request,'report.html',{'data':data,'purchase':"Purchase"})

        if search=="Saving":
            if len(start)==0 and len(end)==0:
                objec=Saving.objects.all()
                p=Paginator(objec,count)
                page=request.GET.get('page')
                data=p.get_page(page)
                return render(request,'report.html',{'data':data,'save':"Saving"})
            else:
                objec=Saving.objects.filter(Date__range=(start,end))
                p=Paginator(objec,count)
                page=request.GET.get('page')
                data=p.get_page(page)
                return render(request,'report.html',{'data':data,'save':"Saving"})

        if search=="Expenses":
            if len(start)==0 and len(end)==0:
                objec=Expenses.objects.all()
                p=Paginator(objec,count)
                page=request.GET.get('page')
                data=p.get_page(page)
                return render(request,'report.html',{'data':data,'expense':"Expense"})
            else:
                objec=Expenses.objects.filter(Date__range=(start,end))
                p=Paginator(objec,count)
                page=request.GET.get('page')
                data=p.get_page(page)
                return render(request,'report.html',{'data':data,'expense':"Expense"})

        if search=="Credit":
            if len(start)==0 and len(end)==0:

                objec=Credit.objects.all()
                p=Paginator(objec,count)
                page=request.GET.get('page')
                data=p.get_page(page)
                return render(request,'report.html',{'data':data,'credit':"Credit"})
            else:
                objec=Credit.objects.filter(Date__range=(start,end))
                p=Paginator(objec,count)
                page=request.GET.get('page')
                data=p.get_page(page)
                return render(request,'report.html',{'data':data,'credit':"Credit"})


    return render(request,'report.html',{'data':data,'sales':"Sales"})
def setting(request):
    return render(request,'setting.html')
def update(request,obj):
    objec=Credit.objects.filter(id=obj)
    if request.method=='POST':
        amnt=request.POST['newamnt']
        for data in objec:
            paid=data.Paid
        for data in objec:
            remain=data.Due_left
        for data in objec:
            date=data.Date
        for data in objec:
            name=data.Customer_name     
        for data in objec:
            add=data.Customer_address  
        for data in objec:
            phon=data.Customer_phone  
        for data in objec:
            pro=data.Product
        for data in objec:
            quan=data.Quantity
        for data in objec:
            rate=data.Rate
        for data in objec:
            tots=data.Total   
          
      
        objec.update(Paid=int(paid)+int(amnt),Due_left=int(remain)-int(amnt))

        #for updating on sales
        sales_object=Sales.objects.filter(Date=date,Customer_name=name,Customer_address=add,Customer_phone=phon,Product=pro,Quantity=quan,Rate=rate,Total=tots)
        sales_object.update(Paid=int(paid)+int(amnt),Due_left=int(remain)-int(amnt))

        objec=Credit.objects.filter(id=obj)
        return render(request,'new.html',{'objec':objec})
    return render(request,'new.html',{'objec':objec})
def searchcredit(request):
    if request.method=='POST':
        date=request.POST['findtext']
        factor=request.POST['searchtype']
        if factor=="Customer Name":
            objec=Credit.objects.filter(Customer_name__icontains=date)
            total=0.0
            remain=0.0
            for data in objec:
                total=float(data.Total)+total
            for data in objec:
                remain=float(data.Due_left)+remain
            p=Paginator(objec,5)
            page=request.GET.get('page')
            data=p.get_page(page)
            return render(request,'credit.html',{'data':data,'total':total,'remain':remain})
            #for total credit and total remain 
        if factor=="Product":
            objec=Credit.objects.filter(Product__icontains=date)
            total=0.0
            remain=0.0
            for data in objec:
                total=float(data.Total)+total
            for data in objec:
                remain=float(data.Due_left)+remain
            p=Paginator(objec,5)
            page=request.GET.get('page')
            data=p.get_page(page)
            return render(request,'credit.html',{'data':data,'total':total,'remain':remain})
        if factor=="Date":
            objec=Credit.objects.filter(Date__icontains=date)
            total=0.0
            remain=0.0
            for data in objec:
                total=float(data.Total)+total
            for data in objec:
                remain=float(data.Due_left)+remain
            p=Paginator(objec,5)
            page=request.GET.get('page')
            data=p.get_page(page)
            return render(request,'credit.html',{'data':data,'total':total,'remain':remain})
       
        return render(request,'credit.html',{'data':data,})


global date,cname,cadd,cphone,amnt
def billtemplate(request):
    global date,cname,cadd,cphone,amnt
    if request.method=='POST':
        date=request.POST['date']
        cname=request.POST['cname']
        cadd=request.POST['caddress']
        cphone=request.POST['cphone']
        amnt=request.POST['paid']
        obj=Salesbill.objects.create(Date=date,Customer_name=cname,Customer_phone=cphone,Customer_address=cadd,Paid=amnt)
        obj.save()
        objec=Salesbill.objects.filter(Date=date,Customer_name=cname,Customer_phone=cphone,Customer_address=cadd,Paid=amnt)
        obj_stock=Stock.objects.all().order_by('Product')
        return render(request,'billtemplate.html',{'objec':objec,'omg':obj_stock,'date':date,'cname':cname,'cadd':cadd,'cphone':cphone,'amnt':amnt})    
    objec=Salesbill.objects.all()
    return render(request,'billtemplate.html',{'objec':objec})

def billtemplates(request):
    global date,cname,cadd,cphone,amnt
    if request.method == 'POST':
        product=request.POST['product']
        quantity=request.POST['quantity']
        rate= request.POST['rate']
        discount=request.POST['discount']

        total =round( (float(quantity) * float(rate)),2)
        dis=round(float(float(discount)/100)*total,2)
        total = (float(quantity) * float(rate))-dis

        check_stock =Stock.objects.filter(Product=product)
        if len(check_stock)==0:
            message ="Not Available in stock..."
            return render(request,'billtemplates.html',{'message':message})
            
        for data in check_stock:
            quantity_left_is = data.Left
        if int(quantity)>int(quantity_left_is):
            message ="Out of Stock."
            return render(request,'billtemplates.html',{'message':message})
            
        else:
            obj=Salesbillitems.objects.create(Date=date,Customer_name=cname,Customer_phone=cphone,Customer_address=cadd,Product=product,Quantity=quantity,Rate=rate,Discount=dis,Total=total)
            obj.save()
            # for decreasing the stock.
            stock_obj = Stock.objects.filter(Product=product)
            for data in stock_obj:
                quantity_left_is = data.Left
            new_quantity=int(quantity_left_is)-int(quantity)
            stock_obj.update(Left=new_quantity)

            objec=Salesbillitems.objects.filter(Date=date,Customer_name=cname,Customer_phone=cphone,Customer_address=cadd)
        # for total amount:
        total = 0.0
        for data in objec:
            total = round(total + float(data.Total),2)
        # for discount amount:
        discount = 0.0
        for data in objec:
            discount = round(discount + float(data.Discount),2)
        # for due left
        due_left = total -float(amnt)
        p=Paginator(objec,4)
        page=request.GET.get('page')
        data=p.get_page(page)
        #for all produccts
        obj_stock=Stock.objects.all().order_by('Product')
        return render(request,'billtemplates.html',{'data':data,'total':total,'omg':obj_stock,'due_left':due_left,'discount':discount,'cname':cname,'date':date,'cadd':cadd,'cphone':cphone,'amnt':amnt})
    objec=Salesbillitems.objects.filter(Date=date,Customer_name=cname,Customer_phone=cphone,Customer_address=cadd)
    # for total amount:
    total = 0.0
    for data in objec:
        total = round(total + float(data.Total),2)
    # for discount amount:
    discount = 0.0
    for data in objec:
        discount = round(discount + float(data.Discount),2)
    # for due left
    due_left = total - float(amnt)
    p=Paginator(objec,4)
    page=request.GET.get('page')
    data=p.get_page(page)
    return render(request,'billtemplates.html',{'data':data,'total':total,'due_left':due_left,'discount':discount,'cname':cname,'date':date,'cadd':cadd,'cphone':cphone,'amnt':amnt})
  
def showbilltemplates(request,idd):
    objec=Salesbill.objects.filter(id=idd)
    for data in objec:
        date=data.Date
        cname=data.Customer_name
        cadd=data.Customer_address
        cphone=data.Customer_phone
        amnt=data.Paid
    obje=Salesbillitems.objects.filter(Date=date,Customer_name=cname,Customer_phone=cphone,Customer_address=cadd,)
    total = 0.0
    for data in obje:
        total = round(total + float(data.Total),2)
    # for discount amount:
    discount = 0.0
    for data in obje:
        discount = round(discount + float(data.Discount),2)
    # for due left
    due_left = total - float(amnt)
    p=Paginator(obje,2)
    page=request.GET.get('page')
    data=p.get_page(page)
    
    return render(request,'showbill.html',{'date':date,'total':total,'discount':discount,'due_left':due_left,'cname':cname,'cadd':cadd,'cphone':cphone,'amnt':amnt,'data':data})    
    

def editbilltemplates(request,idd):
    objec=Salesbill.objects.filter(id=idd)
    for data in objec:
        date=data.Date
        cname=data.Customer_name
        cadd=data.Customer_address
        cphone=data.Customer_phone
        amnt=data.Paid
    obje=Salesbillitems.objects.filter(Date=date,Customer_name=cname,Customer_phone=cphone,Customer_address=cadd,)
    total = 0.0
    for data in obje:
        total = round(total + float(data.Total),2)
    # for discount amount:
    discount = 0.0
    for data in obje:
        discount = round(discount + float(data.Discount),2)
    # for due left
    due_left = total - float(amnt)
    p=Paginator(obje,2)
    page=request.GET.get('page')
    data=p.get_page(page)
    
    return render(request,'editbill.html',{'date':date,'id':idd,'total':total,'discount':discount,'due_left':due_left,'cname':cname,'cadd':cadd,'cphone':cphone,'amnt':amnt,'data':data})    
def updatebill(request,idd):
    objec=Salesbill.objects.filter(id=idd)
    new_amount=request.POST['newamnt']
    for data in objec:
        date=data.Date
        cname=data.Customer_name
        cadd=data.Customer_address
        cphone=data.Customer_phone
        amnt=data.Paid
    obje=Salesbillitems.objects.filter(Date=date,Customer_name=cname,Customer_phone=cphone,Customer_address=cadd,)
    total = 0.0
    for data in obje:
        total = round(total + float(data.Total),2)
    for data in objec:
        paid=data.Paid
    fianal = round(float(new_amount)+float(paid),2)
    objec.update(Paid=fianal)
    # for discount amount:
    discount = 0.0
    for data in obje:
        discount = round(discount + float(data.Discount),2)
    # for due left
    due_left = total - discount -float(fianal)
    p=Paginator(obje,2)
    page=request.GET.get('page')
    data=p.get_page(page)
    return render(request,'editbill.html',{'date':date,'id':idd,'total':total,'discount':discount,'due_left':due_left,'cname':cname,'cadd':cadd,'cphone':cphone,'amnt':fianal,'data':data}) 

def purchasebilltemplate(request):
    global pdate,pcname,pcadd,pcphone,pamnt,pvat,ppan
    if request.method=='POST':
        pdate=request.POST['date']
        pcname=request.POST['cname']
        pcadd=request.POST['caddress']
        pcphone=request.POST['cphone']
        pamnt=request.POST['paid']
        pvat=request.POST['vat']
        ppan=request.POST['pan']
        obj=Purchasebill.objects.create(Date=pdate,Company_name=pcname,Vat=pvat,Pan=ppan,Customer_phone=pcphone,Customer_address=pcadd,Paid=pamnt)
        obj.save()
        objec=Purchasebill.objects.filter(Date=pdate,Company_name=pcname,Vat=pvat,Pan=ppan,Customer_phone=pcphone,Customer_address=pcadd,Paid=pamnt)
        p=Paginator(objec,3)
        page=request.GET.get('page')
        data=p.get_page(page)
        stk=Stock.objects.all()

        return render(request,'purchasebilltemplate.html',{'objec':data,'obj':stk,'vat':pvat,'date':pdate,'cname':pcname,'pan':ppan,'cadd':pcadd,'cphone':pcphone,'amnt':pamnt})    
    objec=Salesbill.objects.all()
    return render(request,'purchasebilltemplate.html',{'objec':objec})

def viewbill(request,idd):
    objec=Purchasebill.objects.filter(id=idd)
    for data in objec:
        pdate=data.Date
        pcname=data.Company_name
        pcadd=data.Customer_address
        pcphone=data.Customer_phone
        pamnt=data.Paid
        pvat=data.Vat
        ppan=data.Pan
    obje=Purchasebillitems.objects.filter(Date=pdate,Company_name=pcname,Customer_phone=pcphone,Customer_address=pcadd)
    # for total amount:
    total = 0.0
    for data in obje:
        total = round(total + float(data.Total),2)
    # for discount amount:
    discount = 0.0
    for data in obje:
        discount = round(discount + float(data.Discount),2)
    # for due left
    
    ntotal=total+((float(pvat)/100)*total)
    due_left = round(ntotal -float(pamnt),2)
    p=Paginator(obje,3)
    page=request.GET.get('page')
    data=p.get_page(page)
    print(data)
    return render(request,'showbill.html',{'date':pdate,'ntotal':ntotal,'total':total,'discount':discount,'vat':pvat,'pan':ppan,'due_left':due_left,'cname':pcname,'cadd':pcadd,'cphone':pcphone,'amnt':pamnt,'data':data})    
    
def purchasebilltemplates(request):

    global pdate,pcname,pcadd,pcphone,pamnt,pvat,ppan
    if request.method == 'POST':
        product=request.POST['product']
        quantity=request.POST['quantity']
        rate= request.POST['rate']
        discount=request.POST['discount']
        total =round( (float(quantity) * float(rate)),2)
        dis=round(float(float(discount)/100)*total,2)
        total = (float(quantity) * float(rate))-dis
        obj=Purchasebillitems.objects.create(Date=pdate,Company_name=pcname,Customer_phone=pcphone,Customer_address=pcadd,Product=product,Quantity=quantity,Rate=rate,Discount=dis,Total=total)
        obj.save()
        # for maintaing the stock.
        stock_obj = Stock.objects.filter(Product=product)
        if len(stock_obj)==0:
            obj=Stock.objects.create(Product=product,Total=quantity,Left=quantity,Cost=rate,Sold=0)
            obj.save()
        elif len(stock_obj)!=0:
            for data in stock_obj:
                quantity_left_is = data.Left
                total_quantity=data.Total
                
            new_quantity=int(quantity_left_is)+int(quantity)
            tot_quantity=int(total_quantity)+int(quantity)
            stock_obj.update(Left=new_quantity,Total=tot_quantity,Cost=rate)

        objec=Purchasebillitems.objects.filter(Date=pdate,Company_name=pcname,Customer_phone=pcphone,Customer_address=pcadd)
        # for total amount:
        total = 0.0
        for data in objec:
            total = round(total + float(data.Total),2)
        # for discount amount:
        discount = 0.0
        for data in objec:
            discount = round(discount + float(data.Discount),2)
        # for due left
        
        ntotal=round(total+((float(pvat)/100)*total),2)
        due_left = round(ntotal -float(pamnt),2)
        p=Paginator(objec,2)
        page=request.GET.get('page')
        data=p.get_page(page)
        obj_stock=Stock.objects.all()
        return render(request,'purchasebilltemplate.html',{'data':data,'obj':obj_stock,'total':total,'vat':pvat,'pan':ppan,'ntotal':ntotal,'due_left':due_left,'discount':discount,'cname':pcname,'date':pdate,'cadd':pcadd,'cphone':pcphone,'amnt':pamnt})
    objec=Purchasebillitems.objects.filter(Date=pdate,Company_name=pcname,Customer_phone=pcphone,Customer_address=pcadd)
    # for total amount:
    total = 0.0
    for data in objec:
        total = round(total + float(data.Total),2)
    # for discount amount:
    discount = 0.0
    for data in objec:
        discount = round(discount + float(data.Discount),2)
    # for due left
    due_left = round(total - discount -float(pamnt),2)
    p=Paginator(objec,4)
    page=request.GET.get('page')
    data=p.get_page(page)
    obj_stock=Stock.objects.all()
    return render(request,'purchasebilltemplate.html',{'data':data,'obj':obj_stock,'total':total,'due_left':due_left,'discount':discount})

def editbillstemplates(request,idd):

    objec=Purchasebill.objects.filter(id=idd)
    for data in objec:
        date=data.Date
        cname=data.Company_name
        cadd=data.Customer_address
        cphone=data.Customer_phone
        amnt=data.Paid
        ppan=data.Pan
    obje=Purchasebillitems.objects.filter(Date=date,Company_name=cname,Customer_phone=cphone,Customer_address=cadd,)
    total = 0.0
    for data in obje:
        total = round(total + float(data.Total),2)
    # for discount amount:
    discount = 0.0
    for data in obje:
        discount = round(discount + float(data.Discount),2)
    # for due left
    due_left = total - discount -float(amnt)
    p=Paginator(obje,2)
    page=request.GET.get('page')
    data=p.get_page(page)
   
    return render(request,'editpurchasebill.html',{'date':date,'id':idd,'pan':ppan,'total':total,'discount':discount,'due_left':due_left,'cname':cname,'cadd':cadd,'cphone':cphone,'amnt':amnt,'data':data})   

def updatepbill(request,idd):
    objec=Purchasebill.objects.filter(id=idd)
    new_amount=request.POST['newamnt']
    for data in objec:
        date=data.Date
        cname=data.Company_name
        cadd=data.Customer_address
        cphone=data.Customer_phone
        amnt=data.Paid
    obje=Purchasebillitems.objects.filter(Date=date,Company_name=cname,Customer_phone=cphone,Customer_address=cadd,)
    total = 0.0
    for data in obje:
        total = round(total + float(data.Total),2)
    for data in objec:
        paid=data.Paid
    fianal = round(float(new_amount)+float(paid),2)
    objec.update(Paid=fianal)
    # for discount amount:
    discount = 0.0
    for data in obje:
        discount = round(discount + float(data.Discount),2)
    # for due left
    due_left = total - discount -float(fianal)
    p=Paginator(obje,4)
    page=request.GET.get('page')
    data=p.get_page(page)
    print(data)
    return render(request,'editpurchasebill.html',{'date':date,'id':idd,'total':total,'discount':discount,'due_left':due_left,'cname':cname,'cadd':cadd,'cphone':cphone,'amnt':fianal,'data':data}) 


#for pagenot
def pagenot(request,text):
    return HttpResponse("404 Error Page NOt found")

