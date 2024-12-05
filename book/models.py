from django.db import models


class Book(models.Model):
    title_en = models.CharField(max_length=255, verbose_name="Title in English")
    title_hi = models.CharField(max_length=255, verbose_name="Title in Hindi")

    class Meta:
        db_table = 'book'
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title_en


class Unit(models.Model):
    book = models.ForeignKey(
        Book, related_name="units", on_delete=models.CASCADE, verbose_name="Book"
    )
    title_en = models.CharField(max_length=255, verbose_name="Title in English")
    title_hi = models.CharField(max_length=255, verbose_name="Title in Hindi")
    unit_number = models.IntegerField(verbose_name="Unit Number")

    class Meta:
        db_table = 'unit'
        verbose_name = "Unit"
        verbose_name_plural = "Units"
        constraints = [
            models.UniqueConstraint(
                fields=["book", "unit_number"], name="unique_book_unit_number"
            )
        ]

    def __str__(self):
        return self.title_en


class SubUnit(models.Model):
    unit = models.ForeignKey(
        Unit, related_name="subunits", on_delete=models.CASCADE, verbose_name="Unit"
    )
    title_en = models.CharField(max_length=255, verbose_name="Title in English")
    title_hi = models.CharField(max_length=255, verbose_name="Title in Hindi")
    content_en = models.TextField(verbose_name="Content in English")
    content_hi = models.TextField(verbose_name="Content in Hindi")
    subunit_number = models.IntegerField(verbose_name="SubUnit Number")

    class Meta:
        db_table = 'sub_unit'
        verbose_name = "SubUnit"
        verbose_name_plural = "SubUnits"
        constraints = [
            models.UniqueConstraint(
                fields=["unit", "subunit_number"], name="unique_unit_subunit_number"
            )
        ]

    def __str__(self):
        return self.title_en


class Question(models.Model):
    subunit = models.ForeignKey(
        SubUnit,
        related_name="questions",
        on_delete=models.CASCADE,
        verbose_name="SubUnit",
    )
    text_en = models.TextField(verbose_name="Question Text in English")
    text_hi = models.TextField(verbose_name="Question Text in Hindi")
    active = models.BooleanField(default=True, verbose_name="Is Active")
    reported = models.BooleanField(default=False, verbose_name="Is Reported")

    class Meta:
        db_table = 'question'
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.text_en[:50]  # Display first 50 characters of the question


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        related_name="choices",
        on_delete=models.CASCADE,
        verbose_name="Question",
    )
    text_en = models.CharField(max_length=255, verbose_name="Choice Text in English")
    text_hi = models.CharField(max_length=255, verbose_name="Choice Text in Hindi")
    is_correct = models.BooleanField(verbose_name="Is Correct Choice")

    class Meta:
        db_table = 'choice'
        verbose_name = "Choice"
        verbose_name_plural = "Choices"

    def __str__(self):
        return self.text_en


class ReportedQuestion(models.Model):
    question = models.ForeignKey(
        Question,
        related_name="reported_questions",
        on_delete=models.CASCADE,
        verbose_name="Question",
    )
    explanation_en = models.TextField(verbose_name="Explanation in English")
    explanation_hi = models.TextField(verbose_name="Explanation in Hindi")
    resolved = models.BooleanField(default=False, verbose_name="Is Resolved")

    class Meta:
        db_table = 'reported_question'
        verbose_name = "Reported Question"
        verbose_name_plural = "Reported Questions"

    def __str__(self):
        return f"Reported: {self.question.text_en[:50]}"
