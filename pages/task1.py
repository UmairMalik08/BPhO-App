import streamlit as st
import numpy as np
import altair as alt
from math import sin, cos, radians
from pandas import DataFrame


def task1():
    st.title("Task 1 - Projectile Motion Model")

    def calculate_parabola(
        int_height, int_velocity, launch_angle, gravity, time_step=0.01
    ):
        x, y = [], []
        iteration_number = 0
        x_base = int_velocity * cos(launch_angle)
        y_base = int_height
        sin_angle = int_velocity * sin(launch_angle)

        while True:
            time = time_step * iteration_number
            current_x = x_base * time
            current_y = y_base + (sin_angle * time) - (0.5 * gravity * time**2)

            if current_y < -0.05:
                break

            x.append(current_x)
            y.append(current_y)
            iteration_number += 1

        return x, y

    launch_angle = radians(
        st.slider("Launch angle(°):", 0, 90, 20, key="launch_angle_task1")
    )
    launch_speed = st.slider("Launch speed(m/s):", 0, 90, 10, key="launch_speed_task1")
    launch_height = st.slider("Launch height(m):", 0, 20, 2, key="launch_height_task1")
    gravity = 9.81

    x_coords1, y_coords1 = calculate_parabola(
        launch_height, launch_speed, launch_angle, gravity
    )

    source1 = DataFrame({"x(m)": x_coords1, "y(m)": y_coords1})

    chart1 = (
        alt.Chart(source1)
        .mark_line()
        .encode(
            x=alt.X(
                "x(m)",
                scale=alt.Scale(domain=(0, (max(source1["x(m)"] * 1.1))), clamp=True),
            ),
            y=alt.Y(
                "y(m)",
                scale=alt.Scale(
                    domain=(-0.1, (max(source1["y(m)"] * 1.1))), clamp=True
                ),
            ),
        )
        .properties(title="Task 1 - Projectile Motion Model")
        .interactive()
    )

    st.altair_chart(chart1, use_container_width=True)
