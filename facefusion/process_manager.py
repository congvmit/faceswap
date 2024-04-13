from typing import Generator, List

from facefusion.typing import ProcessState, QueuePayload

PROCESS_STATE: ProcessState = "pending"

PROCESSED_BATCH_I: int = 0


def reset_batch_i_processed() -> None:
    global PROCESSED_BATCH_I

    PROCESSED_BATCH_I = 0


def increment_batch_i_processed(value: int = 1) -> None:
    global PROCESSED_BATCH_I

    PROCESSED_BATCH_I += value


def get_batch_i_processed() -> int:
    return PROCESSED_BATCH_I


def get_process_state() -> ProcessState:
    return PROCESS_STATE


def set_process_state(process_state: ProcessState) -> None:
    global PROCESS_STATE

    PROCESS_STATE = process_state


def is_checking() -> bool:
    return get_process_state() == "checking"


def is_processing() -> bool:
    return get_process_state() == "processing"


def is_stopping() -> bool:
    return get_process_state() == "stopping"


def is_pending() -> bool:
    return get_process_state() == "pending"


def check() -> None:
    set_process_state("checking")


def start() -> None:
    set_process_state("processing")


def stop() -> None:
    set_process_state("stopping")


def end() -> None:
    set_process_state("pending")


def manage(queue_payloads: List[QueuePayload]) -> Generator[QueuePayload, None, None]:
    for query_payload in queue_payloads:
        if is_processing():
            yield query_payload
