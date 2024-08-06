import streamlit as st
import numpy as np
import altair as alt
from pandas import DataFrame


def task2():
    st.title("Task 2 - Projectile Apogee")

    launch_angle = np.radians(
        st.slider("Launch angle(°):", 0, 90, 20, key="launch_angle_task2")
    )
    launch_speed = st.slider("Launch speed(m/s):", 0, 90, 10, key="launch_speed_task2")
    launch_height = st.slider("Launch height(m):", 0, 20, 2, key="launch_height_task2")
    gravity = 9.81

    launch_range = (launch_speed**2 / gravity) * (
        np.sin(launch_angle) * np.cos(launch_angle)
        + np.cos(launch_angle)
        * (
            (
                np.sin(launch_angle) ** 2
                + (2 * gravity * launch_height) / launch_speed**2
            )
            ** 0.5
        )
    )

    apogee = [
        (launch_speed**2 / gravity) * np.sin(launch_angle) * np.cos(launch_angle),
        (
            launch_height
            + ((launch_speed**2 / (2 * gravity) * (np.sin(launch_angle) ** 2)))
        ),
    ]

    x_coords2 = np.linspace(0, launch_range, 51)
    y_coords2 = (
        launch_height
        + x_coords2 * np.tan(launch_angle)
        - (
            gravity
            / (2 * launch_speed**2)
            * (1 + np.tan(launch_angle) ** 2)
            * x_coords2**2
        )
    )

    source2 = DataFrame({"x(m)": x_coords2, "y(m)": y_coords2})

    trajectory = (
        alt.Chart(source2)
        .mark_line()
        .encode(
            x="x(m)",
            y=alt.Y(
                "y(m)",
                scale=alt.Scale(
                    domain=(-0.1, (max(source2["y(m)"] * 1.1))), clamp=True
                ),
            ),
        )
        .properties(title="Task 2 - Projectile Apogee")
        .interactive()
    )

    apogee_mark = (
        alt.Chart(DataFrame({"x(m)": [apogee[0]], "y(m)": [apogee[1]]}))
        .mark_point(shape="cross", size=100, color="red")
        .encode(
            x="x(m)",
            y=alt.Y(
                "y(m)",
                scale=alt.Scale(
                    domain=(-0.1, (max(source2["y(m)"] * 1.1))), clamp=True
                ),
            ),
        )
        .interactive()
    )

    chart2 = apogee_mark + trajectory

    st.altair_chart(chart2, use_container_width=True)
