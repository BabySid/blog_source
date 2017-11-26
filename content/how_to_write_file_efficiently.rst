怎样高效的写文件
###################

:date: 2016-08-21 21:08
:slug: how-to-write-file-efficiently
:category: 技术
:tags: write;writev
:summary: 写文件是在后台开发中常见的一个基础逻辑，但是面对大量的文件写入，如何写才是比较高效的呢？这里做一个基本的介绍。

在日常的后台开发中，写文件是一个很常见的操作，比如需要将接收到的消息序列化后写到文件中避免消息丢失，或者在存储系统的实现中也需要将数据持久化到磁盘上。

1.  **批量写**

批量读写是针对磁盘IO操作的一个基本原则，主要是因为现代计算机磁盘的硬件结构导致（寻道操作）。这里不再赘述。比较典型的应用是level-db等，将随机写优化为批量写来提高吞吐。

2.  **write & writev**

不论怎么设计系统，最本质上的写操作仍然是 `write` 以及 `writev` 。那么问题来了，如何使用这两个函数效率才是最高的呢？或者对多大的数据怎么写效率才是最高的呢？

自己写程序做了一回测试，通过将100MB的数据写入到磁盘上，每次写入一定数据量，且分别使用 `write` 、`writev` 来写入，得到的性能数据如下：

.. figure:: /images/write_vs_writev_1.jpg
    :width: 500px
    :alt: write vs writev 测试测试

    write vs writev 性能测试

从图上可以看出：
    * `writev` 的性能表现较 `write` 更稳定。
    * 每次写入量1KB以下，建议使用 `writev` 来写入数据。
    * 每次写入量超过1KB，建议使用 `write` 来写入数据。
    * 每次写入量超过32KB，建议使用 `write` 来写入数据。
    * 32KB以上的数据写入，`write` 和 `writev` 差别不大。
    * 对于多缓存的写入，仍建议使用 `writev` 写入。主要是避免内核态调用次数以及缓存拷贝次数的增加。

本文中使用的测试代码：

.. code-block:: cpp
    :linenos:

    #include <unistd.h>
    #include <fcntl.h>
    #include <stdio.h>
    #include <string.h>
    #include <sys/types.h>
    #include <sys/stat.h>
    #include <sys/time.h>
    #include <sys/uio.h>
    #include <assert.h>

    void test_writev(int fd, int size_per_step) {
        struct  timeval start;
        struct  timeval end;

        const static int BUF_SIZE = 1024 * 1024 * 100;

        char* buf = new char[BUF_SIZE];

        for (int i = 0; i < BUF_SIZE; ++i) {
            buf[i] = 'A' + (i % 26);
        }

        gettimeofday(&start, NULL);
        int ret = 0;
        const static int IOV_SIZE = BUF_SIZE / size_per_step;
        struct iovec* iovs = new struct iovec[IOV_SIZE];

        for (int i = 0; i < IOV_SIZE; ++i) {
            iovs[i].iov_base = buf + i * size_per_step;
            iovs[i].iov_len = size_per_step;
        }

        ret += writev(fd, iovs, IOV_SIZE);
        gettimeofday(&end, NULL);
        long diff =  1000000 * (end.tv_sec - start.tv_sec) + end.tv_usec - start.tv_usec;

        printf("time cost is %ldus\n", diff);

        delete[] buf;
        delete[] iovs;

        assert(ret == 104857600);
    }

    void test_write(int fd, int size_per_step) {
        struct  timeval start;

        struct  timeval end;

        const static int BUF_SIZE = 1024 * 1024 * 100;

        char* buf = new char[BUF_SIZE];

        for (int i = 0; i < BUF_SIZE; ++i) {
            buf[i] = 'A' + (i % 26);
        }

        int ret = 0;
        int steps = BUF_SIZE / size_per_step;
        gettimeofday(&start, NULL);

        for (int i = 0; i < steps; ++i) {
            ret += write(fd, buf + i * size_per_step, size_per_step);
        }

        gettimeofday(&end, NULL);

        long diff =  1000000 * (end.tv_sec - start.tv_sec) + end.tv_usec - start.tv_usec;

        printf("time cost is %ldus\n", diff);
        delete[] buf;

        assert(ret == 104857600);
    }

    int main() {
        int fd = open("./data", O_CREAT | O_APPEND | O_WRONLY, 0755);

        if (fd <= 0) {
            printf("open failed\n");
            return -1;
        }

        //test_write(fd, 1024*1024*10);
        test_writev(fd, 1024*1024*10);

        close(fd);
        return 0;
    }




