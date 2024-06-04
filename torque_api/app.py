import subprocess
import asyncio
import psutil
import pandas as pd


class JobScheduler:
    def __init__(self):
        self.running_jobs = {}

    def submit_job(self, job_script_file, function_name="submit_job"):
        try:
            result = subprocess.run(
                ['qsub', job_script_file], check=True, capture_output=True, text=True)
            job_id = str(result.stdout.strip())
            print(f"job submitted succesfully, job ID:{job_id}")
            if job_id in self.running_jobs:
                self.running_jobs[job_id].append(function_name)
            else:
                self.running_jobs[job_id] = [function_name]
            return job_id
        except subprocess.CalledProcessError as e:
            print(f"submit fail, error: {e.stderr}")

    def see_job_status(self, job_id):
        try:
            if job_id is not None:
                result = subprocess.run(['qstat', job_id], check=True,
                                        capture_output=True, text=True)
                print(result.stdout)
            else:
                result = subprocess.run('qstat', check=True,
                                        capture_output=True, text=True)
                print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"fail to retrieve the job, error: {e.stderr}")

    def query_job_priority(self, job_id):
        output = subprocess.run(['qstat', 'f', str(job_id)])
        try:
            if output:
                for line in output.split('\n'):
                    if 'priority' in line.lower():
                        priority = line.split('=')[-1].strip()
                        return priority
        except:
            print("query job priority fail")

    def delete_job(self, job_id):
        try:
            temp_job_id = job_id
            subprocess.run(
                ['qdel', job_id], check=True, capture_output=True, text=True)
            print(f"job deleted succesfully, deleted job id:{temp_job_id}")

        except subprocess.CalledProcessError as e:
            print(f"fail to delete task, error:{e.stderr}")

    def change_job_priority(self, job_id, priority):
        try:
            subprocess.run(
                ['qalter', '-p', str(priority), job_id], check=True, capture_output=True, text=True
            )
            print("change job successful")
        except subprocess.CalledProcessError as e:
            print(f"fail to change priority, error:{e.stderr}")

    def increment_job_priority(self, job_id, increment):
        current_priority = self.query_job_priority(job_id)
        try:
            self.change_job_priority(job_id, int(current_priority + increment))
        except:
            print("changing fail")

    def decrement_job_priority(self, job_id, decrement):
        current_priority = self.query_job_priority(job_id)
        try:
            if current_priority - decrement < 0:
                self.change_job_priority(
                    job_id, int(current_priority - decrement))
        except:
            print("changing fail")

    def change_priority_list(self, job_ids, priority):
        for job_id in job_ids:
            self.change_job_priority(job_id, priority)

    async def is_job_running(self, job_id):
        try:
            result = (subprocess.run(['qstat', job_id], check=True,
                                     capture_output=True, text=True))
            output_lines = result.stdout.split('\n')
            data = [line.split() for line in output_lines]
            if data[2][4] == "R":
                return True
            else:
                return False
        except subprocess.CalledProcessError as e:
            return print(e.stderr)

    async def monitor_jobs(self):
        while self.running_jobs:
            not_completed_jobs = []
            jobs_to_remove = []
            for job_id, function_name in self.running_jobs.items():
                if await self.is_job_running(job_id):
                    not_completed_jobs.append(job_id)
                else:
                    print(f"Job ID: {job_id} ({function_name}) has completed.")
                    jobs_to_remove.append(job_id)
            for job_id in jobs_to_remove:
                del self.running_jobs[job_id]
            print(f"Jobs still running: {self.running_jobs}")
            await asyncio.sleep(10)


# scheduler = JobScheduler()
# scheduler.submit_job("sample_pbs.pbs")
# scheduler.submit_job("sample_pbs.pbs")
# scheduler.submit_job("sample_pbs.pbs")
# scheduler.submit_job("sample_pbs.pbs")
# scheduler.submit_job("sample_pbs.pbs")
# scheduler.submit_job("sample_pbs.pbs")
# scheduler.submit_job("sample_pbs.pbs")
# print(asyncio.run(scheduler.monitor_jobs()))
