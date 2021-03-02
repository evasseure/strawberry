import typing
from enum import Enum
from typing import List, Optional

import pytest

import strawberry


def test_enum_resolver():
    global IceCreamFlavour, Cone

    @strawberry.enum
    class IceCreamFlavour(Enum):
        VANILLA = "vanilla"
        STRAWBERRY = "strawberry"
        CHOCOLATE = "chocolate"

    @strawberry.type
    class Query:
        @strawberry.field
        def best_flavour(self) -> IceCreamFlavour:
            return IceCreamFlavour.STRAWBERRY

    schema = strawberry.Schema(query=Query)

    query = "{ bestFlavour }"

    result = schema.execute_sync(query)

    assert not result.errors
    assert result.data["bestFlavour"] == "STRAWBERRY"

    @strawberry.type
    class Cone:
        flavour: IceCreamFlavour

    @strawberry.type
    class Query:
        @strawberry.field
        def cone(self) -> Cone:
            return Cone(flavour=IceCreamFlavour.STRAWBERRY)

    schema = strawberry.Schema(query=Query)

    query = "{ cone { flavour } }"

    result = schema.execute_sync(query)

    assert not result.errors
    assert result.data["cone"]["flavour"] == "STRAWBERRY"

    del IceCreamFlavour, Cone


def test_enum_arguments():
    global IceCreamFlavour, ConeInput

    @strawberry.enum
    class IceCreamFlavour(Enum):
        VANILLA = "vanilla"
        STRAWBERRY = "strawberry"
        CHOCOLATE = "chocolate"

    @strawberry.type
    class Query:
        @strawberry.field
        def flavour_available(self, flavour: IceCreamFlavour) -> bool:
            return flavour == IceCreamFlavour.STRAWBERRY

    @strawberry.input
    class ConeInput:
        flavour: IceCreamFlavour

    @strawberry.type
    class Mutation:
        @strawberry.mutation
        def eat_cone(self, input: ConeInput) -> bool:
            return input.flavour == IceCreamFlavour.STRAWBERRY

    schema = strawberry.Schema(query=Query, mutation=Mutation)

    query = "{ flavourAvailable(flavour: VANILLA) }"
    result = schema.execute_sync(query)

    assert not result.errors
    assert result.data["flavourAvailable"] is False

    query = "{ flavourAvailable(flavour: STRAWBERRY) }"
    result = schema.execute_sync(query)

    assert not result.errors
    assert result.data["flavourAvailable"] is True

    query = "mutation { eatCone(input: { flavour: VANILLA }) }"
    result = schema.execute_sync(query)

    assert not result.errors
    assert result.data["eatCone"] is False

    query = "mutation { eatCone(input: { flavour: STRAWBERRY }) }"
    result = schema.execute_sync(query)

    assert not result.errors
    assert result.data["eatCone"] is True

    del IceCreamFlavour, ConeInput


def test_enum_falsy_values():
    global IceCreamFlavour, Input

    @strawberry.enum
    class IceCreamFlavour(Enum):
        VANILLA = ""
        STRAWBERRY = 0

    @strawberry.input
    class Input:
        flavour: IceCreamFlavour
        optionalFlavour: typing.Optional[IceCreamFlavour] = None

    @strawberry.type
    class Query:
        @strawberry.field
        def print_flavour(self, input: Input) -> str:
            return f"{input.flavour.value}"

    schema = strawberry.Schema(query=Query)

    query = "{ printFlavour(input: { flavour: VANILLA }) }"
    result = schema.execute_sync(query)

    assert not result.errors
    assert result.data["printFlavour"] == ""

    query = "{ printFlavour(input: { flavour: STRAWBERRY }) }"
    result = schema.execute_sync(query)

    assert not result.errors
    assert result.data["printFlavour"] == "0"

    del IceCreamFlavour, Input


def test_enum_in_list():
    global IceCreamFlavour

    @strawberry.enum
    class IceCreamFlavour(Enum):
        VANILLA = "vanilla"
        STRAWBERRY = "strawberry"
        CHOCOLATE = "chocolate"
        PISTACHIO = "pistachio"

    @strawberry.type
    class Query:
        @strawberry.field
        def best_flavours(self) -> List[IceCreamFlavour]:
            return [IceCreamFlavour.STRAWBERRY, IceCreamFlavour.PISTACHIO]

    schema = strawberry.Schema(query=Query)

    query = "{ bestFlavours }"

    result = schema.execute_sync(query)

    assert not result.errors
    assert result.data["bestFlavours"] == ["STRAWBERRY", "PISTACHIO"]

    del IceCreamFlavour


def test_enum_in_optional_list():
    global IceCreamFlavour

    @strawberry.enum
    class IceCreamFlavour(Enum):
        VANILLA = "vanilla"
        STRAWBERRY = "strawberry"
        CHOCOLATE = "chocolate"
        PISTACHIO = "pistachio"

    @strawberry.type
    class Query:
        @strawberry.field
        def best_flavours(self) -> Optional[List[IceCreamFlavour]]:
            return None

    schema = strawberry.Schema(query=Query)

    query = "{ bestFlavours }"

    result = schema.execute_sync(query)

    assert not result.errors
    assert result.data["bestFlavours"] is None

    del IceCreamFlavour


@pytest.mark.asyncio
async def test_enum_resolver_async():
    global IceCreamFlavour

    @strawberry.enum
    class IceCreamFlavour(Enum):
        VANILLA = "vanilla"
        STRAWBERRY = "strawberry"
        CHOCOLATE = "chocolate"

    @strawberry.type
    class Query:
        @strawberry.field
        async def best_flavour(self) -> IceCreamFlavour:
            return IceCreamFlavour.STRAWBERRY

    schema = strawberry.Schema(query=Query)

    query = "{ bestFlavour }"

    result = await schema.execute(query)

    assert not result.errors
    assert result.data["bestFlavour"] == "STRAWBERRY"

    del IceCreamFlavour


@pytest.mark.asyncio
async def test_enum_in_list_async():
    global IceCreamFlavour

    @strawberry.enum
    class IceCreamFlavour(Enum):
        VANILLA = "vanilla"
        STRAWBERRY = "strawberry"
        CHOCOLATE = "chocolate"
        PISTACHIO = "pistachio"

    @strawberry.type
    class Query:
        @strawberry.field
        async def best_flavours(self) -> List[IceCreamFlavour]:
            return [IceCreamFlavour.STRAWBERRY, IceCreamFlavour.PISTACHIO]

    schema = strawberry.Schema(query=Query)

    query = "{ bestFlavours }"

    result = await schema.execute(query)

    assert not result.errors
    assert result.data["bestFlavours"] == ["STRAWBERRY", "PISTACHIO"]

    del IceCreamFlavour
