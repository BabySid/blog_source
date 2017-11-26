让模块出core时继续运行
########################

:date: 2015-10-18 18:20
:slug: continue-to-run-when-core-occurs
:summary: 当模块出core时，默认都会停止运行，尤其当一份脏数据到处传播时，服务几乎就处于不断的启停状态。如果让模块在出core时继续运行，该如何做到呢？
:category: 技术
:tags: core

模块在代码编写中，对于脏数据的容错不够（实际环境中异常数据的出现其实也是一种正常现象）或者程序bug，经常会引发程序出core，有时候还是线上一闪而过就不再出现的case，给RD、QA的追查带来不便，并且模块由于core不断启停，对于服务的稳定性也有影响。如果可以设计一种机制：

1. 脏数据到来时，针对模块的bug会触发core，但是不应让模块停止，模块过滤掉脏数据继续运行。这样可以减少OP的运维成本，以及线上数据处理的稳定性。
2. 对于脏数据可以将其dump出来并做个监控，这样报警时，可以用这个数据做case复现，提高bug分析的效率。

那么这样对于模块的维护将起到一个不错的作用。这里写了一个demo，示例代码如下：

.. code-block:: cpp
    :linenos:

    #include <stdio.h>
    #include <signal.h>
    #include <setjmp.h>
    #include <assert.h>
    #include <string.h>
    #include <unistd.h>

    jmp_buf g_buf; //实现机制，主要关注点

    bool g_quit; //退出标志

    //模块处理数据结构
    struct stru {
        int len;
    };

    void handler(int sig) {
        if (sig == SIGINT) {
            g_quit = true; //退出程序
            return;
        }

        siglongjmp(g_buf, 1); //实现机制，主要关注点
    }

    void recv_pack(struct stru* data) {
        assert(data != NULL);
        static int i = 0;
        data->len = i % 2 ? 1 : 0;
        i++;
    }

    //将数据dump出来（如磁盘文件）
    void dump_pack(const struct stru& data) {
        printf("dump: %d\n", data.len);
    }

    void process(struct stru* data) {
        assert(data != NULL);

        if (data->len != 0) {
            //异常演示
            int* p = 0; 
            *p = 100;
        }
    }

    int main() {
        signal(SIGSEGV, handler);
        signal(SIGINT, handler);

        g_quit = false;

        struct stru data;

        //实现机制，主要关注点
        if (sigsetjmp(g_buf, 1) != 0) {
            dump_pack(data);
        }

        while (!g_quit) {
            recv_pack(&data);
            process(&data);
            sleep(1); //方便demo演示，避免刷屏
        }


        return 0;
    }
