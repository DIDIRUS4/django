from django.views.generic import View
from django.shortcuts import render


class Main(View):

    def __init__(self) -> None:
        pass

    def solver(self, request, name):
        a = None
        b = None
        c = None
        if request.method == 'GET':
            a = request.GET.get('a')
            b = request.GET.get('b')
            c = request.GET.get('c')
        elif request.method == 'POST':
            a = request.POST.get('a')
            b = request.POST.get('b')
            c = request.POST.get('c')
        print(a, b, c)
        if a is None or b is None or c is None:
            if name == 'education':
                return render(request, 'education.html', {'error': 'Не все коэффициенты заданы'})
            else:
                return render(request, 'index.html', {'error': 'Не все коэффициенты заданы'})
        try:
            a = float(a)
            b = float(b)
            c = float(c)
        except ValueError:
            if name == 'education':
                return render(request, 'education.html', {'error': 'Коэффициенты должны быть числами'})
            else:
                return render(request, 'index.html', {'error': 'Коэффициенты должны быть числами'})
        if a == 0:
            if b == 0:
                if c == 0:
                    if name == 'education':
                        return render(request, 'education.html', {'unresolved': 'Бесконечное количество решений'})
                    else:
                        return render(request, 'index.html', {'ok': 'Бесконечное количество решений'})
                else:
                    if name == 'education':
                        return render(request, 'education.html', {'error': 'Нет решений'})
                    else:
                        return render(request, 'index.html', {'error': 'Нет решений'})
            else:
                root = -c / b
                if name == 'education':
                    return render(request, 'education.html', {'success': True, 'a': a, 'b': b, 'c': c, 'root': root})
                else:
                    return render(request, 'index.html', {'a': a, 'b': b, 'c': c, 'root': root})
        else:
            discriminant = b ** 2 - 4 * a * c
            if discriminant < 0:
                if name == 'education':
                    return render(request, 'education.html', {'error': 'Нет решений'})
                else:
                    return render(request, 'index.html', {'error': 'Нет решений'})
            elif discriminant == 0:
                root = -b / (2 * a)
                if name == 'education':
                    return render(request, 'education.html', {'success': True, 'a': a, 'b': b, 'c': c, 'root': root})
                else:
                    return render(request, 'index.html', {'a': a, 'b': b, 'c': c, 'root': root})
            else:
                root1 = (-b + discriminant ** 0.5) / (2 * a)
                root2 = (-b - discriminant ** 0.5) / (2 * a)
                if name == 'education':
                    return render(request, 'education.html', {'success': True, 'a': a, 'b': b, 'c': c, 'root1': root1, 'root2': root2})
                else:
                    return render(request, 'index.html', {'a': a, 'b': b, 'c': c, 'root1': root1, 'root2': root2})

    def get(self, request):
        name = request.resolver_match.url_name
        if name == 'education':
            return render(request, 'education.html')
        elif name == 'solve':
            return self.solver(request, name)

    

    def post(self, request):
        name = request.resolver_match.url_name
        return self.solver(request, name)


if __name__ == '__main__':
    Main()
