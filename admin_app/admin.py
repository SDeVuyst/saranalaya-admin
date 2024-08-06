from django.contrib import admin, messages
from .models import *
from .utils import helper
from datetime import datetime
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _lazy_
from unfold.contrib.filters.admin import RangeDateFilter, RangeNumericFilter, FieldTextFilter
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from unfold.admin import ModelAdmin
from unfold.decorators import action, display
from unfold.contrib.inlines.admin import StackedInline, TabularInline
from simple_history.admin import SimpleHistoryAdmin
from django import forms
from .sites import saranalaya_admin_site

# Unfold model admin
admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User, site=saranalaya_admin_site)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass

@admin.register(Group, site=saranalaya_admin_site)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

# FORMS #
class AdoptionInlineFormChild(forms.ModelForm):
    class Meta:
        model = AdoptionParent.children.through
        fields = ['child']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['child'].queryset = Child.objects.order_by('name')


class AdoptionInlineFormParent(forms.ModelForm):
    class Meta:
        model = AdoptionParent.children.through
        fields = ['adoptionparent']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['adoptionparent'].queryset = AdoptionParent.objects.order_by('first_name')


class AdoptionSponsoringForm(forms.ModelForm):
    class Meta:
        model = AdoptionParentSponsoring
        fields = ['parent', 'child', 'amount', 'date', 'description']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if 'parent' in self.data:
    #         # only adopted children are available for selection
    #         try:
    #             parent_id = int(self.data.get('parent'))
    #             self.fields['child'].queryset = AdoptionParent.objects.get(id=parent_id).children.all()
    #         except (ValueError, TypeError):
    #             pass  # invalid input from the client; ignore and fallback to empty queryset
    #     elif self.instance.pk:
    #         self.fields['child'].queryset = self.instance.parent.children.all()
        

# FILTERS #
class AmountOfAdoptionParentsFilter(admin.SimpleListFilter):

    title = _('Amount of Adoption Parents')
    parameter_name = _('amount_of_adoption_parents')

    def lookups(self, request, model_admin):
        return [
            ("0", _("No Adoption Parents")),
            ("1", _("1 Adoption Parent")),
            ("2", _("2 Adoption Parents")),
            ("3", _("3 Adoption Parents")),
            ("3+", _("More than 3 Adoption Parents")),
        ]

    def queryset(self, request, queryset):
        
        ap_count = {}
        for ap in AdoptionParent.objects.all():
            children = ap.children.all()

            for child in children:
                if child in ap_count:
                    ap_count[child] += 1
                else:
                    ap_count[child] = 1

        if self.value() == "0":
            all_children = list(Child.objects.all())
            children_with_ap = [ch[0] for ch in ap_count.items()]
            # remaining_children = all_children.difference(children_with_ap)
            set_difference = set(all_children) - set(children_with_ap)
            remaining_children = list(set_difference)

            correct_ch = [ch.pk for ch in remaining_children]
            return queryset.filter(
                id__in=correct_ch
            )
        
        elif self.value() == "1":
            correct_aps = list(filter(
                lambda a: a[1] == 1,
                ap_count.items(),
            ))
            correct_aps = [ch[0].pk for ch in correct_aps]
            return queryset.filter(
                id__in=correct_aps
            )
        
        elif self.value() == "2":
            correct_aps = list(filter(
                lambda a: a[1] == 2,
                ap_count.items(),
            ))
            correct_aps = [ch[0].pk for ch in correct_aps]
            return queryset.filter(
                id__in=correct_aps
            )
        
        elif self.value() == "3":
            correct_aps = list(filter(
                lambda a: a[1] == 3,
                ap_count.items(),
            ))
            correct_aps = [ch[0].pk for ch in correct_aps]
            return queryset.filter(
                id__in=correct_aps
            )

        elif self.value() == "3+":
            correct_aps = list(filter(
                lambda a: a[1] > 3,
                ap_count.items(),
            ))
            correct_aps = [ch[0].pk for ch in correct_aps]
            return queryset.filter(
                id__in=correct_aps
            )
        

        return queryset
  


# INLINES #
class AdoptionInlineChild(TabularInline):
    model = AdoptionParent.children.through
    form = AdoptionInlineFormChild
    verbose_name = _("Adoption Parent - Child")
    verbose_name_plural = _("Adoption Parents - Children")


class AdoptionInlineParent(TabularInline):
    model = AdoptionParent.children.through
    form = AdoptionInlineFormParent
    verbose_name = _("Child - Adoption Parent")
    verbose_name_plural = _("Children - Adoption Parents")


class AdoptionParentSponsoringInline(StackedInline):
    model = AdoptionParentSponsoring
    form = AdoptionSponsoringForm
    extra = 1


class DonationInline(StackedInline):
    model = Donation



# MODELS #

@admin.register(AdoptionParent, site=saranalaya_admin_site)
class AdoptionParentAdmin(SimpleHistoryAdmin, ModelAdmin):
    list_display = ('first_name', 'last_name', 'get_children')
    exclude = ('children',)
    ordering = ('first_name', 'last_name')
    inlines = [ 
        AdoptionInlineChild,
        AdoptionParentSponsoringInline
    ]

    search_fields = ('first_name', 'last_name', 'firm', 'street_name', 'address_number', 'bus', 'postcode', 'city', 'country', 'mail', 'description', 'phone_number', 'children__name', 'children__description')
    list_filter = (
        ('active', admin.BooleanFieldListFilter), 
        'country', 
        'children', 
        ('city', FieldTextFilter)
    )

    list_filter_submit = True

    actions = [
        "add_new_sponsoring",
        "generate_address_list",
        "generate_mail_list",
    ]

    @action(description=_('Add New Payment'))
    def add_new_sponsoring(modeladmin, request, queryset):
        amount_of_sponsors_saved = 0

        for sponsor in queryset:
            if not sponsor.active:
                continue

            children_of_sponsor = [c for c in Child.objects.all() if sponsor in c.get_adoption_parents()]
            
            for child in children_of_sponsor:
                sp = AdoptionParentSponsoring(
                    date=datetime.now(),
                    amount=0, 
                    parent=sponsor,
                    child=child
                )

                sp.save()
                amount_of_sponsors_saved += 1


        return messages.success(request, _(f"Added {amount_of_sponsors_saved} Payments!"))

    @action(description=_("Generate Address List"))
    def generate_address_list(modeladmin, request, queryset):
        return helper.generateAddressList(modeladmin, request, queryset)

    @action(description=_("Generate Mailing List"))
    def generate_mail_list(modeladmin, request, queryset):
        return helper.generateMailList(modeladmin, request, queryset)


@admin.register(Child, site=saranalaya_admin_site)
class ChildAdmin(SimpleHistoryAdmin, ModelAdmin):

    list_display = ('name', 'status_colored', 'day_of_birth', 'get_adoption_parents_formatted')

    @display(
        description=_lazy_('Status'), 
        label={
            StatusChoices.ACTIVE: "success",
            StatusChoices.LEFT: "danger",
            StatusChoices.SUPPORT: "info",
        },
    )
    def status_colored(self, obj):
        return obj.status, obj.get_status_display()
    
    
    ordering = ('name',)
    inlines = [
        AdoptionInlineParent
    ]

    search_fields = ('name', 'gender', 'adoptionparent__first_name', 'adoptionparent__last_name', 'adoptionparent__firm', 'adoptionparent__street_name', 'adoptionparent__postcode', 'adoptionparent__city', 'adoptionparent__country', 'adoptionparent__mail', 'adoptionparent__description', 'adoptionparent__phone_number', 'day_of_birth', 'date_of_admission', 'date_of_leave', 'indian_parent_status', 'status', 'link_website', 'description')
    list_filter = (
        AmountOfAdoptionParentsFilter,
        'gender',
        'status',
        'indian_parent_status',
        ('day_of_birth', RangeDateFilter), 
        ('date_of_admission', RangeDateFilter), 
        ('date_of_leave', RangeDateFilter), 
    )

    list_filter_submit = True


@admin.register(AdoptionParentSponsoring, site=saranalaya_admin_site)
class AdoptionParentSponsoringAdmin(SimpleHistoryAdmin, ModelAdmin):
    class Media:
        js = ('js/paymentcolor.js',)   

    form = AdoptionSponsoringForm

    list_display = ('date', 'amount', 'parent', 'child', 'get_amount_left')
    ordering = ('date', 'amount')

    search_fields = ('date', 'amount', 'description', 'parent__first_name', 'parent__last_name','parent__firm', 'parent__street_name', 'parent__postcode', 'parent__city', 'parent__country', 'parent__mail', 'parent__description', 'parent__phone_number', 'child__name')
    list_filter = (
        ('date', RangeDateFilter), 
        ('amount', RangeNumericFilter), 
        'parent', 'child'
    )

    list_filter_submit = True

    actions = [
        "generate_address_list",
        "generate_mail_list",
    ]

    @action(description=_("Generate Address List"))
    def generate_address_list(modeladmin, request, queryset):
        # queryset should only be the corresponding adoptionparents
        parent_queryset = queryset.values_list('parent', flat=True).distinct()
        parents = AdoptionParent.objects.filter(id__in=parent_queryset)
        return helper.generateAddressList(modeladmin, request, parents)

    @action(description=_("Generate Mailing List"))
    def generate_mail_list(modeladmin, request, queryset):
        # queryset should only be the corresponding adoptionparents
        parent_queryset = queryset.values_list('parent', flat=True).distinct()
        parents = AdoptionParent.objects.filter(id__in=parent_queryset)
        return helper.generateMailList(modeladmin, request, parents)


@admin.register(Sponsor, site=saranalaya_admin_site)
class SponsorAdmin(SimpleHistoryAdmin, ModelAdmin):
    list_display = ('first_name', 'last_name', 'letters')
    ordering = ('first_name', 'last_name')
    inlines = [
        DonationInline
    ]

    search_fields = ('first_name', 'last_name', 'firm', 'street_name', 'address_number', 'bus', 'postcode', 'city', 'country', 'mail', 'description', 'phone_number')
    list_filter = (
        'letters', 
        'country', 
        ('city', FieldTextFilter),
    )
    list_filter_submit = True

    actions = [
        "generate_address_list",
        "generate_mail_list",
    ]

    @action(description=_("Generate Address List"))
    def generate_address_list(modeladmin, request, queryset):
        return helper.generateAddressList(modeladmin, request, queryset)

    @action(description=_("Generate Mailing List"))
    def generate_mail_list(modeladmin, request, queryset):
        return helper.generateMailList(modeladmin, request, queryset)
    

@admin.register(Donation, site=saranalaya_admin_site)
class DonationAdmin(SimpleHistoryAdmin, ModelAdmin):
    list_display = ('date', 'amount', 'sponsor')
    ordering = ('date', 'amount')
    search_fields = ('sponsor__first_name', 'sponsor__last_name', 'sponsor__firm', 'sponsor__street_name', 'sponsor__postcode', 'sponsor__city', 'sponsor__country', 'sponsor__mail', 'sponsor__description', 'sponsor__phone_number', 'amount', 'date', 'description')
    list_filter = (
        ('date' , RangeDateFilter),
        ('amount', RangeNumericFilter),
        'sponsor'
    )
    list_filter_submit = True
