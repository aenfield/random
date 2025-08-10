# Complete SQL to Pandas Operations Guide

This comprehensive reference provides every essential technique for performing SQL operations in pandas with Python, including detailed examples, performance optimizations, and best practices for data professionals transitioning between these technologies.

## Data selection and filtering

### Basic column selection

**SQL approach:**
```sql
SELECT column1, column2, column3 FROM table_name;
SELECT * FROM table_name;
```

**Pandas equivalents:**
```python
# Multiple column selection
df[['column1', 'column2', 'column3']]

# All columns
df  # or df.loc[:, :]

# Single column as DataFrame
df[['column1']]  # Returns DataFrame
df['column1']   # Returns Series
```

### WHERE clause filtering

**SQL filtering:**
```sql
SELECT * FROM tips WHERE total_bill > 10;
SELECT * FROM tips WHERE time = 'Dinner' AND tip > 5.00;
```

**Pandas equivalents:**
```python
# Boolean indexing (fastest for simple conditions)
df[df['total_bill'] > 10]

# Multiple conditions require parentheses and & operator
df[(df['time'] == 'Dinner') & (df['tip'] > 5.00)]

# Query method (SQL-like syntax, better for complex expressions)
df.query('total_bill > 10')
df.query('time == "Dinner" and tip > 5.00')

# External variables in query
min_tip = 5.0
df.query('tip > @min_tip')
```

### Date and time filtering

**Handling datetime operations:**
```python
# Ensure datetime conversion first
df['date_column'] = pd.to_datetime(df['date_column'])

# Date range filtering
df[(df['date_column'] >= '2020-01-01') & (df['date_column'] < '2021-01-01')]

# Extract date components
df[df['date_column'].dt.month == 6]
df[df['date_column'].dt.year == 2020]
df[df['date_column'].dt.dayofweek < 5]  # Weekdays only

# Time-based filtering with datetime accessor
df[df['date_column'].dt.strftime('%Y-%m') == '2021-06']
```

### String operations and pattern matching

**SQL LIKE equivalents:**
```sql
SELECT * FROM table WHERE column LIKE 'prefix%';
SELECT * FROM table WHERE column LIKE '%substring%';
```

**Pandas string methods:**
```python
# Pattern matching
df[df['column'].str.startswith('prefix')]
df[df['column'].str.endswith('suffix')]
df[df['column'].str.contains('substring')]

# Case-insensitive matching
df[df['column'].str.contains('pattern', case=False)]

# NOT LIKE equivalent
df[~df['column'].str.contains('pattern')]

# Regular expressions
df[df['column'].str.contains(r'^[A-Z]\w+', regex=True)]
df[df['column'].str.contains('pattern1|pattern2')]
```

### Numeric and NULL handling

**Range and membership testing:**
```python
# BETWEEN equivalent
df[df['price'].between(100.0, 200.0)]  # Inclusive by default

# IN equivalent
df[df['quantity'].isin([1, 5, 10, 25])]

# NOT IN equivalent
df[~df['quantity'].isin([1, 5, 10, 25])]

# NULL handling
df[df['column'].isna()]   # IS NULL
df[df['column'].notna()]  # IS NOT NULL

# Floating point precision handling
df[np.isclose(df['value'], 10.0, atol=1e-8)]
```

### DISTINCT and sorting operations

**Unique values and ordering:**
```python
# DISTINCT equivalents
df['column1'].unique()  # Returns numpy array
df[['column1', 'column2']].drop_duplicates()

# ORDER BY equivalents
df.sort_values('column1')  # Ascending by default
df.sort_values('column1', ascending=False)
df.sort_values(['column1', 'column2'], ascending=[False, True])

# LIMIT equivalents
df.head(10)  # First 10 rows
df.nlargest(10, 'column')  # Top 10 by value (faster than sort + head)
df.nsmallest(10, 'column')  # Bottom 10 by value
```

## Join operations

### Inner joins

**Standard inner join patterns:**
```python
# Basic inner join
result = pd.merge(df1, df2, on='key', how='inner')

# Multiple keys
result = pd.merge(df1, df2, on=['key1', 'key2'], how='inner')

# Different column names
result = pd.merge(df1, df2, left_on='left_key', right_on='right_key', how='inner')
```

### Left, right, and outer joins

**Complete join type coverage:**
```python
# LEFT JOIN (most commonly used)
result = pd.merge(df1, df2, on='key', how='left')

# RIGHT JOIN
result = pd.merge(df1, df2, on='key', how='right')

# FULL OUTER JOIN
result = pd.merge(df1, df2, on='key', how='outer')

# With indicator column for debugging
result = pd.merge(df1, df2, on='key', how='outer', indicator=True)
```

### Advanced join scenarios

**Complex merge operations:**
```python
# Self-joins (employee hierarchy example)
hierarchy = pd.merge(employees, employees[['emp_id', 'name']], 
                    left_on='manager_id', right_on='emp_id', 
                    how='left', suffixes=('', '_manager'))

# Multiple condition joins using temporary keys
df1['merge_key'] = df1['date'].dt.date.astype(str) + '_' + df1['category']
df2['merge_key'] = df2['date'].dt.date.astype(str) + '_' + df2['category']
result = pd.merge(df1, df2, on='merge_key', how='left').drop('merge_key', axis=1)

# Time series joins with merge_asof
result = pd.merge_asof(trades, quotes, on='timestamp', by='ticker', direction='backward')
```

### Join performance optimization

**Index-based joins for better performance:**
```python
# Set indices for repeated joins (much faster)
df1_indexed = df1.set_index('customer_id')
df2_indexed = df2.set_index('customer_id')

# This is faster for multiple operations
result = df1_indexed.join(df2_indexed, how='left')

# Validation to prevent unexpected results
result = pd.merge(df1, df2, on='key', how='left', validate='one_to_many')
```

## Common Table Expressions and subqueries

### CTE equivalents using variables

**Multi-step query patterns:**
```python
# SQL CTE pattern translation
# WITH regional_sales AS (SELECT region, SUM(sales) FROM sales_data GROUP BY region)

# Step 1: Create intermediate DataFrame
regional_sales = (
    sales_data.groupby('region')['sales']
    .sum()
    .reset_index()
    .rename(columns={'sales': 'total_sales'})
)

# Step 2: Use intermediate results
top_regions = regional_sales[regional_sales['total_sales'] > 1000000]
result = sales_data.merge(top_regions[['region']], on='region')
```

### Method chaining as CTE alternative

**Pandas fluent interface:**
```python
result = (
    sales_data
    .groupby('region')['sales'].sum()
    .reset_index()
    .rename(columns={'sales': 'total_sales'})
    .query('total_sales > 1000000')
    .merge(sales_data, on='region')
)
```

### Subquery patterns

**Correlated and scalar subqueries:**
```python
# Correlated subquery using transform
orders['avg_customer_amount'] = (
    orders.groupby('customer_id')['amount'].transform('mean')
)

# EXISTS equivalent using isin()
customers_with_orders = customers[
    customers['customer_id'].isin(orders['customer_id'])
]

# NOT EXISTS equivalent
customers_without_orders = customers[
    ~customers['customer_id'].isin(orders['customer_id'])
]
```

## Aggregation functions

### Basic GROUP BY operations

**Core aggregation patterns:**
```python
# Single aggregation
df.groupby('customer_id').agg({'amount': 'sum'})

# Multiple aggregations
result = df.groupby('customer_id').agg({
    'order_id': 'count',
    'amount': ['sum', 'mean', 'min', 'max']
}).round(2)

# Named aggregations for cleaner output
result = df.groupby('customer_id').agg(
    total_orders=('order_id', 'count'),
    total_amount=('amount', 'sum'),
    avg_amount=('amount', 'mean')
)
```

### HAVING clause equivalents

**Post-aggregation filtering:**
```python
# SQL: HAVING SUM(amount) > 1000
grouped = df.groupby('customer_id').agg({'amount': 'sum'})
result = grouped[grouped['amount'] > 1000]

# Alternative using query
result = df.groupby('customer_id').agg({'amount': 'sum'}).query('amount > 1000')
```

### Advanced aggregation functions

**LEAD, LAG, and ranking functions:**
```python
# LAG/LEAD equivalents using shift()
df['previous_value'] = df.groupby('group_id')['value'].shift(1)
df['next_value'] = df.groupby('group_id')['value'].shift(-1)

# Ranking functions
df['row_number'] = df.groupby('group_id')['value'].rank(method='first', ascending=False)
df['rank'] = df.groupby('group_id')['value'].rank(method='min', ascending=False)
df['dense_rank'] = df.groupby('group_id')['value'].rank(method='dense', ascending=False)

# Percentiles and quantiles
df.groupby('category')['score'].quantile(0.9)
df.groupby('category')['score'].quantile([0.25, 0.75]).unstack()
```

### Conditional aggregations

**CASE-style aggregations:**
```python
# SQL: SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END)
df.groupby('customer_id').apply(
    lambda x: pd.Series({
        'total_completed': x[x['status'] == 'completed']['amount'].sum(),
        'total_pending': x[x['status'] == 'pending']['amount'].sum(),
        'completion_rate': (x['status'] == 'completed').mean()
    })
)

# Using numpy.where for conditional sums
df['completed_amount'] = np.where(df['status'] == 'completed', df['amount'], 0)
result = df.groupby('customer_id')['completed_amount'].sum()
```

## Window functions

### Rolling window operations

**Time-based and fixed windows:**
```python
# Fixed window rolling
df['rolling_mean_3'] = df['value'].rolling(window=3).mean()

# Time-based rolling window
df.set_index('date', inplace=True)
df['rolling_mean_30d'] = df['value'].rolling('30D').mean()

# Group-wise rolling operations
df['rolling_mean'] = df.groupby('category')['value'].transform(lambda x: x.rolling(3).mean())

# Multiple rolling statistics
rolling_stats = df.groupby('category')['value'].rolling(window=5).agg(['mean', 'std', 'min', 'max'])
```

### Expanding windows and cumulative functions

**Running totals and expanding calculations:**
```python
# Expanding mean (cumulative average)
df['expanding_mean'] = df['value'].expanding().mean()

# Cumulative operations within groups
df['running_total'] = df.groupby('category')['amount'].cumsum()
df['running_count'] = df.groupby('category').cumcount() + 1
df['running_max'] = df.groupby('category')['value'].cummax()
```

### Custom window functions

**Advanced window operations:**
```python
def range_function(x):
    return x.max() - x.min()

def coefficient_of_variation(x):
    return x.std() / x.mean() if x.mean() != 0 else np.nan

# Apply custom functions
df['rolling_range'] = df['value'].rolling(window=5).apply(range_function)
df['rolling_cv'] = df['value'].rolling(window=5).apply(coefficient_of_variation)
```

## Advanced SQL operations

### CASE/WHEN statement equivalents

**Conditional logic patterns:**
```python
# Simple conditions using np.where
df['age_category'] = np.where(
    df['age'] < 25, 'Young',
    np.where(df['age'] <= 65, 'Adult', 'Senior')
)

# Multiple conditions using np.select
conditions = [df['age'] < 25, df['age'].between(25, 65), df['age'] > 65]
choices = ['Young', 'Adult', 'Senior']
df['age_category'] = np.select(conditions, choices, default='Unknown')

# Range-based categorization using pd.cut
df['age_category'] = pd.cut(df['age'], bins=[0, 25, 65, 100], 
                           labels=['Young', 'Adult', 'Senior'])

# New case_when method (pandas 2.2.0+)
df['age_category'] = df['age'].case_when([
    (df['age'] < 25, 'Young'),
    (df['age'].between(25, 65), 'Adult'),
    (df['age'] > 65, 'Senior')
])
```

### PIVOT and UNPIVOT operations

**Data reshaping techniques:**
```python
# PIVOT using pivot_table
pivot_result = sales.pivot_table(
    index='customer_id',
    columns='product',
    values='amount',
    aggfunc='sum',
    fill_value=0
)

# UNPIVOT using melt
unpivot_result = sales_pivot.melt(
    id_vars=['customer_id'],
    value_vars=['product_A', 'product_B'],
    var_name='product',
    value_name='amount'
)

# Stack/unstack for multi-level operations
stacked = df.stack(level=[1, 2])
unstacked = stacked.unstack(fill_value=0)
```

### UNION and set operations

**Combining datasets:**
```python
# UNION ALL equivalent
union_all = pd.concat([df1, df2], ignore_index=True)

# UNION (remove duplicates)
union_result = pd.concat([df1, df2]).drop_duplicates()

# Set difference (anti-join)
difference = df1.merge(df2, how='left', indicator=True)
difference = difference[difference['_merge'] == 'left_only'].drop('_merge', axis=1)
```

## Performance considerations and best practices

### Memory optimization strategies

**Data type optimization for memory efficiency:**
```python
# Optimize data types to reduce memory by 50-80%
df['category'] = df['category'].astype('category')  # For repeated strings
df['int_column'] = pd.to_numeric(df['int_column'], downcast='integer')
df['float_column'] = pd.to_numeric(df['float_column'], downcast='float')

# Memory profiling
print(df.memory_usage(deep=True))
memory_mb = df.memory_usage(deep=True).sum() / 1024**2
print(f"Memory usage: {memory_mb:.2f} MB")

# Categorical optimization can reduce memory by 98% for high-cardinality strings
```

### Vectorization vs apply performance

**Operation selection guidelines:**
```python
# Fast: Vectorized operations (300x faster for numeric)
df['result'] = df['quantity'] * df['price']

# Slower: Apply with lambda functions
# df['result'] = df.apply(lambda x: x['quantity'] * x['price'], axis=1)

# Exception: String operations can be faster with apply
# For text processing, test both approaches and choose based on your data
```

### Chunking for large datasets

**Memory-efficient processing:**
```python
# Process large files in chunks
def process_chunk(chunk):
    return chunk.groupby('category').agg({'value': ['sum', 'mean']})

chunk_results = []
for chunk in pd.read_csv('large_file.csv', chunksize=100000):
    chunk_result = process_chunk(chunk)
    chunk_results.append(chunk_result)

final_result = pd.concat(chunk_results).groupby(level=0).sum()
```

### Common pitfalls to avoid

**Critical issues and solutions:**
```python
# Avoid SettingWithCopyWarning
# Problem: df[df['col'] > 5]['new_col'] = value
# Solution: df.loc[df['col'] > 5, 'new_col'] = value

# Prevent memory leaks from DataFrame copies
# Use inplace operations when original DataFrame not needed
df.drop(columns=['unnecessary'], inplace=True)
df.fillna(0, inplace=True)

# Handle missing values appropriately
df.groupby('category', dropna=False)['value'].sum()  # Include NaN groups
```

### Index optimization

**Performance improvements through indexing:**
```python
# Set index for repeated operations
df_indexed = df.set_index('customer_id')

# Index-based operations are significantly faster
# This is much faster for repeated joins
for dataset in datasets:
    result = df_indexed.join(dataset.set_index('customer_id'))
```

## Data type handling best practices

### Categorical data optimization

**Memory and performance benefits:**
```python
# Convert high-cardinality strings to categorical
df['status'] = df['status'].astype('category')

# Ordered categorical for meaningful comparisons
df['size'] = pd.Categorical(df['size'], 
    categories=['Small', 'Medium', 'Large'], ordered=True)
df[df['size'] >= 'Medium']  # Works with ordered categoricals
```

### Datetime optimization

**Efficient date/time handling:**
```python
# Always use pd.to_datetime for proper datetime handling
df['date_column'] = pd.to_datetime(df['date_column'])

# Consider timezone handling
df['utc_time'] = pd.to_datetime(df['timestamp'], utc=True)

# Extract date components efficiently
df['year'] = df['date_column'].dt.year
df['month_name'] = df['date_column'].dt.month_name()
df['is_weekend'] = df['date_column'].dt.weekday >= 5
```

## Edge cases and troubleshooting

### Handling missing values

**Comprehensive NaN management:**
```python
# Missing values in aggregations
df.groupby('category')['value'].sum()    # Excludes NaN
df.groupby('category').size()            # Includes NaN
df.groupby('category', dropna=False)['value'].sum()  # Include NaN groups

# String operations with NaN
df[df['column'].str.contains('pattern', na=False)]

# Custom NaN handling in functions
def safe_division(x, y):
    return np.where(y == 0, np.nan, x / y)
```

### Performance profiling and debugging

**Tools and techniques:**
```python
# Profile execution time
%timeit operation()

# Memory profiling
from memory_profiler import profile

@profile
def memory_intensive_function():
    # Your code here
    pass

# Debug merge issues
result = pd.merge(df1, df2, on='key', how='outer', indicator=True)
print(result['_merge'].value_counts())
```

## Real-world examples

### Customer analytics pipeline

**Complete analysis workflow:**
```python
def customer_analysis_pipeline(transactions_df):
    # Calculate customer metrics using SQL-equivalent operations
    customer_metrics = (
        transactions_df
        .groupby('customer_id')
        .agg({
            'amount': ['sum', 'count', 'mean'],
            'transaction_date': ['min', 'max']
        })
    )
    
    # Flatten column names
    customer_metrics.columns = ['total_spent', 'transaction_count', 
                              'avg_transaction', 'first_purchase', 'last_purchase']
    
    # Create RFM segments
    today = pd.Timestamp.now()
    customer_metrics['recency'] = (today - customer_metrics['last_purchase']).dt.days
    customer_metrics['frequency'] = customer_metrics['transaction_count']
    customer_metrics['monetary'] = customer_metrics['total_spent']
    
    return customer_metrics
```

### Time series analysis

**Financial data processing:**
```python
def time_series_analysis(stock_data):
    stock_data = stock_data.sort_values('date')
    
    # Moving averages (SQL window function equivalent)
    stock_data['ma_7'] = stock_data['price'].rolling(window=7).mean()
    stock_data['ma_30'] = stock_data['price'].rolling(window=30).mean()
    
    # Lag values (SQL LAG function)
    stock_data['prev_price'] = stock_data['price'].shift(1)
    stock_data['daily_return'] = stock_data['price'].pct_change()
    
    # Cumulative operations
    stock_data['cumulative_return'] = (1 + stock_data['daily_return']).cumprod() - 1
    
    return stock_data
```

This comprehensive guide provides the complete toolkit for translating SQL operations to pandas while maintaining performance, handling edge cases, and following best practices. The key to successful SQL-to-pandas migration lies in understanding both the syntactic differences and the performance characteristics of each approach, combined with proper data type optimization and memory management techniques.