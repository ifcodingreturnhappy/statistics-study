# importing the required modules
import random
import matplotlib.pyplot as plt
import pandas as pd

# Sample size used
sample_size = 1000

# Probability of getting heads when tossing the coin
heads_probability = 0.3

# Dataframe identification of the columns used
SAMPLE_SIZE_COLUMN_NAME = 'SIZE'
HEADS_PROBABILITY_COLUMN_NAME = 'HEADS_P'
HEADS_COLUMN_NAME = 'H'
TAILS_COLUMN_NAME = 'T'


def plot_tosses(data_frame):
    # Construct the bar chart
    ax = data_frame.plot(x=SAMPLE_SIZE_COLUMN_NAME,
                         y=[HEADS_COLUMN_NAME, TAILS_COLUMN_NAME],
                         ylim=(0, 1),
                         kind="bar",
                         title=f"{HEADS_COLUMN_NAME}/{TAILS_COLUMN_NAME} Proportions for {HEADS_COLUMN_NAME} probability of {heads_probability}")

    # Add a note to each bar for better readability
    y_note_adjustment_multiplier = 1.005
    for p in ax.patches:
        ax.annotate(str(p.get_height()),
                    (p.get_x() + p.get_width()/2, p.get_height()
                     * y_note_adjustment_multiplier),
                    ha='center')

    plt.show()


def simulate_tosses(sample_size, heads_probability):
    # toss a coin sample_size times and save the count obtained for each coin side in a dictionary
    results = {
        SAMPLE_SIZE_COLUMN_NAME: sample_size,
        HEADS_PROBABILITY_COLUMN_NAME: heads_probability,
        HEADS_COLUMN_NAME: 0,
        TAILS_COLUMN_NAME: 0,
    }
    for x in range(1, sample_size + 1):
        toss_result = coin_toss(heads_probability)
        if(toss_result == HEADS_COLUMN_NAME):
            results[HEADS_COLUMN_NAME] += 1
        else:
            results[TAILS_COLUMN_NAME] += 1

    # convert the count to a probability
    results[HEADS_COLUMN_NAME] = results[HEADS_COLUMN_NAME] / sample_size
    results[TAILS_COLUMN_NAME] = results[TAILS_COLUMN_NAME] / sample_size

    # return as a dataframe for easier plotting
    return pd.DataFrame([results])


def coin_toss(heads_probability):
    # Throw exception if an invalid probability for the toss is provided
    if heads_probability < 0 or heads_probability > 1:
        raise Exception("Invalid probability value (must be between 0 and 1")

    # Create a random probability value to use in this toss
    randomProbability = random.uniform(0, 1)

    # Compare with the provided probability to simulate a toss
    if(randomProbability <= heads_probability):
        return HEADS_COLUMN_NAME
    else:
        return TAILS_COLUMN_NAME


# Simulate the tosses with the values suggested by the author
tosses = simulate_tosses(sample_size, heads_probability)

# Plot the results of the simulation
plot_tosses(tosses)
