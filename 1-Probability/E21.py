# importing the required modules
import random
import matplotlib.pyplot as plt
import pandas as pd


##############################################################################################
############# TO SEE THE SOLUTION, UNCOMMENT THE CODE AT THE END OF THE SCRIPT ###############
##############################################################################################


# Dataframe identification of the columns used
SAMPLE_SIZE_COLUMN_NAME = 'Sample Size'
HEADS_PROBABILITY_COLUMN_NAME = 'Probability of Heads'
C_HEADS_COLUMN_NAME = 'Count(H)'
P_HEADS_COLUMN_NAME = 'P(H)'
C_TAILS_COLUMN_NAME = 'Count(T)'
P_TAILS_COLUMN_NAME = 'P(T)'


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


def simulate_tosses(sample_size, heads_probability):
    # toss a coin sample_size times and save the count obtained for each coin side in a dictionary, for each size
    results = []
    for current_sample_size in range(1, sample_size + 1):
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


def coin_toss(heads_probability):
    # Throw exception if an invalid probability for the toss is provided
    if heads_probability < 0 or heads_probability > 1:
        raise Exception("Invalid probability value (must be between 0 and 1")

    # Create a random probability value to use in this toss
    randomProbability = random.uniform(0, 1)

    # Compare with the provided probability to simulate a toss
    if(randomProbability <= heads_probability):
        return P_HEADS_COLUMN_NAME
    else:
        return P_TAILS_COLUMN_NAME


# Simulate the tosses with the values suggested by the author
SAMPLE_SIZE = 1000
HEADS_PROBABILITY = 0.3

# -------- UNCOMMENT TO RUN --------
# tosses = simulate_tosses(SAMPLE_SIZE, HEADS_PROBABILITY)
# print(tosses)

# plot(tosses)
# -------- UNCOMMENT TO RUN --------
