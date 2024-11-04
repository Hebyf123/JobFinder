from django.conf import settings
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Resume, Skill,EmployerOffer, Education, Job, Language, FavoriteJob, SentResume, JobCategory, JobSubCategory
from .serializers import ResumeSerializer, LanguageSerializer,WorkFormatSerializer,WorkTypeSerializer,CompanyTypeSerializer,SkillSerializer,JobSerializer,EmployerOfferSerializer, EducationSerializer, JobSerializer, LanguageSerializer, FavoriteJobSerializer, SentResumeSerializer, JobCategorySerializer, JobSubCategorySerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .models import FavoriteWorker,WorkFormat,WorkType,CompanyType
from .serializers import FavoriteWorkerSerializer
from .tasks import send_notification_email  
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import JobSerializer
from .filters import JobFilter
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
class EmployerOfferViewSet(viewsets.ModelViewSet):
    queryset = EmployerOffer.objects.all()
    serializer_class = EmployerOfferSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return EmployerOffer.objects.filter(employer=user)

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)
class JobModerationView(APIView):
    #permission_classes = [permissions.IsAdminUser] 

    def get(self, request, *args, **kwargs):

        jobs = Job.objects.filter(status='pending')
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        job_id = request.data.get('job_id')
        status = request.data.get('status')
        comment = request.data.get('comment')

        job = get_object_or_404(Job, id=job_id)
        if status not in Job.STATUS_CHOICES:
            return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        job.status = status
        job.moderation_comment = comment
        job.save()

        serializer = JobSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)
class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_view_count()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def list_by_user(self, request, user_id=None):  
        user = get_object_or_404(User, id=user_id)
        resumes = Resume.objects.filter(user=user)
        serializer = self.get_serializer(resumes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        skills = request.data.get('skills', [])
        resume = Resume.objects.create(
            user=request.user,
            phone=request.data.get('phone'),
            email=request.data.get('email'),
            linkedin=request.data.get('linkedin'),
            experience_years=request.data.get('experience_years'),
            preferred_city=request.data.get('preferred_city'),
            birth_date=request.data.get('birth_date'),
            salary_range_min=request.data.get('salary_range_min'),
            salary_range_max=request.data.get('salary_range_max'),
            resume_file=request.data.get('resume_file'),
            work_type=request.data.get('work_type'),
            work_format=request.data.get('work_format'),
        )

        resume.skills.set(skills)
        return Response({'status': 'Resume created successfully'}, status=status.HTTP_201_CREATED)

class JobCategoryViewSet(viewsets.ModelViewSet):

    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']  
    permission_classes = [AllowAny]

class JobSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = JobSubCategory.objects.all()
    serializer_class = JobSubCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']  
    permission_classes = [AllowAny]

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filterset_fields = ['id']  
    permission_classes = [AllowAny]
class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    filterset_fields = ['id']  
    permission_classes = [AllowAny]
class WorkFormatViewSet(viewsets.ModelViewSet):
    queryset = WorkFormat.objects.all()
    serializer_class = WorkFormatSerializer
    filterset_fields = ['id']  
    permission_classes = [AllowAny]
class  WorkTypeViewSet(viewsets.ModelViewSet):
    queryset = WorkType.objects.all()
    serializer_class = WorkTypeSerializer
    filterset_fields = ['id']  
    permission_classes = [AllowAny]
class CompanyTypeViewSet(viewsets.ModelViewSet):
    queryset = CompanyType.objects.all()
    serializer_class = CompanyTypeSerializer
    filterset_fields = ['id']  
    permission_classes = [AllowAny]
class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    filterset_fields = ['id']  
    permission_classes = [AllowAny]



class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = JobFilter
    ordering_fields = '__all__'
    ordering = ['-view_count']  
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.increment_view_count() 

            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response({'detail': 'Job not found.'}, status=status.HTTP_404_NOT_FOUND)
    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def list_by_user(self, request, user_id=None):
        user = get_object_or_404(User, id=user_id)
        jobs = Job.objects.filter(user=user)
        serializer = self.get_serializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FavoriteJobViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteJobSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return FavoriteJob.objects.filter(user=self.request.user)
        else:
            return FavoriteJob.objects.none() 

    def perform_create(self, serializer):
        
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"detail": "Вы не можете удалить эту вакансию из избранного."}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)



class FavoriteWorkerViewSet(viewsets.ModelViewSet):
    queryset = FavoriteWorker.objects.all()
    serializer_class = FavoriteWorkerSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return FavoriteWorker.objects.filter(employer=self.request.user)  
        else:
            return FavoriteWorker.objects.none()

    def perform_create(self, serializer):

        serializer.save(employer=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.employer != request.user:
            return Response({"detail": "Вы не можете удалить этого работника из избранного."}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
class SentResumeViewSet(viewsets.ModelViewSet):
    queryset = SentResume.objects.all()
    serializer_class = SentResumeSerializer
    #permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def resumes_sent(self, request):
        """Показать все резюме, отправленные текущим работником"""
        resumes = SentResume.objects.filter(user=request.user)
        serializer = self.get_serializer(resumes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def resumes_received(self, request):
        jobs = [offer.job for offer in EmployerOffer.objects.filter(employer=request.user)]
        resumes = SentResume.objects.filter(job__in=jobs)
        serializer = self.get_serializer(resumes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def send_resume(self, request):
        job_id = request.data.get('job')
        resume_id = request.data.get('resume')

        job = get_object_or_404(Job, id=job_id)
        resume = get_object_or_404(Resume, id=resume_id)

        
        if resume.user != request.user:
            return Response({'detail': 'You can only send your own resume.'}, status=403)

       
        sent_resume, created = SentResume.objects.get_or_create(user=request.user, job=job, resume=resume)

        if not created:
            return Response({'detail': 'You have already sent this resume for this job.'}, status=400)

        return Response({'status': 'Resume sent successfully!'}, status=201)
class EmployerOfferViewSet(viewsets.ModelViewSet):
    queryset = EmployerOffer.objects.all()
    serializer_class = EmployerOfferSerializer
    #permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def offers_sent(self, request):
        if not hasattr(request.user, 'employer_offers'):
            return Response({'detail': 'Not allowed'}, status=403)
        offers = EmployerOffer.objects.filter(employer=request.user)
        serializer = self.get_serializer(offers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def offers_received(self, request):
        if not hasattr(request.user, 'worker_offers'):
            return Response({'detail': 'Not allowed'}, status=403)
        offers = EmployerOffer.objects.filter(worker=request.user)
        serializer = self.get_serializer(offers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_offer(self, request):
        serializer = EmployerOfferSerializer(data=request.data)
        if serializer.is_valid():
            if not hasattr(request.user, 'employer_offers'):
                return Response({'detail': 'Not allowed'}, status=403)
    
            serializer.save(employer=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
