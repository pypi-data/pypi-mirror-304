from .correos_services import test_shipment
from .helpers import test_bank_utils
from .listeners import (
    test_contract_line_listener,
    test_contract_listener,
    test_crm_lead_listener,
    test_partner_bank_listener,
    test_partner_listener,
    test_res_partner_listener,
)
from .models import (
    test_account_move_line,
    test_account_payment_order,
    test_account_payment_return_gateway,
    test_broadband_isp_info,
    test_contract,
    test_contract_line,
    test_coop_agreement,
    test_crm_lead,
    test_crm_lead_line,
    test_hr_attendance_process,
    test_mail_activity,
    test_mass_mailing,
    test_mobile_isp_info,
    test_opencell_configuration_wrapper,
    test_payment_return,
    test_previous_provider,
    test_product_category_technology_supplier,
    test_product_product,
    test_product_template,
    test_production_lot,
    test_res_partner,
    test_res_partner_bank,
    test_server_action,
    test_service_supplier,
    test_stock_move_line,
    test_subscription_request,
)
from .opencell_models import (
    test_address,
    test_crm_account_hierarchy,
    test_customer,
    test_description,
    test_opencell_service_codes,
    test_subscription,
)
from .opencell_services import (
    test_crm_account_hierarchy_create_service,
    test_crm_account_hierarchy_create_strategies,
    test_crm_account_hierarchy_update_service,
    test_crm_account_hierarchy_update_strategies,
    test_customer_update_service,
    test_subscription_service,
)
from .otrs_factories import (
    test_adsl_data_from_crm_lead_line,
    test_customer_data_from_res_partner,
    test_fiber_data_from_crm_lead_line,
    test_mobile_data_from_crm_lead_line,
    test_router_4G_data_from_crm_lead_line,
)
from .services import (
    test_account_invoice_service,
    test_change_partner_emails,
    test_contract_change_tariff_service,
    test_contract_contract_process,
    test_contract_email_change_service,
    test_contract_iban_change_service,
    test_contract_one_shot_service,
    test_coop_agreement_service,
    test_crm_lead_service,
    test_discovery_channel_service,
    test_hashids_service,
    test_mass_mailing_unsubscribe,
    test_mobile_activation_date_service,
    test_partner_email_change_service,
    test_product_catalog_service,
    test_product_one_shot_catalog_service,
    test_provider_service,
    test_res_partner_service,
    test_subscription_request_service,
    test_vat_normalizer,
)
from .services.contract_process import (
    test_fiber_contract_process,
    test_mobile_contract_process,
)
from .services.contract_services import (
    test_contract_contract_service,
    test_contract_count_controller,
    test_contract_get_fiber_contracts_to_pack_controller,
    test_contract_get_terminate_reasons,
    test_contract_search_controller,
    test_contract_terminate_controller,
)
from .somoffice import test_user
from .wizards import (
    test_account_payment_line_create,
    test_contract_address_change_wizard,
    test_contract_compensation_wizard,
    test_contract_force_oc_integration_wizard,
    test_contract_group_change_wizard,
    test_contract_holder_change,
    test_contract_iban_change_force_wizard,
    test_contract_iban_change_wizard,
    test_contract_invoice_payment_wizard,
    test_contract_mobile_check_consumption,
    test_contract_mobile_tariff_change_wizard,
    test_contract_one_shot_request_wizard,
    test_contract_tariff_change_wizard,
    test_create_lead_add_mobile_line,
    test_create_lead_from_partner_wizard,
    test_create_subscription_from_partner,
    test_crm_lead_generate_SIM_delivery_wizard,
    test_crm_lead_remesa_wizard,
    test_crm_leads_validate_wizard,
    test_mail_compose_message_wizard,
    test_partner_email_change_wizard,
    test_payment_order_generated_to_upload_queued_wizard,
)
