# Cohen-Sutherland Algorithm Demonstration

This project demonstrates the Cohen-Sutherland algorithm for line segment clipping and polygon clipping. The algorithm is used to determine the portion of a line segment or a polygon that lies inside a given rectangular window.

## Algorithm Overview

The Cohen-Sutherland algorithm works by dividing the 2D coordinate space into nine regions based on the rectangular window boundaries. Each point of the line segment or polygon is assigned a code based on its position relative to the window. These codes are used to determine the intersection points with the window boundaries.

## Usage

You can test this application [here](https://cohen-sutherland-algorithm.streamlit.app)

To use the application, follow these steps:

1. Specify the coordinates of the rectangular window in the sidebar. The minimum and maximum x and y coordinates can be adjusted using the input fields.

2. Choose the input type between "Line Segment" and "Polygon" in the sidebar.

   - For a line segment, specify the coordinates of the two endpoints (x1, y1) and (x2, y2) in the sidebar.

   - For a polygon, specify the number of points and their coordinates (x, y) in the sidebar.

3. Click on "Show Result" in the sidebar to display the result on the graph.

   - The original line segment or polygon will be shown as a dashed line.

   - If the line segment or polygon intersects with the window, the portion inside the window will be shown as a solid line or filled polygon.

   - The rectangular window will be displayed as a red rectangle.

4. To clear the result and start over, click on "Clear Result" in the sidebar.

Feel free to adjust the input parameters and explore different scenarios using the Cohen-Sutherland algorithm!

## Implementation Details

The project is implemented using the Streamlit library for the user interface and the Plotly library for data visualization. The Cohen-Sutherland algorithm is implemented in the `cohen_sutherland` and `clip_polygon` functions.

The `plot_line_segment` function handles the user input and displays the line segment or polygon, along with the result of the clipping process, on the graph.

---

*Note: This project is for educational purposes and serves as a demonstration of the Cohen-Sutherland algorithm. It may not cover all edge cases or optimizations that can be applied in a real-world implementation.*