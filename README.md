# 游戏服务器学习笔记1------介绍firefly，twisted

实在对不住大家，我不会编辑README.md 。
这篇文字是用mac版本的word编辑的，粘贴到这里以后很多地方格式都乱了，尤其是代码非常影响阅读。
请大家下载这个REAME.md文件然后用word打开，阅读效果会比较好。sorry

Chapter 1  简介
不懂后台的前端不是一个好美工！

目前的全部学习代码已经上传： https://github.com/chenee/firefly_study；后面的笔记会参考这份学习代码。
文档同发我的csdn博客：http://blog.csdn.net/chenee543216

最近在看firefly的代码，想想不如精读一下，果断入门server编程吧。
我会分步post关于firefly的代码阅读和学习笔记。

首先，firefly是国人开源的server，非常值得推介。网站：   www.9miao.com,  QQ群：153643834

firefly是基于twisted开发的，关于twisted和firefly的详细内容，我会结合使用的地方进行介绍。


另外由于我压根是入门菜菜，所以必须有很多错误需要大家来批评，鞭策，指正。在这里先谢过。


 
# 游戏服务器学习笔记 2————   准备工作

我看的firefly版本是 for 暗黑世界的， 服务器版本 1.6 ,客户端版本 1.4; 下载地址为： www.9miao.com ,官网里面找，需要铜板 ☺ 。

客户端是用cocos2dx-V2.1.4实现，由于是分析server代码所以，client端我会在需要的时候简单提一下。不做重点。

服务端代码实际上分成2个部分，需要安装的firefly python库和直接运行的暗黑世界python 代码。

这里是官方的wiki： http://firefly.9miao.com/diabloworld_wiki/index.htm
搭建环境问题，我就不赘述了。到这里假设大家server和client都跑了起来，并且功能正常。（如果有安装问题可以去9秒论坛问）

ok，由于是要研究server代码，所以我们直接把firefly从系统安装目录copy到当前的Diablo目录。然后删掉firefly安装包。（假设大家已经知道python 库的安装相关知识）

我用的是mac系统，终端ls看的话，目录结构应该是这样。
app            appmain.py     config.json    firefly        memcached.sh   startmaster.py tags           tool

这两个是我自己加的。
memcached.sh : (memcache 命令自己google)
$ cat memcached.sh 
memcached -d -m 100 -c 1000 -u root -p 11211
tags: ctags –R的生成文件（ctags自己google）

OK，下面可以开始读代码了。
这里推荐一下pyCham，这个python编辑器非常好用
游戏服务器学习笔记 3————   firefly 的代码结构，逻辑

注：以下所有代码都是拿暗黑来举例，由于本人能力有限很多地方还没有看透彻，所以建议大家只是参考。有不对的地方非常欢迎指正。

一、结构	
系统启动命令是，python statmaster.py,启动以后可以通过ps看到系统启动了以下几个进程：
1、master:管理模块，通过subprocess.Popen()来启动其它模块，该模块启动一个webserver，简单的通过监听本机9998端口，用get方法来获取用户管理命令，目前默认的是2条命令，stop和reload，负责其它模块的stop，reload功能。
只要在本机浏览器输入：http://localhost:9998/stop 或者http://localhost:9998/reload 即可。
2、dbfront：数据库前端模块，负责管理DB和Memcache。比如load用户信息到memcache中，定期（系统写死了1800秒）刷新并同步memcache.
3、gate：这个其实是真正的center，其它模块（除了dbfront）都会和这个模块挂接（通过twisted.pb  后面会抽空详细说明）。
4、net：网络模块，负责监听客户端tcp/ip连接，转发相应的命令数据包给gate。
5、game1：暗黑世界的游戏模块，这个模块里面会处理几乎所有的游戏逻辑，存储所有的游戏数据：比如角色升级的经验等级，各种npc信息，各种掉落信息，各种战斗阵型。这些数据在系统启动前都是保存在mysql里面，game1模块负责load到自己的内存里面（注意，不是memcache里面，而是直接内存）
6、admin：系统管理员模块，其实这个模块对于游戏本身来说，可有可无，主要作用就是导出游戏统计数据，比如在线人数，每天充值数量等等。。。。无非就是简单的load数据库内容在简单做些计算而已，我们不做重点。


二、逻辑	
系统启动的过程是：(只看firefly，不管memcache，mysql等)
$ python startmaster.py
startmaster.py 这个python脚本会实例化class master；
按照顺序启动
一个pb.root 
一个webserver
然后是subprocess.Popen（cmd) 来启动其它子模块。
cmd命令打印出来为：
python appmain.py dbfront config.json
python appmain.py gate config.json
python appmain.py net config.json
python appmain.py game1 config.json
python appmain.py admin config.json

全部启动起来以后，逻辑关系如下：

![逻辑关系示意图](http://www.9miao.com/data/attachment/forum/201401/07/175211ylijjha1h9ah12d1.jpg)
 

master虽然通过红线连接每个模块，但是实际上的工作只是启动和管理，并没有很大的数据交互。
Admin模块虽然挂在这里，但是其基本上只负责统计和“管理员”功能。
大的数据交流，网络服务，游戏逻辑等工作只发生在gate，net，game1 这几个节点。并且根据游戏内容不一样，完全可以进行扩展。（由于俺没有研究过，先不在这里讨论）。



OK，架构简介到这里，后面我们每个模块分开详细介绍。



# 游戏服务器学习笔记 4————   master 模块介绍

（模块的介绍方法都是先说大体功能，在捡一些细节详细讨论。）

master 类很简单，就3个函数，一个init，设置配置信息，并调用masterapp，然后还有一个循环启动子进程的start函数。
这里只有masterapp函数值得我们关注。
代码如下：

 36     def masterapp(self):
 37         config = json.load(open(self.configpath,'r'))
 38         mastercnf = config.get('master')
 39         rootport = mastercnf.get('rootport')
 40         webport = mastercnf.get('webport')
 41         masterlog = mastercnf.get('log')
 42         self.root = PBRoot()
 43         rootservice = services.Service("rootservice")
 44         self.root.addServiceChannel(rootservice)
 45         self.webroot = vhost.NameVirtualHost()
 46         self.webroot.addHost('0.0.0.0', './')                                                                        
 47         GlobalObject().root = self.root
 48         GlobalObject().webroot = self.webroot
 49         if masterlog:
 50             log.addObserver(loogoo(masterlog))#日志处理
 51         log.startLogging(sys.stdout)
 52         import webapp
 53         import rootapp
 54         reactor.listenTCP(webport, DelaySite(self.webroot))
 55         reactor.listenTCP(rootport, BilateralFactory(self.root))


实际上我不喜欢这种编码风格，感觉有点乱，有些过度使用import和python的修饰符。
仔细看，这里首先通过config.json读取配置信息，然后根据配置信息，起一个pb.root,和一个webserver，然后给pb.root 加一个services，这个services类是个非常重要的类，贯穿整个系统。我们下面会详细介绍它。 这里还通过import  webapp 和修饰符@xxx的方法来实现给webserver添加stop 和reload 2个child。实现的功能，我前面其实已经是说过。就是在浏览器里面输入 http://localhost:9998/stop 或者http://localhost:9998/reload 来调用对于的类。具体实现的方法是：
webroot = vhost.NameVirtualHost()
 webroot.putChild(cls.__name__, cls()) ；        
这个vhost.NameVirtualHost().putChild()函数也是twisted的函数，和前面pb.root一样，大家如果等不及我后面的解说可以自己google到twisted网站，上面有详细的doc、samples。

由于看的实在不习惯（可能自己是python、server的新手），所以我就自己按照功能实现改了一下结构，如下，希望大家对比可以更加清晰。（我改动后的所有代码都会抽空上传到github。地址为： https://github.com/chenee 如果没有说明我还没来得及上传，在等等，或者直接M我要。）

22 class Master:
 23     def __init__(self, configpath, mainpath):
 24         """
 25         """
 26         self.configpath = configpath
 27         self.mainpath = mainpath
 28 
 29         config = json.load(open(self.configpath, 'r'))
 30         mastercnf = config.get('master')
 31         self.rootport = mastercnf.get('rootport')
 32         self.webport = mastercnf.get('webport')
 33         self.masterlog = mastercnf.get('log')
 34 
 35     def __startRoot(self):
 36         root = PBRoot("rootservice")
 37         GlobalObject().root = root
 38         reactor.listenTCP(self.rootport, BilateralFactory(root))
 39 
 40 
 41     def __startWeb(self):
 42         webroot = vhost.NameVirtualHost()
 43         webroot.addHost('0.0.0.0', './')
 44         GlobalObject().webroot = webroot
 45         webapp.initWebChildren()                                                                                     
 46         reactor.listenTCP(self.webport, DelaySite(webroot))
 47 
 48 
 49     def startMaster(self):
50 
 51         self.__startRoot()
 52         self.__startWeb()
 53 
 54         if self.masterlog:
 55             log.addObserver(loogoo(self.masterlog))#日志处理
 56         log.startLogging(sys.stdout)
 57 
 58         # reactor.run()
 59 
 60     def startChildren(self):
 61         """
 62         """
 63         print "start children ......"
 64         config = json.load(open(self.configpath, 'r'))
 65         sersconf = config.get('servers')
 66         for sername in sersconf.keys():
 67             cmds = 'python %s %s %s' % (self.mainpath, sername, self.configpath)
 68             subprocess.Popen(cmds, shell=True)
 69         reactor.run()   

我把原先通过addServiceChannel（）添加services的过程放到PBRoot类的__init__里面了，这样改动也适合后面其它模块，反正root逻辑上肯定是需要一个services的。而且这个services就是普通services。（后面还会提到一些services的子类）

另外，把原先通过import webapp 加用修饰类实现的putChild（）功能，直接写到一个注册函数里面。
45   webapp.initWebChildren()                                                                                     
   		 addToWebRoot(stop)
   		 addToWebRoot(reloadmodule)

改动以后的功能和原先一模一样，改动后的代码对我等新手来说可以清晰的看到master模块的结构



OK，下面我们来看刚才提到的services。客户端所有的命令最终都是通过services的    
             callTarget(self, targetKey,*args,**kw) 函数来分发。
比如client端发一条编号为01的命令，或者一条“login”命令，server端到底执行什么处理函数，就是通过services来实现的，具体实现实际上就是在services类里面通过
          self._targets = {} # Keeps track of targets internally
这个字典来保存命令ID/名称 和具体命令实现函数的对应关系。
注册、和注销这个对应关系的函数为services类的：mapTarget（） 、unMapTarget（）。

每个模块（master，gate，net。。。）都有对应的services，但是可能不止一个。
模块之间提供服务，也是通过实现一个services实例，并注册一批相应处理函数来实现的。


OK，到这里master基本介绍完毕。
由于master的webserver功能比较简单，而且和系统的其它模块基本无关。大家可以通过twisted官网的DOC和sample来了解，我就不赘述了。

API:
http://twistedmatrix.com/documents/10.2.0/api/twisted.web.vhost.NameVirtualHost.html 

Twisted Web In 60 Seconds：
https://twistedmatrix.com/documents/current/web/howto/web-in-60/index.html

下篇文章我尽力介绍twisted的PB（Perspective Broker,透明代理）
 
# 游戏服务器学习笔记 5————   twisted Perspective Broker 透明代理

实际上这章压根不需要我来说，twisted官网的Doc里面有专门介绍的章节。写的非常详细。
http://twistedmatrix.com/documents/current/core/howto/index.html

我只能肤浅的说说firefly里面对PB的运用。

首先firefly使用PB的目的是实现各个模块之间的通信，做到“分布式”，逻辑分离。

比如master模块专门负责控制，gate做分发，game1做游戏逻辑，net做网络相关。如果不用twisted.pb的话，我们就要自己写复杂socket逻辑，来实现各个节点之间的数据通讯。
现在有了twisted.pb，“妈妈再也不用担心我的学习”。

Firefly所有的分布式相关代码都在firefly/distribute/目录
__init__.py  child.py     manager.py   node.py      reference.py root.py

root.py 实现PB的server功能
node.py 实现PB的client功能。
child.py 每个client连接上root都会初始化一个child来保存该client的相关信息，并且将这些child通过manager来管理。
manager.py 管理root的child，通过一个字典self._childs = {}，实现一个增删改的小管理器。
reference.py 如果你看了前面twisted官网的介绍就会知道，node只要实例化一个 pb.Referenceable 类，并把它传递给root，那么root就能够把这个pb.Referenceble当成句柄来远程调用client的函数。



前面章节提到master模块实现了一个PBRoot作为server等待client端的连接。我们这里先拿DB模块来说明。（DB模块的其它功能，和我改写的部分后面会详细介绍。）

master模块里面实现的代码如下（这个是我改过的代码，稍后上传git）：
38     def __startRoot(self):
 39         GlobalObject().root = PBRoot("rootservice")
 40         reactor.listenTCP(self.rootport, BilateralFactory(GlobalObject().root))

其中PBRoot类有2个关键函数。

   def remote_register(self,name,transport):
        """设置代理通道
        @param addr: (hostname,port)hostname 根节点的主机名,根节点的端口
        """
        log.msg('node [%s] registerdd' % name)
        child = Child(name,transport)
         # child.setTransport(transport)
        self.childsmanager.addChild(child)

    def remote_callTarget(self,command,*args,**kw):
        """远程调用方法
        @param commandId: int 指令号
        @param data: str 调用参数
        """
        data = self.service.callTarget(command,*args,**kw)
        return data

remote_register(),这个函数名称被我改了，原先好像叫做remote_takeproxy()。大家理解的角度不一样，原先作者lan可能是认为这个函数的功能是root取得其它模块提供给他的代理。我认为，这个函数是其它模块注册到root。

PB的约定是，本地函数起名remote_xxx(),远程函数调用 直接callremote（“XXX”)，所以按照习惯，大家看到的remote_xxx()函数都是提供给对方调用的。

另外，这里补充一下，twisted官网提到，PB一旦建立好连接以后，server和client的行为其实是对等的，大家权限，调用都一样。

再看一下上面2个函数，regist可以看出就是用child类来保存一下注册过来的client。callTarget函数就是通过services来执行远程的调用命令。具体的callTarget逻辑后面有空再介绍。


下面 我们看client端，拿DB来说。和master模块不一样，其它模块，包括dbfront，启动过程依赖配置文件config.json的设定后面详细讨论。这里我们只关注PB相关。

下面的代码取自firefly/server/server.py
(实际上已经被我整理过，但具体代码逻辑还是一样)
59         if masterconf: #这里一定为True
 60             masterport = masterconf.get('rootport')
 61             self.master_remote = RemoteObject(servername)
 62             addr = ('localhost',masterport)
 63             self.master_remote.connect(addr)
 64             GlobalObject().masterremote = self.master_remote

这里的RemoteObject类的初始化__init__函数如下：（firefly/distribute/node.py)
   def __init__(self,name):
 23         """初始化远程调用对象
 24         @param port: int 远程分布服的端口号
 25         @param rootaddr: 根节点服务器地址
 26         """
 27         self._name = name
 28         self._factory = pb.PBClientFactory()
 29         self._reference = ProxyReference()#这个就是pb.Referenceable的子类
 30         self._addr = None



可以看出我们实现了一个RemoteObject类，这个类包括了pb.PBClientFactory 和pb.Referenceble。在line 63对应的代码里面，我们connect的时候
        reactor.connectTCP(addr[0], addr[1], self._factory)
就建立了一个root和node的连接。然后再调用下面的函数。

    def register(self):
        """把本节点注册到RootNode,并且向RootNode发送代理通道对象
        """
        deferedRemote = self._factory.getRootObject()#取得root的调用句柄。
        deferedRemote.addCallback(callBack,'register',self._name,self._reference)#callBack函数会调用pb.callRemote（）

这个函数就2行，第一行是twisted.pb的client取得root的句柄，有了这个句柄，我们就能够通过callRemote来调用root的相应函数。这里调用的regist，对应root的remote_regist()函数，并且把自己的referenceble传递给root，那么后面root就可以通过这个referenceble来调用自己（node）了。


OK，firefly对twisted.pb的封装和实现就介绍到这里。PB的介绍先告一段落，由于俺能力实在有限，可能大家还没有看清楚。
别担心，我们后面接着介绍各个模块的过程中也会穿插firefly的PB运用的细节介绍。之后如果有时间精力我们再对各个模块中运用PB实现的功能做个总结。
 
# 游戏服务器学习笔记 6————   db模块

前面介绍过master模块，现在我们看看dbfront模块，源码在firefly/dbentrust和app/defront 目录。
顾名思义 entrust 就是数据库托管的意思。这个模块实现的功能就是负责从数据库读取数据，并且缓存到memcache。然后定期的检查缓存并写入更新到DB。

刚刚看到9秒论坛里面有篇文章介绍这个dbentrust库的左右。写的很详细。地址如下：
       ht空格tp://www.9miao.com/thread-44002-1-1.html
既然文章已经写了很详细的说明，我就偷懒了：）

下面我主要介绍一下db整体模块的结构，流程，逻辑。
前面的章节应该提到过，除了master模块以外，其它模块（db，gate，net，game1，admin）都是通过master的子进程方式启动。启动代码如下：

    def startChildren(self):
        """
        """
        print "start children ......"
        config = json.load(open(self.configpath, 'r'))
        sersconf = config.get('servers')
        for sername in sersconf.keys():
            cmds = 'python %s %s %s' % (self.mainpath, sername, self.configpath)
            subprocess.Popen(cmds, shell=True)
        reactor.run()

通过简单加打印便可以发现，这里其实就是“python appmain.py db config.json”

OK，那么我们可以抛开master，单独命令行启动这个db模块。
为了更加清晰的学习代码，我已经把每个模块单独分离开，具体分离后的代码请看github。 地址为：htt空格ps://github.com/chenee/firefly_study 

我们下面自己那这份代码解说，大家可以对照源代码进行学习。
（说明，这份代码只是为了学习才拆分开，会存在很多冗余，甚至不一致的地方。仅供参考）
代码目录如下：
1 .                                                                                                                    
  2 ├── app  #原先的游戏逻辑目录，这个和firefly库目录对应，存放游戏具体实现。但是这里被我打乱了。
  3 │   ├── __init__.py
  4 │   ├── dbfront  #数据库操作相关文件目录
  5 │   │   ├── McharacterManager.py #角色管理操作文件，从数据库读取所有角色信息，缓存到memcache
  6 │   │   ├── __init__.py
  7 │   │   ├── initconfig.py  #db模块中游戏部分的初始化文件，负责app目录的内容的加载。
  8 │   │   ├── madminanager.py #MAdmin 类的管理类。Madmin下面会提到。
  9 │   │   ├── mcharacter.py #角色类，角色在memcache中的映射。
 10 │   │   └── memmode.py #几个Madmin类的初始化工作
 11 │   ├── dbfrontserver.py  #启动接口，唯一作用就是调用initconfig.py
 12 │   ├── logs
 13 │   │   └── dbfront.log #log 文件
 14 │   └── share
 15 │       ├── __init__.py
 16 │       └── dbopear   #数据库操作文件，对于db模块来说就只使用了一个文件，typo！
 17 │           ├── __init__.py
 18 │           └── dbCharacter.py # tb_character角色表的select，update封装类。
 19 ├── appmain.py  #启动脚本，读config.json配置文件然后初始化DB模块类
 20 ├── config.json  #配置文件，非常重要的文件
 21 ├── dbpool.py #db连接池，原先的文件只提供初始化和取连接池的2个函数。感觉很多dbopear目录的的sql操作完全可以封装，具体见我game1模块里面的改动，其它几个模块的文件可能不同步。最终会按照game1的模式整合。
 22 ├── dbserver.py #db模块的类文件，这个对于原先FFServer。针对每个模块我把他改成对应名称，便于理解
 23 ├── globalobject.py #全局类，这里的全局指每个模块内部的全局，而不是整个系统的全局。每个模块自己的globalobject类完全可以不同。
 24 ├── leafnode.py #就是原先的node.py，在PB那个章节我们介绍过。
 25 ├── logobj.py #log 类
 26 ├── memclient.py #memcache的客户端实现，提供对memcache的访问操作接口
 27 ├── memobject.py # memcached 关系对象通过key键的名称前缀来建立
各个key-value 直接的关系; 比如memobject.name = “tbl_role”, 那么memobject.get(“id”)得到的就是tbl_role:id的值。 
 28 ├── mmode.py #里面包括2个重要的类，MMode,MAdmin;都是memobject的子类，逻辑上MMode代表内存中的一条数据，MAdmin，代表内存中的一张表。而前面madminanager.py就是这些表的管理类。
MAdmin对应memcache的前缀是表名称：如 tb_item
MMode对应memcache的前缀是pk(primary key，主键ID)。如 tb_item:1001
那么基本的一条数据组织的格式是：tbl_item:1001 {id:10001, name:chenee , money:10000};也就是memcache的key是 “ 表名称:该条的主键值”，value是这条内容的json格式。

验证方式，可以telnet到memcache打印出来看结果。（以前做的，现在记不清了，可能有误，此刻我自己还木有验证）

 29 ├── reference.py #PB 相关，看前面一章介绍
30 ├── run.sh #shell启动脚本,为了方便，我自己写的。
 31 ├── serviceControl.py #对应原先的一个叫做admin.py的文件，其实就是给leafnode加2条命令（stop，reload）这个在PB章节也说过了。
 32 ├── services.py #服务类，前面提过
 33 ├── singleton.py #单例类，我blog上面有相关阐述，后面一章我粘贴过来。
 34 └── util.py #大部分都是sql查询操作的封装函数。
 35 


仔细看完上面目录介绍，基本上应该对DB的结构有个大致掌握了。下面我们分析一下源码。
启动db模块的命令：
$cat run.sh 
python appmain.py
appmain.py 便于学习被我改动过了，如下：
if __name__ == "__main__":
    servername = "dbfront"
    config = json.load(open("config.json", 'r'))

    dbconf = config.get('db')
    memconf = config.get('memcached')
    sersconf = config.get('servers',{})
    masterconf = config.get('master',{})
    serconfig = sersconf.get(servername)

    ser = DBServer()
    ser.config(serconfig, dbconfig=dbconf, memconfig=memconf,masterconf=masterconf)
    ser.start()

实际上就是实例化DBServer类，把从config.json文件读取的信息传递过去。DBServer就是原先firefly/server/server.py文件。改个名字好看。
config.json 也被我改了一下，“services”里面只保留“dbfront”，其它都services内容都无关。就不贴出来了，占地方。

现在看DBServer（FFServer）类：
class DBServer:

    def __init__(self):
        """
        """
        self.leafNode = None
        self.db = None
        self.mem = None
        self.servername = None

    def config(self,config,dbconfig = None,memconfig = None,masterconf=None):
        """配置服务器
        """
        servername = config.get('name')#服务器名称
        logpath = config.get('log')#日志
        hasdb = config.get('db')#数据库连接
        hasmem = config.get('mem')#memcached连接

        app = config.get('app')#入口模块名称

        self.servername = servername

        if masterconf:
            masterport = masterconf.get('rootport')
            addr = ('localhost', masterport)
            self.leafNode = leafNode(servername)
            self.leafNode.connect(addr)
            GlobalObject().leafNode = self.leafNode


        if hasdb and dbconfig:
            log.msg(str(dbconfig))
            dbpool.initPool(**dbconfig)

        if hasmem and memconfig:
            urls = memconfig.get('urls')
            hostname = str(memconfig.get('hostname'))
            mclient.connect(urls, hostname)

        if logpath:
            log.addObserver(loogoo(logpath))#日志处理
        log.startLogging(sys.stdout)


        if app:
            reactor.callLater(0.1,__import__,app)


    def start(self):
        """启动服务器
        """
        log.msg('%s start...'%self.servername)
        log.msg('%s pid: %s'%(self.servername,os.getpid()))
        reactor.run()


根据config.json的解析结果，我们精简掉所有无关内容。发现，DB模块包括以下几个功能模块：
mastconfig #说明我们需要连接一个root，也就是前面提到的master模块
db #有数据库操作，需要建立数据池
mem #有memcache操作，要连接memcache。

所有连接信息，如ip、port等都是从config.json里面取得。
1、masterconfig部分，就是前面PB章节的介绍，这里实现leafNode去连接master模块的root，就不再赘述了。
2、db pool部分也很简单，就是建立一个pool，提供一个connection的接口。大家去了解DBUtils.PooledDB这个库就可以了。
3、mem部分，也没有啥可说，纯memclient就是调用python的Memcache而已，memcache的结构又超级简单，就是get，set。不含任何逻辑的。想要实现逻辑关系，都要自己去构建，就是上面我们提到的MMode和MAdmin等文件来实现。

OK，firefly库部分的调用完毕，这个时候DB模块已经建立了，和master的PB连接，数据池，memcache连接。下面就是游戏内容部分的实现了。

除了master模块，其它所有模块的游戏部分（app目录下面的内容）都是通过
        if app:
            reactor.callLater(0.1,__import__,app)
这种方式来import进来的。对我这种python新手还真的迷惑的半天。实际上就是根据config.json里面对于app项的内容。对于db这里展开是：
   reactor.callLater(0.1,__import__, app.dbfrontserver)
就是过0.1秒执行 import app.dbfrontserver。其内容如下：
GlobalObject().stophandler = initconfig.doWhenStop
initconfig.loadModule()
loadModule（）干3件事情：
def loadModule():
    register_madmin()
    initData()
    CheckMemDB(1800)
注册几个表，初始化角色数据到内存，同步内存数据到数据库

注册表的代码在mmode.py中，过程就是实例化几个MAdmin来表示相应表的结构，然后添加到MAdminManager这个单例管理类中。
MAdmin有几个属性代表表的主键，外键，表名称等信息。
MAdmin的insert函数会调用父类的Memobject的insert函数。
        nowdict = dict(self.__dict__)
        del nowdict['_client']
        newmapping = dict(zip([self.produceKey(keyname) for keyname in nowdict.keys()],
                              nowdict.values()))
        self._client.set_multi(newmapping)
实际上就是根据self的所有属性（除了_client,这个属性指的是memclient）来生成一个字典，然后把这个字典的内容缓存到memcache中。
比如tb_item表对应的MAdmin,生成的memcache内容就包括（不限于）
Key                      value
tb_item:_name      xxxx
tb_item:_lock      xxxx
tb_item:_fk      xxxx
tb_item:_pk    xxxxx
这里其实只是把表结构给缓存到memcache了，压根没有碰表的数据。MAdmin有几个个函数可以取数据，
load（）#这个是根据表名称，select * 并且一条一条生成MMode，然后缓存进memcache，MMode前面提到过，代表一条数据的内存对应数据结构。

getObj(self,pk): #先判断pk这条数据是否在memcache，是否有效，如果没有再从数据库取出来并同步到memcache中。

这两条函数其实在db模块启动过程中都没有被调用，（可以加断点或者打印验证）

OK，分析到这里下面在看角色初始化initData()的部分就简单了
   def initData(self):
        allmcharacter = dbCharacter.getALlCharacterBaseInfo()
        for cinfo in allmcharacter:
            pid = cinfo['id']
            mcha = Mcharacter(pid, 'character%d' % pid, mclient)
            mcha.initData(cinfo)
Mcharacter也是MemObject的子类，做的就是根据数据库中的角色信息实例化Mcharacter内存数据，然后调用memobject的insert同步到memcache。
取角色信息的过程相反。调用mcharacterinfo（）函数，唯一一点不同是，这个函数有@property修饰，我查了一下，表示这个函数可以当成属性来用，python真酷！


这里吐槽一下注释： 摆明是从啥地方copy过来的，注释的牛头不对马嘴，害的我看了老半天，都木有想明白。
"""初始化城镇要塞对象
        @param territoryId: int 领地的ID
        @param guard: int 殖民者的ID
        @param guardname: str 殖民者的名称
        @param updateTime: int 领地被更新的时间
"""
最后再唠叨一下checkAdmins（）；这个函数负责每隔1800（magic number）秒刷一边MAdminManager类管理的所有MAdmin（表）。调用这些MAdmin对应的checkAll（）；
这个checkAll函数会取得memcache中所有缓存数据，比较是否以本表前缀开头，如果是，则判断这些是否有效，是否过期，是否需要写入数据库。。。。

在我看来，这里有些可以优化的逻辑。比如把取memcache所有数据的步骤提到MAdminManager层面，这样每个MAdmin就不用单独执行一遍。
但是如果是多个memcache服务器，又该怎么办？各种头疼，问题太多，智商不够用。

这个函数是魔鬼，我暂时没有敢去动它，等我多学习学习相关内容再去做优化。

 
# 游戏服务器学习笔记 ： 番外篇———Python 单例介绍
__metaclass__方式实现

1 首先网上有很多实现方式，而且stackflow里面有大神详细介绍了各种实现。自己google吧，就不贴URL了。

我这里简述原理，放个简单demo帮助理解。
  1 class Singleton(type):                                                                                               
  2     def __init__(self, name, bases, dic):
  3         print ".... Singleton.init ...."
  4         super(Singleton, self).__init__(name, bases, dic)
  5         self.instance = None
  6 
  7     def __call__(self, *args, **kwargs):
  8         print ".... Singleton.call ...."
  9         if self.instance is None:
 10             self.instance = super(Singleton, self).__call__(*args, **kwargs)
 11         return self.instance
 12 
 13 print "====================== 1 ======================="
 14 class test:
 15     __metaclass__ = Singleton #call Singleton.__init__
 16     def __init__(self):
 17         print "test.init ..."
 18     def __call__(self):
 19         print "test.call ..."
 20 
 21 class test2:
 22     __metaclass__ = Singleton #call Singleton.__init__
 23     def __init__(self):
 24         print "test2.init ..."
 25     def __call__(self):
 26         print "test2.call ..."
 27 
 28 print "====================== 2 ======================="
 29 a = test() #call Singleton.__call__
 30 b = test2() #call sSngleton.__call__
 31 
 32 print "====================== 3 ======================="
 33 a1 = test()
 34 b1 = test2()
 35 print id(a),id(a1),id(b),id(b1)
 36 print "====================== 4 ======================="
 37 a1()
 38 b1()
 39 
 40 print "====================== 5 ======================="
 41 a.c = 100
 42 b.c = 111
 43 print a1.c
 44 print b1.c


输出结果：

1  bash-3.2$ python test.py 
2  ====================== 1 =======================
3  .... Singleton.init ....
4  .... Singleton.init ....
5  ====================== 2 =======================
6  .... Singleton.call ....
7  test.init ...
8  .... Singleton.call ....
9  test2.init ...
10 ====================== 3 =======================
11 .... Singleton.call ....
12 .... Singleton.call ....
13 4476624848 4476624848 4476670096 4476670096
14 ====================== 4 =======================
15 test.call ...
16 test2.call ...
17 ====================== 5 =======================
18 100
19 111





demo中建了2个单例类，test，test2。都是通过__metaclass__ = Singleton的方式。
测试结果：
通过测试输出可以看出，id(a) = id(a1),id(b)=id(b1); 而且创建一个c attribute给a，a1同时也会得到一个一模一样的c，包括c的值。 说明单例OK。

原理：
这里单例是用__metaclass__方式实现。__metaclass__的意思就是class的class。
所以一旦设定test和test2的__metaclass__ == Singleton，就会利用Singleton类的实例来作为test，test2的类。（稍微有点拗口）

请注意line 14和line 22，这2个地方对应输出结果里面line 2,line3的打印。说明：我们一旦设定test，test2的__metaclass__ = Singleton了，Singleton就立刻__init__ ，而且对于每个单例类（这里的test或test2）只在定义的时候做一次。

后面我们实例话test，test2的时候：a = test(),b=test2();则系统会调用Singleton的__call__；实例化几次test,test2,就调用几次Singleton的__call__ 。 所以，我们只要在Singleton的__call__里面做单例的实现即可。

具体实现方式很简单，看源码即可。

补充一下：
test类的__init__ 函数对应 a=test()调用
__call__函数对应 a()
 
# 游戏服务器学习笔记 7 ————   gate模块

前面说过db模块，子模块的启动部分基本都差不多。所以我只介绍不同的地方。gate模块和db模块不同的地方是，gate即作为master的leafnode，同时自己也作为其它模块（net，game1，admin）的root，代码如下。
        if rootport:
            self.root = PBRoot("rootservice")
            reactor.listenTCP(rootport, BilateralFactory(self.root))
            GlobalObject().root = self.root
大家如果看过前面的章节会发现这段代码也很熟悉，对! 它就是master模块的__startRoot函数一样的功能。我们前面在PB章节也详细介绍过。

OK，gate启动代码算介绍完了（怎么感觉什么都没有说呢？），大家瞅一眼我在github上的代码就一目了然了。

下面介绍gate的游戏部分内容，即app目录下面的内容。

这部分代码和db对应部分的调用过程一模一样，我们直接运行到app/gateserver.py。
就一行代码，
initconfig.loadModule()
跟进去发现代码如下：（代码我改过）
def loadModule():
    rservices.init()
    lservices.init()
实际上gate的app部分工作只是注册root services和local services的命令。
前面我们强调过services，是非常重要的类，系统通过这个类来实现具体功能。一个模块可能有多个services。这里我们就碰到了这种情况。

gate模块有3个services，他们分别是：
1、与master通讯的leafNode的services，包括2条命令：stop和reload。

2、自己作为root的services，通过上面loadModule（）里面的rservices.init()注册以下几个命令。代码在：app/gate/rootservice/rservices.py (见我github的目录结构)
def init():
    addToRootService(forwarding)
    addToRootService(pushObject)
    addToRootService(opera_player)
    addToRootService(netconnlost)
3、一个挂接在    GlobalObject().localservice 的services，这个services通过lservices.init()注册3条命令，如下：
    addToLocalService(loginToServer_101)
    addToLocalService(activeNewPlayer_102)
    addToLocalService(roleLogin_103)

其中 services 1 是leafnode的services，所以会被作为root的master调用。
services  2 是自己作为root的services，所以会被gate的leafnode（net，game1，admin等）调用。
而services  3并没有挂接到某个PB端（root，或者node），它是在services 2的forwarding（）函数中通过以下方式调用：
def forwarding(key,dynamicId,data):
    """
    """
    if key in GlobalObject().localservice._targets:
        return GlobalObject().localservice.callTarget(key,dynamicId,data)
    else:
               	 xxxxxx xxxxx xxxx #其它代码逻辑
所以，实际上services 3 可以看做services 2的一部分，只是实现上独立出来成为一个services而已。


我们前面PB章节已经说过firefly的分布式调用逻辑。这里补充一下。
net模块（后面会介绍）会receive客户端（cocos2dx）的数据包，解析出具体命令，然后通过PB的方式，把命令当成参数来远程调用gate的PBRoot的remote_callTarget（）函数。
而这个remote_callTarget()会进一步调用自己的services，也就是上面提到的services 2来处理命令。

For example:
（在firefly源码目录下面有一个tool目录，里面有测试代码clienttest.py可以用来做测试，我们后面介绍net模块的时候尽量详细扒数据，这里只是简单说一下示意流程）

1、客户端登陆，会发送用户名密码的json串给net模块
2、net模块解析出命令为：101， 参数为{username：xxx，password：xxx}；
3、net远程调用gate的remote_callTarget()函数。
4、remote_callTarget()调用PBRoot.services.callTarget，通过解析命令101取得对应的命令函数loginToServer_101（）并执行。（这个解析命令过程，就是前面提到mapTarget和unMapTarget函数实现）；

OK，数据流我们就简单提一下，帮助大家理解模块功能。后面在net，game1模块流程都介绍完毕以后，我们会专门用1，2个章节来仔细分析分析暗黑的数据格式和各种流程。如果有时间和精力，我们尝试反推一下策划，设计内容。

下面一章我们介绍net，再下一章介绍game1，admin就留给读者自己看吧。

 
# 游戏服务器学习笔记 8 ————   net模块

net顾名思义，就是网络模块，负责接受客户端的连接，处理客户端发送过来的数据，解包转发给其它模块。整个firefly系统里面，和用户打交道的也只有这个模块（admin和master虽然提供web操作接口，但是都是服务管理员的）。

我们前面提到，子模块的功能是由config.json来配置驱动的。那么我们看看这个模块的json文件定义了哪些功能。
20     "servers": {
 21         "net": {
 22             "app": "app.netserver", #具有游戏功能模块，在框架启动完毕后需要import app/netserver.py 文件
 23             "log": "app/logs/net.log", #日志
 24             "name": "net", #该模块的名称
 25             "netport": 11009, #!!重要！！ 定义了netport，则firefly会为其启动一个网络服务，来监听客户端连接。
 26             "remoteport": [  #需要连接其它node，这里的其它node定义的是gate。实际上我们可以有不止一个“gate”来实现分布式逻辑。
 27                 {
 28                     "rootname": "gate",
 29                     "rootport": 10000
 30                 }
 31             ]
 32         }                                                                                                     
 33     }


那么对应的启动代码如下：（init 和 start函数省略，只列出关键部分）

40     def config(self, config, dbconfig = None,memconfig = None,masterconf=None):
 41         """配置服务器
 42         """
 43         netport = config.get('netport')#客户端连接
 44         gatelist = config.get('remoteport',[])#remote节点配置列表
 45         servername = config.get('name')#服务器名称
 46         logpath = config.get('log')#日志
 47         app = config.get('app')#入口模块名称
 48         self.servername = servername
 49 
 50         if masterconf:
 51             masterport = masterconf.get('rootport')
 52             addr = ('localhost', masterport)
 53             leafnode = leafNode(servername)
 54             serviceControl.initControl(leafnode.getServiceChannel())
 55             leafnode.connect(addr)
 56             GlobalObject().leafNode = leafnode
 57 
 58         if netport:
 59             self.netfactory = LiberateFactory()
 60             netservice = services.CommandService("netservice")
 61             self.netfactory.addServiceChannel(netservice)
 62             reactor.listenTCP(netport, self.netfactory)                                                       
 63             GlobalObject().netfactory = self.netfactory
 64 
 65         for cnf in gatelist:
 66             rname = cnf.get('rootname')
 67             rport = cnf.get('rootport')

68             self.gates[rname] = leafNode(servername)
 69             addr = ('localhost', rport)
 70             self.gates[rname].connect(addr)
 71 
 72         GlobalObject().remote = self.gates
 73 
 74         if logpath:
 75             log.addObserver(loogoo(logpath))  #日志处理
 76         log.startLogging(sys.stdout)
 77 
 78         if app:
 79             reactor.callLater(0.1, __import__, app)
 80                                            

可以看出主要启动3个功能：
1、masterconfig部分，是说明本模块作为master模块的leafnode要连接master模块，这个和gate模块一样，可以参考前面PB的介绍章节。

2、连接gate模块，这里代码假定了不止一个需要连接的gate；但是实际上我们config.json里面只设定了一个。 这个步骤和连接master一样。

3、真正新鲜的东西是netport部分，这里	LiberateFactory实际上是protocol.ServerFactory的子类。它使用的协议是LiberateProtocol，这个是protocol.Protocol的子类。

如果大家了解twisted，那么我提到ServerFactory，和Protocol，大家就已经明白了netport部分的原理，压根不需要我废话。所以对于新人，不了解twisted，我们的主要任务是学习，并熟悉它。如下：

1、官网的介绍，这个比较简单，但是对于有经验的开发者来说，已经足够了解了（官网上面其它samples，也有不少是用protocol的)
ht空格t空格ps://twistedmatrix.com/documents/current/core/howto/servers.html

2、专门介绍twisted的书籍。有中文版的，内容我记得好像是比较浅显易懂。
h空格ttp://www.amazon.com/exec/obidos/ASIN/1449326110/jpcalsjou-20
第二章专门介绍protocol我就不多说了。

到这里我们假设大家已经熟悉twisted.protocol，那么我们看看firefly的实现部分。
大家知道twisted是事件驱动的，所以整个框架看起来很简单，我们即使对整体不熟悉，只要关注我们关心的事件处理函数部分也是ok的。

首先，
      reactor.listenTCP(netport, self.netfactory)
这里建立一个服务，等待客户端connect。 每次接收到一个client连接，Factory都会调用    Factory.protocol 也就是 LiberateProtocol来处理，类似fork的概念。Factory充当了一个LiberatePtotocol的管理者的角色，干活的还是LibrateProtocol。所以我们主要关心LiberatePtotocol，代码如下：
class LiberateProtocol(protocol.Protocol):
    """协议"""

    buff = ""

    def connectionMade(self):
        """连接建立处理
        """
        log.msg('Client %d login in.[%s,%d]' % (self.transport.sessionno,
                self.transport.client[0], self.transport.client[1]))
        self.factory.connmanager.addConnection(self)
        self.factory.doConnectionMade(self)
        self.datahandler = self.dataHandleCoroutine()
        self.datahandler.next()

    def connectionLost(self, reason):
        """连接断开处理
        """
        log.msg('Client %d login out.'%(self.transport.sessionno))
        self.factory.doConnectionLost(self)
        self.factory.connmanager.dropConnectionByID(self.transport.sessionno)

    def safeToWriteData(self,data,command):
        """线程安全的向客户端发送数据
        @param data: str 要向客户端写的数据
        """
        if not self.transport.connected or data is None:
            return
        senddata = self.factory.produceResult(data,command)
        reactor.callFromThread(self.transport.write,senddata)

    def dataHandleCoroutine(self):
        """
        """
        length = self.factory.dataprotocl.getHeadLenght()#获取协议头的长度
        while True:
            data = yield
            self.buff += data
            while self.buff.__len__() >= length:
                unpackdata = self.factory.dataprotocl.unpack(self.buff[:length])
                if not unpackdata.get('result'):
                    log.msg('illegal data package --')
                    self.transport.loseConnection()
                    break
                command = unpackdata.get('command')
                rlength = unpackdata.get('lenght')
                request = self.buff[length:length+rlength]
                if request.__len__() < rlength:
                    log.msg('some data lose')
                    break
                self.buff = self.buff[length+rlength:]
                d = self.factory.doDataReceived(self, command, request)
                if not d:
                    continue
                d.addCallback(self.safeToWriteData, command)
                d.addErrback(DefferedErrorHandle)

    def dataReceived(self, data):
        """数据到达处理
        @param data: str 客户端传送过来的数据
        """
        self.datahandler.send(data)


可以看到主要处理了3个事件。
connectionMade #客户端连接我们
connectionLost(self, reason) #连接丢失
dataReceived(self, data) #数据到达
当客户端连接的时候，我们会调用Factory的connectmanager（也是简单的一个管理类）来保存当前连接信息。
整个系统只有一个Factory类的实例，但是每当一个连接来的时候，都会fork一个Protocol的实例。所以信息都会保存在Factory的属性里面，比如Factory.connectionManager。
同理，当连接丢失的时候，我们调用connectionManager处理一下即可。没有什么复杂的。

我们主要关注的是数据到来的处理逻辑：
1、数据到达，我们简单的发送给处理函数：        self.datahandler.send(data)
2、这个处理函数包含了yield 语句所以它是一个生成器，generate。具体大家可以google  python yield，会有很详细的介绍文档。
这里只是告诉大家
2.1、datahandler函数，每次调用到yield的地方就会暂停，等待下次被next，或者send唤醒，然后从yield的地方继续执行。
2.2、data = yield，这条语句在被唤醒后 data就被赋值为 send传递进来的参数。
2.3 那么这个函数改写成这样，大家就很容易理解了：
def dataHandleCoroutine(self，sendData):  ########改动地方
        """
        """
        length = self.factory.dataprotocl.getHeadLenght()#获取协议头的长度
            data = sendData   ########改动地方
            self.buff += data
            while self.buff.__len__() >= length:
                unpackdata = self.factory.dataprotocl.unpack(self.buff[:length])
                if not unpackdata.get('result'):
                    log.msg('illegal data package --')
                    self.transport.loseConnection()
                    break
                command = unpackdata.get('command')
                rlength = unpackdata.get('lenght')
                request = self.buff[length:length+rlength]
                if request.__len__() < rlength:
                    log.msg('some data lose')
                    break
                self.buff = self.buff[length+rlength:]
                d = self.factory.doDataReceived(self, command, request)
                if not d:
                    return    ########改动地方
                d.addCallback(self.safeToWriteData, command)
                d.addErrback(DefferedErrorHandle)
3、剩下了就简单了，利用python struct库来解包数据，            
ud = struct.unpack('!sssss3I',dpack)
然后调用自己的services来处理解包后的command和参数。至于如何处理命令，就要看这个services挂什么样的处理函数了。

启动流程介绍完毕，下面就是app里面，暗黑游戏部分的具体处理内容了。

调用流程和前面一样，我们直接到关键函数：
def loadModule():
    netapp.initNetApp()
    import gatenodeapp
这里有些代码冗余和重复，但是没有什么太大影响，我们不提了。
这个函数的第一行代码是我改动过的（原先是import+修饰符方式），大家跟进去看，其实就是初始化一个services的子类：NetCommandService，然后给它挂上Forwarding_0 这个处理函数。

而我们仔细看NetCommandServices发现它override了原先的callTargetSingle，主要是这句改动：
            target = self.getTarget(0)
说明不论啥命令过来，它都写死了调用Forwarding_0来处理。
而Forwarding_0这个函数就一句话，功能是转发前面解析的command和参数给gate模块。

OK到这里结合前面的gate模块，我们应该就可以理出一条client登录的主线。
0、暗黑客户端一启动，就会连接net模块，net模块建立一个对应的connection，并由connectionManager保存。
1、暗黑客户端发送用户名、密码和登陆命令号101： （会封包，这里忽略）
        Json::FastWriter  writer;
        Json::Value person;
        person["username"]=userName;
        person["password"]=password;
        std::string  json_file=writer.write(person);
        CCLog("%s",json_file.c_str());
        SocketManager::getInstance()->sendMessage(json_file.c_str(), 101);

2、net模块接收并解析出命令号 101，参数{name：xxx,pwd：xxx}。然后调用自己的services（实际是NetCommandServices)处理。
3、NetCommandServices，不管37 21，直接写死调用Forwarding_0函数。
4、Fowarding_0函数写死了，用命令fowarding转发给gate模块。
4、gate模块收到它leafNode的调用请求，所以调用自己作为root的services。而这个services在gate/app/gate/rootservice/rservices.py里面注册了forwarding函数，所以就调用它。
5、md，fowarding函数发现这个命令号注册在loacalservices里面，见
gate/app/gate/localservice/lservices.py中：
def init():
    initLocalService()

    addToLocalService(loginToServer_101) ############## 这里
    addToLocalService(activeNewPlayer_102)
    addToLocalService(roleLogin_103)
于是调用loginToServer_101来处理这个命令
6、这个命令就不展开了，很简单，就是取数据，比对是否匹配，check是否有效。然后逐层返回，最后送给客户端


对于登录部分，流程压根没有跑到db、game1和admin模块，所以我们可以直接利用master,gate,net这3个模块做测试
顺序启动
master
gate
net
然后启动tool/clienttest.py 
可以看到net模块的终端会有信息打印。

我自己也写了一个测试程序。已经放在github上面，tool/ clientTestLogin.py；
用的是twisted，很简单。如下：

  1 from twisted.internet.protocol import Protocol, ClientFactory                                                 
  2 
  3 class Echo(Protocol):
  4     def connectionMade(self):
  5         a = 'N%&0\t\x00\x00\x00\x00\x00\x00\x00.\x00\x00\x00e{"password":"chenee","username":"chenee"}\n'
  6         self.transport.write(a)
  7 
  8     def dataReceived(self, data):
  9         print data
 10         #self.transport.loseConnection()
 11 
 12 
 13 class EchoClientFactory(ClientFactory):
 14     def startedConnecting(self, connector):
 15         print 'Started to connect.'
 16 
 17     def buildProtocol(self, addr):
 18         print 'Connected.'
 19         return Echo()
 20 
 21     def clientConnectionLost(self, connector, reason):
 22         print 'Lost connection.  Reason:', reason
 23 
 24     def clientConnectionFailed(self, connector, reason):
 25         print 'Connection failed. Reason:', reason
 26 
 27 from twisted.internet import reactor
 28 reactor.connectTCP("localhost", 11009, EchoClientFactory())
29 reactor.run()                                                                                                 

很简单，就30行代码，而且都是框架 。就是在连接上server后，事件connectionMade里面往server写一条命令。这条命令是我直接copy暗黑客户端的打印，就是一条封装好的数据包。
  5         a = 'N%&0\t\x00\x00\x00\x00\x00\x00\x00.\x00\x00\x00e{"password":"chenee","username":"chenee"}\n'

运行后结果如下：

bash-3.2$ python clientTestLogin.py 
Started to connect.
Connected.
N%&0    We{"data": {"userId": 1915, "characterId": 1000001, "hasRole": true}, "result": true}
可以看出，server成功处理，并且返回我们登录后的角色信息。


OK，这章介绍结束，下面介绍game1模块。



 
# 游戏服务器学习笔记 9 ————   game1模块
game1 囊括了几乎所有游戏逻辑，内容很多。但是多也只是app内容多， 前面的firefly框架启动流程没有什么差别。
如果看官是一直看下来的，扫一眼代码就一目了然，这里不提。直接跳到app部分。

def loadModule():
    """
    """
    load_config_data() #加载数据
    registe_madmin()  #注册几个表到memcache
    from gatenodeapp import *  #实际上是注册各种services的命令

逻辑上game/app启动逻辑分3个部分。
Load_config_data()；里面东西虽然多，但是并不复杂，如下：
def getExperience_Config():
    """获取经验配置表信息"""
    global tb_Experience_config
    sql = "select * from tb_experience"
    result = dbpool.fetchAll(sql)  ########我改过了
    for _item in result:
        tb_Experience_config[_item['level']] = _item
只是取一些游戏中常用的数据表的内容，然后直接保存在game1的内存数据中，不是memcache，因为这是常驻内存，而不是缓存起来的。

其中    result = dbpool.fetchAll(sql) 是我改动了一下，只是把原先copy paste的代码风格整理一下。10几个地方全部是同样复制的代码看起来非常不舒服。
不过这里不但是体力活，而且是细致活，分3中fetch，具体看我改动后的github代码，没有啥技术含量就不提了。

然后是用MAdminManager，来注册管理几个表，这个和前面db章节提到的一模一样。需要注意的是，下面的代码：
def registe_madmin():
    """注册数据库与memcached对应
    """
    MAdminManager().registe(memmode.tb_character_admin)
    MAdminManager().registe(memmode.tb_zhanyi_record_admin)
    MAdminManager().registe(memmode.tbitemadmin)
    MAdminManager().registe(memmode.tb_matrix_amin)
看上去做的只是注册到MAdminManager，并没有初始化。但是其实在文件开头有一个
import memmode
而memmode.py里面是直接裸写的全局变量。所以实际上在这个python文件开头就已经初始化了。
建议把import memmode放到registe_madmin（）函数开头部分。这样逻辑上清晰一些。
或者干脆吧memmode里面的内容全部封装到一个init函数里面更好。

大家明白就好，我懒得改了。


下面看第三行
    from gatenodeapp import *
这个就是利用import+修饰符方式，添加一批services的命令处理函数。跟进去看：

remoteservice = CommandService("gateremote")
GlobalObject().remote["gate"].setServiceChannel(remoteservice)

def remoteserviceHandle(target):
    """
    """
    remoteservice.mapTarget(target)
可以看出，实际上是给连接gate模块的leafNode的services添加的。这样gate转发过来的命令，都会被这些函数解析，处理。然后把结果返回给gate，再返回给net，最终到client端。


前面net章节已经分析了用户登录时，net到gate的数据流。这里唯一不同的是gate的消息处理不再是由localservices处理，而是有gate的root转发出去。（下面是gate模块中对应的代码）
        node = VCharacterManager().getNodeByClientId(dynamicId)
        return GlobalObject().root.callChild(node, key, dynamicId, data)

我们可以看出，firefly中是由gate模块来维护一个虚拟角色管理类，并由这个管理类来管理一批登陆的虚拟角色。
这些VirtualCharacter中会记录用户的虚拟角色到底是在那个game模块上；虽然我们这里只有game1一个游戏内容处理模块（游戏逻辑服务器），但是可以看出firefly的逻辑是支持多个game模块的。
同时也确定了，这些分发管理是由gate模块（或者叫gate服务器）来负责的。
这里的命令虽然很多，但是相互之间比较独立，同事也和firefly的系统架构关联性不大，独立理解起来很方便。我们就不在一一介绍了。

这个部分其实是和系统策划，游戏逻辑密切相关的，所以，如果有空，我们在后面反推暗黑的游戏逻辑的时候，结合cocos2dx客户端再详细说明上面提到的所有的services处理函数的各个功能，以此来展现一个完整的暗黑游戏框架。而不是这里讨论的firefly服务器框架。

OK，OK
这个系列基本告一段落，大概花费我3天时间码字，如果有什么疏忽的地方，冒犯的地方，或者错误的地方，还请各位看官，9miao的朋友多担待。
也请大家积极反馈，批评指点，帮助我改正错误。


最后再次感谢9miao的开源精神，毫无疑问，firefly和暗黑的代码给我提供了极大的帮助！
