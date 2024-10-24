from decimal import Decimal

from mm_std import Err, Ok, fatal, print_table
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TaskID, TextColumn

from mm_balance.balances import Balances
from mm_balance.config import Config, Group
from mm_balance.price import Prices
from mm_balance.token_decimals import TokenDecimals
from mm_balance.total import Total
from mm_balance.utils import fnumber


def print_groups(balances: Balances, config: Config, prices: Prices) -> None:
    for group_index, group in enumerate(config.groups):
        group_balances = balances.get_group_balances(group_index, group.network)
        _print_group(group, group_balances, config, prices)


def _print_group(group: Group, group_balances: list[Balances.Balance], config: Config, prices: Prices) -> None:
    rows = []
    balance_sum = Decimal(0)
    usd_sum = Decimal(0)
    for address_task in group_balances:
        if isinstance(address_task.balance, Err):
            row = [address_task.address, address_task.balance.err]
        elif isinstance(address_task.balance, Ok):
            balance = address_task.balance.ok
            balance_sum += balance
            if config.skip_empty and balance == Decimal(0):
                continue
            row = [address_task.address, fnumber(balance, config.format_number_separator)]
            if config.price:
                balance_usd = round(balance * prices[group.ticker], config.round_ndigits)
                usd_sum += balance_usd
                row.append(fnumber(balance_usd, config.format_number_separator, "$"))
        else:
            fatal("address_task is None!")
        rows.append(row)

    balance_sum_str = fnumber(round(balance_sum, config.round_ndigits), config.format_number_separator)
    sum_row = ["sum", balance_sum_str]
    if config.price:
        usd_sum_str = fnumber(round(usd_sum, config.round_ndigits), config.format_number_separator, "$")
        sum_row.append(usd_sum_str)
    rows.append(sum_row)

    if group.share < Decimal(1):
        sum_share_str = fnumber(round(balance_sum * group.share, config.round_ndigits), config.format_number_separator)
        sum_share_row = [f"sum_share, {group.share}", sum_share_str]
        if config.price:
            usd_sum_share_str = fnumber(round(usd_sum * group.share, config.round_ndigits), config.format_number_separator, "$")
            sum_share_row.append(usd_sum_share_str)
        rows.append(sum_share_row)

    table_headers = ["address", "balance"]
    if config.price:
        table_headers += ["usd"]
    print_table(group.name, table_headers, rows)


def print_nodes(config: Config) -> None:
    rows = []
    for network, nodes in config.nodes.items():
        rows.append([network, "\n".join(nodes)])
    print_table("Nodes", ["network", "nodes"], rows)


def print_token_decimals(token_decimals: TokenDecimals) -> None:
    rows = []
    for network, decimals in token_decimals.items():
        rows.append([network, decimals])
    print_table("Token Decimals", ["network", "decimals"], rows)


def print_prices(config: Config, prices: Prices) -> None:
    if config.price:
        rows = []
        for ticker, price in prices.items():
            rows.append([ticker, fnumber(round(price, config.round_ndigits), config.format_number_separator, "$")])
        print_table("Prices", ["coin", "usd"], rows)


def print_total(config: Config, balances: Balances, prices: Prices) -> None:
    total = Total.calc(balances, prices, config)
    total.print()


def print_errors(config: Config, balances: Balances) -> None:
    error_balances = balances.get_errors()
    if not error_balances:
        return
    rows = []
    for balance in error_balances:
        group = config.groups[balance.group_index]
        rows.append([group.ticker + " / " + group.network, balance.address, balance.balance.err])  # type: ignore[union-attr]
    print_table("Errors", ["coin", "address", "error"], rows)


def create_progress_bar() -> Progress:
    return Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
    )


def create_progress_task(progress: Progress, description: str, total: int) -> TaskID:
    return progress.add_task("[green]" + description, total=total)
