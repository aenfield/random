# SQL → pandas: Deep guide — selecting, joins, aggregation, windows, and more

**Goal:** A practical, opinionated reference that shows how to translate "normal SQL things" into pandas + Python — with code examples, caveats, performance tips, and recipes for tricky parts (dates, floats, NULLs, window functions, CTE-style workflows).

> This document assumes you know basic pandas (`import pandas as pd`, `import numpy as np`) and SQL. Examples use `pd.DataFrame` objects named `df`, `left`, `right`, `transactions`, etc.

---

## Quick mapping (cheat sheet)

- `SELECT col1, col2 FROM table` → `df[['col1', 'col2']]` or `df.loc[:, ['col1','col2']]`
- `SELECT *` → `df` (entire DataFrame)
- `WHERE condition` → boolean indexing: `df[df['x'] > 5]` or `df.query('x > 5 and y == "A"')`
- `ORDER BY x DESC` → `df.sort_values('x', ascending=False)`
- `LIMIT n` → `df.head(n)` or `df.iloc[:n]`
- `GROUP BY a` → `df.groupby('a').agg(...)` (or `.apply`, `.transform`)
- aggregation `SUM`, `AVG`, `COUNT` → `.sum()`, `.mean()`, `.count()` inside `.agg`
- window functions: `LEAD/LAG` → `groupby('p')['v'].shift(-1/1)`; `ROW_NUMBER()` → `groupby('p').cumcount()+1`; `RANK()` → `.rank()`
- `JOIN` → `pd.merge(left, right, how='inner', on='key')` (`how` in `{ 'left','right','inner','outer','cross' }`)
- `UNION` → `pd.concat([df1, df2], ignore_index=True).drop_duplicates()` if `UNION` (unique); omit `drop_duplicates()` for `UNION ALL`
- `EXCEPT` / `MINUS` → `merge(..., indicator=True)` then filter where `_merge == 'left_only'` or use boolean `~df1['key'].isin(df2['key'])`
- `DISTINCT` → `df.drop_duplicates(subset=['col1','col2'])`
- `CASE WHEN` → `np.where(condition, val_if_true, val_if_false)` or `pd.Series.map` or `pd.cut` for binned conditions

---

## 1. Setup & small examples

```python
import pandas as pd
import numpy as np

left = pd.DataFrame({'id':[1,2,3,4], 'val_left':[10,20,30,40]})
right = pd.DataFrame({'id':[3,4,5], 'val_right':[300,400,500]})

# selecting columns
left[['id','val_left']]

# filtering
left[left['val_left'] > 15]
# or
left.query('val_left > 15')

# sort & limit
left.sort_values('val_left', ascending=False).head(2)
```

---

## 2. Selecting & filtering — details and gotchas

### Column selection
- Use `df[['a','b']]` for selecting columns (returns DataFrame). `df['a']` returns a Series.
- `df.loc[:, 'a':'d']` supports slice by column labels. `df.iloc[:, 0:2]` is positional.
- Avoid chained indexing assignment (use `.loc[row_sel, col_sel] = ...` to avoid `SettingWithCopyWarning`).

### Boolean indexing
- Standard: `df[df['x'] > 3]`.
- Combine conditions with `&` / `|` and wrap each condition in parentheses: `df[(df['x']>3) & (df['y']=='A')]`.
- Use `.query()` for readable string-based filters. It can be faster for complex expressions.

### Nulls / missing values
- SQL `IS NULL` ⇨ `df['col'].isna()` or `df['col'].isnull()`.
- `IS NOT NULL` ⇨ `df['col'].notna()`.
- To remove rows with any nulls: `df.dropna()`; on a subset: `df.dropna(subset=['a','b'])`.
- To replace nulls: `df['col'].fillna(value)` or `df.fillna({ 'a':0, 'b':'unknown' })`.

### Strings
- SQL `LIKE '%foo%'` ⇨ `df['s'].str.contains('foo', na=False)` (remember `na=False` to treat NaN as False).
- Case-insensitive: `df['s'].str.contains('foo', case=False, na=False)`.

### Between / IN
- `col BETWEEN x AND y` ⇨ `df[df['col'].between(x, y)]`.
- `col IN (a,b,c)` ⇨ `df[df['col'].isin(['a','b','c'])]`.

### Dates & times (special care)
- Convert input to datetime: `df['date'] = pd.to_datetime(df['date'], errors='coerce')`.
- Filter by date: `df[df['date'] >= '2024-01-01']` works if dtype is datetime64[ns]. Otherwise convert first.
- Extract parts: `df['date'].dt.year`, `.dt.month`, `.dt.date`, `.dt.floor('D')`, `.dt.tz_localize(...)`.
- Beware of timezone-naive vs timezone-aware Timestamps; use `.dt.tz_localize()` to assign a timezone to naive timestamps and `.dt.tz_convert()` to change timezones.

Example:
```python
df['ts'] = pd.to_datetime(df['ts'])
df[df['ts'].dt.date == pd.Timestamp('2024-08-01').date()]
``` 

### Floating point comparisons
- Don’t test equality `df[df['x'] == 0.1]` when values are the result of arithmetic — use `np.isclose`:
```python
mask = np.isclose(df['x'], 0.1, atol=1e-8, rtol=1e-5)
df[mask]
```
- For financial values prefer integer cents (store as `int64`) or `Decimal` for exactness if necessary.

---

## 3. Joins (SQL JOIN) — `merge`, `join`, `concat`

### `pd.merge` (most SQL-like)
```python
pd.merge(left, right, how='inner', on='id')
pd.merge(left, right, how='left', left_on='lkey', right_on='rkey', suffixes=('_L','_R'))
```
- `how`: `'left'`, `'right'`, `'outer'`, `'inner'`, `'cross'` (cross available in modern pandas).
- `indicator=True` adds a `_merge` column with values `'left_only'`, `'right_only'`, `'both'` — useful to implement `EXCEPT` / `INTERSECT` semantics.
- `validate` helps check assumptions, e.g., `validate='one_to_many'`.

### Joining on index
- `left.join(right, how='left')` joins on index by default; or `left.join(right.set_index('key'), on='key')`.

### UNION / CONCAT
- `UNION ALL` ⇨ `pd.concat([df1, df2], ignore_index=True)`.
- `UNION` (distinct) ⇨ `pd.concat([...]).drop_duplicates()`.

### INTERSECT / EXCEPT
- INTERSECT: `pd.merge(df1, df2, how='inner')` on the relevant columns and optionally `.drop_duplicates()`.
- EXCEPT (rows in `df1` not in `df2`):

```python
m = df1.merge(df2, how='left', indicator=True)
result = m[m['_merge'] == 'left_only'].drop(columns=['_merge'])
```

or use `~df1[['k']].isin(df2[['k']])` for single-key cases.

---

## 4. Aggregation, GROUP BY, HAVING

### Simple aggregation
```python
# SQL: SELECT a, SUM(x) AS total FROM t GROUP BY a
df.groupby('a', as_index=False).agg(total=('x','sum'))
```
- Named aggregation (clean): `df.groupby('a').agg(total=('x','sum'), avg_x=('x','mean'))`.
- Use `as_index=False` if you want grouped columns to stay as columns (not index).

### Multiple aggregation functions
```python
df.groupby('a').agg({'x':['sum','mean','count'], 'y':'max'})
# or named
df.groupby('a').agg(total_x=('x','sum'), avg_x=('x','mean'), max_y=('y','max'))
```

### HAVING (filter groups)
- Compute aggregated value and filter: 
```python
grouped = df.groupby('a').agg(total=('x','sum')).reset_index()
filtered = grouped[grouped['total'] > 100]
# If you need original rows for those groups:
result = df[df['a'].isin(filtered['a'])]
```
- Alternative: `filter` on GroupBy: `df.groupby('a').filter(lambda g: g['x'].sum() > 100)` (returns rows from groups that pass predicate).

### Per-row aggregated value (window-style)
- SQL: `SELECT *, SUM(x) OVER (PARTITION BY a) AS tot FROM t`
- pandas: `df['tot'] = df.groupby('a')['x'].transform('sum')` (transform returns a Series aligned to original index).

---

## 5. Window functions (LEAD, LAG, ROW_NUMBER, RANK)

Window functions are the trickiest to map, but pandas provides the building blocks. The typical pattern is to sort, then use `groupby` combined with `shift`, `rank`, `cumcount`, or `rolling`.

### LEAD / LAG
```python
# LAG 1 within partition
df = df.sort_values(['partition_col','order_col'])
df['lag_val'] = df.groupby('partition_col')['value'].shift(1)
# LEAD = shift(-1)
df['lead_val'] = df.groupby('partition_col')['value'].shift(-1)
```

### ROW_NUMBER() over partition ORDER BY
```python
# row number (1-based)
df = df.sort_values(['partition_col','order_col'], ascending=[True, False])
df['row_number'] = df.groupby('partition_col').cumcount() + 1
```

`cumcount()` respects the ordering produced by your `sort_values` call.

### RANK / DENSE_RANK
```python
# rank within partition
df['rank'] = df.groupby('partition_col')['value'].rank(method='min', ascending=False)
# dense rank
df['dense_rank'] = df.groupby('partition_col')['value'].rank(method='dense', ascending=False)
```

`method` choices: `'average', 'min', 'max', 'first', 'dense'` — choose based on how you want ties handled.

### WINDOW aggregates (rolling/expanding/ewm)
- Rolling: fixed-size sliding window: `df['rolling_avg'] = df.groupby('grp')['v'].rolling(window=3, min_periods=1).mean()` but note the result is a Series with a MultiIndex (group key + original index), so use `.reset_index(level=0, drop=True)` to align back.
- Expanding: cumulative window from the start: `df.groupby('grp')['v'].expanding().mean()` (also returns a MultiIndex).
- Exponential weighted: `df.groupby('grp')['v'].apply(lambda s: s.ewm(span=5).mean())`.

Example aligning Rolling result back:
```python
s = df.sort_values(['grp','date']).groupby('grp')['v'].rolling(window=3, min_periods=1).mean()
s = s.reset_index(level=0, drop=True)  # aligns with df index
df['rolling_v'] = s
```

---

## 6. Subqueries & CTE-style workflows

SQL CTEs are just named temporary results. In pandas do the same by creating intermediate DataFrames and name them clearly — or chain with `.pipe()` and small helper functions.

Example SQL: `WITH s AS (SELECT a, SUM(x) as tot FROM t GROUP BY a) SELECT t.* FROM t JOIN s USING (a) WHERE s.tot > 100`.

pandas:
```python
s = df.groupby('a', as_index=False).agg(tot=('x','sum'))
s2 = s[s['tot'] > 100]
res = df.merge(s2, on='a', how='inner')
```

`pipe` pattern for chaining nicely:
```python
def top_groups(df, min_total=100):
    s = df.groupby('a', as_index=False).agg(tot=('x','sum'))
    return s[s['tot'] > min_total]

res = (
    df
    .pipe(top_groups, min_total=100)
    .merge(df, on='a')
)
```

### Emulating correlated subqueries
- If your SQL uses a correlated subquery (per-row lookup of an aggregate), prefer `groupby.transform` so the aggregate aligns to rows. Example: `HAVING value > (SELECT AVG(value) FROM table WHERE group=outer.group)` → `df['avg_by_grp'] = df.groupby('grp')['value'].transform('mean')` then filter `df[df['value'] > df['avg_by_grp']]`.

---

## 7. Advanced aggregates and custom behavior

### Named aggregations & renaming
```python
df.groupby(['a','b'], as_index=False).agg(
    total_amount=('amount', 'sum'),
    mean_price=('price', 'mean'),
    n_orders=('order_id', 'count')
)
```

### Custom aggregation functions
- Pass a Python function: `df.groupby('a').agg(myfunc=('x', lambda s: custom(s)))` or use `.agg({'x': lambda s: ...})`.
- For performance, prefer built-in numpy/pandas functions (sum, mean) which are vectorised; custom Python functions trigger Python-level loops and are slower.

### Multiple roll-ups / multi-index aggregation
- `df.groupby(['a','b']).agg(...)` returns MultiIndex column names when using multiple functions; use `reset_index()` and/or named aggregations to keep things tidy.

---

## 8. Common SQL patterns & pandas recipes

### Top N per group (SQL WITH RANK + filter)
SQL: `SELECT * FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY grp ORDER BY score DESC) rn FROM t) x WHERE rn <= 3`

pandas:
```python
df = df.sort_values(['grp','score'], ascending=[True, False])
df['rn'] = df.groupby('grp').cumcount() + 1
top3 = df[df['rn'] <= 3]
```

### Join an aggregated result back to rows (GROUP BY then JOIN)
```python
agg = df.groupby('user_id', as_index=False).agg(total=('amount','sum'))
res = df.merge(agg, on='user_id', how='left')
```

### Windowed difference (value - previous value)
```python
df['prev_val'] = df.groupby('grp')['value'].shift(1)
df['diff'] = df['value'] - df['prev_val']
```

### Distinct count (approx)
- Exact distinct: `df['user_id'].nunique()` or `df.drop_duplicates(subset=['user_id'])`.
- For very large data, consider specialized tools (not covered here).

---

## 9. Set operations & existence tests

- `EXISTS` / `IN` → `df['col'].isin(other_df['col'])` or merge with `indicator=True`.
- `LEFT SEMI JOIN` behaviour (SQL pattern to keep left rows that match right): `left[left['k'].isin(right['k'])]`.
- `LEFT ANTI JOIN` (keep left rows not in right): `left[~left['k'].isin(right['k'])]`.

---

## 10. Practical example — translating a complex SQL query

**SQL**:
```sql
SELECT t.user_id,
       t.region,
       SUM(t.amount) AS total,
       RANK() OVER (PARTITION BY t.region ORDER BY SUM(t.amount) DESC) AS region_rank
FROM transactions t
WHERE t.date >= '2024-01-01'
GROUP BY t.user_id, t.region
HAVING SUM(t.amount) > 1000
ORDER BY total DESC
LIMIT 10;
```

**pandas**:
```python
# ensure date
transactions['date'] = pd.to_datetime(transactions['date'], errors='coerce')
recent = transactions[transactions['date'] >= '2024-01-01']

# group & aggregate
user_totals = (
    recent
    .groupby(['user_id','region'], as_index=False)
    .agg(total=('amount','sum'))
)

# having
user_totals = user_totals[user_totals['total'] > 1000]

# rank within region
user_totals['region_rank'] = user_totals.groupby('region')['total']                                    .rank(method='dense', ascending=False)

# order & limit
top10 = user_totals.sort_values('total', ascending=False).head(10)
```

Notes: We used `groupby(...).agg(...)` to compute sums, then `groupby(...).rank(...)` to compute per-region ranks. If you wanted row-level totals attached to the original `transactions` rows, use `transform('sum')` instead of `agg`.

---

## 11. Performance tips & best practices

- Prefer vectorized functions (`.sum()`, `.mean()`, `.rank()`, `.shift()` etc.) over `apply`/`iterrows()`.
- Use `category` dtype for low-cardinality string columns used for grouping or joins (saves memory and speeds up groupby/merge).
- If joining repeatedly on the same key, consider `df.set_index('key')` and use index-based joins or re-use the index.
- Use `astype()` to set compact types where safe (e.g., `int32` instead of `int64`) to reduce memory.
- Avoid creating huge intermediate copies. Use `inplace` operations cautiously (theyn't always avoid copies).
- Use `.query()` / `pd.eval()` for complex expressions when appropriate — they can be faster and use fewer temporary objects.

---

## 12. Common pitfalls & gotchas

- `SettingWithCopyWarning`: arise when you slice a DataFrame and then try to assign to it. Use `.loc[...]` to be explicit.
- Joins with duplicate key values can expand rows (cartesian effect). Use `validate` argument in `merge` to assert assumptions: e.g., `validate='one_to_many'`.
- Sorting before `groupby().cumcount()` or `rank()` is essential — groupby operations do not automatically sort rows.
- `rolling` and `expanding` on grouped data produce MultiIndex results — you must align back to original index using `.reset_index(level=0, drop=True)`.
- Watch out for timezone-aware vs timezone-naive datetimes — comparisons may raise errors or be incorrect.

---

## 13. Quick reference examples

```python
# DISTINCT
df.drop_duplicates(subset=['a','b'])

# LIMIT/OFFSET style
df.sort_values('x', ascending=False).iloc[10:20]

# Coalesce (SQL COALESCE(a,b,c))
df['c'] = df['a'].fillna(df['b']).fillna(df['c_default'])
# or
cols = ['a','b','c_default']
df['c'] = df[cols].bfill(axis=1).iloc[:,0]

# CASE WHEN
import numpy as np
# simple
df['label'] = np.where(df['x'] > 0, 'pos', 'nonpos')
# multi-case
conditions = [df['x'] < 0, df['x'] == 0, df['x'] > 0]
choices = ['neg','zero','pos']
df['lbl'] = np.select(conditions, choices, default='unknown')

# EXISTS
mask = df['user_id'].isin(active_users['user_id'])

# Subquery (aggregate filter)
agg = df.groupby('grp').agg(total=('amt','sum')).reset_index()
keep = agg[agg['total'] > 100]['grp']
res = df[df['grp'].isin(keep)]
```

---

## 14. When SQL might be simpler — alternatives

If you *prefer* writing SQL but want to operate on pandas DataFrames, consider tools that let you run SQL directly against DataFrames (e.g., `duckdb`, `pandasql` or `sqlite3` by writing DataFrame to SQL). These trade pure pandas idioms for convenience of SQL and can be helpful for complex analytics pipelines.

---

## 15. Final words & recommended learning path

- Practice translating common queries: filtering, joins, groupby, window functions. For window functions, the combination of `sort_values`, `groupby`, `shift`, `cumcount`, `rank`, and `rolling` will cover nearly every case.
- Learn when to use `.transform()` (to return row-aligned aggregated results) vs `.agg()` (to collapse groups) vs `.apply()` (custom group operations — slower).
- Master `dtype` conversions early — many subtle bugs are due to wrong `dtype` (strings vs datetime vs numeric vs categorical).


---

## Appendix: TL;DR code snippets

(Select a few snippets from above for quick copy-paste)

```python
# join
pd.merge(left, right, how='left', on='id', indicator=True)

# per-group sum back on rows
df['group_sum'] = df.groupby('group')['amount'].transform('sum')

# rank within group
df['r'] = df.groupby('group')['amount'].rank(method='dense', ascending=False)

# lead/lag
df['prev'] = df.groupby('group')['amount'].shift(1)

# rolling mean per group (aligned)
s = df.sort_values(['group','date']).groupby('group')['v'].rolling(window=3, min_periods=1).mean()
s = s.reset_index(level=0, drop=True)
df['rolling_v'] = s
```

---

## (Optional) Further reading

- Official pandas user guide and reference for `merge`, `groupby`, `rolling`, `to_datetime`, `Series.dt`.
- pandas community tutorials and blog posts for concrete patterns (e.g., top-N per group, efficient joins, memory profiling).

---

*If you want, I can:*
- Expand any section into a longer tutorial with step-by-step exercises and test data.
- Provide a Jupyter notebook with runnable examples and synthetic datasets.
- Add a one-page printable cheat sheet PDF.
