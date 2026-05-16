import asyncio

import pytest

from src.task_registry import TaskRegistry


@pytest.fixture(autouse=True)
def reset_registry():
    TaskRegistry.reset_registry()
    yield


def _make_done_task() -> asyncio.Task:
    async def _noop():
        pass

    t = asyncio.ensure_future(_noop())
    t.add_done_callback(lambda _: None)
    return t


@pytest.mark.asyncio
async def test_should_start_new_task_no_existing_task():
    assert TaskRegistry.should_start_new_task("s1") is True


@pytest.mark.asyncio
async def test_should_start_new_task_existing_done_task():
    task = _make_done_task()
    await task
    TaskRegistry.register_task("s1", task)

    assert TaskRegistry.should_start_new_task("s1") is True


@pytest.mark.asyncio
async def test_should_start_new_task_existing_pending_task():
    async def _never_ends():
        await asyncio.Event().wait()

    task = asyncio.ensure_future(_never_ends())
    TaskRegistry.register_task("s1", task)

    try:
        assert TaskRegistry.should_start_new_task("s1") is False
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


@pytest.mark.asyncio
async def test_register_task_stores_task():
    async def _noop():
        pass

    task = asyncio.ensure_future(_noop())
    await task

    TaskRegistry.register_task("s1", task)
    assert TaskRegistry._tasks["s1"] is task


@pytest.mark.asyncio
async def test_register_task_overwrites_existing():
    async def _noop():
        pass

    task1 = asyncio.ensure_future(_noop())
    await task1
    task2 = asyncio.ensure_future(_noop())
    await task2

    TaskRegistry.register_task("s1", task1)
    TaskRegistry.register_task("s1", task2)

    assert TaskRegistry._tasks["s1"] is task2
    assert len(TaskRegistry._tasks) == 1
