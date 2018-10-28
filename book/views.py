from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from book.models import BookInfo


def index(request):

    # BookInfo.objects.all()
    # 1.查询模型数据
    books = BookInfo.objects.all()

    # books
    # 学习模型，所以我们大家知道代码写在哪里就可以了

    # 2.组织上下文
    context = {
        'books':books
    }

    # 3.传递给模板进行渲染
    return render(request,'index.html',context=context)

    # books

    return HttpResponse('ok')
