import numpy as np
import gtransform

'''
Code to orient the initial geometry centered upon the geometric origin
Then scales the object to fit within a window of the width and height supplied

Evan Chodora, 2018
echodor@clemson.edu
'''


def orient(geometry, width, height):

        # Compute object dimensions and distance from the origin
        max_size = np.max(geometry, axis=0)  # Max X,Y,Z values
        min_size = np.min(geometry, axis=0)  # Min X,Y,Z values
        x_trans = 0 - 0.5*(max_size[0]+min_size[0])  # Avg X distance from the origin
        y_trans = 0 - 0.5*(max_size[1]+min_size[1])  # Avg Y distance from the origin
        z_trans = 0 - 0.5*(max_size[2]+min_size[2])  # Avg Z distance from the origin
        geometry = gtransform.translate(geometry, x_trans, y_trans, z_trans)  # Translate object accordingly

        # Compute scaling to center object in the screen
        geometry_scale, _ = gtransform.perspective('iso', geometry, None, None, None)  # Apply perspective
        max_size = np.max(geometry_scale, axis=0)  # Max X and Y values of projected point cloud on display (Z = 0)
        scale = 1
        # Based on whether the object is larger in width or height when projected, apply a scaling factor
        # that will fit the object within the space of the pixel array/clipping region
        if max_size[0] >= max_size[1]:
                scale = (0.5*width)/(2*max_size[0])
        if max_size[0] < max_size[1]:
                scale = (0.5*height)/(2*max_size[1])
        geometry = gtransform.scale(geometry, 1/scale)  # Apply global scaling with appropriate factor

        return geometry
