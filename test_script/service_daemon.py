#!/usr/bin/env python
"""
Windows 服务守护进程
自动重启和监控 FastAPI 服务
"""

import subprocess
import sys
import time
import os
from datetime import datetime
import signal


class ServiceDaemon:
    """服务守护进程"""
    
    def __init__(self, script_path="deploy_api.py"):
        self.script_path = script_path
        self.process = None
        self.restart_count = 0
        self.max_restart_per_minute = 5
        self.restart_times = []
        self.running = True
        
    def log(self, message, level="INFO"):
        """输出日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
    def signal_handler(self, signum, frame):
        """处理退出信号"""
        self.log("收到停止信号，正在关闭服务...", "INFO")
        self.running = False
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.log("强制终止服务进程", "WARNING")
                self.process.kill()
        sys.exit(0)
    
    def should_restart(self):
        """检查是否应该重启（防止频繁重启）"""
        now = time.time()
        # 清理1分钟前的重启记录
        self.restart_times = [t for t in self.restart_times if now - t < 60]
        
        if len(self.restart_times) >= self.max_restart_per_minute:
            self.log(f"重启过于频繁（1分钟内重启{len(self.restart_times)}次），等待60秒...", "WARNING")
            time.sleep(60)
            self.restart_times = []
        
        self.restart_times.append(now)
        return True
    
    def start_service(self):
        """启动服务"""
        try:
            self.log("正在启动服务...", "INFO")
            self.process = subprocess.Popen(
                [sys.executable, self.script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            self.log(f"服务已启动 (PID: {self.process.pid})", "INFO")
            return True
        except Exception as e:
            self.log(f"启动服务失败: {e}", "ERROR")
            return False
    
    def monitor_service(self):
        """监控服务输出"""
        try:
            for line in self.process.stdout:
                print(line, end='')
        except Exception as e:
            self.log(f"监控服务输出异常: {e}", "ERROR")
    
    def run(self):
        """运行守护进程"""
        # 注册信号处理
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        self.log("="*80, "INFO")
        self.log("服务守护进程已启动", "INFO")
        self.log("服务地址: http://localhost:8001", "INFO")
        self.log("API 文档: http://localhost:8001/docs", "INFO")
        self.log("自动重启: 已启用", "INFO")
        self.log("="*80, "INFO")
        self.log("按 Ctrl+C 停止服务", "INFO")
        self.log("", "INFO")
        
        while self.running:
            # 启动服务
            if not self.start_service():
                self.log("启动失败，10秒后重试...", "ERROR")
                time.sleep(10)
                continue
            
            # 监控服务
            self.monitor_service()
            
            # 等待进程结束
            exit_code = self.process.wait()
            
            if not self.running:
                break
            
            self.restart_count += 1
            self.log(f"服务已停止 (退出码: {exit_code}, 重启次数: {self.restart_count})", "WARNING")
            
            # 检查是否应该重启
            if self.should_restart():
                self.log("5秒后自动重启...", "INFO")
                time.sleep(5)
            else:
                break
        
        self.log("守护进程已退出", "INFO")


def main():
    """主函数"""
    print("=" * 80)
    print("Windows 服务守护进程")
    print("=" * 80)
    print()
    
    # 检查服务脚本是否存在
    script_path = os.path.join(os.path.dirname(__file__), "deploy_api.py")
    if not os.path.exists(script_path):
        print(f"错误: 找不到服务脚本: {script_path}")
        input("按 Enter 键退出...")
        sys.exit(1)
    
    # 启动守护进程
    daemon = ServiceDaemon(script_path)
    
    try:
        daemon.run()
    except KeyboardInterrupt:
        print("\n收到中断信号，正在退出...")
    except Exception as e:
        print(f"守护进程异常: {e}")
        input("按 Enter 键退出...")
        sys.exit(1)


if __name__ == "__main__":
    main()
