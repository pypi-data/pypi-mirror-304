def analyze_sales(sales_data):
    grouped_sales = sales_data.groupby('category').agg(
        sales=('sales', 'sum'),
        quantity=('quantity', 'sum')
    )

    grouped_sales = grouped_sales.reset_index()

    return grouped_sales