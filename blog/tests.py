from urllib import response
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post    

# Create your tests here.
class BlogTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testuser', email='testuser@email.com', password='password')

        cls.post =Post.objects.create(
            title='The Gaming Blog',
            body='This is going to be great',
            gamer=cls.user,
        )

    def test_post_model(self):
        self.assertEqual(self.post.title, 'The Gaming Blog')
        self.assertEqual(self.post.body, 'This is going to be great')
        self.assertEqual(self.post.gamer.username, 'testuser')
        self.assertEqual(str(self.post), 'The Gaming Blog')
        self.assertEqual(self.get_absolute_url(), '/post/1/')

    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get('/post/1/')
        self.assertEqual(response.status_code, 200)

    def test_post_listview(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is going to be great')
        self.assertTemplateUsed(response,'home.html')

    def test_post_detailview(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        no_response = self.client.get('/post/1000000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'The Gaming Blog')
        self.assertTemplateUsed(response,'post_detail.html')    