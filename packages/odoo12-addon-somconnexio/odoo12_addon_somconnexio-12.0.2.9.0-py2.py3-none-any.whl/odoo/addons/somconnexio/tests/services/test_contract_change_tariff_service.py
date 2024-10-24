import json
from mock import patch

import odoo
from odoo.addons.easy_my_coop_api.tests.common import BaseEMCRestCase
from odoo.exceptions import UserError


from ...helpers.date import first_day_next_month, date_to_str, last_day_of_this_month
from ...services.contract_change_tariff_process import ContractChangeTariffProcess

HOST = "127.0.0.1"
PORT = odoo.tools.config["http_port"]


class BaseEMCRestCaseAdmin(BaseEMCRestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        # Skip parent class in super to avoid recreating api key
        super(BaseEMCRestCase, cls).setUpClass(*args, **kwargs)


class TestContractChangeTariffService(BaseEMCRestCaseAdmin):
    def setUp(self, *args, **kwargs):
        super().setUp()
        # Mobile
        self.mobile_contract = self.env.ref("somconnexio.contract_mobile_il_20")
        self.old_mobile_product = self.browse_ref("somconnexio.TrucadesIllimitades20GB")
        self.new_mobile_product = self.browse_ref("somconnexio.TrucadesIllimitades50GB")
        self.mobile_data = {
            "product_code": self.new_mobile_product.default_code,
            "phone_number": self.mobile_contract.phone_number,
        }

        # Fiber contract
        self.fiber_contract = self.env.ref("somconnexio.contract_fibra_600")
        self.old_fiber_product = self.browse_ref("somconnexio.Fibra600Mb")
        self.new_fiber_product = self.browse_ref("somconnexio.Fibra100Mb")
        self.fiber_data = {
            "product_code": self.new_fiber_product.default_code,
            "code": self.fiber_contract.code,
        }

        # General
        self.partner = self.mobile_contract.partner_id
        self.url = "/public-api/change-tariff"

    def http_public_post(self, url, data, headers=None):
        if url.startswith("/"):
            url = "http://{}:{}{}".format(HOST, PORT, url)
        return self.session.post(url, json=data)

    def test_route_right_run_wizard_mobile_without_date(self):
        response = self.http_public_post(self.url, data=self.mobile_data)
        expected_start_date = first_day_next_month()

        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractChangeTariffProcess(self.env)
        process.run_from_api(**self.mobile_data)
        partner_activities = self.env['mail.activity'].search(
            [('partner_id', '=', self.partner.id)],
        )
        created_activity = partner_activities[-1]

        self.assertTrue(self.mobile_contract.contract_line_ids[0].date_end)
        self.assertEqual(self.mobile_contract.contract_line_ids[0].product_id,
                         self.old_mobile_product)
        self.assertFalse(self.mobile_contract.contract_line_ids[1].date_end)
        self.assertEqual(
            self.mobile_contract.contract_line_ids[1].date_start, expected_start_date
        )
        self.assertEqual(self.mobile_contract.contract_line_ids[1].product_id,
                         self.new_mobile_product)
        self.assertEquals(created_activity.summary, 'Canvi de tarifa a {}'.format(
            self.new_mobile_product.showed_name))
        self.assertFalse(self.mobile_contract.parent_pack_contract_id)

    def test_route_right_mobile_with_start_date(self):
        expected_start_date = first_day_next_month()
        expected_finished_date = last_day_of_this_month()
        self.mobile_data.update({"start_date": date_to_str(expected_start_date)})

        response = self.http_public_post(self.url, data=self.mobile_data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractChangeTariffProcess(self.env)
        process.run_from_api(**self.mobile_data)

        self.assertEqual(self.mobile_contract.contract_line_ids[0].date_end,
                         expected_finished_date)
        self.assertEqual(self.mobile_contract.contract_line_ids[0].product_id,
                         self.old_mobile_product)
        self.assertFalse(self.mobile_contract.contract_line_ids[1].date_end)
        self.assertEqual(self.mobile_contract.contract_line_ids[1].date_start,
                         expected_start_date)
        self.assertEqual(self.mobile_contract.contract_line_ids[1].product_id,
                         self.new_mobile_product)
        self.assertFalse(self.mobile_contract.parent_pack_contract_id)

    def test_route_right_mobile_with_OTRS_formatted_date(self):
        expected_start_date = first_day_next_month()
        expected_finished_date = last_day_of_this_month()
        self.mobile_data.update(
            {"start_date": "{} 00:00:00".format(date_to_str(expected_start_date))}
        )

        response = self.http_public_post(self.url, data=self.mobile_data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractChangeTariffProcess(self.env)
        process.run_from_api(**self.mobile_data)

        self.assertEqual(self.mobile_contract.contract_line_ids[0].date_end,
                         expected_finished_date)
        self.assertEqual(self.mobile_contract.contract_line_ids[0].product_id,
                         self.old_mobile_product)
        self.assertFalse(self.mobile_contract.contract_line_ids[1].date_end)
        self.assertEqual(self.mobile_contract.contract_line_ids[1].date_start,
                         expected_start_date)
        self.assertEqual(self.mobile_contract.contract_line_ids[1].product_id,
                         self.new_mobile_product)
        self.assertFalse(self.mobile_contract.parent_pack_contract_id)

    def test_route_right_mobile_empty_start_date(self):
        self.mobile_data.update({"start_date": ""})

        response = self.http_public_post(self.url, data=self.mobile_data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractChangeTariffProcess(self.env)
        process.run_from_api(**self.mobile_data)
        expected_start_date = first_day_next_month()

        self.assertTrue(self.mobile_contract.contract_line_ids[0].date_end)
        self.assertEqual(self.mobile_contract.contract_line_ids[0].product_id,
                         self.old_mobile_product)
        self.assertFalse(self.mobile_contract.contract_line_ids[1].date_end)
        self.assertEqual(self.mobile_contract.contract_line_ids[1].date_start,
                         expected_start_date)
        self.assertEqual(self.mobile_contract.contract_line_ids[1].product_id,
                         self.new_mobile_product)
        self.assertFalse(self.mobile_contract.parent_pack_contract_id)

    def test_route_bad_mobile_phone(self):
        wrong_phone = "8383838"
        self.mobile_data.update({"phone_number": wrong_phone})

        response = self.http_public_post(self.url, data=self.mobile_data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractChangeTariffProcess(self.env)

        self.assertRaisesRegex(
            UserError,
            "Mobile contract not found with phone: {}".format(wrong_phone),
            process.run_from_api, **self.mobile_data
        )

    def test_route_bad_product(self):
        wrong_product = "FAKE_DEFAULT_CODE"
        self.mobile_data.update({"product_code": wrong_product})

        response = self.http_public_post(self.url, data=self.mobile_data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractChangeTariffProcess(self.env)

        self.assertRaisesRegex(
            UserError,
            "Product not found with code: {}".format(
                wrong_product),
            process.run_from_api, **self.mobile_data
        )

    def test_route_bad_date(self):
        wrong_date = "202-202-202"
        self.mobile_data.update({"start_date": wrong_date})

        response = self.http_public_post(self.url, data=self.mobile_data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractChangeTariffProcess(self.env)

        self.assertRaisesRegex(
            UserError,
            "Date with unknown format: {}".format(wrong_date),
            process.run_from_api, **self.mobile_data
        )

    def test_route_neither_phone_nor_code(self):
        self.mobile_data.update({"phone_number": "", "code": ""})

        response = self.http_public_post(self.url, data=self.mobile_data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractChangeTariffProcess(self.env)

        self.assertRaises(UserError, process.run_from_api, **self.mobile_data)

    def test_route_right_run_wizard_fiber_without_date(self):
        response = self.http_public_post(self.url, data=self.fiber_data)
        expected_start_date = first_day_next_month()

        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractChangeTariffProcess(self.env)
        process.run_from_api(**self.fiber_data)
        partner_activities = self.env['mail.activity'].search(
            [('partner_id', '=', self.partner.id)],
        )
        created_activity = partner_activities[-1]

        self.assertTrue(self.fiber_contract.contract_line_ids[0].date_end)
        self.assertEqual(self.fiber_contract.contract_line_ids[0].product_id,
                         self.old_fiber_product)
        self.assertFalse(self.fiber_contract.contract_line_ids[1].date_end)
        self.assertEqual(
            self.fiber_contract.contract_line_ids[1].date_start, expected_start_date
        )
        self.assertEqual(self.fiber_contract.contract_line_ids[1].product_id,
                         self.new_fiber_product)
        self.assertEquals(created_activity.summary, 'Canvi de tarifa a {}'.format(
            self.new_fiber_product.showed_name))
        self.assertFalse(self.mobile_contract.parent_pack_contract_id)

    def test_route_right_fiber_with_start_date(self):
        expected_start_date = first_day_next_month()
        expected_finished_date = last_day_of_this_month()
        self.fiber_data.update({"start_date": date_to_str(expected_start_date)})

        response = self.http_public_post(self.url, data=self.fiber_data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractChangeTariffProcess(self.env)
        process.run_from_api(**self.fiber_data)

        self.assertEqual(self.fiber_contract.contract_line_ids[0].date_end,
                         expected_finished_date)
        self.assertEqual(self.fiber_contract.contract_line_ids[0].product_id,
                         self.old_fiber_product)
        self.assertFalse(self.fiber_contract.contract_line_ids[1].date_end)
        self.assertEqual(self.fiber_contract.contract_line_ids[1].date_start,
                         expected_start_date)
        self.assertEqual(self.fiber_contract.contract_line_ids[1].product_id,
                         self.new_fiber_product)
        self.assertFalse(self.mobile_contract.parent_pack_contract_id)

    def test_route_bad_fiber_contract_code(self):
        wrong_code = "inexisting_code"
        self.fiber_data.update({"code": wrong_code})

        response = self.http_public_post(self.url, data=self.fiber_data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractChangeTariffProcess(self.env)

        self.assertRaisesRegex(
            UserError,
            "Contract not found with code: {}".format(wrong_code),
            process.run_from_api, **self.fiber_data
        )

    def test_route_right_run_wizard_parent_pack_contract(self):
        self.mobile_data.update({
            'parent_pack_contract_id': self.fiber_data['code']
        })
        response = self.http_public_post(self.url, data=self.mobile_data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractChangeTariffProcess(self.env)
        process.run_from_api(**self.mobile_data)
        self.assertEqual(
            self.mobile_contract.parent_pack_contract_id, self.fiber_contract
        )

    @patch('odoo.addons.somconnexio.models.contract.Contract._change_tariff_only_in_ODOO')  # noqa
    def test_route_right_run_wizard_shared_bond_id_1_to_2(
            self, mock_change_tariff_odoo):
        """
        No sharing data contract can stay without beeing linked to
        another, but every contract is created independently from the API,
        so always one will be first.
        """

        shared_bond_id = "AAAAABBBB"
        sharing_data_product_2 = self.browse_ref('somconnexio.50GBCompartides2mobils')
        sharing_contract = self.browse_ref(
            'somconnexio.contract_mobile_il_50_shared_1_of_2'
        )
        # Change its shared bond to unlink it from the other contract sharing data with
        sharing_contract.mobile_contract_service_info_id.shared_bond_id = shared_bond_id

        self.assertEquals(len(sharing_contract.sharing_bond_contract_ids), 1)
        self.assertFalse(self.mobile_contract.sharing_bond_contract_ids)

        self.mobile_data.update(
            {
                "phone_number": self.mobile_contract.phone_number,
                "product_code": sharing_data_product_2.default_code,
                "shared_bond_id": shared_bond_id,
            }
        )

        response = self.http_public_post(self.url, data=self.mobile_data)

        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractChangeTariffProcess(self.env)
        process.run_from_api(**self.mobile_data)

        # No tariff change applied to first contract
        mock_change_tariff_odoo.assert_not_called()

        self.assertEqual(
            self.mobile_contract.shared_bond_id,
            sharing_contract.shared_bond_id
        )
        self.assertEquals(
            len(self.mobile_contract.sharing_bond_contract_ids), 2
        )
        self.assertIn(
            self.mobile_contract,
            sharing_contract.sharing_bond_contract_ids,
        )

    def test_route_right_run_wizard_shared_bond_id_2_to_3(self):

        sharing_contract = self.browse_ref(
            'somconnexio.contract_mobile_il_50_shared_1_of_2')
        sharing_data_product_2 = self.browse_ref('somconnexio.50GBCompartides2mobils')
        sharing_data_product_3 = self.browse_ref('somconnexio.50GBCompartides3mobils')
        shared_bond_id = sharing_contract.shared_bond_id
        expected_start_date = first_day_next_month()
        self.mobile_data.update(
            {
                "phone_number": self.mobile_contract.phone_number,
                "product_code": sharing_data_product_3.default_code,
                "shared_bond_id": shared_bond_id,
                "start_date": date_to_str(expected_start_date)
            }
        )
        self.assertFalse(self.mobile_contract.sharing_bond_contract_ids)
        self.assertEquals(
            len(sharing_contract.sharing_bond_contract_ids), 2
        )
        self.assertEquals(
            sharing_contract.current_tariff_product,
            sharing_data_product_2
        )

        response = self.http_public_post(self.url, data=self.mobile_data)

        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractChangeTariffProcess(self.env)
        process.run_from_api(**self.mobile_data)

        self.assertEqual(self.mobile_contract.shared_bond_id, shared_bond_id)

        self.assertEquals(
            len(sharing_contract.sharing_bond_contract_ids), 3
        )
        self.assertIn(
            self.mobile_contract,
            sharing_contract.sharing_bond_contract_ids
        )
        new_tariff_contract_line = sharing_contract.contract_line_ids[-1]
        self.assertEquals(
            new_tariff_contract_line.product_id,
            sharing_data_product_3
        )
        self.assertEquals(
            new_tariff_contract_line.date_start,
            expected_start_date
        )

    def test_route_right_run_wizard_shared_bond_id_3_to_4(self):

        sharing_contract = self.browse_ref(
            'somconnexio.contract_mobile_il_50_shared_1_of_3'
        )
        sharing_data_product_3 = self.browse_ref('somconnexio.50GBCompartides3mobils')
        shared_bond_id = sharing_contract.shared_bond_id
        self.mobile_data.update(
            {
                "phone_number": self.mobile_contract.phone_number,
                "product_code": sharing_data_product_3.default_code,
                "shared_bond_id": shared_bond_id,
            }
        )

        self.assertFalse(self.mobile_contract.sharing_bond_contract_ids)
        self.assertEquals(
            len(sharing_contract.sharing_bond_contract_ids), 3
        )

        response = self.http_public_post(self.url, data=self.mobile_data)

        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractChangeTariffProcess(self.env)

        self.assertRaisesRegex(
            UserError,
            "No more than 3 mobiles can share data together",
            process.run_from_api, **self.mobile_data
        )

    def test_route_right_run_wizard_shared_bond_id_OTRS_empty_character(self):
        self.mobile_data.update(
            {
                "product_code": "SE_SC_REC_MOBILE_2_SHARED_UNL_51200",
                "shared_bond_id": {},
            }
        )
        response = self.http_public_post(self.url, data=self.mobile_data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractChangeTariffProcess(self.env)
        process.run_from_api(**self.mobile_data)

        self.assertFalse(self.mobile_contract.shared_bond_id)
