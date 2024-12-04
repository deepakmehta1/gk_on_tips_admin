from django.core.management.base import BaseCommand
from book.models import Book, Unit, SubUnit, Question, Choice
from book.openai_utils import generate_mcqs


class Command(BaseCommand):
    help = "Generates 10 MCQs for a specific subunit or all subunits within a unit using OpenAI API"

    def add_arguments(self, parser):
        # Required positional arguments
        parser.add_argument("book_id", type=int, help="The ID of the book")
        parser.add_argument("unit_id", type=int, help="The ID of the unit")

        # Optional keyword argument for subunit
        parser.add_argument(
            "--sub_unit_id", type=int, help="The ID of the subunit (optional)"
        )

    def handle(self, *args, **kwargs):
        book_id = kwargs["book_id"]
        unit_id = kwargs["unit_id"]
        sub_unit_id = kwargs.get("sub_unit_id", None)

        # Retrieve the book and unit objects, or return error if not found
        book = self.get_object_or_none(Book, book_id)
        if not book:
            self.stdout.write(f"Error: Book with ID {book_id} not found.\n")
            return

        unit = self.get_object_or_none(Unit, unit_id, book=book)
        if not unit:
            self.stdout.write(
                f"Error: Unit with ID {unit_id} not found in Book ID {book_id}.\n"
            )
            return

        # Handle generation for a specific subunit or all subunits
        if sub_unit_id:
            subunit = self.get_object_or_none(SubUnit, sub_unit_id, unit=unit)
            if subunit:
                self.generate_mcqs_for_subunit(subunit)
            else:
                self.stdout.write(
                    f"Error: SubUnit with ID {sub_unit_id} not found in Unit ID {unit_id}.\n"
                )
        else:
            subunits = SubUnit.objects.filter(unit=unit)
            self.stdout.write(
                f"Generating questions for all SubUnits in Unit: {unit.title_en} - {unit.title_hi}\n"
            )
            total_questions_created = 0
            for subunit in subunits:
                self.stdout.write(
                    f"Generating questions for SubUnit: {subunit.title_en}\n"
                )
                total_questions_created += self.generate_mcqs_for_subunit(subunit)
            self.stdout.write(
                f"Generated {total_questions_created} questions for all subunits in Unit {unit.title_en}.\n"
            )

    def get_object_or_none(self, model, object_id, **filters):
        """Helper method to get object or return None if not found"""
        try:
            return model.objects.get(id=object_id, **filters)
        except model.DoesNotExist:
            return None

    def generate_mcqs_for_subunit(self, subunit):
        """Helper function to generate MCQs and store them"""
        mcqs = generate_mcqs(subunit.content_en)
        if not mcqs:
            self.stdout.write(
                f"No questions generated for SubUnit: {subunit.title_en}\n"
            )
            return 0  # No questions generated

        # Create questions and choices
        total_questions = 0
        for mcq in mcqs:
            question = Question.objects.create(
                subunit=subunit, text_en=mcq["text_en"], text_hi=mcq["text_hi"]
            )
            for choice in mcq["choices"]:
                Choice.objects.create(
                    question=question,
                    text_en=choice["text_en"],
                    text_hi=choice["text_hi"],
                    is_correct=choice["is_correct"],
                )
            total_questions += 1
        return total_questions
