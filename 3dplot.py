







from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import numpy as np

# Fixing random state for reproducibility

[0.5335834565308771, -0.14942924536134222, -0.8324419472535616,134.48632082520803, 
-0.8324419472535616, -0.14942924536134222, 0.5335834565308771, 134.48632082520803, 
-0.5437668126587487, 0.6392458892334706, -0.5437668126587487, 134.48632082520803, 
0.2449083219360642, -0.9381043799561553, 0.2449083219360642, 134.48632082520805, 
-0.5773502691896257, -0.5773502691896257, -0.5773502691896257, 519.6052422706631, 
0.5773502691896257, 0.5773502691896257, 0.5773502691896257, 480.39475773472185]


0.9659258262890683, -0.1830127018922193, -0.1830127018922193, 109.80762113533157,  left 
-0.9659258262890683, -0.1830127018922193, -0.1830127018922193, 109.80762113533157, right
1.0255800994045673e-17, 0.5, -0.8660254037844386, 109.80762113533157, bottom
-5.921189464667501e-18, -0.8660254037844386, 0.5, 109.80762113533157, top
8.373826446313468e-18, -0.7071067811865476, -0.7071067811865476, 424.2540687119285, 
-8.373826446287789e-18, 0.7071067811865476, 0.7071067811865476, 575.7459312940788

xs = []
ys = []
zs = []

#for n in range(8):
    #xs.append(points[3*n])
    #ys.append(points[3*n+1])
    #zs.append(points[3*n+2])

for n in range(8):
    xs.append(points[n])
for n in range(8,16):
    ys.append(points[n])
for n in range(16,24):
    zs.append(points[n])


def randrange(n, vmin, vmax):
    '''
    Helper function to make an array of random numbers having shape (n, )
    with each number distributed Uniform(vmin, vmax).
    '''
    return (vmax - vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')



# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
for m, zlow, zhigh in [('o', -50, -25), ('^', -30, -5)]:
    ax.scatter(xs, ys, zs, marker=m)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
ax.set_xlim(0, 600)
ax.set_ylim(0, 600)
ax.set_zlim(0, 600)

plt.show()