from django.contrib.admin import ModelAdmin, register

from .models import Tag, Ingredient, Recipes, Ingredient_amount, Shopping_cart, Favorite


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'color')


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@register(Recipes)
class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ('count_favorites',)

    def count_favorites(self, obj):
        return obj.favorites.count()

    count_favorites.short_description = 'Число добавлений в избранное'


@register(Ingredient_amount)
class IngredientAmountAdmin(ModelAdmin):
    pass


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    pass


@register(Shopping_cart)
class CartAdmin(ModelAdmin):
    pass
