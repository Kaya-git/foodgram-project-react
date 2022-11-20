from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='название',
        max_length=250,
        unique=True
        )
    color = models.CharField(
        verbose_name='цвет HEX',
        max_length=7,
        unique=True
        )
    slug = models.SlugField(
        verbose_name='слаг',
        max_length=250,
        unique=True
        )
    
    class Meta:
        verbose_name='Тэги'
        verbose_name_plural='Тэги'

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='название ингридиента',
        max_length=250,
        unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name='Ингридиент'
        verbose_name='Ингридиенты' 


class Recipes(models.Model):
    tag = models.ForeignKey(
        Tag, null=True,
        related_name='tag',
        verbose_name='таг рецепта',
        on_delete=models.SET_NULL
        )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='автор рецепта',
        related_name='recipes_author'
        )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Ingredient_amount',
        verbose_name='ингридиенты',
        related_name='recipes'
    )
    name = models.CharField(
        verbose_name='название блюда',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='изображение',
        upload_to='recipes/'
    )
    text = models.TextField(
        verbose_name='Текстовое описание приготовления'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
    )


    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name


class Ingredient_amount(models.Model):
    ricepe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='содержится в данном рецепте',
        related_name='ricepe'
        )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингридиент в составе',
        related_name='ingridient'
    )
    measurement_unit = models.CharField(
        verbose_name='мера измерения',
        max_length=20
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='развесовка'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredients_recipe'
                )
        ]
    
    def __str__(self) -> str:
        return  f'{self.ingredient.name} - {self.amount}'

class Shopping_cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name=' shopping cart',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart_user'
                )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
                )
        ]

    def __str__(self):
        return self.user