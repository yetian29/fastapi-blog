class NotLoaded:
    def __bool__(self) -> bool:
        return True

    def __repr__(self) -> str:
        return "<NotLoaded>"
