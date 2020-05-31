import json  # ***json 임포트 추가***
from django.http import JsonResponse  # for chart_data()
from django.shortcuts import render
from .models import Passenger
from django.db.models import Count, Q


def home(request):
    return render(request, 'chart/home.html')


def world_population(request):
    return render(request, 'chart/world_population.html')


def covid19_view(request):
    return render(request, 'chart/covid19.html')


def ticket_class_view_1(request):  # 방법 1
    print('방법1')
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(
            survived_count=Count('ticket_class',
                                 filter=Q(survived=True)),
            not_survived_count=Count('ticket_class',
                                     filter=Q(survived=False))) \
        .order_by('ticket_class')
    return render(request, 'chart/ticket_class_1.html', {'dataset': dataset})
#  dataset = [
#    {'ticket_class': 1, 'survived_count': 200, 'not_survived_count': 123},
#    {'ticket_class': 2, 'survived_count': 119, 'not_survived_count': 158},
#    {'ticket_class': 3, 'survived_count': 181, 'not_survived_count': 528}
#  ]


def ticket_class_view_2(request):  # 방법 2
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')

    # 빈 리스트 3종 준비
    categories = list()             # for xAxis
    survived_series = list()        # for series named 'Survived'
    not_survived_series = list()    # for series named 'Not survived'

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s Class' % entry['ticket_class'])       # for xAxis
        survived_series.append(entry['survived_count'])             # for series named 'Survived'
        not_survived_series.append(entry['not_survived_count'])     # for series named 'Not survived'

    # json.dumps() 함수로 리스트 3종을 JSON 데이터 형식으로 반환
    return render(request, 'chart/ticket_class_2.html', {
        'categories': json.dumps(categories),
        'survived_series': json.dumps(survived_series),
        'not_survived_series': json.dumps(not_survived_series)
    })


def ticket_dump():
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')

    # 빈 리스트 3종 준비 (series 이름 뒤에 '_data' 추가)
    categories = list()  # for xAxis
    survived_series_data = list()  # for series named 'Survived'
    not_survived_series_data = list()  # for series named 'Not survived'
    survived_rate = list()

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s 등석' % entry['ticket_class'])  # for xAxis
        survived_series_data.append(entry['survived_count'])  # for series named 'Survived'
        not_survived_series_data.append(entry['not_survived_count'])  # for series named 'Not survived'
        survived_rate.append(entry['survived_count'] / (entry['survived_count'] + entry['not_survived_count']) * 100.)

    chart = {
        'chart': {
            'zoomType': 'xy',
            'borderColor': '#9DB0AC',
            'borderWidth': 3,
        },
        'title': {'text': '좌석 등급에 따른 타이타닉 생존/비 생존 인원 및 생존율'},
        'xAxis': {'categories': categories},
        'yAxis': [{  # Primary yAxis
            'labels': {
                'format': '{value} %',
                'style': {'color': 'blue'}
            }, 'title': {
                'text': '생존율',
                'style': {'color': 'blue'}
            },
        }, {  # Secondary yAxis
            'labels': {
                'format': '{value} 명',
                'style': {'color': 'black'}
            }, 'title': {
                'text': '인원',
                'style': {'color': 'black'}
            },
            'opposite': 'true'
        }, ],
        'tooltip': {
            'shared': 'true'
        },
        'legend': {
            'layout': 'vertical',
            'align': 'left',
            'x': 120,
            "verticalAlign": 'top',
            "y": 100,
            'floating': 'true',
            # 'backgroundColor':
            #     Highcharts.defaultOptions.legend.backgroundColor | | # theme
            #     'rgba(255,255,255,0.25)'
        },
        'series': [{
            'name': '생존',
            'type': 'column',
            'yAxis': 1,
            'data': survived_series_data,
            'color': 'green',
            'tooltip': {'valueSuffix': ' 명'}
        }, {
            'name': '비 생존',
            'type': 'column',
            'yAxis': 1,
            'color': 'red',
            'data': not_survived_series_data,
            'tooltip': {'valueSuffix': ' 명'}
        }, {
            'name': '생존율',
            'type': 'spline',
            'data': survived_rate,
            'tooltip': {'valueSuffix': ' %'}
        },
        ]
    }

    dump = json.dumps(chart)
    return dump


def ticket_class_view_3(request):  # 방법 3

    return render(request, 'chart/ticket_class_3.html', {'chart': ticket_dump()})


def json_example(request):  # 접속 경로 'json-example/'에 대응하는 뷰
    return render(request, 'chart/json_example.html')


def chart_data(request):  # 접속 경로 'json-example/data/'에 대응하는 뷰
    dataset = Passenger.objects \
        .values('embarked') \
        .exclude(embarked='') \
        .annotate(total=Count('id')) \
        .order_by('-total')
    #  [
    #    {'embarked': 'S', 'total': 914}
    #    {'embarked': 'C', 'total': 270},
    #    {'embarked': 'Q', 'total': 123},
    #  ]

    # # 탑승_항구 상수 정의
    # CHERBOURG = 'C'
    # QUEENSTOWN = 'Q'
    # SOUTHAMPTON = 'S'
    # PORT_CHOICES = (
    #     (CHERBOURG, 'Cherbourg'),
    #     (QUEENSTOWN, 'Queenstown'),
    #     (SOUTHAMPTON, 'Southampton'),
    # )
    port_display_name = dict()
    for port_tuple in Passenger.PORT_CHOICES:
        port_display_name[port_tuple[0]] = port_tuple[1]
    # port_display_name = {'C': 'Cherbourg', 'Q': 'Queenstown', 'S': 'Southampton'}

    chart = {
        'chart': {
            'type': 'pie',
            'borderColor': '#9DB0AC',
            'borderWidth': 3,
        },
        'title': {'text': '승선 항구에 따른 타이타닉 승객 수'},
        'series': [{
            'name': 'Embarkation Port',
            'data': list(map(
                lambda row: {'name': port_display_name[row['embarked']], 'y': row['total']},
                dataset))
            # 'data': [ {'name': 'Southampton', 'y': 914},
            #           {'name': 'Cherbourg', 'y': 270},
            #           {'name': 'Queenstown', 'y': 123}]
        }]
    }
    # [list(map(lambda))](https://wikidocs.net/64)

    return JsonResponse(chart)

