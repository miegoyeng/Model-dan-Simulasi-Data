import simpy
import random
import numpy as np
from tabulate import tabulate

# Parameter simulasi
RANDOM_SEED = 42  # Untuk hasil yang reproducible
NUM_SERVER = 2    # Jumlah server KRS tersedia
ARRIVAL_RATE = 5   # Rata-rata mahasiswa datang per menit (Poisson Process)
SERVICE_TIME = (2, 7)  # Waktu layanan dalam rentang (min, max) menit
SIMULATION_TIME = 120  # Total waktu simulasi dalam menit

# List untuk menyimpan hasil simulasi
data = []
wait_times = []
idle_times = []
last_finish_time = 0

def student(env, name, server):
    global last_finish_time
    arrival_time = env.now
    with server.request() as request:
        yield request
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)
        service_duration = random.uniform(*SERVICE_TIME)
        idle_time = max(0, arrival_time - last_finish_time)
        idle_times.append(idle_time)
        
        system_status = "Busy" if wait_time > 0 else "Idle"
        
        data.append([name, "\033[91mMengakses KRS\033[0m", f"{arrival_time:.2f} ms", "-", system_status])
        data.append([name, "\033[93mSistem Memproses\033[0m", f"{env.now:.2f} ms", f"{wait_time:.2f} ms", system_status])
        yield env.timeout(service_duration)
        data.append([name, "\033[92mKRS Selesai\033[0m", f"{env.now:.2f} ms", "-", "-"])
        
        last_finish_time = env.now

def student_generator(env, server):
    student_id = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / ARRIVAL_RATE))
        student_id += 1
        env.process(student(env, f"Mahasiswa-{student_id}", server))

# Setup dan jalankan simulasi
def run_simulation():
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    server = simpy.Resource(env, capacity=NUM_SERVER)
    env.process(student_generator(env, server))
    env.run(until=SIMULATION_TIME)
    
    # Analisis waktu tunggu
    if wait_times:
        avg_wait = np.mean(wait_times)
        min_wait = np.min(wait_times)
        max_wait = np.max(wait_times)
        avg_idle = np.mean(idle_times) if idle_times else 0
        
        print(tabulate(data, headers=["Nama", "Kegiatan", "Waktu Akses", "Waktu Tunggu", "Status Server"], tablefmt="grid"))
        print(f"\nAnalisis Waktu Tunggu:")
        print(f"Rata-rata waktu tunggu: {avg_wait:.2f} ms")
        print(f"Waktu tunggu minimum: {min_wait:.2f} ms")
        print(f"Waktu tunggu maksimum: {max_wait:.2f} ms")
        print(f"Rata-rata idle server: {avg_idle:.2f} ms")
    else:
        print("Tidak ada data waktu tunggu.")

if __name__ == "__main__":
    run_simulation()