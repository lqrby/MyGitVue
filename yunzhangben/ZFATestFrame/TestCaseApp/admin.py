
from django import forms
from django.contrib import admin
from .models import Case, Config, AppName
from django.contrib.admin.helpers import ActionForm
import sys
sys.path.append("E:/myTestFile/TestObject/zhongfuan/yunzhangben/yzb_regression")
from case.class_api_test import ZFAclassTestCase

# admin.site.register(models.UserInfo)
#UserInfo模型的管理器（自定制显示内容类）
admin.site.site_title = '测试平台管理系统'
admin.site.site_header = '测试用例后台管理系统'

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    # 文章列表里显示想要显示的字段
    list_display = ('id', 'app_name', 'module', 'title', 'method', 'domain_type', 'url', 'run','update_time','pass_or_not', 'response', "remark")
    # 满20条数据就自动分页
    list_per_page = 20
    #后台数据列表排序方式,负号表示降序排序
    ordering = ('-update_time',)
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'app_name', 'module', 'title', 'url',)
    
    # change_form_template = 'admin/addArticle.html' #跳转到修改页面

    
    # list_editable 设置默认可编辑字段
    list_editable = ['run','remark']

    # fk_fields 设置显示外键字段
    # fk_fields = ('publish_id',)
    
    # 设置不可修改字段
    # readonly_fields = ('creationTime', 'userId')
    # 筛选器
    list_filter = ("app_name","run","module","pass_or_not","domain_type")  # 过滤器
    search_fields = ("id","url","run","title","pass_or_not")  # 搜索字段
    # 是否显示action选择的个数
    actions_selection_counter = True
    # paramter_name = "app_name"
    # date_hierarchy = 'creationTime'  # 详细时间分层筛选　
    #列表顶部，设置为False不在顶部显示，默认为True。
    # actions_on_top=True

    #列表底部，设置为False不在底部显示，默认为False。
    # actions_on_bottom=False

    #批量设置是否运行
    def set_run_yes(self, request, queryset):
        queryset.update(run='yes')
    set_run_yes.short_description = '设置运行为:yes'

    def set_run_no(self, request, queryset):
        queryset.update(run='no')
    set_run_no.short_description = '设置运行为:no'

    #批量运行
    def run_batch(self, request, queryset):
        # queryset.update(run='yes')
        #测试环境:yzb_test_host
        
        app_name, host_key = "云账本", "yzb_test_host"
        ZFAclassTestCase().runAllCase(app_name, host_key)
    run_batch.short_description = '批量运行'
    actions = (set_run_yes,set_run_no,run_batch) #指定自定义actions



class XForm(ActionForm):
    x_field = forms.CharField()


class YourModelAdmin(admin.ModelAdmin):
    action_form = XForm

    
    
    
@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'dict_key', 'dict_value')
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'name', 'dict_key', 'dict_value')

@admin.register(AppName)
class AppNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'name')






