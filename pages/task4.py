import streamlit as st
import altair as alt
import numpy as np
from math import sqrt, sin, cos, tan, asin, radians, degrees
from pandas import DataFrame


def task4():
    st.title("Task 4 - Maximising Distance")

    def original_line(initial_velocity, gravity, launch_angle, height):
        launch_range = (initial_velocity**2 / gravity) * (
            sin(launch_angle) * cos(launch_angle)
            + cos(launch_angle)
            * sqrt(
                sin(launch_angle) ** 2 + (2 * gravity * height) / initial_velocity**2
            )
        )
        time_taken = launch_range / (initial_velocity * cos(launch_angle))

        x_coords = np.linspace(0, launch_range, 51)
        y_coords = (
            height
            + x_coords * np.tan(launch_angle)
            - (
                gravity
                / (2 * initial_velocity**2)
                * (1 + np.tan(launch_angle) ** 2)
                * x_coords**2
            )
        )

        return (x_coords, y_coords, time_taken)

    def maximised_lin(initial_velocity, gravity, height):
        max_angle = asin(1 / (sqrt(2 + (2 * gravity * height / initial_velocity**2))))
        launch_range = (initial_velocity**2 / gravity) * sqrt(
            1 + (2 * gravity * height / initial_velocity**2)
        )
        time_taken = launch_range / (initial_velocity * cos(max_angle))

        x_coords = np.linspace(0, launch_range, 51)

        y_coords = (
            height
            + x_coords * tan(max_angle)
            - (
                gravity
                / (2 * initial_velocity**2)
                * (1 + tan(max_angle) ** 2)
                * x_coords**2
            )
        )

        return (x_coords, y_coords, max_angle, time_taken)

    launch_angle = radians(
        st.slider("Launch angle(°):", 0, 90, 60, key="launch_angle_task4")
    )
    launch_speed = st.slider("Launch speed(m/s):", 0, 90, 10, key="launch_speed_task4")
    launch_height = st.slider("Launch height(m):", 0, 20, 2, key="launch_height_task4")
    gravity = 9.81

    orig_x_coords, orig_y_coords, orig_time = original_line(
        launch_speed, gravity, launch_angle, launch_height
    )
    max_x_coords, max_y_coords, max_angle, max_time = maximised_lin(
        launch_speed, gravity, launch_height
    )

    source4_orig = DataFrame(
        {
            "x": orig_x_coords,
            "y": orig_y_coords,
            "Trajectory": f"θ = {np.around(degrees(launch_angle), 2)}° t={np.around(orig_time, 2)}s",
        }
    )

    source4_max = DataFrame(
        {
            "x": max_x_coords,
            "y": max_y_coords,
            "Trajectory": f"Max θ = {np.around(degrees(max_angle), 2)}° t={np.around(max_time, 2)}s",
        }
    )

    chart4A = (
        alt.Chart(source4_orig)
        .mark_line()
        .encode(
            x=alt.X("x", title="x(m)"),
            y=alt.Y("y", title="y(m)"),
            color=alt.Color("Trajectory:N"),
        )
        .properties(title="Task 4 - Maximising Distance")
        .interactive()
    )

    chart4B = (
        alt.Chart(source4_max)
        .mark_line()
        .encode(
            x=alt.X("x", title="x(m)"),
            y=alt.Y("y", title="y(m)"),
            color=alt.Color("Trajectory:N"),
        )
        .interactive()
    )

    chart4 = chart4A + chart4B

    st.altair_chart(chart4, use_container_width=True)
