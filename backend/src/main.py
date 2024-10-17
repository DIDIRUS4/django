from django.views.generic import View
from django.shortcuts import render


class Main(View):

    def __init__(self) -> None:
        pass

    def get(self, request):
        a = request.GET.get('a')
        b = request.GET.get('b')
        c = request.GET.get('c')

        if a is None or b is None or c is None:
            return render(request, 'index.html', {'error': 'Не все коэффициенты заданы'})

        try:
            a = float(a)
            b = float(b)
            c = float(c)
        except ValueError:
            return render(request, 'index.html', {'error': 'Коэффициенты должны быть числами'})

        if a == 0:
            if b == 0:
                if c == 0:
                    return render(request, 'index.html', {'ok': 'Бесконечное количество решений'})
                else:
                    return render(request, 'index.html', {'error': 'Нет решений'})
            else:
                root = -c / b
                return render(request, 'index.html', {'a': a, 'b': b, 'c': c, 'root': root})
        else:
            discriminant = b ** 2 - 4 * a * c
            if discriminant < 0:
                return render(request, 'index.html', {'error': 'Нет решений'})
            elif discriminant == 0:
                root = -b / (2 * a)
                return render(request, 'index.html', {'a': a, 'b': b, 'c': c, 'root': root})
            else:
                root1 = (-b + discriminant ** 0.5) / (2 * a)
                root2 = (-b - discriminant ** 0.5) / (2 * a)
                return render(request, 'index.html', {'a': a, 'b': b, 'c': c, 'root1': root1, 'root2': root2})


if __name__ == '__main__':
    Main()
