def main(args):
    # Read CSV file
    timestamps, gyro_data, accel_data = read_imu_csv(imu_csv_file)
    
    N = len(timestamps) # number of measurement samples
    data = np.vstack((accel_data.T, gyro_data.T))

    for axis in range(data.shape[0]):
        # Calculate Allan deviation for the current axis
        taus, adevs, _, _ = allantools.adev(data[axis], rate=1.0, data_type="freq")

        # Get random walk segment and bias instability point
        randomWalkSegment = getRandomWalkSegment(taus, adevs)
        biasInstabilityPoint = getBiasInstabilityPoint(taus, adevs)

        # Plot results for the current axis
        plt.figure(figsize=(12,8))
        ax = plt.gca()
        ax.set_yscale('log')
        ax.set_xscale('log')

        plt.plot(taus, adevs)
        plt.plot([randomWalkSegment[0], randomWalkSegment[2]],
                 [randomWalkSegment[1], randomWalkSegment[3]], 'k--')
        plt.plot(1, randomWalkSegment[1], 'rx', markeredgewidth=2.5, markersize=14.0)
        plt.plot(biasInstabilityPoint[0], biasInstabilityPoint[1], 'ro')

        plt.grid(True, which="both")
        plt.title(f'Allan Deviation (Axis {axis + 1})')
        plt.xlabel('Tau (s)')
        plt.ylabel('ADEV')

        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                     ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(20)

        plt.show()

if __name__ == '__main__':
    main(sys.argv)
