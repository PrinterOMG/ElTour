from django.contrib import admin
from rangefilter.filters import NumericRangeFilter, DateRangeFilter, DateTimeRangeFilter

from web_admin.models import TelegramUser, Country, AuthorTour, TourPickup, AuthorTourRequest


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


class CountryAdmin(admin.ModelAdmin):
    pass


def clone_author_tour(modeladmin, request, queryset):
    for ad in queryset:
        ad.pk = None
        ad.save()


clone_author_tour.short_description = 'Дублировать объект'


class AuthorTourAdmin(admin.ModelAdmin):
    fields = ('country', 'month', 'year', 'description', 'symbols_count', 'landing_url', 'image')
    readonly_fields = ('symbols_count', )
    list_display = ('country_name', 'year', 'months')
    list_filter = ('country__name', ('year', NumericRangeFilter))
    actions = [clone_author_tour]

    def country_name(self, object):
        return object.country.name

    def symbols_count(self, obj: TourPickup):
        template = (
            'Авторский тур\n\n'
            'Направление - {country}\n'
            'Дата - {date}\n'
            'Описание:\n'
            '{description}'
        )

        months = obj.months().split(', ')
        max_month = max(months, key=len)

        result_str = template.format(
            country=obj.country.name,
            date=f'{max_month} {obj.year}',
            description=obj.description
        )

        return len(result_str)

    country_name.short_description = 'Страна'
    symbols_count.short_description = 'Кол-во символов'


class AuthorTourRequestAdmin(admin.ModelAdmin):
    list_display = fields = ('user', 'author_tour', 'month', 'created_at')
    list_filter = (
        ('created_at', DateTimeRangeFilter),
        'created_at',
        'author_tour',
        'user'
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


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
admin.site.register(AuthorTourRequest, AuthorTourRequestAdmin)
