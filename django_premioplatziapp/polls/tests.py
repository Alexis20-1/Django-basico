from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse
import datetime


from .models import Question

#testear modelos o vistas
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_questions(self):
        """was_published_recently return False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="Quien es el mejor course director de platzi",pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        
def create_question(question_text, days):
            """Create a question with a given "question_text", and published the given numer of days offset to now(negative for questions published in the past, 
            positive for questions that have yet to be published """
            time =timezone.now() + datetime.timedelta(days = days)
            return Question.objects.create(question_text=question_text, pub_date=time)
class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """if no questions exist, an appropiate message is returned"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        
    def test_future_question(self):
            """questions with a pub_date in the future are not displayed on the index page"""
            create_question("future questions", days=30)
            response = self.client.get(reverse("polls:index"))
            self.assertContains(response, "No polls are available")
            self.assertQuerysetEqual(response.context["latest_question_list"], [])
            
    def test_past_question(self):
            """questions wth a pub_date in the past are displayed on the index page"""
            question = create_question("Past questions", days=-10)
            response = self.client.get(reverse("polls:index"))
            self.assertQuerysetEqual(response.context["latest_question_list"], [question])
    def test_future_question_and_past_question(self):
        """Even if both past and future questions exit, only past questions are displayed"""
        past_question = create_question(question_text="past questions", days=-30)
        future_question = create_question(question_text="past questions", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question])
    def  test_two_past_question(self):
        """The questions index page my display multiple questions"""
        past_question1 = create_question(question_text="past questions1", days=-30)
        past_question2 = create_question(question_text="past questions2", days=-40)    
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question1, past_question2])
        
class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """THE DETAIL VIEW OF A QUESTION WITH A PUB_DATE IN THE FUTURE RETURNS A 404 ERROR NOT FOUND"""
        future_question = create_question(question_text="past questions", days=30)
        url = reverse("polls:detail", args =(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    def test_past_question(self):
        """The detail view od a question with pub_date in the past display the question text"""
        past_question = create_question(question_text="past questions", days=-30)
        url = reverse("polls:detail", args =(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response,past_question.question_text)