import streamlit as st
import altair as alt
import numpy as np
from math import sqrt, sin, cos, radians
from pandas import DataFrame, concat


def task9():
    st.title("Task 9 - Air resistance model")

    def verlet_trajectory_solver(
        gravity,
        time_step,
        launch_height,
        launch_angle,
        launch_speed,
        air_resistance_factor,
    ):
        estimated_steps = 1000

        time_list = np.zeros(estimated_steps)
        x_list = np.zeros(estimated_steps)
        y_list = np.zeros(estimated_steps)
        hypotenuse_velocity_list = np.zeros(estimated_steps)
        vy_list = np.zeros(estimated_steps)
        vx_list = np.zeros(estimated_steps)

        x_list[0] = 0
        y_list[0] = launch_height
        hypotenuse_velocity_list[0] = launch_speed
        vy_list[0] = launch_speed * sin(launch_angle)
        vx_list[0] = launch_speed * cos(launch_angle)

        half_time_step_squared = 0.5 * time_step**2
        n = 0
        non_negative = True

        while non_negative:
            vx_n = vx_list[n]
            vy_n = vy_list[n]
            hypotenuse_velocity_n = hypotenuse_velocity_list[n]

            hypotenuse_velocity_squared = hypotenuse_velocity_n**2
            x_acceleration = (
                -(vx_n / hypotenuse_velocity_n)
                * air_resistance_factor
                * hypotenuse_velocity_squared
            )
            y_acceleration = (
                -gravity
                - (vy_n / hypotenuse_velocity_n)
                * air_resistance_factor
                * hypotenuse_velocity_squared
            )

            x_list[n + 1] = (
                x_list[n] + vx_n * time_step + x_acceleration * half_time_step_squared
            )
            y_list[n + 1] = (
                y_list[n] + vy_n * time_step + y_acceleration * half_time_step_squared
            )

            vx_next = vx_n + x_acceleration * time_step
            vy_next = vy_n + y_acceleration * time_step
            vx_list[n + 1] = vx_next
            vy_list[n + 1] = vy_next

            hypotenuse_velocity_list[n + 1] = sqrt(vx_next**2 + vy_next**2)

            time_list[n + 1] = time_list[n] + time_step

            if y_list[n + 1] < 0:
                non_negative = False

            n += 1

            if n + 1 >= estimated_steps:
                time_list = np.resize(time_list, len(time_list) * 2)
                x_list = np.resize(x_list, len(x_list) * 2)
                y_list = np.resize(y_list, len(y_list) * 2)
                hypotenuse_velocity_list = np.resize(
                    hypotenuse_velocity_list, len(hypotenuse_velocity_list) * 2
                )
                vy_list = np.resize(vy_list, len(vy_list) * 2)
                vx_list = np.resize(vx_list, len(vx_list) * 2)

        time_list = time_list[: n + 1]
        x_list = x_list[: n + 1]
        y_list = y_list[: n + 1]
        vx_list = vx_list[: n + 1]
        vy_list = vy_list[: n + 1]

        return (
            time_list,
            x_list,
            y_list,
            vx_list,
            vy_list,
        )

    col1, col2 = st.columns(2)

    with col1:
        launch_speed = st.slider(
            "Launch speed(m/s):", 0, 90, 20, key="launch_speed_task9"
        )
        launch_height = st.slider(
            "Launch height(m):", 0, 20, 2, key="launch_height_task9"
        )
        launch_angle = radians(
            st.slider("Launch angle(°):", 0, 90, 30, key="launch_angle_task9")
        )
        object_mass = st.slider(
            "Object mass(kg):", 0.0, 10.0, 0.1, key="object_mass_task9"
        )

    with col2:
        drag_coefficient = st.slider(
            "Drag coefficient:", 0.0, 2.0, 1.0, key="drag_coefficient_task9"
        )
        cross_sectional_area = st.slider(
            "Cross-sectional area(m^2):",
            0.0,
            10.0,
            0.0079,
            key="cross_sectional_area_task9",
        )
        air_density = st.slider(
            "Air density(kgm^-3):", 0, 10, 1, key="air_density_task9"
        )

    gravity = 9.81
    time_step = 0.01
    air_resistance_factor = (drag_coefficient * air_density * cross_sectional_area) / (
        2 * object_mass
    )

    t, x, y, vx, vy = verlet_trajectory_solver(
        gravity, time_step, launch_height, launch_angle, launch_speed, 0
    )

    (
        t_air_resistance,
        x_air_resistance,
        y_air_resistance,
        vx_air_resistance,
        vy_air_resistance,
    ) = verlet_trajectory_solver(
        gravity,
        time_step,
        launch_height,
        launch_angle,
        launch_speed,
        air_resistance_factor,
    )

    source9A = DataFrame(
        {"x(m)": x, "y(m)": y, "Trajectory": ["No air resistance"] * len(x)}
    )
    source9B = DataFrame(
        {
            "x(m)": x_air_resistance,
            "y(m)": y_air_resistance,
            "Trajectory": ["Air resistance"] * len(x_air_resistance),
        }
    )

    source9I = concat([source9A, source9B])

    chart9I = (
        alt.Chart(source9I)
        .mark_line()
        .encode(
            x="x(m)",
            y=alt.Y(
                "y(m)",
                scale=alt.Scale(
                    domain=(-0.1, (max(source9I["y(m)"] * 1.1))), clamp=True
                ),
            ),
            color="Trajectory:N",
        )
        .properties(title="Task 9 - Air resistance model")
        .interactive()
    )

    source9AII = DataFrame(
        {"time(s)": t, "vx(m/s)": vx, "Trajectory": ["No air resistance"] * len(t)}
    )
    source9BII = DataFrame(
        {
            "time(s)": t_air_resistance,
            "vx(m/s)": vx_air_resistance,
            "Trajectory": ["Air resistance"] * len(t_air_resistance),
        }
    )
    source9II = concat([source9AII, source9BII])

    chart9II = (
        alt.Chart(source9II)
        .mark_line()
        .encode(
            x="time(s)",
            y=alt.Y(
                "vx(m/s)",
                scale=alt.Scale(
                    domain=(-0.1, (max(source9II["vx(m/s)"] * 1.1))), clamp=True
                ),
            ),
            color="Trajectory:N",
        )
        .properties(title="Task 9 - Air resistance model")
        .interactive()
    )

    st.altair_chart(chart9I, use_container_width=True)
    st.altair_chart(chart9II, use_container_width=True)
