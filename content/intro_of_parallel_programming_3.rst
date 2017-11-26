并行编程简述-并发级别
############################

:date: 2016-12-11 19:50
:slug: intro-of-parallel-programming-3
:summary: 多核编程相关文献中经常会说一个并发算法是wait-free或者lock-free，或者是non-blocking的，这些词汇表示的是并发的程度，或者说并发的级别。本文对这些术语进行简介。
:category: 技术
:tags: 并行编程

并发级别分为以下几个等级：

1.  **Wait-Free 无等待并发**

Wait-Free指的是每一个线程都一直运行下去而无须等待外部条件，整个流程中任何操作都能在一个有限的步骤内完成，这是最高的并发级别，没有任何阻塞。

结合之前原子操作部分的知识，可以简单认为能够直接调用一个原子操作实现的算法或程序就属于Wait-Free，比如下面的increment_reference_counter函数就是Wait-Free的，它封装了atomic_increment这个原子自增原语，多个线程可以同时调用这个函数对同一个内存变量进行自增，而无须任何阻塞（其实也是有阻塞的，是总线锁级别）。

.. code-block:: cpp
    :linenos:

    void increment_reference_counter(rc_base* obj) {
        atomic_increment(obj->rc);
    }

与此做对比，CAS类的调用就不是Wait-Free的，注意Wait-Free的原语都不能包含内部循环，CAS原语使用时通常包含“循环直到成功”的循环内部。

2.  **Lock-Free 无锁并发**

Lock-Free指的是整个系统作为一个整体一直运行下去，系统内部单个线程某段时间内可能会饥饿，这是比Wait-Free弱的并发级别，但系统整体上看依然是没有阻塞的。所有Wait-Free的算法显然都满足Lock-Free的要求。

Lock-Free算法通常可以通过同步原语CAS实现。

.. code-block:: cpp
    :linenos:

    void push(stack* s, node* n) {
        node* head;

        do {
            head = s->head;
            n->next = head;
        } while (!atomic_compare_exchange(s->head, head, n));
    }

多个线程同时调用上述函数，理论上某个线程可以一直困在循环内部，但一旦有一个线程原子操作失败而返回循环，意味着有其他线程成功执行了原子操作而退出循环，从而保证系统整体是没有阻塞的。

其实前面的原子自增函数也可以用下面的原语实现，在这种实现里，不再是所有线程都无阻塞了，某些线程可能会因为CAS失败而回绕若干次循环。

.. code-block:: cpp
    :linenos:

    void increment_reference_counter(rc_base* obj) {
        int rc;
        do {
            rc = obj->rc;
        } while (!atomic_compare_exchange(obj->rc, rc, rc + 1));
    }

3.  **Obstruction-Free 无阻塞并发**

Obstruction-Free是指在任何时间点，一个孤立运行线程的每一个操作可以在有限步之内结束。只要没有竞争，线程就可以持续运行，一旦共享数据被修改，Obstruction-Free 要求中止已经完成的部分操作，并进行回滚。

Obstruction-Free是并发级别更低的非阻塞并发，该算法在不出现冲突性操作的情况下提供单线程式的执行进度保证，所有Lock-Free的算法都是Obstruction-Free的。

4.  **Blocking algoithms 阻塞并发**

阻塞类的算法是并发级别最低的同步算法，它一般需要产生阻塞。可以简单认为基于锁的实现是Blocking的算法。

上述几种并发级别可以使用下图描述：

.. figure:: /images/parallel_level.png
    :width: 500px
    :alt: 图1 并发级别

    图1 并发级别

其中，蓝色是阻塞的算法，绿色是非阻塞算法，金字塔越上方，并发级别越高，性能越好，右边的金字塔是实现工具（原子操作、锁、互斥体等）。