def create_heatmap(processed_data):
    import matplotlib.pyplot as plt
    import numpy as np

    # Assuming processed_data is a dictionary with latitude, longitude, and signal quality
    latitudes = processed_data['latitudes']
    longitudes = processed_data['longitudes']
    signal_quality = processed_data['signal_quality']

    # Create a grid for the heatmap
    heatmap, xedges, yedges = np.histogram2d(longitudes, latitudes, bins=50, weights=signal_quality)

    # Create the figure and axis
    fig, ax = plt.subplots()

    # Create the heatmap
    cax = ax.imshow(heatmap.T, origin='lower', cmap='hot', interpolation='nearest', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])

    # Add color bar
    fig.colorbar(cax)

    # Set labels
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('GPS Signal Quality Heatmap')

    # Show the plot
    plt.show()