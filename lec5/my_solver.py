import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def two_opt(dist:list[list[int]], tour:list[int]):
    N = len(tour)
    if N < 50:
        n = N
    else:
        n = int(N ** 0.8)
    # 現在の距離を計算 distを使う
    current_distance = sum(dist[tour[i]][tour[(i + 1) % N]]
                              for i in range(N))
    
    count = 0
    
    while True:
        count += 1
        print(count)
        past_distance = current_distance
        # tourの中から１点Aを選ぶ。Aの次の点をBとする。Aから距離の近い√N点（N<100の場合はN/2点）に対して、以下の操作を行う。
        # Aから近い点をCとする。Cの次の点をDとする。AB+CDとAC+BDを比較して、AC+BDの方が短かったらBとCを入れ替える。
        for a in tour:
            aIndex = tour.index(a)
            # tourの最後の点の時はスタート地点を、それ以外の時は次の地点をbとする
            if aIndex == len(tour)-1:
                bIndex = tour.index(tour[0])
            else:
                bIndex = tour.index(tour[aIndex+1])

            # aに近い順番にソートして、その中から√N個（N<100の場合はN/2個）のみ選択
            close_cities = sorted(range(len(dist[a])), key=lambda city: dist[a][city])[1:n]
            for c in close_cities:
                cIndex = tour.index(c)
                if cIndex == len(tour)-1:
                    dIndex = tour.index(tour[0])
                else:
                    dIndex = tour.index(tour[cIndex+1])
                new_tour = tour.copy()
                new_tour[bIndex:tour.index(dIndex)] = reversed(tour[bIndex:tour.index(dIndex)])
                # 近い点cとbを入れ替えた状態と現在の状態で距離を比較し、入れ替えた方が良い場合は入れ替える
                new_distance = sum(dist[new_tour[i]][new_tour[(i + 1) % N]]
                                for i in range(N))
                if(new_distance < current_distance):
                    tour = new_tour
                    current_distance = new_distance

        # あまり更新されなくなってきたら終了
        if (past_distance - current_distance)/past_distance < 0.01:
            break

    print(current_distance, count)

    return tour


def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    
    improved_tour = two_opt(dist, tour)
    return improved_tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour, sys.argv[2])

    # tour = solve(read_input("lec5/google-step-tsp/input_2.csv"))
    # print_tour(tour, "lec5/google-step-tsp/output_2.csv")