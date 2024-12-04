from django.contrib import admin
from .models import Book, Unit, SubUnit, Question, Choice, ReportedQuestion


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
    list_display = ["title_en", "title_hi"]
    search_fields = ["title_en", "title_hi"]
    inlines = [UnitInline]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ["title_en", "title_hi", "book"]
    search_fields = ["title_en", "title_hi"]
    inlines = [SubUnitInline]


@admin.register(SubUnit)
class SubUnitAdmin(admin.ModelAdmin):
    list_display = ["title_en", "title_hi", "unit"]
    search_fields = ["title_en", "title_hi"]
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["text_en", "text_hi", "subunit", "active", "reported"]
    search_fields = ["text_en", "text_hi"]
    list_filter = ["active", "reported"]  # Allows filtering by active/reported status
    list_editable = [
        "active",
        "reported",
    ]  # Makes active and reported editable from the list view
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["text_en", "text_hi", "is_correct", "question"]
    search_fields = ["text_en", "text_hi"]


@admin.register(ReportedQuestion)
class ReportedQuestionAdmin(admin.ModelAdmin):
    list_display = ["question", "explanation_en", "explanation_hi", "resolved"]
    search_fields = [
        "question__text_en",
        "question__text_hi",
        "explanation_en",
        "explanation_hi",
    ]
    list_filter = ["resolved"]  # Allows filtering by resolved status
    list_editable = ["resolved"]  # Makes resolved editable from the list view
