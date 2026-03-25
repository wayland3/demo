阶段三：trait、泛型、迭代器（约 1 周）
trait：类似 interface，但有孤儿规则、默认实现、dyn Trait 对象。
泛型与约束：where 子句；常见 trait：Debug、Clone、Default、Iterator。
迭代器：iter / into_iter / iter_mut；map/filter/collect；和 Python 生成器、Go range 对照。
产出：把阶段二的代码改成泛型或拆成 trait，或手写一个小型「管道」式数据处理。

阶段四：模块、测试、文档（约 2–3 天）
mod 树、pub、crate 根、lib.rs vs main.rs。
单元测试、集成测试目录约定；#[cfg(test)]。
文档注释 /// 与 cargo doc --open。
产出：一个含 lib + 测试 + 简短 README 的小项目。

阶段五：常见标准库与习惯用法（约 1 周）
错误处理栈：thiserror / anyhow 何时用（库 vs 二进制）。
字符串与路径：OsString、路径 API；编码意识（UTF-8）。
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
推荐资源（精简）
The Rust Book（官方，主线）
Rust by Example（对照抄改）
Rustlings（习题，强推配合阶段二、三）

如果你愿意，也可以说一下目标（写 CLI / Web / 嵌入式 / 刷题），计划里「阶段五、六」的侧重点可以替你改一版更贴目标的路线。