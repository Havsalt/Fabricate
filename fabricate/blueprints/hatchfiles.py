r"""
[tool.hatch.build.targets.wheel]
include = ["$inject[name]/**", "$inject[script].bat"]
exclude = ["$inject[name]/**/__pycache__"]
"""
