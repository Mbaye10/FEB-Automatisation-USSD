from django.contrib import admin
from .models import CanalUSSD, UseCase, TestResult


class CanalUSSDAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')  
    search_fields = ('code', 'description')  
    ordering = ('code',) 


class UseCaseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'canal','parent' ,'numerousecase','entree', 'sortie_attendue')  
    search_fields = ('nom', 'entree', 'sortie_attendue') 
    list_filter = ('canal',)  
    ordering = ('nom',) 


class TestResultAdmin(admin.ModelAdmin):
    list_display = ('use_case', 'date_test', 'statut', 'message_erreur') 
    search_fields = ('use_case__nom', 'statut', 'message_erreur')  
    list_filter = ('statut', 'date_test')  
    ordering = ('-date_test',) 


admin.site.register(CanalUSSD)
admin.site.register(UseCase)
admin.site.register(TestResult)
