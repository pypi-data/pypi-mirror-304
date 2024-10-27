def mutate(df, col1, col2, new_column, operation):
    """
    A simple mutate function that creates a new column by applying an operation 
    on two existing columns and prints a message when called.
    
    Args:
        df: A pandas DataFrame
        col1: The first column to use in the operation
        col2: The second column to use in the operation
        new_column: The name of the new column to create
        operation: A string representing the operation ('+', '-', '*', '/')
    
    Returns:
        A pandas DataFrame with the new column added
    """
    operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y
    }
    
    if operation in operations:
        df[new_column] = operations[operation](df[col1], df[col2])
    else:
        raise ValueError(f"Unsupported operation '{operation}'. Supported operations are: {list(operations.keys())}")


if __name__ == "__main__":
    mutate()
