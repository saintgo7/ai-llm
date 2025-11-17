"""
30. Task Scheduler - 작업 스케줄러
"""
import time
import threading
from datetime import datetime, timedelta
from queue import PriorityQueue, Queue
import schedule

class Task:
    """스케줄된 작업"""

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.next_run = None
        self.interval = None
        self.repeat = True

    def run(self):
        """작업 실행"""
        try:
            result = self.func(*self.args, **self.kwargs)
            return True, result
        except Exception as e:
            return False, str(e)

    def should_run(self):
        """실행 시간 확인"""
        if self.next_run is None:
            return False
        return datetime.now() >= self.next_run

class TaskScheduler:
    """간단한 작업 스케줄러"""

    def __init__(self):
        self.tasks = []
        self.running = False
        self.thread = None

    def every(self, interval):
        """일정 간격으로 실행"""
        return IntervalTask(self, interval)

    def at(self, time_str):
        """특정 시간에 실행"""
        return TimeTask(self, time_str)

    def once(self, delay_seconds=0):
        """한 번만 실행"""
        return OnceTask(self, delay_seconds)

    def add_task(self, task):
        """작업 추가"""
        self.tasks.append(task)

    def start(self):
        """스케줄러 시작"""
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print("Scheduler started")

    def stop(self):
        """스케줄러 정지"""
        self.running = False
        if self.thread:
            self.thread.join()
        print("Scheduler stopped")

    def _run(self):
        """스케줄러 실행 루프"""
        while self.running:
            current_time = datetime.now()

            for task in self.tasks[:]:
                if task.should_run():
                    success, result = task.run()

                    if success:
                        print(f"[{current_time}] Task executed: {task.func.__name__}")
                    else:
                        print(f"[{current_time}] Task failed: {task.func.__name__} - {result}")

                    # 반복 작업이면 다음 실행 시간 설정
                    if task.repeat and task.interval:
                        task.next_run = current_time + task.interval
                    elif not task.repeat:
                        self.tasks.remove(task)

            time.sleep(1)  # 1초마다 체크

class IntervalTask:
    """간격 기반 작업"""

    def __init__(self, scheduler, seconds):
        self.scheduler = scheduler
        self.seconds = seconds

    def do(self, func, *args, **kwargs):
        """작업 등록"""
        task = Task(func, *args, **kwargs)
        task.interval = timedelta(seconds=self.seconds)
        task.next_run = datetime.now() + task.interval
        task.repeat = True
        self.scheduler.add_task(task)
        return task

class TimeTask:
    """시간 기반 작업"""

    def __init__(self, scheduler, time_str):
        self.scheduler = scheduler
        self.time_str = time_str

    def do(self, func, *args, **kwargs):
        """작업 등록"""
        task = Task(func, *args, **kwargs)

        # 시간 파싱 (HH:MM 형식)
        hour, minute = map(int, self.time_str.split(':'))
        now = datetime.now()
        next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        if next_run <= now:
            next_run += timedelta(days=1)

        task.next_run = next_run
        task.interval = timedelta(days=1)
        task.repeat = True
        self.scheduler.add_task(task)
        return task

class OnceTask:
    """일회성 작업"""

    def __init__(self, scheduler, delay_seconds):
        self.scheduler = scheduler
        self.delay_seconds = delay_seconds

    def do(self, func, *args, **kwargs):
        """작업 등록"""
        task = Task(func, *args, **kwargs)
        task.next_run = datetime.now() + timedelta(seconds=self.delay_seconds)
        task.repeat = False
        self.scheduler.add_task(task)
        return task

class PriorityScheduler:
    """우선순위 기반 작업 스케줄러"""

    def __init__(self, num_workers=3):
        self.task_queue = PriorityQueue()
        self.workers = []
        self.running = False
        self.num_workers = num_workers

    def add_task(self, priority, func, *args, **kwargs):
        """작업 추가 (낮은 숫자가 높은 우선순위)"""
        self.task_queue.put((priority, func, args, kwargs))

    def start(self):
        """워커 시작"""
        self.running = True

        for i in range(self.num_workers):
            worker = threading.Thread(target=self._worker, args=(i,), daemon=True)
            worker.start()
            self.workers.append(worker)

        print(f"Started {self.num_workers} workers")

    def stop(self):
        """워커 정지"""
        self.running = False
        for worker in self.workers:
            worker.join()
        print("All workers stopped")

    def _worker(self, worker_id):
        """워커 스레드"""
        while self.running:
            try:
                priority, func, args, kwargs = self.task_queue.get(timeout=1)
                print(f"[Worker {worker_id}] Executing task (priority: {priority})")
                func(*args, **kwargs)
                self.task_queue.task_done()
            except:
                pass

# 샘플 작업 함수들
def backup_database():
    print("  Backing up database...")

def send_email(to, subject):
    print(f"  Sending email to {to}: {subject}")

def cleanup_temp_files():
    print("  Cleaning up temporary files...")

def generate_report():
    print("  Generating daily report...")

if __name__ == '__main__':
    print("=== Task Scheduler Demo ===\n")

    # 스케줄러 생성
    scheduler = TaskScheduler()

    # 5초마다 실행
    scheduler.every(5).do(backup_database)

    # 3초마다 이메일 발송
    scheduler.every(3).do(send_email, "admin@example.com", "Status Update")

    # 일회성 작업 (2초 후)
    scheduler.once(2).do(cleanup_temp_files)

    # 특정 시간에 실행 (데모를 위해 현재 시간 + 1분)
    next_minute = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")
    scheduler.at(next_minute).do(generate_report)

    # 스케줄러 시작
    scheduler.start()

    try:
        # 15초 동안 실행
        print("Running scheduler for 15 seconds...\n")
        time.sleep(15)
    except KeyboardInterrupt:
        pass
    finally:
        scheduler.stop()

    print("\n=== Priority Scheduler Demo ===\n")

    # 우선순위 스케줄러
    prio_scheduler = PriorityScheduler(num_workers=2)
    prio_scheduler.start()

    # 작업 추가 (낮은 숫자가 높은 우선순위)
    prio_scheduler.add_task(1, lambda: print("  HIGH priority task"))
    prio_scheduler.add_task(5, lambda: print("  LOW priority task"))
    prio_scheduler.add_task(3, lambda: print("  MEDIUM priority task"))
    prio_scheduler.add_task(1, lambda: print("  Another HIGH priority task"))

    # 작업 완료 대기
    time.sleep(3)
    prio_scheduler.stop()
