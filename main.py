import streamlit as st

from pages.task1 import task1
from pages.task2 import task2
from pages.task3 import task3
from pages.task4 import task4
from pages.task5 import task5
from pages.task6 import task6
from pages.task7 import task7
from pages.task8 import task8
from pages.task9 import task9

pages = {
    "Task 1": task1,
    "Task 2": task2,
    "Task 3": task3,
    "Task 4": task4,
    "Task 5": task5,
    "Task 6": task6,
    "Task 7": task7,
    "Task 8": task8,
    "Task 9": task9,
}

st.sidebar.title("BPho Computational Challenge")
selection = st.sidebar.radio("Go to", list(pages.keys()))

pages[selection]()
