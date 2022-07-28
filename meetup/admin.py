from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path

from .models import (
    Meetuper,
    Speaker,
    MeetupProgram,
    Stage,
    Block,
    Event,
    Question,
    Donation
)
from .utils import notify


class QuestionInline(admin.TabularInline):
    model = Question


@admin.register(Meetuper)
class MeetuperAdmin(admin.ModelAdmin):
    list_display = [
        'chat_id',
        'firstname',
        'lastname',
        'email',
        'phone_number',
        'organization',
        'position',
        'is_open_for_communication',
    ]
    inlines = [
        QuestionInline,
    ]


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_filter = ['is_active']
    list_display = [
        'participant',
        'is_active',
    ]
    inlines = [
        QuestionInline,
    ]


class StageInline(admin.TabularInline):
    model = Stage


@admin.register(MeetupProgram)
class MeetupProgramAdmin(admin.ModelAdmin):
    list_filter = ['date']
    list_display = [
        'title',
        'date',
        'start_time',
        'end_time'
    ]
    inlines = [
        StageInline,
    ]
    change_form_template = 'meetups_change_form.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('notify/', self.send_notifications),
            path('program_changed/', self.send_program_notifications)
        ]
        return my_urls + urls

    def send_notifications(self, request):
        notify()
        self.message_user(request, 'Оповещения отправлены')
        return redirect('../')

    def send_program_notifications(self, request):
        notify()
        self.message_user(
            request,
            'Оповещения об изменениях в программе отправлены'
        )
        return redirect('../')



class BlockInline(admin.TabularInline):
    model = Block


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_filter = ['program']
    list_display = [
        'title',
        'program',
        'start_time',
        'end_time'
    ]
    inlines = [
        BlockInline,
    ]


class EventInline(admin.TabularInline):
    model = Event


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_filter = ['stage']
    list_display = [
        'title',
        'stage',
        'start_time',
        'end_time'
    ]
    inlines = [
        EventInline,
    ]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_filter = ['is_active', 'speaker']
    list_display = [
        'title',
        'speaker',
        'block',
        'start_time',
        'end_time',
        'is_active'
    ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_filter = [
        'date',
        'is_answered',
        'speaker'
    ]
    list_display = [
        'text',
        'date',
        'speaker',
        'meetuper',
        'is_answered'
    ]


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_filter = ['date']
    list_display = [
        'meetuper',
        'date',
        'amount',
    ]
