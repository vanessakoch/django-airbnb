from django.test import TestCase
from airbnb.forms import ReserveForm, CommentForm, SearchForm

class ReserveFormTestCase(TestCase):
    
    def test_form_reserve_home(self):
        form = ReserveForm({
            'initial_date': '20/10/2020',
            'final_date': '30/10/2020',
            'number_peoples': 5
        })
        self.assertTrue(form.is_valid())

    def test_blank_data_reserve_home(self):
        form = ReserveForm({
            'final_date': "10/10/2020",
            'number_peoples': 2,
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'initial_date': ['Este campo é obrigatório.'],
        })

class CommentFormTestCase(TestCase):

    def test_form_comment_home(self):
        form = CommentForm({
            'author': 'Vanessa',
            'text': 'Some text'
        })
        self.assertTrue(form.is_valid())

    def test_blank_data_comment_home(self):
        form = CommentForm({})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'text': ['Este campo é obrigatório.'],
            'author': ['Este campo é obrigatório.'],
        })

class SearchFormTestCase(TestCase):
    def test_form_search_home(self):
        form = SearchForm({
            'local': 'Canoinhas',
            'number_of_days': 10,
            'number_of_peoples': 2
        })
        self.assertTrue(form.is_valid())

    def test_blank_data_search_home(self):
        form = SearchForm({})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'local': ['Este campo é obrigatório.'],
            'number_of_days': ['Este campo é obrigatório.'],
            'number_of_peoples': ['Este campo é obrigatório.'],
        })