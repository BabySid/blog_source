#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

#############################################################################
# http://pelican-docs-zh-cn.readthedocs.org/en/latest
#############################################################################

#############################################################################
###########  基本设置 ###########################################################
#############################################################################

#默认作者（输入您的名字）
AUTHOR = u'MiLimin'

#如果您使用多种语言，可以在此设置日期格式，详情参加“日期格式与区域设置”
DATE_FORMATS = { 'zh': ('zh_CN.UTF-8',  '%Y-%m-%d %H:%M:%S'), }

#如果您不希望在文章元数据中指定类别，将该项设置为 True ，利用子目录安排文章结构，子目录将成为文章的分类，
#如果设置为 False ， DEFAULT_CATEGORY 将作为备用选项。
USE_FOLDER_AS_CATEGORY  = True

#默认文章分类
DEFAULT_CATEGORY = '随笔'

#默认日期格式
#DEFAULT_DATE_FORMAT  = '%a %d %B %Y'

#是否在模板菜单上显示页面，可以在模板中选择是否使用该配置项
DISPLAY_PAGES_ON_MENU = False

#是否在模板菜单上显示分类，可以在模板中选择是否使用该配置项
DISPLAY_CATEGORIES_ON_MENU = True

#如果设为“fs”，当无法从元数据中获取日期信息时，Pelican将会使用文件系统时间戳信息（mtime）
#如果设为元组对象，默认的datetime对象将通过元组的构造方法生成
#DEFAULT_DATE = None

#文章和页面的默认元数据设置
#DEFAULT_METADATA = ()

#Extra configuration settings for the docutils publisher (applicable only to reStructuredText).
#DOCUTILS_SETTINGS = {}

#使用正则表达式提取文件名的元数据，在元数据对象中设置用来匹配所有组。
#默认只能从文件名中提取日期，如果你想同时提取date和slug，设置如下： '(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'.
#FILENAME_METADATA  = '(?P<date>\d{4}-\d{2}-\d{2}).*'

#例如 FILENAME_METADATA, 从一个页面的完整路径相对于内容源目录进行解析
#PATH_METADATA = ''

#通过相对路径添加元数据字典关键字
EXTRA_PATH_METADATA = { 'extra/custom.css': {'path': 'static/custom.css'},
                        'extra/about.html': {'path': 'about.html'},
                        'extra/runcode.js': {'path': 'static/runcode.js'},
                        'extra/baidutongji.js': {'path': 'static/baidutongji.js'}, }

#删除output目录，优点在于避免生成不必要的文件，同时， 该设置具有一定风险，请谨慎处理。
#DELETE_OUTPUT_DIRECTORY = False

#在output目录中应该保留元组文件名，典型的案例则是用于保存版本控制数据。例如 (".hg", ".git", ".bzr")
#OUTPUT_RETENTION = ()

#使用Jinja扩展列表
#JINJA_EXTENSIONS = []

#Jinja2 filters自定义列表，字典应该映射filter函数的filtername。例如: {'urlencode': urlencode_filter}
#JINJA_FILTERS  = {}

#更改时区. 提供区域列表或是代表区域的字符串
#LOCALE  = ""

#A list of tuples containing the logging level (up to warning) and the message to be ignored.
#For example: [(logging.WARN, 'TAG_SAVE_AS is set to False')]
#LOG_FILTER = []

#生成或者忽略文件扩展或者阅读分类字典。
#例如： 避免生成 .html 文件, set: READERS = {'html': None}. 添加自定义 foo 扩展阅读，set: READERS = {'foo': FooReader}
READERS  = {'html': None}

#文件匹配模式列表。用于忽略一些源文件。例如, 默认 ['.#*'] 将会忽略emacs编辑器的锁定文件.
#IGNORE_FILES  = ['.#*']

#关于Markdown可用的扩展列表。
#参考Python Markdown 文档查看支持扩展列表 (注意：在设置文件中定义该值将会覆盖和替换默认值，如果你的目标是在默认值上添加设置，则需要明确说明并列举所需Marksown完整扩展列表。
#MD_EXTENSIONS  = ['codehilite(css_class=highlight)','extra']

#文件生成目录
OUTPUT_PATH = 'output/'

#输入文件目录
#PATH  = 'content'

#页面生成目录
PAGE_PATHS  = ['pages']

#查找页面需要忽略的文件夹列表
PAGE_EXCLUDES = []

#文章输入文件目录
#ARTICLE_PATHS = ['']

#查找文章需要忽略的文件夹列表
#ARTICLE_EXCLUDES = []

#如果希望复制文章和页面的原始格式(e.g. Markdown or reStructuredText)，请设置为True并指定 OUTPUT_PATH.
OUTPUT_SOURCES = False

#控制资源生成扩展，默认值为 .text. 如果没有有效的字符串，将使用默认值。
#OUTPUT_SOURCES_EXTENSION = '.text'

#定义是否使用文档相对URL链接，只有当测试时设置为 True ，如果你完全理解该效果，则可以用于links或者feeds。
#RELATIVE_URLS  = False

#A list of directories where to look for plugins.
PLUGIN_PATHS = ['plugins/']

#载入插件
PLUGINS  = ['tag_cloud']

# 站点名称
SITENAME = u"BlackFox' Home"

#站点URL。默认未定义，所以最好指定SITEURL；如果未指定，无法生成对应feeds的URLs。
#应该包含 http:// 以及你的域名, 结尾不加/，例如: SITEURL = 'http://mydomain.com'
SITEURL = 'http://blackfox1983.github.io'

#包含文章生成时的模板页
#TEMPLATE_PAGES = None

#在output目录中提供可访问的静态路径 “static”. 默认将会复制 “images” 文件夹到output目录.
STATIC_PATHS = ['images', 'extra']

#A list of directories to exclude when looking for static files.
#STATIC_EXCLUDES = []

#显示日期信息，生成Atom和RSS时间信息
TIMEZONE = 'Asia/Shanghai'

#如果设置为True, 一些排版效果将会纳入生成的HTML文件中，通过 Typogrify 库, 安装方式: pip install typogrify
TYPOGRIFY = False

#A list of tags for Typogrify to ignore. By default Typogrify will ignore pre and code tags.
#TYPOGRIFY_IGNORE_TAGS = []

#直接使用模板。 通常情况下直接使用模板生成index页面的内容，(e.g., tags and category index pages).
#如果无需标签和分类合集,设置 DIRECT_TEMPLATES = ('index', 'archives')
DIRECT_TEMPLATES  = ('index', 'tags', 'categories', 'archives')

#提供可以分页的模板
PAGINATED_DIRECT_TEMPLATES = ['index']

#文章摘要最大字数。如果设置为 None ，将导致摘要和原文内容一致
SUMMARY_MAX_LENGTH = 100

#Jinja2 模板搜索列表.可以从主题中单独分离出来。 例如: projects, resume, profile ... 这些模板需要使用 DIRECT_TEMPLATES 设置.
#EXTRA_TEMPLATES_PATHS  = []

#If disabled, content with dates in the future will get a default status of draft
WITH_FUTURE_DATES = True

#将选项列表传递给AsciiDoc
#ASCIIDOC_OPTIONS = []

#如果仅用, 内容和日期将以草稿形式保存
#WITH_FUTURE_DATES  = True

#内部链接分析的正则表达式。默认内部链接语法标识符表明 filename, 使用 {} 或者 ||. 标识符位于 { 和 } 之间
#INTRASITE_LINK_REGEX  = '[{|](?P<what>.*?)[|}]'

#针对reStructuredText代码块，Pygments默认设置列表
PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

#Specifies where you want the slug to be automatically generated from.
#Can be set to title to use the ‘Title:’ metadata tag or basename to use the article’s file name when creating the slug.
#SLUGIFY_SOURCE = 'title'

#If True, save content in a cache file
CACHE_CONTENT = True

#If set to 'reader', save only the raw content and metadata returned by readers.
#If set to 'generator', save processed content objects.
CONTENT_CACHING_LAYER = 'reader'

#Directory in which to store cache files.
CACHE_PATH = 'cache'

#If True, use gzip to (de)compress the cache files.
GZIP_CACHE = True

#Controls how files are checked for modifications.
CHECK_MODIFIED_METHOD = 'mtime'

#If True, load unmodified content from cache.
LOAD_CONTENT_CACHE = True

#If True, do not load content cache in autoreload mode when the settings file changes.
AUTORELOAD_IGNORE_CACHE = False

#If this list is not empty, only output files with their paths in this list are written.
#Paths should be either absolute or relative to the current Pelican working directory.
#WRITE_SELECTED = []

#############################################################################
###########  URL设置 ###########################################################
#############################################################################

#文章URL
ARTICLE_URL  = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/'

#文章保存位置
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

#he metadata attribute used to sort articles. By default, the articles_page.object_list template variable is ordered by slug.
#If you modify this, make sure all articles contain the attribute you specify.
#You can also specify a “sorting” function of one argument that is used to extract a comparison key from each article.
#For example, sorting by title without using the built-in functionality would use the function operator.attrgetter('title').
#ARTICLE_ORDER_BY = 'slug'

#设置特定语言格式文章的URL
#ARTICLE_LANG_URL  = '{slug}-{lang}.html'

#设置特定语言格式文章的存储位置
#ARTICLE_LANG_SAVE_AS  = '{slug}-{lang}.html'

#The URL to refer to an article draft.
#DRAFT_URL = 'drafts/{slug}.html'

#The place where we will save an article draft.
#DRAFT_SAVE_AS = 'drafts/{slug}.html'

#The URL to refer to an article draft which doesn’t use the default language.
#DRAFT_LANG_URL = 'drafts/{slug}-{lang}.html'

#The place where we will save an article draft which doesn’t use the default language.
#DRAFT_LANG_SAVE_AS = 'drafts/{slug}-{lang}.html'

#页面URL链接
PAGE_URL  = 'pages/{slug}/'

#页面存储位置
PAGE_SAVE_AS  = 'pages/{slug}/index.html'

#The metadata attribute used to sort pages. By default the PAGES template variable is ordered by basename (i.e., path not included).
#Note that the option 'basename' is a special option supported in the source code. If you modify this setting, make sure all pages contain the attribute you specify.
#You can also specify a “sorting” function of one argument that is used to extract a comparison key from each page.
#For example, the basename function looks similar to lambda x: os.path.basename(getattr(x, 'source_path', '')).
#PAGE_ORDER_BY = 'basename'

#设置特定语言格式页面的URL
#PAGE_LANG_URL  = 'pages/{slug}-{lang}.html'

#设置特定语言格式页面的存储位置
#PAGE_LANG_SAVE_AS  = 'pages/{slug}-{lang}.html'

#类别URl
#CATEGORY_URL  = 'category/{slug}.html'

#类别保存位置
#CATEGORY_SAVE_AS  = 'category/{slug}.html'

#标签URL
TAG_URL  = 'tag/{slug}.html'

#标签页面保存位置
TAG_SAVE_AS  = 'tag/{slug}.html'

#标签列表URL
TAGS_URL  = 'tags.html'

#标签列表保存位置
TAGS_SAVE_AS  = 'tags.html'

#作者URl
#AUTHOR_URL  = 'author/{slug}.html'

#作者存储位置
#AUTHOR_SAVE_AS  = 'author/{slug}.html'

#作者列表URL
#AUTHORS_URL  = 'authors.html'

#作者列表存储位置
#AUTHORS_SAVE_AS  = 'authors.html'

#存储模板生成文件内容位置. <DIRECT_TEMPLATE_NAME> 名称大写
#('index', 'tags', 'categories', 'archives') by default
#<DIRECT_TEMPLATE_NAME>_SAVE_AS

#文章归类页面存储位置
#ARCHIVES_SAVE_AS  = 'archives.html'

#按年归类的文章存储位置
YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'

#按月归类的文章存储位置
#MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/index.html'

#按日归类的文章存储位置
#DAY_ARCHIVE_SAVE_AS  = False

#Substitutions to make prior to stripping out non-alphanumerics when generating slugs.
#Specified as a list of 2-tuples of (from, to) which are applied in order.
#SLUG_SUBSTITUTIONS = ()

#############################################################################
###########  Feed设置 #######################################################
#############################################################################

#The domain prepended to feed URLs. Since feed URLs should always be absolute,
#it is highly recommended to define this (e.g., “http://feeds.example.com”).
#If you have already explicitly defined SITEURL (see above) and want to use the same domain for your feeds,
#you can just set: FEED_DOMAIN = SITEURL.
#FEED_DOMAIN = SITEURL

#Relative URL to output the Atom feed.
#FEED_ATOM = None

#Relative URL to output the RSS feed
#FEED_RSS  = None

#Relative URL to output the all posts Atom feed: this feed will contain all posts regardless of their language.
FEED_ALL_ATOM = None

#Relative URL to output the all posts RSS feed: this feed will contain all posts regardless of their language.
#FEED_ALL_RSS = None

#Where to put the category Atom feeds.
CATEGORY_FEED_ATOM = None

#Where to put the category RSS feeds.
#CATEGORY_FEED_RSS = None

#Where to put the author Atom feeds.
AUTHOR_FEED_ATOM = None

#Where to put the author RSS feeds.
AUTHOR_FEED_RSS = None

#Relative URL to output the tag Atom feed. It should be defined using a “%s” match in the tag name.
#TAG_FEED_ATOM = None

#Relative URL to output the tag RSS feed
#TAG_FEED_RSS  = None

#Maximum number of items allowed in a feed. Feed item quantity is unrestricted by default.
FEED_MAX_ITEMS = 0



#############################################################################
###########  分页设置 ###########################################################
#############################################################################

#The minimum number of articles allowed on the last page.
#Use this when you don't want the last page to only contain a handful of articles.
#DEFAULT_ORPHANS  = 0

#The maximum number of articles to include on a page, not including orphans.
#False to disable pagination.
DEFAULT_PAGINATION = 10

#A set of patterns that are used to determine advanced pagination output.
#PAGINATION_PATTERNS 用来配置创建的子页面，该设置是同序列的三元组，每个元组内容如下:
#(minimum page, URL setting, SAVE_AS setting,)
#如，PAGINATION_PATTERNS = (
#    	(1, '{base_name}/', '{base_name}/index.html'),
#   	(2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
#	)
#PAGINATION_PATTERNS =

#############################################################################
###########  云标签设置 ###########################################################
#############################################################################

#Count of different font sizes in the tag cloud
TAG_CLOUD_STEPS = 3

#Maximum number of tags in the cloud.
TAG_CLOUD_MAX_ITEMS = 100

TAG_CLOUD_SORTING = 'alphabetically'

#############################################################################
###########  翻译设置 ###########################################################
#############################################################################

#The default language to use.
DEFAULT_LANG = u'zh'

#Where to put the Atom feed for translations.
#TRANSLATION_FEED_ATOM = 'feeds/all-%s.atom.xml'
TRANSLATION_FEED_ATOM  = None

#Where to put the RSS feed for translations.
#TRANSLATION_FEED_RSS = None


#############################################################################
###########  内容排序设置 ########################################################
#############################################################################

#Order archives by newest first by date. (False: orders by date with older articles first.)
NEWEST_FIRST_ARCHIVES = True

#Reverse the category order. (True: lists by reverse alphabetical order; default lists alphabetically.)
REVERSE_CATEGORY_ORDER = False


#############################################################################
###########  主题设置 ###########################################################
#############################################################################

#Theme to use to produce the output.
#Can be a relative or absolute path to a theme folder, or the name of a default theme or a theme installed via pelican-themes
THEME = 'themes/pelican-bootstrap3'

#Destination directory in the output path where Pelican will place the files collected from THEME_STATIC_PATHS. Default is theme.
#THEME_STATIC_DIR  = 'theme'

#Static theme paths you want to copy. Default value is static, but if your theme has other static paths, you can put them here.
#If files or directories with the same names are included in the paths defined in this settings, they will be progressively overwritten.
#THEME_STATIC_PATHS  = ['static']

#Specify the CSS file you want to load.
#CSS_FILE  = 'main.css'

#A list of tuples (Title, URL) for additional menu items to appear at the beginning of the main menu.
MENUITEMS = (("首页","http://blackfox1983.github.io/"),
             ("关于", "/about.html"),)

#A list of tuples (Title, URL) for links to appear on the header.
# Blogroll
LINKS = (('Linux工具指南', 'http://linuxtools-rst.readthedocs.org/zh_CN/latest/'),
         ('Git指南', 'http://githowto.com/setup'),)

#A list of tuples (Title, URL) to appear in the “social” section.
# Social widget
SOCIAL = (('我的微博', 'http://weibo.com/blackfox1983/'),
          ('百度', 'http://www.baidu.com/'),
          ('Google', 'http://google.com.hk/'),
          ('GitHub', 'https://github.com/'),
          )

# 社区评论系统的用户名
#DISQUS_SITENAME = u'blackfox1983'
#DUOSHUO_SITENAME = u'blackfox1983'

###############################################################################
####For pelican-bootstrap3
###############################################################################

#show the author of the article at the top of the article and in the index of articles
SHOW_ARTICLE_AUTHOR = True

#show the Category of each article
SHOW_ARTICLE_CATEGORY = True

#show the article modified date next to the published date.
SHOW_DATE_MODIFIED = True

PYGMENTS_STYLE = 'colorful'

#使用pelican-bootstrap3.CUSTOM_CSS来调整代码行、代码区域展现风格
CUSTOM_CSS = 'static/custom.css'

USE_PAGER = True

DOCUTIL_CSS = True

#SITELOGO = 'images/site_logo.gif'

FAVICON = 'images/favicon.jpg'

BANNER = 'images/site_logo.gif'

#BANNER_SUBTITLE = ''

BANNER_ALL_PAGES = True

ABOUT_ME = '<a href="mailto:blackfox1983@163.com?subject=博客来信">联系我</a>'

AVATAR = '/images/profile.jpg'

BOOTSTRAP_NAVBAR_INVERSE = True

CC_LICENSE = 'CC-BY-NC-SA'

#通过修改模板templates/base.html，支持百度统计
CUSTOM_JS = 'static/baidutongji.js'
