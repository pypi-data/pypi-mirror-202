import unittest
import pycallrail.callrail as crl
import os
from pycallrail.api.call import Call
from unittest import mock

api_key = os.environ.get("API_KEY", "4a0c4ee1afda7b3872c098834c0fbe0f")

class TestCallAccountMethods(unittest.TestCase):
    """
    Test the various call related methods from the Account class.
    """
    def setUp(self):
        self.cr = crl.CallRail(api_key=api_key)
        self.account = self.cr.get_account("ACCfc800e85eba74b62ae02ef58fd76b0db")

    def tearDown(self):
        self.cr = None
        self.account = None

    def test_init(self):
        self.assertIsInstance(self.account, crl.Account)

    def test_init_with_no_api_key(self):
        with self.assertRaises(Exception):
            crl.CallRail()
    
    @mock.patch('pycallrail.api.accounts.Account.list_calls')
    def test_list_calls(self, mock_list_calls):
        mock_list_calls.return_value = [
            Call(data=
                {
                    "answered": False,
                    "business_phone_number": None,
                    "customer_city": "Denver",
                    "customer_country": "US",
                    "customer_name": "RUEGSEGGER SIMO",
                    "customer_phone_number": "+13036231131",
                    "customer_state": "CO",
                    "direction": "inbound",
                    "duration": 4,
                    "id": "CAL8154748ae6bd4e278a7cddd38a662f4f",
                    "recording": "https://api.callrail.com/v3/a/227799611/calls/111222333/recording.json",
                    "recording_duration": "27",
                    "recording_player": "https://app.callrail.com/calls/111222333/recording?access_key=3b91eb7f7cc08a4d01ed",
                    "start_time": "2017-01-24T11:27:48.119-05:00",
                    "tracking_phone_number": "+13038163491",
                    "voicemail": False,
                    "agent_email": "gil@televised.com"
                }, parent=self.account),
            Call(data=
                {
                    "answered": False,
                    "business_phone_number": None,
                    "customer_city": "Denver",
                    "customer_country": "US",
                    "customer_name": "RUEGSEGGER SIMO",
                    "customer_phone_number": "+13036231131",
                    "customer_state": "CO",
                    "direction": "inbound",
                    "duration": 4,
                    "id": "CAL8154748ae6bd4e278a7cddd38a662f4f",
                    "recording": "https://api.callrail.com/v3/a/227799611/calls/111222333/recording.json",
                    "recording_duration": "27",
                    "recording_player": "aa",
                    "start_time": "2017-01-24T11:27:48.119-05:00",
                    "tracking_phone_number": "+13038163491",
                    "voicemail": False,
                    "agent_email": "lop@lok.edu"
                }, parent=self.account)
        ]

        calls = self.account.list_calls()
        self.assertEqual(len(calls), 2)
        self.assertIsInstance(calls[0], crl.Call)
        self.assertIsInstance(calls[1], crl.Call)
        self.assertEqual(calls[0].agent_email, "gil@televised.com")
        self.assertEqual(calls[0].id, "CAL8154748ae6bd4e278a7cddd38a662f4f")

    @mock.patch('pycallrail.api.accounts.Account.get_call')
    def test_get_call(self, mock_get_call):
        mock_get_call.return_value = Call(data=
            {
                "answered": False,
                "business_phone_number": None,
                "customer_city": "Denver",
                "customer_country": "US",
                "customer_name": "RUEGSEGGER SIMO",
                "customer_phone_number": "+13036231131",
                "customer_state": "CO",
                "direction": "inbound",
                "duration": 4,
                "id": "CAL8154748ae6bd4e278a7cddd38a662f4f",
                "recording": "https://api.callrail.com/v3/a/227799611/calls/111222333/recording.json",
                "recording_duration": "27",
                "recording_player": "https://app.callrail.com/calls/111222333/recording?access_key=3b91eb7f7cc08a4d01ed",
                "start_time": "2017-01-24T11:27:48.119-05:00",
                "tracking_phone_number": "+13038163491",
                "voicemail": False,
                "agent_email": "gil@televised.com"
            }, parent=self.account)
        call = self.account.get_call("CAL8154748ae6bd4e278a7cddd38a662f4f")
        self.assertIsInstance(call, crl.Call)
        self.assertEqual(call.agent_email, "gil@televised.com")
        self.assertEqual(call.id, "CAL8154748ae6bd4e278a7cddd38a662f4f")

        @mock.patch('pycallrail.api.call.Call.update')
        def test_update_call(self, mock_update_call):
            mock_update_call.return_value = Call(data=
                {
                    "answered": False,
                    "business_phone_number": None,
                    "customer_city": "Denver",
                    "customer_country": "US",
                    "customer_name": "RUEGSEGGER SIMO",
                    "customer_phone_number": "+13036231131",
                    "customer_state": "CO",
                    "direction": "inbound",
                    "duration": 4,
                    "id": "CAL8154748ae6bd4e278a7cddd38a662f4f",
                    "recording": "https://api.callrail.com/v3/a/227799611/calls/111222333/recording.json",
                    "recording_duration": "27"
                }, parent=self.account)
            
            # Update the call, but not actually in the system
            call = Call(data=
                {
                    "answered": False,
                    "business_phone_number": None,
                    "customer_city": "Denver",
                    "customer_country": "US",
                    "customer_name": "RUEGSEGGER SIMO",
                    "customer_phone_number": "+13036231131",
                    "customer_state": "CO",
                    "direction": "inbound",
                    "duration": 4,
                    "id": "CAL8154748ae6bd4e278a7cddd38a662f4f",
                    "recording": "https://api.callrail.com/v3/a/227799611/calls/111222333/recording.json",
                    "recording_duration": "27"
                }, parent=self.account)
            
            #TODO: finish writing this test