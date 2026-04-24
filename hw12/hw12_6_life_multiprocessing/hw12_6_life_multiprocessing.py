import multiprocessing
import random as r


def simulate_life(org_id: int) -> str:
    """
    Simulates one life cycle of an organism.
    :param org_id: unique identifier of the organism
    :return: status of the organism after the cycle
    """
    life_resource = 10 * r.randint(4, 10)
    life_satiety = r.randint(40, 100)
    life_resource_loss = life_resource + r.randint(-50, 0)
    life_satiety_loss = life_satiety + r.randint(-80, -20)

    if life_resource_loss <= 0 or life_satiety_loss <= 0:
        return "dead"
    elif life_resource_loss > 30 and life_satiety_loss > 30:
        return "reproduced"
    else:
        return "survived"


if __name__ == "__main__":
    population_size = 80000
    organisms = list(range(1, population_size + 1))
    with multiprocessing.Pool() as pool:
        results = pool.map(simulate_life, organisms)

    stats = {
        "Died": results.count('dead'),
        "Survived": results.count('survived'),
        "Gave birth": results.count('reproduced')
    }

    print("=" * 40)
    print(f"{'Start population size ':<25} | {population_size:>12,}")
    for label, value in stats.items():
        print(f"{label:<25} | {value:>12,}")
    print("=" * 40)
