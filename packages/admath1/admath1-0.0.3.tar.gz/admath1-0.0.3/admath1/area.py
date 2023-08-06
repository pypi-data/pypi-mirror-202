PI = 3.14159265359

def traingle(
        base:float,
        height:float,
) -> None:
    '''Find area of Traingle'''
    return 1/2*(base*height)

def rect(
        length:float,
        width:float,
) -> None:
    '''Find area of Rectangle'''
    return length*width

def square(
        side:float,
) -> None:
    '''Find area of Square'''
    return side**2

def circle(
        radius:float
) -> None:
    '''Find area of Circle'''
    return round(PI*radius,2)

def trapezoid(
        top_base:float,
        bottom_base:float,
        height:float
) -> None:
    '''Find area of Trapexoid'''

    return ((top_base+bottom_base)/2)*height

def ellipse(
        radius_major_axis:float,
        radius_minor_axis:float,
) -> None:
    '''Find area of Ellipse'''
    return round(PI*radius_major_axis*radius_minor_axis,2)


def parallelogram(
         base:float,
        height:float,
) -> None:
    '''Find area of parallelogram'''
    return base*height

def rhombus(
        diagonal1:float,
        diagonal2:float
) -> None:
    '''Find area of Rhombus'''
    return (diagonal1*diagonal2)/2

# nopt completed
def regular_polygon(
        side:float,
        side_number:float
) -> None:
    '''Find area of regular_polygon'''
    # r=round(side_number*(PI/180),6)
    # return round(PI*radius,2)

def sphare(
        radius:float
) -> None:
    '''Find area of Shpare'''
    return round(4*PI*(radius*radius),2)

def cube(
        side:float
) -> None:
    '''Find area of Cube'''
    return 6*(side**2)

def cylinder(
        radius:float,
        height:float
) -> None:
    '''Find area of Cylinder'''
    return round((2*PI*(radius**2)+(2*PI*radius*height)),4)

def kite(
    diagonal1:float,
    diagonal2:float
) -> None:        
    '''Find area of Kite'''
    return round((diagonal1*diagonal2)/2,3)

def Annulus(
        outer_radius:float,
        inner_radius:float
) -> None:
    '''Find area of Annulus'''
    return round(PI*((outer_radius**2)-(inner_radius**2)),3)







