import streamlit as st
from st_img_selector import st_img_selector

from PIL import Image
import numpy as np

selected_indices = st_img_selector(
    images=[
        "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg",
        "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg",
        "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg",
    ],
    corner_radius=10,
    selection_color="#FF0000",
    img_per_row=3,
    border_thickness=4,
    max_row_height=200,
    value=[]
)

st.write("Selected image indices:", selected_indices)
