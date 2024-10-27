from unittest.mock import MagicMock

import pandas as pd

from firefly.run_browser.widgets import Browser1DPlotWidget


async def test_plot_1d_runs(qtbot):
    widget = Browser1DPlotWidget()
    qtbot.addWidget(widget)
    assert len(widget.data_items) == 0
    # Set some runs
    widget.plot_runs({"hello": pd.Series(data=[10, 20, 30], index=[1, 2, 3])})
    assert "hello" in widget.data_items.keys()
    # Now update it again and check that the data item is reused
    mock_data_item = MagicMock()
    widget.data_items["hello"] = mock_data_item
    widget.plot_runs({"hello": pd.Series(data=[40, 50], index=[4, 5])})
    assert widget.data_items["hello"] is mock_data_item
    mock_data_item.setData.assert_called_once()
