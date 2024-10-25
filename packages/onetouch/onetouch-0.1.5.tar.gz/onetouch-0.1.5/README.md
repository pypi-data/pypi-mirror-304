# ONETOUCH
一款集成了数据清洗,模型训练,模型评估的简单python软件包
# ONETOUCH Package
onetouch is a Python package designed to streamline data processing, model training, and evaluation with minimal code.
## Installation
To install the onetouch package, run the following command in your terminal or command prompt:
```bash
pip install onetouch
```
## Usage
### Importing the onetouch Package
To use the onetouch package, import it into your Python script as follows:

```python
import onetouch as ot
```
### One2Three Class
The `One2Three` class is a convenient tool for data preprocessing, model training, and evaluation, also known as "one-click triple action".
#### Basic Usage
filepath format-supported: '*.csv', '*.xlsx'
##### Method 1: Direct File Access
The first method involves directly accessing a file:
- `df`: Data (pd.DataFrame) - Not required, use `None` if not provided.
- `label`: Target label (str) - Optional, defaults to the last column if not specified.
- `filepath`: File path (str) - Required.
Example:

```python
import onetouch as ot

data = ot.One2Three(None, 'label', 'FilePath')
```
##### Method 2: Importing Data
The second method involves importing data:
- `df`: Data (pd.DataFrame) - Required.
- `label`: Target label (str) - Optional, defaults to the last column if not specified.
- `filepath`: File path (str) - Not required, use `None` if not provided.
Example:

```python
import onetouch as ot
import pandas as pd

df = pd.read_csv('FilePath')
# You can also use the following syntax:
# data = sa.One2Three(df, None, None)
data = ot.One2Three(df, 'label', None)
```
For more detailed usage instructions and examples, please refer to the package documentation or reach out to the onetouch community.