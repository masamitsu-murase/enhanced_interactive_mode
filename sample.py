import enum


class A:
    class_attr1 = "Class Attr1"
    """docstring for A.class_attr1"""

    class_attr2 = class_attr3 = "Class Attr 2, 3"
    """docstring for A.class_attr2 and A.class_attr3
    2nd line
    3行目"""

    @property
    def prop1(self):
        """docstring for A.prop1"""
        return 0

    @property
    def prop2(self):
        """docstring for A.prop2"""
        return 0

    def method1(self):
        """docstring for A.method1
        """
        pass

    def method2(self):
        """docstring for A.method2
        """
        pass


if True:
    class B(A):
        class_attr1 = "Class Attr1 (B)"
        """docstring for B.class_attr1"""

        class_attr2 = "Class Attr 2 (B)"
        """docstring for B.class_attr2
        2nd line
        3行目"""

        @property
        def prop1(self):
            """docstring for B.prop1"""
            return 0

        def method1(self):
            """docstring for B.method1
            """
            pass


class E(enum.IntEnum):
    AA = 1
    """docstring for Enum AA"""
    BB = 2
    """docstring for Enum BB"""
    CC = 3
    """docstring for Enum CC"""
