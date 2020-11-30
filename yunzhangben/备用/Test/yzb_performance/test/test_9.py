import psutil

print("CPU逻辑数量",psutil.cpu_count()) # CPU逻辑数量

print("CPU物理核心",psutil.cpu_count(logical=False)) # CPU物理核心
print("总内存大小是",psutil.virtual_memory())
print("交换区大小是:",psutil.swap_memory())

#统计CPU的用户／系统／空闲时间：
print("统计CPU的用户／系统／空闲时间：",psutil.cpu_times())

#通过psutil获取磁盘分区、磁盘使用率和磁盘IO信息：
print("磁盘分区信息：",psutil.disk_partitions())
print("磁盘使用情况：",psutil.disk_usage('/'))
print("磁盘IO：",psutil.disk_io_counters())

#获取网络信息
print("# 获取网络读写字节／包的个数",psutil.net_io_counters())
print("获取网络接口信息",psutil.net_if_addrs())
print("获取网络接口状态",psutil.net_if_stats())

#要获取当前网络连接信息，使用net_connections()：
print("获取当前网络连接信息",psutil.net_connections())


#获取进程信息
print("所有进程ID",psutil.pids())
#p = psutil.Process(3776) # 获取指定进程ID=3776，其实就是当前Python交互环境
# print("进程名称",p.name())
# print("进程exe路径",p.exe())
# print("进程工作目录",p.cwd())
# print("进程启动的命令行",p.cmdline())
# print("父进程",p.parent())
# print("子进程列表",p.children())
# print("进程状态",p.status())
# print("进程用户名",p.username())
# print("进程创建时间",p.create_time())
# print("进程终端",p.terminal())
# print("进程使用的CPU时间",p.cpu_times())
# print("进程使用的内存",p.memory_info())
# print("进程打开的文件",p.open_files())
# print("进程相关网络连接",p.connections())
# print("进程的线程数量",p.num_threads())
# print("所有线程信息",p.threads())
# print("进程环境变量",p.environ())
# print("结束进程",p.terminate())

print("模拟出ps命令的效果:",psutil.test())
