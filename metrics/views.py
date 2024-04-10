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
    
    steps_data_json=json.dumps(steps_data)

    # Pass the plot path to the template
    context = {'steps_data_json': steps_data_json}
    return context
    # return render(request, 'steps_barplot.html', context)
        


def get_metric_data(request, metric):
    data = None
    # print(request.session['credentials'])
    if "credentials" in request.session:
        try:
            credentials = Credentials(**request.session["credentials"])
            service = build('fitness', 'v1', credentials=credentials)
            
            end_time = datetime.datetime.now().replace(hour=23, minute=59, second=59)
            start_time = end_time - datetime.timedelta(days=10)
            print(start_time.timestamp())
            print(end_time.timestamp())

            data = service.users().dataset().aggregate(userId='me', body={
                "aggregateBy": [{
                    "dataTypeName": dataTypes[metric],
                    "dataSourceId": dataSources[metric]
                }],
                "bucketByTime": {"durationMillis": 86400000},
                "startTimeMillis": int(start_time.timestamp()) * 1000,
                "endTimeMillis": int(end_time.timestamp()) * 1000,
            }).execute()
            
        except Exception as e:
            print(e)
            data = None
    
    context=steps_barplot(data)
    print(context)
    print(type(context))
    return render(request, 'metrics/display_metric_data.html', context)
