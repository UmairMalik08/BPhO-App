import streamlit as st
import altair as alt
import numpy as np
from math import sqrt, sin, cos, asin, isclose, radians
from pandas import DataFrame


def task7():
    st.title("Task 7 - Min-max points")

    launch_angles = st.text_input(
        "Launch angle(°):", "30, 45, 60, 70.53, 78, 85", key="launch_angles_task7"
    )
    launch_angles = list(launch_angles.split(", "))
    launch_angles_degrees = [float(angle) for angle in launch_angles]
    launch_angles_radians = [radians(float(angle)) for angle in launch_angles]

    launch_speed = st.slider("Launch speed(m/s):", 0, 90, 10, key="launch_speed_task7")
    launch_height = st.slider("Launch height(m):", 0, 20, 2, key="launch_height_task7")
    gravity = 9.81

    time = list(np.linspace(0, 2.5, 100))

    data_lines_range, data_lines_y, data_points_range, data_points_y = [], [], [], []

    for angle_deg, angle_rad in zip(launch_angles_degrees, launch_angles_radians):
        turning_points, x_list, y_list = [], [], []

        r = [
            sqrt(
                (launch_speed**2 * t**2)
                - (gravity * t**3 * launch_speed * sin(angle_rad))
                + (0.25 * gravity**2 * t**4)
            )
            for t in time
        ]

        if angle_rad >= asin(2 / 3 * sqrt(2)):
            turning_points.append(
                ((3 * launch_speed) / (2 * gravity))
                * (sin(angle_rad) + sqrt(sin(angle_rad) ** 2 - (8 / 9)))
            )
            turning_points.append(
                ((3 * launch_speed) / (2 * gravity))
                * (sin(angle_rad) - sqrt(sin(angle_rad) ** 2 - (8 / 9)))
            )
            if isclose(turning_points[0], turning_points[1], abs_tol=0.05):
                turning_points.pop(1)

        x_list = [launch_speed * t * cos(angle_rad) for t in time]
        y_list = [
            launch_speed * t * sin(angle_rad) - (0.5 * gravity * t**2) for t in time
        ]

        for t, r_value in zip(time, r):
            data_lines_range.append(
                {"time(s)": t, "range(m)": r_value, "Angle": f"{angle_deg}°"}
            )

        for point in turning_points:
            index = sqrt(
                (launch_speed**2 * point**2)
                - (gravity * point**3 * launch_speed * sin(angle_rad))
                + (0.25 * gravity**2 * point**4)
            )
            data_points_range.append(
                {
                    "time(s)": point,
                    "range(m)": index,
                }
            )

        for x, y in zip(x_list, y_list):
            data_lines_y.append({"x(m)": x, "y(m)": y, "Angle": f"{angle_deg}°"})

        for point in turning_points:
            x_point = launch_speed * point * cos(angle_rad)
            y_point = launch_speed * point * sin(angle_rad) - (0.5 * gravity * point**2)

            data_points_y.append(
                {
                    "x(m)": x_point,
                    "y(m)": y_point,
                }
            )

    source7A = DataFrame(data_lines_range)
    source7B = DataFrame(data_points_range)

    source7C = DataFrame(data_lines_y)
    source7D = DataFrame(data_points_y)

    chart7A = (
        alt.Chart(source7A)
        .mark_line()
        .encode(
            x=alt.X(
                "time(s)",
                scale=alt.Scale(domain=(0, 2.5), clamp=True),
            ),
            y="range(m)",
            color="Angle",
        )
        .properties(title="Task 7 - Min-max points")
        .interactive()
    )

    chart7B = (
        alt.Chart(source7B)
        .mark_point(shape="cross", size=100, color="red")
        .encode(
            x=alt.X(
                "time(s)",
                scale=alt.Scale(domain=(0, 2.5), clamp=True),
            ),
            y="range(m)",
        )
        .interactive()
    )

    chart7C = (
        alt.Chart(source7C)
        .transform_filter((alt.datum["y(m)"] >= -5) & (alt.datum["y(m)"] <= 5))
        .mark_line()
        .encode(
            x="x(m)",
            y="y(m)",
            color="Angle",
        )
        .interactive()
    )

    chart7D = (
        alt.Chart(source7D)
        .mark_point(shape="cross", size=100, color="red")
        .encode(
            x="x(m)",
            y="y(m)",
        )
        .interactive()
    )

    chart7I = chart7A + chart7B
    chart7II = chart7C + chart7D

    st.altair_chart(chart7I, use_container_width=True)
    st.altair_chart(chart7II, use_container_width=True)
