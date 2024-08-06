import streamlit as st
import altair as alt
import numpy as np
from math import sin, cos, radians
from pandas import DataFrame


def task8():
    st.title("Task 8 - Projectile Bounce")

    def verlet_trajectory_solver(
        max_bounce_number,
        coefficient_of_restitution,
        gravity,
        time_step,
        launch_height,
        launch_angle,
        launch_speed,
    ):
        vy_initial = launch_speed * sin(launch_angle)
        vx_initial = launch_speed * cos(launch_angle)

        estimated_steps = 1000

        time_list = np.zeros(estimated_steps)
        x_list = np.zeros(estimated_steps)
        y_list = np.zeros(estimated_steps)
        vy_list = np.zeros(estimated_steps)
        vx_list = np.zeros(estimated_steps)

        x_list[0] = 0
        y_list[0] = launch_height
        vy_list[0] = vy_initial
        vx_list[0] = vx_initial

        nBounce = 0
        n = 0

        while nBounce <= max_bounce_number:
            if n + 1 >= len(time_list):
                time_list = np.resize(time_list, len(time_list) * 2)
                x_list = np.resize(x_list, len(x_list) * 2)
                y_list = np.resize(y_list, len(y_list) * 2)
                vy_list = np.resize(vy_list, len(vy_list) * 2)
                vx_list = np.resize(vx_list, len(vx_list) * 2)

            x_list[n + 1] = x_list[n] + vx_list[n] * time_step
            y_list[n + 1] = (
                y_list[n] + vy_list[n] * time_step - 0.5 * gravity * time_step**2
            )

            vx_list[n + 1] = vx_list[n]
            vy_list[n + 1] = vy_list[n] - gravity * time_step

            time_list[n + 1] = time_list[n] + time_step

            if y_list[n + 1] < 0:
                y_list[n + 1] = 0
                vy_list[n + 1] = -coefficient_of_restitution * vy_list[n + 1]
                nBounce += 1

            n += 1

        time_list = time_list[: n + 1]
        x_list = x_list[: n + 1]
        y_list = y_list[: n + 1]
        vy_list = vy_list[: n + 1]
        vx_list = vx_list[: n + 1]

        return (time_list, x_list, y_list)

    max_bounce_number = 6

    col1, col2 = st.columns(2)

    with col1:
        launch_angle = radians(
            st.slider("Launch angle(°):", 0, 90, 60, key="launch_angle_task8")
        )
        launch_speed = st.slider(
            "Launch speed(m/s):", 0, 90, 5, key="launch_speed_task8"
        )

    with col2:
        launch_height = st.slider(
            "Launch height(m):", 0, 20, 10, key="launch_height_task8"
        )
        coefficient_of_restitution = st.slider(
            "Coefficient of restitution:",
            0.0,
            1.0,
            0.7,
            key="coefficient_of_restitution_task8",
        )
    max_bounce_number = 6

    gravity = 9.81
    time_step = 0.05

    t, x, y = verlet_trajectory_solver(
        max_bounce_number,
        coefficient_of_restitution,
        gravity,
        time_step,
        launch_height,
        launch_angle,
        launch_speed,
    )

    source8 = DataFrame({"x(m)": x, "y(m)": y})

    chart8 = (
        alt.Chart(source8)
        .mark_line()
        .encode(
            x="x(m)",
            y=alt.Y(
                "y(m)",
                scale=alt.Scale(
                    domain=(-0.1, (max(source8["y(m)"] * 1.1))), clamp=True
                ),
            ),
        )
        .properties(title="Task 8 - Projectile Bounce")
        .interactive()
    )

    st.altair_chart(chart8, use_container_width=True)
