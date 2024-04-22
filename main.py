import streamlit as st
import plotly.graph_objects as go


def cohen_sutherland(x_min, y_min, x_max, y_max, x1, y1, x2, y2):
    INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8

    def compute_code(x, y):
        code = INSIDE
        if x < x_min:
            code |= LEFT
        elif x > x_max:
            code |= RIGHT
        if y < y_min:
            code |= BOTTOM
        elif y > y_max:
            code |= TOP
        return code

    code1, code2 = compute_code(x1, y1), compute_code(x2, y2)

    while (code1 | code2) != 0:
        if (code1 & code2) != 0:
            return None, None

        x, y = 0, 0

        if code1 != 0:
            code_out = code1
        else:
            code_out = code2

        if code_out & TOP:
            x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
            y = y_max
        elif code_out & BOTTOM:
            x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
            y = y_min
        elif code_out & RIGHT:
            y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
            x = x_max
        elif code_out & LEFT:
            y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
            x = x_min

        if code_out == code1:
            x1, y1 = x, y
            code1 = compute_code(x1, y1)
        else:
            x2, y2 = x, y
            code2 = compute_code(x2, y2)

    return (x1, y1), (x2, y2)


def clip_polygon(x_min, y_min, x_max, y_max, polygon_points):
    clipped_polygon = []

    for i in range(len(polygon_points)):
        x1, y1 = polygon_points[i]
        x2, y2 = polygon_points[(i + 1) % len(polygon_points)]

        intersection1, intersection2 = cohen_sutherland(x_min, y_min, x_max, y_max, x1, y1, x2, y2)

        if intersection1 and intersection2:
            clipped_polygon.extend([intersection1, intersection2])

    return clipped_polygon


def plot_line_segment(x_min, y_min, x_max, y_max, x1, y1, x2, y2, is_polygon=False, polygon_points=None):
    st.sidebar.markdown("### Input Data")
    x_min = st.sidebar.number_input("Minimum x-coordinate of the window:", value=-10)
    y_min = st.sidebar.number_input("Minimum y-coordinate of the window:", value=-10)
    x_max = st.sidebar.number_input("Maximum x-coordinate of the window:", value=10)
    y_max = st.sidebar.number_input("Maximum y-coordinate of the window:", value=10)

    st.sidebar.markdown("### Input Type")
    input_type = st.sidebar.radio("Choose input type:", ["Line Segment", "Polygon"])

    if input_type == "Line Segment":
        x1 = st.sidebar.number_input("x1:", value=-5)
        y1 = st.sidebar.number_input("y1:", value=-5)
        x2 = st.sidebar.number_input("x2:", value=5)
        y2 = st.sidebar.number_input("y2:", value=5)
    else:
        num_points = st.sidebar.number_input("Number of polygon points:", value=3, min_value=3, max_value=10)
        polygon_points = []
        for i in range(num_points):
            x = st.sidebar.number_input(f"x{i + 1}:", value=i)
            y = st.sidebar.number_input(f"y{i + 1}:", value=i)
            polygon_points.append((x, y))

    st.sidebar.markdown("### Algorithm Demonstration")
    st.sidebar.markdown("Choose an action:")
    action = st.sidebar.radio("", ["Show Result", "Clear Result"])

    if action == "Show Result":
        st.sidebar.success("Result displayed on the chart.")
    elif action == "Clear Result":
        st.sidebar.warning("Result cleared.")
        return

    fig = go.Figure()

    if input_type == "Line Segment":
        fig.add_trace(go.Scatter(x=[x1, x2], y=[y1, y2], line=dict(dash="dash"), name="Original Line Segment"))
        intersection1, intersection2 = cohen_sutherland(x_min, y_min, x_max, y_max, x1, y1, x2, y2)

        if intersection1 and intersection2:
            fig.add_trace(go.Scatter(x=[intersection1[0], intersection2[0]], y=[intersection1[1], intersection2[1]],
                                     line=dict(dash="solid"), name="Line Segment Inside Window"))
    else:
        fig.add_trace(go.Scatter(x=[point[0] for point in polygon_points + [polygon_points[0]]],
                                 y=[point[1] for point in polygon_points + [polygon_points[0]]],
                                 line=dict(dash="dash"), name="Original Polygon"))

        clipped_polygon = clip_polygon(x_min, y_min, x_max, y_max, polygon_points)

        if clipped_polygon:
            fig.add_trace(go.Scatter(x=[point[0] for point in clipped_polygon],
                                     y=[point[1] for point in clipped_polygon],
                                     line=dict(dash="solid"), fill="toself", name="Polygon Inside Window"))

    fig.add_shape(
        type="rect",
        x0=x_min,
        y0=y_min,
        x1=x_max,
        y1=y_max,
        line=dict(color="red", width=2),
        fillcolor="rgba(0,0,0,0)"
    )

    fig.update_layout(
        xaxis=dict(range=[x_min - 2, x_max + 2]),
        yaxis=dict(range=[y_min - 2, y_max + 2]),
        showlegend=False
    )

    st.plotly_chart(fig)


st.title("Cohen-Sutherland Algorithm Demonstration")

plot_line_segment(-10, -10, 10, 10, -5, -5, 5, 5, is_polygon=True)
