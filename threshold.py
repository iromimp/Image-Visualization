"""
"""

import os
import plotly.graph_objects as go
import dash
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc, dash_table
from dash_slicer import VolumeSlicer
from dash.dependencies import Input, Output, State
import tkinter
from tkinter import filedialog as fd
import variables


app = dash.Dash(__name__, update_title=None, external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)
server = app.server
FILE_DIR = 'D:/data/'

app.layout = html.Div(

    children=[

        dbc.Navbar(
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div(
                                        [
                                            html.H3("Bone Metastasis Segmentation",
                                                    style={'color': 'White', 'align': 'Left'}),

                                        ],
                                        id="app-title",
                                    ),

                                ],
                                md=True,
                                align="left",
                            ),
                        ],
                        align="left",
                    ),
                ],
                fluid=True,
            ),
            dark=True,
            color="dark",
            sticky="top",
        ),
        # Upload files
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div([
                        html.H5('Patient File:',
                                style={'width': '20%', 'display': 'inline-block', 'text-align': 'left'}),
                        html.Div(id='selected_directory',
                                 style={'width': '30%', 'display': 'none'}),
                        html.Div(id='selected_file', children='No file selected!',
                                 style={'width': '30%', 'display': 'inline-block'}),
                        dbc.Button('Upload Patient File', id='open_excel_button', n_clicks=0)
                    ]),

                    html.Br(),
                ]
            ),
        ),
        # Graph bar to display all the axes
        dbc.Card(

            dbc.CardBody(

                [
                    html.Div([
                        html.H5('Select the Segmentation Method',
                                style={'width': '100%', 'display': 'inline-block', 'text-align': 'center'}),
                        dbc.Button('Fixed Threshold', id='open_threshold', outline=True, color="primary",
                                   className="me-1", n_clicks=0),
                        dbc.Button('K-means', id='open_k_means', outline=True, color="secondary", className="me-1",
                                   n_clicks=0),
                        dbc.Button('Deep Learning', id='open_deep_learn', outline=True, color="success",
                                   className="me-1", n_clicks=0)
                    ]),

                    html.Hr(),

                    html.Div(id='images'
                             ),
                    html.Div(
                        [
                            dbc.Label("SUV Threshold", width=4),
                            dcc.Slider(
                                id="suv-slider", min=0, max=50, step=0.5, value=2.5,
                                tooltip={"placement": "bottom", "always_visible": True}
                            ),
                        ]
                    ),

                ],
            ),

        ),

        html.Br(),

    ],
)

"""
Function to upload and update mat files
"""


# 1. Callback for open_excel button
@app.callback(
    Output(component_id='selected_file', component_property='children'),
    Output(component_id='selected_directory', component_property='children'),
    Input(component_id='open_excel_button', component_property='n_clicks'),
    prevent_initial_call=True
)
def open_excel_function(open_excel):
    print('*** 1A. Callback open_file_dialog')
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    print("***", trigger, "is triggered.")

    if trigger == 'open_excel_button':
        root = tkinter.Tk()
        root.withdraw()
        # root.iconbitmap(default='Extras/transparent.ico')

        file_directory = tkinter.filedialog.askopenfilename(initialdir=FILE_DIR)
        file_name = os.path.basename(file_directory)
        ('***', file_directory)
        ct_img, ct_pt_bone_mask, voxel_volume = variables.image_variables(file_directory)

        root.destroy()  # <--- SOLUTION
    else:
        file_name = None

    return file_name, file_directory


@app.callback(
    Output('images', 'children'),
    Input('open_threshold', 'n_clicks'),
    State('selected_directory', 'children'),
)
def create_volume_slicer(n_clicks, path):
    ct_img, ct_pt_bone_mask = variables.image_variables(path)
    # Create slicer objects
    slicer0 = VolumeSlicer(app, ct_img, axis=0, color="#00ff99", scene_id="ct_bone")
    slicer1 = VolumeSlicer(app, ct_img, axis=1, color="#00ff99", scene_id="ct_bone")
    slicer2 = VolumeSlicer(app, ct_img, axis=2, color="#00ff99", scene_id="ct_bone")
    print(type(slicer0))
    return (
        html.Div(
            dbc.Row(
                [
                    dcc.Store(id={"context": "app", "scene": slicer0.scene_id, "name": "setpos"}),

                    dbc.Col(
                        html.Div(
                            [
                                html.Center(html.H1("Transversal")),
                                slicer0.graph,
                                html.Br(),
                                slicer0.slider,
                                *slicer0.stores,
                                html.Div(
                                    [
                                        dbc.Label("Contrast Limit", width=6),
                                        dcc.RangeSlider(
                                            id="clim-slider0", min=ct_img.min(), max=ct_img.max(),
                                            value=(260, 1000),
                                            tooltip={"placement": "bottom", "always_visible": True}
                                        ),
                                    ]
                                ),

                                html.Div(id='slicer0_stats')
                            ]
                        ),

                    ),
                    dbc.Col(
                        html.Div(

                            [
                                html.Center(html.H1("Coronal")),
                                slicer1.graph,
                                html.Br(),
                                slicer1.slider,
                                *slicer1.stores,
                                html.Div(
                                    [
                                        dbc.Label("Contrast Limit", width=6),
                                        dcc.RangeSlider(
                                            id="clim-slider1", min=ct_img.min(), max=ct_img.max(),
                                            value=(260, 1000),
                                            tooltip={"placement": "bottom", "always_visible": True}
                                        ),
                                    ],
                                ),

                                html.Div(id='slicer1_stats'),
                            ],
                        ),
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Center(html.H1("Sagittal")),
                                slicer2.graph,
                                html.Br(),
                                slicer2.slider,
                                *slicer2.stores,
                                html.Div(
                                    [
                                        dbc.Label("Contrast Limit", width=6),
                                        dcc.RangeSlider(
                                            id="clim-slider2", min=ct_img.min(), max=ct_img.max(),
                                            value=(260, 1000),
                                            tooltip={"placement": "bottom", "always_visible": True}
                                        ),
                                    ]
                                ),

                                html.Div(id='slicer2_stats')
                            ]
                        ),
                    ),

                ],
                style={"display": "grid", "gridTemplateColumns": "33% 33% 33%"}
            ),

        )
    )


if __name__ == "__main__":
    # Note: dev_tools_props_check negatively affects the performance of VolumeSlicer
    app.run_server(debug=True, dev_tools_props_check=False)
