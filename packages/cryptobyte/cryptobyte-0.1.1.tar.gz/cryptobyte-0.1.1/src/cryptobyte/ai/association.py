from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

dataset = [
    ['milk', 'bread', 'nuts'],
    ['milk', 'bread'],
    ['milk', 'eggs', 'nuts'],
    ['milk', 'bread', 'eggs'],
    ['bread', 'nuts'],
]

df = pd.DataFrame(dataset)
df_encoded = pd.get_dummies(df, prefix='', prefix_sep='')

frequent = apriori(df_encoded, min_support=0.5, use_colnames=True)
print(frequent)

rules = association_rules(frequent, metric="lift", min_threshold=1.0)
print(rules)
