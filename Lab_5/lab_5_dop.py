import dash
from dash import dcc, html, Input, Output, State
import numpy as np
import plotly.graph_objs as go

# INITIAL PARAMETERS
# Harmonic signal parameters
AMP_INIT = 1.0       # Initial amplitude
FREQ_INIT = 1.0      # Initial frequency in Hz
PHASE_INIT = 0.5     # Initial phase (radians)

# Noise parameters
NOISE_MEAN_INIT = 0.0    # Initial noise mean
NOISE_STD_INIT = 0.1     # Initial noise standard deviation

# Filter parameter for our custom moving average filter (window size)
FILTER_WINDOW_INIT = 5   # Initial window size (should be an odd positive integer)

# Time vector for signal generation
TIME = np.linspace(0, 10, 1000)

# Global noise vector. This vector is updated only when noise parameters change.
global_noise = np.random.normal(NOISE_MEAN_INIT, NOISE_STD_INIT, size=TIME.shape)

# CUSTOM FILTER FUNCTION
def moving_average_filter(signal_array, window_size):
    window_size = int(window_size)
    kernel = np.ones(window_size) / window_size
    filtered = np.convolve(signal_array, kernel, mode='same')
    return filtered


# SIGNAL GENERATION FUNCTION
def generate_harmonic_signal(time, amplitude, frequency, phase, add_noise):
    pure_signal = amplitude * np.sin(2 * np.pi * frequency * time + phase)
    if add_noise:
        return pure_signal + global_noise
    return pure_signal


# DASH APP LAYOUT
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Interactive Signal Processing Demo", style={'textAlign':'center'}),

    html.Div([
        dcc.Graph(id='raw-signal-graph', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='filtered-signal-graph', style={'width': '48%', 'display': 'inline-block'})
    ]),
    
    html.Br(),
    
    # Row of sliders for harmonic signal parameters
    html.Div([
        html.Div([
            html.Label("Amplitude (A)"),
            dcc.Slider(
                id='amp-slider',
                min=0.1,
                max=10,
                step=0.1,
                value=AMP_INIT,
                marks={0.1:'0.1', 5:'5', 10:'10'},
                tooltip={"always_visible": False, "placement": "bottom"}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '0 10px'}),
        html.Div([
            html.Label("Frequency (Hz)"),
            dcc.Slider(
                id='freq-slider',
                min=0.1,
                max=10,
                step=0.1,
                value=FREQ_INIT,
                marks={0.1:'0.1', 5:'5', 10:'10'},
                tooltip={"always_visible": False, "placement": "bottom"}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '0 10px'}),
        html.Div([
            html.Label("Phase (radians)"),
            dcc.Slider(
                id='phase-slider',
                min=0,
                max=2*np.pi,
                step=0.1,
                value=PHASE_INIT,
                marks={0:'0', 3.14:'π', 6.28:'2π'},
                tooltip={"always_visible": False, "placement": "bottom"}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '0 10px'})
    ]),
    
    html.Br(),
    
    # Row: Sliders for noise parameters and checklist for noise toggle
    html.Div([
        html.Div([
            html.Label("Noise Mean"),
            dcc.Slider(
                id='noise-mean-slider',
                min=-1.0,
                max=1.0,
                step=0.1,
                value=NOISE_MEAN_INIT,
                marks={-1.0:'-1', 0:'0', 1.0:'1'},
                tooltip={"always_visible": False, "placement": "bottom"}
            )
        ], style={'width': '45%', 'display': 'inline-block', 'padding': '0 10px'}),
        html.Div([
            html.Label("Noise Std Dev"),
            dcc.Slider(
                id='noise-std-slider',
                min=0.0,
                max=1.0,
                step=0.05,
                value=NOISE_STD_INIT,
                marks={0.0:'0', 0.5:'0.5', 1.0:'1'},
                tooltip={"always_visible": False, "placement": "bottom"}
            )
        ], style={'width': '45%', 'display': 'inline-block', 'padding': '0 10px'}),
        html.Div([
            dcc.Checklist(
                id='show-noise-checklist',
                options=[{'label': 'Show Noise', 'value': 'SHOW'}],
                value=['SHOW']
            )
        ], style={'width': '10%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingTop': '25px'})
    ]),
    
    html.Br(),
    
    # Row: Drop-down for filter type and slider for filter window size
    html.Div([
        html.Div([
            html.Label("Filter Type"),
            dcc.Dropdown(
                id='filter-dropdown',
                options=[{'label': 'Moving Average Filter', 'value': 'MA'}],
                value='MA',
                clearable=False
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '0 10px'}),
        html.Div([
            html.Label("Filter Window Size"),
            dcc.Slider(
                id='filter-window-slider',
                min=1,
                max=51,
                step=2,  # Use only odd numbers for symmetry
                value=FILTER_WINDOW_INIT,
                marks={1:'1', 11:'11', 21:'21', 31:'31', 41:'41', 51:'51'},
                tooltip={"always_visible": False, "placement": "bottom"}
            )
        ], style={'width': '60%', 'display': 'inline-block', 'padding': '0 10px'})
    ]),
    
    html.Br(),
    
    # Reset button
    html.Button('Reset', id='reset-button', n_clicks=0, style={'fontSize': 18})
])


# CALLBACK: Update Graphs
@app.callback(
    [Output('raw-signal-graph', 'figure'),
     Output('filtered-signal-graph', 'figure')],
    [Input('amp-slider', 'value'),
     Input('freq-slider', 'value'),
     Input('phase-slider', 'value'),
     Input('noise-mean-slider', 'value'),
     Input('noise-std-slider', 'value'),
     Input('show-noise-checklist', 'value'),
     Input('filter-dropdown', 'value'),
     Input('filter-window-slider', 'value'),
     Input('reset-button', 'n_clicks')]
)
def update_graphs(amplitude, frequency, phase, noise_mean, noise_std, show_noise_list, filter_type, filter_window, n_clicks):
    # If 'SHOW' is in the checklist, display noise.
    display_noise = 'SHOW' in show_noise_list

    # Update global noise vector based on noise parameters.
    global global_noise
    global_noise = np.random.normal(noise_mean, noise_std, size=TIME.shape)
    
    # Generate raw harmonic signal.
    raw_signal = generate_harmonic_signal(TIME, amplitude, frequency, phase, display_noise)
    
    # Apply selected filter (here, only Moving Average Filter is available)
    if filter_type == 'MA':
        filtered_signal = moving_average_filter(raw_signal, filter_window)
    else:
        filtered_signal = raw_signal  # Fallback (should not happen)
    
    # Build Plotly figures
    raw_fig = {
        'data': [go.Scatter(x=TIME, y=raw_signal, mode='lines', line=dict(color='dodgerblue'))],
        'layout': go.Layout(
            title='Raw Harmonic Signal (Noisy or Clean)',
            xaxis={'title': 'Time'},
            yaxis={'title': 'Amplitude'},
            template='plotly_white'
        )
    }
    filt_fig = {
        'data': [go.Scatter(x=TIME, y=filtered_signal, mode='lines', line=dict(color='darkorange'))],
        'layout': go.Layout(
            title='Filtered Signal (Moving Average Filter)',
            xaxis={'title': 'Time'},
            yaxis={'title': 'Amplitude'},
            template='plotly_white'
        )
    }
    return raw_fig, filt_fig

# CALLBACK: Reset Controls
@app.callback(
    [Output('amp-slider', 'value'),
     Output('freq-slider', 'value'),
     Output('phase-slider', 'value'),
     Output('noise-mean-slider', 'value'),
     Output('noise-std-slider', 'value'),
     Output('filter-window-slider', 'value'),
     Output('show-noise-checklist', 'value')],
    [Input('reset-button', 'n_clicks')]
)
def reset_controls(n_clicks):
    if n_clicks > 0:
        return AMP_INIT, FREQ_INIT, PHASE_INIT, NOISE_MEAN_INIT, NOISE_STD_INIT, FILTER_WINDOW_INIT, ['SHOW']
    raise dash.exceptions.PreventUpdate

# RUN THE APP
if __name__ == '__main__':
    app.run(debug=True)
