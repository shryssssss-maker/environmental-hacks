import unittest
from scanner.adapters.owner_b import OwnerB
from scanner.core import ScanContext


class NetworkRepositoryScanTest(unittest.TestCase):
    def test_registered_network_checks_are_visible_but_source_only_scan_cannot_confirm_them(self):
        context = ScanContext('fixture:repo', 'b' * 40, 'source-only',
                              [('app.js', 'const payload = JSON.stringify({a: 1});')], {})
        runs = OwnerB().run(context)
        network = [run for run in runs if run.check_id.startswith('NET-')]
        self.assertEqual({run.check_id for run in network}, {f'NET-{i:02}' for i in range(1, 13)})
        self.assertTrue(all(run.unavailable and not run.result and not run.error for run in network))
        self.assertTrue(all('no runtime network waste is confirmed' in run.unavailable for run in network))


if __name__ == '__main__':
    unittest.main()
