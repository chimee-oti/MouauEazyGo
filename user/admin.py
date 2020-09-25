from django.contrib import admin
from user.models import NewUser, Profile
from django.contrib.auth.admin import UserAdmin
from django import forms


# the follow code will append the user profile inline at the bottom of
# the user 's models and not place it in a seperate models like the main
# NewUser model.
class NewUserInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


# add the custom models to django admin
# also include cusomisation features for the interface
class UserAdminConfig(UserAdmin):
    model = NewUser
    # add the profile inline to the NewUser model
    inlines = (NewUserInline, )
    search_fields = ('email', 'user_name', 'first_name',)
    list_filter = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')
    ordering = ('first_name',)
    list_display = ('email', 'user_name', 'first_name',
                    'last_name', 'is_active', 'is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        # ('Personal', {'fields': ('about',)}),
    )
    # formfield_overrides = {
    #     NewUser.about: {'widget': forms.Textarea(attrs={'rows': 10, 'cols': 40})},
    # }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdminConfig, self).get_inline_instances(request, obj)


admin.site.register(NewUser, UserAdminConfig)
