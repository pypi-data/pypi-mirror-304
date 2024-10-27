import pandas as pd
import pytest
from pydplyr.arrange import arrange

def test_arrange_valid_column():
    # Arrange
    data = {'A': [3, 1, 2], 'B': [9, 8, 7]}
    df = pd.DataFrame(data)
    
    # Act
    arrange(df, 'A')
    
    # Assert
    assert df['A'].tolist() == [1, 2, 3], "Failed to sort by column 'A' in ascending order."

def test_arrange_non_existent_column():
    # Arrange
    data = {'A': [3, 1, 2], 'B': [9, 8, 7]}
    df = pd.DataFrame(data)
    
    # Act & Assert
    with pytest.raises(KeyError):
        arrange(df, 'C')  # Column 'C' does not exist

def test_arrange_with_nan_values():
    # Arrange
    data = {'A': [3, None, 2], 'B': [9, 8, None]}
    df = pd.DataFrame(data)
    
    # Act
    arrange(df, 'A')
    
    # Assert
    assert df['A'].isna().sum() == 1, "Failed to handle NaN values properly."
    assert df['A'].tolist() == [2, 3, None], "Failed to sort with NaN values in column 'A'."

def test_arrange_empty_dataframe():
    # Arrange
    df = pd.DataFrame(columns=['A', 'B'])
    
    # Act
    arrange(df, 'A')
    
    # Assert
    assert df.empty, "Failed to handle an empty DataFrame."

def test_arrange_with_duplicates():
    # Arrange
    data = {'A': [2, 1, 2, 1], 'B': [9, 8, 7, 6]}
    df = pd.DataFrame(data)
    
    # Act
    arrange(df, 'A')
    
    # Assert
    assert df['A'].tolist() == [1, 1, 2, 2], "Failed to sort correctly with duplicate values."

def test_arrange_single_row_dataframe():
    # Arrange
    data = {'A': [1], 'B': [9]}
    df = pd.DataFrame(data)
    
    # Act
    arrange(df, 'A')
    
    # Assert
    assert df['A'].tolist() == [1], "Failed to handle a single-row DataFrame."

if __name__ == "__main__":
    pytest.main()
