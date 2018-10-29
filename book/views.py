from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from book.models import BookInfo, PeopleInfo


def index(request):
    # BookInfo.objects.all()
    # 1.查询模型数据
    books = BookInfo.objects.all()

    # books
    # 学习模型，所以我们大家知道代码写在哪里就可以了

    # 2.组织上下文
    context = {
        'books': books
    }

    # 3.传递给模板进行渲染
    return render(request, 'index.html', context=context)

    # books

    return HttpResponse('ok')


##########################增删改#########################################

# 增加数据  2种方式
# 第一种方式
from book.models import BookInfo

book = BookInfo(
    name='python入门',
    pub_date='2000-1-1',
    readcount=20
)

# book.commentcount = 100

# 这种方式我们需要手动调用 save方法进行保存
book.save()


# 第二种，直接保存
"""
在命令行输入下面代码，返回的便是book
BookInfo.objects.create(
    name='java1',
    pub_date='2010-1-1',
    readcount=100
)
"""

book = BookInfo.objects.create(
    name='java1',
    pub_date='2010-1-1',
    readcount=100
)

# 修改数据

#第一种
# 先获取模型对象
# select * from bookinfo where id = 1
book = BookInfo.objects.get(id=6)
# 直接采用 对象.属性 = 值
book.name = 'java 啦啦啦啦'
book.readcount=20
#需要调用 save来保存
book.save()

# BookInfo.objects.get(id=5).update(name='python ～～～')  错误的

# 第二种方式 直接保存
BookInfo.objects.filter(id=5).update(name='python高级',commentcount=10000)

# 在命令行第二行显示的1，表示受影响的行数是1行
# >>> BookInfo.objects.filter(id=5).update(name='python高级',commentcount=10000)
# 1
# >>>

# 得到的是单一对象
# BookInfo.objects.get(id=6)
# 得到的是单一对象结果集
# BookInfo.objects.filter(id=5)

#删除
#第一种： 先获取对象，调用 delete方法
book = BookInfo.objects.get(id=6)

book.delete()

# 第二种
BookInfo.objects.filter(id=5).delete()


##########################查询   #########################################

# get  获取单一结果
BookInfo.objects.get(id=1)
BookInfo.objects.get(pk=1) # pk primary key 主键

BookInfo.objects.get(pk=10) # pk primary key 主键

BookInfo.objects.all()

#count
BookInfo.objects.all().count()


"""
filter过滤出多个结果   0,1,n
exclude排除掉符合条件剩下的结果
get过滤单一结果

这三个语句的语法形式为： 模型.objects.方法（字段名__运算符=值）

"""
# where
# 查询编号为1的图书
BookInfo.objects.get(id=1)
# exact   adj. 准确的，精密的；精确的
BookInfo.objects.get(id__exact=1)

BookInfo.objects.filter(id=1)

"""
结果对比，   get得到的是单一对象
            filter得到的是列表
详情如下：
命令行的运行结果：

>>> BookInfo.objects.get(id__exact=1)
<BookInfo: 射雕英雄传>
>>> BookInfo.objects.filter(id=1)
<QuerySet [<BookInfo: 射雕英雄传>]>

"""


# 查询名字为 射雕英雄传的书籍
BookInfo.objects.get(name='射雕英雄传')
BookInfo.objects.get(name__exact='射雕英雄传')

"""
其他的功能：（其中boaok作为一个变量来接收，可以得到它的其他属性）
>>> book = BookInfo.objects.get(id=1)
>>> book.commentcount
34
"""

# 查询书名包含'湖'的图书
BookInfo.objects.filter(name__contains='湖')
BookInfo.objects.get(name__contains='湖')

# 查询书名以'部'结尾的图书
BookInfo.objects.filter(name__endswith='部')

# 查询书名为空的图书
BookInfo.objects.filter(name__isnull=True)

# 查询编号为1或3或5的图书
# where id in ();
BookInfo.objects.filter(id__in=[1,3,5])

# 查询编号大于3的图书
# 大于        gt       (greater than)
# 大于等于      gte     (greater than equal)
# 小于        lt       (less than)
# 小于等于      lte     (less than equal)
BookInfo.objects.filter(id__gt=3)

# 查询编号不等于3的图书
BookInfo.objects.exclude(id=3)

# 查询1980年发表的图书
BookInfo.objects.filter(pub_date__year=1980)
BookInfo.objects.filter(pub_date__year='1980')

"""
>>> BookInfo.objects.filter(pub_date__year=1980)
<QuerySet [<BookInfo: 射雕英雄传>]>
>>> BookInfo.objects.filter(pub_date__year='1980')
<QuerySet [<BookInfo: 射雕英雄传>]>
"""

# 查询1990年1月1日后发表的图书
BookInfo.objects.filter(pub_date__gt='1990-1-1')


########################F对象和Q对象#########################

# F对象
# 之前的查询都是对象的属性与常量值比较，两个属性怎么比较呢？
# 答：使用F对象，被定义在django.db.models中。

# 获取评论量大于阅读量的书籍

#借助于F对象
# 语法形式为： 以filter为例
# filter(字段名__运算符=F('字段名'))

from django.db.models import F

BookInfo.objects.filter(commentcount__gt=F('readcount'))


#Q
# Q对象
# 多个过滤器逐个调用表示逻辑与关系，同sql语句中where部分的and关键字。
# 如果需要实现逻辑或or的查询，需要使用Q()对象结合|运算符，
# Q对象被义在django.db.models中。


# 查询 id大于2的书籍 并且 阅读量大于20
# where id>2 and readcount>20

# and的2中查询方式
# 1.
BookInfo.objects.filter(id__gt=2).filter(readcount__gt=20)

# 2.
BookInfo.objects.filter(id__gt=2,readcount__gt=20)

# 查询 id大于2的书籍 或者 阅读量大于20
# or
# Q对象来实现： Q对象的语法形式为： Q(字段名__运算符=值)
# or:    Q(字段名__运算符=值) | Q(字段名__运算符=值)

from django.db.models import Q

BookInfo.objects.filter(Q(id__gt=2) | Q(readcount__gt=20))

#  查询书籍Id不为3 的
BookInfo.objects.exclude(id=3)
# 可以用Q对象实现 not查询
# 语法形式为： ~Q()

BookInfo.objects.filter(~Q(id=3))


########################聚合函数 和 排序#########################

# Max,Min,Avg,Count,Sum

# 聚合函数的使用需要更改函数，使用
# 语法： objects.aggregate(Xxx('字段名'))

# 获取阅读量总数

from django.db.models import Sum,Max,Min,Avg,Count
BookInfo.objects.aggregate(Sum('readcount'))
BookInfo.objects.aggregate(Max('readcount'))
BookInfo.objects.aggregate(Min('readcount'))
BookInfo.objects.aggregate(Avg('readcount'))
BookInfo.objects.aggregate(Count('readcount'))

"""
数据库中数据：
mysql> select * from bookinfo;
+----+-----------------+------------+-----------+--------------+-----------+
| id | name            | pub_date   | readcount | commentcount | is_delete |
+----+-----------------+------------+-----------+--------------+-----------+
|  1 | 射雕英雄传      | 1980-05-01 |        12 |           34 |         0 |
|  2 | 天龙八部        | 1986-07-24 |        36 |           40 |         0 |
|  3 | 笑傲江湖        | 1995-12-24 |        20 |           80 |         0 |
|  4 | 雪山飞狐        | 1987-11-11 |        58 |           24 |         0 |
+----+-----------------+------------+-----------+--------------+-----------+
4 rows in set (0.00 sec)

mysql>

命令行，输出结果：
>>> from django.db.models import Sum,Max,Min,Avg,Count
>>> BookInfo.objects.aggregate(Sum('readcount'))
{'readcount__sum': 126}
>>> BookInfo.objects.aggregate(Max('readcount'))
{'readcount__max': 58}
>>> BookInfo.objects.aggregate(Min('readcount'))
{'readcount__min': 12}
>>> BookInfo.objects.aggregate(Avg('readcount'))
{'readcount__avg': 31.5}
>>> BookInfo.objects.aggregate(Count('readcount'))
{'readcount__count': 4}
"""

#排序
# order_by('字段')

# 默认是 升序
BookInfo.objects.all().order_by('readcount')

# 降序
BookInfo.objects.all().order_by('-readcount')


########################关联查询#########################


# 查询书籍为1的所有人物信息

#根据书籍查询人物
#书籍和人物是　１：　ｎ的关系，　书籍模型中　没有人物相关的字段

# 系统自动为我们创建一个属性，属性的命名是采用：
# 关联模型类名小写_set

book = BookInfo.objects.get(id=1)

people = book.peopleinfo_set.all()

# 查询人物为1的书籍信息

# 根据人物查询数据
# 根据n 查询1， 人物模型中 有书籍外键，我们直接使用外键就可以
from book.models import PeopleInfo
person = PeopleInfo.objects.get(id=1)

person.book.name


########################关联查询的筛选#########################

# 1:n的关系模型中， 根据 人物（n）进行条件查询
# 我们需要采用的语法形式为：
# 以filter为例： filter(关联模型类名小写__字段名__运算符=值)
# 查询图书，要求图书人物为"郭靖"

BookInfo.objects.filter(peopleinfo__name__exact='郭靖')
BookInfo.objects.filter(peopleinfo__name='郭靖')  #简写

# 查询图书，要求图书中人物的描述包含"八"
BookInfo.objects.filter(peopleinfo__description__contains='八')

# 根据书籍（1）查询人物（n）
# 人物中有书籍的外键：
# 我们就采用： 以filter为例： filter(外键__字段名__运算符=值)

#查询书名为“天龙八部”的所有人物
PeopleInfo.objects.filter(book__name__exact='天龙八部')
PeopleInfo.objects.filter(book__name='天龙八部')

# 查询图书阅读量大于30的所有人物
PeopleInfo.objects.filter(book__readcount__gt=30)


#缓存  --》 将硬盘中的数据 保存在 Redis中，当cpu使用的时候优先从 内存中获取
#       cpu在第一个获取数据的时候，如果内存中，没有，从磁盘中获取， 从磁盘获取之后，会缓存在内存中
        #以便下次使用

# mysql的数据是保存在      硬盘中         读取慢         空间大

# redis数据保存在        内存中         读取快         空间小

# 用这行代码查询的话，是直接从硬盘中查询的，在数据库的日志记录中可以看到每次都会有查询
# >>> [book.id for book in BookInfo.objects.all()]
# [1, 2, 3, 4, 14, 15]

# 用这行代码查询的话，第一次是直接从硬盘中查询的，在日志记录中会显示，之后便会存储到内存中，
# 之后的每次查询都是从内存中查询的，在日志记录中便不会再显示
# >>> books = BookInfo.objects.all()
# >>> [book.id for book in books]

# 例子：
"""
>>> [book.id for book in BookInfo.objects.all()]
[1, 2, 3, 4, 14, 15]
>>> [book.id for book in BookInfo.objects.all()]
[1, 2, 3, 4, 14, 15]
>>> [book.id for book in BookInfo.objects.all()]
[1, 2, 3, 4, 14, 15]

>>> books = BookInfo.objects.all()
>>> [book.id for book in books]
[1, 2, 3, 4, 14, 15]
>>> [book.id for book in books]
[1, 2, 3, 4, 14, 15]
>>> [book.id for book in books]
[1, 2, 3, 4, 14, 15]
>>>
"""


# 限制查询结果集
BookInfo.objects.all()[0:2]

# 默认从第一条开始获取，可以省略 0
BookInfo.objects.all()[:2]

#一个值，当索引使用
BookInfo.objects.all()[0]