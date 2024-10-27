use std::env;
use std::fs::File;
use std::io::prelude::*;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        eprintln!("[*] Usage: {} <filename>", args[0]);
        std::process::exit(1);
    }

    let file_name = &args[1];
    let file_path = format!("{}.pro", file_name);

    // 创建文件
    let mut file = File::create(file_path).expect("Failed to create file");

    // 写入内容
    let content = "TEMPLATE = subdirs\nSUBDIRS += \n";
    file.write_all(content.as_bytes())
        .expect("Failed to write to file");

    println!("File created and content written successfully.");
}
