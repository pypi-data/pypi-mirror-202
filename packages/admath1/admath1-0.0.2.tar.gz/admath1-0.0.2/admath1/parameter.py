PI = 3.14159265359

def circle(
        radius:float
) -> None:
    '''Find Perimeter of Circle'''
    return round(2*PI*radius,3)


def ractangle(
        length:float,
        width:float
) -> None:
    '''Find Perimeter of Ractangle'''
    return 2*(length*width)

def Triangle(
        side1:float,
        side2:float,
        side3:float
) -> None:
    '''Find Perimeter of Triangle'''
    return side1+side2+side3

def square(
        side:float
) -> None:
    '''Find Perimeter of Square'''
    return 4*side

def regular_polygon(
        side:float,
        number_side:float
) -> None:
    '''Find Perimeter of Regular_Polygon'''
    return side*number_side

def circle(
        radius:float
) -> None:
    '''Find Perimeter of Circle'''
    return round(2*PI*radius,3)
def circle(
        radius:float
) -> None:
    '''Find Perimeter of Circle'''
    return round(2*PI*radius,3)


def trapezoid(
        top_base:float,
        bottom_base:float,
        right_height:float,
        left_height:float
) -> None:
    '''Find Perimeter of Trapexoid'''

    return top_base+bottom_base+right_height+left_height

def parallelogram(
        side1:float,
        side2:float
) -> None:
    '''Find Perimeter of Parallelogram:'''
    return 2(side1+side2)

def ellipse(
        major_axis:float,
        minor_axis:float,
) -> None:
    '''Find Perimeter of Ellipse'''
    return round(PI*(major_axis+minor_axis),3)


def kite(
        diagonal1:float,
        diagonal2:float
) -> None:
    '''Find Perimeter of Kite'''
    return (2*diagonal1)+(2*diagonal2)


def rhombus(
        side:float
) -> None:
    '''Find Perimeter of Rhombus'''
    return 4*side


def hexagon(
        side:float
)->None:
    """Find perimeter of Hexagon"""
    return 6*side

def equi_traingle(
        side:float
) -> None:
    '''Find Perimeter of Equilateral triangle'''
    return 3*side

def annulus(
        outer_radius:float,
        inner_radius:float
) -> None:
    '''Find Perimeter of Annulus'''
    return round(2*PI*(outer_radius+inner_radius),3)


