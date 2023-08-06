# `bimmm`

The `bimmm` is a package to analyse MMM models and visualize them

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install bimmm.

```bash
pip install bimmm
```

## 1. Usage Decomposition for logistic regressions over time

```python

# import modules
import pandas as pd
import numpy as np
from bimmm.analyse_mmm_models import mmm, s_curve, decay
import ssl
import statsmodels.formula.api as smf
import plotly.io as pio
pio.renderers.default = "browser"
import warnings
warnings.filterwarnings("ignore")


# Get some example data (you might need to run ssl._create_default_https_context = ssl._create_unverified_context:
ssl._create_default_https_context = ssl._create_unverified_context
url = 'https://raw.githubusercontent.com/SimonTeg/nlodatascience/master/sales_vs_media.csv'
df_example = pd.read_csv(url)
# make a dataset for the historical data with the sales, and one to forecast the sales
df_train = df_example.iloc[:26]
df_forecast = df_example.iloc[26:]

# Make your model
formule = 'sales ~ s_curve(decay(tv, 0.3), 3) + s_curve(decay(radio, 0.2), 7) + jackpot + jan + apr + dec + ' \
          'sunday_near_drawing + event + competitor + consumer_trust'
model = smf.ols(formula=formule, data=df_train)

# mmm object maken
analyse_model = mmm(model=model, var_date=df_train.maand_jaar, df=df_train)

# Actual vs fit
analyse_model.actual_vs_fit_graph().show()

# Decompositie
analyse_model.decomposition_graph().show()
analyse_model.decompositie_sum()

# Kosten van de kanalen waarvan je de ROI wilt weten
media_dict = {'tv': 10, 'radio': 5}
analyse_model.roi(media_dict, 'sales')

# Model results
analyse_model.model_characteristics()
analyse_model.VIF()

# Analyse for adding variables
analyse_model.select_n_largest_outliers(5)
analyse_model.check_variables_to_add()
``` 

## License

Copyright (c) 2023 Rumiko
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
