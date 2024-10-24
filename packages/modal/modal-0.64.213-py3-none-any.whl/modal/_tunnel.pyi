import modal.client
import synchronicity.combined_types
import typing
import typing_extensions

class Tunnel:
    host: str
    port: int
    unencrypted_host: str
    unencrypted_port: int

    @property
    def url(self) -> str: ...
    @property
    def tls_socket(self) -> typing.Tuple[str, int]: ...
    @property
    def tcp_socket(self) -> typing.Tuple[str, int]: ...
    def __init__(self, host: str, port: int, unencrypted_host: str, unencrypted_port: int) -> None: ...
    def __repr__(self): ...
    def __eq__(self, other): ...
    def __setattr__(self, name, value): ...
    def __delattr__(self, name): ...
    def __hash__(self): ...

def _forward(
    port: int, *, unencrypted: bool = False, client: typing.Optional[modal.client._Client] = None
) -> typing.AsyncContextManager[Tunnel]: ...

class __forward_spec(typing_extensions.Protocol):
    def __call__(
        self, port: int, *, unencrypted: bool = False, client: typing.Optional[modal.client.Client] = None
    ) -> synchronicity.combined_types.AsyncAndBlockingContextManager[Tunnel]: ...
    def aio(
        self, port: int, *, unencrypted: bool = False, client: typing.Optional[modal.client.Client] = None
    ) -> typing.AsyncContextManager[Tunnel]: ...

forward: __forward_spec
