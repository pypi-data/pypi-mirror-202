#!/usr/bin/env python
"""Tests for `legacyplatequery` package."""
import legacyplatequery as lpdata

lpdata.auth('wangweihua', 'xxx')

lpdata.get_total_of_plates()


lpdata.get_total_of_star_catalog()

ra = 12.0
dec = 12.0
radius = 12
# 搜寻底片
plates = lpdata.get_plates_by_radial_query(ra, dec, radius)
print(plates)


# 搜寻星表
stars = lpdata.get_star_catalog_by_radial_query(ra, dec)
print(stars)
