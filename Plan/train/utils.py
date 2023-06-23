import openpyxl

from django.core.paginator import Paginator

from .models import DoneMaiDate, Maintenance


def page_control(request, objects, count):
    paginator = Paginator(objects, count)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def dict_create(main: Maintenance, donemai: DoneMaiDate, k, result):
    """Вспомогательная функция создания словаря с данными для вывода."""
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


def excel_open(file):
    """Функция считывания данных из файла с пробегами."""
    book = openpyxl.open(file, read_only=True, data_only=True)
    sheet = book.active
    myfile_list: list = []
    for row in range(2, sheet.max_row+1):
        serial = sheet[row][0].value
        number = sheet[row][1].value
        if isinstance(number, int):
            number = f'{number:03d}'
        data = sheet['C1'].value
        data = data.strftime("%d.%m.%Y")
        mileage = sheet[row][3].value
        #  mejremont = sheet[row][4].value
        #  leto = sheet[row][5].value
        #  status = sheet[row][6].value
        temporarily = [serial, number, mileage, data]
        myfile_list.append(temporarily)
    return myfile_list
