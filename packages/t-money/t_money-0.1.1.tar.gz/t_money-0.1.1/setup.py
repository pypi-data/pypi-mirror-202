# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['t_money']
setup_kwargs = {
    'name': 't-money',
    'version': '0.1.1',
    'description': 'Advanced Python 3.10 Dataclass for handling monetary values, keeping amount and currency together',
    'long_description': '# Money dataclass\nAdvanced Python 3.10 Dataclass for handling monetary values, keeping amount and currency together\n\nThis `Money` class provides a simple and efficient way to manage amounts of money and perform arithmetic operations and comparisons on them. It supports different currencies and ensures that the operations are only performed on matching currencies to avoid inconsistencies.\n\n## Features\n\n- Initialize a `Money` object with a specific amount and currency.\n- Perform arithmetic operations between `Money` objects with the same currency.\n- Compare and sort `Money` objects.\n- Convert a `Money` object to another currency.\n- Round a `Money` object to a specified number of decimal places.\n- Serialize and deserialize `Money` objects to/from JSON.\n\n## Usage\n\n    from t_money import Money\n\n### Creating a Money object\n\n```python\nusd = Money(Decimal("10.50"), "USD")\n```\n\n### Create a Money object from string\n\n```python\nusd_from_str = Money.from_str("USD 5.25")\n```\n\n### Arithmetic operations\n\n```python\nusd1 = Money(Decimal("10.50"), "USD")\nusd2 = Money(Decimal("5.50"), "USD")\n\nusd_sum = usd1 + usd2\nusd_difference = usd1 - usd2\nusd_product = usd1 * Decimal("2")\n```\n\n### Comparisons\n\n```python\nprint(usd1 == usd2)\nprint(usd1 < usd2)\n```\n\n### Rounding\n\n```python\nrounded_usd = usd1.round_to(1)\n```\n\n### Currency conversion\n\n```python\neur = usd.convert("EUR", Decimal("0.85"))\n```\n\n### Money is hashable\n\n```python\nmoney_set = {usd1, usd2}\n```\n\n### Serialization and deserialization\n\n```python\nimport json\n\n# Serialize data containing Money object\ndata = {\'money\': usd}\njson_str = json.dumps(data, default=money_serializer)\n\n# Deserialize JSON data to Money object\nloaded_data = json.loads(json_str, object_hook=money_deserializer)\n```\n\n## Error Handling\n\nWhen performing operations on `Money` objects with different currencies, a `DifferentCurrencyError` will be raised. Make sure to handle this error if necessary when dealing with multiple currencies.\n\n\n',
    'author': 'Jordan Dimov',
    'author_email': 'jdimov@a115.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jordan-dimov/t_money',
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
