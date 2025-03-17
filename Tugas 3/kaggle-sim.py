import pandas as pd
import simpy
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np


file_path = "Customer_support_data.csv"
df = pd.read_csv(file_path)


df["Issue_reported at"] = pd.to_datetime(df["Issue_reported at"], errors="coerce")
df["issue_responded"] = pd.to_datetime(df["issue_responded"], errors="coerce")


df["waiting_time"] = (df["issue_responded"] - df["Issue_reported at"]).dt.total_seconds()
df = df.dropna(subset=["waiting_time"])  


class CustomerServiceSystem:
    def __init__(self, env, num_agents, service_time):
        self.env = env
        self.agent = simpy.Resource(env, num_agents)
        self.service_time = service_time
    
    def serve_customer(self, customer_id):
        service_duration = np.random.exponential(self.service_time)
        yield self.env.timeout(service_duration)


def run_simulation(num_agents, service_time, num_customers):
    env = simpy.Environment()
    system = CustomerServiceSystem(env, num_agents, service_time)
    
    def customer(env, customer_id, system):
        arrival_time = env.now
        with system.agent.request() as request:
            yield request
            yield env.process(system.serve_customer(customer_id))
            waiting_time = env.now - arrival_time
            waiting_times.append(waiting_time)
    
    global waiting_times
    waiting_times = []
    for i in range(num_customers):
        env.process(customer(env, i, system))
    env.run()
    return waiting_times


num_agents = 5
service_time = df["waiting_time"].mean()
num_customers = 100
simulated_waiting_times = run_simulation(num_agents, service_time, num_customers)


plt.figure(figsize=(10, 5))
sns.histplot(simulated_waiting_times, bins=30, kde=True)
plt.xlabel("Waiting Time (seconds)")
plt.ylabel("Frequency")
plt.title("Distribution of Simulated Waiting Times")
plt.show()


df["hour"] = df["Issue_reported at"].dt.hour
hourly_counts = df.groupby("hour").size()
plt.figure(figsize=(10, 5))
sns.heatmap(hourly_counts.values.reshape(-1, 1), annot=True, fmt="d", cmap="coolwarm", cbar=False)
plt.xlabel("Hour of Day")
plt.ylabel("Number of Issues Reported")
plt.title("Customer Issues Reported by Hour")
plt.show()


if "CSAT Score" in df.columns:
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x=df["waiting_time"], y=df["CSAT Score"], alpha=0.5)
    plt.xlabel("Waiting Time (seconds)")
    plt.ylabel("CSAT Score")
    plt.title("Correlation between Waiting Time and CSAT Score")
    plt.show()
