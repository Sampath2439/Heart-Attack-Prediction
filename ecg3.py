import serial
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from drawnow import *

def main():
    # Start serial communication between the computer and Arduino.
    arduino = serial.Serial('COM11', 9600)
    quantity = 'a'

    while isinstance(quantity, float) is False:
        try:
            minutes = float(input('Recording time (minutes) >> '))

            ###########################################################################
            # Number of samples to be taken. The script won't stop until all samples are collected.
            # For testing, use a small number, e.g., 0.1 = 1500 samples.
            # 250 is the sampling frequency, 250 samples per second, configure in the Arduino script.
            ############################################################################

            quantity = minutes * 5 * 250
        except ValueError:
            minutes = input('Enter the recording time again >> ')

    print('Starting')

    plt.ion()  # Interactive mode for real-time plotting.

    # Function for real-time plotting.
    def plot_real_time():
        plt.ylim(100, 650)  # Y-axis limits
        plt.plot(data)  # Plot ECG data from the 'data' array.
        plt.xlabel('Time (milliseconds)')
        plt.ylabel('Voltage (mV)')
        plt.title('Electrocardiogram')
        plt.ticklabel_format(useOffset=False)  # Do not autoscale the Y-axis.

    # Array to store sensor data.
    data = []

    while len(data) < quantity:
        try:
            info = arduino.readline()
            try:
                float_info = int(info)
                data.append(float_info)
            except ValueError:
                print("Invalid data format:", info)

            drawnow(plot_real_time)
            plt.pause(0.00000001)

        except KeyboardInterrupt:
            break

    print('Data captured')

    # Create a DataFrame and save the data to a CSV file.
    ecg_data = pd.DataFrame({'ECG_Value': data})
    name = input("File name: ")
    filename = name + ".csv"
    ecg_data.to_csv(filename, index=False)

    # Analyze the acquired data from the sensor.
    ecg_data = pd.read_csv(filename)
    ecg_values = ecg_data['ECG_Value']

    # Detect R-peaks in the ECG signal.
    peaks, _ = find_peaks(ecg_values, distance=150)
    distances = np.diff(peaks)

    # Calculate and display beats per minute (BPM).
    bpm = (ecg_values.size / np.mean(distances)) / (ecg_values.size / 15000)

    print('Detected {} beats per minute.'.format(round(bpm)))

    # Show the graph of detected R-peaks.
    fig1 = plt.figure(1)
    plt.plot(ecg_values, 'b')
    plt.plot(peaks, ecg_values[peaks], 'rx')

    # Show the graph of the distribution of distances between R-peaks, equivalent to a heartbeat.
    fig2 = plt.figure(2)
    plt.hist(distances)
    plt.xlabel('Distance (samples)')
    plt.ylabel('Frequency')
    plt.title('Distribution of distance between local maxima (peaks)')
    plt.show()

    # Save the generated graphs as images.
    save = input('Save images? (s = yes, n = no): ')

    if save.lower() == 's':
        fig1.savefig(name + "_ecg.png")
        fig2.savefig(name + "_dist.png")
    else:
        pass

# Call the main function.
if __name__ == '__main__':
    main()
