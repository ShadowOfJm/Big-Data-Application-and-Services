# generate_dmesg_for_wordcount.py

import random

def generate_dmesg_log(filename="dmesg.log", num_lines=1000):
    """
    生成一个模拟的 dmesg 日志文件，用于 Hadoop WordCount 示例。

    Args:
        filename (str): 要生成的文件名。
        num_lines (int): 要生成的日志行数。
    """
    # 模拟一些常见的内核日志词汇
    log_words = [
        "kernel", "system", "boot", "memory", "cpu", "driver", "usb", "network",
        "ethernet", "wifi", "disk", "partition", "filesystem", "mounted", "error",
        "warning", "info", "initialized", "detected", "found", "loading", "module",
        "device", "attached", "detached", "failed", "success", "timeout", "buffer",
        "cache", "interrupt", "timer", "clock", "acpi", "power", "battery", "thermal",
        "input", "mouse", "keyboard", "audio", "video", "graphics", "display",
        "started", "finished", "process", "task", "scheduler", "context", "switch",
        "page", "fault", "segmentation", "protection", "user", "root", "login",
        "authentication", "security", "audit", "log", "message", "service", "daemon",
        "configuration", "setting", "parameter", "option", "value", "status", "state",
        "running", "stopped", "active", "inactive", "enabled", "disabled", "ok", "done"
    ]

    # 一些常见的短语结构
    phrases = [
        "{word1}: {word2} {word3} initialized",
        "{word1}: {word2} driver loaded successfully",
        "{word1}: {word2} device attached",
        "{word1}: {word2} error - {word3} failed",
        "{word1}: {word2} warning - {word3} timeout",
        "{word1}: {word2} info - {word3} started",
        "{word1}: {word2} {word3} detected",
        "system: {word1} and {word2} are {word3}",
        "boot: {word1} {word2} process {word3}",
        "memory: {word1} buffer {word2} allocated for {word3}",
        "{word1}: {word2} module {word3}",
        "network: {word1} {word2} interface {word3}",
        "disk: {word1} partition {word2} {word3}",
        "filesystem: {word1} mounted on {word2} status {word3}",
        "{word1}: {word2} {word3} finished",
        "acpi: {word1} power {word2} state {word3}",
        "input: {word1} {word2} {word3} event",
        "audio: {word1} {word2} {word3} configured"
    ]

    with open(filename, 'w', encoding='utf-8') as f:
        for _ in range(num_lines):
            # 随机选择一个短语模板
            template = random.choice(phrases)
            # 填充随机词汇
            log_entry = template.format(
                word1=random.choice(log_words),
                word2=random.choice(log_words),
                word3=random.choice(log_words)
            )
            # 写入文件并换行
            f.write(log_entry + "\n")

    print(f"已生成包含 {num_lines} 行模拟日志的文件: {filename}")

if __name__ == "__main__":
    generate_dmesg_log()
