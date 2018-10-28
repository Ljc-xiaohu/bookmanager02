from django.db import models

# Create your models here.
"""
sqlite3 虽然是一个关系型数据库但是它是小型的数据库 主要在移动端使用，不能满足我们的需求

"""


# 1. 模型类需要继承自 models.Model
class BookInfo(models.Model):
    """
        字段名
            1.字段名不能使用 python关键字 也不能使用mysql关键字
            2.我们不能使用 连续的下划线（__）

        字段类型

        字段选项



        insert into bookinfo(name, pub_date, readcount,commentcount, is_delete) values
    ('射雕英雄传', '1980-5-1', 12, 34, 0),
    ('天龙八部', '1986-7-24', 36, 40, 0),
    ('笑傲江湖', '1995-12-24', 20, 80, 0),
    ('雪山飞狐', '1987-11-11', 58, 24, 0);

        """
    # 书籍名，发布时间，阅读量，评论量，是否逻辑删除
    name = models.CharField(max_length=10, unique=True, null=False)

    # 发布时间
    pub_date = models.DateField(null=True, verbose_name='admin站点显示的字段')

    # 阅读量
    readcount = models.IntegerField(default=0)

    # 评论量
    commentcount = models.IntegerField(default=0)

    # 是否逻辑删除
    is_delete = models.BooleanField(default=False)

    # 修改模型的相关配置信息，例如： 表名
    class Meta:  # 固定写法
        db_table = 'bookinfo'
        verbose_name = 'admin站点显示的内容'

    def __str__(self):
        return self.name


# 准备人物列表信息的模型类
class PeopleInfo(models.Model):
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    name = models.CharField(max_length=20, verbose_name='名称')
    # choices 枚举类型

    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    description = models.CharField(max_length=200, null=True, verbose_name='描述信息')
    # on_delete 书籍和人物是 -- 1：n的关系
    # 外键的级联操作
    # 1：n
    # 主表数据删除，对从表的影响
    # 主表删除， 从表拒绝
    # 主表删除， 从表删除
    # 主表删除， 从表不受影响，数据保留

    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE, verbose_name='图书')  # 外键

    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'peopleinfo'
        verbose_name = '人物信息'

    def __str__(self):
        return self.name


"""

外键的级联操作

#书籍表  1
create table book_01(
    id int primary key auto_increment,
    name varchar(10) not NULL
) charset utf8;

insert into book_01(name) values ('三国演义');

#人物表 n
create table people_01(
  id int primary key auto_increment,
  name VARCHAR(10) not NULL ,
  book_id int,
  FOREIGN KEY(book_id) REFERENCES book_01(id) ON DELETE RESTRICT  #RESTRICT 拒绝删除
) charset utf8;

insert into people_01(name,book_id) VALUES ('刘备',1);





#书籍表  1
create table book_02(
    id int primary key auto_increment,
    name varchar(10) not NULL
) charset utf8;

insert into book_02(name) values ('三国演义');

#人物表 n
create table people_02(
  id int primary key auto_increment,
  name VARCHAR(10) not NULL ,
  book_id int,
  FOREIGN KEY(book_id) REFERENCES book_02(id) ON DELETE  set null # 主表删除，从表字段 为null
) charset utf8;

insert into people_02(name,book_id) VALUES ('刘备',1);




#书籍表  1
create table book_03(
    id int primary key auto_increment,
    name varchar(10) not NULL
) charset utf8;

insert into book_03(name) values ('三国演义');

#人物表 n
create table people_03(
  id int primary key auto_increment,
  name VARCHAR(10) not NULL ,
  book_id int,
  FOREIGN KEY(book_id) REFERENCES book_03(id) ON DELETE  CASCADE #CASCADE 主表删除，从表也删除
) charset utf8;

insert into people_03(name,book_id) VALUES ('刘备',1);

"""
