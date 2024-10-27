import torch
import torch.nn as nn
import sys
import odak
from odak.learn.wave import generate_complex_field, phase_gradient, speckle_contrast


def test():
    torch.random.seed()
    phase = torch.rand(1920, 1080)
    amplitude = torch.rand_like(phase)
    complex_field = generate_complex_field(amplitude, phase)
    kernel = torch.tensor([[[[0, -1, 0], [-1, 4, -1], [0, -1, 0]]]], dtype=torch.float32) / 4
    kernel_size = 7
    step_size = (3, 3)
    phase_gradient_calculator = phase_gradient(
                                               kernel = kernel,
                                               loss = nn.MSELoss()
                                              )

    speckle_contrast_calculator = speckle_contrast(
                                                   kernel_size = kernel_size,
                                                   step_size = step_size,
                                                   loss = nn.MSELoss()
                                                  )
    complex_field_phase = odak.learn.wave.calculate_phase(complex_field)
    complex_field_amplitude = odak.learn.wave.calculate_amplitude(complex_field)
    phase_gradient_regular = phase_gradient_calculator(complex_field_phase)
    speckle_contrast_regular = speckle_contrast_calculator(complex_field_amplitude)
    assert True == True



if  __name__ ==  '__main__':
    sys.exit(test())
