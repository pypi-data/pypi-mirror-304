from split import *
import pandas as pd
df = pd.DataFrame({'source': ['a', 'a', 'a', 'd', 'e', 'f','g','h','i','j'],
                   'target': ['b', 'j', 'k', 'c', 'd', 'e','d','e','d','e'],
                   'edge_type': [2, 3, 1, 1, 1, 2, 3, 3, 2, 1]
                   })

# sampled_df = df['ID'].sample(frac=0.2, random_state=42)
# print(sampled_df)

# random_state=42
# train_idx, test_idx = get_edge_type_split_train_test(df, test_frac=0.2, random_state=random_state)
# print('test: ', df.iloc[test_idx])
# print('train: ', df.iloc[train_idx])

di = get_random_n_split(df, 5)
print('done')

