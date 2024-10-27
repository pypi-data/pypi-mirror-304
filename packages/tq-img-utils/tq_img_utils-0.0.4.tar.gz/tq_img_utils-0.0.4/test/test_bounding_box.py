from tq_img_utils import BoundingBox


def test_area():
    print()
    try:
        BoundingBox(1, 1, -1, 3)
    except ValueError as e:
        print(e)  # The area of the bounding must be positive(w:-1, h:3).


def test_constrain():
    print()
    b = BoundingBox(1, 1, 3, 3, (2, 2))
    print(b)  # BoundingBox(x=1, y=1, width=1, height=1)


def test_constrain_warn():
    print()
    try:
        BoundingBox(1, 1, 3, 3, (2, 2), True)
    except ValueError as e:
        print(e)  # The bounding((1, 1, 3, 3)) is out of constraint((2, 2)).
