from __future__ import annotations
from typing import Literal, Callable, Any

type Validity = Literal["valid"] | Literal["invalid"] | Literal["busy"]
type MaybeState[T] = StateNode[T] | T
type Use = Callable[[MaybeState[Any]], Any]


global_version = 0


def new_version() -> int:
    global global_version
    global_version += 1
    return global_version


def evaluate_node(node: GraphNode) -> bool:
    if node.validity == "busy":
        raise RecursionError("cyclical evaluation")
    # elif node.validity == "valid":
    #     return False

    needs_calculation = (
        node.validity == "invalid"
        or node.absolute_version == -1
        or node.cached_version == -1
    )

    if not needs_calculation:
        for user in node.users:
            if user.cached_version > node.absolute_version:
                needs_calculation = True
                break

    if not needs_calculation:
        return False

    for using in node.using:
        using.users.remove(node)
    node.using.clear()

    meaningfully_changed = node._evaluate() or node.cached_version == -1

    node.absolute_version = new_version()

    if meaningfully_changed:
        node.cached_version = node.absolute_version

    return meaningfully_changed


def change_node(node: GraphNode):
    if not evaluate_node(node):
        return

    search_now: set[GraphNode] = {node}
    search_next: set[GraphNode] = set()

    while len(search_now) > 0:
        for node in search_now:
            if node.validity == "busy":
                raise RecursionError("cyclical evaluation")
            elif node.validity == "valid":
                node.validity = "invalid"
                search_next.update(node.users)

        search_now.clear()
        search_next, search_now = search_now, search_next


def depend_node(dependant: GraphNode, dependancy: GraphNode):
    dependant.using.add(dependancy)
    dependancy.users.add(dependant)


class GraphNode:
    validity: Validity
    cached_version: int = -1
    absolute_version: int = -1
    users: set[GraphNode]
    using: set[GraphNode]

    def __init__(self) -> None:
        self.validity = "valid"
        self.users = set()
        self.using = set()

    def _evaluate(self) -> bool: ...


class StateNode[T](GraphNode):
    cached_value: T

    def get(self) -> T:
        evaluate_node(self)

        return self.cached_value


class Source[T](StateNode[T]):
    def __init__(self, initial_value: T) -> None:
        super().__init__()

        self.cached_value = initial_value

    def _evaluate(self) -> bool:
        return True

    def set(self, new_value: T):
        self.cached_value = new_value
        change_node(self)


class Derived[T](StateNode[T]):
    _use: Use
    _processor: Callable[[Use], T]

    def __init__(self, processor: Callable[[Use], T]) -> None:
        super().__init__()

        def use(x: MaybeState[Any]):
            if isinstance(x, StateNode):
                depend_node(self, x)
                return x.get()
            return x

        self._use = use
        self._processor = processor

    def _evaluate(self) -> bool:
        try:
            old_value = self.cached_value
        except:
            old_value = None

        new_value = self._processor(self._use)

        self.cached_value = new_value

        return new_value != old_value


source = Source(1)
derived = Derived(lambda use: use(source) + 1)
super_derived = Derived(lambda use: use(derived) * 10)

print("get derived", derived.get())

source.set(15)

print(source.get())
print("get derived", derived.get())
print("get super_derived", super_derived.get())

source.set(-10)

print(source.get())
print("get derived", derived.get())
print("get super_derived", super_derived.get())
