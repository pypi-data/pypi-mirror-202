# texturize — Copyright (c) 2020, Novelty Factory KG.  See LICENSE for details.

import math

import torch
from creativeai.vision import encoders

from .app import Application, Result
from .io import *


@torch.no_grad()
def process_iterations(
    cmd,
    *,
    size: tuple,
    log: object = None,
    octaves: int = None,
    variations: int = 1,
    iterations: tuple = (400,),
    model: str = "VGG11",
    layers: str = None,
    mode: str = None,
    device: str = None,
    precision: str = None,
):
    """Synthesize a new texture and return a PyTorch tensor at each iteration.
    """

    # Configure the default options dynamically, unless overriden.
    factor = math.sqrt((size[0] * size[1]) / (32 ** 2))
    octaves = octaves or getattr(cmd, "octaves", int(math.log(factor, 2) + 1.0))
    iterations = iterations if isinstance(iterations, tuple) else (iterations,)

    # Setup the application to use throughout the synthesis.
    app = Application(log, device, precision)

    # Encoder used by all the critics at every octave.
    encoder = getattr(encoders, model + 'Encoder')(pretrained=True, pool_type=torch.nn.AvgPool2d)
    encoder = encoder.to(device=app.device, dtype=app.precision)
    app.encoder = encoder
    app.layers = layers
    app.mode = mode

    # Coarse-to-fine rendering, number of octaves specified by user.
    seed = None
    for octave, scale in enumerate(2 ** s for s in range(octaves - 1, -1, -1)):
        app.log.info(f"\n OCTAVE #{octave} ")
        app.log.debug("<- scale:", f"1/{scale}")

        app.progress = app.log.create_progress_bar(100)

        result_size = (variations, 3, size[1] // scale, size[0] // scale)
        app.log.debug("<- seed:", tuple(result_size[2:]))

        for dtype in [torch.float32, torch.float16]:
            if app.precision != dtype:
                app.precision = dtype
                app.encoder = app.encoder.to(dtype=dtype)
                if seed is not None:
                    seed = seed.to(app.device)

            try:
                critics = cmd.prepare_critics(app, scale)
                seed = cmd.prepare_seed_tensor(app, result_size, previous=seed)

                its = iterations[-1] if octave >= len(iterations) else iterations[octave]
                for i, result in enumerate(app.process_octave(
                    seed, app.encoder, critics, octave, scale, iterations=its,
                )):
                    yield result

                seed = result.tensor
                del result
                break

            except RuntimeError as e:
                if "CUDA out of memory." not in str(e):
                    raise
                app.log.error(f"ERROR: Out of memory at octave {octave}.")
                app.log.debug(e)

                import gc; gc.collect
                torch.cuda.empty_cache()


@torch.no_grad()
def process_octaves(cmd, **kwargs):
    """Synthesize a new texture from sources and return a PyTorch tensor at each octave.
    """
    for r in process_iterations(cmd, **kwargs):
        if r.iteration >= 0:
            continue

        yield Result(
            r.tensor, r.octave, r.scale, -r.iteration, r.loss, r.rate, r.retries
        )


def process_single_command(cmd, log: object, output: str = None, properties: list = [], **config: dict):
    for result in process_octaves(cmd, log=log, **config):
        result = cmd.finalize_octave(result)

        filenames = []
        for i in range(result.tensor.shape[0]):
            from .io import save_tensor_to_files
            filename = output.format(
                octave=result.octave,
                variation=f"_{i}" if result.tensor.shape[0] > 1 else "",
                command=cmd.__class__.__name__.lower(),
                prop="_{prop}" if len(properties) else "",
            )
            save_tensor_to_files(result.tensor[i:i+1], filename, properties)
            log.debug("\n=> output:", filename)
            filenames.append(filename)

    return result, filenames
