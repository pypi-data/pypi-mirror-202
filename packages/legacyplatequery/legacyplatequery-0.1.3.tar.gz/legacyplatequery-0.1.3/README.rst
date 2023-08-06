=================
legacyplate query
=================

Description
-----------
legacyplatequery is a legacyplate query tool developed by Shanghai Astronomical Observatory. 
It provide a python package like Astroquery.


Installation
------------

You can use pip command to install it:
```shell
pip install legacyplatequery
```

Usage
-----

1. import the package.

```python
import  legacyplatequery as lpdata
```

2. Login

```python
user = 'wangweihua'
password = 'xxx'
lpdata.auth(user, password)
```

3. Get the total number of legacy plate

```python
lpdata.get_total_of_plates()
```

4. Get the total number of the stars in the star catalog

```python
lpdata.get_total_of_star_catalog()
```

5. Search the legacy plates with `q3c_radial_query`

```python
ra = 12.0
dec = 12.0
radius = 12
plates = lpdata.get_plates_by_radial_query(ra, dec, radius)
print(plates)
```

6. Search the stars with `q3c_radial_query`

```python
stars = lpdata.get_star_catalog_by_radial_query(ra, dec)
print(stars)
```



