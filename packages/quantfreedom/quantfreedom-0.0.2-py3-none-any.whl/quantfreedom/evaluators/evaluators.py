import pandas as pd
import numpy as np
import plotly.graph_objects as go
from itertools import product
from plotly.subplots import make_subplots
from quantfreedom._typing import pdFrame, Union, Array1d


def combine_evals(
    first_eval_data: pdFrame,
    second_eval_data: pdFrame,
    plot_results: bool = False,
    first_eval_data_needs_prices: bool = False,
    second_eval_data_needs_prices: bool = False,
    prices: pdFrame = None,
    first_ind_data: pdFrame = None,
    second_ind_data: pdFrame = None,
) -> pdFrame:
    """
    _summary_

    Parameters
    ----------
    first_eval_data : pdFrame
        _description_
    second_eval_data : pdFrame
        _description_
    plot_results : bool, optional
        _description_, by default False
    first_eval_data_needs_prices : bool, optional
        _description_, by default False
    second_eval_data_needs_prices : bool, optional
        _description_, by default False
    prices : pdFrame, optional
        _description_, by default None
    first_ind_data : pdFrame, optional
        _description_, by default None
    second_ind_data : pdFrame, optional
        _description_, by default None

    Returns
    -------
    pdFrame
        _description_

    Raises
    ------
    ValueError
        _description_
    ValueError
        _description_
    ValueError
        _description_
    ValueError
        _description_
    """

    if plot_results and (first_ind_data is None or second_ind_data is None):
        raise ValueError(
            "Make sure you are sending first and second indicator data if you want to plot")
    elif plot_results:
        if first_eval_data_needs_prices and prices is None:
            raise ValueError("You need to provide prices to plot the candles")
        elif not first_eval_data_needs_prices and prices is not None:
            raise ValueError(
                "Make sure you set first_eval_data_needs_prices to true if you want to send price data")
    elif not plot_results and (
        first_eval_data_needs_prices or
        prices is not None or
        first_ind_data is not None or
        second_ind_data is not None
    ):
        raise ValueError(
            "Make sure you set plot_results to true if you want to send any plotting data.")

    if len(first_eval_data.columns.levels) < len(second_eval_data.columns.levels):
        temp = len(first_eval_data.columns.levels)
    else:
        temp = len(second_eval_data.columns.levels)

    list_for_product = []
    pd_col_names = []
    for x in range(temp):
        if list(first_eval_data.columns.levels[x]) == list(second_eval_data.columns.levels[x]):
            list_for_product.append(list(first_eval_data.columns.levels[x]))
            pd_col_names.append(first_eval_data.columns.names[x])
    levels = list(product(*list_for_product))

    pd_col_names = pd_col_names + list(first_eval_data.droplevel(pd_col_names, axis=1).columns.names) + \
        list(second_eval_data.droplevel(pd_col_names, axis=1).columns.names)

    combine_array = np.empty(
        (first_eval_data.shape[0], first_eval_data[levels[0]].shape[1] * second_eval_data[levels[0]].shape[1] * len(levels)), dtype=np.bool_
    )

    try:
        second_eval_data[levels[0]].columns[0][0]
        temp_smaller_def_columns = list(second_eval_data[levels[0]].columns)
    except:
        temp_smaller_def_columns = []
        for value in list(second_eval_data[levels[0]].columns):
            temp_smaller_def_columns.append((value,))

    try:
        first_eval_data[levels[0]].columns[0][0]
        temp_big_def_columns = list(first_eval_data[levels[0]].columns)
    except:
        temp_big_def_columns = []
        for value in list(first_eval_data[levels[0]].columns):
            temp_big_def_columns.append((value,))

    comb_counter = 0
    pd_multind_tuples = ()
    for level in levels:
        temp_big_df = first_eval_data[level]
        temp_small_df = second_eval_data[level]
        for big_count, big_values in enumerate(temp_big_df.values.T):

            for small_count, small_values in enumerate(temp_small_df.values.T):

                combine_array[:, comb_counter] = np.logical_and(
                    big_values == True, small_values == True
                )

                pd_multind_tuples = pd_multind_tuples + (
                    level + temp_big_def_columns[big_count] +
                    temp_smaller_def_columns[small_count],
                )

                comb_counter += 1

    if plot_results:
        plot_index = second_eval_data.index

        temp_first_ind_data = first_ind_data.iloc[:, -1]
        temp_second_ind_data = second_ind_data.iloc[:, -1]

        temp_combine_array = combine_array[:, -1]

        # candle data with subplot
        if first_eval_data_needs_prices and not second_eval_data_needs_prices:
            temp_prices = prices[list(prices.columns)[-1][0]]
            fig = make_subplots(
                rows=2,
                cols=1,
                shared_xaxes=True,
            )
            fig.add_traces(
                data=[
                    go.Candlestick(
                        x=plot_index,
                        open=temp_prices.open,
                        high=temp_prices.high,
                        low=temp_prices.low,
                        close=temp_prices.close,
                        name="Candles",
                    ),
                    go.Scatter(
                        x=plot_index,
                        y=temp_first_ind_data,
                        mode="lines",
                        line=dict(width=3, color='#60BFE1'),
                        name="First Ind",
                    ),
                    go.Scatter(
                        x=plot_index,
                        y=np.where(
                            temp_combine_array,
                            temp_first_ind_data,
                            np.nan,
                        ),
                        mode="markers",
                        marker=dict(size=3, color='yellow'),
                        name="Combo Signals",
                    ),
                ],
                rows=1,
                cols=1,
            )
            fig.add_traces(
                data=[
                    go.Scatter(
                        x=plot_index,
                        y=temp_second_ind_data,
                        mode="lines",
                        line=dict(width=2, color='#60BFE1'),
                        name="Second Ind",
                    ),
                    go.Scatter(
                        x=plot_index,
                        y=np.where(
                            temp_combine_array,
                            temp_second_ind_data,
                            np.nan,
                        ),
                        mode="markers",
                        marker=dict(size=3, color='yellow'),
                        name="Combo Signals",
                    ),
                ],
                rows=2,
                cols=1,
            )
            fig.update_xaxes(rangeslider_visible=False)
            fig.update_layout(height=700, title="Last Column of the Results")
            fig.show()

        elif first_eval_data_needs_prices and second_eval_data_needs_prices:
            temp_prices = prices[list(prices.columns)[-1][0]]
            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=plot_index,
                        open=temp_prices.open,
                        high=temp_prices.high,
                        low=temp_prices.low,
                        close=temp_prices.close,
                        name="Candles",
                    ),

                    # First Plot
                    go.Scatter(
                        x=plot_index,
                        y=temp_first_ind_data,
                        mode="lines",
                        line=dict(width=3, color='#60BFE1'),
                        name="First Ind",
                    ),

                    # Second Plot
                    go.Scatter(
                        x=plot_index,
                        y=temp_second_ind_data,
                        mode="lines",
                        line=dict(width=3, color='#84E5AC'),
                        name="Second Ind",
                    ),
                    go.Scatter(
                        x=plot_index,
                        y=np.where(
                            temp_combine_array,
                            temp_second_ind_data,
                            np.nan,
                        ),
                        mode="markers",
                        marker=dict(size=3, color='yellow'),
                        name="Combo Signals",
                    ),
                ],
            )
            fig.update_xaxes(rangeslider_visible=False)
            fig.update_layout(height=500, title="Last Column of the Results")
            fig.show()

        elif not first_eval_data_needs_prices and not second_eval_data_needs_prices:
            fig = go.Figure(
                data=[
                    # First Plot
                    go.Scatter(
                        x=plot_index,
                        y=temp_first_ind_data,
                        mode="lines",
                        line=dict(width=2, color='green'),
                        name="First Ind",
                    ),

                    # Second Plot
                    go.Scatter(
                        x=plot_index,
                        y=temp_second_ind_data,
                        mode="lines",
                        line=dict(width=3, color='red'),
                        name="Second Ind",
                    ),
                    go.Scatter(
                        x=plot_index,
                        y=np.where(
                            temp_combine_array,
                            temp_second_ind_data,
                            np.nan,
                        ),
                        mode="markers",
                        marker=dict(size=3, color='yellow'),
                        name="Combo Signals",
                    ),
                ],
            )
            fig.update_xaxes(rangeslider_visible=False)
            fig.update_layout(height=500, title="Last Column of the Results")
            fig.show()

    return pd.DataFrame(
        combine_array,
        index=second_eval_data.index,
        columns=pd.MultiIndex.from_tuples(
            tuples=list(pd_multind_tuples),
            names=pd_col_names,
        ),
    )


def eval_is_above(
    want_to_evaluate: pdFrame,
    user_args: Union[list[int, float], int, float, Array1d] = None,
    indicator_data: pdFrame = None,
    prices: pdFrame = None,
    cand_ohlc: str = None,
    plot_results: bool = False,
) -> pdFrame:
    if not isinstance(want_to_evaluate, pdFrame):
        raise ValueError("Data must be a dataframe with multindex")

    want_to_evaluate_values = want_to_evaluate.values
    want_to_evaluate_name = want_to_evaluate.columns.names[1].split("_")[0]
    pd_col_names = list(want_to_evaluate.columns.names) + [
        want_to_evaluate_name + "_is_above"
    ]
    pd_multind_tuples = ()

    if isinstance(user_args, (list, Array1d)):
        if not all(isinstance(x, (int, float, np.int_, np.float_)) for x in user_args):
            raise ValueError("user_args must be a list of ints or floats")
        user_args = np.asarray(user_args)

        eval_array = np.empty(
            (want_to_evaluate.shape[0], want_to_evaluate.shape[1] * user_args.size), dtype=np.bool_
        )

        eval_array_counter = 0
        temp_eval_values = want_to_evaluate.values.T
        for count, value in enumerate(want_to_evaluate.values.T):
            for eval_col in range(user_args.size):
                eval_array[:, eval_array_counter] = np.where(
                    value > user_args[eval_col], True, False
                )
                eval_array_counter += 1

                pd_multind_tuples = pd_multind_tuples + (
                    want_to_evaluate.columns[count] + (user_args[eval_col],),
                )

        if plot_results:
            temp_eval_values = want_to_evaluate.iloc[:, -1].values
            plot_index = want_to_evaluate.index

            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=plot_index,
                        y=temp_eval_values,
                        mode="lines",
                        line=dict(width=2),
                        name=want_to_evaluate_name,
                    ),
                    go.Scatter(
                        x=plot_index,
                        y=np.where(
                            eval_array[:, -1],
                            temp_eval_values,
                            np.nan,
                        ),
                        mode="markers",
                        marker=dict(size=4),
                        name="Signals",
                    ),
                ]
            )
            fig.update_layout(height=500, title="Last Column of the Results")
            fig.show()

    elif isinstance(prices, pdFrame):
        if cand_ohlc == None or cand_ohlc.lower() not in (
            "open",
            "high",
            "low",
            "close",
        ):
            raise ValueError(
                "cand_ohlc must be open, high, low or close when sending price data"
            )

        eval_array = np.empty_like(want_to_evaluate, dtype=np.bool_)
        symbols = list(prices.columns.levels[0])
        eval_array_counter = 0

        for symbol in symbols:
            temp_prices_values = prices[symbol][cand_ohlc].values
            if not all(isinstance(x, (np.int_, np.float_)) for x in temp_prices_values):
                raise ValueError("price data must be ints or floats")

            temp_eval_values = want_to_evaluate[symbol].values.T

            for values in temp_eval_values:
                eval_array[:, eval_array_counter] = np.where(
                    values > temp_prices_values, True, False
                )

                pd_multind_tuples = pd_multind_tuples + (
                    want_to_evaluate.columns[eval_array_counter] +
                    (cand_ohlc,),
                )
                eval_array_counter += 1

        if plot_results:
            temp_prices = prices[prices.columns.levels[0][-1]]
            temp_eval_values = want_to_evaluate.iloc[:, -1].values
            plot_index = want_to_evaluate.index

            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=plot_index,
                        open=temp_prices.open,
                        high=temp_prices.high,
                        low=temp_prices.low,
                        close=temp_prices.close,
                        name="Candles",
                    ),
                    go.Scatter(
                        x=plot_index,
                        y=temp_eval_values,
                        mode="lines",
                        line=dict(width=4, color='lightblue'),
                        name=want_to_evaluate_name,
                    ),
                    go.Scatter(
                        x=plot_index,
                        y=np.where(
                            eval_array[:, -1],
                            temp_eval_values,
                            np.nan,
                        ),
                        mode="markers",
                        marker=dict(size=3, color='yellow'),
                        name="Signals",
                    ),
                ]
            )
            fig.update_xaxes(rangeslider_visible=False)
            fig.update_layout(height=500, title="Last Column of the Results")
            fig.show()

        return pd.DataFrame(
            eval_array,
            index=want_to_evaluate.index,
            columns=pd.MultiIndex.from_tuples(
                tuples=list(pd_multind_tuples),
                names=pd_col_names,
            ),
        ).swaplevel(1, -1, axis=1)

    elif isinstance(indicator_data, pdFrame):
        want_to_evaluate_name = want_to_evaluate.columns.names[-1].split("_")[
            1]
        indicator_data_name = indicator_data.columns.names[-1].split("_")[0]

        pd_col_names = list(want_to_evaluate.columns.names) + [
            want_to_evaluate_name + "_is_above"
        ]

        want_to_evaluate_settings_tuple_list = want_to_evaluate.columns.to_list()

        eval_array = np.empty_like(want_to_evaluate,  dtype=np.bool_,)
        pd_multind_tuples = ()

        indicator_data_levels = list(indicator_data.columns)
        eval_array_counter = 0

        for level in indicator_data_levels:
            temp_indicator_values = indicator_data[level].values
            temp_evaluate_values = want_to_evaluate[level].values.T

            for values in temp_evaluate_values:
                eval_array[:, eval_array_counter] = np.where(
                    values > temp_indicator_values,
                    True,
                    False,
                )
                pd_multind_tuples = pd_multind_tuples + \
                    (want_to_evaluate_settings_tuple_list[eval_array_counter] + (
                        indicator_data_name,),)
                eval_array_counter += 1

        if plot_results:
            temp_eval_values = want_to_evaluate.iloc[:, -1].values
            temp_ind_values = indicator_data.iloc[:, -1].values
            plot_index = want_to_evaluate.index

            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=plot_index,
                        y=temp_ind_values,
                        mode="lines",
                        line=dict(width=2),
                        name=want_to_evaluate_name,
                    ),
                    go.Scatter(
                        x=plot_index,
                        y=temp_eval_values,
                        mode="lines",
                        line=dict(width=2),
                        name=want_to_evaluate_name,
                    ),
                    go.Scatter(
                        x=plot_index,
                        y=np.where(
                            eval_array[:, -1],
                            temp_eval_values,
                            np.nan,
                        ),
                        mode="markers",
                        marker=dict(size=4),
                        name="Signals",
                    ),
                ]
            )
            fig.update_layout(height=500, title="Last Column of the Results")
            fig.show()

    elif isinstance(user_args, (int, float)):
        eval_array = np.where(want_to_evaluate_values > user_args, True, False)

        for col in range(want_to_evaluate.shape[1]):
            pd_multind_tuples = pd_multind_tuples + (
                want_to_evaluate.columns[col] + (user_args,),
            )

        if plot_results:
            temp_eval_values = want_to_evaluate.iloc[:, -1].values
            plot_index = want_to_evaluate.index

            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=plot_index,
                        y=temp_eval_values,
                        mode="lines",
                        line=dict(width=2),
                        name=want_to_evaluate_name,
                    ),
                    go.Scatter(
                        x=plot_index,
                        y=np.where(
                            eval_array[:, -1],
                            temp_eval_values,
                            np.nan,
                        ),
                        mode="markers",
                        marker=dict(size=4),
                        name="Signals",
                    ),
                ]
            )
            fig.update_layout(height=500, title="Last Column of the Results")
            fig.show()
    else:
        raise ValueError(
            "something is wrong with what you sent please make sure the type of variable you are sending matches with the type required"
        )
    return pd.DataFrame(
        eval_array,
        index=want_to_evaluate.index,
        columns=pd.MultiIndex.from_tuples(
            tuples=list(pd_multind_tuples),
            names=pd_col_names,
        ),
    )


def eval_is_below(
    want_to_evaluate: pdFrame,
    user_args: Union[list[int, float], int, float, Array1d] = None,
    indicator_data: pdFrame = None,
    prices: pdFrame = None,
    cand_ohlc: str = None,
    plot_results: bool = False,
) -> pdFrame:
    """
    _summary_

    Parameters
    ----------
    want_to_evaluate : pdFrame
        _description_
    user_args : Union[list[int, float], int, float, Array1d], optional
        _description_, by default None
    indicator_data : pdFrame, optional
        _description_, by default None
    prices : pdFrame, optional
        _description_, by default None
    cand_ohlc : str, optional
        _description_, by default None
    plot_results : bool, optional
        _description_, by default False

    Returns
    -------
    pdFrame
        _description_

    Raises
    ------
    ValueError
        _description_
    ValueError
        _description_
    ValueError
        _description_
    ValueError
        _description_
    ValueError
        _description_
    """
    if not isinstance(want_to_evaluate, pdFrame):
        raise ValueError("Data must be a dataframe with multindex")

    want_to_evaluate_values = want_to_evaluate.values
    want_to_evaluate_name = want_to_evaluate.columns.names[1].split("_")[0]
    pd_col_names = list(want_to_evaluate.columns.names) + [
        want_to_evaluate_name + "_is_below"
    ]
    pd_multind_tuples = ()

    if isinstance(user_args, (list, Array1d)):
        if not all(isinstance(x, (int, float, np.int_, np.float_)) for x in user_args):
            raise ValueError("user_args must be a list of ints or floats")
        user_args = np.asarray(user_args)

        eval_array = np.empty(
            (want_to_evaluate.shape[0], want_to_evaluate.shape[1] * user_args.size), dtype=np.bool_
        )

        eval_array_counter = 0
        temp_eval_values = want_to_evaluate.values.T
        for count, value in enumerate(want_to_evaluate.values.T):
            for eval_col in range(user_args.size):
                eval_array[:, eval_array_counter] = np.where(
                    value < user_args[eval_col], True, False
                )
                eval_array_counter += 1

                pd_multind_tuples = pd_multind_tuples + (
                    want_to_evaluate.columns[count] + (user_args[eval_col],),
                )

        if plot_results:
            temp_eval_values = want_to_evaluate.iloc[:, -1].values
            plot_index = want_to_evaluate.index

            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=plot_index,
                        y=temp_eval_values,
                        mode="lines",
                        line=dict(width=2),
                        name=want_to_evaluate_name,
                    ),
                    go.Scatter(
                        x=plot_index,
                        y=np.where(
                            eval_array[:, -1],
                            temp_eval_values,
                            np.nan,
                        ),
                        mode="markers",
                        marker=dict(size=4),
                        name="Signals",
                    ),
                ]
            )
            fig.update_layout(height=500, title="Last Column of the Results")
            fig.show()

    elif isinstance(prices, pdFrame):
        if cand_ohlc == None or cand_ohlc.lower() not in (
            "open",
            "high",
            "low",
            "close",
        ):
            raise ValueError(
                "cand_ohlc must be open, high, low or close when sending price data"
            )

        eval_array = np.empty_like(want_to_evaluate, dtype=np.bool_)
        symbols = list(prices.columns.levels[0])
        eval_array_counter = 0

        for symbol in symbols:
            temp_prices_values = prices[symbol][cand_ohlc].values
            if not all(isinstance(x, (np.int_, np.float_)) for x in temp_prices_values):
                raise ValueError("price data must be ints or floats")

            temp_eval_values = want_to_evaluate[symbol].values.T

            for values in temp_eval_values:
                eval_array[:, eval_array_counter] = np.where(
                    values < temp_prices_values, True, False
                )

                pd_multind_tuples = pd_multind_tuples + (
                    want_to_evaluate.columns[eval_array_counter] +
                    (cand_ohlc,),
                )
                eval_array_counter += 1

        if plot_results:
            temp_prices = prices[prices.columns.levels[0][-1]]
            temp_eval_values = want_to_evaluate.iloc[:, -1].values
            plot_index = want_to_evaluate.index

            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=plot_index,
                        open=temp_prices.open,
                        high=temp_prices.high,
                        low=temp_prices.low,
                        close=temp_prices.close,
                        name="Candles",
                    ),
                    go.Scatter(
                        x=plot_index,
                        y=temp_eval_values,
                        mode="lines",
                        line=dict(width=4, color='lightblue'),
                        name=want_to_evaluate_name,
                    ),
                    go.Scatter(
                        x=plot_index,
                        y=np.where(
                            eval_array[:, -1],
                            temp_eval_values,
                            np.nan,
                        ),
                        mode="markers",
                        marker=dict(size=3, color='yellow'),
                        name="Signals",
                    ),
                ]
            )
            fig.update_xaxes(rangeslider_visible=False)
            fig.update_layout(height=500, title="Last Column of the Results")
            fig.show()

        return pd.DataFrame(
            eval_array,
            index=want_to_evaluate.index,
            columns=pd.MultiIndex.from_tuples(
                tuples=list(pd_multind_tuples),
                names=pd_col_names,
            ),
        ).swaplevel(1, -1, axis=1)

    elif isinstance(indicator_data, pdFrame):
        want_to_evaluate_name = want_to_evaluate.columns.names[-1].split("_")[
            1]
        indicator_data_name = indicator_data.columns.names[-1].split("_")[0]

        pd_col_names = list(want_to_evaluate.columns.names) + [
            want_to_evaluate_name + "_is_below"
        ]

        want_to_evaluate_settings_tuple_list = want_to_evaluate.columns.to_list()

        eval_array = np.empty_like(want_to_evaluate,  dtype=np.bool_,)
        pd_multind_tuples = ()

        indicator_data_levels = list(indicator_data.columns)
        eval_array_counter = 0

        for level in indicator_data_levels:
            temp_indicator_values = indicator_data[level].values
            temp_evaluate_values = want_to_evaluate[level].values.T

            for values in temp_evaluate_values:
                eval_array[:, eval_array_counter] = np.where(
                    values < temp_indicator_values,
                    True,
                    False,
                )
                pd_multind_tuples = pd_multind_tuples + \
                    (want_to_evaluate_settings_tuple_list[eval_array_counter] + (
                        indicator_data_name,),)
                eval_array_counter += 1

        if plot_results:
            temp_eval_values = want_to_evaluate.iloc[:, -1].values
            temp_ind_values = indicator_data.iloc[:, -1].values
            plot_index = want_to_evaluate.index

            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=plot_index,
                        y=temp_ind_values,
                        mode="lines",
                        line=dict(width=2),
                        name=want_to_evaluate_name,
                    ),
                    go.Scatter(
                        x=plot_index,
                        y=temp_eval_values,
                        mode="lines",
                        line=dict(width=2),
                        name=want_to_evaluate_name,
                    ),
                    go.Scatter(
                        x=plot_index,
                        y=np.where(
                            eval_array[:, -1],
                            temp_eval_values,
                            np.nan,
                        ),
                        mode="markers",
                        marker=dict(size=4),
                        name="Signals",
                    ),
                ]
            )
            fig.update_layout(height=500, title="Last Column of the Results")
            fig.show()

    elif isinstance(user_args, (int, float)):
        eval_array = np.where(want_to_evaluate_values < user_args, True, False)

        for col in range(want_to_evaluate.shape[1]):
            pd_multind_tuples = pd_multind_tuples + (
                want_to_evaluate.columns[col] + (user_args,),
            )

        if plot_results:
            temp_eval_values = want_to_evaluate.iloc[:, -1].values
            plot_index = want_to_evaluate.index

            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=plot_index,
                        y=temp_eval_values,
                        mode="lines",
                        line=dict(width=2),
                        name=want_to_evaluate_name,
                    ),
                    go.Scatter(
                        x=plot_index,
                        y=np.where(
                            eval_array[:, -1],
                            temp_eval_values,
                            np.nan,
                        ),
                        mode="markers",
                        marker=dict(size=4),
                        name="Signals",
                    ),
                ]
            )
            fig.update_layout(height=500, title="Last Column of the Results")
            fig.show()
    else:
        raise ValueError(
            "something is wrong with what you sent please make sure the type of variable you are sending matches with the type required"
        )
    return pd.DataFrame(
        eval_array,
        index=want_to_evaluate.index,
        columns=pd.MultiIndex.from_tuples(
            tuples=list(pd_multind_tuples),
            names=pd_col_names,
        ),
    )
