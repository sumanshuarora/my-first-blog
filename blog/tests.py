from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from .models import Post
from .forms import PostForm


class PostModelTest(TestCase):
    """Test cases for the Post model"""
    
    def setUp(self):
        """Set up test user and post"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            text='This is a test post content.',
            created_date=timezone.now()
        )
    
    def test_post_creation(self):
        """Test that a post can be created successfully"""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.text, 'This is a test post content.')
        self.assertEqual(self.post.author, self.user)
        self.assertIsNotNone(self.post.created_date)
        self.assertIsNone(self.post.published_date)
    
    def test_post_str_method(self):
        """Test the string representation of a post"""
        self.assertEqual(str(self.post), 'Test Post')
    
    def test_post_publish_method(self):
        """Test the publish method sets published_date"""
        self.assertIsNone(self.post.published_date)
        self.post.publish()
        self.assertIsNotNone(self.post.published_date)
        self.assertLessEqual(
            self.post.published_date,
            timezone.now()
        )


class PostFormTest(TestCase):
    """Test cases for the PostForm"""
    
    def test_post_form_valid_data(self):
        """Test form with valid data"""
        form = PostForm(data={
            'title': 'Test Title',
            'text': 'Test content for the post.'
        })
        self.assertTrue(form.is_valid())
    
    def test_post_form_missing_title(self):
        """Test form with missing title"""
        form = PostForm(data={
            'text': 'Test content without title.'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_post_form_missing_text(self):
        """Test form with missing text"""
        form = PostForm(data={
            'title': 'Test Title'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)
    
    def test_post_form_empty_data(self):
        """Test form with no data"""
        form = PostForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)


class PostListViewTest(TestCase):
    """Test cases for the post_list view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create published post
        self.published_post = Post.objects.create(
            author=self.user,
            title='Published Post',
            text='This post is published.',
            created_date=timezone.now(),
            published_date=timezone.now()
        )
        
        # Create unpublished post
        self.unpublished_post = Post.objects.create(
            author=self.user,
            title='Unpublished Post',
            text='This post is not published.',
            created_date=timezone.now()
        )
    
    def test_post_list_view_status_code(self):
        """Test that post list view returns 200"""
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_post_list_view_uses_correct_template(self):
        """Test that post list view uses correct template"""
        response = self.client.get(reverse('post_list'))
        self.assertTemplateUsed(response, 'blog/post_list.html')
    
    def test_post_list_shows_only_published_posts(self):
        """Test that only published posts appear in the list"""
        response = self.client.get(reverse('post_list'))
        self.assertContains(response, 'Published Post')
        self.assertNotContains(response, 'Unpublished Post')
    
    def test_post_list_view_context(self):
        """Test that post list view has correct context"""
        response = self.client.get(reverse('post_list'))
        self.assertTrue('posts' in response.context)
        self.assertEqual(len(response.context['posts']), 1)


class PostDetailViewTest(TestCase):
    """Test cases for the post_detail view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Detail Test Post',
            text='This is the post content.',
            created_date=timezone.now(),
            published_date=timezone.now()
        )
    
    def test_post_detail_view_status_code(self):
        """Test that post detail view returns 200"""
        response = self.client.get(
            reverse('post_detail', kwargs={'pk': self.post.pk})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_post_detail_view_uses_correct_template(self):
        """Test that post detail view uses correct template"""
        response = self.client.get(
            reverse('post_detail', kwargs={'pk': self.post.pk})
        )
        self.assertTemplateUsed(response, 'blog/post_detail.html')
    
    def test_post_detail_view_shows_correct_content(self):
        """Test that post detail shows correct content"""
        response = self.client.get(
            reverse('post_detail', kwargs={'pk': self.post.pk})
        )
        self.assertContains(response, 'Detail Test Post')
        self.assertContains(response, 'This is the post content.')
    
    def test_post_detail_view_nonexistent_post(self):
        """Test that accessing non-existent post returns 404"""
        response = self.client.get(
            reverse('post_detail', kwargs={'pk': 9999})
        )
        self.assertEqual(response.status_code, 404)


class PostNewViewTest(TestCase):
    """Test cases for the post_new view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_post_new_view_get_authenticated(self):
        """Test GET request to new post view when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_edit.html')
        self.assertIsInstance(response.context['form'], PostForm)
    
    def test_post_new_view_post_valid_data(self):
        """Test POST request with valid data creates a post"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('post_new'), {
            'title': 'New Test Post',
            'text': 'Content of the new post.'
        })
        
        # Check redirect
        self.assertEqual(response.status_code, 302)
        
        # Check post was created
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, 'New Test Post')
        self.assertEqual(post.author, self.user)
        self.assertIsNotNone(post.published_date)
    
    def test_post_new_view_post_invalid_data(self):
        """Test POST request with invalid data doesn't create post"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('post_new'), {
            'title': '',  # Empty title
            'text': 'Some content.'
        })
        
        # Should re-render form with errors
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 0)


class PostEditViewTest(TestCase):
    """Test cases for the post_edit view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Original Title',
            text='Original content.',
            created_date=timezone.now()
        )
    
    def test_post_edit_view_get_authenticated(self):
        """Test GET request to edit post view when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('post_edit', kwargs={'pk': self.post.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_edit.html')
        self.assertIsInstance(response.context['form'], PostForm)
    
    def test_post_edit_view_post_valid_data(self):
        """Test POST request with valid data updates the post"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('post_edit', kwargs={'pk': self.post.pk}),
            {
                'title': 'Updated Title',
                'text': 'Updated content.'
            }
        )
        
        # Check redirect
        self.assertEqual(response.status_code, 302)
        
        # Check post was updated
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
        self.assertEqual(self.post.text, 'Updated content.')
        self.assertIsNotNone(self.post.published_date)
    
    def test_post_edit_view_nonexistent_post(self):
        """Test editing non-existent post returns 404"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('post_edit', kwargs={'pk': 9999})
        )
        self.assertEqual(response.status_code, 404)


class URLTests(TestCase):
    """Test cases for URL routing"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='URL Test Post',
            text='Testing URLs.',
            created_date=timezone.now(),
            published_date=timezone.now()
        )
    
    def test_post_list_url_resolves(self):
        """Test that post list URL resolves correctly"""
        url = reverse('post_list')
        self.assertEqual(url, '/')
    
    def test_post_detail_url_resolves(self):
        """Test that post detail URL resolves correctly"""
        url = reverse('post_detail', kwargs={'pk': self.post.pk})
        self.assertEqual(url, f'/post/{self.post.pk}/')
    
    def test_post_new_url_resolves(self):
        """Test that post new URL resolves correctly"""
        url = reverse('post_new')
        self.assertEqual(url, '/post/new/')
    
    def test_post_edit_url_resolves(self):
        """Test that post edit URL resolves correctly"""
        url = reverse('post_edit', kwargs={'pk': self.post.pk})
        self.assertEqual(url, f'/post/{self.post.pk}/edit/')
