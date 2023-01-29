from django.core.paginator import Paginator

from .models import DoneMaiDate, Maintenance


def page_control(request, objects, count):
    paginator = Paginator(objects, count)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def result_mai_list(main: Maintenance, donemai: DoneMaiDate):
    """Функция расчета необходимых к выводу проведенных ТО."""
    i: int = 0  # счетчик выполненных инспекций
    k: int = 0  # счетчик будущих инспекций
    result: list = []  # итоговый список
    while k < len(main) and k < (len(donemai) + 7):
        # если выполненные инспекции совпадают с порядком проведения
        if i < len(donemai) and donemai[i].maintenance == main[k]:
            check = {
                "number": donemai[i].maintenance.number,
                "type": donemai[i].maintenance.type,
                "mileage": donemai[i].mileage,
                "maintenance_date": donemai[i].maintenance_date,
                "place": donemai[i].place,
                "comment": donemai[i].comment,
                "done": True,
                "pk": donemai[i].pk,
            }
            result.append(check)
            i += 1
            k += 1
        # если пропущена инспекция
        elif i < len(donemai) and donemai[i].maintenance.number:
            check = {
                "number": main[k].number,
                "type": main[k].type,
                "mileage": main[k].mileage,
                "maintenance_date": "-",
                "place": "-",
                "comment": "не проводилась",
                "done": False,
                "pk": main[k].pk,
            }
            result.append(check)
            k += 1
        # внеочередная инспекция
        elif i < len(donemai):
            check = {
                "number": donemai[i].maintenance.number,
                "type": donemai[i].maintenance.type,
                "mileage": donemai[i].mileage,
                "maintenance_date": donemai[i].maintenance_date,
                "place": donemai[i].place,
                "comment": donemai[i].comment,
                "done": True,
                "pk": donemai[i].pk,
            }
            result.append(check)
            i += 1
        # выполненные инспекции закончились
        elif i >= len(donemai):
            check = {
                "number": main[k].number,
                "type": main[k].type,
                "mileage": main[k].mileage,
                "maintenance_date": "-",
                "place": "-",
                "comment": "не проводилась",
                "done": False,
                "pk": main[k].pk,
            }
            result.append(check)
            k += 1
    return result
