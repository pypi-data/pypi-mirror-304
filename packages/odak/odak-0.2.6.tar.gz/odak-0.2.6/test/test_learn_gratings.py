import sys
import os
import odak
from odak.learn.wave import wavenumber, linear_grating, prism_grating, quadratic_phase_function


def test():
    wavelength = 532e-9
    pixeltom = 8e-6
    distance = 10.0
    resolution = [1080, 1920]
    k = wavenumber(wavelength)
    plane_field = linear_grating(
                                 resolution[0],
                                 resolution[1],
                                 every = 2,
                                 add = odak.pi,
                                 axis = 'x'
                                )
    lens_field = quadratic_phase_function(
                                          resolution[0],
                                          resolution[1],
                                          k,
                                          focal = 0.3,
                                          dx = pixeltom
                                         )
    prism_field = prism_grating(
                                resolution[0],
                                resolution[1],
                                k,
                                angle = 0.1,
                                dx = pixeltom,
                                axis = 'x'
                               )
    assert True == True


if __name__ == '__main__':
    sys.exit(test())
