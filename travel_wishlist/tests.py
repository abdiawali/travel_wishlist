from django.test import TestCase
from django.urls import reverse
from .models import Place

class TestHomePage(TestCase):

    def test_home_page_shows_empty_list_message_for_empty_db(self):
        home_page_url = reverse('place_list')
        response = self.client.get(home_page_url)
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'You have no places in your wishlist')

class TestWishList(TestCase):
    fixtures = ['test_places']

    def test_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')

class TestVisitedPage(TestCase):

    def test_visited_page_shows_empty_list_message_for_empty_db(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'You have not visited any places yet')

class visited_list(TestCase):

    fixtures = ['test_places']

    def test_visited_list_shows_visited_places(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'San Francisco')
        self.assertContains(response, 'Moab')
        self.assertNotContains(response, 'New York')
        self.assertNotContains(response, 'Tokyo')

class Test_add_new_place(TestCase):
    def test_add_new_unvisited_place(self):
        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Tokyo', 'visited': False}

        response = self.client.post(add_place_url, new_place_data, follow=True)

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        response_place = response.context['places']
        self.assertEqual(1, len(response_place))
        tokyo_from_response = response_place[0]

        tokyo_from_db = Place.objects.get(name='Tokyo', visited=False)
        
        self.assertEqual(tokyo_from_db, tokyo_from_response)

class Test_visited_place(TestCase):

    fixtures = ['test_places']

    def test_visit_place(self):
        visit_place_url = reverse('place_was_visited', args=(2,))
        response = self.client.post(visit_place_url, follow=True)

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertNotContains(response, 'New York')
        self.assertContains(response, 'Tokyo')

        new_york = Place.objects.get(pk=2)
        self.assertTrue(new_york.visited)

    def test_non_existent_place(self):
        visit_non_existent_place_url = reverse('place_was_visited', args=(500,))
        response = self.client.post(visit_non_existent_place_url, follow=True)

        self.assertEqual(404, response.status_code)