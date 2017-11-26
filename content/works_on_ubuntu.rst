Ubuntu环境配置
#################

:date: 2017-11-26 21:36
:slug: works-on-ubuntu
:summary: 最近家里的电脑从之前的CentOS7迁移到了Ubuntu，各种配置总结汇总在这里，方便日后查看翻阅。
:category: 技术
:tags: Ubuntu

之前VMWare上安装了CentOS7，消耗整机资源还是很大，后来偶然尝试了下Ubuntu，从用户体验到软件配置均便利很多，且资源消耗量也较CentOS小的多。

例行的，安装了Ubuntu之后，少不了各种环境配置、改造之类的工作，这里记录下，方便后续重装、升级后的回归：

1. 系统镜像选择：ubuntu-16.04.3-desktop-amd64，或者其他版本的64位桌面系统。注意，i686为32位系统。
    * 若安装时，VMWare提示已存在Ubuntu，进行简易安装。取消简易安装的方法：新建虚拟机时不要选择镜像。新建后启动时再设置镜像路径。
#. 安装选择
    * 硬件配置：4Core/4G MEM/100G DISK/桥接。其他默认
#. 安装后，重启，取消镜像文件后继续(Enter)
    * 安装VMwareTools；
    * 卸载亚马逊、libreoffice等系统默认软件
        * sudo apt-get remove unity-webapps-common
        * sudo apt-get remove libreoffice-common  
    * 系统环境设置
        * 锁屏。取消锁屏以及恢复时的密码设置
        * 选择外观；开启工作区
        * 设置终端
            * 颜色->浅黄背景黑字。使用背景透明
            * 主题：Tango
    * 安装软件
        * 安装samba服务器
        
        .. code-block:: shell
            :linenos:

            $ sudo apt-get install samba
            $ #修改/etc/samba/smb.conf。追加以下内容（匿名登录）
            [share]
                comment = Share In Ubuntu
                path = /home/ritam/
                browseable = yes
                create mask = 0700
                read only = false
                valid users = ritam
                guest ok = yes
            $ sudo smbpasswd -a ritam
            $ sudo /etc/init.d/samba restart

        * 更新vim （默认的用户体验太差如无法高亮等）

        .. code-block:: shell
            :linenos:
        
            $sudo apt install vim
        
        * 同步原备份文件: .vimrc(.vim_runtime)、.bashrc、g2help、document(blog)、softwares
        * 安装astyle

        .. code-block:: shell
            :linenos:
        
            $sudo apt install astyle

        * 安装pelican
   
        .. code-block:: shell
            :linenos:
        
            $ sudo apt-get install python-pip   
            $ pip install pelican

        * 编译tree

        .. code-block:: shell
            :linenos:
        
            $ cd $tree_source
            $ make
            $ mv tree ~/programes/

        * 安装astyle

        .. code-block:: shell
            :linenos:
        
            $ sudo apt-get install astyle

        * 安装git

        .. code-block:: shell
            :linenos:
        
            $ sudo apt-get install git
            $ #配置git config（重新部署，需要重新git clone代码库）
            $ git config --global user.name "b*********3"
            $ git config --global user.email "b********3@**3.com"
        