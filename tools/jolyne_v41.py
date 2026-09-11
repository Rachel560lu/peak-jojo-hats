"""Jolyne-only v0.4.1 braid correction, in +Y face / +Z up coordinates.

The two long strands start *inside* the upper rear hair shell. Their centerlines
follow its ellipsoid while their section changes from a low, broad gathering of
hair into a raised interwoven plait. This avoids a separate constant-depth braid
being pasted onto the curved skull. No other hairstyle parts are modified here.
"""
import math
import numpy as np


def add_braid(m, sweep, ribbon, hairpoint):
    """Replace jolyne()'s old final plait, torus and tail with this call.

    ``sweep``, ``ribbon`` and ``hairpoint`` are the existing models_v4 helpers.
    The module only appends geometry to ``m`` and uses shared colors 28, 29, 30.
    """
    def unit(v):
        v = np.asarray(v, dtype=float)
        return v / max(np.linalg.norm(v), 1e-10)

    def smooth(a, b, value):
        u = np.clip((value - a) / (b - a), 0.0, 1.0)
        return u * u * (3.0 - 2.0 * u)

    def skin_y(x, z):
        # Same ellipsoid as Jolyne's dark scalp. x/z therefore also control y;
        # the old fixed y=-1.44 left a visible gap behind the upper skull.
        return -1.46 * math.sqrt(max(.04, 1.0 - (x / 1.46)**2 - (z / 1.49)**2))

    def center(t, sign):
        z = 1.19 - 2.045 * t
        start = smooth(.12, .30, t)
        angle = 5.0 * math.pi * max(0.0, (t - .20) / .80)
        amplitude = np.interp(t, [0, .22, .55, .82, 1], [.06, .16, .145, .105, .047])
        x = sign * amplitude * ((1.0 - start) + start * math.cos(angle))
        # Roots are buried; the finished braid lifts gradually and naturally
        # continues past the rounded nape instead of plunging into the head.
        lift = np.interp(t, [0, .12, .30, .62, .84, 1], [-.022, .002, .095, .13, .17, .26])
        over_under = sign * .067 * start * math.sin(angle) * (1.0 - .32 * t)
        return np.array([x, skin_y(x, z) - lift + over_under, z])

    def strand(sign, color):
        m.part()
        rings = []
        steps, sides = 72, 8
        for j in range(steps + 1):
            t = j / steps
            p = center(t, sign)
            tangent = unit(center(min(1, t + .001), sign) - center(max(0, t - .001), sign))
            # A flattened section remains broad along the scalp and shallow
            # radially; unlike the v0.4 plait there are no capped bead segments.
            radial = unit([p[0] / 1.46**2, p[1] / 1.46**2, p[2] / 1.49**2])
            normal = unit(radial - tangent * np.dot(radial, tangent))
            across = unit(np.cross(normal, tangent))
            normal = np.cross(tangent, across)
            width = np.interp(t, [0, .07, .18, .35, .62, .84, 1], [.012, .085, .205, .158, .13, .106, .083])
            depth = np.interp(t, [0, .10, .22, .42, .78, 1], [.012, .023, .055, .070, .062, .051])
            rings.append([p + across * width * math.cos(a) + normal * depth * math.sin(a)
                          for a in np.linspace(0, math.tau, sides, endpoint=False)])
        m.face(list(reversed(rings[0])), color)
        for a, b in zip(rings, rings[1:]):
            for k in range(sides):
                m.face([a[k], a[(k + 1) % sides], b[(k + 1) % sides], b[k]], color)
        m.face(rings[-1], color)

    # A low tapered green gathering patch crosses the crown into the first
    # crossover. Unlike a standard ribbon it has a vanishing root section;
    # there is no visible blunt cap or little fork above the finished braid.
    m.part()
    patch_rings = []
    for j in range(25):
        t = j / 24
        phi = 19 + 62 * t
        p = hairpoint(180, phi, (1.46, 1.46, 1.49))
        radial = unit(p / np.array([1.46, 1.46, 1.49])**2)
        center_lift = -.025 + .04 * math.sin(math.pi * t)**.65
        p = p + radial * center_lift
        width = np.interp(t, [0, .20, .48, .74, 1], [.003, .14, .32, .27, .055])
        depth = .005 + .06 * math.sin(math.pi * t)
        patch_rings.append([p + np.array([1., 0., 0.]) * width * math.cos(a)
                            + radial * depth * math.sin(a)
                            for a in np.linspace(0, math.tau, 8, endpoint=False)])
    m.face(list(reversed(patch_rings[0])), 29)
    for a, b in zip(patch_rings, patch_rings[1:]):
        for k in range(8):
            m.face([a[k], a[(k + 1) % 8], b[(k + 1) % 8], b[k]], 29)
    m.face(patch_rings[-1], 29)
    strand(-1, 29)
    strand(1, 29)

    bottom = (center(1, -1) + center(1, 1)) * .5
    tie_axis = unit(bottom - (center(.97, -1) + center(.97, 1)) * .5)
    # Tie has a matching orientation and encloses the tapered terminal strands.
    m.torus(bottom, .128, .043, 30, normal=tie_axis, n=20, m=8)
    # Slimmer continuation leaves from *inside* the tie. A gradual bend replaces
    # the former oversized J-shaped bulb and keeps away from the scout's neck.
    x, y, z = bottom
    sweep(m, [(x, y, z + .025), (x - .10, y - .08, z - .32),
              (x + .19, y - .13, z - .54), (x + .27, y - .11, z - .35)],
          [.095, .155, .132, .006], [.058, .092, .070, .004], 29,
          normal=(0, -1, 0), steps=18, sides=10)
