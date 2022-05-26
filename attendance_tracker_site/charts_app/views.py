
from django.shortcuts import render
from attendance_tracker.models import Student
from django.db.models import Count

def pie_chart(request):
    print("In pie-chart!")
    labels = []
    data = []


    result = (Student.objects.values('departement')
    .annotate(dcount=Count('departement'))
    .order_by()
    )
    print(result)
    for Entry in result:
        labels.append(Entry['departement'])
        data.append(Entry['dcount'])
        print(Entry['departement'],Entry['dcount'])
    #queryset = Student.objects..order_by('departement')

    #for departement in queryset:
    #    labels.append(city.name)
    #    data.append(city.population)

    #return render(request, 'pie_chart.html', {
    return render(request,'charts_app/index.html',{
        'labels': labels,
        'data': data,
    })

#def index(request):
#    print("In charts")
#    return render(request, 'charts_app/index.html')

