import turtle
import math


def square_vertices(x: float, y: float, size: float, heading: float):
    """Повертає список з 4 комплексних чисел - вершин квадрата"""
    ang = math.radians(heading)
    v = complex(math.cos(ang), math.sin(ang)) * size
    p0 = complex(x, y)
    p1 = p0 + v
    p2 = p1 + v * 1j
    p3 = p0 + v * 1j
    return [p0, p1, p2, p3]


def draw_filled_square(t: turtle.Turtle, pts: list[complex]):
    """Малює контур квадрата"""
    t.penup()
    t.goto(pts[0].real, pts[0].imag)
    t.pendown()
    for p in pts[1:]:
        t.goto(p.real, p.imag)
    t.goto(pts[0].real, pts[0].imag)


def pythagor_tree(t: turtle.Turtle, x: float, y: float, size: float, heading: float, depth: int, angle_deg: float):
    """Малює дерево Піфагора"""
    if depth < 0 or size <= 0:
        return

    pts = square_vertices(x, y, size, heading)
    draw_filled_square(t, pts)

    if depth == 0:
        return

    p0, p1, p2, p3 = pts

    theta = math.radians(angle_deg)
    rot = complex(math.cos(theta), math.sin(theta))
    P = p3 + (p2 - p3) * math.cos(theta) * rot

    size_left = abs(P - p3)
    heading_left = heading + angle_deg
    pythagor_tree(t, p3.real, p3.imag, size_left, heading_left, depth - 1, angle_deg)

    size_right = abs(p2 - P)
    heading_right = math.degrees(math.atan2((p2 - P).imag, (p2 - P).real))
    pythagor_tree(t, P.real, P.imag, size_right, heading_right, depth - 1, angle_deg)


if __name__ == '__main__':
    try:
        depth = int(input("Введіть рівень рекурсії (наприклад 6): "))
    except Exception:
        depth = 6
    
    angle = 45.0
    size = 120.0

    screen = turtle.Screen()
    screen.setup(width=1000, height=800)
    screen.bgcolor('white')
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)

    # start bottom-center
    start_x = -size / 2
    start_y = -300 / 2
    pythagor_tree(t, start_x, start_y, size, 0.0, depth, angle)

    screen.mainloop()
    