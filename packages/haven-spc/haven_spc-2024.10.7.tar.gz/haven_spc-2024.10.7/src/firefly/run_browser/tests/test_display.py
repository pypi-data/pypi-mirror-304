import asyncio

import pytest
from qtpy.QtWidgets import QFileDialog

from firefly.run_browser.display import RunBrowserDisplay


@pytest.fixture()
async def display(qtbot, catalog, mocker):
    mocker.patch(
        "firefly.run_browser.widgets.ExportDialog.exec_",
        return_value=QFileDialog.Accepted,
    )
    mocker.patch(
        "firefly.run_browser.widgets.ExportDialog.selectedFiles",
        return_value=["/net/s255data/export/test_file.nx"],
    )
    mocker.patch("firefly.run_browser.client.DatabaseWorker.export_runs")
    display = RunBrowserDisplay(root_node=catalog)
    qtbot.addWidget(display)
    display.clear_filters()
    # Wait for the initial database load to process
    await display._running_db_tasks["init_load_runs"]
    await display._running_db_tasks["update_combobox_items"]
    return display


@pytest.mark.asyncio
async def test_db_task(display):
    async def test_coro():
        return 15

    result = await display.db_task(test_coro())
    assert result == 15


@pytest.mark.asyncio
async def test_db_task_interruption(display):
    async def test_coro(sleep_time):
        await asyncio.sleep(sleep_time)
        return sleep_time

    # Create an existing task that will be cancelled
    task_1 = display.db_task(test_coro(1.0), name="testing")
    # Now execute another task
    result = await display.db_task(test_coro(0.01), name="testing")
    assert result == 0.01
    # Check that the first one was cancelled
    with pytest.raises(asyncio.exceptions.CancelledError):
        await task_1
    assert task_1.done()
    assert task_1.cancelled()


def test_load_runs(display):
    assert display.runs_model.rowCount() > 0
    assert display.ui.runs_total_label.text() == str(display.runs_model.rowCount())


@pytest.mark.asyncio
async def test_update_selected_runs(display):
    # Change the proposal item
    item = display.runs_model.item(0, 1)
    assert item is not None
    display.ui.run_tableview.selectRow(0)
    # Update the runs
    await display.update_selected_runs()
    # Check that the runs were saved
    assert len(display.db.selected_runs) > 0
