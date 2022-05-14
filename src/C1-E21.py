import pandas as pd
import matplotlib.pyplot as plt
import random

from schema import *
from tools import progressbar


def coin_toss(heads_probability):
    # Throw exception if an invalid probability for the toss is provided
    if heads_probability < 0 or heads_probability > 1:
        raise Exception("Invalid probability value (must be between 0 and 1)")

    # Create a random probability value to compare with the head's probability
    randomProbability = random.uniform(0, 1)

    # Compare with the provided probability to simulate a toss
    if(randomProbability <= heads_probability):
        return P_HEADS_COLUMN_NAME
    else:
        return P_TAILS_COLUMN_NAME


def simulate_tosses(sample_size, heads_probability):
    # toss a coin sample_size times and save the count obtained for each coin side in a dictionary, for each size
    results = []
    for current_sample_size in progressbar(range(1, sample_size + 1), "Simulating tosses: ", bar_size=40):
        results_for_size = {
            SAMPLE_SIZE_COLUMN_NAME: current_sample_size,
            HEADS_PROBABILITY_COLUMN_NAME: heads_probability,
            C_HEADS_COLUMN_NAME: 0,
            C_TAILS_COLUMN_NAME: 0,
            P_HEADS_COLUMN_NAME: 0,
            P_TAILS_COLUMN_NAME: 0,
        }
        for y in range(1, current_sample_size + 1):
            toss_result = coin_toss(heads_probability)
            if(toss_result == P_HEADS_COLUMN_NAME):
                results_for_size[C_HEADS_COLUMN_NAME] += 1
            else:
                results_for_size[C_TAILS_COLUMN_NAME] += 1

        # Calculate the probability using the count and store it in the proper column
        results_for_size[P_HEADS_COLUMN_NAME] = results_for_size[C_HEADS_COLUMN_NAME] / \
            current_sample_size
        results_for_size[P_TAILS_COLUMN_NAME] = results_for_size[C_TAILS_COLUMN_NAME] / \
            current_sample_size

        # append the results for this sample size to the list of all results
        results.append(results_for_size)

    # return as a dataframe for easier plotting
    return pd.DataFrame(results)


def plot(data_frame):
    # Construct and plot the chart
    ax = data_frame.plot(x=SAMPLE_SIZE_COLUMN_NAME,
                         y=[P_HEADS_COLUMN_NAME],
                         ylim=(0, 1),
                         lw=1,
                         title=f"Evolution of {P_HEADS_COLUMN_NAME} with increase in sample size")

    ax.axhline(y=data_frame[HEADS_PROBABILITY_COLUMN_NAME].values[0], xmin=0, xmax=data_frame[SAMPLE_SIZE_COLUMN_NAME].values[0],
               color='r', linestyle='--', lw=2, label=f"{P_HEADS_COLUMN_NAME}={data_frame[HEADS_PROBABILITY_COLUMN_NAME].values[0]}")

    plt.legend()
    plt.show()


# ---------------------------------------------------------------------
# Simulate the tosses with the values suggested by the author
def run(sample_size=5000, heads_probability=0.3):
    tosses = simulate_tosses(sample_size, heads_probability)
    print(tosses)

    plot(tosses)


run()
# ---------------------------------------------------------------------
