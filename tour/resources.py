from import_export import resources, fields, widgets

from hotels.models import Hotel_Data
from .models import Package, Tour

class packages_resource(resources.ModelResource):
    TourName = fields.Field(column_name='نام تور', attribute='TourName', widget=widgets.ForeignKeyWidget(Tour, 'Title'))
    HotelName = fields.Field(column_name='هتل اول', attribute='HotelName', widget=widgets.ForeignKeyWidget(Hotel_Data, 'HotelName'))
    Mhotel = fields.Field(column_name='هتل دوم', attribute='Mhotel', widget=widgets.ForeignKeyWidget(Hotel_Data, 'HotelName'))
    M1hotel = fields.Field(column_name='هتل سوم', attribute='M1hotel', widget=widgets.ForeignKeyWidget(Hotel_Data, 'HotelName'))
    M2hotel = fields.Field(column_name='هتل چهارم', attribute='M2hotel', widget=widgets.ForeignKeyWidget(Hotel_Data, 'HotelName'))
    M3hotel = fields.Field(column_name='هتل پنجم', attribute='M3hotel', widget=widgets.ForeignKeyWidget(Hotel_Data, 'HotelName'))
    DoubleBedPrice = fields.Field(column_name='دو تخته', attribute='DoubleBedPrice')
    SingleBedPrice = fields.Field(column_name='یک دتخته', attribute='SingleBedPrice')
    BabyWithBedPrice = fields.Field(column_name='کودک با تخت', attribute='BabyWithBedPrice')
    BabyWithoutBedPrice = fields.Field(column_name='کودک بدون تخت', attribute='BabyWithoutBedPrice')
    InfontPrice = fields.Field(column_name='نوزاد', attribute='InfontPrice')

    class Meta:
        model = Package
        fields = ('id', 'TourName', 'HotelName', 'Mhotel', 'M1hotel', 'M2hotel', 'M3hotel',
                  'DoubleBedPrice', 'SingleBedPrice',
                  'BabyWithBedPrice', 'BabyWithoutBedPrice', 'InfontPrice')
        export_order = ('TourName', 'HotelName', 'Mhotel', 'M1hotel', 'M2hotel', 'M3hotel',
                        'DoubleBedPrice', 'SingleBedPrice',
                        'BabyWithBedPrice', 'BabyWithoutBedPrice', 'InfontPrice', 'id')

class packages_import_resource(resources.ModelResource):
    DoubleBedPrice = fields.Field(column_name='دو تخته', attribute='DoubleBedPrice')
    SingleBedPrice = fields.Field(column_name='یک دتخته', attribute='SingleBedPrice')
    BabyWithBedPrice = fields.Field(column_name='کودک با تخت', attribute='BabyWithBedPrice')
    BabyWithoutBedPrice = fields.Field(column_name='کودک بدون تخت', attribute='BabyWithoutBedPrice')
    InfontPrice = fields.Field(column_name='نوزاد', attribute='InfontPrice')

    class Meta:
        model = Package
        fields = ('id',
                  'DoubleBedPrice', 'SingleBedPrice',
                  'BabyWithBedPrice', 'BabyWithoutBedPrice', 'InfontPrice')
        export_order = (
                        'DoubleBedPrice', 'SingleBedPrice',
                        'BabyWithBedPrice', 'BabyWithoutBedPrice', 'InfontPrice', 'id')
        skip_unchanged = True
        report_skipped = False
