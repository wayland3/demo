fn main() {
    let mut s = 123;
    s = 321;
    println!("{s}");
}
// 1. Move (所有权转移)
fn move_example() {
    let s1 = String::from("hello"); // 堆上分配的字符串
    let s2 = s1;                    // s1 的所有权转移到 s2。本质是栈上的指针、长度、容量被复制，堆内存不变。
    
    // println!("{}", s1);          // 编译错误：use of moved value 's1'。防止由于离开作用域导致的 Double Free。
    println!("s2: {}", s2);
}