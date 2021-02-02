import field

def getMovement(robots_data, idx):

    # need to adjust by the user
    mangnitude_factor = 10
    
    force, direction = field.getResultant(robots_data, idx)

    return (force * mangnitude_factor , direction)


def action(robots_data, power_factor, test_case_obj):

    no_of_robots = len(robots_data)
    results = []
    for i in range(no_of_robots):
        results.append(field.getResultant(robots_data, i, power_factor, test_case_obj))
    return results
