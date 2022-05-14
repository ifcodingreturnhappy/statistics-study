import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from schema import *
from tools import progressbar

np.random.seed(0)


def create_samples(sample_sizes: list, amount_of_repetitions: int, heads_probability: float):
    # Initialize the output variable
    output = []

    # Loop all the provided sample sizes
    for size in sample_sizes:
        # Initialize a variable that will keep the count of heads (X for the given problem)
        results_for_size = {
            SAMPLE_SIZE_COLUMN_NAME: size,
            REPETITIONS_PERFORMED_COLUMN_NAME: amount_of_repetitions,
            HEADS_PROBABILITY_COLUMN_NAME: heads_probability,
            HEADS_COUNT_COLUMN_NAME: np.empty(amount_of_repetitions),
        }

        # Do the exeperiment N times (so that we can average out the results later)
        for i in progressbar(range(amount_of_repetitions), f"Simulating tosses ({SAMPLE_SIZE_COLUMN_NAME}={size}): ", bar_size=40):

            # Create a sample with the size provided using a uniform probability distribution
            # See https://www.geeksforgeeks.org/numpy-random-uniform-in-python/
            x = np.where(np.random.uniform(
                low=0, high=1, size=size) < heads_probability, 1, 0)

            # Add the current sample to the count variable
            results_for_size[HEADS_COUNT_COLUMN_NAME][i] = np.sum(x)

        # Append the count variable to the result
        output.append(results_for_size)

    return pd.DataFrame(output)


def plot_samples(data_frame):
    # Initialize figure
    plt.figure(figsize=(14, 10))

    # NOTE: Looping through a dataframe is slow, but since is only for showcase purposes and is not production code, I will allow it.
    data_frame = data_frame.reset_index()
    for index, row in data_frame.iterrows():
        # Create one subplot per row, one for each row in the dataframe provided
        ax = plt.subplot(data_frame.shape[0], 1, index+1)

        # The histogram with the counts of heads
        ax.hist(row[HEADS_COUNT_COLUMN_NAME], density=True, bins=120,
                label='X', color='C0')

        # An auxiliar vertical line with the average of the counts
        ax.vlines(row[HEADS_COUNT_COLUMN_NAME].mean(),
                  ymin=0,
                  ymax=get_y_max(index),
                  label=f"Average of {HEADS_COUNT_COLUMN_NAME}", color='C1')

        # An auxiliar vertical line with the expected value for the average (see the framing of the exercise)
        ax.vlines(row[HEADS_PROBABILITY_COLUMN_NAME] * row[SAMPLE_SIZE_COLUMN_NAME],
                  ymin=0,
                  ymax=get_y_max(index),
                  label=f"{SAMPLE_SIZE_COLUMN_NAME} × {HEADS_PROBABILITY_COLUMN_NAME}", color='C2')

        # Legend and title to help interpret the chart
        ax.legend(loc='upper right')
        ax.set_title(f'n = {row[SAMPLE_SIZE_COLUMN_NAME]}')

    plt.show()


def get_y_max(iteration):
    # returns a properr y max value for this specific exercise
    ymax = 5 / (pow(10, iteration))
    return ymax


# ---------------------------------------------------------------------
# Run the experiment with the values suggested by the author
def run(sample_sizes=[10, 100, 1000],
        amount_of_repetitions=50000,
        heads_probability=0.3):

    results = create_samples(sample_sizes,
                             amount_of_repetitions,
                             heads_probability)

    print(results)

    plot_samples(results)


run()
# ---------------------------------------------------------------------
