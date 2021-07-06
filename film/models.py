import re
from django.conf import settings
from django.db import models
from django.urls import reverse


# 작성, 변경날짜
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hit = models.IntegerField(default=0)
    class Meta:
        abstract = True

class BaseModelExtend(BaseModel):
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                           related_name=f'like_{__qualname__}_set')

    def is_like_user(self, user):  # TODO 나중에 user변수에 현재유저의 pk값을 대입하는 로직을 짜면 된다.

        return self.like_user_set.filter(pk=user.pk).exists()

    def get_likes(self):

        return self.like_user_set.all().count()

# 영화 리뷰 페이지
class Film(BaseModelExtend):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_film_set', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    url = models.URLField(blank=True)
    context = models.TextField()
    country = models.CharField(max_length=50)
    director = models.CharField(max_length=10)
    actors = models.CharField(max_length=100,blank=True)
    staffs = models.CharField(max_length=100,blank=True)
    is_picked = models.BooleanField(default=False)
    on_streaming = models.BooleanField(default=False)
    grade = models.CharField(max_length=10)
    genre_set = models.ManyToManyField('Genre', blank=True)
    tag_set = models.ManyToManyField('TagFilm', blank=True)
    image = models.ImageField(upload_to="film/%Y/%m/%d", blank=True)
    def __str__(self):
        return self.title

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.context)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = TagFilm.objects.get_or_create(name=tag_name)
            tag_list.append(tag)

        self.tag_set.add(*tag_list) #TODO tag_set db에 넣는 쿼리 어디서처리할지? 일단 작동확인하기
        return tag_list

    def get_absolute_url(self):
        return reverse("film:review_detail", args=[self.pk])

    def get_rate(self):
        rates = 0
        for comment in self.Comment.all():
            rates += comment.rate
        if not isinstance(rates, int):
            rates = 0
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
    post = models.ForeignKey(Film, on_delete=models.CASCADE,related_name='Comment')
    message = models.TextField()

    class Meta:
        ordering = ['-id']

class CommentInComment(BaseModel):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='CommentInComment')
    message = models.TextField()

    class Meta:
        ordering = ['-id']

# 자유게시판
class FreeBoard(BaseModelExtend):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Choices = ('정보공유', '정보공유'),('일상', '일상'),('잡담', '잡담')
    category = models.CharField(max_length=10, choices=Choices)
    title = models.CharField( max_length=50)
    context = models.TextField()
    image = models.ImageField(upload_to="freeboard/%Y/%m/%d",blank=True)
    tag_set = models.ManyToManyField('TagFreeBoard',blank=True)

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)",self.context)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = TagFreeBoard.objects.get_or_create(name=tag_name)
            tag_list.append(tag_name)
        return tag_list

    class Meta:
        ordering = ['-created_at']

# 태그 in 자유게시판
class TagFreeBoard(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# 댓글 in 자유게시판
class CommentFreeBoard(BaseModel):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(FreeBoard, on_delete=models.CASCADE, related_name='CommentFreeBoard')
    message = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return '%d: %s' % (self.pk, self.message)

class CommentInCommentFreeBoard(BaseModel):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(CommentFreeBoard, on_delete=models.CASCADE, related_name='CommentInCommentFreeBoard')
    message = models.TextField()

    class Meta:
        ordering = ['-id']

# 구인 스태프
class HirePostStaff(BaseModelExtend):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authors')
    thumbs = models.IntegerField(blank=True,default=0)
    Choices = ('영화', '영화'), ('드라마', '드라마'), ('뮤직비디오', '뮤직비디오'), ('광고', '광고')
    category = models.CharField(max_length=10, choices=Choices)
    title = models.CharField( max_length=50)
    image = models.ImageField(upload_to="HirePost/Staff/image/%Y/%m/%d",blank=True)
    upload = models.FileField(upload_to="HirePost/Staff/upload/%Y/%m/%d",blank=True)
    company = models.CharField(max_length=20)
    company_loca = models.CharField( max_length=50,blank=True)
    company_desc = models.TextField()
    company_url = models.URLField(blank=True)
    job_position = models.CharField( max_length=50) # 카테고리 쓸지 고민
    context = models.TextField()
    requirement = models.TextField()
    advantage = models.TextField(blank=True)
    job_loca = models.CharField(max_length=100,blank=True)
    deadline = models.DateTimeField()
    manager = models.CharField(max_length=10)
    payment = models.IntegerField()

    # 카테고리 시급,주급,일급,월급 초이스
    Choices = ('시급', '시급'), ('일급', '일급'), ('주급', '주급'), ('월급', '월급')
    wage_choice = models.CharField(max_length=10, choices=Choices,blank=True)

    tag_set = models.ManyToManyField('TagPostStaff', blank=True)
    # 지원현황
    is_applied_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                           related_name='staff_is_applied_set')

    def is_applied_user(self, user):
        return self.is_applied_set.filter(pk=user.pk).exists()

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.context)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = TagPostStaff.objects.get_or_create(name=tag_name)
            tag_list.append(tag_name)
        return tag_list

    class Meta:
        ordering = ['-created_at']

# 태그 in 구인스태프
class TagPostStaff(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# 댓글 in 구인스태프
class CommentHirePostStaff(BaseModel):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(HirePostStaff, on_delete=models.CASCADE,related_name='CommentHirePostStaff')
    message = models.TextField()

    class Meta:
        ordering = ['-created_at']

class CommentInCommentHirePostStaff(BaseModel):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(CommentHirePostStaff, on_delete=models.CASCADE,related_name='CommentInCommentHirePostStaff')
    message = models.TextField()

    class Meta:
        ordering = ['-id']


# 구인 액터
class HirePostActor(BaseModelExtend):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thumbs = models.IntegerField()
    Choices = ('영화', '영화'), ('드라마', '드라마'), ('뮤직비디오', '뮤직비디오'), ('광고', '광고')
    category = models.CharField(max_length=10, choices=Choices)
    title = models.CharField( max_length=50)
    image = models.ImageField(upload_to="HirePost/Actor/image/%Y/%m/%d",blank=True)
    upload = models.FileField(upload_to="HirePost/Actor/%Y/upload/%m/%d",blank=True)
    company = models.CharField(max_length=20)
    company_loca = models.CharField(max_length=50,blank=True)
    company_desc = models.TextField()
    company_url = models.URLField(blank=True)
    job_position = models.CharField(max_length=50)  # 카테고리 쓸지 고민
    context = models.TextField()
    requirement = models.TextField()
    advantage = models.TextField(blank=True)
    job_loca = models.CharField(max_length=100, blank=True)
    deadline = models.DateTimeField()
    payment = models.IntegerField()
    manager = models.CharField(max_length=10)
    tag_set = models.ManyToManyField('TagPostActor', blank=True)

    # 지원현황
    is_applied_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                           related_name='actor_is_applied_set')

    def is_applied_user(self, user):
        return self.is_applied_set.filter(pk=user.pk).exists()

    def __str__(self):
        return self.title

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.context)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = TagPostActor.objects.get_or_create(name=tag_name)
            tag_list.append(tag_name)
        return tag_list

# 태그 in 구인 액터
class TagPostActor(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# 댓글 in 구인 액터
class CommentHirePostActor(BaseModel):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(HirePostActor, on_delete=models.CASCADE,related_name='CommentHirePostActor')
    message = models.TextField()

    class Meta:
        ordering = ['-created_at']

class CommentInCommentHirePostActor(BaseModel):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(CommentHirePostActor, on_delete=models.CASCADE,related_name='CommentInCommentHirePostActor')
    message = models.TextField()

    class Meta:
        ordering = ['-id']


# 이력서 스태프
class ResumeStaff(BaseModelExtend):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Choices = ('영화', '영화'), ('드라마', '드라마'), ('뮤직비디오', '뮤직비디오'), ('광고', '광고')
    category = models.CharField(max_length=10, choices=Choices)
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='Resume/Staff/image/%Y/%m/%d',blank=True)
    upload = models.FileField(blank=True, upload_to='Resume/Staff/upload/%Y/%m/%d')
    title = models.CharField( max_length=50)
    tel = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    context = models.TextField()
    Choices = ('촬영', '촬영'), ('연출', '연출'), ('시나리오', '시나리오'), ('음악', '음악'),
    ('편집', '편집'), ('애니메이션', '애니메이션'), ('특수효과', '특수효과'), ('헤어-메이크업', '헤어-메이크업'),
    ('미술', '미술'), ('스턴트', '스턴트'), ('외국어', '외국어'), ('안무', '안무'), ('경영지원', '경영지원'), ('기타', '기타')
    category = models.CharField(max_length=10, choices=Choices)
    resume_url = models.URLField(blank=True)
    tag_set = models.ManyToManyField('TagResumeStaff', blank=True)
    is_publish = models.BooleanField(default=False)
    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.context)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = TagResumeStaff.objects.get_or_create(name=tag_name)
            tag_list.append(tag_name)
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
class ResumeActor(BaseModelExtend):## 액터스용

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    height = models.IntegerField()
    gender_choices = ('남자', '남자'), ('여자', '여자')
    gender = models.CharField(max_length=4, choices=gender_choices)
    resume_url = models.URLField(blank=True)
    context = models.TextField()
    agency = models.CharField(max_length=50, blank=True)
    career = models.TextField(blank=True)
    category_choices = ('아역', '아역'), ('청소년', '청소년'), ('성인', '성인'), ('중장년', '중장년')
    category = models.CharField(max_length=10, choices=category_choices)
    image = models.ImageField(upload_to="Resume/Actor/image/%Y/%m/%d")
    upload = models.FileField(upload_to="Resume/Actor/upload/%Y/%m/%d",blank=True)
    tel = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    tag_set = models.ManyToManyField('TagResumeActor', blank=True)
    is_publish = models.BooleanField(default=False)
    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.context)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = TagResumeActor.objects.get_or_create(name=tag_name)
            tag_list.append(tag_name)
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
    upload = models.FileField(upload_to="Qna/%Y/%m/%d", blank=True)  # TODO settings에 저장 디렉토리 검색하기
