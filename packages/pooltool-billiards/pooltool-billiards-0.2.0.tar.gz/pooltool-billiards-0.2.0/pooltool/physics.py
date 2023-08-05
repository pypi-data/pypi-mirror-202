#! /usr/bin/env python
"""Compilation of physics equations implemented as functions.

A convention is upheld for the input and output variable names that is consistent across
functions.  All units are SI
(https://en.wikipedia.org/wiki/International_System_of_Units)

`rvw` : numpy.array
    The ball state
    (https://ekiefl.github.io/2020/12/20/pooltool-alg/#what-is-the-system-state).  It is
    a 3x3 numpy array where rvw[0, :] is the displacement vector (r), rvw[1, :] is the
    velocity vector (v), and rvw[2, :] is the angular velocity vector (w). For example,
    rvw[1, 1] refers to the y-component of the velocity vector.
`R` : float
    The radius of the ball.
`m` : float
    The mass of the ball.
`h` : float
    The height of the cushion.
`s` : int
    The motion state of the ball. Definitions are found in pooltool.state_dict
`mu` : float
    The coefficient of friction. If ball motion state is sliding, assume coefficient of
    sliding friction. If rolling, assume coefficient of rolling friction. If spinning,
    assume coefficient of spinning friction
`u_s` : float
    The sliding coefficient of friction.
`u_sp` : float
    The spinning coefficient of friction.
`u_r` : float
    The rolling coefficient of friction.
`e_c` : float
    The cushion coefficient of restitution
`f_c` : float
    The cushion coefficient of friction
`g` : float
    The acceleration due to gravity felt by a ball.
"""

import math

import numpy as np
from numba import jit

import pooltool.constants as const
import pooltool.utils as utils


def resolve_ball_ball_collision(rvw1, rvw2):
    """FIXME Instantaneous, elastic, equal mass collision"""

    r1, r2 = rvw1[0], rvw2[0]
    v1, v2 = rvw1[1], rvw2[1]

    v_rel = v1 - v2
    v_mag = np.linalg.norm(v_rel)

    n = utils.unit_vector_fast(r2 - r1)
    t = utils.coordinate_rotation_fast(n, np.pi / 2)

    beta = utils.angle_fast(v_rel, n)

    rvw1[1] = t * v_mag * np.sin(beta) + v2
    rvw2[1] = n * v_mag * np.cos(beta) + v2

    return rvw1, rvw2


def resolve_ball_cushion_collision(rvw, normal, R, m, h, e_c, f_c):
    """Inhwan Han (2005) 'Dynamics in Carom and Three Cushion Billiards'"""

    # orient the normal so it points away from playing surface
    normal = normal if np.dot(normal, rvw[1]) > 0 else -normal

    # Change from the table frame to the cushion frame. The cushion frame is defined by
    # the normal vector is parallel with <1,0,0>.
    psi = utils.angle_fast(normal)
    rvw_R = utils.coordinate_rotation_fast(rvw.T, -psi).T

    # The incidence angle--called theta_0 in paper
    phi = utils.angle_fast(rvw_R[1]) % (2 * np.pi)

    # Get mu and e
    e = get_ball_cushion_restitution(rvw_R, e_c)
    mu = get_ball_cushion_friction(rvw_R, f_c)

    # Depends on height of cushion relative to ball
    theta_a = np.arcsin(h / R - 1)

    # Eqs 14
    sx = rvw_R[1, 0] * np.sin(theta_a) - rvw_R[1, 2] * np.cos(theta_a) + R * rvw_R[2, 1]
    sy = (
        -rvw_R[1, 1]
        - R * rvw_R[2, 2] * np.cos(theta_a)
        + R * rvw_R[2, 0] * np.sin(theta_a)
    )
    c = rvw_R[1, 0] * np.cos(theta_a)  # 2D assumption

    # Eqs 16
    I = 2 / 5 * m * R**2
    A = 7 / 2 / m
    B = 1 / m

    # Eqs 17 & 20
    PzE = (1 + e) * c / B
    PzS = np.sqrt(sx**2 + sy**2) / A

    if PzS <= PzE:
        # Sliding and sticking case
        PX = -sx / A * np.sin(theta_a) - (1 + e) * c / B * np.cos(theta_a)
        PY = sy / A
        PZ = sx / A * np.cos(theta_a) - (1 + e) * c / B * np.sin(theta_a)
    else:
        # Forward sliding case
        PX = -mu * (1 + e) * c / B * np.cos(phi) * np.sin(theta_a) - (
            1 + e
        ) * c / B * np.cos(theta_a)
        PY = mu * (1 + e) * c / B * np.sin(phi)
        PZ = mu * (1 + e) * c / B * np.cos(phi) * np.cos(theta_a) - (
            1 + e
        ) * c / B * np.sin(theta_a)

    # Update velocity
    rvw_R[1, 0] += PX / m
    rvw_R[1, 1] += PY / m
    # rvw_R[1,2] += PZ/m

    # Update angular velocity
    rvw_R[2, 0] += -R / I * PY * np.sin(theta_a)
    rvw_R[2, 1] += R / I * (PX * np.sin(theta_a) - PZ * np.cos(theta_a))
    rvw_R[2, 2] += R / I * PY * np.cos(theta_a)

    # Change back to table reference frame
    rvw = utils.coordinate_rotation_fast(rvw_R.T, psi).T

    return rvw


def get_ball_cushion_restitution(rvw, e_c):
    """Get restitution coefficient dependent on ball state

    Parameters
    ==========
    rvw: np.array
        Assumed to be in reference frame such that <1,0,0> points
        perpendicular to the cushion, and in the direction away from the table

    Notes
    =====
    - https://essay.utwente.nl/59134/1/scriptie_J_van_Balen.pdf suggests a constant
      value of 0.85
    """

    return e_c
    return max([0.40, 0.50 + 0.257 * rvw[1, 0] - 0.044 * rvw[1, 0] ** 2])


def get_ball_cushion_friction(rvw, f_c):
    """Get friction coeffecient depend on ball state

    Parameters
    ==========
    rvw: np.array
        Assumed to be in reference frame such that <1,0,0> points
        perpendicular to the cushion, and in the direction away from the table
    """

    ang = utils.angle_fast(rvw[1])

    if ang > np.pi:
        ang = np.abs(2 * np.pi - ang)

    ans = f_c
    return ans


@jit(nopython=True, cache=const.numba_cache)
def skip_ball_ball_collision(rvw1, rvw2, s1, s2, R1, R2):
    if (s1 == const.spinning or s1 == const.pocketed or s1 == const.stationary) and (
        s2 == const.spinning or s2 == const.pocketed or s2 == const.stationary
    ):
        # Neither balls are moving. No collision.
        return True

    if s1 == const.pocketed or s2 == const.pocketed:
        # One of the balls is pocketed
        return True

    if s1 == const.rolling and s2 == const.rolling:
        # Both balls are rolling (straight line trajectories). Here I am checking
        # whether both dot products face away from the line connecting the two balls. If
        # so, they are guaranteed not to collide
        r12 = rvw2[0] - rvw1[0]
        dot1 = r12[0] * rvw1[1, 0] + r12[1] * rvw1[1, 1] + r12[2] * rvw1[1, 2]
        if dot1 <= 0:
            dot2 = r12[0] * rvw2[1, 0] + r12[1] * rvw2[1, 1] + r12[2] * rvw2[1, 2]
            if dot2 >= 0:
                return True

    if s1 == const.rolling and (s2 == const.spinning or s2 == const.stationary):
        # ball1 is rolling, which guarantees a straight-line trajectory. Some
        # assumptions can be made based on this fact
        r12 = rvw2[0] - rvw1[0]

        # ball2 is not moving, so we can pinpoint the range of angles ball1 must be
        # headed in for a collision
        d = np.linalg.norm(r12)
        unit_d = r12 / d
        unit_v = utils.unit_vector_fast(rvw1[1])

        # Angles are in radians
        # Calculate forwards and backwards angles, e.g. 10 and 350, take the min
        angle = np.arccos(np.dot(unit_d, unit_v))
        max_hit_angle = 0.5 * np.pi - math.acos((R1 + R2) / d)
        if angle > max_hit_angle:
            return True

    if s2 == const.rolling and (s1 == const.spinning or s1 == const.stationary):
        # ball2 is rolling, which guarantees a straight-line trajectory. Some
        # assumptions can be made based on this fact
        r21 = rvw1[0] - rvw2[0]

        # ball1 is not moving, so we can pinpoint the range of angles ball2 must be
        # headed in for a collision
        d = np.linalg.norm(r21)
        unit_d = r21 / d
        unit_v = utils.unit_vector_fast(rvw2[1])

        # Angles are in radians
        # Calculate forwards and backwards angles, e.g. 10 and 350, take the min
        angle = np.arccos(np.dot(unit_d, unit_v))
        max_hit_angle = 0.5 * np.pi - math.acos((R1 + R2) / d)
        if angle > max_hit_angle:
            return True

    return False


def get_ball_ball_collision_coeffs(rvw1, rvw2, s1, s2, mu1, mu2, m1, m2, g1, g2, R):
    """Get the quartic coeffs required to determine the ball-ball collision time"""
    c1x, c1y = rvw1[0, 0], rvw1[0, 1]
    c2x, c2y = rvw2[0, 0], rvw2[0, 1]

    if s1 in const.nontranslating:
        a1x, a1y, b1x, b1y = 0, 0, 0, 0
    else:
        phi1 = utils.angle_fast(rvw1[1])
        v1 = np.linalg.norm(rvw1[1])

        u1 = (
            np.array([1, 0, 0])
            if s1 == const.rolling
            else utils.coordinate_rotation_fast(
                utils.unit_vector_fast(utils.get_rel_velocity_fast(rvw1, R)), -phi1
            )
        )

        K1 = -0.5 * mu1 * g1
        cos_phi1 = np.cos(phi1)
        sin_phi1 = np.sin(phi1)

        a1x = K1 * (u1[0] * cos_phi1 - u1[1] * sin_phi1)
        a1y = K1 * (u1[0] * sin_phi1 + u1[1] * cos_phi1)
        b1x = v1 * cos_phi1
        b1y = v1 * sin_phi1

    if s2 in const.nontranslating:
        a2x, a2y, b2x, b2y = 0, 0, 0, 0
    else:
        phi2 = utils.angle_fast(rvw2[1])
        v2 = np.linalg.norm(rvw2[1])

        u2 = (
            np.array([1, 0, 0])
            if s2 == const.rolling
            else utils.coordinate_rotation_fast(
                utils.unit_vector_fast(utils.get_rel_velocity_fast(rvw2, R)), -phi2
            )
        )

        K2 = -0.5 * mu2 * g2
        cos_phi2 = np.cos(phi2)
        sin_phi2 = np.sin(phi2)

        a2x = K2 * (u2[0] * cos_phi2 - u2[1] * sin_phi2)
        a2y = K2 * (u2[0] * sin_phi2 + u2[1] * cos_phi2)
        b2x = v2 * cos_phi2
        b2y = v2 * sin_phi2

    Ax, Ay = a2x - a1x, a2y - a1y
    Bx, By = b2x - b1x, b2y - b1y
    Cx, Cy = c2x - c1x, c2y - c1y

    a = Ax**2 + Ay**2
    b = 2 * Ax * Bx + 2 * Ay * By
    c = Bx**2 + 2 * Ax * Cx + 2 * Ay * Cy + By**2
    d = 2 * Bx * Cx + 2 * By * Cy
    e = Cx**2 + Cy**2 - 4 * R**2

    return a, b, c, d, e


@jit(nopython=True, cache=const.numba_cache)
def get_ball_ball_collision_coeffs_fast(
    rvw1, rvw2, s1, s2, mu1, mu2, m1, m2, g1, g2, R
):
    """Get quartic coeffs required to determine the ball-ball collision time

    (just-in-time compiled)

    Notes
    =====
    - Speed comparison in pooltool/tests/speed/get_ball_ball_collision_coeffs.py
    """

    c1x, c1y = rvw1[0, 0], rvw1[0, 1]
    c2x, c2y = rvw2[0, 0], rvw2[0, 1]

    if s1 == const.spinning or s1 == const.pocketed or s1 == const.stationary:
        a1x, a1y, b1x, b1y = 0, 0, 0, 0
    else:
        phi1 = utils.angle_fast(rvw1[1])
        v1 = np.linalg.norm(rvw1[1])

        u1 = (
            np.array([1, 0, 0], dtype=np.float64)
            if s1 == const.rolling
            else utils.coordinate_rotation_fast(
                utils.unit_vector_fast(utils.get_rel_velocity_fast(rvw1, R)), -phi1
            )
        )

        K1 = -0.5 * mu1 * g1
        cos_phi1 = np.cos(phi1)
        sin_phi1 = np.sin(phi1)

        a1x = K1 * (u1[0] * cos_phi1 - u1[1] * sin_phi1)
        a1y = K1 * (u1[0] * sin_phi1 + u1[1] * cos_phi1)
        b1x = v1 * cos_phi1
        b1y = v1 * sin_phi1

    if s2 == const.spinning or s2 == const.pocketed or s2 == const.stationary:
        a2x, a2y, b2x, b2y = 0.0, 0.0, 0.0, 0.0
    else:
        phi2 = utils.angle_fast(rvw2[1])
        v2 = np.linalg.norm(rvw2[1])

        u2 = (
            np.array([1, 0, 0], dtype=np.float64)
            if s2 == const.rolling
            else utils.coordinate_rotation_fast(
                utils.unit_vector_fast(utils.get_rel_velocity_fast(rvw2, R)), -phi2
            )
        )

        K2 = -0.5 * mu2 * g2
        cos_phi2 = np.cos(phi2)
        sin_phi2 = np.sin(phi2)

        a2x = K2 * (u2[0] * cos_phi2 - u2[1] * sin_phi2)
        a2y = K2 * (u2[0] * sin_phi2 + u2[1] * cos_phi2)
        b2x = v2 * cos_phi2
        b2y = v2 * sin_phi2

    Ax, Ay = a2x - a1x, a2y - a1y
    Bx, By = b2x - b1x, b2y - b1y
    Cx, Cy = c2x - c1x, c2y - c1y

    a = Ax**2 + Ay**2
    b = 2 * Ax * Bx + 2 * Ay * By
    c = Bx**2 + 2 * Ax * Cx + 2 * Ay * Cy + By**2
    d = 2 * Bx * Cx + 2 * By * Cy
    e = Cx**2 + Cy**2 - 4 * R**2

    return a, b, c, d, e


def get_ball_ball_collision_time(rvw1, rvw2, s1, s2, mu1, mu2, m1, m2, g1, g2, R):
    """Get the time until collision between 2 balls

    NOTE This is deprecated. Rather than solve the roots of a single polynomial
    equation, as is done in this function, all roots of a given collision class are
    solved simultaneously via utils.roots
    """
    a, b, c, d, e = get_ball_ball_collision_coeffs(
        rvw1, rvw2, s1, s2, mu1, mu2, m1, m2, g1, g2, R
    )
    roots = np.roots([a, b, c, d, e])

    roots = roots[(abs(roots.imag) <= const.tol) & (roots.real > const.tol)].real

    return roots.min() if len(roots) else np.inf


@jit(nopython=True, cache=const.numba_cache)
def skip_ball_linear_cushion_collision(rvw, s, u_r, g, R, p1, p2, normal):
    if s == const.spinning or s == const.pocketed or s == const.stationary:
        # Ball isn't moving. No collision.
        return True

    if s == const.rolling:
        # Since the ball is rolling, it is a straight line trajectory. The strategy here
        # is to see whether the trajectory of the ball is going to intersect with either
        # of the collisions defined by a linear cushion segment. Let r1 be the position
        # of the ball and r2 be the final position of the ball (rolling to a stop). Let
        # p11 and p21 be the intersection points of the first intersection line, and let
        # p12 and p22 be the intersection points of the second. This code uses
        # orientation to determine if If r1 -> r2 intersects p11 -> p21 or p12 -> p22
        p11 = p1 + R * normal
        p12 = p1 - R * normal
        p21 = p2 + R * normal
        p22 = p2 - R * normal

        t = np.linalg.norm(rvw[1]) / (u_r * g)
        v_0_hat = utils.unit_vector_fast(rvw[1])
        r1 = rvw[0]
        r2 = r1 + rvw[1] * t - 0.5 * u_r * g * t**2 * v_0_hat

        o1 = utils.orientation(r1, r2, p11)
        o2 = utils.orientation(r1, r2, p21)
        o3 = utils.orientation(p11, p21, r1)
        o4 = utils.orientation(p11, p21, r2)
        # Whether or not trajectory intersects with first intersection line
        int1 = (o1 != o2) and (o3 != o4)

        o1 = utils.orientation(r1, r2, p12)
        o2 = utils.orientation(r1, r2, p22)
        o3 = utils.orientation(p12, p22, r1)
        o4 = utils.orientation(p12, p22, r2)
        # Whether or not trajectory intersects with first intersection line
        int2 = (o1 != o2) and (o3 != o4)

        if not int1 and not int2:
            return True

    return False


def get_ball_linear_cushion_collision_time(rvw, s, lx, ly, l0, p1, p2, mu, m, g, R):
    """Get the time until collision between ball and linear cushion segment"""
    if s in const.nontranslating:
        return np.inf

    phi = utils.angle_fast(rvw[1])
    v = np.linalg.norm(rvw[1])

    u = np.array(
        [1, 0, 0]
        if s == const.rolling
        else utils.coordinate_rotation_fast(
            utils.unit_vector_fast(utils.get_rel_velocity_fast(rvw, R)), -phi
        )
    )

    ax = -0.5 * mu * g * (u[0] * np.cos(phi) - u[1] * np.sin(phi))
    ay = -0.5 * mu * g * (u[0] * np.sin(phi) + u[1] * np.cos(phi))
    bx, by = v * np.cos(phi), v * np.sin(phi)
    cx, cy = rvw[0, 0], rvw[0, 1]

    A = lx * ax + ly * ay
    B = lx * bx + ly * by
    C1 = l0 + lx * cx + ly * cy + R * np.sqrt(lx**2 + ly**2)
    C2 = l0 + lx * cx + ly * cy - R * np.sqrt(lx**2 + ly**2)

    root1, root2 = utils.quadratic_fast(A, B, C1)
    root3, root4 = utils.quadratic_fast(A, B, C2)
    roots = np.array(
        [
            root1,
            root2,
            root3,
            root4,
        ]
    )

    roots = roots[(abs(roots.imag) <= const.tol) & (roots.real > const.tol)].real

    # All roots beyond this point are real and positive

    for i, root in enumerate(roots):
        rvw_dtau, _ = evolve_state_motion(s, rvw, R, m, mu, 1, mu, g, root)
        s_score = -np.dot(p1 - rvw_dtau[0], p2 - p1) / np.dot(p2 - p1, p2 - p1)
        if not (0 <= s_score <= 1):
            roots[i] = np.inf

    return roots.min() if len(roots) else np.inf


@jit(nopython=True, cache=const.numba_cache)
def get_ball_linear_cushion_collision_time_fast(
    rvw, s, lx, ly, l0, p1, p2, direction, mu, m, g, R
):
    """Get time until collision between ball and linear cushion segment

    (just-in-time compiled)

    Notes
    =====
    - Speed comparison in
      pooltool/tests/speed/get_ball_circular_cushion_collision_coeffs.py
    """
    if s == const.spinning or s == const.pocketed or s == const.stationary:
        return np.inf

    phi = utils.angle_fast(rvw[1])
    v = np.linalg.norm(rvw[1])

    u = (
        np.array([1, 0, 0], dtype=np.float64)
        if s == const.rolling
        else utils.coordinate_rotation_fast(
            utils.unit_vector_fast(utils.get_rel_velocity_fast(rvw, R)), -phi
        )
    )

    K = -0.5 * mu * g
    cos_phi = np.cos(phi)
    sin_phi = np.sin(phi)

    ax = K * (u[0] * cos_phi - u[1] * sin_phi)
    ay = K * (u[0] * sin_phi + u[1] * cos_phi)
    bx, by = v * cos_phi, v * sin_phi
    cx, cy = rvw[0, 0], rvw[0, 1]

    A = lx * ax + ly * ay
    B = lx * bx + ly * by

    if direction == 0:
        C = l0 + lx * cx + ly * cy + R * np.sqrt(lx**2 + ly**2)
        root1, root2 = utils.quadratic_fast(A, B, C)
        roots = [root1, root2]
    elif direction == 1:
        C = l0 + lx * cx + ly * cy - R * np.sqrt(lx**2 + ly**2)
        root1, root2 = utils.quadratic_fast(A, B, C)
        roots = [root1, root2]
    else:
        C1 = l0 + lx * cx + ly * cy + R * np.sqrt(lx**2 + ly**2)
        C2 = l0 + lx * cx + ly * cy - R * np.sqrt(lx**2 + ly**2)
        root1, root2 = utils.quadratic_fast(A, B, C1)
        root3, root4 = utils.quadratic_fast(A, B, C2)
        roots = [root1, root2, root3, root4]

    min_time = np.inf
    for root in roots:
        if np.abs(root.imag) > const.tol:
            continue

        if root.real <= const.tol:
            continue

        rvw_dtau, _ = evolve_state_motion(s, rvw, R, m, mu, 1, mu, g, root)
        s_score = -np.dot(p1 - rvw_dtau[0], p2 - p1) / np.dot(p2 - p1, p2 - p1)

        if not (0 <= s_score <= 1):
            continue

        if root.real < min_time:
            min_time = root.real

    return min_time


def get_ball_circular_cushion_collision_coeffs(rvw, s, a, b, r, mu, m, g, R):
    """Get quartic coeffs required to determine the ball-circular-cushion collision time

    Parameters
    ==========
    a : float
        The x-coordinate of the cushion segment's center
    b : float
        The y-coordinate of the cushion segment's center
    r : float
        The radius of the cushion segment's center
    mu : float
        The rolling or sliding coefficient of friction. Should match the value of s
    """

    if s in const.nontranslating:
        return np.inf, np.inf, np.inf, np.inf, np.inf

    phi = utils.angle_fast(rvw[1])
    v = np.linalg.norm(rvw[1])

    u = np.array(
        [1, 0, 0]
        if s == const.rolling
        else utils.coordinate_rotation_fast(
            utils.unit_vector_fast(utils.get_rel_velocity_fast(rvw, R)), -phi
        )
    )

    K = -0.5 * mu * g
    cos_phi = np.cos(phi)
    sin_phi = np.sin(phi)

    ax = K * (u[0] * cos_phi - u[1] * sin_phi)
    ay = K * (u[0] * sin_phi + u[1] * cos_phi)
    bx, by = v * cos_phi, v * sin_phi
    cx, cy = rvw[0, 0], rvw[0, 1]

    A = 0.5 * (ax**2 + ay**2)
    B = ax * bx + ay * by
    C = ax * (cx - a) + ay * (cy - b) + 0.5 * (bx**2 + by**2)
    D = bx * (cx - a) + by * (cy - b)
    E = 0.5 * (a**2 + b**2 + cx**2 + cy**2 - (r + R) ** 2) - (cx * a + cy * b)

    return A, B, C, D, E


@jit(nopython=True, cache=const.numba_cache)
def get_ball_circular_cushion_collision_coeffs_fast(rvw, s, a, b, r, mu, m, g, R):
    """Get quartic coeffs required to determine the ball-circular-cushion collision time

    (just-in-time compiled)

    Notes
    =====
    - Speed comparison in
      pooltool/tests/speed/get_ball_circular_cushion_collision_coeffs.py
    """

    if s == const.spinning or s == const.pocketed or s == const.stationary:
        return np.inf, np.inf, np.inf, np.inf, np.inf

    phi = utils.angle_fast(rvw[1])
    v = np.linalg.norm(rvw[1])

    u = (
        np.array([1, 0, 0], dtype=np.float64)
        if s == const.rolling
        else utils.coordinate_rotation_fast(
            utils.unit_vector_fast(utils.get_rel_velocity_fast(rvw, R)), -phi
        )
    )

    K = -0.5 * mu * g
    cos_phi = np.cos(phi)
    sin_phi = np.sin(phi)

    ax = K * (u[0] * cos_phi - u[1] * sin_phi)
    ay = K * (u[0] * sin_phi + u[1] * cos_phi)
    bx, by = v * cos_phi, v * sin_phi
    cx, cy = rvw[0, 0], rvw[0, 1]

    A = 0.5 * (ax**2 + ay**2)
    B = ax * bx + ay * by
    C = ax * (cx - a) + ay * (cy - b) + 0.5 * (bx**2 + by**2)
    D = bx * (cx - a) + by * (cy - b)
    E = 0.5 * (a**2 + b**2 + cx**2 + cy**2 - (r + R) ** 2) - (cx * a + cy * b)

    return A, B, C, D, E


def get_ball_circular_cushion_collision_time(rvw, s, a, b, r, mu, m, g, R):
    """Get the time until collision between ball and circular cushion segment

    NOTE This is deprecated. Rather than solve the roots of a single polynomial
    equation, as is done in this function, all roots of a given collision class are
    solved simultaneously via utils.roots

    Parameters
    ==========
    a : float
        The x-coordinate of the cushion segment's center
    b : float
        The y-coordinate of the cushion segment's center
    r : float
        The radius of the cushion segment's center
    mu : float
        The rolling or sliding coefficient of friction. Should match the value of s
    """
    A, B, C, D, E = get_ball_circular_cushion_collision_coeffs(
        rvw, s, a, b, r, mu, m, g, R
    )
    roots = np.roots([A, B, C, D, E])

    roots = roots[(abs(roots.imag) <= const.tol) & (roots.real > const.tol)].real

    return roots.min() if len(roots) else np.inf


def get_ball_pocket_collision_coeffs(rvw, s, a, b, r, mu, m, g, R):
    """Get the quartic coeffs required to determine the ball-pocket collision time

    Parameters
    ==========
    a : float
        The x-coordinate of the pocket's center
    b : float
        The y-coordinate of the pocket's center
    r : float
        The radius of the pocket's center
    mu : float
        The rolling or sliding coefficient of friction. Should match the value of s
    """

    if s in const.nontranslating:
        return np.inf, np.inf, np.inf, np.inf, np.inf

    phi = utils.angle_fast(rvw[1])
    v = np.linalg.norm(rvw[1])

    u = (
        np.array([1, 0, 0])
        if s == const.rolling
        else utils.coordinate_rotation_fast(
            utils.unit_vector_fast(utils.get_rel_velocity_fast(rvw, R)), -phi
        )
    )

    K = -0.5 * mu * g
    cos_phi = np.cos(phi)
    sin_phi = np.sin(phi)

    ax = K * (u[0] * cos_phi - u[1] * sin_phi)
    ay = K * (u[0] * sin_phi + u[1] * cos_phi)
    bx, by = v * cos_phi, v * sin_phi
    cx, cy = rvw[0, 0], rvw[0, 1]

    A = 0.5 * (ax**2 + ay**2)
    B = ax * bx + ay * by
    C = ax * (cx - a) + ay * (cy - b) + 0.5 * (bx**2 + by**2)
    D = bx * (cx - a) + by * (cy - b)
    E = 0.5 * (a**2 + b**2 + cx**2 + cy**2 - r**2) - (cx * a + cy * b)

    return A, B, C, D, E


@jit(nopython=True, cache=const.numba_cache)
def get_ball_pocket_collision_coeffs_fast(rvw, s, a, b, r, mu, m, g, R):
    """Get quartic coeffs required to determine the ball-pocket collision time

    (just-in-time compiled)

    Notes
    =====
    - Speed comparison in
      pooltool/tests/speed/get_ball_circular_cushion_collision_coeffs.py
    """

    if s == const.spinning or s == const.pocketed or s == const.stationary:
        return np.inf, np.inf, np.inf, np.inf, np.inf

    phi = utils.angle_fast(rvw[1])
    v = np.linalg.norm(rvw[1])

    u = (
        np.array([1, 0, 0], dtype=np.float64)
        if s == const.rolling
        else utils.coordinate_rotation_fast(
            utils.unit_vector_fast(utils.get_rel_velocity_fast(rvw, R)), -phi
        )
    )

    K = -0.5 * mu * g
    cos_phi = np.cos(phi)
    sin_phi = np.sin(phi)

    ax = K * (u[0] * cos_phi - u[1] * sin_phi)
    ay = K * (u[0] * sin_phi + u[1] * cos_phi)
    bx, by = v * cos_phi, v * sin_phi
    cx, cy = rvw[0, 0], rvw[0, 1]

    A = 0.5 * (ax**2 + ay**2)
    B = ax * bx + ay * by
    C = ax * (cx - a) + ay * (cy - b) + 0.5 * (bx**2 + by**2)
    D = bx * (cx - a) + by * (cy - b)
    E = 0.5 * (a**2 + b**2 + cx**2 + cy**2 - r**2) - (cx * a + cy * b)

    return A, B, C, D, E


def get_ball_pocket_collision_time(rvw, s, a, b, r, mu, m, g, R):
    """Get the time until collision between ball and pocket

    NOTE This is deprecated. Rather than solve the roots of a single polynomial
    equation, as is done in this function, all roots of a given collision class are
    solved simultaneously via utils.roots

    Parameters
    ==========
    a : float
        The x-coordinate of the pocket's center
    b : float
        The y-coordinate of the pocket's center
    r : float
        The radius of the pocket's center
    mu : float
        The rolling or sliding coefficient of friction. Should match the value of s
    """

    A, B, C, D, E = get_ball_pocket_collision_coeffs(rvw, s, a, b, r, mu, m, g, R)
    roots = np.roots([A, B, C, D, E])

    roots = roots[(abs(roots.imag) <= const.tol) & (roots.real > const.tol)].real

    return roots.min() if len(roots) else np.inf


def get_slide_time(rvw, R, u_s, g):
    return 2 * np.linalg.norm(utils.get_rel_velocity_fast(rvw, R)) / (7 * u_s * g)


def get_roll_time(rvw, u_r, g):
    _, v, _ = rvw
    return np.linalg.norm(v) / (u_r * g)


def get_spin_time(rvw, R, u_sp, g):
    _, _, w = rvw
    return np.abs(w[2]) * 2 / 5 * R / u_sp / g


@jit(nopython=True, cache=const.numba_cache)
def get_slide_time_fast(rvw, R, u_s, g):
    return 2 * np.linalg.norm(utils.get_rel_velocity_fast(rvw, R)) / (7 * u_s * g)


@jit(nopython=True, cache=const.numba_cache)
def get_roll_time_fast(rvw, u_r, g):
    _, v, _ = rvw
    return np.linalg.norm(v) / (u_r * g)


@jit(nopython=True, cache=const.numba_cache)
def get_spin_time_fast(rvw, R, u_sp, g):
    _, _, w = rvw
    return np.abs(w[2]) * 2 / 5 * R / u_sp / g


def get_ball_energy(rvw, R, m):
    """Get the energy of a ball

    Currently calculating linear and rotational kinetic energy. Need to add potential
    energy if z-axis is freed
    """
    # Linear
    LKE = m * np.linalg.norm(rvw[1]) ** 2 / 2

    # Rotational
    I = 2 / 5 * m * R**2
    RKE = I * np.linalg.norm(rvw[2]) ** 2 / 2

    return LKE + RKE


@jit(nopython=True, cache=const.numba_cache)
def evolve_ball_motion(state, rvw, R, m, u_s, u_sp, u_r, g, t):
    if state == const.stationary or state == const.pocketed:
        return rvw, state

    if state == const.sliding:
        dtau_E_slide = get_slide_time_fast(rvw, R, u_s, g)

        if t >= dtau_E_slide:
            rvw = evolve_slide_state(rvw, R, m, u_s, u_sp, g, dtau_E_slide)
            state = const.rolling
            t -= dtau_E_slide
        else:
            return evolve_slide_state(rvw, R, m, u_s, u_sp, g, t), const.sliding

    if state == const.rolling:
        dtau_E_roll = get_roll_time_fast(rvw, u_r, g)

        if t >= dtau_E_roll:
            rvw = evolve_roll_state(rvw, R, u_r, u_sp, g, dtau_E_roll)
            state = const.spinning
            t -= dtau_E_roll
        else:
            return evolve_roll_state(rvw, R, u_r, u_sp, g, t), const.rolling

    if state == const.spinning:
        dtau_E_spin = get_spin_time_fast(rvw, R, u_sp, g)

        if t >= dtau_E_spin:
            return (
                evolve_perpendicular_spin_state(rvw, R, u_sp, g, dtau_E_spin),
                const.stationary,
            )
        else:
            return evolve_perpendicular_spin_state(rvw, R, u_sp, g, t), const.spinning


@jit(nopython=True, cache=const.numba_cache)
def evolve_state_motion(state, rvw, R, m, u_s, u_sp, u_r, g, t):
    """Variant of evolve_ball_motion that does not respect motion transition events"""
    if state == const.stationary or state == const.pocketed:
        return rvw, state
    elif state == const.sliding:
        return evolve_slide_state(rvw, R, m, u_s, u_sp, g, t), const.sliding
    elif state == const.rolling:
        return evolve_roll_state(rvw, R, u_r, u_sp, g, t), const.rolling
    elif state == const.spinning:
        return evolve_perpendicular_spin_state(rvw, R, u_sp, g, t), const.spinning


@jit(nopython=True, cache=const.numba_cache)
def evolve_slide_state(rvw, R, m, u_s, u_sp, g, t):
    if t == 0:
        return rvw

    # Angle of initial velocity in table frame
    phi = utils.angle_fast(rvw[1])

    rvw_B0 = utils.coordinate_rotation_fast(rvw.T, -phi).T

    # Relative velocity unit vector in ball frame
    u_0 = utils.coordinate_rotation_fast(
        utils.unit_vector_fast(utils.get_rel_velocity_fast(rvw, R)), -phi
    )

    # Calculate quantities according to the ball frame. NOTE w_B in this code block
    # is only accurate of the x and y evolution of angular velocity. z evolution of
    # angular velocity is done in the next block

    rvw_B = np.empty((3, 3), dtype=np.float64)
    rvw_B[0, 0] = rvw_B0[1, 0] * t - 0.5 * u_s * g * t**2 * u_0[0]
    rvw_B[0, 1] = -0.5 * u_s * g * t**2 * u_0[1]
    rvw_B[0, 2] = 0
    rvw_B[1, :] = rvw_B0[1] - u_s * g * t * u_0
    rvw_B[2, :] = rvw_B0[2] - 5 / 2 / R * u_s * g * t * utils.cross_fast(
        u_0, np.array([0, 0, 1], dtype=np.float64)
    )

    # This transformation governs the z evolution of angular velocity
    rvw_B[2, 2] = rvw_B0[2, 2]
    rvw_B = evolve_perpendicular_spin_state(rvw_B, R, u_sp, g, t)

    # Rotate to table reference
    rvw_T = utils.coordinate_rotation_fast(rvw_B.T, phi).T
    rvw_T[0] += rvw[0]  # Add initial ball position

    return rvw_T


@jit(nopython=True, cache=const.numba_cache)
def evolve_roll_state(rvw, R, u_r, u_sp, g, t):
    if t == 0:
        return rvw

    r_0, v_0, w_0 = rvw

    v_0_hat = utils.unit_vector_fast(v_0)

    r = r_0 + v_0 * t - 0.5 * u_r * g * t**2 * v_0_hat
    v = v_0 - u_r * g * t * v_0_hat
    w = utils.coordinate_rotation_fast(v / R, np.pi / 2)

    # Independently evolve the z spin
    temp = evolve_perpendicular_spin_state(rvw, R, u_sp, g, t)

    w[2] = temp[2, 2]

    new_rvw = np.empty((3, 3), dtype=np.float64)
    new_rvw[0, :] = r
    new_rvw[1, :] = v
    new_rvw[2, :] = w

    return new_rvw


@jit(nopython=True, cache=const.numba_cache)
def evolve_perpendicular_spin_component(wz, R, u_sp, g, t):
    if t == 0:
        return wz

    if np.abs(wz) < const.tol:
        return wz

    alpha = 5 * u_sp * g / (2 * R)

    if t > np.abs(wz) / alpha:
        # You can't decay past 0 angular velocity
        t = np.abs(wz) / alpha

    # Always decay towards 0, whether spin is +ve or -ve
    sign = 1 if wz > 0 else -1

    wz_final = wz - sign * alpha * t
    return wz_final


@jit(nopython=True, cache=const.numba_cache)
def evolve_perpendicular_spin_state(rvw, R, u_sp, g, t):
    # Otherwise ball.state.rvw will be modified and corresponding entry in self.history
    # FIXME framework has changed, this may not be true. EDIT This is still true.
    rvw = rvw.copy()

    rvw[2, 2] = evolve_perpendicular_spin_component(rvw[2, 2], R, u_sp, g, t)
    return rvw


def cue_strike(m, M, R, V0, phi, theta, a, b):
    """Strike a ball
                              , - ~  ,
    ◎───────────◎         , '          ' ,
    │           │       ,             ◎    ,
    │      /    │      ,              │     ,
    │     /     │     ,               │ b    ,
    ◎    / phi  ◎     ,           ────┘      ,
    │   /___    │     ,            -a        ,
    │           │      ,                    ,
    │           │       ,                  ,
    ◎───────────◎         ,               '
      bottom cushion        ' - , _ , -
                     ______________________________
                              playing surface
    Parameters
    ==========

    m : positive float
        ball mass

    M : positive float
        cue mass

    R : positive, float
        ball radius

    V0 : positive float
        What initial velocity does the cue strike the ball?

    phi : float (degrees)
        The direction you strike the ball in relation to the bottom cushion

    theta : float (degrees)
        How elevated is the cue from the playing surface, in degrees?

    a : float
        How much side english should be put on? -1 being rightmost side of ball, +1
        being leftmost side of ball

    b : float
        How much vertical english should be put on? -1 being bottom-most side of ball,
        +1 being topmost side of ball

    Notes
    =====
    - This function creates unrealistic magnitudes of spin. To compensate, I've got a
      fake factor that scales down the passed a and b values, called
      pooltool.english_fraction

    """

    a *= R * const.english_fraction
    b *= R * const.english_fraction

    phi *= np.pi / 180
    theta *= np.pi / 180

    I = 2 / 5 * m * R**2

    c = np.sqrt(R**2 - a**2 - b**2)

    # Calculate impact force F.  In Leckie & Greenspan, the mass term in numerator is
    # ball mass, which seems wrong.  See
    # https://billiards.colostate.edu/faq/cue-tip/force/
    numerator = 2 * M * V0
    temp = (
        a**2
        + (b * np.cos(theta)) ** 2
        + (c * np.cos(theta)) ** 2
        - 2 * b * c * np.cos(theta) * np.sin(theta)
    )
    denominator = 1 + m / M + 5 / 2 / R**2 * temp
    F = numerator / denominator

    # 3D FIXME
    # v_B = -F/m * np.array([0, np.cos(theta), np.sin(theta)])
    v_B = -F / m * np.array([0, np.cos(theta), 0])

    vec_x = -c * np.sin(theta) + b * np.cos(theta)
    vec_y = a * np.sin(theta)
    vec_z = -a * np.cos(theta)

    vec = np.array([vec_x, vec_y, vec_z])
    w_B = F / I * vec

    # Rotate to table reference
    rot_angle = phi + np.pi / 2
    v_T = utils.coordinate_rotation_fast(v_B, rot_angle)
    w_T = utils.coordinate_rotation_fast(w_B, rot_angle)

    return v_T, w_T


def is_overlapping(rvw1, rvw2, R1, R2):
    return np.linalg.norm(rvw1[0] - rvw2[0]) < (R1 + R2)
