from django.core.paginator import Paginator

from .models import DoneMaiDate, Maintenance


def page_control(request, objects, count):
    paginator = Paginator(objects, count)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def dict_create(main: Maintenance, donemai: DoneMaiDate, k, result):
    mileage = '{0:,}'.format(donemai[0].mileage).replace(',', ' ')
    check = {
        "mileage": mileage,
        "number": donemai[0].maintenance.number,
        "type": donemai[0].maintenance.type,
        "maintenance_date": donemai[0].maintenance_date,
        "place": donemai[0].place,
        "comment": donemai[0].comment,
        "done": True,
        "pk": donemai[0].pk,
        "author": donemai[0].author,
        "musthave": donemai[0].musthave,
    }
    result.append(check)


def result_mai_list(main: Maintenance, donemai: DoneMaiDate):
    """Функция расчета необходимых к выводу проведенных ТО."""
    i: int = 0  # счетчик выполненных инспекций
    k: int = 0  # счетчик будущих инспекций
    result: list = []  # итоговый список
    while k < len(main):
        if donemai and donemai[0].maintenance == main[k]:
            dict_create(main, donemai, k, result)
            k += 1
            donemai.pop(i)
        elif donemai and donemai[0].maintenance.order is False:
            dict_create(main, donemai, k, result)
            donemai.pop(0)
        else:
            check = {
                "number": main[k].number,
                "type": main[k].type,
                "mileage": '{0:,}'.format(main[k].mileage).replace(',', ' '),
                "maintenance_date": "-",
                "place": "-",
                "comment": "не проводилась",
                "done": False,
                "pk": main[k].pk,
            }
            result.append(check)
            k += 1
    return result
