from django.views.generic import View
from django.shortcuts import render
from second.models import Calculator
from django.db import connection
from django.core.paginator import Paginator
from ops.models import News

class Main(View):

    def __init__(self) -> None:
        pass

    def fetch_data(self) -> list:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM second_calculator")
            rows = cursor.fetchall()
            # for row in rows:
            #     print(row)
            return rows
    
    def getDBData(self, request):
        return render(request, 'monitor.html', {'data': self.fetch_data()})

    def solver(self, request, name):
        a = None
        b = None
        c = None
        if request.method == 'GET':
            a = request.GET.get('a')
            b = request.GET.get('b')
            c = request.GET.get('c')
        elif request.method == 'POST':
            a = float(request.POST.get('a'))
            b = float(request.POST.get('b'))
            c = float(request.POST.get('c'))
            
        if (name == 'solve'):
        # print(a, b, c)
            if a is None or b is None or c is None:
                return render(request, 'calc.html', {'error': 'Не все коэффициенты заданы'})
            try:
                a = float(a)
                b = float(b)
                c = float(c)
            except ValueError:
                return render(request, 'calc.html', {'error': 'Коэффициенты должны быть числами'})
            if a == 0:
                if b == 0:
                    if c == 0:
                        return render(request, 'calc.html', {'ok': 'Бесконечное количество решений'})
                    else:
                        return render(request, 'calc.html', {'error': 'Нет решений'})
                else:
                    root = -c / b
                    return render(request, 'calc.html', {'a': a, 'b': b, 'c': c, 'root': root})
            else:
                discriminant = b ** 2 - 4 * a * c
                if discriminant < 0:
                    return render(request, 'calc.html', {'error': 'Нет решений'})
                elif discriminant == 0:
                    root = -b / (2 * a)
                    return render(request, 'calc.html', {'a': a, 'b': b, 'c': c, 'root': root})
                else:
                    root1 = (-b + discriminant ** 0.5) / (2 * a)
                    root2 = (-b - discriminant ** 0.5) / (2 * a)
                    return render(request, 'calc.html', {'a': a, 'b': b, 'c': c, 'root1': root1, 'root2': root2})
        elif (name == 'education'):
            root1 = float(request.POST.get('root1'))
            root2 = float(request.POST.get('root2'))
            isCorrectStatus = False
            discriminant = b ** 2 - 4 * a * c
            if discriminant < 0 and root1 == 0 and root2 == 0:
                isCorrectStatus = True
            elif discriminant == 0:
                if round(root1, 2) == round(-b / (2 * a), 2):
                    isCorrectStatus = True
            else:
                if round(root1, 2) == round((-b + discriminant ** 0.5) / (2 * a), 2) and round(root2, 2) == round((-b - discriminant ** 0.5) / (2 * a), 2):
                    isCorrectStatus = True
                    
            calc = Calculator(a=a, b=b, c=c, root1=root1, root2=root2, isCorrect=isCorrectStatus)
            calc.save()
            
            if (isCorrectStatus):
                return render(request, 'education.html', {'ok': 'Ваш ответ является решением'})
            else:
                return render(request, 'education.html', {'error': 'Ваш ответ не является решением', 'correct': 'Правильное решение: ' + str(a) + 'x^2 + ' + str(b) + 'x + ' + str(c) + ' имеет корни ' + str(round((-b + discriminant ** 0.5) / (2 * a), 2)) + ' и ' + str(round((-b - discriminant ** 0.5) / (2 * a), 2))})
            
    def news(self, request):
        news_list = News.objects.all()
        paginator = Paginator(news_list, 4)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        news_id = request.GET.get('news_id')
        if news_id:
            return render(request, 'news.html', {'news': News.objects.get(id=news_id)})
        return render(request, 'newsall.html', {'news_list': page_obj})

    def get(self, request):
        name = request.resolver_match.url_name
        print(name)
        if name == 'education':
            return render(request, 'education.html')
        elif name == 'solve':
            return self.solver(request, name)
        elif name == 'monitor':
            return self.getDBData(request)
        elif name == 'news':
            return self.news(request)
        else:
            return render(request, 'index.html')


    def post(self, request):
        name = request.resolver_match.url_name
        return self.solver(request, name)


if __name__ == '__main__':
    Main()
