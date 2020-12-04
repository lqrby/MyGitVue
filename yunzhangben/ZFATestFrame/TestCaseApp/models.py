from django.db import models
import django.utils.timezone as timezone
from django.contrib import admin
from django.contrib.auth.models import User 
from DjangoUeditor.models import UEditorField #头部增加这行代码导入UEditorField





class AppName(models.Model):
    """
    # app名称表
    """
    name = models.CharField('所属app',max_length=30)
    class Meta:
        verbose_name = 'app名字'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)

class Case(models.Model):
    """
    # 测试用例
    """
    app_name = models.ForeignKey(AppName, on_delete=models.CASCADE, verbose_name='业务应用', blank=False, null=True)
    module = models.CharField('模块名称', max_length=20 )
    title = models.CharField('用例名称', max_length=30 )
    method = models.CharField('请求方法', max_length=10 )
    native_choices = (
        (0, 'native'),
        (1, 'api_h5'),
        (2, 'quiz_h5'),
        (3, 'deputy_h5'),
    )
    domain_type = models.IntegerField('域名类型',default=0, choices=native_choices)
    url = models.CharField('接口(url)', max_length=256 )
    run_choices = (
        ('yes', '是'),
        ('no', '否'),
    )
    run = models.CharField('是否运行', default="yes", max_length=4, choices=run_choices )
    headers = models.CharField('headers请求头', max_length=1024)
    pre_case_id = models.IntegerField('是否有前置用例id',default=-1)
    pre_fields = models.CharField('需要前置字段', max_length=256)
    # Postposition_relation_id = models.IntegerField('是否有后置(关联)用例id',default=-1)
    # Postposition_relation = models.CharField('后置(关联)用例的字段', max_length=256)
    request_data = models.CharField('请求参数', max_length=1024)
    expect_result = models.CharField('预期结果', max_length=32 )
    assert_choices = (
        ('status', 'status'),
        ('data_list', 'data_list'),
        ('data_array', 'data_array'),
        ('data_item', 'data_item'),
        ('data_rotate', 'data_rotate'),
    )
    assert_type = models.CharField('断言类型', choices=assert_choices, max_length=32 )
    pass_choices = (
        ('unknown', '未知'),
        ('False', '否'),
        ('True', '是'),
    )
    pass_or_not = models.CharField('是否通过', max_length=10, default="unknown", choices=pass_choices, blank=True, null=True)
    msg = models.TextField('描述', default="",blank=True, null=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    response = models.TextField('实际结果', default="", blank=True, null=True)
    remark = models.CharField('备注', max_length=100, default="", blank=True, null=True)
    
    class Meta:
        verbose_name = '测试用例表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.app_name)

    



class Config(models.Model):
    """
    # 配置
    """
    name = models.ForeignKey(AppName, on_delete=models.CASCADE, verbose_name='所属app', blank=False, null=True)
    dict_key = models.CharField('字典key',max_length=32)
    dict_value = models.CharField('字典值',max_length=256)
    api_key = models.CharField('apikey',max_length=255, default="null",blank=True, null=True)
    
    class Meta:
        verbose_name = '测试配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)









    
    
    

    
