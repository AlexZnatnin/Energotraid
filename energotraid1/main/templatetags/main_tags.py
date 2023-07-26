from django import template

register = template.Library()

menu = [{'title':'Тарифы' ,'url_name':'#' },
        {'title': 'Контрагенты','url_name':'#' },
        {'title': 'Точки учета','url_name': '#'},
        {'title': 'Договоры','url_name':'#'} ]

@register.inclusion_tag('main/show_menu.html')
def show_menu():
    return {'menu' : menu }