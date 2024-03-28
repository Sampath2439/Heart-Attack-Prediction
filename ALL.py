import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

fs = 100  # Sample frequency

heartbeat = pd.read_csv(r"D:\CSP Project\sample.csv")

# Replace this with your detected R-peak indices
r_peak_indices = [36  ,70 ,107 ,181 ,215 ,264,316 ,355 ,409 ,440 ,476 ,549 ,577 ,629 ,667 ,701 ,749 ,797 ,858 ,889 ,937 ,991]

# Define windows for P, Q, R, and S peak detection (adjust as needed)
window_before_r = int(0.1 * fs)  # 100 ms before R-peak
window_after_r = int(0.1 * fs)   # 100 ms after R-peak
window_before_q = int(0.05 * fs)  # 50 ms before R-peak

p_peak_indices = []
q_peak_indices = []
r_peak_values = []  # Store the R-peak values for reference
s_peak_indices = []

for r_peak_index in r_peak_indices:
    r_peak_value = heartbeat.iloc[:, 0][r_peak_index]

    # Detect P-peak (local maximum) within the window before R-peak
    p_peak_index = r_peak_index - np.argmax(heartbeat.iloc[:, 0][r_peak_index - window_before_r:r_peak_index])

    # Detect Q-peak (local minimum) within the window before R-peak
    q_peak_index = r_peak_index - np.argmin(heartbeat.iloc[:, 0][r_peak_index - window_before_q:r_peak_index])

    # Detect S-peak (local minimum) within the window after R-peak
    s_peak_index = r_peak_index + np.argmin(heartbeat.iloc[:, 0][r_peak_index:r_peak_index + window_after_r])

    # Append P, Q, R, and S peak indices to their respective lists
    p_peak_indices.append(p_peak_index)
    q_peak_indices.append(q_peak_index)
    r_peak_values.append(r_peak_value)
    s_peak_indices.append(s_peak_index)

# Plot the ECG signal with P, Q, R, and S peaks
plt.plot(heartbeat.iloc[:, 0][0:1000])
plt.plot(r_peak_indices, r_peak_values, 'ro', label='R-peaks')
plt.plot(p_peak_indices, heartbeat.iloc[:, 0][0:1000][p_peak_indices], 'go', label='P-peaks')
plt.plot(q_peak_indices, heartbeat.iloc[:, 0][0:1000][q_peak_indices], 'yo', label='Q-peaks')
plt.plot(s_peak_indices, heartbeat.iloc[:, 0][0:1000][s_peak_indices], 'bo', label='S-peaks')

plt.legend()
plt.show()
