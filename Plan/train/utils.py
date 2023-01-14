from django.core.paginator import Paginator


def page_control(request, objects, count):
    paginator = Paginator(objects, count)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
