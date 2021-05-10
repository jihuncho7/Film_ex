import re
from django.conf import settings
from django.db import models
from django.urls import reverse

# 작성, 변경날짜
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# 영화 리뷰 페이지
class Film(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_post_set', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    url = models.URLField(blank=True)
    context = models.TextField()
    country = models.CharField(max_length=50)
    director = models.CharField(max_length=10)
    is_picked = models.BooleanField(default=False)
    on_streaming = models.BooleanField(default=False)
    genre_set = models.ManyToManyField('Genre', blank=True)
    tag_set = models.ManyToManyField('TagFilm', blank=True)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                           related_name='like_post_set')
    def __str__(self):
        return self.title

    def is_like_user(self, user): # TODO 나중에 user변수에 현재유저의 pk값을 대입하는 로직을 짜면 된다.

        return self.like_user_set.filter(pk=user.pk).exists()

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.context)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = TagFilm.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

    def get_absolute_url(self):
        return reverse("film:review_detail", args=[self.pk])

    def get_rate(self):
        rates = 0
        for comment in self.comment_set.all():
            rates += comment.rate
            return rates

    class Meta:
        ordering = ['-created_at']


# 태그 in 영화리뷰모델
class TagFilm(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# 장르 in 영화리뷰모델
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# 댓글 in 영화리뷰모델
class Comment(BaseModel):

    rate = models.IntegerField(default=1, choices=((i,i) for i in range(1,6)))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Film, on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        ordering = ['-id']

# 자유게시판
class FreeBoard(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.TextChoices('freeboardtype','질문 소식')
    title = models.CharField( max_length=50)
    context = models.TextField()
    image = models.ImageField(upload_to="freeboard/%Y/%m/%d",blank=True)

# 구인 스태프
class HirePostStaff(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thumbs = models.IntegerField(blank=True)
    category = models.TextChoices('poststafftype','영화 드라마 뮤직비디오 광고')
    title = models.CharField( max_length=50)
    image = models.ImageField(upload_to="HirePost/Staff/%Y/%m/%d",blank=True)
    company = models.CharField(max_length=20)
    company_loca = models.CharField( max_length=50,blank=True)
    company_desc = models.TextField()
    company_url = models.URLField(blank=True)
    job_position = models.CharField( max_length=50) # 카테고리 쓸지 고민
    detail = models.TextField()
    requirement = models.TextField()
    advantage = models.TextField(blank=True)
    job_loca = models.CharField(max_length=100,blank=True)
    deadline = models.DateTimeField()
    # 카테고리 시급,주급,일급,월급 초이스
    payment_category = models.TextChoices('paymenttype','시급 일급 주급 월급')
    payment = models.IntegerField()

    tag_set = models.ManyToManyField('TagPostStaff', blank=True)

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.context)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = TagPostStaff.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

# 태그 in 구인스태프
class TagPostStaff(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# 구인 액터
class HirePostActor(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thumbs = models.IntegerField()
    category = models.TextChoices('postacotortype','영화 드라마 뮤직비디오 광고')
    title = models.CharField( max_length=50)
    image = models.ImageField(upload_to="HirePost/Actor/%Y/%m/%d",blank=True)
    company = models.CharField(max_length=20)
    company_loca = models.CharField(max_length=50,blank=True)
    company_desc = models.TextField()
    company_url = models.URLField(blank=True)
    job_position = models.CharField(max_length=50)  # 카테고리 쓸지 고민
    detail = models.TextField()
    requirement = models.TextField()
    advantage = models.TextField(blank=True)
    job_loca = models.CharField(max_length=100, blank=True)
    deadline = models.DateTimeField()
    payment = models.IntegerField()
    tag_set = models.ManyToManyField('TagPostActor', blank=True)

    def __str__(self):
        return str(self.thumbs)

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.context)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = TagPostActor.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

# 태그 in 구인 액터
class TagPostActor(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# class Profile(BaseModel): 유저 프로필
#     nickname
#     name
#     image

# 이력서 스태프
class ResumeStaff(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.TextChoices('poststafftype','영화 드라마 뮤직비디오 광고')
    name = models.CharField(max_length=20)
    upload = models.FileField(blank=True)
    title = models.CharField( max_length=50)
    tel = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    context = models.TextField()
    # education TODO Workexp 와 동일한 고민
    #  prize TODO Workexp 와 동일한 고민
    # etc  TODO Workexp 와 동일한 고민
    category = models.TextChoices('resumestafftype', '촬영 연출 시나리오 음악\
                                                     편집 애니메이션 특수효과\
                                                     헤어-메이크업 미술 스턴트 외국어\
                                                     안무 경영지원 기타')
    resume_url = models.URLField(blank=True)
    tag_set = models.ManyToManyField('TagResumeStaff', blank=True)

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.context)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = TagResumeStaff.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

# 태그 in 이력서 스탭
class TagResumeStaff(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# class Workexp: TODO 따로 모델 뺄지 말지 고민하기 = 함수쓸지 클래스 추가할지
#     work_exp_date = models.DateField()
#     work_exp_where = models.CharField(max_length=50)
#     work_exp = models.TextField()

# 이력서 액터
class ResumeActor(BaseModel):## 액터스용
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.TextChoices('gendertype','여 남')
    # education
    # prize
    # etc
    resume_url = models.URLField(blank=True)
    context = models.TextField()
    agency = models.CharField(max_length=50, blank=True)
    category = models.TextChoices('resumeactortype','아역 청소년 성인 중장년')
    image = models.ImageField(upload_to="Resume/Actor/%Y/%m/%d")
    tag_set = models.ManyToManyField('TagResumeActor', blank=True)

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.context)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = TagResumeActor.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list
# 태그 in 이력서 액터
class TagResumeActor(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# QnA 모델
class QnA(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField()
    date = models.DateTimeField()
    context = models.TextField()
    is_done = models.BooleanField()
    upload = models.FileField(upload_to="Qna/%Y/%m/%d",blank=True) #TODO settings에 저장 디렉토리 검색하기
