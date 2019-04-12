
# Modified from https://www.python-course.eu/levenshtein_distance.php
def __iterative_levenshtein(s, t, weights=(1,1,1)):
    """ 
    iterative_levenshtein(s, t) -> ldist
    ldist is the Levenshtein distance between the strings 
    s and t.
    For all i and j, dist[i,j] will contain the Levenshtein 
    distance between the first i characters of s and the 
    first j characters of t
    
    weight_dict: keyword parameters setting the costs for characters,
                 the default value for a character will be 1
    """
    rows = len(s)+1
    cols = len(t)+1
    
    
    dist = [[0 for x in range(cols)] for x in range(rows)]
    # source prefixes can be transformed into empty strings 
    # by deletions:
    for row in range(1, rows):
        dist[row][0] = dist[row-1][0] + s[row-1]weights[0]
    # target prefixes can be created from an empty source string
    # by inserting the characters
    for col in range(1, cols):
        dist[0][col] = dist[0][col-1] + t[col-1]weights[1]
        
    for col in range(1, cols):
        for row in range(1, rows):
            deletes = s[row-1]weights[0]
            inserts = t[col-1]weights[1]
            subs = max( (s[row-1]weights[2], t[col-1]weights[2]))
            if s[row-1] == t[col-1]:
                subs = 0
            else:
                subs = subs
            dist[row][col] = min(dist[row-1][col] + deletes,
                                 dist[row][col-1] + inserts,
                                 dist[row-1][col-1] + subs) # substitution
 
    return dist[row][col]

def editDistance(phenotype, title_bank, weights=(1, 1, 1)):
    """
    Calculate the shortest levenshtein distance between phenotype and known titles.

    Args:
        phenotype (str) : Candidate phenotype.
        title_bank (dict) : Known titles, needs to have dictionaries as values, and those disctionaries need to have
                            'title' key.
        weights (tuple of floats) : Weights for different operations. In order: Delete, Insert, Substitute
    
    Returns:
        int : Shortest edit distance.
    """

    # Checking for exact match from the dictionary is fast
    if phenotype in title_bank:
        return 0

    closest = 1000

    for b_id, b_info in title_bank.items():
        # Skip candidates using lower-bound of the levenshtein distance.
        # Does not take the weights into account
        if abs(len(phenotype.strip()) - len(b_info["title"].strip())) > closest:
            continue

        levenshtein = __iterative_levenshtein(phenotype.strip(), b_info["title"].strip(), weights)
        closest = min(closest, levenshtein)
    
    return closest