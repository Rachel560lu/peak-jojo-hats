"""One continuous pompadour envelope: forehead roll, crown and skull share topology."""
import math
import numpy as np


# Rows: t, lateral radius, front radius, rear radius, front/side/rear height.
# The forward lip curls down into the hairline; the rear declines into the skull.
PROFILE = np.array([
    [0.00, 0.00, 0.00, 0.00, 1.84, 1.84, 1.84],
    [0.20, 0.56, 0.70, 0.48, 1.97, 1.82, 1.74],
    [0.40, 1.03, 1.33, 0.91, 1.95, 1.63, 1.39],
    [0.60, 1.31, 1.69, 1.24, 1.68, 1.27, 0.87],
    [0.80, 1.44, 1.62, 1.43, 1.19, 0.76, 0.10],
    [1.00, 1.45, 1.24, 1.11, 0.75, 0.06,-0.99],
], dtype=float)


def profile(t):
    """C1 cubic interpolation makes adjacent loft sections tangent-continuous."""
    x = min(4.999999999, max(0, t * 5))
    i = int(x); f = x - i
    rows = PROFILE[:, 1:]
    p, q = rows[i], rows[i + 1]
    before = rows[i - 1] if i else 2 * p - q
    after = rows[i + 2] if i < 4 else 2 * q - p
    dp = (q - before) * .5; dq = (after - p) * .5
    return (2*f**3-3*f**2+1)*p + (f**3-2*f**2+f)*dp + (-2*f**3+3*f**2)*q + (f**3-f**2)*dq


def point(a, t):
    rx, front, back, zf, zs, zb = profile(t)
    ca, sa = math.cos(a), math.sin(a)
    def rounded(v):
        return v * ((v*v+.04)/1.04)**(-.075)
    def blend(v, exponent):
        return ((v*v+.04)**(exponent*.5)-.04**(exponent*.5))/(1.04**(exponent*.5)-.04**(exponent*.5))
    x = rx * rounded(sa)
    y = (front if ca >= 0 else back) * rounded(ca)
    z = zs + (zf-zs if ca >= 0 else zb-zs) * blend(ca,.55 if ca >= 0 else 1.3)
    # A loft between unequal-height rings can cut through the spherical head.
    # Smooth radial clearance prevents this without an extra hidden scalp shell.
    p = np.array([x, y, z]); radius = np.linalg.norm(p)
    delta = radius - 1.465
    target = .5 * (radius + 1.465 + math.sqrt(delta*delta + .012**2))
    x, y, z = p * (target / radius)
    # Low relief is sculpted into the SAME surface, never separate oval tubes.
    # Front ridges roll over the lip; rear comb marks are much shallower.
    fade = math.sin(math.pi*t)**.8
    fore = max(0, ca)**.7
    crest = (.5 + .5*math.cos(12*math.pi*x/1.45 + .25*y))**3
    back_crest = (.5 + .5*math.cos(math.tau*(t*4.3 + .18*abs(sa))))**4
    h = fade * (.060*fore*crest + .019*(1-fore)*back_crest)
    radial = np.array([x/1.45**2, y/1.48**2, max(.03, z)/1.84**2])
    radial /= max(np.linalg.norm(radial), 1e-9)
    return np.array([x, y, z]) + radial*h


def build(m):
    m.part()
    # Dense around azimuth for shallow ridges, not extra piled components.
    around, rings = 144, 56
    grid = [[point(i*math.tau/around, j/rings) for i in range(around)] for j in range(rings+1)]
    for j in range(rings):
        for i in range(around):
            k = (i+1) % around
            m.face([grid[j][i], grid[j][k], grid[j+1][k], grid[j+1][i]], 25)
    return m
