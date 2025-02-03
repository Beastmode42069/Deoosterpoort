import sqlite3
import matplotlib.pyplot as plt

def extract_data():
    # Connect to the SQLite database
    conn = sqlite3.connect("detections.db")
    cursor = conn.cursor()

    # Query to extract frame_number, person_count, and timestamp from the detections table
    cursor.execute("SELECT frame_number, person_count, timestamp FROM detections ORDER BY frame_number")
    data = cursor.fetchall()

    conn.close()

    # Extract frame numbers, person counts, and timestamps into separate lists
    frame_numbers = [row[0] for row in data]
    person_counts = [row[1] for row in data]
    timestamps = [row[2] for row in data]

    return frame_numbers, person_counts, timestamps

def count_per_100th_frame(frame_numbers, person_counts, timestamps):
    # Create lists to store the frame numbers, summed counts, and timestamps for every 125th frame
    frame_groups = []
    summed_counts = []
    time_stamps = []
    
    # Iterate through the frames and count only every 100th frame
    for i in range(0, len(frame_numbers), 100):  # Step by 100
        frame_groups.append(frame_numbers[i])
        summed_counts.append(round(person_counts[i]))  # Round the person count to the nearest integer
        time_stamps.append(timestamps[i])  # Get the timestamp for the corresponding frame
    
    return frame_groups, summed_counts, time_stamps

def plot_graph(frame_groups, summed_counts, time_stamps):
    # Create a plot
    plt.figure(figsize=(10, 6))

    # Plot the data
    plt.plot(time_stamps, summed_counts, marker='o', color='b', label='People Count (Every 100th Frame)')

    # Adding title and labels
    plt.title("People Count Every 100th Frame (With Timestamps)", fontsize=16)
    plt.xlabel("Time (Seconds)", fontsize=12)
    plt.ylabel("People Count", fontsize=12)

    # Ensure y-axis ticks are whole numbers
    plt.yticks(range(min(summed_counts), max(summed_counts) + 1))

    # Annotate each point with the people count and the time it was counted
    for i in range(len(time_stamps)):
        plt.text(time_stamps[i], summed_counts[i], f'{summed_counts[i]}', ha='center', va='bottom', fontsize=10)

    # Display the plot
    plt.grid(True)
    plt.legend()
    plt.show()

def main():
    # Extract data from the database
    frame_numbers, person_counts, timestamps = extract_data()

    # Count people every 100th frame
    frame_groups, summed_counts, time_stamps = count_per_100th_frame(frame_numbers, person_counts, timestamps)

    # Plot the graph with annotations
    plot_graph(frame_groups, summed_counts, time_stamps)

if __name__ == "__main__":
    main()
