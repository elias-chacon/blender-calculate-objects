# Object Sum Tool for Blender

## Objective
The **Object Sum Tool** is a powerful and intuitive addon for Blender users who need to quickly and efficiently calculate the sum of dimensions or areas for multiple objects in a scene based on a common name prefix. This addon eliminates the need for manual calculations, making it especially useful for artists working with large projects that involve complex object arrangements.

## Necessity
In Blender, when working with a large number of objects that share common naming conventions, it can be difficult and time-consuming to calculate the combined dimensions or areas. The Object Sum Tool automates this process, saving you time and effort. Whether you're working with architectural models, product design, or any other type of scene that involves repetitive object structures, this tool will help you gather important information quickly and accurately.

## Functionality
The **Object Sum Tool** allows you to:

- **Sum Dimensions**: Calculate the total sum of an object's dimension (X, Y, or Z) for all selected objects with a shared prefix.
- **Calculate Areas**: Compute the total area (XY, XZ, or YZ) or even the volume (XYZ) for the selected objects.
- **History Tracking**: Keep track of all your previous calculations in a history log, making it easy to review past results.
- **Export to CSV**: Export your results and the dimensions of each object in a CSV format for further analysis or record-keeping.
- **Flexible Number Formatting**: Toggle between dot or comma for decimal formatting to match your region's preferences.

### How it works:
1. **Prefix Selection**: You can input a prefix to filter objects that match this naming convention.
2. **Choose Calculation Type**: Select whether you want to sum the dimensions (X, Y, Z) or calculate areas/volume (XY, XZ, YZ, XYZ).
3. **Calculation**: The addon will gather all visible objects matching the prefix and compute the requested sum or area.
4. **History**: The result of each calculation is logged in the history section for quick reference.
5. **Export**: You can export the results into a CSV file, which includes the object names and their individual dimensions.

## Features:
- Automatically filters objects by their name prefix.
- Supports calculation of X, Y, Z dimensions, as well as area and volume.
- History management for easy access to previous calculations.
- CSV export for easy data sharing or record-keeping.
- Comma vs. dot decimal separator to match user preferences.

## Installation
1. Download the latest version of the addon.
2. In Blender, go to `Edit > Preferences > Add-ons > Install`.
3. Locate the downloaded `.zip` file and click **Install Addon**.
4. Enable the addon by checking the checkbox next to "Object Sum Tool."

## Usage
1. Open the **Object Sum Tool** panel in the **3D View** under the **Tools** tab.
2. Enter a prefix for the objects you wish to calculate.
3. Choose the type of calculation you want (X, Y, Z, or area/volume).
4. Click the **Calculate** button to perform the sum.
5. Review the result in the **History** section.
6. Optionally, export the results to a CSV file using the **Export to CSV** button.

## Contributing
Feel free to fork the repository, submit issues, or open pull requests. Contributions are welcome!

## License
This addon is released under the [MIT License](LICENSE).
