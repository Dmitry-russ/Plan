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
    flag: bool = True  # дополнительный флаг
    result: list = []  # итоговый список
    while k < len(main):
        #  i = 0
        #  flag = True
        #  while i < len(donemai) and flag:
        if donemai and donemai[0].maintenance == main[k]:
            check = {
                    "mileage": donemai[0].mileage,
                    "number": donemai[0].maintenance.number,
                    "type": donemai[0].maintenance.type,
                    "maintenance_date": donemai[0].maintenance_date,
                    "place": donemai[0].place,
                    "comment": donemai[0].comment,
                    "done": True,
                    "pk": donemai[0].pk,
                    "author": donemai[0].author,
                }
            result.append(check)
            k += 1
            donemai.pop(i)
            #  flag = False
        elif donemai and donemai[0].maintenance.order == False:
            check = {
                    "mileage": donemai[0].mileage,
                    "number": donemai[0].maintenance.number,
                    "type": donemai[0].maintenance.type,
                    "maintenance_date": donemai[0].maintenance_date,
                    "place": donemai[0].place,
                    "comment": donemai[0].comment,
                    "done": True,
                    "pk": donemai[0].pk,
                    "author": donemai[0].author,
            }
            result.append(check)
            donemai.pop(0)
            #  flag = False
        else:
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
