import dataclasses
import typing
import irisml.core


def clip_imagenet_generator(label_name: str) -> typing.List[str]:
    templates = [
        'a bad photo of a {}.',
        'a photo of many {}.',
        'a sculpture of a {}.',
        'a photo of the hard to see {}.',
        'a low resolution photo of the {}.',
        'a rendering of a {}.',
        'graffiti of a {}.',
        'a bad photo of the {}.',
        'a cropped photo of the {}.',
        'a tattoo of a {}.',
        'the embroidered {}.',
        'a photo of a hard to see {}.',
        'a bright photo of a {}.',
        'a photo of a clean {}.',
        'a photo of a dirty {}.',
        'a dark photo of the {}.',
        'a drawing of a {}.',
        'a photo of my {}.',
        'the plastic {}.',
        'a photo of the cool {}.',
        'a close-up photo of a {}.',
        'a black and white photo of the {}.',
        'a painting of the {}.',
        'a painting of a {}.',
        'a pixelated photo of the {}.',
        'a sculpture of the {}.',
        'a bright photo of the {}.',
        'a cropped photo of a {}.',
        'a plastic {}.',
        'a photo of the dirty {}.',
        'a jpeg corrupted photo of a {}.',
        'a blurry photo of the {}.',
        'a photo of the {}.',
        'a good photo of the {}.',
        'a rendering of the {}.',
        'a {} in a video game.',
        'a photo of one {}.',
        'a doodle of a {}.',
        'a close-up photo of the {}.',
        'a photo of a {}.',
        'the origami {}.',
        'the {} in a video game.',
        'a sketch of a {}.',
        'a doodle of the {}.',
        'a origami {}.',
        'a low resolution photo of a {}.',
        'the toy {}.',
        'a rendition of the {}.',
        'a photo of the clean {}.',
        'a photo of a large {}.',
        'a rendition of a {}.',
        'a photo of a nice {}.',
        'a photo of a weird {}.',
        'a blurry photo of a {}.',
        'a cartoon {}.',
        'art of a {}.',
        'a sketch of the {}.',
        'a embroidered {}.',
        'a pixelated photo of a {}.',
        'itap of the {}.',
        'a jpeg corrupted photo of the {}.',
        'a good photo of a {}.',
        'a plushie {}.',
        'a photo of the nice {}.',
        'a photo of the small {}.',
        'a photo of the weird {}.',
        'the cartoon {}.',
        'art of the {}.',
        'a drawing of the {}.',
        'a photo of the large {}.',
        'a black and white photo of a {}.',
        'the plushie {}.',
        'a dark photo of a {}.',
        'itap of a {}.',
        'graffiti of the {}.',
        'a toy {}.',
        'itap of my {}.',
        'a photo of a cool {}.',
        'a photo of a small {}.',
        'a tattoo of the {}.'
        ]
    return [t.format(label_name) for t in templates]


def clip_imagenet_short_generator(label_name: str) -> typing.List[str]:
    templates = ['itap of a {}.',
                 'a bad photo of the {}.',
                 'a origami {}.',
                 'a photo of the large {}.',
                 'a {} in a video game.',
                 'art of the {}.',
                 'a photo of the small {}.']
    return [t.format(label_name) for t in templates]


class TemplateGenerator:
    def __init__(self, template):
        self._template = template or '{}'
        if '{}' not in self._template:
            raise ValueError('Template must contain {}')

    def __call__(self, label_name: str) -> typing.List[str]:
        return [self._template.format(label_name)]


class Task(irisml.core.TaskBase):
    """Create a prompt generator for a classification task.

    Supported generator:
        'clip_imagenet': Generates 80 prompts that are introduced in the openai/CLIP repository. (https://github.com/openai/CLIP)
        'clip_imagenet_short': Generates 7 prompts that are introduced in the openai/CLIP repository.
        'template': Use the provided template to generate a single prompt.

    Config:
        name (str): Name of the generator.
        template (str): Template to use for the 'template' generator.
    """
    VERSION = '0.2.0'

    @dataclasses.dataclass
    class Config:
        name: str = 'clip_imagenet'
        template: typing.Optional[str] = None

    @dataclasses.dataclass
    class Outputs:
        generator: typing.Callable[[str], typing.List[str]]

    GENERATORS = {
        'clip_imagenet': clip_imagenet_generator,
        'clip_imagenet_short': clip_imagenet_short_generator
    }

    def execute(self, inputs):
        if self.config.name == 'template':
            return self.Outputs(TemplateGenerator(self.config.template))

        if self.config.name not in self.GENERATORS:
            raise ValueError(f"Unknown generator name: {self.config.name}")
        gen = self.GENERATORS[self.config.name]
        return self.Outputs(gen)

    def dry_run(self, inputs):
        return self.execute(inputs)
