from django.contrib import admin
from rangefilter.filters import NumericRangeFilter, DateRangeFilter, DateTimeRangeFilter

from web_admin.models import TelegramUser, Country, AuthorTour, TourPickup


class TelegramUserAdmin(admin.ModelAdmin):
    fields = ('telegram_id', 'phone', 'name', 'birthday', 'full_name', 'mention', 'mailing_sub', 'created_at')

    readonly_fields = ('telegram_id', 'phone', 'full_name', 'mention', 'created_at')

    list_display = ('mention', 'phone', 'name', 'full_name', 'birthday', 'mailing_sub', 'created_at')

    list_display_links = ('mention', 'phone')

    list_filter = (('birthday', DateRangeFilter), ('created_at', DateTimeRangeFilter), 'mailing_sub')

    search_fields = ('name', 'full_name', 'phone', 'mention', 'telegram_id')
    search_help_text = 'Введите имя, номер телефона или ID...'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CountryAdmin(admin.ModelAdmin):
    pass


class AuthorTourAdmin(admin.ModelAdmin):
    fields = ('country', 'month', 'year', 'description', 'landing_url', 'image_url')
    list_display = ('country_name', 'year', 'month')
    list_filter = ('country__name', 'month', ('year', NumericRangeFilter))

    def country_name(self, object):
        return object.country.name

    country_name.short_description = 'Страна'


class TourPickupAdmin(admin.ModelAdmin):
    list_display = ('departure_city', 'country', 'adults_count', 'kids_count', 'pretty_stars', 'food_type', 'date',
                    'night_count', 'telegram_user')

    list_filter = ('hotel_stars', 'night_count', 'food_type', ('adults_count', NumericRangeFilter),
                   ('kids_count', NumericRangeFilter), ('date', DateRangeFilter), 'country', 'departure_city')

    fields = ('departure_city', 'country', 'adults_count', 'kids_count', 'pretty_kids_ages', 'pretty_stars',
              'food_type', 'date', 'night_count', 'telegram_user')

    readonly_fields = fields

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(AuthorTour, AuthorTourAdmin)
admin.site.register(TourPickup, TourPickupAdmin)
