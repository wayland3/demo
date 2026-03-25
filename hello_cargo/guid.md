

错误处理栈：thiserror / anyhow 何时用（库 vs 二进制）。
并发入门：std::thread、Arc、Mutex；与 Go goroutine、Python GIL+线程对比。
Send / Sync：直觉即可，知道「跨线程传递要满足什么」。
产出：多线程统计词频或简单任务队列（无异步）。

阶段六（可选加深）：异步、宏、unsafe
async/.await：tokio 生态；与 Go 调度器对比（模型不同，别硬套）。
宏：声明式宏 macro_rules! 入门；过程宏仅了解用途。
unsafe：何时不可避免；尽量晚学、少写。
贯穿始终的练习建议
主题	小项目idea
所有权	链表/图在标准库外的手写（感受借用难点）
错误处理	小 CLI：读文件、解析、输出
trait/泛型	迷你序列化或「策略」替换
并发	Arc<Mutex<HashMap>> 缓存
