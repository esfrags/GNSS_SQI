def route_signal_strength(all_signal_quality_data, all_route_analysis, threshold=5):
    import matplotlib.pyplot as plt
    import numpy as np


    # Merge all latitudes, longitudes, and signal quality values
    latitudes = []
    longitudes = []
    signal_quality = []

    for route_analysis, signal_quality_data in zip(all_route_analysis, all_signal_quality_data):
        latitudes.extend(route_analysis.get('latitudes', []))
        longitudes.extend(route_analysis.get('longitudes', []))
        signal_quality.extend(signal_quality_data)

    if not (latitudes and longitudes and signal_quality):
        print("Insufficient data for heatmap.")
        return

    # Create a grid for the heatmap
    heatmap, xedges, yedges = np.histogram2d(
        longitudes, latitudes, bins=50, weights=signal_quality
    )

    # Mask bins with no data (zeros)
    heatmap_masked = np.ma.masked_where(heatmap == 0, heatmap)

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))

    # Create the heatmap (only route will be visible)
    cax = ax.imshow(
        heatmap_masked.T,
        origin='lower',
        cmap='hot',
        interpolation='nearest',
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]]
    )

    # Add color bar
    fig.colorbar(cax, ax=ax, label='Signal Quality')

    # Set labels
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('GPS Signal Quality Heatmap (Route Only)')

    plt.show()