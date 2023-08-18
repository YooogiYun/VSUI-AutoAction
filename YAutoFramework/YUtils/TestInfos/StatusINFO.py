from enum import IntFlag

import pytest

from YAutoFramework.YUtils.Logger.Ylogger import GlobalLogger


class ScriptStatus(IntFlag) :
	"""
	该 Enum 用于表示脚本编写和管理状态：使用十六进制 实现按位运算，,实现 Flags 的效果
	与脚本运行结果无关
	"""
	Obsolete = -1
	Archive = 0
	Coding = 2
	Fixing = Coding
	InReview = 4
	Reviewed = 8
	Accepted = 16

	@classmethod
	def get_binary_sets(cls) :
		result = []
		for idx1, s1 in enumerate(cls) :
			for idx2, s2 in enumerate(cls) :
				if idx1 < idx2 :
					result.append((s1, 'and', s2, s1 and s2))
					result.append((s1, 'or', s2, s1 or s2))
		return result

	def __or__(self, other: IntFlag) :
		return ScriptStatus(self.value | other.value)

	def __and__(self, other: IntFlag) :
		return ScriptStatus(self.value & other.value)


@GlobalLogger.global_log(message="Test the script status")
@pytest.mark.parametrize('value', ScriptStatus.get_binary_sets())
def test_ScriptStatus(value) :
	s1, operator_type, s2, v = value
	assert operator_type == 'and' or operator_type == 'or'
	assert v == max(s1.value, s2.value) if operator_type == 'and' else min(s1.value, s2.value)
