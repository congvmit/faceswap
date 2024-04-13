from time import sleep
from typing import Optional, Tuple

import gradio

import facefusion.globals
from facefusion import process_manager, wording
from facefusion.core import conditional_process_batch
from facefusion.filesystem import clear_temp, is_image, is_video
from facefusion.memory import limit_system_memory
from facefusion.normalizer import normalize_output_path
from facefusion.uis.core import get_ui_component, register_ui_component

OUTPUT_IMAGE: Optional[gradio.Image] = None
OUTPUT_VIDEO: Optional[gradio.Video] = None
OUTPUT_START_BUTTON: Optional[gradio.Button] = None
OUTPUT_CLEAR_BUTTON: Optional[gradio.Button] = None
OUTPUT_STOP_BUTTON: Optional[gradio.Button] = None
OUTPUT_PROGRESS_BAR: Optional[gradio.Progress] = None
OUTPUT_PROGRESS_BAR_LABEL: Optional[gradio.Label] = None


def render() -> None:
    global OUTPUT_IMAGE
    global OUTPUT_VIDEO
    global OUTPUT_START_BUTTON
    global OUTPUT_STOP_BUTTON
    global OUTPUT_CLEAR_BUTTON
    global OUTPUT_PROGRESS_BAR
    global OUTPUT_PROGRESS_BAR_LABEL

    OUTPUT_START_BUTTON = gradio.Button(
        value=wording.get("uis.start_button"), variant="primary", size="sm"
    )
    OUTPUT_STOP_BUTTON = gradio.Button(
        value=wording.get("uis.stop_button"),
        variant="primary",
        size="sm",
        visible=False,
    )
    OUTPUT_CLEAR_BUTTON = gradio.Button(
        value=wording.get("uis.clear_button"), size="sm"
    )
    OUTPUT_PROGRESS_BAR = gradio.Progress()
    OUTPUT_PROGRESS_BAR_LABEL = gradio.Label(
        label="Progress", value="Waiting...", visible=False
    )
    register_ui_component("output_progress_bar", OUTPUT_PROGRESS_BAR)
    # def __call__(
    #     self,
    #     progress: float | tuple[int, int | None] | None,
    #     desc: str | None = None,
    #     total: int | None = None,
    #     unit: str = "steps",
    #     _tqdm=None,
    # ):
    #     """
    #     Updates progress tracker with progress and message text.
    #     Parameters:
    #         progress: If float, should be between 0 and 1 representing completion. If Tuple, first number represents steps completed, and second value represents total steps or None if unknown. If None, hides progress bar.
    #         desc: description to display.
    #         total: estimated total number of steps.
    #         unit: unit of iterations.
    #     """


def listen() -> None:
    # global OUTPUT_PROGRESS_BAR_LABEL, OUTPUT_START_BUTTON, OUTPUT_STOP_BUTTON
    output_path_textbox = get_ui_component("output_path_textbox")
    if output_path_textbox:
        OUTPUT_START_BUTTON.click(
            start,
            outputs=[
                OUTPUT_START_BUTTON,
                OUTPUT_STOP_BUTTON,
                OUTPUT_PROGRESS_BAR_LABEL,
            ],
        )
        OUTPUT_START_BUTTON.click(
            process,
            outputs=[
                OUTPUT_START_BUTTON,
                OUTPUT_STOP_BUTTON,
                OUTPUT_PROGRESS_BAR_LABEL,
            ],
        )
    OUTPUT_STOP_BUTTON.click(stop, outputs=[OUTPUT_START_BUTTON, OUTPUT_STOP_BUTTON])
    OUTPUT_CLEAR_BUTTON.click(clear)


def start() -> Tuple[gradio.Button, gradio.Button, gradio.Label]:
    # while not process_manager.is_processing():
    #     sleep(0.5)
    return (
        gradio.Button(visible=False),
        gradio.Button(visible=True),
        gradio.Label(visible=True),
    )


def process() -> Tuple[gradio.Button, gradio.Button, gradio.Label]:
    print("Go here!")
    # normed_output_path = normalize_output_path(
    #     facefusion.globals.target_path, facefusion.globals.output_path
    # )
    if facefusion.globals.system_memory_limit > 0:
        limit_system_memory(facefusion.globals.system_memory_limit)
    conditional_process_batch()
    return (
        gradio.Button(visible=True),
        gradio.Button(visible=False),
        gradio.Label(value="Done"),
    )


def stop() -> Tuple[gradio.Button, gradio.Button]:
    process_manager.stop()
    return gradio.Button(visible=True), gradio.Button(visible=False)


def clear() -> Tuple[gradio.Label]:
    # while process_manager.is_processing():
    #     sleep(0.5)
    if facefusion.globals.target_path:
        clear_temp(facefusion.globals.target_path)
    return gradio.Label(value="Waiting...", visible=False)
