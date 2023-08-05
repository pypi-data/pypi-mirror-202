# MIT License

# Copyright (c) 2023 kaalam.ai The Authors of Jazz

# Hosted at https://github.com/kaalam/snakeit.git

import re


class SnakeIt():

	@staticmethod
	def help():
		usage = """
Usage:
------

  snakeit --help  Shows this help.
"""
		print(usage)
		return 1
