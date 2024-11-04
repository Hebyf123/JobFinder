from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from jobs.models import Job, Resume, FavoriteJob, SentResume, Notification
from jobs.serializers import ResumeSerializer, JobSerializer

User = get_user_model()

class JobAndResumeTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='password', email='user2@example.com')
        
        self.resume = Resume.objects.create(
            user=self.user1, phone='1234567890', email='user1@example.com', experience_years=3, 
            preferred_city='City', birth_date='1990-01-01', salary_range_min=50000, 
            salary_range_max=70000, work_type='fulltime', work_format='offline'
        )
        
        self.job = Job.objects.create(
            employer=self.user2, title="Job Title", description="Job Description", 
            required_experience=2, city="City", salary_min=30000, salary_max=60000, 
            work_type='fulltime', work_format='offline', status='approved'
        )

    def test_get_single_resume(self):
        """Тест получения одного резюме"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('resume-detail', kwargs={'pk': self.resume.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user1.id)

    def test_get_multiple_resumes(self):
        """Тест получения нескольких резюме"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('resume-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_add_job_to_favorites(self):
        """Тест добавления вакансии в избранное"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('favorite-jobs')
        data = {'job_id': self.job.id}  # Используйте 'job_id'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_send_resume_to_job(self):
        """Тест отправки резюме на вакансию"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('send-resume')
        data = {'user': self.user1.id, 'job': self.job.id, 'resume': self.resume.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_job_view_increment(self):
        """Тест увеличения просмотров вакансии"""
        #self.client.force_authenticate(user=self.user1)
        url = reverse('job-detail', kwargs={'pk': self.job.pk})
        response = self.client.get(url)
        self.job.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.job.view_count, 1)





