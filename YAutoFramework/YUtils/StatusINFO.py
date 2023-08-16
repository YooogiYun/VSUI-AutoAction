import string
from enum import IntFlag

import pytest


class ScriptStatus(IntFlag) :
	'''
	该 Enum 用于表示脚本编写和管理状态: 使用十六进制 实现按位运算,,实现 Flags 的效果
	与脚本运行结果无关
	'''
	Obsolete = 2,
	Archive = 4,
	Coding = 8,
	Fixing = 16
	InReview = 32,
	Reviewed = 64,
	Accepted = 128,

	@classmethod
	def get_binary_sets(cls) :
		res = { }
		for idx1, s1 in enumerate(cls) :
			for idx2, s2 in enumerate(cls) :
				if idx1 < idx2 :
					res[f'{s1.name} and {s2.name}'] = s1 and s2
					res[f'{s1.name} or {s2.name}'] = s1 or s2
		return res

	def __or__(self, other: IntFlag) :
		return ScriptStatus(self.value | other.value)

	def __and__(self, other: IntFlag) :
		return ScriptStatus(self.value & other.value)


@pytest.mark.parametrize('operator_set', ScriptStatus.get_binary_sets())
def test_ScriptStatus(operator_set) :
	for k, v in operator_set :
		s1, operator_type, s2 = k.split(string.whitespace)
		print(str.join('-', k.split(string.whitespace)))
