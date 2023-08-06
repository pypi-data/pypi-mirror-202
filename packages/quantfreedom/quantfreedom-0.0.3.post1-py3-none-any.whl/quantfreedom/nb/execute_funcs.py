"""
Testing the tester
"""

import numpy as np
from numba import njit

from quantfreedom._typing import Optional
from quantfreedom.nb.helper_funcs import fill_order_records_nb, fill_strat_records_nb
from quantfreedom.nb.buy_funcs import long_increase_nb, long_decrease_nb
from quantfreedom.nb.sell_funcs import short_increase_nb, short_decrease_nb
from quantfreedom._typing import (
    RecordArray,
    Array1d,
    Optional,
)
from quantfreedom.enums.enums import (
    OrderType,
    SL_BE_or_Trail_BasedOn,
    OrderStatus,
    AccountState,
    EntryOrder,
    OrderResult,
    StopsOrder,
    StaticVariables,
)


@njit(cache=True)
def check_sl_tp_nb(
    high_price: float,
    low_price: float,
    open_price: float,
    close_price: float,
    order_settings_counter: int,
    entry_type: int,
    fee_pct: float,
    bar: int,
    account_state: AccountState,
    order_result: OrderResult,
    stops_order: StopsOrder,
    order_records_id: Optional[Array1d] = None,
    order_records: Optional[RecordArray] = None,
):
    # Check SL
    moved_sl_to_be_new = order_result.moved_sl_to_be
    moved_tsl = False
    record_sl_move = False
    order_type_new = entry_type
    price_new = order_result.price
    size_value_new = np.inf
    sl_prices_new = order_result.sl_prices
    tsl_prices_new = order_result.tsl_prices

    average_entry = order_result.average_entry

    # checking if we are in a long
    if order_type_new == OrderType.LongEntry:
        # Regular Stop Loss
        if low_price <= sl_prices_new:
            price_new = sl_prices_new
            order_type_new = OrderType.LongSL
        # Trailing Stop Loss
        elif low_price <= tsl_prices_new:
            price_new = tsl_prices_new
            order_type_new = OrderType.LongTSL
        # Liquidation
        elif low_price <= order_result.liq_price:
            price_new = order_result.liq_price
            order_type_new = OrderType.LongLiq
        # Take Profit
        elif high_price >= order_result.tp_prices:
            price_new = order_result.tp_prices
            order_type_new = OrderType.LongTP

        # Stop Loss to break even
        elif not moved_sl_to_be_new and stops_order.sl_to_be:
            if stops_order.sl_to_be_based_on == SL_BE_or_Trail_BasedOn.low_price:
                sl_be_based_on = low_price
            elif stops_order.sl_to_be_based_on == SL_BE_or_Trail_BasedOn.close_price:
                sl_be_based_on = close_price
            elif stops_order.sl_to_be_based_on == SL_BE_or_Trail_BasedOn.open_price:
                sl_be_based_on = open_price
            elif stops_order.sl_to_be_based_on == SL_BE_or_Trail_BasedOn.high_price:
                sl_be_based_on = high_price

            if (
                sl_be_based_on - average_entry
            ) / average_entry > stops_order.sl_to_be_when_pct_from_avg_entry:
                if stops_order.sl_to_be_zero_or_entry == 0:
                    # this formula only works with a 1 because it represents a size val of 1
                    # if i were to use any other value for size i would have to use the solving for tp code
                    sl_prices_new = (fee_pct * average_entry + average_entry) / (
                        1 - fee_pct
                    )
                else:
                    sl_prices_new = average_entry
                moved_sl_to_be_new = True
                order_type_new = OrderType.MovedSLtoBE
                record_sl_move = True
            price_new = np.nan
            size_value_new = np.nan

        # Trailing Stop Loss
        elif stops_order.tsl_true_or_false:
            if stops_order.tsl_based_on == SL_BE_or_Trail_BasedOn.low_price:
                trail_based_on = low_price
            elif stops_order.tsl_based_on == SL_BE_or_Trail_BasedOn.high_price:
                trail_based_on = high_price
            elif stops_order.tsl_based_on == SL_BE_or_Trail_BasedOn.open_price:
                trail_based_on = open_price
            elif stops_order.tsl_based_on == SL_BE_or_Trail_BasedOn.close_price:
                trail_based_on = close_price

            # not going to adjust every candle
            x = (
                trail_based_on - average_entry
            ) / average_entry > stops_order.tsl_when_pct_from_avg_entry
            if x:
                temp_tsl_price = (
                    trail_based_on - trail_based_on * stops_order.tsl_trail_by_pct
                )
                if temp_tsl_price > tsl_prices_new:
                    tsl_prices_new = temp_tsl_price
                    moved_tsl = True
                    order_type_new = OrderType.MovedTSL
            price_new = np.nan
            size_value_new = np.nan
        else:
            price_new = np.nan
            size_value_new = np.nan

    # checking if we are in a short
    elif order_type_new == OrderType.ShortEntry:
        # Regular Stop Loss
        if high_price >= sl_prices_new:
            price_new = sl_prices_new
            order_type_new = OrderType.ShortSL
        # Trailing Stop Loss
        elif high_price >= tsl_prices_new:
            price_new = tsl_prices_new
            order_type_new = OrderType.ShortTSL
        # Liquidation
        elif high_price >= order_result.liq_price:
            price_new = order_result.liq_price
            order_type_new = OrderType.ShortLiq
        # Take Profit
        elif low_price <= order_result.tp_prices:
            price_new = order_result.tp_prices
            order_type_new = OrderType.ShortTP

        # Stop Loss to break even
        elif not moved_sl_to_be_new and stops_order.sl_to_be:
            if stops_order.sl_to_be_based_on == SL_BE_or_Trail_BasedOn.low_price:
                sl_be_based_on = low_price
            elif stops_order.sl_to_be_based_on == SL_BE_or_Trail_BasedOn.close_price:
                sl_be_based_on = close_price
            elif stops_order.sl_to_be_based_on == SL_BE_or_Trail_BasedOn.open_price:
                sl_be_based_on = open_price
            elif stops_order.sl_to_be_based_on == SL_BE_or_Trail_BasedOn.high_price:
                sl_be_based_on = high_price

            if (
                average_entry - sl_be_based_on
            ) / average_entry > stops_order.sl_to_be_when_pct_from_avg_entry:
                if stops_order.sl_to_be_zero_or_entry == 0:
                    # this formula only works with a 1 because it represents a size val of 1
                    # if i were to use any other value for size i would have to use the solving for tp code
                    sl_prices_new = (average_entry - fee_pct * average_entry) / (
                        1 + fee_pct
                    )
                else:
                    sl_prices_new = average_entry
                moved_sl_to_be_new = True
                order_type_new = OrderType.MovedSLtoBE
                record_sl_move = True
            price_new = np.nan
            size_value_new = np.nan

        # Trailing Stop Loss
        elif stops_order.tsl_true_or_false:
            if stops_order.tsl_based_on == SL_BE_or_Trail_BasedOn.high_price:
                trail_based_on = high_price
            elif stops_order.tsl_based_on == SL_BE_or_Trail_BasedOn.close_price:
                trail_based_on = close_price
            elif stops_order.tsl_based_on == SL_BE_or_Trail_BasedOn.open_price:
                trail_based_on = open_price
            elif stops_order.tsl_based_on == SL_BE_or_Trail_BasedOn.low_price:
                trail_based_on = low_price

            # not going to adjust every candle
            x = (
                average_entry - trail_based_on
            ) / average_entry > stops_order.tsl_when_pct_from_avg_entry
            if x:
                temp_tsl_price = (
                    trail_based_on + trail_based_on * stops_order.tsl_trail_by_pct
                )
                if temp_tsl_price < tsl_prices_new:
                    tsl_prices_new = temp_tsl_price
                    moved_tsl = True
                    order_type_new = OrderType.MovedTSL
            price_new = np.nan
            size_value_new = np.nan
        else:
            price_new = np.nan
            size_value_new = np.nan

    order_result_new = OrderResult(
        average_entry=order_result.average_entry,
        fees_paid=order_result.fees_paid,
        leverage=order_result.leverage,
        liq_price=order_result.liq_price,
        moved_sl_to_be=moved_sl_to_be_new,
        order_status=order_result.order_status,
        order_status_info=order_result.order_status_info,
        order_type=order_type_new,
        pct_chg_trade=order_result.pct_chg_trade,
        position=order_result.position,
        price=price_new,
        realized_pnl=order_result.realized_pnl,
        size_value=size_value_new,
        sl_pcts=order_result.sl_pcts,
        sl_prices=sl_prices_new,
        tp_pcts=order_result.tp_pcts,
        tp_prices=order_result.tp_prices,
        tsl_pcts_init=order_result.tsl_pcts_init,
        tsl_prices=tsl_prices_new,
    )

    if order_records is not None and (record_sl_move or moved_tsl):
        fill_order_records_nb(
            bar=bar,
            order_records=order_records,
            order_settings_counter=order_settings_counter,
            order_records_id=order_records_id,
            account_state=account_state,
            order_result=order_result_new,
        )

    return order_result_new


@njit(cache=True)
def process_order_nb(
    price: float,
    bar: int,
    order_type: int,
    entries_col: int,
    order_settings_counter: int,
    symbol_counter: int,
    account_state: AccountState,
    entry_order: EntryOrder,
    order_result: OrderResult,
    static_variables_tuple: StaticVariables,
    order_records: Optional[RecordArray] = None,
    order_records_id: Optional[Array1d] = None,
    strat_records: Optional[RecordArray] = None,
    strat_records_filled: Optional[Array1d] = None,
):
    fill_strat = False
    if order_type == OrderType.LongEntry:
        account_state_new, order_result_new = long_increase_nb(
            price=price,
            entry_order=entry_order,
            order_result=order_result,
            account_state=account_state,
            static_variables_tuple=static_variables_tuple,
        )
    elif order_type == OrderType.ShortEntry:
        account_state_new, order_result_new = short_increase_nb(
            price=price,
            entry_order=entry_order,
            order_result=order_result,
            account_state=account_state,
            static_variables_tuple=static_variables_tuple,
        )
    elif OrderType.LongLiq <= order_type <= OrderType.LongTSL:
        account_state_new, order_result_new = long_decrease_nb(
            order_result=order_result,
            account_state=account_state,
            fee_pct=static_variables_tuple.fee_pct,
        )
        fill_strat = True
    elif OrderType.ShortLiq <= order_type <= OrderType.ShortTSL:
        account_state_new, order_result_new = short_decrease_nb(
            order_result=order_result,
            account_state=account_state,
            fee_pct=static_variables_tuple.fee_pct,
        )
        fill_strat = True

    if (
        fill_strat
        and strat_records is not None
        and order_result_new.order_status == OrderStatus.Filled
    ):
        fill_strat_records_nb(
            entries_col=entries_col,
            order_settings_counter=order_settings_counter,
            symbol_counter=symbol_counter,
            strat_records=strat_records,
            strat_records_filled=strat_records_filled,
            equity=account_state_new.equity,
            pnl=order_result_new.realized_pnl,
        )

    if (
        order_records is not None
        and order_result_new.order_status == OrderStatus.Filled
    ):
        fill_order_records_nb(
            bar=bar,
            order_records=order_records,
            order_settings_counter=order_settings_counter,
            order_records_id=order_records_id,
            account_state=account_state_new,
            order_result=order_result_new,
        )

    return account_state_new, order_result_new
