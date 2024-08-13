from aiogram.fsm.state import StatesGroup, State


class FileSG(StatesGroup):
    wait_for_file = State()
