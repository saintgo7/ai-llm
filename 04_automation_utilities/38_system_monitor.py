"""
38. System Monitor - 시스템 모니터링 도구
"""
import psutil
import platform
import time
from datetime import datetime, timedelta

class SystemMonitor:
    """시스템 리소스 모니터"""

    @staticmethod
    def get_cpu_info():
        """CPU 정보"""
        return {
            'physical_cores': psutil.cpu_count(logical=False),
            'total_cores': psutil.cpu_count(logical=True),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'cpu_freq': psutil.cpu_freq().current if psutil.cpu_freq() else 0,
            'per_cpu': psutil.cpu_percent(interval=1, percpu=True)
        }

    @staticmethod
    def get_memory_info():
        """메모리 정보"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        return {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'percent': mem.percent,
            'swap_total': swap.total,
            'swap_used': swap.used,
            'swap_percent': swap.percent
        }

    @staticmethod
    def get_disk_info():
        """디스크 정보"""
        partitions = psutil.disk_partitions()
        disk_info = []

        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                })
            except PermissionError:
                continue

        return disk_info

    @staticmethod
    def get_network_info():
        """네트워크 정보"""
        net_io = psutil.net_io_counters()

        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'errin': net_io.errin,
            'errout': net_io.errout
        }

    @staticmethod
    def get_process_list(limit=10):
        """프로세스 목록 (CPU 사용률 순)"""
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # CPU 사용률로 정렬
        processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)

        return processes[:limit]

    @staticmethod
    def get_system_info():
        """시스템 정보"""
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time

        return {
            'system': platform.system(),
            'node_name': platform.node(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'boot_time': boot_time,
            'uptime': str(uptime).split('.')[0]
        }

    @staticmethod
    def get_battery_info():
        """배터리 정보"""
        if hasattr(psutil, 'sensors_battery'):
            battery = psutil.sensors_battery()
            if battery:
                return {
                    'percent': battery.percent,
                    'secsleft': battery.secsleft,
                    'power_plugged': battery.power_plugged
                }
        return None

    @staticmethod
    def format_bytes(bytes):
        """바이트를 읽기 쉬운 형식으로 변환"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024
        return f"{bytes:.2f} PB"

    @classmethod
    def print_system_status(cls):
        """시스템 상태 출력"""
        print("=== SYSTEM STATUS ===\n")

        # 시스템 정보
        sys_info = cls.get_system_info()
        print(f"System: {sys_info['system']} {sys_info['release']}")
        print(f"Node: {sys_info['node_name']}")
        print(f"Uptime: {sys_info['uptime']}\n")

        # CPU
        cpu = cls.get_cpu_info()
        print(f"--- CPU ---")
        print(f"Cores: {cpu['physical_cores']} physical, {cpu['total_cores']} logical")
        print(f"Usage: {cpu['cpu_percent']}%")
        print(f"Frequency: {cpu['cpu_freq']:.2f} MHz\n")

        # 메모리
        mem = cls.get_memory_info()
        print(f"--- Memory ---")
        print(f"Total: {cls.format_bytes(mem['total'])}")
        print(f"Available: {cls.format_bytes(mem['available'])}")
        print(f"Used: {cls.format_bytes(mem['used'])} ({mem['percent']}%)")
        print(f"Swap: {cls.format_bytes(mem['swap_used'])} / {cls.format_bytes(mem['swap_total'])} ({mem['swap_percent']}%)\n")

        # 디스크
        print(f"--- Disk ---")
        for disk in cls.get_disk_info():
            print(f"{disk['mountpoint']}: {cls.format_bytes(disk['used'])} / {cls.format_bytes(disk['total'])} ({disk['percent']}%)")
        print()

        # 네트워크
        net = cls.get_network_info()
        print(f"--- Network ---")
        print(f"Sent: {cls.format_bytes(net['bytes_sent'])}")
        print(f"Received: {cls.format_bytes(net['bytes_recv'])}\n")

        # 배터리
        battery = cls.get_battery_info()
        if battery:
            print(f"--- Battery ---")
            print(f"Charge: {battery['percent']}%")
            print(f"Plugged In: {battery['power_plugged']}\n")

        # 프로세스
        print(f"--- Top 5 Processes (by CPU) ---")
        for i, proc in enumerate(cls.get_process_list(5), 1):
            print(f"{i}. {proc['name']} (PID {proc['pid']}): CPU {proc.get('cpu_percent', 0):.1f}%, MEM {proc.get('memory_percent', 0):.1f}%")

class ResourceMonitor:
    """리소스 모니터링 및 경고"""

    def __init__(self, cpu_threshold=80, memory_threshold=80, disk_threshold=90):
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.disk_threshold = disk_threshold
        self.alerts = []

    def check_resources(self):
        """리소스 체크 및 경고"""
        self.alerts = []

        # CPU 체크
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > self.cpu_threshold:
            self.alerts.append(f"HIGH CPU: {cpu_percent}%")

        # 메모리 체크
        mem_percent = psutil.virtual_memory().percent
        if mem_percent > self.memory_threshold:
            self.alerts.append(f"HIGH MEMORY: {mem_percent}%")

        # 디스크 체크
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                if usage.percent > self.disk_threshold:
                    self.alerts.append(f"HIGH DISK ({partition.mountpoint}): {usage.percent}%")
            except PermissionError:
                pass

        return self.alerts

    def monitor(self, interval=5, duration=60):
        """지속적 모니터링"""
        end_time = time.time() + duration
        print(f"Monitoring for {duration} seconds...\n")

        while time.time() < end_time:
            alerts = self.check_resources()

            if alerts:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ALERTS:")
                for alert in alerts:
                    print(f"  ⚠ {alert}")
            else:
                cpu = psutil.cpu_percent(interval=1)
                mem = psutil.virtual_memory().percent
                print(f"[{datetime.now().strftime('%H:%M:%S')}] OK - CPU: {cpu}%, MEM: {mem}%")

            time.sleep(interval)

# 사용 예제
if __name__ == '__main__':
    print("=== System Monitor Demo ===\n")

    # 시스템 상태 출력
    SystemMonitor.print_system_status()

    # 리소스 모니터링
    print("\n=== Resource Monitoring ===")
    monitor = ResourceMonitor(cpu_threshold=50, memory_threshold=50)

    print("\nChecking resources once...")
    alerts = monitor.check_resources()
    if alerts:
        for alert in alerts:
            print(f"⚠ {alert}")
    else:
        print("✓ All resources within normal limits")

    # 실시간 모니터링 (15초)
    print("\n=== Live Monitoring (15 seconds) ===")
    monitor.monitor(interval=3, duration=15)

    print("\nNote: Install psutil with: pip install psutil")
