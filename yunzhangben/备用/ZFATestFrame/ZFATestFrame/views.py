# from django.http import HttpResponse
# from django.shortcuts import render
 
# def hello(request):
#     return HttpResponse("Hello world ! ")

# def runoob(request):
#     context = {}
#     context['hello'] = 'Hello World!'
#     print("888")
#     return render(request, 'runoob.html', context)

# #首页
# def index(request):
#     banner = Banner.objects.filter(is_active=True)[0:4]
#     tui = Article.objects.filter(tui__id=1)[:3]
#     list = Article.objects.all().order_by('-id') #[0:2] 最新文章根据文章id倒序排序
#     hot = Article.objects.all().order_by('views')[:10]  #热门文章排行根据浏览量升序排序
#     link = Link.objects.all()
#     page = request.GET.get('page')
#     paginator = Paginator(list, 5)
#     try:
#         list = paginator.page(page)#获取当前页码的记录
#     except PageNotAnInteger:
#         list = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
#     except EmptyPage:
#         list = paginator.page(paginator.num_pages)#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
#     return render(request, 'index.html', locals())

# #列表页
# def list(request,lid):
#     list = Article.objects.filter(category_id=lid)
#     cname = Category.objects.get(id=lid)
#     page = request.GET.get('page')
#     paginator = Paginator(list, 5)
#     try:
#         list = paginator.page(page)#获取当前页码的记录
#     except PageNotAnInteger:
#         list = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
#     except EmptyPage:
#         list = paginator.page(paginator.num_pages)#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
#     return render(request, 'list.html', locals())