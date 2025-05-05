import random
import math
import matplotlib.pyplot as plt


towns = [
    "Windhoek", "Swakopmund", "Walvis Bay", "Otjiwarongo", "Tsumeb",
    "Grootfontein", "Mariental", "Keetmanshoop", "Ondangwa", "Oshakati"
]


distance_matrix = [
    [0, 360, 400, 250, 435, 515, 270, 495, 620, 640],
    [360, 0, 35, 470, 650, 730, 500, 730, 840, 860],
    [400, 35, 0, 490, 670, 750, 470, 700, 870, 890],
    [250, 470, 490, 0, 180, 260, 430, 650, 360, 380],
    [435, 650, 670, 180, 0, 70, 610, 830, 200, 220],
    [515, 730, 750, 260, 70, 0, 680, 900, 160, 180],
    [270, 500, 470, 430, 610, 680, 0, 220, 790, 810],
    [495, 730, 700, 650, 830, 900, 220, 0, 1010, 1030],
    [620, 840, 870, 360, 200, 160, 790, 1010, 0, 40],
    [640, 860, 890, 380, 220, 180, 810, 1030, 40, 0],
]

class TSP:
    def __init__(self, towns, distances):
        self.towns = towns
        self.distances = distances

    def total_distance(self, route):
        distance = 0
        for i in range(len(route)):
            from_town = route[i]
            to_town = route[(i + 1) % len(route)] 
            distance += self.distances[from_town][to_town]
        return distance

class SimulatedAnnealingSolver:
    def __init__(self, tsp, temp=10000, cooling_rate=0.003, max_iter=10000):
        self.tsp = tsp
        self.temp = temp
        self.cooling_rate = cooling_rate
        self.max_iter = max_iter

    def accept_probability(self, old_cost, new_cost, temperature):
        if new_cost < old_cost:
            return 1.0
        return math.exp((old_cost - new_cost) / temperature)

    def random_neighbor(self, route):
        a, b = random.sample(range(1, len(route)), 2) 
        neighbor = route[:]
        neighbor[a], neighbor[b] = neighbor[b], neighbor[a]
        return neighbor

    def solve(self):
        current_route = list(range(len(self.tsp.towns)))
        random.shuffle(current_route[1:])  
        best_route = current_route[:]
        best_cost = self.tsp.total_distance(best_route)
        current_cost = best_cost
        temperature = self.temp

        for _ in range(self.max_iter):
            neighbor = self.random_neighbor(current_route)
            neighbor_cost = self.tsp.total_distance(neighbor)

            if self.accept_probability(current_cost, neighbor_cost, temperature) > random.random():
                current_route = neighbor
                current_cost = neighbor_cost
                if neighbor_cost < best_cost:
                    best_route = neighbor
                    best_cost = neighbor_cost
            temperature *= (1 - self.cooling_rate)
            if temperature < 1e-10:
                break
        return best_route, best_cost

def plot_route(tsp, route, title):
    x = [i for i in range(len(route) + 1)]
    y = [tsp.towns[i] for i in route + [route[0]]]
    print(f"\n{title}")
    print(" -> ".join([tsp.towns[i] for i in route + [route[0]]]))
    print(f"Total Distance: {tsp.total_distance(route)} km")
    plt.figure(figsize=(10, 4))
    plt.plot(x, route + [route[0]], marker='o')
    plt.title(title)
    plt.xticks(x, y, rotation=45)
    plt.xlabel("Route Order")
    plt.ylabel("Town Index")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    tsp = TSP(towns, distance_matrix)
    solver = SimulatedAnnealingSolver(tsp)
    initial_route = list(range(len(towns)))
    random.shuffle(initial_route[1:])
    initial_distance = tsp.total_distance(initial_route)
    final_route, final_distance = solver.solve()
    plot_route(tsp, initial_route, "Initial Random Route")
    plot_route(tsp, final_route, "Optimized Route via Simulated Annealing")
