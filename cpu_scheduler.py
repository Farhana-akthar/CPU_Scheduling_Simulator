import matplotlib.pyplot as plt

# Function to calculate Waiting Time and Turnaround Time for FCFS and SJF
def calculate_times(processes, arrival, burst):
    n = len(processes)
    waiting = [0]*n
    turnaround = [0]*n

    # For FCFS/SJF assume processes are sorted by arrival
    for i in range(1, n):
        waiting[i] = max(0, waiting[i-1] + burst[i-1] - arrival[i])
    for i in range(n):
        turnaround[i] = waiting[i] + burst[i]
    return waiting, turnaround

# Function to display table and average times
def display_table(processes, arrival, burst, waiting, turnaround):
    print("\nProcess\tArrival\tBurst\tWaiting\tTurnaround")
    for i in range(len(processes)):
        print(f"{processes[i]}\t{arrival[i]}\t{burst[i]}\t{waiting[i]}\t{turnaround[i]}")
    print(f"\nAverage Waiting Time: {sum(waiting)/len(waiting):.2f}")
    print(f"Average Turnaround Time: {sum(turnaround)/len(turnaround):.2f}")

# Function to draw Gantt Chart
def gantt_chart(processes, burst, title="Gantt Chart"):
    start_time = [0]*len(processes)
    for i in range(1, len(processes)):
        start_time[i] = start_time[i-1] + burst[i-1]
    
    fig, gnt = plt.subplots()
    gnt.set_ylim(0, 50)
    gnt.set_xlim(0, sum(burst)+5)
    gnt.set_xlabel('Time')
    gnt.set_yticks([15])
    gnt.set_yticklabels(['CPU'])
    gnt.grid(True)
    
    colors = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple']
    
    for i in range(len(processes)):
        gnt.broken_barh([(start_time[i], burst[i])], (10, 10), facecolors=(colors[i % len(colors)]))
        gnt.text(start_time[i]+burst[i]/2 - 0.5, 15, processes[i], color='white')
    
    plt.title(title)
    plt.show()

# Function for Round Robin Scheduling
def round_robin(processes, burst, time_quantum):
    n = len(processes)
    rem_burst = burst.copy()
    waiting = [0]*n
    turnaround = [0]*n
    t = 0
    gantt_processes = []
    gantt_times = []

    while True:
        done = True
        for i in range(n):
            if rem_burst[i] > 0:
                done = False
                if rem_burst[i] > time_quantum:
                    t += time_quantum
                    rem_burst[i] -= time_quantum
                    gantt_processes.append(processes[i])
                    gantt_times.append(time_quantum)
                else:
                    t += rem_burst[i]
                    waiting[i] = t - burst[i]
                    turnaround[i] = t
                    gantt_processes.append(processes[i])
                    gantt_times.append(rem_burst[i])
                    rem_burst[i] = 0
        if done:
            break
    return waiting, turnaround, gantt_processes, gantt_times

# -------- Main Program --------
print("===== CPU Scheduling Simulator =====")
n = int(input("Enter number of processes: "))
processes = []
arrival = []
burst = []

for i in range(n):
    processes.append(f"P{i+1}")
    arrival.append(int(input(f"Arrival time for P{i+1}: ")))
    burst.append(int(input(f"Burst time for P{i+1}: ")))

print("\nSelect Scheduling Algorithm:")
print("1. FCFS")
print("2. SJF (Non-Preemptive)")
print("3. Round Robin")
choice = int(input("Enter choice (1/2/3): "))

if choice == 1:
    # Sort by arrival time
    combined = sorted(zip(processes, arrival, burst), key=lambda x: x[1])
    processes, arrival, burst = zip(*combined)
    waiting, turnaround = calculate_times(list(processes), list(arrival), list(burst))
    display_table(list(processes), list(arrival), list(burst), waiting, turnaround)
    gantt_chart(list(processes), list(burst), title="FCFS Gantt Chart")

elif choice == 2:
    # Sort by burst time, then arrival time
    combined = sorted(zip(processes, arrival, burst), key=lambda x: (x[2], x[1]))
    processes, arrival, burst = zip(*combined)
    waiting, turnaround = calculate_times(list(processes), list(arrival), list(burst))
    display_table(list(processes), list(arrival), list(burst), waiting, turnaround)
    gantt_chart(list(processes), list(burst), title="SJF Gantt Chart")

elif choice == 3:
    tq = int(input("Enter Time Quantum: "))
    waiting, turnaround, gantt_processes, gantt_times = round_robin(list(processes), list(burst), tq)
    display_table(list(processes), arrival, burst, waiting, turnaround)
    gantt_chart(gantt_processes, gantt_times, title="Round Robin Gantt Chart")

else:
    print("Invalid choice! Exiting...")
