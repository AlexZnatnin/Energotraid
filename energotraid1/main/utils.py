import datetime
import xml.etree.ElementTree as ET
from datetime import date
from lxml import etree
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import *


def read_80000_area(file):
    tree = ET.parse(file)
    root = tree.getroot()
    comment_a = str('в справочник занесена информация о сечениях')
    comment_b = str('новой инфы не обнаружено')
    comment_a_true = False
    comment = str('')
    # импорт area
    for area_elem in root.iter('area'):
        ats_code = int(area_elem.get('ats-code'))
        name = area_elem.get('name')
        # Check if an area with the same ats_code already exists
        if Area.objects.filter(ats_code=ats_code).exists():
            continue  # Skip this area, as it already exists in the database

        # Create a new Area object and save it to the database
        area = Area(name=name, ats_code=ats_code)
        comment_a = comment_a + str(' ') + str(ats_code) + ', '
        comment_a_true = True
        # Set other fields of the area object based on the XML attributes or values
        area.save()
        if comment_a_true == True:
            comment = comment_a
        else:
            comment = comment_b
    return comment


def read_80000_tu(file):
    tree = ET.parse(file)
    root = tree.getroot()
    comment = str('Добавлены точки учета: ')
    for delivery_point_elem in root.iter('delivery-point'):
        ats_code = delivery_point_elem.get('ats-code')
        name_elem = delivery_point_elem.find('name')
        connection_name = name_elem.get('connection-name') if name_elem is not None else None

        # If name element is not found, check for composite-name attribute
        if connection_name is None:
            connection_name = delivery_point_elem.get('composite-name')

        # If connection_name is still None, check for location-description attribute
        if connection_name is None and name_elem is not None:
            connection_name = name_elem.get('location-description')

        # Check if the delivery point already exists in the database
        if not Tu.objects.filter(ats_code=ats_code).exists():
            # Create a new DeliveryPoint object and save it to the database
            delivery_point = Tu(ats_code=ats_code, name=connection_name)
            delivery_point.save()
            comment += ' ' + str(ats_code) + ', '
    return comment


def read_80000_measuring_point(file):
    tree = ET.parse(file)
    root = tree.getroot()
    comment = str('Добавлены точки измерения: ')
    for measuring_point_elem in root.iter('measuring-point'):
        ats_code = measuring_point_elem.get('ats-code')
        name_elem = measuring_point_elem.find('name')
        connection_name_try = name_elem.get('connection-name')
        connection_name = name_elem.get('connection-name') if name_elem is not None else None
        location_description = name_elem.get('location-description') if connection_name_try is not None else None
        if not Measuring_point.objects.filter(ats_code=ats_code).exists():
            # Create a new DeliveryPoint object and save it to the database
            measuring_point = Measuring_point(ats_code=ats_code, name=connection_name,
                                              location_description=location_description)
            measuring_point.save()
            comment += ' ' + str(ats_code) + ', '
    return comment


def read_80000_link(file):
    tree = ET.parse(file)
    root = tree.getroot()
    comment = str('Добавлены связи: ')
    for area_elem in root.iter('area'):
        ats_code = area_elem.get('ats-code')
        comment += "<br>"
        comment += 'для сечения ' + str(ats_code)
        comment += "<br>"
        serv_point_elem = area_elem.find('serviced-points-list')
        for link in serv_point_elem.findall('delivery-point-measuring-point-link'):
            # for serv_point_elem in root.iter('serviced-points-list'):
            #     delivery_point_measuring_point_link_elem = serv_point_elem.findall(
            #         'delivery-point-measuring-point-link')
            #     for link in delivery_point_measuring_point_link_elem:
            comment += "<br>"
            # ---в цикле вытаскиваем точки
            measuring_point_code = str(link.get('measuring-point-code'))
            delivery_point_code = str(link.get('delivery-point-code'))
            comment += 'сечение: ' + str(ats_code) + '- точка учета:' + str(
                delivery_point_code) + '-точка измерения:' + str(measuring_point_code)
            area_obj = Area.objects.get(ats_code=ats_code)
            mp_obj = Measuring_point.objects.get(ats_code=measuring_point_code)
            dp_obj = Tu.objects.get(ats_code=delivery_point_code)
            if mp_obj.tu == None:
                Measuring_point.objects.filter(ats_code=mp_obj.ats_code).update(tu=dp_obj)
            if dp_obj.Area == None:
                Tu.objects.filter(ats_code=dp_obj.ats_code).update(Area=area_obj)
    return comment


def read_80000_channels(file):
    # Load the XML file
    tree = ET.parse(file)
    root = tree.getroot()

    # Initialize the comment
    comment = ' '

    # Iterate over measuring-point tags
    for measuring_point in root.iter('measuring-point'):
        ats_code_point = measuring_point.get('ats-code')
        mp_obj = Measuring_point.objects.get(ats_code=ats_code_point)
        # Iterate over measuring-channel tags inside measuring-device
        for measuring_device in measuring_point.iter('measuring-device'):
            for measuring_channel in measuring_device.iter('measuring-channel'):
                ats_code_channel = measuring_channel.get('ats-code')
                period = measuring_channel.get('period')
                if not Measuring_channel.objects.filter(Measuring_point_code=ats_code_point,
                                                        ats_code=ats_code_channel).exists():
                    comment += str(ats_code_channel)
                    channel = Measuring_channel.objects.create(Measuring_point_code=ats_code_point,
                                                               ats_code=ats_code_channel, Measuring_point=mp_obj)
                    channel.save()
                    # Append the connection information to the comment
                    comment += f"добавлен канал,установлена связь между каналом {ats_code_channel} "
                    comment += f"и точкой учёта {ats_code_point} .\n"

    return comment


def read_80020(file):
    tree = ET.parse(file)
    root = tree.getroot()
    datetime_element = root.find('.//datetime')
    day_element = datetime_element.find('day')

    date_string = day_element.text
    date_object = datetime.datetime.strptime(date_string, '%Y%m%d').date()
    # Initialize the comment
    comment = ' '
    for measuring_point in root.iter('measuringpoint'):
        ats_code_point = measuring_point.get('code')
        name_point = measuring_point.get('name')
        # настроить создание точки измерения
        if not Measuring_point.objects.filter(ats_code=ats_code_point).exists():
            mp_obj = Measuring_point.objects.create(ats_code=ats_code_point, name=name_point)
        mp_obj=Measuring_point.objects.get(ats_code=ats_code_point)
        for measuringchannel in measuring_point.iter('measuringchannel'):
            ats_code_channel = measuringchannel.get('code')
            comment += str(ats_code_channel)

            # настроить создание изм. канала
            if not Measuring_channel.objects.filter(Measuring_point_code=ats_code_point,
                                                    ats_code=ats_code_channel).exists():
                ch_obj = Measuring_channel.objects.create(Measuring_point_code=ats_code_point,
                                                          ats_code=ats_code_channel)
            ch_obj=Measuring_channel.objects.get(Measuring_point_code=ats_code_point,
                                                    ats_code=ats_code_channel)
            for period in measuringchannel.iter('period'):
                pstart = period.get('start')
                pend = period.get('end')
                for value_elem in period.iter('value'):
                    value = value_elem.text
                    # создание данных измерений если их нет
                    if not Measuring_data.objects.filter(Measuring_point_code=ats_code_point,
                                                         channel_ats_code=ats_code_channel, period_start=pstart,
                                                         date=date_object).exists():
                        data1 = Measuring_data.objects.create(Measuring_point_code=ats_code_point,
                                                             channel_ats_code=ats_code_channel,
                                                              Measuring_point=mp_obj,
                                                             Measuring_channel=ch_obj,
                                                              period_start=pstart,
                                                             period_end=pend, value=value,
                                                             date=date_object
                                                              )
                        comment += 'точка измерения: ' + str(ats_code_point) + '-канал' + str(
                            ats_code_channel) + 'период: ' + str(pstart) + ':' + str(pend) + ' Данные измерений:' + str(value)+'<br>'
    return comment
