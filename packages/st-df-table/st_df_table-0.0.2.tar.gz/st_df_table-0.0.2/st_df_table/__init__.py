import os

import pandas as pd
import streamlit.components.v1 as components

_RELEASE = True

if os.getenv("_ST_TABLE_NOT_RELEASE_"):
    _RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "st_table",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_table", path=build_dir)


def st_table(
    df: pd.DataFrame,
    head_align: str = "center",
    data_align: str = "left",
    head_bg_color: str = "white",
    data_bg_color: str = "white",
    head_color: str = "black",
    data_color: str = "black",
    head_font_weight: str = "bold",
    data_font_weight: str = "normal",
    bordered: bool = True,
    border_color: str = "black",
    border_width: int = 1,
    table_width: int = None,
    sortable: bool = True,
    key=None,
):
    """Displays Pandas DataFrame

    Parameters
    ----------
    df: pd.DataFrame
    head_align: str - aligning table header, values are: "center", "left", "right"
    data_align: str - align table data, values are: "center", "left", "right"
    head_bg_color: str - table header background color
    data_bg_color: str - table data background color
    head_color: str - table header text color
    data_color: str - table data text color
    head_font_weight: str - table header font weight
    data_font_weight: str - table data font weight
    bordered: bool - table bordered
    border_color: str - table border color
    border_width: int - table border width in pixels
    table_width: int - table width in pixels
    sortable: bool - table columns sortable
    key: str
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    None

    """
    columns = [{"dataField": col, "text": col, "sort": sortable} for col in df.columns]
    data = df.reset_index().to_dict(orient="records")
    _component_func(
        key=key,
        columns=columns,
        data=data,
        head_align=head_align,
        data_align=data_align,
        head_bg_color=head_bg_color,
        data_bg_color=data_bg_color,
        head_color=head_color,
        data_color=data_color,
        head_font_weight=head_font_weight,
        data_font_weight=data_font_weight,
        bordered=bordered,
        border_color=border_color,
        border_width=border_width,
        table_width=table_width,
    )
