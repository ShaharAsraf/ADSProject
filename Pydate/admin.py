from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserData, PersonalityTestItem, PersonalityTestAnswer, PersonalQuestionContent, \
    PersonalQuestionAnswer, PersonalQuestionUser, UserLog, Match


class ProfileInline(admin.StackedInline):
    model = UserData
    can_delete = False
    verbose_name_plural = 'UserData'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(PersonalQuestionUser)
admin.site.register(PersonalQuestionAnswer)
admin.site.register(PersonalQuestionContent)
admin.site.register(Match)
admin.site.register(UserLog)
admin.site.register(PersonalityTestItem)
admin.site.register(PersonalityTestAnswer)
admin.site.register(UserData)
