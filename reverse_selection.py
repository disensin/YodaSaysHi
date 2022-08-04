from pymel import all as pm
"""
Reverse the Maya selection! That's it! Super useful when
parenting, Constraining, etc.
Great stuff!
"""
pm.select(pm.selected()[::-1])
