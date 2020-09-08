from django.contrib import admin
from rest_framework import routers
from django.urls import path, include
from api import views
from django.conf.urls import include, url, re_path

from django.conf import settings
from django.conf.urls.static import static

router = routers.SimpleRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'skills', views.SkillViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'requests', views.RequestViewSet)
router.register(r'ratings', views.RatingViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'proposals', views.ProposalViewSet)
router.register(r'pictures', views.PictureViewSet)
router.register(r'files', views.ProjectFileViewSet)
router.register(r'favorites', views.FollowerViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'projectStages', views.ProjectStageViewSet)
router.register(r'projectJournal', views.ProjectJournalViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'kanban', views.KbCardViewSet)

slashless_router = routers.SimpleRouter(trailing_slash=False)
slashless_router.registry = router.registry[:]

urlpatterns = [
    url(r'admin/', admin.site.urls),
#     path('chat/', include('chat.urls')),
    url(r'^', include(router.urls)),
    url(r'^', include(slashless_router.urls)),
    re_path(r'login\/?$', views.user.login, name='login'),
    re_path(r'logout\/?$', views.user.logout, name='logout'),
    re_path(r'register\/?$', views.user.register, name='register'),
    re_path(r'registerConfirmation\/?$', views.user.register_confirmation, name='register_confirmation'),
    re_path(r'registerSendConfirmation\/?$', views.user.register_mail_send, name='register_confirmation_resend_email'),
    re_path(r'loadUser\/?$', views.user.loadUser, name='loadUser'),
    re_path(r'loadHeader\/?$', views.user.loadHeader, name='loadHeader'),
    re_path(r'registerProject\/?$', views.project.registerProject,
            name='registerProject'),
    re_path(r'registerService\/?$', views.service.registerService,
            name='registerService'),
    re_path(r'inviteService\/?$', views.service.inviteService,
            name='inviteService'),
    re_path(r'resetPassword\/?$', views.user.reset_password,
            name='reset_password'),
    re_path(r'changePassword\/?$', views.user.change_password,
            name='change_Password'),
    re_path(r'changePasswordRecovery\/?$', views.user.change_password_recovery,
            name='change_password_recovery'),
    re_path(r'tbkInit\/?$', views.transbank.initTransaction,
            name='start_transaction'),
    re_path(r'tbkNormal\/?$', views.transbank.normal_return_webpay,
            name='normal_transaction'),
    re_path(r'tbkFinal\/?$', views.transbank.normal_final,
            name='final_transaction'),
#     re_path(r'testing\/?$', views.transbank.testing,
#             name='final_transaction'),
    re_path(r'changeBoard\/?$', views.kb_card.changeBoard,
            name='change_board')



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
