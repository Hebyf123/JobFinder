from rest_framework import serializers
from .models import Resume, Skill,EmployerOffer,FavoriteWorker, WorkType,WorkFormat,Education,CompanyType, WORK_TYPES_CHOICES,Job, Language, FavoriteJob, SentResume, JobCategory, JobSubCategory
from django.contrib.auth import get_user_model
class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = '__all__'
class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = ['name']

class WorkFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkFormat
        fields = ['name']

class CompanyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyType
        fields = ['name']
class JobSubCategorySerializer(serializers.ModelSerializer):
    category = JobCategorySerializer(read_only=True)

    class Meta:
        model = JobSubCategory
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'



class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class ResumeSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)
    education = serializers.PrimaryKeyRelatedField(queryset=Education.objects.all(), many=True)
    languages = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), many=True)
    view_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Resume
        fields = '__all__'

    def create(self, validated_data):
        skills = validated_data.pop('skills', [])
        resume = Resume.objects.create(**validated_data)
        resume.skills.set(skills)
        return resume

    def update(self, instance, validated_data):
        skills = validated_data.pop('skills', [])
        instance.skills.set(skills)
        return super().update(instance, validated_data)

class JobSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)
    category = serializers.PrimaryKeyRelatedField(queryset=JobCategory.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=JobSubCategory.objects.all())  
    education_levels = serializers.PrimaryKeyRelatedField(queryset=Education.objects.all(), many=True)
    languages = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), many=True)
    status = serializers.ChoiceField(choices=Job.STATUS_CHOICES)
    type = serializers.PrimaryKeyRelatedField(queryset=CompanyType.objects.all(), many=True)
    work_type = serializers.PrimaryKeyRelatedField(queryset=WorkType.objects.all(), many=True)
    work_format = serializers.PrimaryKeyRelatedField(queryset=WorkFormat.objects.all(), many=True)
    
    class Meta:
        model = Job
        fields = '__all__'
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    category_id = self.initial_data.get('category') if 'initial_data' in kwargs else None
    #    print(f"Received category_id: {category_id}")  # Добавьте это для отладки
    #    if category_id:
    #        try:
    #            self.fields['subcategory'].queryset = JobSubCategory.objects.filter(category_id=category_id)
    #            print(f"Set subcategory queryset: {self.fields['subcategory'].queryset}")  # Добавьте это для отладки
    #        except (KeyError, ValueError):
    #            pass

    def create(self, validated_data):
        skills = validated_data.pop('skills', [])
        education_levels = validated_data.pop('education_levels', [])
        languages = validated_data.pop('languages', [])
        work_type_data = validated_data.pop('work_type', [])
        work_format_data = validated_data.pop('work_format', [])
        company_type_data = validated_data.pop('type', [])  

        category_data = validated_data.pop('category', None)
        subcategory_data = validated_data.pop('subcategory', None)

        job = Job.objects.create(**validated_data, category=category_data, subcategory=subcategory_data)

        job.skills.set(skills)
        job.education_levels.set(education_levels)
        job.languages.set(languages)
        job.work_type.set(work_type_data)
        job.work_format.set(work_format_data)
        job.type.set(company_type_data)

        return job

    def update(self, instance, validated_data):
        skills = validated_data.pop('skills', [])
        education_levels = validated_data.pop('education_levels', [])
        languages = validated_data.pop('languages', [])
        work_type_data = validated_data.pop('work_type', [])
        work_format_data = validated_data.pop('work_format', [])
        company_type_data = validated_data.pop('type', [])  

        
        category_data = validated_data.pop('category', None)
        subcategory_data = validated_data.pop('subcategory', None)

        
        if category_data:
            instance.category = category_data
        if subcategory_data:
            instance.subcategory = subcategory_data

        instance.skills.set(skills)
        instance.education_levels.set(education_levels)
        instance.languages.set(languages)
        instance.work_type.set(work_type_data)
        instance.work_format.set(work_format_data)
        instance.type.set(company_type_data)

        return super().update(instance, validated_data)



class FavoriteWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteWorker
        fields = ['employer', 'worker']

class FavoriteJobSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)

    class Meta:
        model = FavoriteJob
        fields = '__all__'
class SentResumeSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    resume_title = serializers.CharField(source='resume.title', read_only=True)

    class Meta:
        model = SentResume
        fields = ['id', 'user', 'user_username', 'job', 'job_title', 'resume', 'resume_title']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
class EmployerOfferSerializer(serializers.ModelSerializer):
    employer_username = serializers.CharField(source='employer.username', read_only=True)
    worker_username = serializers.CharField(source='worker.username', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)

    class Meta:
        model = EmployerOffer
        fields = ['id', 'employer', 'employer_username', 'worker', 'worker_username', 'job', 'job_title', 'created_at']
        read_only_fields = ['employer', 'created_at']

    def create(self, validated_data):
        validated_data['employer'] = self.context['request'].user
        return super().create(validated_data)