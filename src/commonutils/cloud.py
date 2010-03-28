import math

def calculate_thresholds(counts, steps=4, is_linear = False):
    """
    Takes a list of counts and returns the list of thresholds
    for the given number of steps
    """
    thresholds = []
    if counts == []:
        return thresholds
    if counts != []:
        max_count = float(max(counts))
        min_count = float(min(counts))

    # there are (steps - 1) thresholds
    if is_linear:
        # linear distribution
        delta = (max_count - min_count) / float(steps)
        thresholds = [min_count + i * delta for i in range(1, steps)]
    else:
        # logarithmic distribution
        thresholds = [math.pow(max_count - min_count, float(i) / float(steps-1)) \
                      for i in range(1, steps)]
    return thresholds

def calculate_weights(counts, thresholds):
    """
    Takes a list of counts and a list of thresholds,
    returns a list of weights corresponding each count item in the counts list
    """
    weights = []
    steps = len(thresholds) + 1
    for i in range(len(counts)):
        for j in range(steps - 1):
            if counts[i] <= thresholds[j]:
                weights.append(j + 1)
                break
            elif j == steps - 2:
                # last step
                weights.append(j + 2)
    return weights

def calculate_cloud(items, steps=4, is_linear = False):
    """
    Accepts a list of items in the format [['ankara', 3], ['izmir', 5], ...]
    and returns a dict in the format {'ankara':1, 'izmir':2}
    """
    thresholds = []
    counts = [item[1] for item in items]
    thresholds = calculate_thresholds(counts=counts, steps=steps)
    weights = calculate_weights(counts, thresholds)
    list = {}
    for i in range(len(items)):
        list[items[i][0]] = weights[i]
    return list


if __name__ == '__main__':
    """
    list = [['ank', 1], ['ist', 13], ['izm', 4], ['ant', 14], ['adn', 15]]
    calculate_cloud(list, steps=4)
    print list
    """
    

