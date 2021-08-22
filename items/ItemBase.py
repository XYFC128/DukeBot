from utils import PrintState


class ItemBase:
    def acquired() -> PrintState:
        return None


    def init_user_stack(channel, user, user_stack: list) -> None:
        pass


    def use(channel, user, user_stack: list, data) -> None:
        pass