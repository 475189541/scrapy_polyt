# scrapy_polyt
### 基于Scrapy的Python3.6 保利剧院抢票爬虫

+ middlewares.py: 重试中间件。
+ settings.py: Scrapy默认设置。
+ spiders_polty.py: 保利爬虫程序。
+ starts.py: 调试启动文件入口。
+ 欢迎有能力的开发者共同维护，半年之内此项目我还会继续跟进。
+ 对喜爱音乐剧的用户(非黄牛党)提供技术支持。
+ 问题和讨论可以发到我的邮箱475189541@qq.com。
+ 爬虫环境部署于linux环境，windows环境下的问题不予解答。

### 实现功能
```
1.一键登录。
2.自动按照条件搜索符合条件的剧。
3.加快订单的生成逻辑。
4.自动创建订单，登录web版保利剧院官网，在我的订单上有显示，剩下的手动付款。
5.简化订单创建逻辑，最快2秒能完成第１，２，３，４步骤。
6.代码中很少使用外部库，方便部署安装。
7.对于保利官网基于cookie的反爬机制，已经通过解js破解了acw_sc__v2的计算过程。
```

### 项目由来

```
1.人工抢票抢了很多次抢不到。
2.带宽有限，等加载完html + js + css + image　票早没了。
3.黄牛人数众多，大量囤积门票，并且装备优良，实在拼不过。
4.给普通用户提供一个可以和黄牛抗争的工具。
```

### 使用教程

#### 1.运行前你需要安装并配置好环境：

+ Python 3.6
+ Scrapy
+ curl

#### 2.环境安装

+ 切换至与requirements.txt同级目录
+ pip install -r requirements.txt
+ sudo apt-get install -y curl

#### 3.调试运行

+ 切换至与starts.py同级目录下
+ 终端命令行键入python starts.py

#### 4.部署运行(Linux)

+ 终端命令行键入scrapydart
+ 打开一个新的终端 切换至starts.py同级目录下 命令行键入scrapyd-deploy -p scrapy_polyt
+ 打开浏览器，输入地址　http://localhost:6800/
+ curl http://localhost:6800/schedule.json -d project=scrapy_polyt -d spider=spiders_polyt

#### ５.部署运行(Windows)

+ 与Linux类似，但是坑较多，不予解答


