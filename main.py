# Hides an egg always on the full degree (e.g. 0° or 37°)
# Hides exactly one egg on each degree, in total 360 eggs.
# Observes the distance rule with at least 160m (>= 160m)
# Moves away from the sundial only when necessary and always as less as possible
# Moves always clockwise
# Hides the next egg as close as possible to the last
# Hides the first egg directly north on 0° 160m from the sundial

import math
from functools import lru_cache
from typing import List, Tuple


@lru_cache(maxsize=None)
def get_m_for_degree(winkel_grad: int) -> float:
    winkel_rad = math.radians(winkel_grad)
    winkel_x_achse = math.pi / 2 - winkel_rad
    steigung = math.tan(winkel_x_achse)
    return steigung


@lru_cache(maxsize=None)
def line_circle_intersection(h, k, r, m, b):
    a = 1 + m**2
    b = 2 * m * (b - k) - 2 * h
    c = h**2 + (b - k) ** 2 - r**2
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return None
    sqrt_discriminant = math.sqrt(discriminant)
    x1 = (-b + sqrt_discriminant) / (2 * a)
    x2 = (-b - sqrt_discriminant) / (2 * a)
    y1 = m * x1 + b
    y2 = m * x2 + b
    return (round(x1, 8), round(y1, 8)), (round(x2, 8), round(y2, 8))


def y_axis_circle_intersection(a, b, r):
    if abs(a) <= r:
        x1 = 0
        y1 = b + math.sqrt(r**2 - a**2)
        x2 = 0
        y2 = b - math.sqrt(r**2 - a**2)
        return (round(x1, 8), round(y1, 8)), (round(x2, 8), round(y2, 8))
    else:
        return None


def choose_point_for_degree(p1, p2, degree):
    if degree == 90:
        return p1 if p1[0] > 0 else p2
    if degree == 270:
        return p1 if p1[0] < 0 else p2
    if (0 <= degree <= 90) or (270 <= degree <= 360):
        return p1 if p1[1] > 0 else p2
    return p1 if p1[1] < 0 else p2


def is_far_away_from_every_point(point, p_list):
    for p in p_list:
        distanz = math.sqrt((point[0] - p[0]) ** 2 + (point[1] - p[1]) ** 2)
        if distanz < 160:
            return False
    return True


def get_next_degree(degree_list):
    last_degree = degree_list[-1]
    for i in range(last_degree + 1, 360):
        if i not in degree_list:
            return i
    for i in range(0, last_degree):
        if i not in degree_list:
            return i


def find_next_point(degree, circle_list):
    winkel_rad = math.radians(degree)
    x = math.sin(winkel_rad)
    y = math.cos(winkel_rad)
    schritt = 1
    punkt = (x * schritt, y * schritt)
    while not is_far_away_from_every_point(punkt, circle_list):
        schritt += 0.01
        punkt = (round(x * schritt, 8), round(y * schritt, 8))
    return punkt


def distance_to_cero(point):
    x, y = point
    distanz = math.sqrt((x - 0) ** 2 + (y - 0) ** 2)
    return round(distanz, 3)


def find_next_min_index(lst, start_index, degrees):
    filtered_lst = [x for i, x in enumerate(lst) if i not in degrees]
    if not filtered_lst:
        return None, None
    min_value = min(filtered_lst)
    min_indices = [i for i, x in enumerate(lst) if x == min_value and i not in degrees]
    checked = False
    result_index = -1
    for index in min_indices:
        if index > start_index:
            result_index = index
            checked = True
    if not checked:
        result_index = min_indices[0] if min_indices else None
    result_distance = min_value
    return result_index, result_distance


def do_for_all_degrees(start, end, eggs, degrees, current_circle_radius):
    for degree in range(start, end):
        if degree in degrees:
            continue
        if degree in [0, 180]:
            intersections = y_axis_circle_intersection(0, 0, current_circle_radius)
        else:
            m = get_m_for_degree(degree)
            intersections = line_circle_intersection(0, 0, current_circle_radius, m, 0)
        if intersections is None:
            continue
        p = choose_point_for_degree(intersections[0], intersections[1], degree)
        decision = is_far_away_from_every_point(p, eggs)
        if decision:
            eggs.append(p)
            degrees.append(degree)


def main():
    eggs: List[Tuple[float, float]] = [(0.0, 160.0)]
    degrees = [0]
    START_RADIUS = 160
    current_circle_radius = START_RADIUS
    first_egg_radius = 0
    round = 0

    while len(eggs) < 360:
        round += 1
        print("ROUND:", round)
        if round != 1:
            distances_to_cero = []
            for i in range(0, 359):
                np = find_next_point(i, eggs)
                distances_to_cero.append(distance_to_cero(np))
            res = find_next_min_index(distances_to_cero, degrees[-1], degrees)
            if res[0] is not None and res[1] is not None:
                current_circle_radius = res[1] 
                first_egg_radius = res[0]
            else:
                print("ERROOOOOOOOOOOOOOOR")

        print(eggs, degrees, current_circle_radius, first_egg_radius)
        do_for_all_degrees(first_egg_radius, 360, eggs, degrees, current_circle_radius)
        do_for_all_degrees(0, first_egg_radius, eggs, degrees, current_circle_radius)

        print("-------------")
        for i, egg in enumerate(eggs):
            print(i, egg)
        print(degrees)
        print()

main()
