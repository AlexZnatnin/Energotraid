from .models import *

class Calc_model:
    def __init__(self, area_ats_code):
        self.area_ats_code = area_ats_code
        self.gtp_list = []
        self.delivery_point_list = []
        self.measuring_point_list = []

        #self.name

        # Connect to the database and retrieve the required data
        self.populate_data()

    def populate_data(self):
        # Retrieve the area based on area_ats_code
        try:
            area = Area.objects.get(ats_code=self.area_ats_code)
        except Area.DoesNotExist:
            # Handle the case when the area is not found
            return

        # Retrieve related models based on the area
        delivery_points = Tu.objects.filter(Area=area)
        measuring_points = Measuring_point.objects.filter(tu__in=delivery_points)
        # Assign values to the class fields
        self.delivery_point_list = [str(delivery_point.ats_code) for delivery_point in delivery_points]
        self.measuring_point_list = [str(measuring_point.ats_code) for measuring_point in measuring_points]


def create_or_retrieve_calc_model(area_ats_code):
    # Check if a Calc_model object already exists with the given area_ats_code
    existing_obj = Calc_model.objects.filter(area_ats_code=area_ats_code).first()
    if existing_obj:
        # If an object already exists, return it
        return existing_obj

    # If no existing object found, create a new instance of Calc_model
    calc_model = Calc_model(area_ats_code)

    # Save the calc_model object to the database
    calc_model.save()

    return calc_model

