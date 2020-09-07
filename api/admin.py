from django.contrib import admin
from api.models import Category, Project, Service, Request, Skill, User, Rating, Proposal, Question, Notification, KbCard, ProjectFile, ProjectStage, LogTransbank
# Register your models here.

from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display=['id', 'email', 'name_and_last_name', 'username' ]
    list_display_links = ['email', 'name_and_last_name' ]
    # list_filter =['status', 'owner', 'created_at']
    search_fields = ['email', 'username']

    def name_and_last_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)


    class Meta:
        model=User

class InlineRequest(admin.TabularInline):
    model = Request
    extra = 1
    max_num = 1

class InlineKbCard(admin.TabularInline):
    model = KbCard
    extra = 1
    max_num = 7

class InlineProposal(admin.TabularInline):
    model = Proposal
    extra = 1
    max_muber = 1


class ProjectAdmin(admin.ModelAdmin):
    inlines = [InlineRequest, InlineKbCard]
    list_display=['id', 'title','status', 'owner', 'collaborator_id']
    list_display_links = ['title']
    list_editable = ['status' ]
    list_filter =['status', 'owner', 'created_at']
    search_fields = ['owner__email', 'title']

    def get_form(self, request, obj= None , **kwargs):
        if request.user.is_staff:
            self.exclude = ('collaborator_id', 'visits')
        return super(ProjectAdmin, self).get_form(request, obj=obj, **kwargs)

    class Meta:
        model=Project

class ServiceAdmin(admin.ModelAdmin):
    list_display=['id', 'title','status', 'owner']
    list_filter =['status', 'owner', 'created_at']
    search_fields = ['owner__email', 'title']

    class Meta:
        model=Service
    
# class RequestAdmin(admin.TabularInline):
#     model = Request
#     list_display=['id', 'status', 'emitter', 'invited']

class RequestAdmin(admin.ModelAdmin):
    inlines = [InlineProposal]
    list_display=['emitter','status', 'project', 'invited']
    list_filter =['project','emitter','status']
    search_fields = ['project__id', 'project__title', 'emitter__id', 'emitter__email']

    class Meta:
        model=Service


class ProposalAdmin(admin.ModelAdmin):
    list_display=['emitter', 'get_project', 'request', 'accepted' ]
    list_filter =['request', 'emitter']
    search_fields = ['request__project__id', 'request__project__title', 'emitter__id', 'emitter__email']

    def get_project(self, obj):
        return obj.request.project

    class Meta:
        model=Proposal


admin.site.site_header = 'Panel de Administrador Te Necesito'
admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Question)
admin.site.register(Request, RequestAdmin)
admin.site.register(Proposal, ProposalAdmin)
admin.site.register(Rating)
admin.site.register(Notification)
admin.site.register(ProjectFile)
admin.site.register(KbCard)
admin.site.register(ProjectStage)
admin.site.register(LogTransbank)
admin.site.register(Skill)
admin.site.register(Category)
# admin.site.register()
