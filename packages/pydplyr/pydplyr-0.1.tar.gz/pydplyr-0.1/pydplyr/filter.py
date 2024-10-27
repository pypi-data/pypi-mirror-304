def filter(df, condition):
    """A simple filter function that filters datasets when given a condition.

    Args: 
        df: A pandas DataFrame
        condition: A string that represents the condition to filter the DataFrame

    Returns:
        A pandas DataFrame that has been filtered based on the condition

    Example:
        >>> from pydplyr.filter import filter
        >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        >>> filter(df, 'A > 1')
           A  B
        1  2  5
    """
    return df.query(condition)



if __name__ == "__main__":
    filter()