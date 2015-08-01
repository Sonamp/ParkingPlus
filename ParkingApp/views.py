from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse, Http404
from ParkingApp.models import FloorPlan, CarEntryExit
import datetime

# Create your views here.
    
# car entry form
class CarEntryForm(forms.Form):
    carNo = forms.CharField(label ='Enter Car No ', max_length=10)
    floorNo = forms.IntegerField(label = "Enter parking floor no ")
    timeEntered = forms.DateTimeField(initial = datetime.datetime.now().replace(microsecond = 0), label= "Car entry date time ",  widget=forms.TextInput(attrs={'readonly':'readonly'}))   # default value is the current date time
    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            value = int(self.cleaned_data.get('floorNo'))
        except:
            pass
        else:
            avlParking = FloorPlan.objects.all()
            floors = [x.floorNo for x in avlParking]
            if value not in floors:
                raise forms.ValidationError(u'%s is not a valid floor no.' % value)
            else:
                floor = [x for x in avlParking if x.floorNo == value]
                if(floor[0].availableParking == 0):
                    raise forms.ValidationError(u'Parking is full for floor %s' %value)
        return cleaned_data        
        
carEntry_form = CarEntryForm(auto_id = False)

# car search form, search the entered car with car no and show the time exit in the read only field set to the current time
class CarSearchForm(forms.Form):
    carNo = forms.CharField(label ='Enter Car No ')
    timeExit = forms.DateTimeField(initial = datetime.datetime.now().replace(microsecond = 0), label= "Car exit date time ",  widget=forms.TextInput(attrs={'readonly':'readonly'}))    
    def clean(self):
        clean_data = self.cleaned_data
        if(clean_data.get('carNo')):
            car = CarEntryExit.objects.filter(carNo = clean_data.get('carNo'))
            if not car:
                raise forms.ValidationError(u'%s is not exist in the parking' %clean_data.get('carNo'))
        return clean_data    
        
carSearch_form = CarSearchForm(auto_id = False)

# report form, to generate the car entry exit report between entered from and to date.
class ReportForm(forms.Form):
    fromDate = forms.DateField(label ='From date ')
    toDate = forms.DateField(label = 'To date ')  
    
report_form = ReportForm(auto_id = False)



def home(request):
    print 'home request'    
    avlParking = FloorPlan.objects.all()
    carEntry_form.fields["timeEntered"].initial = datetime.datetime.now().replace(microsecond = 0)
    
    return render(
        request,
        'ParkingApp/home.html',
        {
            'parkings':avlParking,
            'form':carEntry_form,
        }
    )
    
# validate and save the car entry data if it is valid    
def carentry(request):
    c = CarEntryExit()
    form = CarEntryForm(request.POST)
    if form.is_valid():
        c.carNo = request.POST['carNo']
        c.floorNo = request.POST['floorNo']
        c.timeEntered = request.POST['timeEntered']
        c.save()
        print c.floorNo
        floor = FloorPlan.objects.filter(floorNo = c.floorNo)
        if floor:
            print floor[0]
            floor[0].availableParking = floor[0].availableParking - 1
            floor[0].save()
        return redirect('home')
    else:
        avlParking = FloorPlan.objects.all()
        return render(request,'ParkingApp/home.html',{'parkings':avlParking, 'form':form})
    


def carsearch(request):
    carSearch_form.fields['timeExit'].initial = datetime.datetime.now().replace(microsecond = 0)
    return render(
        request,
        'ParkingApp/exit.html',
        {
            'form':carSearch_form
        }
    )
    
def report(request):
    return render(
        request,
        'ParkingApp/report.html',
        {
            'reportform': report_form
        }
    )
# calculate parking fee for the time the car is parked    
def calculateFee(tmDiff):
    try:
        d = divmod(tmDiff, 86400)     # days
        h = divmod(d[1],3600)  # hours
        m = divmod(h[1],60)  # minutes
        #s = m[1]  # seconds
        fee = 0    
        if d[0]>0 : #if car is parked for more than one day then fee charged even if it is exceeding 1 min to next day  $20 /day
            fee += d[0]*20
            if h[0]>0 or m[0] >0:
                fee += 20
        elif h[0]>0 and h[0]<6 : # if car is parked from 0-6 hours the fee is $3/hour
            fee += h[0]*3
        elif h[0] > 6 or h[0] == 6 and m[0] > 0: # car is parked for more than 6 hours, fee is $20/day
            fee += 20  
        elif h[0] == 6 and m[0] == 0:
            fee += h[0]*3  
        if d[0]==0 and h[0]<6 and m[0]>0: # if car is parked for extra mins to hour the fee is $3 for exceeding mins
            fee += 3        
        return fee 
    except IndexError:
        print "Error in calculating fee."
   


def carexit(request):
    form = CarSearchForm(request.POST)
    if(form.is_valid()):
        c = None
    #search car with car no which is entered but time not exited
        car = CarEntryExit.objects.filter(carNo = request.POST['carNo'], timeExit = None)    
        if car:
            try:
                caronexit = car[0]
                caronexit.timeExit = request.POST['timeExit']
                caronexit.save()     
            except CarEntryExit.DoesNotExist:
                raise Http404("Search failed..No car exist!!")    
            caraftersave = CarEntryExit.objects.filter(carNo = request.POST['carNo'], timeEntered = caronexit.timeEntered)# same the car exit time
            if caraftersave: 
                try:                
                    timeDiff = caraftersave[0].timeExit - caraftersave[0].timeEntered # get the exit and entry time difference
                    caraftersave[0].feePaid = calculateFee(timeDiff.total_seconds())   # calculate fee
                    caraftersave[0].save() #save the calculated fee
                    c = caraftersave[0]              
                except CarEntryExit.DoesNotExist:
                    raise Http404("Search failed..No car exist!!")  
                floor = FloorPlan.objects.filter(floorNo = caraftersave[0].floorNo) #add the  empty parking lot to floor
                if floor:
                        floor[0].availableParking = floor[0].availableParking + 1
                        floor[0].save()
        return render(request, 'ParkingApp/exit.html', {'form':carSearch_form, 'car' : c, 'return': 'yes'})
    return render(request, 'ParkingApp/exit.html', {'form': form})
#generate the car entry exit report in csv format
def getreport(request):    
    import csv
    from django.utils.encoding import smart_str    
    response = HttpResponse(content_type='text/csv')
    form = ReportForm(request.POST)
    if form.is_valid():
        date = request.POST['fromDate'].split('-') 
        fromDate = datetime.datetime(int(date[0]), int(date[1]),int(date[2])) # format the from date (eg: 2015-03-10 00:00:00)
        date = request.POST['toDate'].split('-')
        toDate = datetime.datetime(int(date[0]), int(date[1]),int(date[2]),23,59,59) # format the to date (eg: 2015-03-15 23:59:59)
        car = CarEntryExit.objects.filter(timeEntered__gt = fromDate, timeExit__lt = toDate) #filter car data based on date
        if car: 
            response['Content-Disposition'] = 'attachment; filename=CarEntryExitReport.csv'
            writer = csv.writer(response, csv.excel)
            response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
            #write header
            writer.writerow([ 
                smart_str(u"Car No"),
                smart_str(u"Floor No"),
                smart_str(u"Entry DateTime"),
                smart_str(u"Exit DateTime"),
                smart_str(u"Fee Paid"),
            ])
            #write car data
            for obj in car:
                writer.writerow([
                    smart_str(obj.carNo),
                    smart_str(obj.floorNo),
                    smart_str(obj.timeEntered),
                    smart_str(obj.timeExit),
                    smart_str(obj.feePaid),
                ])
        return response
    return render(request,'ParkingApp/report.html',{'reportform':form})
        


    
