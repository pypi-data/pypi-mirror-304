"""
Ensure the library can handle large data.
"""
import numpy as np
import pandas as pd

import cshelve

from helpers import unique_key


def test_large():
    """
    Update a relative large DataFrame in the DB to verify it is possible.
    """
    db = cshelve.open("tests/configurations/azure-integration/standard.ini")

    key_pattern = unique_key + "test_large"

    # 167.46 MiB
    df = pd.DataFrame(
        np.random.randint(0, 100, size=(844221, 26)),
        columns=list("ABCDEFGHIGKLMNOPQRSTUVWXYZ"),
    )

    db[key_pattern] = df
    new_df = db[key_pattern]

    assert id(new_df) != id(df)
    assert new_df.equals(df)
