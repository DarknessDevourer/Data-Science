import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy import signal


# INITIAL PARAMETER CONSTANTS
# Parameters for the harmonic signal:
AMP_INIT = 1.0              # Initial amplitude of the harmonic signal
FREQ_INIT = 1.0             # Initial frequency (Hz)
PHASE_INIT = 0.5            # Initial phase shift (radians)

# Parameters for the noise:
NOISE_MEAN_INIT = 0.0       # Initial mean value of the noise
NOISE_STD_INIT = 0.1        # Initial noise standard deviation 

# Parameter for the Gaussian filter 
GAUSS_SIGMA_INIT = 2.0      

# Time vector for signal generation:
TIME = np.linspace(0, 10, 1000)

# A global noise vector is generated only once.
# The noise is updated only when noise parameters change.
global_noise = np.random.normal(NOISE_MEAN_INIT, NOISE_STD_INIT, size=TIME.shape)

# FUNCTION: generate_signal
def generate_signal(time, amplitude, frequency, phase, add_noise):
    """
    Generates a harmonic signal (sine wave) and adds noise if requested.
    
    Parameters:
        time (array): Time vector.
        amplitude (float): Amplitude of the harmonic signal.
        frequency (float): Frequency of the harmonic signal.
        phase (float): Phase shift.
        add_noise (bool): If True, the global noise is added; if False, a clean signal is generated.
    
    Returns:
        array: Harmonic signal (with or without noise).
    """
    pure_signal = amplitude * np.sin(frequency * time + phase)
    if add_noise:
        return pure_signal + global_noise
    return pure_signal

# FUNCTION: apply_gaussian_filter
def apply_gaussian_filter(signal_array, sigma):
    """
    Applies a Gaussian filter to the input signal using convolution.
    
    Parameters:
        signal_array (array): Input signal.
        sigma (float): Standard deviation for the Gaussian window.
    
    Returns:
        array: Filtered signal.
    """
    window = signal.windows.gaussian(len(signal_array), sigma)
    filtered = signal.convolve(signal_array, window / window.sum(), mode='same')
    return filtered

# UPDATE FUNCTIONS
def update_plots(val):
    """
    Updates both plots (raw and filtered signal) when any slider or checkbox changes.
    
    This function is called when the user modifies any of the following:
    - Harmonic signal parameters: amplitude, frequency, phase
    - Noise display toggle (checkbox)
    - Gaussian filter parameter (sigma)
    """
    amplitude = amp_slider.val
    frequency = freq_slider.val
    phase = phase_slider.val
    # 'Show Noise' checkbox: True means noise will be displayed, False means a clean signal.
    display_noise = noise_check.get_status()[0]
    gauss_sigma = gauss_sigma_slider.val

    # Generate the raw harmonic signal (with noise added according to checkbox setting)
    raw_signal = generate_signal(TIME, amplitude, frequency, phase, display_noise)
    plot_raw.set_ydata(raw_signal)
    
    # Apply the Gaussian filter to the raw signal
    filtered_signal = apply_gaussian_filter(raw_signal, gauss_sigma)
    plot_filtered.set_ydata(filtered_signal)
    
    plt.draw()

def update_noise_parameters(val):
    """
    Updates the global noise vector when noise parameters are changed and refreshes the plots.
    
    This ensures that if the noise mean or standard deviation is changed,
    the noise is regenerated and the updated noise is used in the signal generation.
    """
    global global_noise
    noise_mean = noise_mean_slider.val
    noise_std = noise_std_slider.val
    global_noise = np.random.normal(noise_mean, noise_std, size=TIME.shape)
    update_plots(None)

def reset_all(event):
    """
    Resets all parameters (harmonic signal, noise, filter) to their initial default values.
    
    When the user clicks the 'Reset' button, all sliders return to their original values.
    """
    amp_slider.reset()
    freq_slider.reset()
    phase_slider.reset()
    noise_mean_slider.reset()
    noise_std_slider.reset()
    gauss_sigma_slider.reset()

# BUILD THE GRAPHICAL INTERFACE (PLOTS AND WIDGETS)
# Create a figure with two subplots:
# Top plot: shows the raw harmonic signal (with or without noise).
# Bottom plot: shows the filtered signal (using the Gaussian filter).
fig, (ax_raw, ax_filtered) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

# Increase the bottom margin to make room for sliders/controls.
plt.subplots_adjust(left=0.18, bottom=0.4, right=0.75, top=0.9, hspace=0.5)

# --- Top Plot: Raw Harmonic Signal ---
initial_raw_signal = generate_signal(TIME, AMP_INIT, FREQ_INIT, PHASE_INIT, True)
plot_raw, = ax_raw.plot(TIME, initial_raw_signal, color='dodgerblue', lw=2)
ax_raw.set_title('Harmonic Signal (Noisy or Clean)', fontsize=14, color='darkslateblue', pad=15)
ax_raw.set_ylabel('Amplitude', fontsize=12)
ax_raw.grid(True, linestyle='--', alpha=0.6)

# --- Bottom Plot: Filtered Signal (after applying Gaussian Filter) ---
initial_filtered = apply_gaussian_filter(initial_raw_signal, GAUSS_SIGMA_INIT)
plot_filtered, = ax_filtered.plot(TIME, initial_filtered, color='darkorange', lw=2)
ax_filtered.set_title('Filtered Signal (Gaussian Filter)', fontsize=14, color='darkred', pad=10)
ax_filtered.set_xlabel('Time', fontsize=12)
ax_filtered.set_ylabel('Amplitude', fontsize=12)
ax_filtered.grid(True, linestyle='--', alpha=0.6)

# WIDGETS FOR HARMONIC SIGNAL PARAMETERS
# Slider for Amplitude
ax_amp = plt.axes([0.16, 0.30, 0.65, 0.03], facecolor='lightsteelblue')
amp_slider = Slider(ax_amp, 'Amplitude (A)', 0.1, 10.0, valinit=AMP_INIT, color='cyan')
amp_slider.on_changed(update_plots)

# Slider for Frequency
ax_freq = plt.axes([0.16, 0.25, 0.65, 0.03], facecolor='lightsteelblue')
freq_slider = Slider(ax_freq, 'Frequency (ω)', 0.1, 10.0, valinit=FREQ_INIT, color='cyan')
freq_slider.on_changed(update_plots)

# Slider for Phase
ax_phase = plt.axes([0.16, 0.20, 0.65, 0.03], facecolor='lightsteelblue')
phase_slider = Slider(ax_phase, 'Phase (φ)', 0, 2 * np.pi, valinit=PHASE_INIT, color='cyan')
phase_slider.on_changed(update_plots)

# WIDGETS FOR NOISE PARAMETERS
# Slider for Noise Mean
ax_noise_mean = plt.axes([0.16, 0.15, 0.65, 0.03], facecolor='lightseagreen')
noise_mean_slider = Slider(ax_noise_mean, 'Noise Mean', -1.0, 1.0, valinit=NOISE_MEAN_INIT, color='lime')
noise_mean_slider.on_changed(update_noise_parameters)

# Slider for Noise Standard Deviation
ax_noise_std = plt.axes([0.16, 0.10, 0.65, 0.03], facecolor='lightseagreen')
noise_std_slider = Slider(ax_noise_std, 'Noise Std Dev', 0.0, 1.0, valinit=NOISE_STD_INIT, color='lime')
noise_std_slider.on_changed(update_noise_parameters)

# WIDGET FOR GAUSSIAN FILTER PARAMETER
# Slider for Gaussian σ value used in filtering
ax_gauss_sigma = plt.axes([0.16, 0.05, 0.65, 0.03], facecolor='lightsalmon')
gauss_sigma_slider = Slider(ax_gauss_sigma, 'Gaussian σ', 0, 10, valinit=GAUSS_SIGMA_INIT, color='orangered')
gauss_sigma_slider.on_changed(update_plots)

# WIDGET: Checkbox for Noise Toggle
# Checkbox to select whether to display noise on the harmonic signal.
ax_noise_checkbox = plt.axes([0.78, 0.70, 0.15, 0.1], facecolor='aliceblue')
noise_check = CheckButtons(ax_noise_checkbox, ['Show Noise'], [True])
noise_check.on_clicked(update_plots)

# WIDGET: Reset Button
# Button that resets all parameters to their initial values.
ax_reset = plt.axes([0.78, 0.63, 0.15, 0.05])
reset_button = Button(ax_reset, 'Reset', color='salmon')
reset_button.on_clicked(reset_all)


# USER INSTRUCTIONS (Console Output)
print("Instructions:")
print("-------------")
print("1. Use the 'Amplitude', 'Frequency', and 'Phase' sliders to adjust the harmonic signal.")
print("2. Use the 'Noise Mean' and 'Noise Std Dev' sliders to change the properties of the noise.")
print("   - The noise is regenerated only when these sliders are adjusted.")
print("3. Toggle the 'Show Noise' checkbox to display a noisy signal or a clean signal.")
print("4. The top plot shows the raw harmonic signal (with or without noise),")
print("   while the bottom plot shows the signal after applying a Gaussian filter.")
print("5. Use the 'Gaussian σ' slider to adjust the filter's standard deviation.")
print("6. Click the 'Reset' button to restore all parameters to their default values.")
print("-------------")
print("Enjoy experimenting with the interactive signal processing demo!")

plt.show()
