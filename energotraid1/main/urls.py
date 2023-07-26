from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('energy_app',main.urls)


    #--------------------маршрутизация--------------------------------
    path('',views.index),
    path('cp',views.cp,name='cp'),
    path('counterparty/<int:counterparty_id>',views.counterparty,name='counterparty'),
    path('cp_create',views.cp_create,name='cp_create'),
    path('cont_create',views.cont_create,name='cont_create'),
    path('cont',views.cont,name='cont'),

    #-----точки учёта-----------
    path('tu',views.tu,name='tu'),
    path('tu/<int:tu_id>', views.tu_view, name='tu_view'),
    path('tu_create',views.tu_create,name='tu_create'),

    #-----сечение---------------
    path('area',views.area,name='area'),
    path('create_calc_model/<int:area_ats_code>',views.create_calc_model,name='create_calc_model'),
    #path('area/<int:area_id>',views.atea_view),
    #path('area_create',views.area_create)

    # -----точки измерения---------------
    path('measuring_point', views.measuring_point, name='measuring_point'),
    # path('measuring_point/<int:area_id>',views.measuring_point_view),
    # path('measuring_point_create',views.measuring_point_create)

    #------измерительные каналы----------
    path('measuring_channel',views.measuring_channel,name='measuring_channel'),

    # ------данные измерений----------
    path('measuring_data', views.measuring_data, name='measuring_data'),

    path('rate',views.rate,name='rate'),
    path('import',views.import1,name='import1'),
    path('import80000',views.import80000,name='import80000'),
    path('main/upload_success', views.upload_success, name='upload_success'),
    path('uploaded_maket',views.uploaded_maket,name='uploaded_maket'),
    path('import_data_80000/<int:pk>/',views.import_data_80000,name='import_data_80000'),

    path('calculate', views.calculate,name='calculate')
    #-----------------------------------------------------------------------------------------------
]
