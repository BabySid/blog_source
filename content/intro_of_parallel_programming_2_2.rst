并行编程简述-内存模型(2)
#########################

:date: 2016-10-30 21:40
:slug: intro-of-parallel-programming-2-2
:summary: 内存模型对于并行编程非常重要，了解内存模型可以加深程序员对并行编程的掌握。本文则介绍并行编程中涉及的内存模型的缓存一致性的基础知识。
:category: 技术
:tags: 并行编程

1.  **缓存一致性** 

`Cache Coherence` 简称 CC， 缓存一致性协议是在共享缓存多处理器架构中确保最终一致性最突出、最重要的机制。这些协议在缓存线（cache-line）级别实现了对一致性的保证。缓存线是从主内存中读取数据和向内存中写入数据的缓存单位（至少从一致性机制的角度看是这样的）。商用处理器上三个最突出最重要的缓存一致性协议： `MOESI、MESI、MESIF` 的缩写都来自它们为缓存线定义的各种状态：Modified（已修改）, Owned（被占用）,Exclusive（独占的）, Shared（共享的）, Invalid（无效的）, 以及 Forward（转发的）。缓存一致性协议在对内存确保最终一致性的内存一致性机制的帮助下对这些状态进行管理。

以下为部分处理器中采用的缓存一致性协议：

Intel 奔腾：MESI 协议

AMD Opteron：MOESI 协议

Intel i7：MESIF 协议

再介绍了缓存一致性的基本概念后，问题来了：为什么需要缓存CC？

从 `前文 <http://blackfox1983.github.io/posts/2016/09/03/intro-of-parallel-programming-1/>`_ 的体系结构图可以看到，一般每个核心都有一个私有的L1级和L2级Cache，同一个物理CPU上的多个核心共享一个L3级缓存，这样的设计是出于提高内存访问性能的考虑。但是这样就有一个问题了，每个核心之间的私有L1，L2级缓存之间需要同步。比如，核心1上的线程A对一个共享变量global_counter进行了加1操作，这个被写入的新值存到核心1的L1缓存里了；此时另一个核心2上的线程B要读global_counter了，但是核心2的L1缓存里的global_counter的值还是旧值，最新被写入的值现在还在核心1上。这就需要CPU有一个模块来保证，同一个内存的数据在同一时刻对任何对其可见的核心看来，数据是一致的，由图中可知，这种专门的组件就是缓存控制器 `Cbox,Bbox` 。

此外，关于缓存一致性的详细介绍，可参见15年所作博文 `Cache一致性简介 <http://blackfox1983.github.io/posts/2015/10/11/intro-of-cache-coherency/>`_ 。

2.  **伪共享**

+ 定义 

从上述内容可以知道，缓存一致性协议操作的最小对象是缓存行，缓存行内数据的修改、写入内存、写入其他缓存等操作都会改变其状态，这样，在共享缓存多核架构里，数据结构如果组织不好，就非常容易出现多个核线程反复修改同一条缓存行的数据导致缓存行状态频繁变化从而导致严重性能问题，这就是伪共享现象。

下图就是一个伪共享的例子，Core1上运行的线程想修改变量x，Core2上运行的线程想修改变量y，但x和y刚好在一个缓存行上。每个线程都要去竞争缓存行的所有权来更新变量。如果Core1获得了所有权，缓存子系统将会使Core2中对应的缓存行失效。当核心2获得了所有权然后执行更新操作，Core1就要使自己对应的缓存行失效。这会来来回回的经过L3缓存，大大影响了性能。如果互相竞争的核心位于不同的插槽，就要额外横跨插槽连接，问题可能更加严重。

.. figure:: /images/cache_coherence.png
    :width: 330px
    :alt: 图1 伪共享

    图1 伪共享

+ 解决 

相比缓存行导致性能问题的严重性，解决这个问题的方案显得非常简单，这就是缓存行填充。通过填充缓存行，使得某个核心线程频繁操作的数据独享缓存行，这样就不会出现伪共享问题了。

.. code-block:: cpp
    :linenos:

    #define N_THR 8

    struct counter {
        unsigned long long value;
    };

    static volatile struct counter counters[N_THR];

    void* thread(void* unused) {
        while (!leave) {
            counters[UNIQUE_THREAD_ID].value++;
        }

        return NULL;
    }

32位机下 `long long` 是8字节，一个缓存行64字节，则可以存储8个counter, 这样最差的情况下同时会有8个线程争夺同一个缓存行的操作权，性能会非常低。解决方式非常简单，如下所示，每个counter变量增加一个填充变量pad，使得一个counter变量刚好是一个缓存行大小，这样数组counters每个元素占用一个缓存行，所有线程独占自己的缓存行，避免了伪共享问题。（性能至少提高 **4X**）

.. code-block:: cpp
    :linenos:

    struct counter {
        unsigned long long value;
        char pad[64 - sizeof(unsigned long long)];
    };