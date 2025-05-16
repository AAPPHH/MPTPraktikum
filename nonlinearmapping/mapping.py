import numpy as np
import sys
from matplotlib import pyplot as plt

N = 4096
mu = 0.5
std = 0.03


def f(x):
    x = np.power(x, 0.8)
    # x = 3*x**2 - 2*x**3
    # x = 0.5 + 0.5 * np.sin(8.0 * np.pi * x)
    # x = 3*x**2 - 2*x**3

    # x = 3*x**2 - 2*x**3
    # x = 3*x**2 - 2*x**3
    return x


def grad_f(x):
    return (f(x + 0.01) - f(x)) / 0.01


fig, axs = plt.subplots(2, 2)


def draw():
    # Create normal distributed values
    x = np.clip(np.random.normal(mu, std, (N,)), 0, 1)

    # Map them through the non-linearity
    y = f(x)

    # Output Histogram
    axs[0, 0].hist(y, 32, orientation="horizontal", density=True)
    axs[0, 0].set_box_aspect(4.0)
    axs[0, 0].set_ylim(-0.1, 1.1)

    # Mapping Function
    x1 = np.linspace(0.0, 1.0, 256)
    y1 = f(x1)
    axs[0, 1].plot(x1, y1)

    # Tangent
    m = grad_f(mu)
    b = f(mu) - m * mu
    y2 = m * x1 + b
    axs[0, 1].plot(x1, y2)

    # Calculate estimate mu/std of mapped function
    mu_estimated = m * mu + b
    std_estimted = std * np.abs(m)
    y = np.exp(-((x1 - mu_estimated) ** 2) / (2 * std_estimted**2)) / (
        std_estimted * np.sqrt(2 * np.pi)
    )
    axs[0, 0].plot(y, x1)

    # Boundaries
    axs[0, 1].plot([mu - 3 * std, mu - 3 * std], [0, 1], "k--")
    axs[0, 1].plot([mu + 3 * std, mu + 3 * std], [0, 1], "k--")

    axs[0, 1].set_xlim(-0.1, 1.1)
    axs[0, 1].set_ylim(-0.1, 1.1)
    axs[1, 0].set_axis_off()

    # Input Histogram
    axs[1, 1].hist(x, 32, density=True)
    axs[1, 1].set_box_aspect(0.25)
    axs[1, 1].set_xlim(-0.1, 1.1)

    y = np.exp(-((x1 - mu) ** 2) / (2 * std**2)) / (std * np.sqrt(2 * np.pi))
    axs[1, 1].plot(x1, y)


def on_press(event):
    global mu, std
    print("press", event.key)
    sys.stdout.flush()

    if event.key == "+":
        mu = np.clip(mu + 0.02, 0.0, 1.0)

    if event.key == "-":
        mu = np.clip(mu - 0.02, 0.0, 1.0)

    if event.key == "*":
        std = np.clip(std * 1.08, 0.0, 1.0)

    if event.key == "/":
        std = np.clip(std / 1.08, 0.0, 1.0)

    axs[0, 0].clear()
    axs[0, 1].clear()
    axs[1, 0].clear()
    axs[1, 1].clear()
    draw()
    fig.canvas.draw()


draw()
fig.canvas.mpl_connect("key_press_event", on_press)
plt.show()

# def plot_function(image, col):
#     W, H = image.shape[1], image.shape[0]

#     x0, y0 = None, None
#     for x1 in np.linspace(0.0, 1.0, W // 10):
#         y1 = 1.0 - f(x1)

#         if x0 is not None:
#             cv2.line(image, (int(x0 * W), int(y0 * H)), (int(x1 * W), int(y1 * H)), col, 1)

#         x0, y0 = x1, y1

# image = np.zeros((512, 512, 3))

# C = 48
# plot_function(image[C:-C, C:-C], (0.8, 0.5, 0.1))
# cv2.imshow("Mapping", image)
# cv2.waitKey(0)
