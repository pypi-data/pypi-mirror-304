import unittest
from unittest.mock import patch

from src.versionhawk.versionhawk import get_package_versions, get_github_releases, parse_input


class TestVersionHawk(unittest.TestCase):

    @patch('requests.get')
    def test_get_package_versions(self, mock_get):
        # Mocking PyPI response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'releases': {
                '1.0.0': [],
                '1.1.0': [],
                '2.0.0': [],
            }
        }

        versions = get_package_versions('requests')
        self.assertEqual(versions, ['1.0.0', '1.1.0', '2.0.0'])

    @patch('requests.get')
    def test_get_github_releases(self, mock_get):
        # Mocking GitHub response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {'tag_name': 'v1.0.0'},
            {'tag_name': 'v1.1.0'},
            {'tag_name': 'v2.0.0'},
        ]

        versions = get_github_releases('psf', 'requests')
        self.assertEqual(versions, ['v1.0.0', 'v1.1.0', 'v2.0.0'])

    def test_parse_input_valid_github_url(self):
        input_str = "https://github.com/psf/requests"
        result = parse_input(input_str)
        self.assertEqual(result, ('github', 'psf', 'requests'))

    def test_parse_input_valid_pypi_url(self):
        input_str = "https://pypi.org/project/requests/"
        result = parse_input(input_str)
        self.assertEqual(result, ('pypi', 'requests'))

    def test_parse_input_owner_repo_format(self):
        input_str = "psf/requests"
        result = parse_input(input_str)
        self.assertEqual(result, ('github', 'psf', 'requests'))

    def test_parse_input_only_package_name(self):
        input_str = "requests"
        result = parse_input(input_str)
        self.assertEqual(result, ('pypi', 'requests'))

    def test_parse_input_invalid_owner_repo_format(self):
        input_str = "invalid_owner/invalid_repo"
        result = parse_input(input_str)
        self.assertEqual(result, ('github', 'invalid_owner', 'invalid_repo'))

    def test_parse_input_github_with_branch(self):
        input_str = "https://github.com/psf/requests/tree/main"
        result = parse_input(input_str)
        self.assertEqual(result, ('github', 'psf', 'requests'))


if __name__ == '__main__':
    unittest.main()