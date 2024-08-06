import streamlit as st
import altair as alt
import numpy as np
from math import log10, ceil, floor
from pandas import DataFrame


def task5():
    st.title("Task 5 - Bounding Parabola")

    def round_up(num):
        if num == 0:
            return 0
        order_of_magnitude = floor(log10(abs(num)))
        factor = 10 ** (2 - order_of_magnitude - 1)
        return ceil(num * factor) / factor

    def low_ball(a, b, c, launch_speed, height, gravity):
        low_ball_radians = np.atan(min(np.roots([a, b, c])))

        launch_range = (launch_speed**2 / gravity) * (
            np.sin(low_ball_radians) * np.cos(low_ball_radians)
            + np.cos(low_ball_radians)
            * np.sqrt(
                np.sin(low_ball_radians) ** 2 + (2 * gravity * height) / launch_speed**2
            )
        )
        x_coords = np.linspace(0, launch_range, 101)
        y_coords = (
            height
            + x_coords * (np.tan(low_ball_radians))
            - (
                (gravity / (2 * launch_speed**2))
                * ((1 + np.tan(low_ball_radians) ** 2) * x_coords**2)
            )
        )

        return (x_coords, y_coords)

    def high_ball(a, b, c, launch_speed, height, gravity):
        high_ball_radians = np.atan(max(np.roots([a, b, c])))

        launch_range = (launch_speed**2 / gravity) * (
            np.sin(high_ball_radians) * np.cos(high_ball_radians)
            + np.cos(high_ball_radians)
            * np.sqrt(
                np.sin(high_ball_radians) ** 2
                + (2 * gravity * height) / launch_speed**2
            )
        )
        x_coords = np.linspace(0, launch_range, 101)
        y_coords = (
            height
            + x_coords * (np.tan(high_ball_radians))
            - (
                (gravity / (2 * launch_speed**2))
                * ((1 + np.tan(high_ball_radians) ** 2) * x_coords**2)
            )
        )

        return (x_coords, y_coords)

    def min_ball(minimum_initial_velocity, height, target_x, target_y, gravity):
        minimum_speed_radians = np.atan(
            (target_y + np.sqrt(target_x**2 + target_y**2)) / target_x
        )

        launch_range = (minimum_initial_velocity**2 / gravity) * (
            np.sin(minimum_speed_radians) * np.cos(minimum_speed_radians)
            + np.cos(minimum_speed_radians)
            * np.sqrt(
                np.sin(minimum_speed_radians) ** 2
                + (2 * gravity * height) / minimum_initial_velocity**2
            )
        )
        x_coords = np.linspace(0, launch_range, 101)
        y_coords = (
            height
            + x_coords * (np.tan(minimum_speed_radians))
            - (
                (gravity / (2 * minimum_initial_velocity**2))
                * ((1 + np.tan(minimum_speed_radians) ** 2) * x_coords**2)
            )
        )

        return (x_coords, y_coords)

    def max_range(launch_speed, gravity, height):
        max_angle = np.asin(
            (np.sqrt(2 + (2 * gravity * height / launch_speed**2)) ** -1)
        )
        launch_range = (launch_speed**2 / gravity) * np.sqrt(
            1 + (2 * gravity * height / launch_speed**2)
        )
        time_taken = launch_range / (launch_speed * np.cos(max_angle))

        x_coords = np.linspace(0, launch_range, 51)
        y_coords = (
            height
            + x_coords * (np.tan(max_angle))
            - (
                gravity
                / (2 * launch_speed**2)
                * (1 + np.tan(max_angle) ** 2)
                * x_coords**2
            )
        )

        return (x_coords, y_coords, max_angle, time_taken, launch_range)

    def bounding(launch_speed, launch_height, gravity, launch_range):

        x_coords = np.linspace(0, launch_range, 101)
        y_coords = (
            (launch_speed**2 / (2 * gravity))
            - (gravity / (2 * launch_speed**2)) * x_coords**2
        ) + launch_height

        return (x_coords, y_coords)

    gravity = 9.81

    col1, col2 = st.columns(2)

    with col1:
        target_x = st.number_input("Target x(m):", value=1000, key="target_x_task5")
        target_y = st.number_input("Target y(m):", value=200, key="target_y_task5")

    minimum_initial_velocity = int(
        np.sqrt(gravity) * np.sqrt(target_y + np.sqrt(target_x**2 + target_y**2))
    )

    with col2:
        launch_height = st.slider(
            "Launch height(m):", 0, 20, 0, key="launch_height_task5"
        )
        launch_speed = st.slider(
            "Launch speed(m/s):",
            min_value=int(round_up(minimum_initial_velocity)),
            max_value=int(round_up(minimum_initial_velocity * 5)),
            value=150,  # int(round_up(minimum_initial_velocity) * 1.5),
            key="launch_speed_task5",
        )

    a = (gravity / (2 * launch_speed**2)) * target_x**2
    b = -target_x
    c = target_y - launch_height + (gravity * target_x**2) / (2 * launch_speed**2)

    max_x_coords, max_y_coords, max_angle, max_time, launch_range = max_range(
        launch_speed, gravity, launch_height
    )
    min_x, min_y = min_ball(
        minimum_initial_velocity, launch_height, target_x, target_y, gravity
    )
    high_x, high_y = high_ball(a, b, c, launch_speed, launch_height, gravity)
    low_x, low_y = low_ball(a, b, c, launch_speed, launch_height, gravity)
    bounding_x_coords, bounding_y_coords = bounding(
        launch_speed, launch_height, gravity, launch_range
    )

    source5_bounding = DataFrame(
        {
            "x": bounding_x_coords,
            "y": bounding_y_coords,
            "Trajectory": f"Bounding",
        }
    )

    source5_max = DataFrame(
        {
            "x": max_x_coords,
            "y": max_y_coords,
            "Trajectory": f"Max dist.",
        }
    )

    source5_high = DataFrame(
        {
            "x": high_x,
            "y": high_y,
            "Trajectory": f"High",
        }
    )

    source5_low = DataFrame(
        {
            "x": low_x,
            "y": low_y,
            "Trajectory": f"Low",
        }
    )

    source5_min = DataFrame(
        {
            "x": min_x,
            "y": min_y,
            "Trajectory": f"Min u",
        }
    )

    chart5A = (
        alt.Chart(source5_bounding)
        .mark_line()
        .encode(
            x=alt.X("x", title="x(m)"),
            y=alt.Y("y", title="y(m)"),
            color=alt.Color("Trajectory:N"),
        )
        .properties(title="Task 5 - Bounding Parabola")
        .interactive()
    )

    chart5A = (
        alt.Chart(source5_max)
        .mark_line()
        .encode(
            x=alt.X("x", title="x(m)"),
            y=alt.Y("y", title="y(m)"),
            color=alt.Color("Trajectory:N"),
        )
        .interactive()
    )

    chart5B = (
        alt.Chart(source5_high)
        .mark_line()
        .encode(
            x=alt.X("x", title="x(m)"),
            y=alt.Y("y", title="y(m)"),
            color=alt.Color("Trajectory:N"),
        )
        .interactive()
    )

    chart5C = (
        alt.Chart(source5_min)
        .mark_line()
        .encode(
            x=alt.X("x", title="x(m)"),
            y=alt.Y("y", title="y(m)"),
            color=alt.Color("Trajectory:N"),
        )
        .interactive()
    )

    chart5D = (
        alt.Chart(source5_low)
        .mark_line()
        .encode(
            x=alt.X("x", title="x(m)"),
            y=alt.Y("y", title="y(m)"),
            color=alt.Color("Trajectory:N"),
        )
        .interactive()
    )

    chart5E = (
        alt.Chart(source5_bounding)
        .mark_line(strokeDash=[8, 4])
        .encode(
            x=alt.X("x", title="x(m)"),
            y=alt.Y("y", title="y(m)"),
            color=alt.Color("Trajectory:N"),
        )
        .interactive()
    )

    chart5_focus_point = (
        alt.Chart(
            DataFrame(
                {"x(m)": [target_x], "y(m)": [target_y], "Trajectory": f"Focus Point"}
            )
        )
        .mark_point(shape="cross", size=100, color="red")
        .encode(x="x(m)", y="y(m)")
        .interactive()
    )

    chart5 = chart5A + chart5B + chart5C + chart5D + chart5E + chart5_focus_point

    st.altair_chart(chart5, use_container_width=True)
