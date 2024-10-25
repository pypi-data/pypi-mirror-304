import os
import streamlit as st
import streamlit.components.v1 as components
import base64
from PIL import Image
import numpy as np
import io

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "st_img_selector",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_img_selector", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def st_img_selector(
    images,
    value=[],
    corner_radius=10,
    selection_color="#555555",
    img_per_row=4,
    border_thickness=4,
    max_row_height=300,
    key=None,
):
    """Create a new instance of 'image_select' component."""
    # Process the images
    processed_images = []
    for img in images:
        if isinstance(img, str):
            if img.startswith("http://") or img.startswith("https://"):
                # It's a URL
                processed_images.append(img)
            else:
                # Assume it's a local file path
                with open(img, "rb") as f:
                    img_bytes = f.read()
                encoded = base64.b64encode(img_bytes).decode()
                data_uri = f"data:image/jpeg;base64,{encoded}"
                processed_images.append(data_uri)
        elif isinstance(img, Image.Image):
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            encoded = base64.b64encode(buffered.getvalue()).decode()
            data_uri = f"data:image/jpeg;base64,{encoded}"
            processed_images.append(data_uri)
        elif isinstance(img, np.ndarray):
            pil_img = Image.fromarray(img)
            buffered = io.BytesIO()
            pil_img.save(buffered, format="JPEG")
            encoded = base64.b64encode(buffered.getvalue()).decode()
            data_uri = f"data:image/jpeg;base64,{encoded}"
            processed_images.append(data_uri)
        else:
            raise ValueError("Unsupported image type")

    # Call the Streamlit component
    component_value = _component_func(
        images=processed_images,
        value=value,
        corner_radius=corner_radius,
        selection_color=selection_color,
        img_per_row=img_per_row,
        border_thickness=border_thickness,
        max_row_height=max_row_height,
        key=key,
        default=value,
    )

    return component_value