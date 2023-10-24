from django.test import TestCase
from django.contrib.auth.models import User
from app3d.models import Model3d, Badge, CustomUser
from django.urls import reverse
from django.utils import timezone


class DetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.model3d = Model3d.objects.create(user=self.user, views=999)
        self.badge_star = Badge.objects.create(name="Star", description="Le modèle d'un utilisateur a plus de 1k vues")
        self.badge_pioneer = Badge.objects.create(name="Pioneer", description="L'utilisateur est inscrit depuis plus d'un an")

    def test_detail_view_increase_views(self):
        self.client.force_login(self.user)
        url = reverse('detail', args=[self.model3d.id])
        response = self.client.get(url)
        
        self.model3d.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.model3d.views, 1000)  

    def test_detail_view_badge_star(self):
        self.client.force_login(self.user)
        self.model3d.views = 1000  
        self.model3d.save()

        url = reverse('detail', args=[self.model3d.id])
        response = self.client.get(url)

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.has_badge("Star"))  

    def test_detail_view_badge_pioneer(self):
        self.client.force_login(self.user)
        self.user.date_joined = timezone.now() - timezone.timedelta(days=366)  # Un an et un jour
        self.user.save()

        url = reverse('detail', args=[self.model3d.id])
        response = self.client.get(url)

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.has_badge("Pioneer"))  




class CustomUserTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.badge_star = Badge.objects.create(name="Star", description="Le modèle d'un utilisateur a plus de 1k vues")
        self.badge_pioneer = Badge.objects.create(name="Pioneer", description="L'utilisateur est inscrit depuis plus d'un an")

    def test_has_badge(self):
        # Vérifie que l'utilisateur n'a pas le badge "Star"
        self.assertFalse(self.user.has_badge("Star"))

        # Ajoute le badge "Star" à l'utilisateur
        self.user.badges.add(self.badge_star)

        # Vérifie que l'utilisateur a maintenant le badge "Star"
        self.assertTrue(self.user.has_badge("Star"))

    def test_is_pioneer(self):
        # Vérifie que l'utilisateur n'est pas un pionnier
        self.assertFalse(self.user.is_pioneer())

        # Modifie la date d'inscription de l'utilisateur pour qu'elle remonte à il y a plus d'un an
        one_year_ago = timezone.now() - timezone.timedelta(days=366)
        self.user.date_joined = one_year_ago
        self.user.save()

        self.assertTrue(self.user.is_pioneer())


# Create your tests here.

