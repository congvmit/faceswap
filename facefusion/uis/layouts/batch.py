import multiprocessing

import gradio

# from facefusion.uis.components import preview
from facefusion.uis.components import (
    about,
    common_options,
    execution,
    execution_queue_count,
    execution_thread_count,
    face_analyser,
    face_masker,
)
from facefusion.uis.components import face_selector_batch as face_selector
from facefusion.uis.components import (
    frame_processors,
    frame_processors_options,
    memory,
)
from facefusion.uis.components import output_batch as output
from facefusion.uis.components import output_options_batch as output_options
from facefusion.uis.components import source_batch as source
from facefusion.uis.components import target_batch as target
from facefusion.uis.components import temp_frame, trim_frame


def pre_check() -> bool:
    return True


def pre_render() -> bool:
    return True


def render() -> gradio.Blocks:
    with gradio.Blocks() as layout:
        with gradio.Row():
            with gradio.Column(scale=2):
                # with gradio.Blocks():
                #     about.render()``
                with gradio.Blocks():
                    frame_processors.render()
                with gradio.Blocks():
                    frame_processors_options.render()
                with gradio.Blocks():
                    execution.render()
                    execution_thread_count.render()
                    execution_queue_count.render()
                with gradio.Blocks():
                    memory.render()
                with gradio.Blocks():
                    temp_frame.render()
                with gradio.Blocks():
                    output_options.render()
            with gradio.Column(scale=2):
                with gradio.Blocks():
                    source.render()
                with gradio.Blocks():
                    target.render()
                with gradio.Blocks():
                    output.render()
            with gradio.Column(scale=3):
                # with gradio.Blocks():
                #     preview.render()
                # with gradio.Blocks():
                #     trim_frame.render()
                with gradio.Blocks():
                    face_selector.render()
                with gradio.Blocks():
                    face_masker.render()
                with gradio.Blocks():
                    face_analyser.render()
                with gradio.Blocks():
                    common_options.render()
    return layout


def listen() -> None:
    frame_processors.listen()
    frame_processors_options.listen()
    execution.listen()
    execution_thread_count.listen()
    execution_queue_count.listen()
    memory.listen()
    temp_frame.listen()
    output_options.listen()
    source.listen()
    target.listen()
    output.listen()
    # preview.listen()
    # trim_frame.listen()
    face_selector.listen()
    face_masker.listen()
    face_analyser.listen()
    common_options.listen()


def run(ui: gradio.Blocks) -> None:
    concurrency_count = min(8, multiprocessing.cpu_count())
    ui.queue(concurrency_count=concurrency_count)
    ui.launch(show_api=False, quiet=False)
