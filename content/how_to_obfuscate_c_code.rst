怎么混淆C代码
#################

:date: 2015-07-11 13:00
:slug: how-to-obfuscate-c-code
:category: 技术
:tags: IOCCC;代码混淆
:summary: 如何写一段big很高的代码呢？这里是自己的一些心得以及 `示例代码 <http://blackfox1983.github.io/about.html>`_


最近在看了过去几届 `IOCCC <http://www.ioccc.nrg>`_ 的获奖代码，在佩服作者的创意以及能力的同时，也体会了一把代码方面的奇趣。用Linus的话说“Just for fun”。就着闲暇时光，自己也小玩了一把。
不过，玩归玩，还是需要阐述下个人观点，避免造成误导：

- Coding是一个很严肃的事情，尤其是实际的项目开发中，代码经常需要运行若干年并且需要一批批的RD来维护，排版、混乱、潜在缺陷的代码会造成难以估量的维护成本。因此，在任何项目开始前，均建议制定合理的适合项目本身的编码规范并严格执行。（就算是一次性的项目，一份漂亮的代码也是专业能力的体现）
- 每个程序员都有把代码写乱的可能，只是程度不同。需要注意的是要控制好这个度。能力越大的人，写出“Big更高”来炫技的代码的能力也越大。
- 本文展现的示例，正面看是探索代码本身的乐趣，也可以更深入的理解编程语言，反面看，则是一些不好编码习惯的一些体现。不求big有多高，但是千万别给后人在代码中挖坑。

言归正传，本文的示例代码是打印一份自己的的简历。最终的代码以及输出可参见 `示例代码 <http://blackfox1983.github.io/about.html>`_ 。下面则讲述怎么一步步写出这份Big很高的代码。

注：这里的代码使用 `gcc source.c` 编译。平台：Linux

1. 简单直接的实现
    既然仅仅是打印简历，而简历内容也是固定的。那么直接使用printf就可以了。代码如下：

.. code-block:: c
    :linenos:

    #include <stdio.h>

    const char* msg =
        "MiLimin\n"
        "blackfox1983@163.com\n"
        "QQ:115519153\n"
        "Changping District\n"
        "Beijing, China\n"
        "\n"
        /*限于篇幅，忽略部分内容，全文输出可参见示例代码部分*/
        "- Maintained libraries(e.g. network, db-query) running in all Game-Servers\n";

    void main() {
        printf("%s", msg);
    }

从炫技的角度来看，这个简直弱爆了（当然还有更弱的，直接使用N个printf依次打印……）。怎么向人说你是写很多年C代码的呢。我们需要Bigger一些。

2. 信息编码
    若直接输出原始字符串，怎么弄都可以从代码中看出原始的数据，这个比较low。进一步混淆的话，可能想到的就是排版了，但是排版也是很low的一种办法。在这里采用的是编码，即将原始字符数据转为可打印的其他字符（即ASCII码表中[32,126]部分的字符）。具体的编码方法参考凯撒密码而设计：
    
    - 首先定义一个base，这个base确定为31。主要是考虑不再常见的可打印字符列表中，较隐蔽
    - 密文字符采用原字符与31的差值对应的可打印字符来表示。原字符计算方法为: `31+passcode`
    - 对于部分密文表示会有一些case，如换行('\n')与31的差值为-20，且会出现[0,31]取件的字符，因此需要对这部分字符做一些处理。考虑到目标字符中不会出现下划线('_')，且下划线本身容易和变量名混在一起，因此使用下划线表示换行符；对于差值小于32的字符，则增加一个'~'符号来表示其后相连的字符需要做进一步的运算来获得原字符: `(passcode+31)/2`

    对应的代码如下：

.. code-block:: c
    :linenos:

    #include <stdio.h>
    #include <string.h>

    /*原始明文
    const char* msg =
        "MiLimin\n"
        "blackfox1983@163.com\n"
        "QQ:115519153\n"
        "Changping District\n"
        "Beijing, China\n"
        "\n"
        //限于篇幅，忽略部分内容，全文输出可参见示例代码部分
        "- Maintained libraries(e.g. network, db-query) running in all Game-Servers\n";

    char buf[1024];

    //生成密文
    void general_passwd() {
        int size = strlen(msg);
        int index = 0;
        int i = 0;

        for (; i < size; ++i) {
            int d = msg[i] - 31;

            if (d < 0) {
                buf[index++] = '_'; //处理'\n'
            } else if (d < 31) {
                buf[index++] = '~'; //处理[0-31]的字符
                buf[index++] = (char)(msg[i] * 2 - 31);
            } else {
                buf[index++] = d;
            }
        }
    }*/

    //密文。这是后续主要处理的数据
    const char* passwd = ".J-JNJO_CMBDLGPY~C~S~Q~G!~C~M~G~=DPN_22~U~C~C~K~K~C~S~C~\
    K~G_$IBOHQJOH~!%JTUSJDU_#FJKJOH~9~!$IJOB__&EVDBUJPO__.~=4~=~!BU~!$PMMFHF~!PG~!\
    $PNQVUFS~!4DJFODF~!BOE~!5FDIOPMPHZ~!BU~!6OJWFSTJUZ~!PG~!+JMJO~!~;~!$IBOHDIVO~9\
    ~!+JMJO_4FQUFNCFS~!~C~9~!~E~A~A~O~!UP~!+VMZ~!~C~9~!~E~A~C~A_~;~!4UVEJFE~!UIFPS\
    Z~!PG~!$PNQVUFS~!4DJFODF~9~!F~=H~=~!$PNQVUBCJMJUZ~!~-~!$PNQMFYJUZ_~;~!3FTFBSDI\
    FE~!PG~!#PU/FU_~;~!%JE~!1SPKFDUT~9~!F~=H~=~!8FC~9~!%FTLUPQ~!4PGUXBSFT~!PO~!~!8\
    JOEPXT~!BOE~!4FSWFST~!PO~!-JOVY__#~=4~=~!BU~!$PMMFHF~!PG~!$PNQVUFS~!4DJFODF~!B\
    OE~!5FDIOPMPHZ~!BU~!6OJWFSTJUZ~!PG~!+JMJO~!~;~!$IBOHDIVO~9~!+JMJO_4FQUFNCFS~!~\
    C~9~!~E~A~A~E~!UP~!+VMZ~!~C~9~!~E~A~A~M_~;~!\'PDVTFE~!PO~!UIF~!UIFPSZ~!PG~!$PN\
    QVUFS~!4DJFODF_~;~!5BVHIU~!NZTFMG~!/FUXPSL~!4FDVSJUZ~!BOE~!QSBDUJDF_~;~!1SPHSB\
    NJOH~!PO~!+PK~1+J-JO~!6OJWFSTJUZ~!0OMJOF~!+VEHF~!4ZTUFN~3__&NQMPZNFOU__3~-%~9~\
    !#BJEV~9~!*OD~=~!~;~!#FJKJOH_\"QSJM~!~C~G~9~!~E~A~C~C~!UP~!/PX_~;~!%FWFMPQFE~!\
    TFWFSBM~!NPEVMFT~!BOE~!MJCSBSJFT_~;~!1SPWJEFE~!EFTJHO~!XPSL~!GPS~!#BJEV~;4QJEF\
    S~/T~!BOE~!8FC.BTUFS~;1MBUGPSN~/T~!MBVODI__4PGUXBSF~!&OHJOFFS~9~!,JOHTPGU~9~!*\
    OD~=~!~;~!%BMJBO~9~!-JBPOJOH_+VOF~!~A~C~9~!~E~A~C~A~9~!UP~!.BSDI~!~E~K~9~!~E~A\
    ~C~C_~;~!%FWFMPQFE~!3FBMN~;4FSWFS_~;~!.BJOUBJOFE~!MJCSBSJFT~1F~=H~=~!OFUXPSL~9\
    ~!EC~;RVFSZ~3~!SVOOJOH~!JO~!BMM~!(BNF~;4FSWFST_";

    void print(const int base, const char* passwd) {
        int size = strlen(passwd);
        int i = 0;
        int flag = 0;

        for (; i < size; i++) {
            if (passwd[i] == '_') {
                putchar('\n');
                continue;
            }

            if (passwd[i] == '~') {
                flag = 1;
                continue;
            }

            if (flag == 1) {
                putchar((base + passwd[i]) / 2);
                flag = 0;
            } else {
                putchar(base + passwd[i]);
            }
        }
    }

    void main() {
        //general_passwd();
        //print(31, buf);
        print(31, passwd);
    }

3. 常量替换
    代码到了这个地步（只保留print部分），已经是天书了，但是从混淆炫技的角度来看，远远不够。现在需要将代码中的常量(31)替换掉。
    这里就需要有一定的知识广度和深度了。

    - C中的[]运算符含义首址+偏移。因此buf[i]与i[buf]均表示 `buf+i`
    -  `unix` 是linux平台下定义的一个宏，值为1
    -  `~-i` 其实是`i-1`

    此外，再增加一步运算，`31=32-1`。

.. code-block:: c
    :linenos:

    void print(const int base, const char* passwd) {
    //...
    }

    void main() {
        const int base = ~-(unix<<-~~~+unix)["Show respect to the Best Hackers all over the world."];
        print(base, passwd);
    }

4. 使用while替换for
    一般来说，while循环要比for循环复杂些。上述代码使用while编写后，主要部分代码如下（顺便去掉了strlen的使用，减少了头文件引用）：   

.. code-block:: c
    :linenos:

    //const char* passwd = ...

    void print(const int base, const char* passwd) {
        int i = 0;
        int flag = 0;

        while (passwd[i] != 0) { {
            if (passwd[i] == '_') {
                putchar('\n');
                i++;
                continue;
            }

            if (passwd[i] == '~') {
                flag = 1;
                i++;
                continue;
            }

            if (flag == 1) {
                putchar((base + passwd[i]) / 2);
                flag = 0;
            } else {
                putchar(base + passwd[i]);
            }

            i++;
        }
    }

    //main...

5. 循环变递归
    在某些时候，递归可以简化代码，但是大部分是把代码复杂化且变的效率低下。将上述while循环变为递归后，主要部分代码如下：   

.. code-block:: c
    :linenos:

    //const char* passwd = ...

    void print(int idx, int flag, const int base, const char* passwd) {
        if (passwd[idx] != 0) {
            if (flag == 1) {
                putchar((base + passwd[idx]) / 2);
                print(idx + 1, 0, base, passwd);
            } else if (passwd[idx] == '_') {
                putchar('\n');
                print(idx + 1, 0, base, passwd);
            } else if (passwd[idx] == '~') {
                print(idx + 1, 1, base, passwd);
            } else {
                putchar(base + passwd[idx]);
                print(idx + 1, 0, base, passwd);
            }
        }
    }

    void main() {
        const int base = ~ -(unix << -~~~ +unix)["Show respect to the Best Hackers all over the world."];
        print(0, 0, base, passwd);
    }

6. 混乱代码结构
    这里介绍个技巧，将代码中的 `if-else` 结构使用 `?:` 三元表达式替换：   

.. code-block:: c
    :linenos:

    //const char* passwd = ...

    void print(int idx, int flag, const int base, const char* passwd) {
        passwd[idx] != 0 ? flag == 1 ? (putchar((base + passwd[idx]) / 2), print(idx + 1, 0, base, passwd))
        : passwd[idx] == '_' ? (putchar('\n'), print(idx + 1, 0, base,
                                passwd)) : passwd[idx] == '~' ? print(idx + 1, 1, base, passwd) :
        (putchar(base + passwd[idx]), print(idx + 1, 0, base, passwd)) : 0;   

    }

    //main...

7. 只保留main函数
    如果到这里就结束，big还是不够高。现在进一步要把除main之外的其他部分（全局常量、函数、头文件等）都干掉。这里有几个知识点先介绍下：

    - putchar()在C代码中不需要任何头文件，包括stdio.h
    - main函数的老式声明可以支持多个参数，且参数类型不指定则默认为int
    - main函数运行时，使用老式声明且第一个参数为int时，第一次运行时，第一个参数值为1

.. code-block:: c
    :linenos:

    void main(first, idx, flag, base, passwd) const char* passwd;{
        1 <= first ? main(0, 0, 0, 
            ~ -(unix << -~~~+unix)["Show respect to the Best Hackers all over the world."],
    ".J-JNJO_CMBDLGPY~C~S~Q~G!~C~M~G~=DPN_22~U~C~C~K~K~C~S~C~K~G_$IBOHQJOH~!%JTUSJ\
    DU_#FJKJOH~9~!$IJOB__&EVDBUJPO__.~=4~=~!BU~!$PMMFHF~!PG~!$PNQVUFS~!4DJFODF~!BO\
    E~!5FDIOPMPHZ~!BU~!6OJWFSTJUZ~!PG~!+JMJO~!~;~!$IBOHDIVO~9~!+JMJO_4FQUFNCFS~!~C\
    ~9~!~E~A~A~O~!UP~!+VMZ~!~C~9~!~E~A~C~A_~;~!4UVEJFE~!UIFPSZ~!PG~!$PNQVUFS~!4DJF\
    ODF~9~!F~=H~=~!$PNQVUBCJMJUZ~!~-~!$PNQMFYJUZ_~;~!3FTFBSDIFE~!PG~!#PU/FU_~;~!%J\
    E~!1SPKFDUT~9~!F~=H~=~!8FC~9~!%FTLUPQ~!4PGUXBSFT~!PO~!~!8JOEPXT~!BOE~!4FSWFST~\
    !PO~!-JOVY__#~=4~=~!BU~!$PMMFHF~!PG~!$PNQVUFS~!4DJFODF~!BOE~!5FDIOPMPHZ~!BU~!6\
    OJWFSTJUZ~!PG~!+JMJO~!~;~!$IBOHDIVO~9~!+JMJO_4FQUFNCFS~!~C~9~!~E~A~A~E~!UP~!+V\
    MZ~!~C~9~!~E~A~A~M_~;~!\'PDVTFE~!PO~!UIF~!UIFPSZ~!PG~!$PNQVUFS~!4DJFODF_~;~!5B\
    VHIU~!NZTFMG~!/FUXPSL~!4FDVSJUZ~!BOE~!QSBDUJDF_~;~!1SPHSBNJOH~!PO~!+PK~1+J-JO~\
    !6OJWFSTJUZ~!0OMJOF~!+VEHF~!4ZTUFN~3__&NQMPZNFOU__3~-%~9~!#BJEV~9~!*OD~=~!~;~!\
    #FJKJOH_\"QSJM~!~C~G~9~!~E~A~C~C~!UP~!/PX_~;~!%FWFMPQFE~!TFWFSBM~!NPEVMFT~!BOE\
    ~!MJCSBSJFT_~;~!1SPWJEFE~!EFTJHO~!XPSL~!GPS~!#BJEV~;4QJEFS~/T~!BOE~!8FC.BTUFS~\
    ;1MBUGPSN~/T~!MBVODI__4PGUXBSF~!&OHJOFFS~9~!,JOHTPGU~9~!*OD~=~!~;~!%BMJBO~9~!-\
    JBPOJOH_+VOF~!~A~C~9~!~E~A~C~A~9~!UP~!.BSDI~!~E~K~9~!~E~A~C~C_~;~!%FWFMPQFE~!3\
    FBMN~;4FSWFS_~;~!.BJOUBJOFE~!MJCSBSJFT~1F~=H~=~!OFUXPSL~9~!EC~;RVFSZ~3~!SVOOJO\
    H~!JO~!BMM~!(BNF~;4FSWFST_") :
        (passwd[idx] != 0 ? flag == 1 ? (putchar((base + passwd[idx]) / 2), main(0, idx + 1, 0, base,
                                         passwd))
         : passwd[idx] == '_' ? (putchar('\n'), main(0, idx + 1, 0, base,
                                 passwd)) : passwd[idx] == '~' ? main(0, idx + 1, 1, base, passwd) :
         (putchar(base + passwd[idx]), main(0, idx + 1, 0, base, passwd)) : 0);
    }

8. 变量替换
    继续提高Big，仅仅把变量写成 `i,j,k` 这类命名方法已经过时了，来点时髦的：    

.. code-block:: c
    :linenos:
    
    main(_, __, ___, ____, _____)const char* _____; {
        1 <= _ ? main(0, 0, 0, 
            ~ -(unix << -~~~+unix)["Show respect to the Best Hackers all over the world."],
        ".J-JNJO_CMBDLGPY~C~S~Q~G!~C~M~G~=DPN_22~U~C~C~K~K~C~S~C~K~G_$IBOHQJOH~!%JTUSJ\
        DU_#FJKJOH~9~!$IJOB__&EVDBUJPO__.~=4~=~!BU~!$PMMFHF~!PG~!$PNQVUFS~!4DJFODF~!BO\
        E~!5FDIOPMPHZ~!BU~!6OJWFSTJUZ~!PG~!+JMJO~!~;~!$IBOHDIVO~9~!+JMJO_4FQUFNCFS~!~C\
        ~9~!~E~A~A~O~!UP~!+VMZ~!~C~9~!~E~A~C~A_~;~!4UVEJFE~!UIFPSZ~!PG~!$PNQVUFS~!4DJF\
        ODF~9~!F~=H~=~!$PNQVUBCJMJUZ~!~-~!$PNQMFYJUZ_~;~!3FTFBSDIFE~!PG~!#PU/FU_~;~!%J\
        E~!1SPKFDUT~9~!F~=H~=~!8FC~9~!%FTLUPQ~!4PGUXBSFT~!PO~!~!8JOEPXT~!BOE~!4FSWFST~\
        !PO~!-JOVY__#~=4~=~!BU~!$PMMFHF~!PG~!$PNQVUFS~!4DJFODF~!BOE~!5FDIOPMPHZ~!BU~!6\
        OJWFSTJUZ~!PG~!+JMJO~!~;~!$IBOHDIVO~9~!+JMJO_4FQUFNCFS~!~C~9~!~E~A~A~E~!UP~!+V\
        MZ~!~C~9~!~E~A~A~M_~;~!\'PDVTFE~!PO~!UIF~!UIFPSZ~!PG~!$PNQVUFS~!4DJFODF_~;~!5B\
        VHIU~!NZTFMG~!/FUXPSL~!4FDVSJUZ~!BOE~!QSBDUJDF_~;~!1SPHSBNJOH~!PO~!+PK~1+J-JO~\
        !6OJWFSTJUZ~!0OMJOF~!+VEHF~!4ZTUFN~3__&NQMPZNFOU__3~-%~9~!#BJEV~9~!*OD~=~!~;~!\
        #FJKJOH_\"QSJM~!~C~G~9~!~E~A~C~C~!UP~!/PX_~;~!%FWFMPQFE~!TFWFSBM~!NPEVMFT~!BOE\
        ~!MJCSBSJFT_~;~!1SPWJEFE~!EFTJHO~!XPSL~!GPS~!#BJEV~;4QJEFS~/T~!BOE~!8FC.BTUFS~\
        ;1MBUGPSN~/T~!MBVODI__4PGUXBSF~!&OHJOFFS~9~!,JOHTPGU~9~!*OD~=~!~;~!%BMJBO~9~!-\
        JBPOJOH_+VOF~!~A~C~9~!~E~A~C~A~9~!UP~!.BSDI~!~E~K~9~!~E~A~C~C_~;~!%FWFMPQFE~!3\
        FBMN~;4FSWFS_~;~!.BJOUBJOFE~!MJCSBSJFT~1F~=H~=~!OFUXPSL~9~!EC~;RVFSZ~3~!SVOOJO\
        H~!JO~!BMM~!(BNF~;4FSWFST_") : (_____[__] != 0 ? ___ == 1 ? (putchar((____ + __[_____]) / 2),
        main(0, __ + 1, 0, ____, _____)) : _____[__] == '_' ? (putchar('\n'), main(0, __ + 1, 0, ____,
        _____)) : _____[__] == '~' ? main(0, __ + 1, 1, ____, _____) : (putchar(____ + _____[__]), main(0,
        __ + 1, ___, ____, _____)) : 0);
    }    

9. 消灭最后剩余的两个函数main、putchar
    这里主要使用宏定义来处理，如果只是写成 `#define _____ main` 这类的，还是有些low，得把信息隐藏掉。
    这里介绍几个相关的背景：

    - Raymond：`Eric Steven Raymond <https://it.wikipedia.org/wiki/Eric_Steven_Raymond>`_ 。著名的计算机程序员，开源软件运动的旗手,经典十大黑客之一（其他齐名的有Linus、Mitnick等）。顶顶大名的五部曲便出自这位大牛之手
    - Revolution Operating System：在微软垄断下有一件东西永远它永远不会给你――真正的自由。也正是因为这个原因，不少先锋人物站出来反抗微软帝国，并努力建立一种新的操作系统――没有人为的限制，任何人都可以自由地使用。 为了记录这些人的艰苦历程，J.T.S. Moore拍摄了全新的记录片――REVOLUTON OS，向公众介绍这些建立Linux操作系统，奋起反抗垄断的斗士的人生经历。 REVOLUTION OS中记录了Linux的创建人Linus Torvemlds以及Richemrd Stemllmemn, Bruce Perens, Eric Remymond, Briemn Behlendorf, Michemel Tiememnn, Lemrry Augustin, Fremnk mond, Briemn Behlendorf, Michemel Tiememnn, Lemrry Augustin, Fremnk Hecker, Rob Memldem等多位大牛人的生活经历或者采访记录
    - Hackers: Heroes of the Computer Revolution：作者为Steven Levy。介绍了从20世纪50年代早期跨越到80年代后期，追述了计算机革命中初期黑客的丰功伟绩，他们都是最聪明和最富有个性的精英。他们勇于承担风险，勇于挑战规则，并把世界推向了一个全新的发展方向。其中包括著名黑客的资料，包括比尔·盖茨、马克·扎克伯格、理查德·斯托曼和史蒂夫·沃兹尼亚克，并讲述了从早期计算机研究实验室到最初的家用计算机期间一些妙趣横生的故事

.. code-block:: c
    :linenos:

    #define _________(l,n,m,V,W,X,Y,Z,b,c,d,t,u,v,w,x,y,o,N,O,P,Q,R,H,I,J,K,L,M,S,\
    T,U,a,e,f,g,h)  R##a##y##m##o##n##d
    #define  ________  _________(H,a,c,k,e,r,s,:, H,e,r,o,e,s, o,f, t,h,e, C,o,m,p,u,t,e,r, R,e,v,o,l,u,t,i,o,n)
    #define _______(B,C,D,E,F,G,H,I,Z,A,J,K,L,M,N,V,W,X,O,P,Q,R,S,T,U) U##N##I##X
    #define ______  _______(R,e,v,o,l,u,t,i,o,n, O,p,e,r,a,t,i,n,g, S,y,s,t,e,m)

    //main(...
    //______(... 

10. 优雅的排版，打扫战场
     终于到了最后了，还有几件事情收尾。

    - 将目前代码中的数字进一步的复杂化，如 `1` 改写为 `!0` ，利用各种数组的操作技巧替换原有的数组编写方式。
    - 排版：代码虽然不可读了，但是整体表现上还是要优雅一些。代码也是艺术品。在这里设计的是一块题词的匾额，用以怀念当年学习的黑客技术。这里有些技巧：采用80字符的列宽提高用户视觉体验，采用注释进行补位，最后的0替换为日期格式的数字减运算，宏定义字符居中显示增加美感等。

    最终代码如下：

.. code-block:: c
    :linenos:

    /**********Save the code as C file and compile it with gcc4.8.2***************/
    #define _________(l,n,m,V,W,X,Y,Z,b,c,d,t,u,v,w,x,y,o,N,O,P,Q,R,H,I,J,K,L,M,S,\
    T,U,a,e,f,g,h)/*------------------------------------------------------------*/\
                            R##a##y##m##o##n##d
    /*---------------------------------------------------------------------------*/
    #define  ________  _________(\
                              H,a,c,k,e,r,s,:,\
     H,e,r,o,e,s,     o,f,     t,h,e,     C,o,m,p,u,t,e,r,     R,e,v,o,l,u,t,i,o,n)
    /*---------------------------------------------------------------------------*/
    #define _______(B,C,D,E,F,G,H,I,Z,A,J,K,L,M,N,V,W,X,O,P,Q,R,S,T,U)    /******/\
                                U##N##I##X
    /*---------------------------------------------------------------------------*/
    #define ______  _______(\
                R,e,v,o,l,u,t,i,o,n,   O,p,e,r,a,t,i,n,g,   S,y,s,t,e,m)
    /*---------------------------------------------------------------------------*/
    ______(_,__,___,____,_____)const char* _____;{!0<=_?______(0,0,0,/*************
    *******************************************************************************
    ******************************************************************************/
    ~-(unix<<-~~~+unix)["Show respect to the Best Hackers all over the world."],/**
    *******************************************************************************
    ******************************************************************************/
    ".J-JNJO_CMBDLGPY~C~S~Q~G!~C~M~G~=DPN_22~U~C~C~K~K~C~S~C~K~G_$IBOHQJOH~!%JTUSJ\
    DU_#FJKJOH~9~!$IJOB__&EVDBUJPO__.~=4~=~!BU~!$PMMFHF~!PG~!$PNQVUFS~!4DJFODF~!BO\
    E~!5FDIOPMPHZ~!BU~!6OJWFSTJUZ~!PG~!+JMJO~!~;~!$IBOHDIVO~9~!+JMJO_4FQUFNCFS~!~C\
    ~9~!~E~A~A~O~!UP~!+VMZ~!~C~9~!~E~A~C~A_~;~!4UVEJFE~!UIFPSZ~!PG~!$PNQVUFS~!4DJF\
    ODF~9~!F~=H~=~!$PNQVUBCJMJUZ~!~-~!$PNQMFYJUZ_~;~!3FTFBSDIFE~!PG~!#PU/FU_~;~!%J\
    E~!1SPKFDUT~9~!F~=H~=~!8FC~9~!%FTLUPQ~!4PGUXBSFT~!PO~!~!8JOEPXT~!BOE~!4FSWFST~\
    !PO~!-JOVY__#~=4~=~!BU~!$PMMFHF~!PG~!$PNQVUFS~!4DJFODF~!BOE~!5FDIOPMPHZ~!BU~!6\
    OJWFSTJUZ~!PG~!+JMJO~!~;~!$IBOHDIVO~9~!+JMJO_4FQUFNCFS~!~C~9~!~E~A~A~E~!UP~!+V\
    MZ~!~C~9~!~E~A~A~M_~;~!\'PDVTFE~!PO~!UIF~!UIFPSZ~!PG~!$PNQVUFS~!4DJFODF_~;~!5B\
    VHIU~!NZTFMG~!/FUXPSL~!4FDVSJUZ~!BOE~!QSBDUJDF_~;~!1SPHSBNJOH~!PO~!+PK~1+J-JO~\
    !6OJWFSTJUZ~!0OMJOF~!+VEHF~!4ZTUFN~3__&NQMPZNFOU__3~-%~9~!#BJEV~9~!*OD~=~!~;~!\
    #FJKJOH_\"QSJM~!~C~G~9~!~E~A~C~C~!UP~!/PX_~;~!%FWFMPQFE~!TFWFSBM~!NPEVMFT~!BOE\
    ~!MJCSBSJFT_~;~!1SPWJEFE~!EFTJHO~!XPSL~!GPS~!#BJEV~;4QJEFS~/T~!BOE~!8FC.BTUFS~\
    ;1MBUGPSN~/T~!MBVODI__4PGUXBSF~!&OHJOFFS~9~!,JOHTPGU~9~!*OD~=~!~;~!%BMJBO~9~!-\
    JBPOJOH_+VOF~!~A~C~9~!~E~A~C~A~9~!UP~!.BSDI~!~E~K~9~!~E~A~C~C_~;~!%FWFMPQFE~!3\
    FBMN~;4FSWFS_~;~!.BJOUBJOFE~!MJCSBSJFT~1F~=H~=~!OFUXPSL~9~!EC~;RVFSZ~3~!SVOOJO\
    H~!JO~!BMM~!(BNF~;4FSWFST_"):(__[_____]!=0?___==1?(________((____+__[_____])>>1
    ),______(0,__+1,!___,____,_____)):*(_____+__)=='_'?(________(012),______(0,__+1
    ,___,____,_____)):*(__+_____)=='~'?______(0,__+1,!___,____,_____):(________(///
    ____+*(__+_____)),______(0,__+1,___,____,_____)):/*============================
    ===============================================================================
                                               by blackfox*/ 2015-07-15-00-00-00);}
    /*****************************************************************************/