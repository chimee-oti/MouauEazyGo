from django.contrib import admin
from user.models import User, Profile
from django.contrib.auth.admin import UserAdmin
from django import forms


# the follow code will append the user profile inline at the bottom of
# the user 's models and not place it in a seperate models like the main
# User model.
class UserInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


# add the custom models to django admin
# also include cusomisation features for the interface
class UserAdminConfig(UserAdmin):
    model = User
    # add the profile inline to the User model
    inlines = (UserInline, )
    search_fields = ('email', 'username', 'firstname',)
    list_filter = ('email', 'username', 'firstname', 'is_active', 'is_staff')
    ordering = ('firstname',)
    list_display = ('email', 'username', 'firstname',
                    'lastname', 'is_active', 'is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'firstname',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'firstname', 'lastname', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdminConfig, self).get_inline_instances(request, obj)


admin.site.register(User, UserAdminConfig)
admin.site.register(Profile)
