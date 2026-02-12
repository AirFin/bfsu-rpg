# -*- coding: utf-8 -*-
"""
碰撞检测模块
"""


class CollisionSystem:
    """碰撞检测系统"""
    
    @staticmethod
    def rect_collision(rect1, rect2):
        """
        矩形碰撞检测
        rect: (x, y, width, height)
        """
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        
        return (x1 < x2 + w2 and
                x1 + w1 > x2 and
                y1 < y2 + h2 and
                y1 + h1 > y2)
    
    @staticmethod
    def point_in_rect(point, rect):
        """
        点是否在矩形内
        point: (x, y)
        rect: (x, y, width, height)
        """
        px, py = point
        rx, ry, rw, rh = rect
        
        return rx <= px <= rx + rw and ry <= py <= ry + rh
    
    @staticmethod
    def entity_collision(entity1, entity2):
        """
        两个实体的碰撞检测
        实体需要有 x, y, width, height 属性
        """
        rect1 = (entity1.x, entity1.y, entity1.width, entity1.height)
        rect2 = (entity2.x, entity2.y, entity2.width, entity2.height)
        return CollisionSystem.rect_collision(rect1, rect2)
