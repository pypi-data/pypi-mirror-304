# Adaptyper

Очень старается адаптировать один тип данных в другой

```py
from adaptyper import convert

# float
convert.to_float(None)  # 0.0
convert.to_float('')  # 0.0
convert.to_float('123,456')  # 123.456
convert.to_float(' 123\xa0456\xa0')  # 123456.0
convert.to_float('tRuE')  # 1.0
convert.to_float(True)  # 1.0
convert.to_float(1)  # 1.0
convert.to_float('.3')  # 0.3

# int
# тоже что и float,
# только формат int + банковское округление (по-умолчанию True)
convert.to_int('.6',True)  # 1
convert.to_int('.6',False)  # 0
convert.to_int('1.5',True)  # 2
convert.to_int('1.5',False)  # 1
```