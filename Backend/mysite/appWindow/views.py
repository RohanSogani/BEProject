from django.shortcuts import render
from django.core.urlresolvers import reverse
from appWindow.models import apkUpload
from appWindow.forms import apkUploadForm
from django.http import HttpResponseRedirect, HttpResponse
from . import runAndrowarn
import pymongo, re
import androidMapping as aMap
import manifest



'''
#for getting list of all reviewed apps
def apps(request):
    return render(request,'apps.html',{'apps':Apps.objects.all()})

def app(request,app_id=1):
    return render(request,'app.html',{'app':Apps.objects.get(id=app_id)})

'''


# logi for uploading files
def upload(request):
    # print "Inside upload"

    #logic for recently scanned apps
    client = pymongo.MongoClient()
    db = client['xCalDB']
    collection = db['AppReports']

    if request.method == 'GET':
        name = request.GET.get('application_name', None)
        if name is not None:
            return HttpResponseRedirect(reverse('showReport', args=[name]))

    apkName = ''
    if request.method == 'POST':
        form = apkUploadForm(request.POST, request.FILES)

        if form.is_valid():
            apk = apkUpload(docfile=request.FILES['docfile'])
            apkName = request.FILES['docfile']
            # print apkName

            apk.save()
            itm = collection.find_one({"apk_file.file_name": apkName.name})

            if itm is None:
                runAndrowarn.runAW(apkName.name)

            return HttpResponseRedirect(reverse('showReport', args=[apkName.name]))

    else:
        form = apkUpload()
        apkName = ''



    recentdata = collection.find({}).sort("_id",-1).limit(5)
    mostsearched = collection.find({}).sort("search_count",-1).limit(5)

    context = {
        'form': form,
        'name': apkName,
        'recentdata':recentdata,
        'mostsearched':mostsearched,
    }
    return render(request, "upload.html", context)


# Display static analysis report of uploaded apk
def showReport(request, file_name):
    # print 'Inside showReport()'
    client = pymongo.MongoClient()
    db = client['xCalDB']
    collection = db['AppReports']

    data = collection.find_one({"apk_file.file_name": file_name})
    print 'going_in'
    print data
    
    # Increment search_count of apk in db
    data['search_count'] += 1 
    key = { '_id' : data['_id'] }
    collection.replace_one(key, data)


    if data.get('permission_levels',None) == None:
        manifest.getManifest('/home/nishad/BE_Project/bitbucket/xcalibur/Backend/mysite/media/apks/' + file_name)
        donut_dict = aMap.parseTxt('/home/nishad/BE_Project/bitbucket/xcalibur/Backend/mysite/appWindow/AndroidManifest.xml')
        donut_list = []
        donut_list.append(donut_dict['signature|System'])
        donut_list.append(donut_dict['system'])
        donut_list.append(donut_dict['development'])
        donut_list.append(donut_dict['normal'])
        donut_list.append(donut_dict['dangerous'])
        donut_list.append(donut_dict['signature'])
        data['permission_levels'] = donut_list
        key = { '_id' : data['_id'] }
        collection.replace_one(key, data)
    else:
        donut_list = data['permission_levels']

    print donut_list


    print 'out_of_parse'

    context = {
        'data': data,
        'donut_list': donut_list
    }

    return render(request, "report.html", context)


# Search for an apk which is previously analysed
def searchReport(request):
    client = pymongo.MongoClient()
    db = client['xCalDB']
    collection = db['AppReports']

    if request.method == 'GET':
        name = request.GET.get('application_name','')
        # Search for substring using regex ( case insensititve )
        regexString = '.*' + name + '.*'

        data = collection.find_one({ 'apk_file.file_name' : re.compile(regexString,re.IGNORECASE) })  

        # Change name to actual name of the apk that's found

        if data is not None:
            name = data['apk_file']['file_name'][0]
            # str() needed for converting name from unicode to ascii to work with Django
            return HttpResponseRedirect(reverse('showReport',args=[str(name)]))


    context = {
        'data':data,
    }

    return render(request,"searchReport.html",context)


def invalidApp(request):
    return render(request, "invalidApp.html", {})


# generates list of all analysed apks
def allReports(request):
    client = pymongo.MongoClient()
    db = client['xCalDB']
    collection = db['AppReports']

    if request.method == 'GET':
        name = request.GET.get('application_name', None)
        if name is not None:
            return HttpResponseRedirect(reverse('showReport', args=[name]))

    data = collection.find()  # returns a cursor to the collection

    count_dict = {}
    count_dict['sigOrSys'] = 0
    count_dict['system'] = 0
    count_dict['development'] = 0
    count_dict['normal'] = 0
    count_dict['dangerous'] = 0
    count_dict['signature'] = 0

    for itm in data:
        count_dict['sigOrSys'] += len(itm['permission_levels'][0])
        count_dict['system'] += len(itm['permission_levels'][1])
        count_dict['development'] += len(itm['permission_levels'][2])
        count_dict['normal'] += len(itm['permission_levels'][3])
        count_dict['dangerous'] += len(itm['permission_levels'][4])
        count_dict['signature'] += len(itm['permission_levels'][5]) 

    data = collection.find()  # returns a cursor to the collection

    context = {
        'data': data,
        'count_dict' : count_dict
    }

    return render(request, "allReports.html", context)

def deleteReports(request):
    client = pymongo.MongoClient()
    db = client['xCalDB']
    collection = db['AppReports']
    collection.delete_many({})
    return HttpResponse("deleted all reports in DB")


def index(request):
    return render(request,"index.html",{})

def appwindow(request):
    return render(request,"appwindow.html",{})

def hacksense(request):
    return render(request,"hacksense.html",{})

def intellisight(request):
    return render(request,"intellisight.html",{})

def grouppermissions(request):
    return render(request,"grouppermissions.html",{})

def compare(request):
    client = pymongo.MongoClient()
    db = client['xCalDB']
    collection = db['AppReports']

    if request.method == 'POST':
        print 'in post'
        apkName1 = request.POST['apkname1']
        apkName2 = request.POST['apkname2']


        apk1 = collection.find_one({"apk_file.file_name": apkName1})
        print 'going_in'


        if apk1.get('permission_levels',None) == None:
            manifest.getManifest('/home/nishad/BE_Project/bitbucket/xcalibur/Backend/mysite/media/apks/' + file_name)
            donut_dict = aMap.parseTxt('/home/nishad/BE_Project/bitbucket/xcalibur/Backend/mysite/appWindow/AndroidManifest.xml')
            donut_list = []
            donut_list.append(donut_dict['signature|System'])
            donut_list.append(donut_dict['system'])
            donut_list.append(donut_dict['development'])
            donut_list.append(donut_dict['normal'])
            donut_list.append(donut_dict['dangerous'])
            donut_list.append(donut_dict['signature'])
            apk1['permission_levels'] = donut_list
            key = { '_id' : apk1['_id'] }
            collection.replace_one(key, apk1)
        else:
            donut_list1 = apk1['permission_levels']


        #####################

        apk2 = collection.find_one({"apk_file.file_name": apkName2})
        print 'going_in'
    


        if apk2.get('permission_levels',None) == None:
            manifest.getManifest('/home/nishad/BE_Project/bitbucket/xcalibur/Backend/mysite/media/apks/' + file_name)
            donut_dict = aMap.parseTxt('/home/nishad/BE_Project/bitbucket/xcalibur/Backend/mysite/appWindow/AndroidManifest.xml')
            donut_list = []
            donut_list.append(donut_dict['signature|System'])
            donut_list.append(donut_dict['system'])
            donut_list.append(donut_dict['development'])
            donut_list.append(donut_dict['normal'])
            donut_list.append(donut_dict['dangerous'])
            donut_list.append(donut_dict['signature'])
            apk2['permission_levels'] = donut_list
            key = { '_id' : apk2['_id'] }
            collection.replace_one(key, apk2)
        else:
            donut_list2 = apk2['permission_levels']




        context = {
            'apk1': apk1,
            'donut_list1': donut_list1,
            'apk2': apk2,
            'donut_list2': donut_list2,
        }

        return render(request, "finalComparison.html", context)        
    else:
        print 'out of post'
        data1 = collection.find()  # returns a cursor to the collection
        data2 = collection.find()
        
        context = {
            'data1': data1,
            'data2': data2,
        }

        return render(request,"compare.html",context)

def team(request):
    return render(request,"team.html",{})

def finalComparison(request):
    return render(request,"finalComparison.html",{})