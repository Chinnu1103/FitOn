from django.shortcuts import render, redirect
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
from asgiref.sync import sync_to_async
import asyncio
import datetime
import pandas as pd
from aws_conf import get_dynamodb_resource

dataTypes = {
    "heart_rate": "com.google.heart_rate.bpm",
    "resting_heart_rate": "com.google.heart_rate.bpm",
    "steps": "com.google.step_count.delta",
    "sleep": "com.google.sleep.segment",
    "oxygen": "com.google.oxygen_saturation",
    "activity": "com.google.activity.segment"
}

df = pd.read_csv('google_fit_activity_types.csv')

#function to convert miliseconds to Day
def parse_millis(millis):
    return datetime.datetime.fromtimestamp(int(millis) / 1000).strftime("%b %d, %I %p")

def list_metrics(request):
    return render(request, 'metrics/metric_list.html')

def steps_barplot(data):
    # Your steps data
    print("inside steps function\n")
    steps_data=[]
    for record in data['bucket']:
        if len(record['dataset'][0]['point'])==0:
            continue
        else:
            d={}
            d['start']=parse_millis(record['startTimeMillis'])
            d['end']=parse_millis(record['endTimeMillis'])
            d['count']=record['dataset'][0]['point'][0]['value'][0]['intVal']
            steps_data.append(d)

    # Pass the plot path to the template
    context = {'steps_data_json': steps_data}
    return context

def heartrate_plot(data):
    print("inside heart function\n")
    heart_data=[]
    for record in data['bucket']:
        if len(record['dataset'][0]['point'])==0:
            continue
        else:
            print(record['dataset'][0]['point'][0]['value'])
            d={}
            d['start']=parse_millis(record['startTimeMillis'])
            d['end']=parse_millis(record['endTimeMillis'])
            d['count']=float(record['dataset'][0]['point'][0]['value'][0]['fpVal'])
            d['min']=int(record['dataset'][0]['point'][0]['value'][1]['fpVal'])
            d['max']=int(record['dataset'][0]['point'][0]['value'][2]['fpVal'])
            heart_data.append(d)

    # Pass the plot path to the template
    context = {'heart_data_json': heart_data}
    return context

def resting_heartrate_plot(data):
    print("inside resting heart function\n")
    resting_heart_data=[]
    for record in data['bucket']:
        if len(record['dataset'][0]['point'])==0:
            continue
        else:
            d={}
            d['start']=parse_millis(record['startTimeMillis'])
            d['end']=parse_millis(record['endTimeMillis'])
            d['count']=int(record['dataset'][0]['point'][0]['value'][0]['fpVal'])
            resting_heart_data.append(d)

    # Pass the plot path to the template
    context = {'resting_heart_data_json': resting_heart_data}
    return context

def sleep_plot(data):
    print("inside sleep function\n")
    sleep_data=[]
    for record in data['session']:
        d={}
        d['start']=parse_millis(record['startTimeMillis'])
        d['end']=parse_millis(record['endTimeMillis'])
        d['count']=(int(record['endTimeMillis']) - int(record['startTimeMillis']))/1000/60/60
        sleep_data.append(d)

    # Pass the plot path to the template
    context = {'sleep_data_json': sleep_data}
    return context   

def activity_plot(data):
    print("inside activity function\n")
    activity_data={}
    for record in data['bucket'][0]['dataset'][0]['point']:
        print(record)
        act = df.loc[df['Integer'] == record['value'][0]['intVal']]['Activity Type'].values[0]
        duration = round(int(record['value'][1]['intVal'])/1000/60, 2)
        
        if act in activity_data:
            activity_data[act] += duration
        else:
            activity_data[act] = duration
    
    activity_data = sorted(activity_data.items(), key=lambda x: x[1], reverse=True)
    activity_data = activity_data[:10]

    # Pass the plot path to the template
    context = {'activity_data_json': activity_data}
    return context  

def oxygen_plot(data):
    print("inside oxygen saturation function\n")
    oxygen_data=[]
    for record in data['bucket']:
        if len(record['dataset'][0]['point'])==0:
            continue
        else:
            d={}
            d['start']=parse_millis(record['startTimeMillis'])
            d['end']=parse_millis(record['endTimeMillis'])
            d['count']=int(record['dataset'][0]['point'][0]['value'][0]['fpVal'])
            oxygen_data.append(d)

    # Pass the plot path to the template
    context = {'oxygen_data_json': oxygen_data}
    return context

async def fetch_metric_data(service, metric, total_data, duration, frequency):
    
    end_time = datetime.datetime.now() - datetime.timedelta(minutes=1)
    
    if duration == "day":
        start_time = end_time - datetime.timedelta(hours=23, minutes=59)
    elif duration == "week":
        start_time = end_time - datetime.timedelta(days=6, hours=23, minutes=59)
    elif duration == "month":
        start_time = end_time - datetime.timedelta(days=29, hours=23, minutes=59)
    elif duration == "quarter":
        start_time = end_time - datetime.timedelta(days=89, hours=23, minutes=59)
    
    if frequency == "hourly":
        bucket = 3600000
    elif frequency == "daily":
        bucket = 86400000
    elif frequency == "weekly":
        bucket = 604800000
    elif frequency == "monthly":
        bucket = 2592000000
    
    print(start_time.timestamp())
    print(end_time.timestamp())
    
    start_date = start_time.strftime('%Y-%m-%d')
    end_date = end_time.strftime('%Y-%m-%d')
    
    if metric == "sleep":
        data = service.users().sessions().list(userId='me', activityType=72, startTime=f'{start_date}T00:00:00.000Z', endTime=f'{end_date}T23:59:59.999Z').execute()
    
    else:        
        data = service.users().dataset().aggregate(userId='me', body={
            "aggregateBy": [{
                "dataTypeName": dataTypes[metric]
            }],
            "bucketByTime": {"durationMillis": bucket},
            "startTimeMillis": int(start_time.timestamp()) * 1000,
            "endTimeMillis": int(end_time.timestamp()) * 1000,
        }).execute()
    
    if metric=="heart_rate":
        context=heartrate_plot(data)
        total_data['heartRate']=context
    elif metric=="steps":
        context=steps_barplot(data)
        total_data['steps']=context
    elif metric=="resting_heart_rate":
        context=resting_heartrate_plot(data)
        total_data['restingHeartRate']=context
    elif metric=="sleep":
        context=sleep_plot(data)
        total_data['sleep']=context
    elif metric=="activity":
        context=activity_plot(data)
        total_data['activity']=context
    elif metric=="oxygen":
        context=oxygen_plot(data)
        total_data['oxygen']=context

@sync_to_async
def get_credentials(request):
    if "credentials" in request.session:
        credentials = Credentials(**request.session["credentials"])
        return credentials
    
    return None

async def fetch_all_metric_data(request, duration, frequency):
    total_data = {}
    credentials = await get_credentials(request)
    if credentials:
        try:
            service = build('fitness', 'v1', credentials=credentials)
            tasks = []
            for metric in dataTypes.keys():
                tasks.append(fetch_metric_data(service, metric, total_data, duration, frequency))
            
            await asyncio.gather(*tasks)
        except Exception as e:
            print(e)
            total_data = {}
    
    else:
        print("Not signed in Google")
    
    return total_data
        

async def get_metric_data(request):
    
    duration = 'week'
    frequency = 'daily'
    
    if request.GET.get('data_drn'):
        duration = request.GET.get('data_drn')
    
    if request.GET.get('data_freq'):
        frequency = request.GET.get('data_freq')    
    
    total_data = await fetch_all_metric_data(request, duration, frequency)
    
    context = {'data': total_data}
    print(total_data)
    return render(request, 'metrics/display_metric_data.html', context)

def health_data_view(request):
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table('Django')

    if request.user.is_authenticated:
        print(request.user.id)
    default_email = "test@example.com"

    if request.method == 'POST':
        data = request.POST
        print(data)
        table.put_item(
            Item={
                'email': default_email,  # Use the default email
                'metric': data.get('metric'),
                'time': data.get('time'),
                'value': data.get('value')
            }
        )
        return render(request, 'metrics/display_metric_data.html', {})

    # Fetch all the metrics data from DynamoDB
    response = table.scan()
    metrics_data = {}
    for item in response['Items']:
        metric = item['metric']
        if metric not in metrics_data:
            metrics_data[metric] = []
        metrics_data[metric].append(item)

    for metric in metrics_data:
        metrics_data[metric].sort(key=lambda x: x['time'], reverse=True)

    return render(request, 'metrics/display_metric_data.html', {'metrics_data': metrics_data})