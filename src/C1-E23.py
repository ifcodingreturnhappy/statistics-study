import random
import pandas as pd
import matplotlib.pyplot as plt

from schema import *
from tools import progressbar


def fair_die_toss(die_size):
    # Throw exception if an invalid die size is provided
    if die_size <= 0:
        raise Exception("Invalid die size (must be greater than 0)")

    # Return a random face of the die
    return random.randint(1, die_size)


def is_toss_in_event_space(event_space, toss_result):
    # Checks if the face of the die belongs to the space of the event
    return toss_result in event_space


def simulate_tosses(sample_size, die_size, A_event_space, B_event_space, AB_event_space):
    # Initialize the output
    results = []

    # Run the simulation sample_size times
    for current_sample_size in progressbar(range(1, sample_size + 1), f"Simulating tosses: ", bar_size=40, delete_bar_on_complete=False):
        # Initialize the output for the current sample size
        toss_result = {
            SAMPLE_SIZE_COLUMN_NAME: current_sample_size,
            A_COUNT_COLUMN_NAME: 0,
            B_COUNT_COLUMN_NAME: 0,
            AB_COUNT_COLUMN_NAME: 0,
            A_PROBABILITY_COLUMN_NAME: 0,
            B_PROBABILITY_COLUMN_NAME: 0,
            AxB_PROBABILITY_COLUMN_NAME: 0,
            AB_PROBABILITY_COLUMN_NAME: 0
        }

        for i in range(current_sample_size):

            toss = fair_die_toss(die_size)

            # Check if A occured and increment the count if yes
            if(is_toss_in_event_space(A_event_space, toss)):
                toss_result[A_COUNT_COLUMN_NAME] += 1

            # Check if B occured and increment the count if yes
            if(is_toss_in_event_space(B_event_space, toss)):
                toss_result[B_COUNT_COLUMN_NAME] += 1

            # Check if AB occured and increment the count if yes
            if(is_toss_in_event_space(AB_event_space, toss)):
                toss_result[AB_COUNT_COLUMN_NAME] += 1

        # Calculate the probabilities for this sample size by doing count / current sample size
        toss_result[A_PROBABILITY_COLUMN_NAME] = toss_result[A_COUNT_COLUMN_NAME] / \
            current_sample_size
        toss_result[B_PROBABILITY_COLUMN_NAME] = toss_result[B_COUNT_COLUMN_NAME] / \
            current_sample_size
        toss_result[AxB_PROBABILITY_COLUMN_NAME] = toss_result[A_PROBABILITY_COLUMN_NAME] * \
            toss_result[B_PROBABILITY_COLUMN_NAME]
        toss_result[AB_PROBABILITY_COLUMN_NAME] = toss_result[AB_COUNT_COLUMN_NAME] / \
            current_sample_size

        # Append this sample size's results to the final result
        results.append(toss_result)

    # return the results as a pandas dataframe and the expected probabilities for each event
    return pd.DataFrame(results), len(A_event_space) / die_size, len(B_event_space) / die_size, len(AB_event_space) / die_size


def plot_simulation(data_frame, expected_pa, expected_pb, expected_pab, A, B, AB, die_size):
    # Define the values to use in the plot
    x = data_frame[SAMPLE_SIZE_COLUMN_NAME].tolist()
    y_pa = data_frame[A_PROBABILITY_COLUMN_NAME].tolist()
    y_pb = data_frame[B_PROBABILITY_COLUMN_NAME].tolist()
    y_pa_pb = data_frame[AxB_PROBABILITY_COLUMN_NAME].tolist()
    y_pab = data_frame[AB_PROBABILITY_COLUMN_NAME].tolist()

    # Define the subplots to use
    fig, axs = plt.subplots(3, 1)

    # ------------------------------------------------------
    # Plot the probability of A
    axs[0].set_title(
        f"Evolution of {A_PROBABILITY_COLUMN_NAME},{B_PROBABILITY_COLUMN_NAME} and {AB_PROBABILITY_COLUMN_NAME} with increase in {SAMPLE_SIZE_COLUMN_NAME}, on a {die_size}x sided die")
    axs[0].plot(x, y_pa, label=r'$\hat{}$'.format(
        A_PROBABILITY_COLUMN_NAME))

    # Plot expected value for A
    axs[0].plot(x, [expected_pa] * len(x),
                label=f"{A_PROBABILITY_COLUMN_NAME}={expected_pa}")
    axs[0].legend(loc='upper right')
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Plot the probability of B
    axs[1].plot(x, y_pb, label=r'$\hat{}$'.format(B_PROBABILITY_COLUMN_NAME))

    # Plot expected value for B
    axs[1].plot(x, [expected_pb] * len(x),
                label=f"{B_PROBABILITY_COLUMN_NAME}={expected_pb}")
    axs[1].legend(loc='upper right')
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Plot the probability of AB
    axs[2].plot(x, y_pab, label=r'$\hat{}$'.format(AB_PROBABILITY_COLUMN_NAME))

    # Plot P(A) x P(B)
    axs[2].plot(x, y_pa_pb, label=r'$\hat{}$'.format(
        AxB_PROBABILITY_COLUMN_NAME))

    # Plot expected value for AB
    axs[2].plot(x, [expected_pab] * len(x),
                label=f"{AB_PROBABILITY_COLUMN_NAME}={expected_pab}")
    axs[2].legend(loc='upper right')
    # ------------------------------------------------------

    plt.figtext(0.4, 0.03, f"A = {A}, B = {B}, AB = {AB}")

    plt.legend()
    plt.show()


# ---------------------------------------------------------------------
# Run the experiment with the values suggested by the author
def run(sample_size=1000, die_size=6, A=[2, 4, 6], B=[1, 2, 3, 4], AB=[2, 4]):
    simulation_result, pa, pb, pab = simulate_tosses(
        sample_size, die_size, A, B, AB)

    print(simulation_result)

    plot_simulation(simulation_result, pa, pb, pab, A, B, AB, die_size)


# Independent events
run()

# Non independent events
# run(A=[2, 4, 6], B=[2, 4, 5], AB=[2, 4])

# ---------------------------------------------------------------------
