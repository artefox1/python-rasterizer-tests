import pygame
from pygame.locals import *
import sys

from PIL.Image import open as openim, Image

TILESIZE = 16
TILESX = 64
TILESY = 64
STEPSIZE = 0.4
SAMPLESCALE = 5
RADIUS = 1

# Courtesy of artefox
def triangle(p0, p1, p2, color, arr):
    v0, v1, v2 = p0, p1, p2
    if v0[1] > v1[1]:
        v0, v1 = v1, v0
    if v1[1] > v2[1]:
        v1, v2 = v2, v1
    if v0[1] > v1[1]:
        v0, v1 = v1, v0

    # Deltas
    dx_01 = v1[0] - v0[0]
    dy_01 = v1[1] - v0[1]
    dx_02 = v2[0] - v0[0]
    dy_02 = v2[1] - v0[1]
    dx_12 = v2[0] - v1[0]
    dy_12 = v2[1] - v1[1]

    # Deltas for colors
    dr_01 = v1[2] - v0[2]
    dg_01 = v1[3] - v0[3]
    db_01 = v1[4] - v0[4]
    dr_02 = v2[2] - v0[2]
    dg_02 = v2[3] - v0[3]
    db_02 = v2[4] - v0[4]
    dr_12 = v2[2] - v1[2]
    dg_12 = v2[3] - v1[3]
    db_12 = v2[4] - v1[4]

    # Slopes dx/dy
    step_01 = dx_01 / dy_01 if dy_01 != 0 else float('inf')
    step_02 = dx_02 / dy_02 if dy_02 != 0 else float('inf')
    step_12 = dx_12 / dy_12 if dy_12 != 0 else float('inf')

    # Slopes for colors
    step_r_01 = dr_01 / dy_01 if dy_01 != 0 else 0
    step_g_01 = dg_01 / dy_01 if dy_01 != 0 else 0
    step_b_01 = db_01 / dy_01 if dy_01 != 0 else 0
    step_r_02 = dr_02 / dy_02 if dy_02 != 0 else 0
    step_g_02 = dg_02 / dy_02 if dy_02 != 0 else 0
    step_b_02 = db_02 / dy_02 if dy_02 != 0 else 0
    step_r_12 = dr_12 / dy_12 if dy_12 != 0 else 0
    step_g_12 = dg_12 / dy_12 if dy_12 != 0 else 0
    step_b_12 = db_12 / dy_12 if dy_12 != 0 else 0

    x0, x1 = float(v0[0]), float(v0[0])
    r0, g0, b0, r1, g1, b1 = float(v0[2]), float(v0[3]), float(v0[4]), float(v0[2]), float(v0[3]), float(v0[4])
    short = step_01 > step_02 # 0 is left, 1 is right

    if v0[1] != v1[1]:
        for y in range(v0[1], v1[1]):
            x_step_r = (r1 - r0) / (x1 - x0) if x1 != x0 else 0
            x_step_g = (g1 - g0) / (x1 - x0) if x1 != x0 else 0
            x_step_b = (b1 - b0) / (x1 - x0) if x1 != x0 else 0
            r = r0
            g = g0
            b = b0

            for x in range(int(x0), int(x1)):
                arr[y][x] = (r, g, b)
                r += x_step_r
                g += x_step_g
                b += x_step_b
            if short:
                x0 += step_02
                x1 += step_01

                r0 += step_r_02
                g0 += step_g_02
                b0 += step_b_02
                r1 += step_r_01
                g1 += step_g_01
                b1 += step_b_01
            else:
                x0 += step_01
                x1 += step_02

                r0 += step_r_01
                g0 += step_g_01
                b0 += step_b_01
                r1 += step_r_02
                g1 += step_g_02
                b1 += step_b_02
    else:
        x1 = float(v1[0])
        if x0 > x1:
            x0, x1 = x1, x0
            r0, r1 = r1, r0
            g0, g1 = g1, g0
            b0, b1 = b1, b0
            short = False
    
    if short:
        x1 = float(v1[0])
    else:
        x0 = float(v1[0])

    if v1[1] != v2[1]:
        for y in range(v1[1], v2[1]):
            x_step_r = (r1 - r0) / (x1 - x0) if x1 != x0 else 0
            x_step_g = (g1 - g0) / (x1 - x0) if x1 != x0 else 0
            x_step_b = (b1 - b0) / (x1 - x0) if x1 != x0 else 0
            r = r0
            g = g0
            b = b0

            for x in range(int(x0), int(x1)):
                arr[y][x] = (r, g, b)
                r += x_step_r
                g += x_step_g
                b += x_step_b
            if short:
                x0 += step_02
                x1 += step_12

                r0 += step_r_02
                g0 += step_g_02
                b0 += step_b_02
                r1 += step_r_12
                g1 += step_g_12
                b1 += step_b_12
            else:
                x0 += step_12
                x1 += step_02

                r0 += step_r_12
                g0 += step_g_12
                b0 += step_b_12
                r1 += step_r_02
                g1 += step_g_02
                b1 += step_b_02
    return arr

def contrast(x):
    return -30*(x/15)**3+45*(x/15)**2

def saturate(x):
    return 15-(x-15)**2/15

def identity(x):
    return x

def iterate(fn, n):
    def inner(x):
        for i in range(n):
            x = fn(x)
        return x
    return inner

def chain(a, b):
    def inner(x):
        return a(b(x))
    return inner

def imtoarr(path):
    arr = [[(0, 0, 0) for i in range(TILESX)] for j in range(TILESY)]
    with openim(path) as im:
        im: Image
        xs, ys = im.size
        for x in range(TILESX):
            for y in range(TILESY):
                imx = int(x*(xs/TILESX))
                imy = int(y*(ys/TILESY))
                col = im.getpixel((imx, imy))
                arr[y][x] = tuple(map(lambda v: round(v/0x11), col))
    return arr

if __name__ == "__main__":
    DISPLAYSURF = pygame.display.set_mode((TILESIZE*TILESX, TILESIZE*TILESY))

    def genmaps(endpos=(60, 60)):
        pre_aa = [[(0, 0, 0) for i in range(TILESX)] for j in range(TILESY)]
        line_start = (4, 4)
        line_end = (46, 27)#endpos
        col_start = (3, 3, 3)#(9, 2, 6)
        col_end = (11, 11, 11)#(12, 14, 2)
        x1, y1 = line_start
        x2, y2 = line_end
        r1, g1, b1 = col_start
        r2, g2, b2 = col_end

        dist = ((x1-x2)**2+(y1-y2)**2)**0.5
        coeff = STEPSIZE/dist
        dx = (x2-x1)*coeff
        dy = (y2-y1)*coeff
        dr = (r2-r1)*coeff
        dg = (g2-g1)*coeff
        db = (b2-b1)*coeff
        nsteps = int(dist/STEPSIZE)
        x = x1
        y = y1
        r = r1
        g = g1
        b = b1
        for i in range(nsteps):
            realx = int(x)
            realy = int(y)
            realr = int(r)
            realg = int(g)
            realb = int(b)
            for ofsx in range(-RADIUS, RADIUS+1):
                for ofsy in range(-RADIUS, RADIUS+1):
                    pre_aa[realy+ofsy][realx+ofsx] = (realr, realg, realb)
            x += dx
            y += dy
            r += dr
            g += dg
            b += db
        pre_aa[y2][x2] = (r2, g2, b2)

        return pre_aa

    def band_processor(rproc, gproc, bproc):
        avg = lambda dataset: sum(dataset)/len(dataset)
        return lambda samplelist: (rproc(avg(samplelist[0])), gproc(avg(samplelist[1])), bproc(avg(samplelist[2])))

    def genmap(pre_aa, bp=band_processor(identity, identity, identity)):
        post_aa = [[(0, 0, 0) for i in range(TILESX)] for j in range(TILESY)]
        for y in range(TILESY-SAMPLESCALE+1):
            for x in range(TILESX-SAMPLESCALE+1):
                samples = []
                for sx in range(SAMPLESCALE):
                    for sy in range(SAMPLESCALE):
                        samples.append(pre_aa[y+sy][x+sx])
                avg = bp(list(zip(*samples)))
                post_aa[y][x] = avg
        return post_aa

    use_aa = False
    #premap = imtoarr("wafl.png")
    premap = [[(0, 0, 0) for i in range(TILESX)] for j in range(TILESY)]
    premap = triangle((3, 2, 15, 0, 0), (57, 12, 0, 15, 0), (45, 53, 0, 0, 15), None, premap)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                use_aa = not use_aa
        pre = premap#genmaps(tuple(map(lambda i: int(i/TILESIZE), pygame.mouse.get_pos())))
        post = genmap(pre)
        DISPLAYSURF.fill((0, 0, 0))
        l = post if use_aa else pre
        for y, row in enumerate(l):
            for x, col in enumerate(row):
                pygame.draw.rect(DISPLAYSURF, tuple(map(lambda v: v*0x11, col)), (x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE))
        pygame.display.update()