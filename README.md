# archer_dbmp

该项目主要是为了让MySQL数据库维护管理尽量的自动化起来，对于基本的操作能解放相关人员的双手。并且同时也能让相关的开发人员更好的对数据库进行操作。

该项目是使用Django开发的，属于一个web项目。

### 前奏

安装一些包和模块

```
yum install lzma libffi-devel -y
pip install Django
pip install paramiko
pip install MySQL-python

# 在备份客户端中有用到此模块
pip install sqlalchemy
pip install sqlacodegen
```

>**传送门:**
> 
>备份客户端介绍:
>https://github.com/daiguadaidai/mysql_backup_client


### 初始化数据库

在项目的中有一个`sql`目录，该目录下有一个`my_free_schema.sql`文件。将该文件导入到`MySQL`数据库中就行了。

###### 目录结构

```
.
├── archer_dbmp
│   ├── settings.py
├── common
├── dbmp
├── logs
├── manage.py
├── README.md
├── sql
│   ├── models.py
│   └── my_free_schema.sql
├── static
└── templates
```

###### 导入数据库表结构

```
mysql -uroot -pxxx -h127.0.0.1 -P3306 < my_free_schema.sql
```

这样就在`MySQL`实例中创建了一个`my_free`的数据库

###### 初始化一条操作系统记录

在数据库中执行以下命令：

```
INSERT INTO cmdb_os VALUES(NULL,
    'hostname-0',
    'alias-0',
    inet_aton('192.168.111.0'),
    'username-0',
    'password-0',
    '(0)this is remark',
    NOW(),
    NOW());
```

有关表字段的相关含义等内容，请自行到数据库中查看注释。

> **Tips:**
> 如果你有多个操作系统，也可以初始化多条`cmdb_os`的记录，在该项目没有添加操作系统的功能。主要是因为操作系统的信息主要是在`archer_cmdb`中实现。

### 启动使用archer_dbmp

启动和使用`archer_dbmp`其实就是启动一个Django项目

###### 稍微设置`setting.py`文件

```
cat archer_dbmp/settings.py

... omit ...

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'my_free',
        'USER':'root',
        'PASSWORD':'xxx',
        'HOST':'127.0.0.1',
        'PORT':'3306',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

... omit ...
```

###### 启动`archer_dbmp`

```
python manage.py runserver 0.0.0.0:8000
```

###### 访问`archer_dbmp`

在浏览器上输入一下地址(注意替换为自己的地址):

```
http://127.0.0.1:8000
```

>**Tips:**
>有能力的朋友可以结合Ningx来搭建环境。
