import streamlit as st
import altair as alt
import numpy as np
from math import sqrt, sin, cos, tan, asin, radians, degrees, log
from scipy.integrate import quad
from pandas import DataFrame


def task6():
    st.title("Task 6 - Distance Traveled")

    def original_line(launch_speed, gravity, launch_angle, launch_height):
        launch_range = (launch_speed**2 / gravity) * (
            sin(launch_angle) * cos(launch_angle)
            + cos(launch_angle)
            * sqrt(
                sin(launch_angle) ** 2 + (2 * gravity * launch_height) / launch_speed**2
            )
        )
        x_coords = np.linspace(0, launch_range, 51)
        y_coords = (
            launch_height
            + x_coords * (np.tan(launch_angle))
            - (
                gravity
                / (2 * launch_speed**2)
                * (1 + np.tan(launch_angle) ** 2)
                * x_coords**2
            )
        )

        return (x_coords, y_coords)

    def maximised_lin(launch_speed, gravity, launch_height):
        max_angle = asin(
            1 / (sqrt(2 + (2 * gravity * launch_height / launch_speed**2)))
        )
        launch_range = (launch_speed**2 / gravity) * sqrt(
            1 + (2 * gravity * launch_height / launch_speed**2)
        )

        x_coords = np.linspace(0, launch_range, 51)
        y_coords = (
            launch_height
            + x_coords * (np.tan(max_angle))
            - (
                gravity
                / (2 * launch_speed**2)
                * (1 + np.tan(max_angle) ** 2)
                * x_coords**2
            )
        )

        return (x_coords, y_coords, max_angle)

    def integrand(x, tan_theta, tan_theta_squared, gravity, launch_speed):
        return sqrt(
            1
            + (tan_theta - (gravity * x / launch_speed**2) * (1 + tan_theta_squared))
            ** 2
        )

    def general_dist(launch_speed, gravity, launch_angle, x):
        tan_theta = tan(launch_angle)
        tan_theta_squared = tan_theta**2

        integral = quad(
            integrand, 0, x, args=(tan_theta, tan_theta_squared, gravity, launch_speed)
        )[0]

        return integral

    launch_angle = radians(
        st.slider("Launch angle(°):", 0, 90, 60, key="launch_angle_task6")
    )
    launch_speed = st.slider("Launch speed(m/s):", 0, 90, 10, key="launch_speed_task6")
    launch_height = st.slider("Launch height(m):", 0, 20, 2, key="launch_height_task6")
    gravity = 9.81

    orig_x_coords, orig_y_coords = original_line(
        launch_speed, gravity, launch_angle, launch_height
    )
    max_x_coords, max_y_coords, max_angle = maximised_lin(
        launch_speed, gravity, launch_height
    )

    max_orig_x = orig_x_coords[-1]
    orig_distance = general_dist(launch_speed, gravity, launch_angle, max_orig_x)

    max_max_x = max_x_coords[-1]
    max_distance = general_dist(launch_speed, gravity, max_angle, max_max_x)

    source6_orig = DataFrame(
        {
            "x": orig_x_coords,
            "y": orig_y_coords,
            "Trajectory": f"θ = {np.around(degrees(launch_angle), 1)}° Dist = {round(orig_distance, 2)}m",
        }
    )

    source6_max = DataFrame(
        {
            "x": max_x_coords,
            "y": max_y_coords,
            "Trajectory": f"Max θ = {np.around(degrees(max_angle), 1)}° Dist = {round(max_distance, 2)}m",
        }
    )

    chart6A = (
        alt.Chart(source6_orig)
        .mark_line()
        .encode(
            x=alt.X("x", title="x(m)"),
            y=alt.Y("y", title="y(m)"),
            color="Trajectory:N",
        )
        .properties(title="Task 6 - Distance Traveled")
        .interactive()
    )

    chart6B = (
        alt.Chart(source6_max)
        .mark_line()
        .encode(
            x=alt.X("x", title="x(m)"),
            y=alt.Y("y", title="y(m)"),
            color=alt.Color("Trajectory:N"),
        )
        .interactive()
    )

    chart6 = chart6A + chart6B

    st.altair_chart(chart6, use_container_width=True)
