import os
import numpy as np
import pandas as pd

path_to_data = f"{os.getcwd()}/data"

# Baseline LAU
df_pillar_baseline_lau_18_19 = pd.read_csv(f"{path_to_data}/df-baseline-18-19.csv").set_index('Pillar')

# KPI-level (sub-pillar) LAU and Cost
df_kpi_fdp_cost = pd.read_csv(f"{path_to_data}/df-kpi-fdp-cost.csv").set_index(['Pillar', 'KPI'])
df_kpi_fdp_lau = pd.read_csv(f"{path_to_data}/df-kpi-fdp-lau.csv").set_index(['Pillar', 'KPI'])

# Cost per LAU
df_kpi_fdp_cost_per_lau = pd.eval('df_kpi_fdp_cost/df_kpi_fdp_lau')

# KPI Rank
df_kpi_rank = df_kpi_fdp_cost_per_lau.rank()

# % of LAU contributed by KPI
df_kpi_lau_ratio = \
(df_kpi_fdp_lau
 .reset_index()
 .groupby(['Pillar'])
 .apply(lambda fr: fr.set_index('KPI').apply(lambda c: c/c.sum())))

# Pillar-level LAU and Cost

df_pillar_fdp_lau = \
(df_kpi_fdp_lau
 .reset_index()
 .drop('KPI', axis=1)
 .groupby('Pillar')
 .sum())

df_pillar_fdp_cost = \
(df_kpi_fdp_cost
 .reset_index()
 .drop('KPI', axis=1)
 .groupby('Pillar')
 .sum())

# cost per lau - pillar level
df_pillar_fdp_cost_per_lau = pd.eval('df_pillar_fdp_cost/df_pillar_fdp_lau')

# Minimum Cost of Pillar
df_pillar_min_cost = pd.read_csv(f"{path_to_data}/df-pillar-min-cost.csv").set_index('Pillar')

df_kpi_level_minimum_allocation_all_markets = pd.read_csv(f"{path_to_data}/df_kpi_level_minimum_allocation_all_markets.csv")

df_pillar_minimum_additional_lau = \
df_kpi_level_minimum_allocation_all_markets.pivot_table(index='Pillar',
                                                        columns='Market',
                                                        values='minimum_lau',
                                                        aggfunc='sum')


def budget_allocation_for_target_LAU(MARKET: str,
                                     lau_target: int,
                                     df_kpi_fdp_cost_per_lau: pd.DataFrame,
                                     df_pillar_min_cost: pd.DataFrame,
                                     df_kpi_level_minimum_allocation_all_markets: pd.DataFrame,
                                     verbose=False):
    """
    Calculates the budget needed for acquiring the specified number of LAUs

    1 - Allocates the minimum pillar budgets
    2 - Calculates LAU that will be acquired with the minimum investment
    3 - Assign balance LAU to KPIs in order of their rank
    4 - Calculate the additional costs for each KPI
    5 - Aggregate the costs and LAUs at the pillar level
    """
    df_initial_allocation = (df_kpi_level_minimum_allocation_all_markets
                             .query(f"Market == '{MARKET}'")
                             .drop('Market', axis=1))

    minimum_lau = df_initial_allocation.minimum_lau.sum()
    balance_lau = lau_target - minimum_lau

    list_srs = []
    additional_cost = 0

    for KPI in df_initial_allocation.sort_values('Rank_KPI').loc[:, 'KPI'].tolist():
        """
        For each KPI (by order of rank), check if there are LAU that need to be allocated
        Yes: calculate #-LAUs that the KPI can take (based on FDP Cost and Cost-per-LAU)
        """
        srs = df_initial_allocation.query(f"KPI == '{KPI}'").squeeze()

        if balance_lau > 0 and srs['minimum_cost'] < srs['Cost_FDP_KPI']:

            srs['additional_lau'] = min((srs['Cost_FDP_KPI'] - srs['minimum_cost']) / srs['cost_per_lau'],
                                        balance_lau)
            srs['additional_cost'] = srs['additional_lau'] * srs['cost_per_lau']

            balance_lau = balance_lau - srs['additional_lau']

            print(f"Allocated ${int(srs['additional_cost']):,d} to [{srs['Pillar']}: {KPI}] ... remaining={int(balance_lau):,d}") if verbose else ""
        else:
            srs['additional_lau'] = 0
            srs['additional_cost'] = 0
        list_srs.append(srs)

    return (
        pd.concat(list_srs, axis=1)
        .T.set_index(['Pillar', 'KPI'])
        .apply(lambda c: pd.to_numeric(c))
        .sort_index(axis=1)
    )

# ------------------------------------------------------------------------
# Function to create data needed for displaying Market Submission View
# ------------------------------------------------------------------------


def get_initial_submission_table(MARKET: str, LAU_TARGET: int):
    """
    """
    df = \
    budget_allocation_for_target_LAU(MARKET=MARKET,
                                     lau_target=LAU_TARGET,
                                     df_kpi_fdp_cost_per_lau=df_kpi_fdp_cost_per_lau,
                                     df_pillar_min_cost=df_pillar_min_cost,
                                     df_kpi_level_minimum_allocation_all_markets=df_kpi_level_minimum_allocation_all_markets)

    df_budget_alloc_KPI_level = \
    (df
     .astype(int)
     .eval("total_cost = minimum_cost + additional_cost")
     .eval("total_lau = minimum_lau + additional_lau")
     .eval("total_cost_as_perc_fdp = total_cost/Cost_FDP_KPI")
     .drop(['Cost_FDP_KPI', 'Rank_KPI'], axis=1))

    df_budget_alloc_pillar_level = \
    (df_budget_alloc_KPI_level
     .reset_index()
     .drop('KPI', axis=1)
     .groupby('Pillar')
     .sum()
    )

    total_budget = f"Budget=${int(df_budget_alloc_pillar_level['total_cost'].sum().round()/10**3):,d}k"

    lau_by_pillar = \
    (pd.concat([
        df_pillar_baseline_lau_18_19[MARKET].divide(10**3).rename('Baseline'),
        df_pillar_minimum_additional_lau[MARKET].rename('Minimum'),
        df_budget_alloc_pillar_level['total_lau'].rename('Submitted'),
        df_pillar_fdp_lau[MARKET].divide(10**3).rename('FDP')
    ], axis=1, sort=True)
     .round()
     .astype(int)
     .applymap(lambda i: f"{int(i):,d}K"))

    return {
        'total_budget': total_budget,
        'lau_by_pillar': lau_by_pillar
    }
