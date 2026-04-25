from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Iterable, Type

type Action[C] = Callable[[C], None]

def iter_enum[E](enum_cls : Type[E]) -> list[E]:
    return list(en)

class InvalidTransition(Exception):
    pass
    #def __init__(self, msg):
    #    super().__init__(msg)


@dataclass
class StateMachine[S:Enum, E:Enum, C]:
    transitions: dict[tuple[S, E], tuple[S, Action[C]]] = field(default_factory=dict[tuple[S, E], tuple[S, Action[C]]])

    def iter_enum[E](enum_cls : Type[E]) -> list[E]:
        return list(enum_cls)

    def add_transition(self, from_state: S, event: E, to_state: S, func: Action[C]):
        self.transitions[(from_state, event)] = (to_state, func)

    def next_transition(self, state:S, event:E) -> tuple[S, Action[C]]:
        try:
            return self.transitions[(state, event)]
        except KeyError as e:
            raise InvalidTransition(f"Cannot {event.name} when {state.name}") from e

    def handle(self, ctx: C, state: S, event: E) -> S:
        next_state, action = self.next_transition(state, event)
        action(ctx)
        return next_state

    def transition(self, from_state: S|Iterable[S], event: E, to_state: S):
        if not isinstance(from_state, Iterable):
            from_state = (from_state,)

        def decorator(func: Action[C])->Action[C]:
            for state in from_state:
                self.add_transition(state, event, to_state, func)
            return func

        return decorator

    def stick(self, from_state: S|Iterable[S]):
        if not isinstance(from_state, Iterable):
            from_state = (from_state,)

        def decorator(func: Action[C])->Action[C]:
            for state in from_state:
                for event in StateMachine.iter_enum(E):
                    self.add_transition(state, event, state, func)
            return func

        return decorator
