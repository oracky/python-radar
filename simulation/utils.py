from dataclasses import dataclass


@dataclass
class Point2D:
    x : float
    y : float


class PointHelper:
    @staticmethod
    def get_sign(p1 : Point2D, p2 : Point2D, p3 : Point2D):
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)
    
    @staticmethod
    def is_point_in_triangle(pt : Point2D, v1 : Point2D, v2 : Point2D, v3 : Point2D):
        d1 = PointHelper.get_sign(pt, v1, v2)
        d2 = PointHelper.get_sign(pt, v2, v3)
        d3 = PointHelper.get_sign(pt, v3, v1)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not(has_neg and has_pos)
