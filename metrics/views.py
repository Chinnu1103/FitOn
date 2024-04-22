from django.shortcuts import render, redirect
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
import json
import datetime


dataTypes = {
    "heart_rate": "com.google.heart_rate.bpm",
    "resting_heart_rate": "com.google.heart_rate.bpm",
    "steps": "com.google.step_count.delta",
    "sleep": "com.google.sleep.segment",
    "exercise": "com.google.activity.exercise"
}

dataSources = {
    "heart_rate": "derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm",
    "resting_heart_rate": "derived:com.google.heart_rate.bpm:com.google.android.gms:resting_heart_rate<-merge_heart_rate_bpm",
    "steps": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps",
    "sleep": "derived:com.google.sleep.segment:com.google.android.gms:merged",
    "exercise": "derived:com.google.activity.exercise:com.google.android.gms:merged"
}


#function to convert miliseconds to Day
def parse_millis(millis):
    return datetime.datetime.fromtimestamp(int(millis) / 1000).strftime('%Y-%m-%d')

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
            d={}
            d['start']=parse_millis(record['startTimeMillis'])
            d['end']=parse_millis(record['endTimeMillis'])
            d['count']=int(record['dataset'][0]['point'][0]['value'][0]['fpVal'])
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
    for record in data['bucket']:
        if len(record['dataset'][0]['point'])==0:
            continue
        else:
            d={}
            d['start']=parse_millis(record['startTimeMillis'])
            d['end']=parse_millis(record['endTimeMillis'])
            d['count']=int(record['dataset'][0]['point'][0]['value'][0]['fpVal'])
            sleep_data.append(d)

    # Pass the plot path to the template
    context = {'sleep_data_json': sleep_data}
    return context


def get_metric_data(request):
    total_data = {}
    if "credentials" in request.session:
        try:
            credentials = Credentials(**request.session["credentials"])
            service = build('fitness', 'v1', credentials=credentials)
            
            end_time = datetime.datetime.now().replace(hour=23, minute=59, second=59)
            start_time = end_time - datetime.timedelta(days=10)
            print(start_time.timestamp())
            print(end_time.timestamp())
            for metric in dataTypes.keys():
                data = service.users().dataset().aggregate(userId='me', body={
                    "aggregateBy": [{
                        "dataTypeName": dataTypes[metric],
                        "dataSourceId": dataSources[metric]
                    }],
                    "bucketByTime": {"durationMillis": 86400000},
                    "startTimeMillis": int(start_time.timestamp()) * 1000,
                    "endTimeMillis": int(end_time.timestamp()) * 1000,
                }).execute()
                if metric=="heart_rate":
                    context=heartrate_plot(data)
                    total_data['heartRate']=context
                elif metric=="steps":
                    context=steps_barplot(data)
                    total_data['steps']=context
                    print(total_data)
                elif metric=="resting_heart_rate":
                    context=resting_heartrate_plot(data)
                    total_data['restingHeartRate']=context
                # elif metric=="sleep":
                #     context=sleep_plot(data)
                #     total_data['sleep']=context   
        except Exception as e:
            print(e)
            data = None

    context = {'data':total_data}
    

    return render(request, 'metrics/display_metric_data.html', context)
