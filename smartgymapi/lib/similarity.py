import logging

from smartgymapi.lib.math import normalize, triangle_number

log = logging.getLogger(__name__)


def get_ordered_list_similarity(target_list, comparison_list):
    """Returns similarity of 2 lists that are ordered by importance.

    These 2 lists should contain  values that are ordered by most
    important to least important. Each value can only occur once.

    The algorithm will assign a higher score to values matching of higher
    importance. This score will decrease the further away the matching value
    is found.
    """

    if not target_list or not comparison_list:
        # If one of the lists does not exist or is empty we can return early
        return 0

    # The initial weight should be set to the index +1 of the target value last
    # found in the comparison list. The algorithm should punish the comparison
    # for giving less importance to the target value but not for having
    # additional values after that.
    for index, value in enumerate(comparison_list):
        if value in target_list:
            initial_weight = index + 1

    if initial_weight == 0:
        # no matching values, no similarity
        return 0

    # A dictionary to contain the comparison value as a key and the similarity
    # as a value
    similarity = 0
    max_similarity = triangle_number(len(target_list))
    min_similarity = 0

    for index, target_value in enumerate(target_list):
        # Make sure the values are of decreasing importance
        weight = initial_weight - index

        for comparison_index, comparison_value in enumerate(comparison_list):
            if target_value == comparison_value:
                similarity += weight
                # We've found the matching value so we can stop searching
                break

            # if the target value is found at a higher index (so lower down
            # the list) we should punish the comparison for giving less
            # importance to the value
            if index < comparison_index:
                weight -= 1

    return normalize(similarity, min_similarity, max_similarity)
