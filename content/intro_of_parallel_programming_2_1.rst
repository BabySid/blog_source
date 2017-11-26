并行编程简述-内存模型(1)
#########################

:date: 2016-09-10 22:34
:slug: intro-of-parallel-programming-2-1
:summary: 内存模型对于并行编程非常重要，了解内存模型可以加深程序员对并行编程的掌握。本文则介绍并行编程中涉及的内存模型的原子操作部分的基础知识。
:category: 技术
:tags: 并行编程

介绍内存模型，首先说明几个基础问题：

- 什么是内存模型

CPU硬件有自己的内存模型，不同的编程语言也有自己的内存模型。那么什么是内存模型？简单的说就是程序员、编程语言和硬件之间的一个契约，它保证了共享的内存地址里的值在需要的时候是可见的，且保证了机器执行代码的结果与程序员脑子里的预期是一致的。它最大的作用是取得可编程性与性能优化之间的一个平衡。

- 并行编程为什么需要关注内存模型

对于C/C++，目前缺少一个并发的内存模型，使得开发多核程序的程序员不得不面对内存操作的一些细节。（.net/java等基于虚拟机的语言其内存模型相对完善些）。
 
- 并行编程需要关注内存模型的哪些方面

`操作原子性、缓存一致性、顺序一致性` 。非常重要的一点思想是：你的代码不一定如你想象中那样执行。

1. **操作原子性**

原子性操作是指，在整个系统可见范围内，一个操作要不就没有发生，要不就执行完毕，没有中间状态出现。

在多线程程序里，哪些操作具有天然的原子性？哪些操作需要原子操作原语的支持？原子操作原语底层机制是什么？要回答这些问题，首先需要从硬件讲起。以常见的X86 CPU来说，根据Intel的参考手册，它基于以下三种机制保证了操作原子性：

+ Guaranteed atomic operations
+ Bus locking, using the LOCK# signal and the LOCK instruction prefix
+ Cache coherency protocols that ensure that atomic operations can be carried out on cached data structures (cache lock); this mechanism is present in the Pentium 4, Intel Xeon, and P6 family processors

这三个机制相互独立，相辅相承。简单的理解起来：

+ 一些基本的内存读写操作是本身已经被硬件提供了原子性保证（例如读写单个字节的操作）。
+ 一些需要保证原子性但是没有被第（1）条机制提供支持的操作（例如read-modify-write）可以通过使用”LOCK#”来锁定总线，从而保证操作的原子性。原子操作原语是基于“LOCK#”总线锁实现的。
+ 因为很多内存数据是已经存放在L1/L2 cache中了，对这些数据的原子操作只需要与本地的cache打交道，而不需要与总线打交道，所以CPU就提供了 `cache coherency` 机制来保证其它的那些也cache了这些数据的CPU能读到最新的值。

A. *硬件原子操作*

那么CPU对（1）中哪些基本的操作提供了原子性支持呢？根据Intel手册8.1.1节的介绍：

从Intel486开始，以下的基本内存操作是原子的：

+ Reading or writing a byte（一个字节的读写）
+ Reading or writing a word aligned on a 16-bit boundary（对齐到16位边界的字的读写）
+ Reading or writing a doubleword aligned on a 32-bit boundary（对齐到32位边界的双字的读写）

从Pentium开始，除了之前支持的原子操作外又新增了以下原子操作：

+ Reading or writing a quadword aligned on a 64-bit boundary（对齐到64位边界的四字的读写）
+ 16-bit accesses to uncached memory locations that fit within a 32-bit data bus（未缓存且在32位数据总线范围之内的内存地址的访问）

从P6 family开始，除了之前支持的原子操作又新增了以下原子操作：

+ Unaligned 16-, 32-, and 64-bit accesses to cached memory that fit within a cache line（对单个cache line中缓存地址的未对齐的16/32/64位访问）

那么哪些操作是非原子的呢？

Accesses to cacheable memory that are split across bus widths, cache lines, and page boundaries are not guaranteed to be atomic by the Intel Core 2 Duo, Intel® Atom™, Intel Core Duo, Pentium M, Pentium 4, Intel Xeon, P6 family, Pentium, and Intel486 processors.

简单来说，那些被总线带宽、cache line 以及 page大小 给分隔开了的内存地址的访问不是原子的，你如果想保证这些操作是原子的，你就得求助于机制（2），对总线发出相应的控制信号才行。

需要注意的是尽管从P6 family开始对一些非对齐的读写操作已经提供了原子性保障，但是非对齐访问是非常影响性能的，需要尽量避免。当然了，对于一般的程序员来说不需要太担心这个，因为大部分编译器会自动帮你完成内存对齐。

下面一道题可以帮助理解硬件原子操作：

**以下多线程对int型变量x的操作，哪几个需要进行同步（）：A. x=y; B. x++; C. ++x; D. x=1;**

可以看下对应的反汇编代码：

.. code-block:: cpp
    :linenos:
    
    // x = y;
    mov eax,dword ptr [y]
    mov dword ptr [x],eax
    
    // x++;
    mov eax,dword ptr [x]
    add eax,1
    mov dword ptr [x],eax

    // ++x;
    mov eax,dword ptr [x]
    add eax,1
    mov dword ptr [x],eax

    // x = 1;
    mov dword ptr [x],1

很显然，x=1是原子操作。因为x是int类型，32位CPU上int占32位，在X86上由硬件直接提供了原子性支持。实际上不管有多少个线程同时执行类似x=1这样的赋值语句，x的值最终还是被赋的值（而不会出现例如某个线程只更新了x的低16位然后被阻塞，另一个线程紧接着又更新了x的低24位然后又被阻塞，从而出现x的值被损坏了的情况）。

再来看x++和++x。其实类似x++, x+=2, ++x这样的操作在多线程环境下是需要同步的。因为X86会按三条指令的形式来处理这种语句：从内存中读x的值到寄存器中，对寄存器加1，再把新值写回x所处的内存地址（见上面的反汇编代码）。

例如有两个线程，它们按照如下顺序执行（注意读x和写回x是原子操作，两个线程不能同时执行）：

.. csv-table:: 多线程执行 x++
    :header: "Time", "Thread1", "Thread2"
    :widths: 10, 20, 20

    0, "load eax, x", ""
    1, "", "load eax, x"
    2, "add eax, 1", "add exa, 1"
    3, "store x, eax", ""
    4, "", "store x, eax"


我们会发现最终x的值会是1而不是2，因为Thread1的结果被覆盖掉了。这种情况需要借助概述中的机制2来实现操作原子性。

最后来看看x=y，在X86上它包含两个操作：读取y至寄存器，再把该值写入x。读y的值这个操作本身是原子的，把值写入x也是原子的，但是两者合起来是不是原子操作呢？这里需要取决于上下文，如果只是简单的 {y = 1; x = y;} 是不需要原子保证的。

举个反例，例如有两个线程，线程1要执行{y = 1; x = y;}，线程2要执行{y = 2; y = 3;}，假设它们按如下时间顺序执行

.. csv-table:: 多线程执行 x=y
    :header: "Time", "Thread1", "Thread2"
    :widths: 10, 20, 20

    0, "store y, 1", ""
    1, "", "store y, 2"
    2, "load eax, y", ""
    3, "", "store y, 3"
    4, "store x, eax", ""

此时线程1的执行语句被线程2打断，导致最终线程1中x的值为2，而不是它原本想要的1。此时则需要加上相应的同步语句确保 y = 2 不会在线程1的两条语句之间发生。

B. *总线锁*

对于硬件无法保证的原子操作，可以通过原子操作原语来保证，原子操作原语一般要基于总线锁实现：在x86 平台上，CPU提供了在指令执行期间对总线加锁的手段。CPU芯片上有一条引线 `#HLOCK pin` ，如果汇编语言的程序中在一条指令前面加上前缀 `LOCK` ，经过汇编以后的机器代码就使CPU在执行这条指令的时候把 `#HLOCK pin` 的电位拉低，持续到这条指令结束时放开，从而把总线锁住，这样同一总线上别的CPU就暂时不能通过总线访问内存了，保证了这条指令在多处理器环境中的原子性。

常见的原子操作原语如下：

+ CAS

这是最常见的原子操作原语。在不同系统下可能有以下命名：`CAS, compare-and-exchange, compare-and-set, std::atomic_compare_exchange, InterlockedCompareExchange, __sync_val_compare_and_swap, LOСK CMPXCHG and other` 。

在某些论文里经常看到 `RMW （read-modify-write）` ，CAS 就是一种RMW，其伪代码如下：

.. code-block:: cpp
    :linenos:

    T compare-and-swap(T* location, T cmp, T xchg) {

        do atomically  
        {
            T val = *location;
            if (cmp == val)
                *location = xchg;
            return val;
        }

    }

如果该地址是期望的值 cmp，这种 RMW 会将一个新的值 xchg 放入地址 location，否则返回location的值。

下面的 `DPDK` 的真实实现代码，第一句MPLOCKED其实是 `lock` 指令，就是锁总线，确保同一时间只有一个CPU线程能写这块内存，然后是 `cmpxchgl` 指令，用于比较并交换操作数，这个指令是原子的。写完之后，通过 `cache一致性模型` 保证所有核心看到和操作的是同一块实际内存的值而不是自己缓存内的值。最后一句 `:"memory"` 是内存屏障（内存屏障属于顺序一致性的内容，后续会单独介绍）。从这里可以看出，`锁` 实际上被移到了CPU内部实现。另外一个需要注意的是，目标内存dst必须是 `volatile` 修饰的，意思是编译器每次遇到这个变量都必须从内存读值，而不能从核心自己的缓存或寄存器读值。

.. code-block:: cpp
    :linenos:

    static inline int
    rte_atomic32_cmpset(volatile uint32_t* dst, uint32_t exp, uint32_t src) {
        uint8_t res;

        asm volatile(
            MPLOCKED
            "cmpxchgl %[src], %[dst];"
            "sete %[res];"
            : [res] "=a"(res),      /* output */
            [dst] "=m"(*dst)
            : [src] "r"(src),       /* input */
            "a"(exp),
            "m"(*dst)
            : "memory");            /* no-clobber list */
        return res;
    }

总结起来就是 `volatile + lock指令 +  cmpxchgl指令 + 缓存一致性模型 + memory指令= 原子操作原语CAS` 。

+ fetch-and-add

`fetch-and-add` 也是一种RMW, 在不同系统下可能有以下命名：`atomic_fetch_add, InterlockedExchangeAdd, LOСK XADD` 。其伪代码如下：

.. code-block:: cpp
    :linenos:

    T fetch-and-add(T* location, T x) {

        do atomically
        {
            T val = *location;
            *location = val + x;
            return val;
        }

    }

同一类型的原语还有 `fetch-and-sub, fetch-and-and, fetch-and-or, fetch-and-xor`。

+ exchange

`exchange` 也是RMW， 同含义的有 `atomic_exchange, XCHG` 。伪代码如下：

.. code-block:: cpp
    :linenos:

    T exchange(T* location, T x) {

        do atomically
        {
            T val = *location;
            *location = x;
            return val;
        }
    }

将新值x放入位置location, 将该位置的旧值返回。 

+ atomic loads and stores

这是非RMW的原子操作，类似的如 `atomic_get, atomic_set, atomic_inc, atomic_dec` 等。