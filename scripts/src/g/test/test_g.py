from ..g import hardReset
from mock import patch

empty_remainder = []
remainder_with_commits = [1]
remainder_with_commits_string = ['1']
normal_reset_parameters = ['reset --hard HEAD']
commit_removal_reset_parameters = ['reset --hard HEAD~1']

@patch('scripts.src.g.g.git')
class TestHardReset:
  def test_subject_calls_normal_hard_reset_if_no_remainder(self, mock_git):
    hardReset(empty_remainder)
    mock_git.assert_called_with(normal_reset_parameters)

  def test_subject_calls_commit_reset_if_commit_number_passed_in(self, mock_git):
    hardReset(remainder_with_commits)
    mock_git.assert_called_with(commit_removal_reset_parameters)

  def test_subject_calls_commit_reset_if_commit_string_passed_in(self, mock_git):
    hardReset(remainder_with_commits_string)
    mock_git.assert_called_with(commit_removal_reset_parameters)