import pandas as pd
import decimal

def count_decimals(value):
    # Convert the value to a decimal and count the number of decimal places
    return decimal.Decimal(str(value)).as_tuple().exponent * -1

column_name = 'VALOR TOTAL'  # Replace with the actual name of the column

# Apply the count_decimals() function to each value in the column
decimals_count = df_ventas[column_name].apply(count_decimals)

# Find the value with the most significant number of decimals
value_with_most_decimals = df_ventas[column_name][decimals_count.idxmax()]
