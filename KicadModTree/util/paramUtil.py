# KicadModTree is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KicadModTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2016-2018 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>
# (C) 2018 by Rene Poeschl, github @poeschlr


from KicadModTree.Vector import *


def toNumberArray(value, length=2, min_value=1, member_type=int):
    r""" Convert value into an array of given type with given length

    :param value:
        Possible input types:
          * numnber (int or float) -> returns array filled with copies of value
          * dict -> arreay created with values for keys 'x', 'y', 'z'.
            dict only supported for len 2 and 3
          * list or tuple -> truncated to length
          * Vector -> truncated to lenght

    :param length: (``int``) -- default: 2
        Defines the length of the resulting array

    :min_value: (``int``) -- default: 1
        Defines the minimum alowed value (raise value error if too low)
        None -> No check

    :param mamber_type: (``type``) -- default: <type: int>
        all members of the array will be converted to this type
    """
    if type(value) in [int, float]:
        result = [value for i in range(length)]
    elif type(value) is dict:
        if length in [2, 3]:
            KEYS = ['x', 'y', 'z']
            result = [value[KEYS[i]] for i in range(length)]
        else:
            raise TypeError('Dict only supported for length 2 or 3.')
    elif type(value) in [list, tuple]:
        if len(value) >= length:
            result = value[:length]
    elif type(value) in [Vector2D, Vector3D]:
        if len(value) < length:
            raise TypeError('Vector dimensions ({}) are too low. Must be at least {}'.format(len(value), length))
        result = list(value)
    else:
        raise TypeError('Unsupported type: {}'.format(type(value)))

    result = [member_type(v) for v in result]

    if min_value is not None:
        for v in result:
            if v < min_value:
                raise ValueError("Value ({}) too small. Linit is {}.".format(v, min_value))

    return result


def toIntArray(value, length=2, min_value=1):
    r""" Convert value into an array of ints of given length

    :param value:
        Possible input types:
          * numnber (int or float) -> returns array filled with copies of value
          * dict -> arreay created with values for keys 'x', 'y', 'z'.
            dict only supported for len 2 and 3
          * list or tuple -> truncated to length
          * Vector -> truncated to lenght

    :param length: (``int``) -- default: 2
        Defines the length of the resulting array

    :min_value: (``int``) -- default: 1
        Defines the minimum alowed value (raise value error if too low)
        None -> No check
    """
    return toNumberArray(value, length, min_value, member_type=int)


def toFloatArray(value, length=2, min_value=1):
    r""" Convert value into an array of floats of given length

    :param value:
        Possible input types:
          * numnber (int or float) -> returns array filled with copies of value
          * dict -> arreay created with values for keys 'x', 'y', 'z'.
            dict only supported for len 2 and 3
          * list or tuple -> truncated to length
          * Vector -> truncated to lenght

    :param length: (``int``) -- default: 2
        Defines the length of the resulting array

    :min_value: (``int``) -- default: 1
        Defines the minimum alowed value (raise value error if too low)
        None -> No check
    """
    return toNumberArray(value, length, min_value, member_type=int)


def toVectorUseCopyIfNumber(value, length=2, low_limit=None, must_be_larger=True):
    r""" Convert value into an vector of given dimension

    :param value:
        The value to convert.
        Supported types are all types allowed for vector constructor plus int/float.
        If int/float vector will be initialized with the correct number of copies.

    :param length: (2 or 3) -- default: 2
        Defines the dimension of the resulting vector

    :param low_limit: (``int``) -- default: None
        Defines the minimum alowed value (raise value error if too low)
        None -> No check

    :param must_be_larger: (``bool``) -- default: True
       Defines if the number must be larger than the limit or if the limit is
       the minimum value.
    """

    if type(value) in [int, float]:
        result = [value for i in range(length)]
    else:
        result = value

    if low_limit is not None:
        limits = toFloatArray(low_limit, length, min_value=None)
        i = 0
        for v in result if type(result) is not dict else result.values():
            if v < limits[i] or (must_be_larger and v <= limits[i]):
                raise ValueError("Value ({}) too small. Linit is {}.".format(v, low_limit))
            i += 1

    if length == 2:
        return Vector2D(result)
    if length == 3:
        return Vector3D(result)

    raise ValueError("length must be 2 or 3")
