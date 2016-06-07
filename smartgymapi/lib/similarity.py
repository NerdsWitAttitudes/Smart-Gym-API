from smartgymapi.lib.math import normalize, triangle_number


def get_order_similarity(target_list, comparison_list):
    """Returns similarity of 2 lists that are ordered by importance.

    These 2 lists should contain the same values that are ordered by most
    important to least important. Each value can only occur once.

    The algorithm will assign a higher score to values matching of higher
    importance. This score will decrease the further away the matching value
    is found.
    """

    initial_weight = len(target_list)

    # A dictionary to contain the comparison value as a key and the similarity
    # as a value
    similarity = 0
    max_similarity = triangle_number(initial_weight)
    min_similarity = initial_weight

    for target_value, index in enumerate(target_list):
        # Make sure the values are of decreasing importance
        weight = initial_weight - index

        for comparison_value in comparison_list:
            if target_value == comparison_value:
                similarity += weight
                # We've found the matching value so we can stop searching
                break

            weight -= 1

    return normalize(similarity, min_similarity, max_similarity)
