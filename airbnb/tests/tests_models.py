import datetime

from django.test import TestCase
from django.utils import timezone
from users.models import CustomUser
from blog.models import Post, PostLike, PostDislike, PostComment
from airbnb.models import Home, Address, Reserve, Comment, Rating, Search

class HomeTestCase(TestCase):
    
    def setUp(self):
        Address.objects.create(
            country = "Brasil",
            zipcode = "89444000",
            state = "Santa Catarina",
            city = "Canoinhas",
            street = "Paula Pereira",
            phone = "36220000"
        )

        CustomUser.objects.create(
            username = "Admin",
            email = "admin@gmail.com",
            birth_date ="1970-10-10",
            password = "123987456"
        )

        Home.objects.create(
            owner = CustomUser.objects.get(username="Admin"), 
            image = "../static/img/img_notfound.png",
            name = "Hotel Canoinhas",
            description = "O melhor lugar para sua família",
            price = "545.00",
            created_date = timezone.now(),
            address = Address.objects.get(street="Paula Pereira", phone="36220000"),
        )


    def test_home_is_published(self):
        home = Home.objects.get(name='Hotel Canoinhas')
        self.assertIsNone(home.published_date, None)

    def test_create_address_and_home(self):
        address = Address.objects.get(street="Paula Pereira", phone="36220000")
        home = Home.objects.get(name='Hotel Canoinhas')

        self.assertEqual(home.address.city, 'Canoinhas')
        self.assertEqual(home.address.state, 'Santa Catarina')

    def test_create_user_home(self):
        home = Home.objects.get(name='Hotel Canoinhas')
        self.assertEqual(home.owner.email, 'admin@gmail.com')

    def test_set_home_publish(self):
        home = Home.objects.get(name='Hotel Canoinhas')
        home.publish()
        self.assertIsNotNone(home.published_date)

    def test_reserve_home(self):
        reserve = Reserve.objects.create(
            home = Home.objects.get(name="Hotel Canoinhas"),
            user = CustomUser.objects.get(username="Admin"),
            initial_date = timezone.now(),
            final_date = timezone.now() + datetime.timedelta(days=4),
            number_peoples = 3,
            total_value = 0
        )

        reserve.set_total_value()
        self.assertEqual(reserve.total_value, 6540.00)

    def test_rating_home(self):
        rating = Rating.objects.create(
            home= Home.objects.get(name='Hotel Canoinhas'),
            user= CustomUser.objects.get(username="Admin"),
            stars= 4
        )

        self.assertEqual(rating.stars, 4)

    def test_existing_local_search(self):
        search = Search.objects.create(
            user = CustomUser.objects.get(username="Admin"),
            local = "Canoinhas",
            number_of_days = 5,
            number_of_peoples = 2,
        )

        second_search = Search.objects.create(
            user = CustomUser.objects.get(username="Admin"),
            local = "Mafra",
            number_of_days = 20,
            number_of_peoples = 4,
        )

        search_filter_one = Home.objects.filter(address__city = search.local).count()
        search_filter_two = Home.objects.filter(address__city = second_search.local).count()

        self.assertGreater(search_filter_one, 0)
        self.assertAlmostEqual(search_filter_two, 0)

    def test_comment_home(self):
        comment = Comment.objects.create(
            home = Home.objects.get(name='Hotel Canoinhas'),
            author = "Vanessa",
            text = "Novo comentário",
            created_date = timezone.now()
        )

        self.assertIs(comment.approved_comment, False)
        comment.approve()
        self.assertIs(comment.approved_comment, True)

class BlogTestCase(TestCase):

    def setUp(self):

        CustomUser.objects.create(
            username = "Vanessa",
            email = "vanessa@gmail.com",
            birth_date ="1992-10-15",
            password = "123987456"
        )

        Post.objects.create(
            author = CustomUser.objects.get(username="Vanessa"),
            title = "Blog",
            text = "Novo comentário",
            created_date = timezone.now(),
            published_date = timezone.now()
        )

        Post.objects.create(
            author = CustomUser.objects.get(username="Vanessa"),
            title = "Segundo",
            text = "Mais um comentário",
            created_date = timezone.now(),
            published_date = timezone.now()
        )

    def test_create_post_blog(self):
        post = Post.objects.get(title="Blog")

        self.assertIs(post.views, 0)
        self.assertIs(post.likes_count(), 0)
        self.assertIs(post.dislikes_count(), 0)
        self.assertIs(post.approved_comments().count(), 0)

    def test_like_post_blog(self):
        like = PostLike.objects.create(
            user = CustomUser.objects.get(username="Vanessa"),
            post = Post.objects.get(title = "Blog"),
            created_date = timezone.now()
        )

        self.assertGreater(like.post.likes_count(),0)

    def test_dislike_post_blog(self):
        dislike = PostDislike.objects.create(
            user = CustomUser.objects.get(username="Vanessa"),
            post = Post.objects.get(title = "Segundo"),
            created_date = timezone.now()
        )
        
        self.assertGreater(dislike.post.dislikes_count(), 0)

        
    def test_create_comment_post_blog(self):
        comment_post = PostComment.objects.create(
            post = Post.objects.get(title="Segundo"),
            author = "Maria",
            text = "Novo texto do post",
        )

        self.assertFalse(comment_post.approved_comment)
        self.assertEqual(comment_post.post.approved_comments().count(), 0)

        comment_post.approve()

        self.assertTrue(comment_post.approved_comment)
        self.assertEqual(comment_post.post.approved_comments().count(), 1)
