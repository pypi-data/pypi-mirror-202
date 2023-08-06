import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from IPython import get_ipython
from dash import Dash, dcc, html, dash_table
from jupyter_dash import JupyterDash
from plotly.subplots import make_subplots
from dash_bootstrap_templates import load_figure_template

from quantfreedom.enums.enums import OrderType
from quantfreedom._typing import pdFrame, RecordArray
from quantfreedom.plotting.plot_helper_functions import (
    get_candle_trace_data,
    append_to_trace_data_list,
)

np.set_printoptions(formatter={"float_kind": "{:.2f}".format})

pd.options.display.float_format = "{:,.2f}".format

load_figure_template("darkly")
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
try:
    shell = str(get_ipython())
    if "ZMQInteractiveShell" in shell:
        app = JupyterDash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])
    elif shell == "TerminalInteractiveShell":
        app = JupyterDash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])
    else:
        app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])
except NameError:
    app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])

bg_color = "#0b0b18"


def strat_dashboard(
    indicator_dict: dict,
    prices: pdFrame,
    order_records: RecordArray,
) -> JupyterDash:
    """
    Function Name
    -------------
        strat_dashboard

    Quick Summary
    -------------
        Creates a dashboard with your trades, indicators, cumliative PnL and the order records of all the trades.

    Explainer Video
    ---------------
        Coming_Soon

    Required Parameters
    -------------------
    Variable Name: Variable Type

    indicator_dict: dict
        You need to create a dictionary of all your indicators.

        If you have any indicators that need to go on the candle stick chart then make a key named candle_chart and inside of that you put your indicator values with keys called value with a number after it like in the example, then you provide the entries

        If you have indicators that need their own chart then create a key called indicator with a number after it and then provide the indicator values and the entries in new keys.

        Example:
            indicator_dict = {
                    "candle_chart": {
                        "values1": ema_300_ind[[('BTCUSDT', 300)]],
                        "values2": ema_600_ind[[('BTCUSDT', 600)]],
                        "entries": entries[[("BTCUSDT", 30, 50, 300, 600)]],
                        },
                    "indicator1": {
                        "values1": rsi_ind[[('BTCUSDT', 30)]],
                        "entries": entries[[("BTCUSDT", 30, 50, 300, 600)]],
                        },
                    "indicator2": {
                        "values1": atr_ind[[('BTCUSDT', 50)]],
                        "entries": entries[[("BTCUSDT", 30, 50, 300, 600)]],
                        },
                    }
    prices: pdFrame
        Your prices info as one symbol like prices['BTCUSDT']

    order_records: RecordArray
        Order Records

    Returns
    -------
    JupyterDash
        Returns a jupyter dashboard that will open up in a new window when you click on the local host url
    """

    amount_of_subplots = 0

    for keys in indicator_dict.keys():
        if "indicator" in keys:
            amount_of_subplots += 1

    layout_height = 500 + (250 * amount_of_subplots)
    candle_chart_height_pct = [500 / layout_height]

    if amount_of_subplots > 0:
        subchart_heights_pct = np.array(
            [((layout_height - 500) / layout_height) / amount_of_subplots]
            * amount_of_subplots
        ).tolist()
        row_heights = candle_chart_height_pct + subchart_heights_pct
        fig = make_subplots(
            rows=amount_of_subplots + 1,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.02,
            row_heights=row_heights,
        )
    else:
        fig = make_subplots()

    index_prices = prices.index.to_list()

    # candle chart trace
    fig.add_traces(
        data=get_candle_trace_data(
            index_prices=index_prices,
            prices=prices,
            order_records=order_records,
            indicator_dict=indicator_dict,
        ),
        rows=1,
        cols=1,
    )
    try:
        del indicator_dict["candle_chart"]
    except:
        pass

    row_count = 2
    for indicator_dict_value in indicator_dict.values():
        trace_data_list = []
        temp_ind_vals = np.array([0], dtype=object)
        for ind_key, ind_value in indicator_dict_value.items():
            append_to_trace_data_list(
                trace_data_list=trace_data_list,
                index_prices=index_prices,
                dict_key=ind_key,
                dict_value=ind_value,
                temp_ind_vals=temp_ind_vals,
            )
        fig.add_traces(
            data=trace_data_list,
            rows=row_count,
            cols=1,
        )
        row_count += 1
    fig.update_xaxes(row=1, col=1, rangeslider_visible=False)
    fig.update_yaxes(row=1, col=1, tickprefix="$")
    fig.update_layout(
        height=layout_height,
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
    )
    candle_trades_and_ind = (
        html.H1(
            "All Trades For This Strategy",
            style={
                "textAlign": "center",
                "font-weight": "bold",
                "font-size": "5em",
                "padding-top": "20px",
            },
        ),
        dcc.Graph(
            id="candles-trades",
            figure=fig,
        ),
    )

    y_pnl = np.append(
        0,
        order_records["real_pnl"][~np.isnan(order_records["real_pnl"])].cumsum(),
    )

    pnl_graph = go.Figure(
        data=[
            go.Scatter(
                x=np.arange(0, y_pnl.size),
                y=y_pnl,
                mode="lines+markers",
                marker=dict(size=6),
                line=dict(color="#247eb2"),
            ),
        ]
    ).update_layout(
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
    )
    pnl_graph.update_yaxes(tickprefix="$"),

    pnl_graph = (
        html.H1(
            "Cumulative PnL Over Time",
            style={
                "textAlign": "center",
                "font-weight": "bold",
            },
        ),
        dcc.Graph(
            id="pnl-graph",
            figure=pnl_graph,
        ),
    )

    d_table = pd.DataFrame(order_records)
    for i in range(len(OrderType._fields)):
        d_table.replace({"order_type": {i: OrderType._fields[i]}}, inplace=True)

    for col in d_table:
        if d_table[col].dtype == "float64":
            d_table[col] = d_table[col].map("{:,.2f}".format)
    d_table = d_table.to_dict("records")

    d_table = (
        html.H1(
            "Table of All Orders",
            style={
                "textAlign": "center",
                "font-weight": "bold",
            },
        ),
        dash_table.DataTable(
            data=d_table,
            id="d-table",
            page_size=50,
            # page_action='none',
            style_table={"height": "400px", "overflowY": "auto"},
            fixed_rows={"headers": True},
            style_header={"backgroundColor": "rgb(30, 30, 30)", "color": "white"},
            style_data={"backgroundColor": "rgb(50, 50, 50)", "color": "white"},
            style_cell_conditional=[
                {"if": {"column_id": "settings_id"}, "width": "110px"},
                {"if": {"column_id": "order_id"}, "width": "90px"},
            ],
        ),
    )

    app.layout = html.Div(
        [
            html.Div(
                candle_trades_and_ind,
            ),
            html.Div(
                pnl_graph,
            ),
            html.Div(
                d_table,
            ),
        ]
    )

    return app.run_server(debug=True, port=3003)
