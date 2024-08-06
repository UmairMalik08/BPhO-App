import streamlit as st
import altair as alt
import numpy as np
from math import log10, ceil, floor
from pandas import DataFrame, concat


def task3():
    st.title("Task 3 - Projectile to hit point")

    def round_up(num):
        if num == 0:
            return 0
        order_of_magnitude = floor(log10(abs(num)))
        factor = 10 ** (2 - order_of_magnitude - 1)
        return ceil(num * factor) / factor

    def low_ball(a, b, c, launch_speed, height, target_x, gravity):
        low_ball_radians = np.arctan(np.min(np.roots([a, b, c])))
        x_coords = np.linspace(0, target_x, 101)
        y_coords = (
            height
            + x_coords * np.tan(low_ball_radians)
            - (
                gravity
                / (2 * launch_speed**2)
                * (1 + np.tan(low_ball_radians) ** 2)
                * x_coords**2
            )
        )

        return x_coords, y_coords

    def high_ball(a, b, c, launch_speed, height, target_x, gravity):
        high_ball_radians = np.arctan(np.max(np.roots([a, b, c])))
        x_coords = np.linspace(0, target_x, 101)
        y_coords = (
            height
            + x_coords * np.tan(high_ball_radians)
            - (
                (gravity / (2 * launch_speed**2))
                * ((1 + np.tan(high_ball_radians) ** 2) * x_coords**2)
            )
        )

        return x_coords, y_coords

    def min_ball(minimum_initial_velocity, height, target_x, target_y, gravity):
        minimum_speed_radians = np.arctan(
            (target_y + np.sqrt(target_x**2 + target_y**2)) / target_x
        )
        x_coords = np.linspace(0, target_x, 101)
        y_coords = (
            height
            + x_coords * np.tan(minimum_speed_radians)
            - (
                (gravity / (2 * minimum_initial_velocity**2))
                * ((1 + np.tan(minimum_speed_radians) ** 2) * x_coords**2)
            )
        )

        return x_coords, y_coords

    col1, col2 = st.columns(2)

    gravity = 9.81

    with col1:
        target_x = st.number_input("Target x(m):", value=1000, key="target_x_task3")
        target_y = st.number_input("Target y(m):", value=200, key="target_y_task3")

    minimum_initial_velocity = int(
        np.sqrt(gravity) * np.sqrt(target_y + np.sqrt(target_x**2 + target_y**2))
    )

    with col2:
        launch_height = st.slider(
            "Launch height(m):", 0, 20, 0, key="launch_height_task3"
        )
        launch_speed = st.slider(
            "Launch speed(m/s):",
            min_value=int(round_up(minimum_initial_velocity)),
            max_value=int(round_up(minimum_initial_velocity * 5)),
            value=int(round_up(minimum_initial_velocity) * 1.5),
            key="launch_speed_task3",
        )

    a = (gravity / (2 * launch_speed**2)) * target_x**2
    b = -target_x
    c = target_y - launch_height + (gravity * target_x**2) / (2 * launch_speed**2)

    low_x, low_y = low_ball(a, b, c, launch_speed, launch_height, target_x, gravity)
    high_x, high_y = high_ball(a, b, c, launch_speed, launch_height, target_x, gravity)
    min_x, min_y = min_ball(
        minimum_initial_velocity, launch_height, target_x, target_y, gravity
    )

    source3A = DataFrame({"x(m)": low_x, "y(m)": low_y, "Trajectory": "Low Ball"})
    source3B = DataFrame({"x(m)": high_x, "y(m)": high_y, "Trajectory": "High Ball"})
    source3C = DataFrame({"x(m)": min_x, "y(m)": min_y, "Trajectory": "Min Ball"})

    source3 = concat([source3A, source3B, source3C])

    chart = (
        alt.Chart(source3)
        .mark_line()
        .encode(x="x(m)", y="y(m)", color=alt.Color("Trajectory:N"))
        .properties(title="Task 3 - Projectile to hit point")
        .interactive()
    )

    focus_point = (
        alt.Chart(DataFrame({"x(m)": [target_x], "y(m)": [target_y]}))
        .mark_point(shape="cross", size=100, color="red")
        .encode(x="x(m)", y="y(m)")
        .interactive()
    )

    chart3 = chart + focus_point

    st.altair_chart(chart3, use_container_width=True)
