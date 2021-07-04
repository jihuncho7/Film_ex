from django.urls import path, include
from django.views.generic import TemplateView
from film import views
from .views import *
from rest_framework import routers
# -- Film의 view 와 멥핑해 주는 곳 -----------------

app_name = 'film'

router = routers.DefaultRouter()
# film review
router.register('FilmOrderbyRate',FilmOrderbyRateViewSet)
router.register('FilmEditorChoice',FilmEditorChoiceViewSet)
router.register('FilmOnStreaming',FilmOnStreamingViewSet)
# freeboard
router.register('freeboard',FreeBoardViewSet)
# hire post
router.register('hirepoststaff',HirePostStaffViewSet)
router.register('hirepostactor',HirePostActorViewSet)
# Resume
router.register('resumestaff',ResumeStaffViewSet)
router.register('resumeactor',ResumeActorViewSet)
router.register('resumestaffboard',ResumeStaffBoard)
router.register('resumeactorboard',ResumeActorBoard)

# QnA
router.register('qna',QnAViewSet)
# Comments
router.register('comment/film',CommentViewset)
router.register('comment/film/in',CommentInCommmentViewset)
router.register('comment/freeboard',CommentFreeBoardViewset)
router.register('comment/freeboard/in',CommentInCommmentFreeBoardViewset)
router.register('comment/hirepoststaff',CommentHirePostStaffViewset)
router.register('comment/hirepoststaff/in',CommentInCommentHirePostStaffViewset)
router.register('comment/hirepostactor',CommentHirePostActorViewset)
router.register('comment/hirepostactor/in',CommentInCommentHirePostActorViewset)


urlpatterns = [
    path(r'',include(router.urls)),
    path('homebanner/', Home_banner.as_view(), name='homebanner'),
    path('HirePostStaff_imgfilter/', HirePostStaff_imgfilter.as_view(), name='HirePostStaff_imgfilter'),
    path('MypageApplied', MypageApplied.as_view(), name='MypageApplied'),
    path('WrittenByMe', WrittenByMe.as_view(), name='WrittenByMe'),
    path('CountLikedPost', CountLikedPost.as_view(), name='CountLikedPost'),
    path('CountAllPost', CountAllPost.as_view(), name='CountAllPost'),
    path('SearchAllView', SearchAllView.as_view(), name='SearchAllView'),
    # path('SearchAll', SearchAll.as_view(), name='SearchAll'),

    #path('review/', views.review, name='review'),
]
