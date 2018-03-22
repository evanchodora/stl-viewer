import numpy as np


'''
Code to draw lines between vertices of STL faces
 - Pass in the numpy array of vertices in form [x y z h]
 - Each row represents a point and every 3 rows represents a connected object face
 - Clip lines using a line clipping algorithm (50px within display screen)
 - Draws lines using a version of the Bresenham's Line Algorithm

Evan Chodora, 2018
echodor@clemson.edu
'''


def draw_lines(geometry, normal, camera, view, width, height):
        num_faces = int((geometry.shape[0])/3)  # Every 3 points represents a single face
        geometry = np.around(geometry)  # Round geometry values to integer values for pixel mapping
        geometry = geometry.astype(int)  # Convert geometry matrix to integers
        geometry = geometry[:, 0:2]  # Specifically pull the X and Y coordinates
        points = []
        xmin, xmax = 0 - (width - 100) / 2, 0 + (width - 100) / 2  # X extremes of the clipping region
        ymin, ymax = 0 - (height - 100) / 2, 0 + (height - 100) / 2  # Y extremes of the clipping region

        for f in range(0, num_faces):  # Loop every each face in the geometry set
                dot = np.dot(normal[f, 0:3], camera)  # Dot the outward surface normal with the camera vector

                if dot < 0.0 or view == 'wire':
                        xy = [geometry[3*(f+1)-3].tolist(), geometry[3*(f+1)-2].tolist(), geometry[3*(f+1)-1].tolist()]
                        line = [[xy[0][0], xy[0][1], xy[1][0], xy[1][1]],
                                [xy[1][0], xy[1][1], xy[2][0], xy[2][1]],
                                [xy[2][0], xy[2][1], xy[0][0], xy[0][1]]]
                        for l in [0, 1, 2]:
                                x1, y1, x2, y2 = clipping(line[l][0], line[l][1], line[l][2], line[l][3],
                                                          xmin, xmax, ymin, ymax)
                                if x1 != 9999:  # Check if line has any points within screen to even draw
                                        # Run line drawing algorithm on the 3 lines between face points
                                        points.append(line_algo(x1, y1, x2, y2))

        points = [item for sublist in points for item in sublist]  # Flatten list sets
        line_points = np.asarray(points).reshape((-1, 2))  # Reshape and convert to XY numpy array to plot
        return line_points


def line_algo(x0, y0, x1, y1):
        # Calculate line points using an adapted version of the Bresenham's Line Algorithm
        # https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
        # https://www.cs.helsinki.fi/group/goa/mallinnus/lines/bresenh.html
        coords = []
        # Determine if the line slope is steeper than 1
        steep = abs(y1-y0) > abs(x1-x0)

        if steep:  # Reflect line across Y=X to have slope where: -0.5 < m < 0.5
                x0, y0 = y0, x0
                x1, y1 = y1, x1

        pts_reversed = False
        if x0 > x1:  # Swap left and right X's so line increases in Y as X increases
                x0, x1 = x1, x0
                y0, y1 = y1, y0
                pts_reversed = True

        deltax = x1-x0
        deltay = y1-y0

        error = int(deltax/2.0)
        ystep = 1 if y0 < y1 else -1

        y = y0
        for x in range(int(x0), int(x1)+1):
                coord = [y, x] if steep else [x, y]  # If was steep reverse back, otherwise keep order
                coords.append(coord)
                error -= abs(deltay)
                if error < 0:
                        y += ystep
                        error += deltax
        if pts_reversed:
            coords.reverse()  # Restore orginal coordinate order if previously swapped
        return coords


def clipping(x1, y1, x2, y2, xmin, xmax, ymin, ymax):
        # Clip each line to the screen buffer dimensions (50px within display window)

        # Assign location codes
        inside = 0  # 0000
        left = 1  # 0001
        right = 2  # 0010
        below = 4  # 0100
        above = 8  # 1000

        # Check the location condition of a given X and Y coordinate in reference to the clipping region
        def check_cond(xc, yc):
                code = inside  # Initialize state
                if xc < xmin:
                        code |= left
                elif xc > xmax:
                        code |= right
                if yc < ymin:
                        code |= below
                elif yc > ymax:
                        code |= above
                return code  # Return location condition of the point

        code1 = check_cond(x1, y1)  # Check left endpoint of the line
        code2 = check_cond(x2, y2)  # Check right endpoint of the line

        # While both points aren't already in the display area
        # If they initially are inside or are clipped inside, then break out and return new clipped endpoints
        while (code1 | code2) != 0:

                if (code1 & code2) != 0:  # If both points are outside of screen, reject both
                        return 9999, 9999, 9999, 9999  # Return condition to skip point set when drawing lines
                else:
                        # Identify first point outside the region to begin clipping along the line
                        if code1 != 0:
                                code_out = code1  # x1,y1 outside region
                        else:
                                code_out = code2  # x2,y2 outside region
                        # Based on each condition move along the slope of each line (Line Clipping Algorithm)
                        if code_out & above:
                                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                                y = ymax
                        elif code_out & below:
                                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                                y = ymin
                        elif code_out & right:
                                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                                x = xmax
                        elif code_out & left:
                                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                                x = xmin
                        if code_out == code1:  # x1,y1 point was out of the region
                                x1 = x
                                y1 = y
                                code1 = check_cond(x1, y1)  # Check condition of new point and loop
                        else:  # x2,y2 point was out of the region
                                x2 = x
                                y2 = y
                                code2 = check_cond(x2, y2)  # Check condition of new point and loop
        return x1, y1, x2, y2  # Return points that are within the clipping region for line drawing
