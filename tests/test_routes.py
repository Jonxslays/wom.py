# wom.py - An asynchronous wrapper for the Wise Old Man API.
# Copyright (c) 2023-present Jonxslays
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

import pytest

from wom import CompiledRoute
from wom import Route


@pytest.fixture()
def mock_get() -> Route:
    return Route("GET", "/69420")


@pytest.fixture()
def mock_post() -> Route:
    return Route("POST", "/69420/{}/hi/{}")


def test_route_instantiation(mock_get: Route) -> None:
    assert mock_get.method == "GET"
    assert mock_get.uri == "/69420"


def test_route_compiles(mock_get: Route) -> None:
    compiled = mock_get.compile()
    assert isinstance(compiled, CompiledRoute)
    assert compiled.route == mock_get
    assert compiled.uri == "/69420"
    assert compiled.method == "GET"
    assert not compiled.params


def test_route_compiles_w_uri(mock_post: Route) -> None:
    compiled = mock_post.compile(1, 2)
    assert isinstance(compiled, CompiledRoute)
    assert compiled.route == mock_post
    assert compiled.uri == "/69420/1/hi/2"
    assert compiled.method == "POST"
    assert not compiled.params


def test_route_compiles_w_params(mock_get: Route) -> None:
    compiled = mock_get.compile().with_params({"test": 1})
    assert isinstance(compiled, CompiledRoute)
    assert compiled.route == mock_get
    assert compiled.uri == "/69420"
    assert compiled.method == "GET"
    assert len(compiled.params) == 1
    assert compiled.params["test"] == 1
