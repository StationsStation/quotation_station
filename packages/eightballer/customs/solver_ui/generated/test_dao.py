import sys
import json
import random
import unittest
from copy import deepcopy
from pathlib import Path
from contextlib import contextmanager


sys.path.append(str(Path(__file__).parent / "dao"))

from request_for_quote_dao import RequestforquoteDAO
from create_r_f_q_dao import CreaterfqDAO
from quote_dao import QuoteDAO
from r_f_q_error_dao import RfqerrorDAO
from accept_dao import AcceptDAO


class TestDAOs(unittest.TestCase):
    """Test DAOs."""

    @classmethod
    def setUpClass(cls):
        """Setup class-level fixtures."""
        cls.data_file = Path(__file__).parent / "dao" / "aggregated_data.json"
        cls.backup_file = cls.data_file.with_suffix('.json.bak')

        # Create a backup of the original file
        cls.data_file.rename(cls.backup_file)

    @classmethod
    def tearDownClass(cls):
        """Tear down class-level fixtures."""
        # Restore the original file
        if cls.backup_file.exists():
            cls.backup_file.rename(cls.data_file)

    def setUp(self):
        """Setup DAOs and restore data file before each test."""
        self.requestforquotedao = RequestforquoteDAO()
        self.createrfqdao = CreaterfqDAO()
        self.quotedao = QuoteDAO()
        self.rfqerrordao = RfqerrorDAO()
        self.acceptdao = AcceptDAO()
        self._restore_data_file()

    def tearDown(self):
        """Restore data file after each test."""
        self._restore_data_file()

    def _restore_data_file(self):
        """Restore the data file from the backup."""
        if self.backup_file.exists():
            self.backup_file.replace(self.data_file)

    @contextmanager
    def _data_file_context(self):
        """Context manager for data file operations."""
        try:
            yield
        finally:
            self._restore_data_file()

    def test_requestforquotedao(self):
        """Test CRUD operations for RequestforquoteDAO."""
        with self._data_file_context():
            dummy_data = {"amount_in": 44, "ask_token_id": "dummy_7352", "bid_token_id": "dummy_1102", "buyer_wallet_address": "dummy_2108", "chain_id": "dummy_2844", "expiration_time": 40}

            # Test insert
            try:
                self.requestforquotedao.insert(dummy_data)
                all_data = self.requestforquotedao.get_all()
                self.assertEqual(len(all_data), 6)
                self.assertTrue(any(item == dummy_data for item in all_data))
                print("Insert operation successful for RequestforquoteDAO")
            except Exception as e:
                self.fail(f"Insert operation failed for RequestforquoteDAO: {e}")

            # Test get_all
            try:
                result = self.requestforquotedao.get_all()
                self.assertIsInstance(result, list)
                self.assertEqual(len(result), 6)
                self.assertTrue(any(all(item[k] == v for k, v in dummy_data.items()) for item in result))
                print("Get all operation successful for RequestforquoteDAO")
            except Exception as e:
                self.fail(f"Get all operation failed for RequestforquoteDAO: {e}")

            # Test get_by_id
            try:
                all_items = self.requestforquotedao.get_all()

                result = self.requestforquotedao.get_by_id("6")

                self.assertIsNotNone(result)
                self.assertEqual(result, dummy_data)
                print("Get by id operation successful for RequestforquoteDAO")
            except Exception as e:
                self.fail(f"Get by id operation failed for RequestforquoteDAO: {e}")

            # Test update
            try:
                all_items = self.requestforquotedao.get_all()
                update_data = deepcopy(dummy_data)
                random_item = random.choice(range(len(all_items)))
                hashmap_key = str(random_item + 1)

                result = self.requestforquotedao.update(hashmap_key, **update_data)
                all_items = self.requestforquotedao.get_all()
                self.assertIsNotNone(result)
                self.assertEqual(update_data, all_items[int(hashmap_key) - 1])
                updated_item = self.requestforquotedao.get_by_id(hashmap_key)
                self.assertEqual(updated_item, update_data)
                print("Update operation successful for RequestforquoteDAO")
            except Exception as e:
                self.fail(f"Update operation failed for RequestforquoteDAO: {e}")

            # Test delete
            try:
                all_items = self.requestforquotedao.get_all()
                random_index = random.choice(range(len(all_items)))
                hashmap_key = str(random_index + 1)

                item_to_delete = all_items[int(hashmap_key) - 1]

                result = self.requestforquotedao.delete(hashmap_key)
                self.assertTrue(result)
                all_data_after_delete = self.requestforquotedao.get_all()
                self.assertEqual(len(all_data_after_delete), len(all_items) - 1)
                deleted_item = self.requestforquotedao.get_by_id(hashmap_key)
                self.assertIsNone(deleted_item)
                print("Delete operation successful for RequestforquoteDAO")
            except Exception as e:
                self.fail(f"Delete operation failed for RequestforquoteDAO: {e}")

    def test_createrfqdao(self):
        """Test CRUD operations for CreaterfqDAO."""
        with self._data_file_context():
            dummy_data = {"rfq": "dummy_9300"}

            # Test insert
            try:
                self.createrfqdao.insert(dummy_data)
                all_data = self.createrfqdao.get_all()
                self.assertEqual(len(all_data), 6)
                self.assertTrue(any(item == dummy_data for item in all_data))
                print("Insert operation successful for CreaterfqDAO")
            except Exception as e:
                self.fail(f"Insert operation failed for CreaterfqDAO: {e}")

            # Test get_all
            try:
                result = self.createrfqdao.get_all()
                self.assertIsInstance(result, list)
                self.assertEqual(len(result), 6)
                self.assertTrue(any(all(item[k] == v for k, v in dummy_data.items()) for item in result))
                print("Get all operation successful for CreaterfqDAO")
            except Exception as e:
                self.fail(f"Get all operation failed for CreaterfqDAO: {e}")

            # Test get_by_id
            try:
                all_items = self.createrfqdao.get_all()

                result = self.createrfqdao.get_by_id("6")

                self.assertIsNotNone(result)
                self.assertEqual(result, dummy_data)
                print("Get by id operation successful for CreaterfqDAO")
            except Exception as e:
                self.fail(f"Get by id operation failed for CreaterfqDAO: {e}")

            # Test update
            try:
                all_items = self.createrfqdao.get_all()
                update_data = deepcopy(dummy_data)
                random_item = random.choice(range(len(all_items)))
                hashmap_key = str(random_item + 1)

                result = self.createrfqdao.update(hashmap_key, **update_data)
                all_items = self.createrfqdao.get_all()
                self.assertIsNotNone(result)
                self.assertEqual(update_data, all_items[int(hashmap_key) - 1])
                updated_item = self.createrfqdao.get_by_id(hashmap_key)
                self.assertEqual(updated_item, update_data)
                print("Update operation successful for CreaterfqDAO")
            except Exception as e:
                self.fail(f"Update operation failed for CreaterfqDAO: {e}")

            # Test delete
            try:
                all_items = self.createrfqdao.get_all()
                random_index = random.choice(range(len(all_items)))
                hashmap_key = str(random_index + 1)

                item_to_delete = all_items[int(hashmap_key) - 1]

                result = self.createrfqdao.delete(hashmap_key)
                self.assertTrue(result)
                all_data_after_delete = self.createrfqdao.get_all()
                self.assertEqual(len(all_data_after_delete), len(all_items) - 1)
                deleted_item = self.createrfqdao.get_by_id(hashmap_key)
                self.assertIsNone(deleted_item)
                print("Delete operation successful for CreaterfqDAO")
            except Exception as e:
                self.fail(f"Delete operation failed for CreaterfqDAO: {e}")

    def test_quotedao(self):
        """Test CRUD operations for QuoteDAO."""
        with self._data_file_context():
            dummy_data = {"amount_out": 64, "ask_token_id": "dummy_2583", "bid_token_id": "dummy_7361", "chain_id": "dummy_5247", "seller_wallet_address": "dummy_5471"}

            # Test insert
            try:
                self.quotedao.insert(dummy_data)
                all_data = self.quotedao.get_all()
                self.assertEqual(len(all_data), 6)
                self.assertTrue(any(item == dummy_data for item in all_data))
                print("Insert operation successful for QuoteDAO")
            except Exception as e:
                self.fail(f"Insert operation failed for QuoteDAO: {e}")

            # Test get_all
            try:
                result = self.quotedao.get_all()
                self.assertIsInstance(result, list)
                self.assertEqual(len(result), 6)
                self.assertTrue(any(all(item[k] == v for k, v in dummy_data.items()) for item in result))
                print("Get all operation successful for QuoteDAO")
            except Exception as e:
                self.fail(f"Get all operation failed for QuoteDAO: {e}")

            # Test get_by_id
            try:
                all_items = self.quotedao.get_all()

                result = self.quotedao.get_by_id("6")

                self.assertIsNotNone(result)
                self.assertEqual(result, dummy_data)
                print("Get by id operation successful for QuoteDAO")
            except Exception as e:
                self.fail(f"Get by id operation failed for QuoteDAO: {e}")

            # Test update
            try:
                all_items = self.quotedao.get_all()
                update_data = deepcopy(dummy_data)
                random_item = random.choice(range(len(all_items)))
                hashmap_key = str(random_item + 1)

                result = self.quotedao.update(hashmap_key, **update_data)
                all_items = self.quotedao.get_all()
                self.assertIsNotNone(result)
                self.assertEqual(update_data, all_items[int(hashmap_key) - 1])
                updated_item = self.quotedao.get_by_id(hashmap_key)
                self.assertEqual(updated_item, update_data)
                print("Update operation successful for QuoteDAO")
            except Exception as e:
                self.fail(f"Update operation failed for QuoteDAO: {e}")

            # Test delete
            try:
                all_items = self.quotedao.get_all()
                random_index = random.choice(range(len(all_items)))
                hashmap_key = str(random_index + 1)

                item_to_delete = all_items[int(hashmap_key) - 1]

                result = self.quotedao.delete(hashmap_key)
                self.assertTrue(result)
                all_data_after_delete = self.quotedao.get_all()
                self.assertEqual(len(all_data_after_delete), len(all_items) - 1)
                deleted_item = self.quotedao.get_by_id(hashmap_key)
                self.assertIsNone(deleted_item)
                print("Delete operation successful for QuoteDAO")
            except Exception as e:
                self.fail(f"Delete operation failed for QuoteDAO: {e}")

    def test_rfqerrordao(self):
        """Test CRUD operations for RfqerrorDAO."""
        with self._data_file_context():
            dummy_data = {"error_code": "dummy_8323"}

            # Test insert
            try:
                self.rfqerrordao.insert(dummy_data)
                all_data = self.rfqerrordao.get_all()
                self.assertEqual(len(all_data), 6)
                self.assertTrue(any(item == dummy_data for item in all_data))
                print("Insert operation successful for RfqerrorDAO")
            except Exception as e:
                self.fail(f"Insert operation failed for RfqerrorDAO: {e}")

            # Test get_all
            try:
                result = self.rfqerrordao.get_all()
                self.assertIsInstance(result, list)
                self.assertEqual(len(result), 6)
                self.assertTrue(any(all(item[k] == v for k, v in dummy_data.items()) for item in result))
                print("Get all operation successful for RfqerrorDAO")
            except Exception as e:
                self.fail(f"Get all operation failed for RfqerrorDAO: {e}")

            # Test get_by_id
            try:
                all_items = self.rfqerrordao.get_all()

                result = self.rfqerrordao.get_by_id("6")

                self.assertIsNotNone(result)
                self.assertEqual(result, dummy_data)
                print("Get by id operation successful for RfqerrorDAO")
            except Exception as e:
                self.fail(f"Get by id operation failed for RfqerrorDAO: {e}")

            # Test update
            try:
                all_items = self.rfqerrordao.get_all()
                update_data = deepcopy(dummy_data)
                random_item = random.choice(range(len(all_items)))
                hashmap_key = str(random_item + 1)

                result = self.rfqerrordao.update(hashmap_key, **update_data)
                all_items = self.rfqerrordao.get_all()
                self.assertIsNotNone(result)
                self.assertEqual(update_data, all_items[int(hashmap_key) - 1])
                updated_item = self.rfqerrordao.get_by_id(hashmap_key)
                self.assertEqual(updated_item, update_data)
                print("Update operation successful for RfqerrorDAO")
            except Exception as e:
                self.fail(f"Update operation failed for RfqerrorDAO: {e}")

            # Test delete
            try:
                all_items = self.rfqerrordao.get_all()
                random_index = random.choice(range(len(all_items)))
                hashmap_key = str(random_index + 1)

                item_to_delete = all_items[int(hashmap_key) - 1]

                result = self.rfqerrordao.delete(hashmap_key)
                self.assertTrue(result)
                all_data_after_delete = self.rfqerrordao.get_all()
                self.assertEqual(len(all_data_after_delete), len(all_items) - 1)
                deleted_item = self.rfqerrordao.get_by_id(hashmap_key)
                self.assertIsNone(deleted_item)
                print("Delete operation successful for RfqerrorDAO")
            except Exception as e:
                self.fail(f"Delete operation failed for RfqerrorDAO: {e}")

    def test_acceptdao(self):
        """Test CRUD operations for AcceptDAO."""
        with self._data_file_context():
            dummy_data = {"quote": "dummy_5369"}

            # Test insert
            try:
                self.acceptdao.insert(dummy_data)
                all_data = self.acceptdao.get_all()
                self.assertEqual(len(all_data), 6)
                self.assertTrue(any(item == dummy_data for item in all_data))
                print("Insert operation successful for AcceptDAO")
            except Exception as e:
                self.fail(f"Insert operation failed for AcceptDAO: {e}")

            # Test get_all
            try:
                result = self.acceptdao.get_all()
                self.assertIsInstance(result, list)
                self.assertEqual(len(result), 6)
                self.assertTrue(any(all(item[k] == v for k, v in dummy_data.items()) for item in result))
                print("Get all operation successful for AcceptDAO")
            except Exception as e:
                self.fail(f"Get all operation failed for AcceptDAO: {e}")

            # Test get_by_id
            try:
                all_items = self.acceptdao.get_all()

                result = self.acceptdao.get_by_id("6")

                self.assertIsNotNone(result)
                self.assertEqual(result, dummy_data)
                print("Get by id operation successful for AcceptDAO")
            except Exception as e:
                self.fail(f"Get by id operation failed for AcceptDAO: {e}")

            # Test update
            try:
                all_items = self.acceptdao.get_all()
                update_data = deepcopy(dummy_data)
                random_item = random.choice(range(len(all_items)))
                hashmap_key = str(random_item + 1)

                result = self.acceptdao.update(hashmap_key, **update_data)
                all_items = self.acceptdao.get_all()
                self.assertIsNotNone(result)
                self.assertEqual(update_data, all_items[int(hashmap_key) - 1])
                updated_item = self.acceptdao.get_by_id(hashmap_key)
                self.assertEqual(updated_item, update_data)
                print("Update operation successful for AcceptDAO")
            except Exception as e:
                self.fail(f"Update operation failed for AcceptDAO: {e}")

            # Test delete
            try:
                all_items = self.acceptdao.get_all()
                random_index = random.choice(range(len(all_items)))
                hashmap_key = str(random_index + 1)

                item_to_delete = all_items[int(hashmap_key) - 1]

                result = self.acceptdao.delete(hashmap_key)
                self.assertTrue(result)
                all_data_after_delete = self.acceptdao.get_all()
                self.assertEqual(len(all_data_after_delete), len(all_items) - 1)
                deleted_item = self.acceptdao.get_by_id(hashmap_key)
                self.assertIsNone(deleted_item)
                print("Delete operation successful for AcceptDAO")
            except Exception as e:
                self.fail(f"Delete operation failed for AcceptDAO: {e}")


if __name__ == "__main__":
    unittest.main()