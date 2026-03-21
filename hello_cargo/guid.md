

#### 4. 读 stdin + CLI 参数（阶段一产出示例）

```rust
use std::env;
use std::io::{self, BufRead};

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    println!("程序名: {}", args[0]);
    for (i, a) in args.iter().enumerate().skip(1) {
        println!("参数 {i}: {a}");
    }

    let stdin = io::stdin();
    println!("输入一行回车：");
    let mut line = String::new();
    stdin.lock().read_line(&mut line)?;
    println!("你输入了: {}", line.trim_end());
    Ok(())
}
```

**说明**：`main` 返回 `Result<(), E>` 时，错误会在退出时打印（Rust 1.26+）；`read_line` 会把换行也读进 `String`，展示用 `trim_end()`。

#### 5. 对照 Go：包 vs `mod` / `use`

- **Go**：`package foo`，同目录多为同一包，`import "path/to/bar"`。
- **Rust**：一个 **crate**（库或二进制）一棵模块树；`src/main.rs` 或 `src/lib.rs` 是 crate 根；`mod child;` 对应文件 `src/child.rs` 或 `src/child/mod.rs`；`use crate::child::Thing` 把路径拉进当前作用域。
- **要点**：Rust 的「可见性」靠 `pub`，默认模块内私有；Go 则是首字母大写导出。

极简双文件示例（需 `cargo new` 后自行加 `src/config.rs` 并在 `main.rs` 顶部写 `mod config;`）：

```rust
// src/config.rs
pub const APP_NAME: &str = "demo";

// src/main.rs
mod config;

fn main() {
    println!("{}", config::APP_NAME);
}
```

#### 6. 对照 Python：无隐式转换、debug 下整数溢出

```rust
fn main() {
    let a: i32 = 10;
    // let b: u32 = a;  // 编译错误：不允许无提示的 i32 -> u32

    let x: i8 = 100;
    let y: i8 = 50;
    // let z = x + y;   // debug 下可能 panic：算术溢出检查
    let z = x.checked_add(y).expect("overflow");  // 显式处理更安全
    println!("{z}");
}
```

**说明**：`cargo build` 默认 debug 开启溢出检查；`cargo build --release` 下溢出为**未定义行为**（与 C 类似），生产里对可能溢出的运算用 `checked_*` / `saturating_*` / `wrapping_*`。

---

阶段二：所有权三件套（核心，约 1–2 周，可拉长）
所有权：move、Copy 类型 vs 非 Copy；String vs &str。
借用：& / &mut、同一作用域内可变借用唯一性；与 Python「全是引用」、Go「指针+GC」对比。
生命周期（先直觉）：为什么编译器要标注；常见模式「输入生命周期 = 输出生命周期」；暂时不深究复杂签名。
Result / Option：? 运算符；与 Go 的 (T, error)、Python 异常对比——显式错误在类型里。
产出：实现一个小库函数（例如解析一行配置、返回 Result），再写一个调用它的 main。

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