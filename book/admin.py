from django.contrib import admin
from .models import Book, Unit, SubUnit, Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  # You can define how many extra choices should appear

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3

class SubUnitInline(admin.TabularInline):
    model = SubUnit
    extra = 3

class UnitInline(admin.TabularInline):
    model = Unit
    extra = 3

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_hi']
    search_fields = ['title_en', 'title_hi']
    inlines = [UnitInline]

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_hi', 'book']
    search_fields = ['title_en', 'title_hi']
    inlines = [SubUnitInline]

@admin.register(SubUnit)
class SubUnitAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_hi', 'unit']
    search_fields = ['title_en', 'title_hi']
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text_en', 'text_hi', 'subunit']
    search_fields = ['text_en', 'text_hi']
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text_en', 'text_hi', 'is_correct', 'question']
    search_fields = ['text_en', 'text_hi']
