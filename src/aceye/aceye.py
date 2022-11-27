import os
import json
import requests
import rich_click as click
import yaml
import urllib3
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

urllib3.disable_warnings()

class ACEye():
    def __init__(self,
                url,
                username,
                password):
        self.aci = url
        self.username = username
        self.password = password

    def aceye(self):
        self.make_directories()
        self.cookie = self.get_token()
        parsed_json = json.dumps(self.tenants(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.epgs(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.bridge_domains(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.contexts(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.application_profiles(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.l3outs(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.l2outs(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.topSystem(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.subnets(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.endpoints(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.fabric_nodes(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.physical_interfaces(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.leaf_interface_profiles(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.spine_interface_profiles(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.leaf_switch_profiles(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.spine_switch_profiles(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.vlan_pools(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.attachable_access_entity_profiles(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.contracts(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.filters(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.physical_domains(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.l3_domains(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.qos_classes(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.fault_summary(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        # parsed_json = json.dumps(self.audit_log(), indent=4, sort_keys=True)
        # self.all_files(parsed_json)
        parsed_json = json.dumps(self.ip_addresses(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        # parsed_json = json.dumps(self.events(), indent=4, sort_keys=True)
        # self.all_files(parsed_json)
        parsed_json = json.dumps(self.licenses(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.bgp_rr(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.interface_policies(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.interface_profiles(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.fabric_pods(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.fabric_paths(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.prefix_list(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.prefix_list_detailed(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.users(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.security_domains(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.contract_subjects(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.health(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.fabric_node_ssl_certificate(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.tenant_health(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.fabric_membership(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.cluster_health(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.device_packages(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.cluster_aggregate_interfaces(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.l3_interfaces(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.access_control_entities(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.access_control_instances(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.access_control_rules(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.access_control_scopes(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.cluster_physical_interfaces(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.compute_controllers(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.compute_domains(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.compute_endpoint_policy_descriptions(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.compute_providers(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.arp_adjacency_endpoints(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.arp_db(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.arp_domain(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.arp_entity(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.arp_interface(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.arp_instances(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.bgp_domains(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.bgp_domain_af(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.bgp_entities(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.bgp_instances(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.bgp_instances_policy(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.bgp_peers(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.bgp_peer_af_entries(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.bgp_peer_entries(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.bgp_rr_policies(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.cdp_adjacency_endpoints(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.cdp_entities(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.cdp_interfaces(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.cdp_instances(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.cdp_interface_addresses(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.cdp_management_addresses(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.cluster_rs_member_interfaces(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.compute_rs_domain_policies(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_board_slots(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_boards(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_cpus(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_chassis(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_dimms(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_fabric_extenders(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_fabric_ports(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_fpga(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_fan_trays(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_fan_tray_slots(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_indicator_leds(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_line_cards(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_line_card_slots(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_leaf_ports(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_port_locator_leds(), indent=4, sort_keys=True)
        self.all_files(parsed_json)        
        parsed_json = json.dumps(self.equipment_power_supplies(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_power_supply_slots(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_rs_io(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_sensors(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_sp_cmn_blk(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.equipment_sprom_lc(), indent=4, sort_keys=True)
        self.all_files(parsed_json)

    def make_directories(self):
        api_list = ['Access Control Entities',
                    'Access Control Instances',
                    'Access Control Rules',
                    'Access Control Scopes',
                    'Application Profiles',
                    'ARP Adjacency Endpoints',
                    'ARP Database',
                    'ARP Domain',
                    'ARP Entity',
                    'ARP Instances',
                    'ARP Interfaces',
                    'Attachable Access Entity Profiles',
                    'Audit Log',
                    'BGP Domain Address Families',
                    'BGP Domains',
                    'BGP Entities',
                    'BGP Instances',
                    'BGP Instances Policy',
                    'BGP Peers',
                    'BGP Peers AF Entries',
                    'BGP Peers Entries',
                    'BGP Route Reflector Policies',
                    'BGP Route Reflectors',
                    'Bridge Domains',
                    'CDP Adjacency Endpoints',
                    'CDP Entities',
                    'CDP Instances',
                    'CDP Interface Addresses',
                    'CDP Interfaces',
                    'CDP Management Addresses',
                    'Cluster Aggregate Interfaces',
                    'Cluster Health',
                    'Cluster Physical Interfaces',
                    'Cluster RS Member Interfaces',
                    'Compute Controllers',
                    'Compute Domains',
                    'Compute Endpoint Policy Descriptions',
                    'Compute Providers',
                    'Compute RS Domain Policies',
                    'Contexts',
                    'Contracts',
                    'Contract Subjects',
                    'Device Packages',
                    'Endpoints',
                    'EPG',
                    'Equipment Board Slots',
                    'Equipment Boards',
                    'Equipment Chassis',
                    'Equipment CPUs',
                    'Equipment DIMMs',
                    'Equipment Fabric Extenders',
                    'Equipment Fabric Ports',
                    'Equipment Fan Tray Slots',
                    'Equipment Fan Trays',
                    'Equipment Fans',
                    'Equipment Field Programmable Gate Arrays',
                    'Equipment Indicator LEDs',
                    'Equipment Leaf Ports',
                    'Equipment Line Card Slots',
                    'Equipment Line Cards',
                    'Equipment Port Locator LEDs',
                    'Equipment Power Supplies',
                    'Equipment Power Supply Slots',
                    'Equipment RS IO Port Physical Configs',
                    'Equipment Sensors',
                    'Equipment SP Common Blocks',
                    'Equipment SPROM LCs',
                    'Events',
                    'Fabric Membership',
                    'Fabric Nodes',
                    'Fabric Node SSL Certificates',
                    'Fabric Paths',
                    'Fabric Pods',
                    'Fault Summary',
                    'Filters',
                    'Health',
                    'Interface Policies',
                    'Interface Profiles',
                    'IP Addresses',
                    'License Entitlements',
                    'L2Outs',
                    'L3 Domains',
                    'L3 Interfaces',
                    'L3Outs',
                    'Leaf Interface Profiles',
                    'Leaf Switch Profiles',
                    'Physical Domains',
                    'Physical Interfaces',
                    'Prefix List',
                    'Prefix List Detailed',
                    'QOS Classes',
                    'Security Domains',
                    'Spine Interface Profiles',
                    'Spine Switch Profiles',
                    'Subnets',
                    'Tenant',
                    'Tenant Health',
                    'Top System',
                    'Users',
                    'VLAN Pools']
        current_directory = os.getcwd()
        for api in api_list:
            final_directory = os.path.join(current_directory, rf'{ api }/JSON')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/YAML')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/CSV')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/HTML')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/Markdown')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/Mindmap')
            os.makedirs(final_directory, exist_ok=True)

    def get_token(self):
        url = f"{ self.aci }/api/aaaLogin.json"
        payload = json.dumps({
            "aaaUser": {
                "attributes": {
                "name": f"{ self.username }",
                "pwd": f"{ self.password }"
                }
            }
        })

        response = requests.request("POST", url, data=payload, verify=False)
        print(f"<Authentication Status code {response.status_code} for { url }>")
        return response.cookies

    def tenants(self):
        self.url = f"{ self.aci }/api/node/class/fvTenant.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Tenant Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def epgs(self):
        self.url = f"{ self.aci }/api/node/class/fvAEPg.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<EPG Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def bridge_domains(self):
        self.url = f"{ self.aci }/api/node/class/fvBD.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Bridge Domains Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def contexts(self):
        self.url = f"{ self.aci }/api/node/class/fvCtx.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Contexts Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def application_profiles(self):
        self.url = f"{ self.aci }/api/node/class/fvAp.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Application Profiles Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def l3outs(self):
        self.url = f"{ self.aci }/api/node/class/l3extOut.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<L3Outs Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def l2outs(self):
        self.url = f"{ self.aci }/api/node/class/l2extOut.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<L2Outs Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def topSystem(self):
        self.url = f"{ self.aci }/api/node/class/topSystem.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Top System Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def subnets(self):
        self.url = f"{ self.aci }/api/node/class/fvSubnet.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Subnet Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def endpoints(self):
        self.url = f"{ self.aci }/api/node/class/fvCEp.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Connected Endpoints Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def fabric_nodes(self):
        self.url = f"{ self.aci }/api/node/class/fabricNode.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Fabric Nodes Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def physical_interfaces(self):
        self.url = f"{ self.aci }/api/node/class/fabricNode.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Fabric Nodes Status code { response.status_code } for { self.url }>")
        node_response_dict  = response.json()
        physical_interfaces = []
        for node in node_response_dict['imdata']:
            self.url = f"{ self.aci }/api/node/class/{ node['fabricNode']['attributes']['dn']}/l1PhysIf.json"
            response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
            print(f"<Physical Interface Status code { response.status_code } for { self.url }>")
            response_dict  = response.json()
            physical_interfaces.append(response_dict['imdata'])
        return physical_interfaces

    def leaf_interface_profiles(self):
        self.url = f"{ self.aci }/api/node/class/infraAccPortP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Leaf Interface Profiles Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def spine_interface_profiles(self):
        self.url = f"{ self.aci }/api/node/class/infraSpAccPortP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Spine Interface Profiles Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def leaf_switch_profiles(self):
        self.url = f"{ self.aci }/api/node/class/infraNodeP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Leaf Switch Profiles Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def spine_switch_profiles(self):
        self.url = f"{ self.aci }/api/node/class/infraSpineP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Spine Switch Profiles Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def vlan_pools(self):
        self.url = f"{ self.aci }/api/node/class/fvnsVlanInstP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<VLAN Pools Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def attachable_access_entity_profiles(self):
        self.url = f"{ self.aci }/api/node/class/infraAttEntityP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Attachable Access Entity Profiles Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def contracts(self):
        self.url = f"{ self.aci }/api/node/class/vzBrCP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Contracts Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def filters(self):
        self.url = f"{ self.aci }/api/node/class/vzEntry.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Filters Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def physical_domains(self):
        self.url = f"{ self.aci }/api/node/class/physDomP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Physical Domains Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def l3_domains(self):
        self.url = f"{ self.aci }/api/node/class/l3extDomP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<L3 Domains Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def qos_classes(self):
        self.url = f"{ self.aci }/api/node/class/qosClass.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<QOS Classes Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def fault_summary(self):
        self.url = f"{ self.aci }/api/node/class/faultSummary.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Fault Summary Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def audit_log(self):
        self.url = f"{ self.aci }/api/node/class/aaaModLR.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Audit Log Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def ip_addresses(self):
        self.url = f"{ self.aci }/api/node/class/fvIp.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<IP Addresses Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def events(self):
        self.url = f"{ self.aci }/api/node/class/eventRecord.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Events Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def licenses(self):
        self.url = f"{ self.aci }/api/node/class/licenseEntitlement.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<License Entitlements Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def bgp_rr(self):
        self.url = f"{ self.aci }/api/node/class/bgpRRNodePEp.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<BGP Route Reflectors Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def interface_policies(self):
        self.url = f"{ self.aci }/api/node/class/infraPortS.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Interface Policies Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def interface_profiles(self):
        self.url = f"{ self.aci }/api/node/class/infraProfile.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Interface Profiles Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def fabric_pods(self):
        self.url = f"{ self.aci }/api/node/class/fabricPod.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Fabric Pods Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def fabric_paths(self):
        self.url = f"{ self.aci }/api/node/class/fabricPath.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Fabric Paths Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def prefix_list(self):
        self.url = f"{ self.aci }/api/node/class/fvTenant.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Tenant Status code { response.status_code } for { self.url }>")
        tenants  = response.json()
        prefix_lists = []
        for tenant in tenants['imdata']:
            self.url = f"{ self.aci }/api/node/mo/uni/tn-{ tenant['fvTenant']['attributes']['name'] }.json?query-target=subtree&target-subtree-class=rtctrlSubjP"
            response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
            print(f"<Prefix List Status code { response.status_code } for { self.url }>")
            response_dict  = response.json()
            prefix_lists.append(response_dict['imdata'])
        return prefix_lists

    def prefix_list_detailed(self):
        self.url = f"{ self.aci }/api/node/class/fvTenant.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Tenant Status code { response.status_code } for { self.url }>")
        tenants  = response.json()
        prefix_lists = []
        ip_prefix_list_details = []
        for tenant in tenants['imdata']:
            self.url = f"{ self.aci }/api/node/mo/uni/tn-{ tenant['fvTenant']['attributes']['name'] }.json?query-target=subtree&target-subtree-class=rtctrlSubjP"
            response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
            print(f"<Prefix List Status code { response.status_code } for { self.url }>")
            response_dict  = response.json()
            prefix_lists.append(response_dict['imdata'])
            for item in prefix_lists:
                for prefix in item:
                    self.url = f"{ self.aci }/api/node/mo/uni/tn-{ tenant['fvTenant']['attributes']['name'] }/subj-{ prefix['rtctrlSubjP']['attributes']['name']}.json?query-target=children&target-subtree-class=rtctrlMatchRtDest"
                    response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
                    print(f"<Prefix List Detailed Status code { response.status_code } for { self.url }>")
                    response_dict  = response.json()
                    ip_prefix_list_details.append(response_dict['imdata'])
        return ip_prefix_list_details

    def users(self):
        self.url = f"{ self.aci }/api/node/class/aaaUser.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Users Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def security_domains(self):
        self.url = f"{ self.aci }/api/node/class/aaaDomain.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Security Domains Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def contract_subjects(self):
        self.url = f"{ self.aci }/api/node/class/vzSubj.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Contract Subjects Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def health(self):
        self.url = f"{ self.aci }/api/node/mo/topology/health.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Health Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def fabric_node_ssl_certificate(self):
        self.url = f"{ self.aci }/api/node/class/pkiFabricNodeSSLCertificate.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<PKI Fabric Node SSL Certificate code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def tenant_health(self):
        self.url = f"{ self.aci }/api/node/class/fvTenant.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Tenant Status code { response.status_code } for { self.url }>")
        tenants  = response.json()
        tenant_health = []
        for tenant in tenants['imdata']:
            self.url = f"{ self.aci }/api/mo/uni/tn-{ tenant['fvTenant']['attributes']['name'] }/health.json"
            response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
            print(f"<Tenant Health Status code { response.status_code } for { self.url }>")
            response_dict  = response.json()
            tenant_health.append(response_dict['imdata'])
        return tenant_health

    def fabric_membership(self):
        self.url = f"{ self.aci }/api/node/class/topSystem.json?query-target=subtree&target-subtree-class=firmwareCtrlrRunning"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Fabric Membership code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def cluster_health(self):
        self.url = f"{ self.aci }/api/node/mo/topology/pod-1/node-1/av.json?query-target=children&target-subtree-class=infraWiNode"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Cluster Health code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def device_packages(self):
        self.url = f"{ self.aci }/api/node/class/vnsMDev.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Device Packages code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def cluster_aggregate_interfaces(self):
        self.url = f"{ self.aci }/api/node/class/cnwAggrIf.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Cluster Aggregate Interfaces code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def l3_interfaces(self):
        self.url = f"{ self.aci }/api/node/class/l3Inst.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<L3 Interfaces code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def access_control_entities(self):
        self.url = f"{ self.aci }/api/node/class/actrlEntity.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Access Control Entities code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def access_control_instances(self):
        self.url = f"{ self.aci }/api/node/class/actrlInst.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Access Control Instances code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def access_control_rules(self):
        self.url = f"{ self.aci }/api/node/class/actrlRule.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Access Control Rules code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def access_control_scopes(self):
        self.url = f"{ self.aci }/api/node/class/actrlScope.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Access Control Scopes code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def cluster_physical_interfaces(self):
        self.url = f"{ self.aci }/api/node/class/cnwPhysIf.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Cluster Physical Interfaces code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def compute_controllers(self):
        self.url = f"{ self.aci }/api/node/class/compCtrlr.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Compute Controllers code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def compute_domains(self):
        self.url = f"{ self.aci }/api/node/class/compDom.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Compute Domains code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def compute_endpoint_policy_descriptions(self):
        self.url = f"{ self.aci }/api/node/class/compEpPD.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Compute Endpoint Policy Descriptions code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def compute_providers(self):
        self.url = f"{ self.aci }/api/node/class/compProv.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Compute Providers code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def arp_adjacency_endpoints(self):
        self.url = f"{ self.aci }/api/node/class/arpAdjEp.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<ARP Adjacency Endpoints code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def arp_db(self):
        self.url = f"{ self.aci }/api/node/class/arpDb.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<ARP Database code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def arp_domain(self):
        self.url = f"{ self.aci }/api/node/class/arpDom.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<ARP Domain code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def arp_entity(self):
        self.url = f"{ self.aci }/api/node/class/arpEntity.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<ARP Entity code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def arp_interface(self):
        self.url = f"{ self.aci }/api/node/class/arpIf.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<ARP Interfaces code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def arp_instances(self):
        self.url = f"{ self.aci }/api/node/class/arpInst.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<ARP Instances code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def bgp_domains(self):
        self.url = f"{ self.aci }/api/node/class/bgpDom.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<BGP Domains code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def bgp_domain_af(self):
        self.url = f"{ self.aci }/api/node/class/bgpDomAf.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<BGP Domain Address Family code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def bgp_entities(self):
        self.url = f"{ self.aci }/api/node/class/bgpEntity.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<BGP Entity code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def bgp_instances(self):
        self.url = f"{ self.aci }/api/node/class/bgpInst.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<BGP Instances code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def bgp_instances_policy(self):
        self.url = f"{ self.aci }/api/node/class/bgpInstPol.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<BGP Instances Policy code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def bgp_peers(self):
        self.url = f"{ self.aci }/api/node/class/bgpPeer.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<BGP Peers code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def bgp_peer_af_entries(self):
        self.url = f"{ self.aci }/api/node/class/bgpPeerAfEntry.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<BGP Peers AF Entries code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def bgp_peer_entries(self):
        self.url = f"{ self.aci }/api/node/class/bgpPeerEntry.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<BGP Peers Entries code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def bgp_rr_policies(self):
        self.url = f"{ self.aci }/api/node/class/bgpRRP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<BGP Route Reflector Policies code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def cdp_adjacency_endpoints(self):
        self.url = f"{ self.aci }/api/node/class/cdpAdjEp.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<CDP Adjacency Endpoints code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def cdp_entities(self):
        self.url = f"{ self.aci }/api/node/class/cdpEntity.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<CDP Entities code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def cdp_interfaces(self):
        self.url = f"{ self.aci }/api/node/class/cdpIf.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<CDP Interfaces code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def cdp_instances(self):
        self.url = f"{ self.aci }/api/node/class/cdpInst.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<CDP Instances code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def cdp_interface_addresses(self):
        self.url = f"{ self.aci }/api/node/class/cdpIntfAddr.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<CDP Interface Addresses code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def cdp_management_addresses(self):
        self.url = f"{ self.aci }/api/node/class/cdpMgmtAddr.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<CDP Management Addresses code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def cluster_rs_member_interfaces(self):
        self.url = f"{ self.aci }/api/node/class/cnwRsMbrIfs.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Cluster Node RS Member Interfaces code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def compute_rs_domain_policies(self):
        self.url = f"{ self.aci }/api/node/class/compRsDomP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Compute RS Domain Policies code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_board_slots(self):
        self.url = f"{ self.aci }/api/node/class/eqptBSlot.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment Board Slots code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_boards(self):
        self.url = f"{ self.aci }/api/node/class/eqptBoard.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment Boards code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_cpus(self):
        self.url = f"{ self.aci }/api/node/class/eqptCPU.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment CPUs code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_chassis(self):
        self.url = f"{ self.aci }/api/node/class/eqptCh.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment Chassis code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_dimms(self):
        self.url = f"{ self.aci }/api/node/class/eqptDimm.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment DIMMs code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_fabric_extenders(self):
        self.url = f"{ self.aci }/api/node/class/eqptExtCh.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment Fabric Extenders code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_fabric_ports(self):
        self.url = f"{ self.aci }/api/node/class/eqptFabP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment Fabric Ports code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_fans(self):
        self.url = f"{ self.aci }/api/node/class/eqptFan.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment Fans code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_fpga(self):
        self.url = f"{ self.aci }/api/node/class/eqptFpga.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment Field Programmable Gate Arrays code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_fan_trays(self):
        self.url = f"{ self.aci }/api/node/class/eqptFt.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment Fan Trays code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_fan_tray_slots(self):
        self.url = f"{ self.aci }/api/node/class/eqptFtSlot.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment Fan Tray Slots code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_indicator_leds(self):
        self.url = f"{ self.aci }/api/node/class/eqptIndLed.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment Indicator LEDs code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_line_cards(self):
        self.url = f"{ self.aci }/api/node/class/eqptLC.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment Line Cards code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_line_card_slots(self):
        self.url = f"{ self.aci }/api/node/class/eqptLCSlot.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment Line Card Slots code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_leaf_ports(self):
        self.url = f"{ self.aci }/api/node/class/eqptLeafP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment Leaf Ports code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_port_locator_leds(self):
        self.url = f"{ self.aci }/api/node/class/eqptLocLed.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment Port Locator LEDs code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_power_supplies(self):
        self.url = f"{ self.aci }/api/node/class/eqptPsu.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment Power Supplies code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_power_supply_slots(self):
        self.url = f"{ self.aci }/api/node/class/eqptPsuSlot.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment Power Supply Slots code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_rs_io(self):
        self.url = f"{ self.aci }/api/node/class/eqptRsIoPPhysConf.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment RS IO Port Physical Configuration code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_sensors(self):
        self.url = f"{ self.aci }/api/node/class/eqptSensor.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment Sensors code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_sp_cmn_blk(self):
        self.url = f"{ self.aci }/api/node/class/eqptSpCmnBlk.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment SP Common Blocks code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def equipment_sprom_lc(self):
        self.url = f"{ self.aci }/api/node/class/eqptSpromLc.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Equipment SPROM LC code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return response_dict

    def json_file(self, parsed_json):
        if "Tenant" in self.url:
            with open('Tenant/JSON/Tenants.json', 'w' ) as f:
                f.write(parsed_json)

        if "AEPg" in self.url:
            with open('EPG/JSON/EPGs.json', 'w' ) as f:
                f.write(parsed_json)

        if "BD" in self.url:
            with open('Bridge Domains/JSON/Bridge Domains.json', 'w' ) as f:
                f.write(parsed_json)

        if "Ctx" in self.url:
            with open('Contexts/JSON/Contexts.json', 'w' ) as f:
                f.write(parsed_json)

        if "Ap" in self.url:
            with open('Application Profiles/JSON/Application Profiles.json', 'w' ) as f:
                f.write(parsed_json)

        if "l3extOut" in self.url:
            with open('L3Outs/JSON/L3Outs.json', 'w' ) as f:
                f.write(parsed_json)

        if "l2extOut" in self.url:
            with open('L2Outs/JSON/L2Outs.json', 'w' ) as f:
                f.write(parsed_json)

        if "topSystem" in self.url:
            if "?" not in self.url:
                with open('Top System/JSON/Top System.json', 'w' ) as f:
                    f.write(parsed_json)

        if "Subnet" in self.url:
            with open('Subnets/JSON/Subnets.json', 'w' ) as f:
                f.write(parsed_json)

        if "CEp" in self.url:
            with open('Endpoints/JSON/Endpoints.json', 'w' ) as f:
                f.write(parsed_json)

        if "fabricNode" in self.url:
            with open('Fabric Nodes/JSON/Fabric Nodes.json', 'w' ) as f:
                f.write(parsed_json)

        if "l1PhysIf" in self.url:
            with open('Physical Interfaces/JSON/Physical Interfaces.json', 'w' ) as f:
                f.write(parsed_json)

        if "infraAccPortP" in self.url:
            with open('Leaf Interface Profiles/JSON/Leaf Interface Profiles.json', 'w' ) as f:
                f.write(parsed_json)

        if "infraSpAccPortP" in self.url:
            with open('Spine Interface Profiles/JSON/Spine Interface Profiles.json', 'w' ) as f:
                f.write(parsed_json)

        if "infraNodeP" in self.url:
            with open('Leaf Switch Profiles/JSON/Leaf Switch Profiles.json', 'w' ) as f:
                f.write(parsed_json)

        if "infraSpineP" in self.url:
            with open('Spine Switch Profiles/JSON/Spine Switch Profiles.json', 'w' ) as f:
                f.write(parsed_json)

        if "fvnsVlanInstP" in self.url:
            with open('VLAN Pools/JSON/VLAN Pools.json', 'w' ) as f:
                f.write(parsed_json)

        if "infraAttEntityP" in self.url:
            with open('Attachable Access Entity Profiles/JSON/Attachable Access Entity Profiles.json', 'w' ) as f:
                f.write(parsed_json)

        if "vzBrCP" in self.url:
            with open('Contracts/JSON/Contracts.json', 'w' ) as f:
                f.write(parsed_json)

        if "vzEntry" in self.url:
            with open('Filters/JSON/Filters.json', 'w' ) as f:
                f.write(parsed_json)

        if "physDomP" in self.url:
            with open('Physical Domains/JSON/Physical Domains.json', 'w' ) as f:
                f.write(parsed_json)

        if "l3extDomP" in self.url:
            with open('L3 Domains/JSON/L3 Domains.json', 'w' ) as f:
                f.write(parsed_json)

        if "qosClass" in self.url:
            with open('QOS Classes/JSON/QOS Classes.json', 'w' ) as f:
                f.write(parsed_json)

        if "faultSummary" in self.url:
            with open('Fault Summary/JSON/Fault Summary.json', 'w' ) as f:
                f.write(parsed_json)

        if "aaaModLR" in self.url:
            with open('Audit Log/JSON/Audit Log.json', 'w' ) as f:
                f.write(parsed_json)

        if "fvIp" in self.url:
            with open('IP Addresses/JSON/IP Addresses.json', 'w' ) as f:
                f.write(parsed_json)

        if "eventRecord" in self.url:
            with open('Events/JSON/Events.json', 'w' ) as f:
                f.write(parsed_json)

        if "licenseEntitlement" in self.url:
            with open('License Entitlements/JSON/License Entitlements.json', 'w' ) as f:
                f.write(parsed_json)

        if "bgpRRNodePEp" in self.url:
            with open('BGP Route Reflectors/JSON/BGP Route Reflectors.json', 'w' ) as f:
                f.write(parsed_json)

        if "infraPortS" in self.url:
            with open('Interface Policies/JSON/Interface Policies.json', 'w' ) as f:
                f.write(parsed_json)

        if "infraProfile" in self.url:
            with open('Interface Profiles/JSON/Interface Profiles.json', 'w' ) as f:
                f.write(parsed_json)

        if "fabricPod" in self.url:
            with open('Fabric Pods/JSON/Fabric Pods.json', 'w' ) as f:
                f.write(parsed_json)

        if "fabricPath" in self.url:
            with open('Fabric Paths/JSON/Fabric Paths.json', 'w' ) as f:
                f.write(parsed_json)

        if "rtctrlSubjP" in self.url:
            with open('Prefix List/JSON/Prefix List.json', 'w' ) as f:
                f.write(parsed_json)

        if "rtctrlMatchRtDest" in self.url:
            with open('Prefix List Detailed/JSON/Prefix List Detailed.json', 'w' ) as f:
                f.write(parsed_json)

        if "aaaUser" in self.url:
            with open('Users/JSON/Users.json', 'w' ) as f:
                f.write(parsed_json)

        if "aaaDomain" in self.url:
            with open('Security Domains/JSON/Security Domains.json', 'w' ) as f:
                f.write(parsed_json)

        if "vzSubj" in self.url:
            with open('Contract Subjects/JSON/Contract Subjects.json', 'w' ) as f:
                f.write(parsed_json)

        if "topology/health" in self.url:
            with open('Health/JSON/Health.json', 'w' ) as f:
                f.write(parsed_json)

        if "pkiFabricNodeSSLCertificate" in self.url:
            with open('Fabric Node SSL Certificates/JSON/Fabric Node SSL Certificates.json', 'w' ) as f:
                f.write(parsed_json)

        if "tn-" and "health" in self.url:
            with open('Tenant Health/JSON/Tenant Health.json', 'w' ) as f:
                f.write(parsed_json)

        if "firmwareCtrlrRunning" in self.url:
            with open('Fabric Membership/JSON/Fabric Membership.json', 'w' ) as f:
                f.write(parsed_json)

        if "infraWiNode" in self.url:
            with open('Cluster Health/JSON/Cluster Health.json', 'w' ) as f:
                f.write(parsed_json)

        if "vnsMDev" in self.url:
            with open('Device Packages/JSON/Device Packages.json', 'w' ) as f:
                f.write(parsed_json)

        if "cnwAggrIf" in self.url:
            with open('Cluster Aggregate Interfaces/JSON/Cluster Aggregate Interfaces.json', 'w' ) as f:
                f.write(parsed_json)

        if "l3Inst" in self.url:
            with open('L3 Interfaces/JSON/L3 Interfaces.json', 'w' ) as f:
                f.write(parsed_json)

        if "actrlEntity" in self.url:
            with open('Access Control Entities/JSON/Access Control Entities.json', 'w' ) as f:
                f.write(parsed_json)

        if "actrlInst" in self.url:
            with open('Access Control Instances/JSON/Access Control Instances.json', 'w' ) as f:
                f.write(parsed_json)

        if "actrlRule" in self.url:
            with open('Access Control Rules/JSON/Access Control Rules.json', 'w' ) as f:
                f.write(parsed_json)

        if "actrlScope" in self.url:
            with open('Access Control Scopes/JSON/Access Control Scopes.json', 'w' ) as f:
                f.write(parsed_json)

        if "cnwPhysIf" in self.url:
            with open('Cluster Physical Interfaces/JSON/Cluster Physical Interfaces.json', 'w' ) as f:
                f.write(parsed_json)

        if "compCtrlr" in self.url:
            with open('Compute Controllers/JSON/Compute Controllers.json', 'w' ) as f:
                f.write(parsed_json)

        if "compDom" in self.url:
            with open('Compute Domains/JSON/Compute Domains.json', 'w' ) as f:
                f.write(parsed_json)

        if "compEpPD" in self.url:
            with open('Compute Endpoint Policy Descriptions/JSON/Compute Endpoint Policy Descriptions.json', 'w' ) as f:
                f.write(parsed_json)

        if "compProv" in self.url:
            with open('Compute Providers/JSON/Compute Providers.json', 'w' ) as f:
                f.write(parsed_json)

        if "arpAdjEp" in self.url:
            with open('ARP Adjacency Endpoints/JSON/ARP Adjacency Endpoints.json', 'w' ) as f:
                f.write(parsed_json)

        if "arpDb" in self.url:
            with open('ARP Database/JSON/ARP Database.json', 'w' ) as f:
                f.write(parsed_json)

        if "arpDom" in self.url:
            with open('ARP Domain/JSON/ARP Domain.json', 'w' ) as f:
                f.write(parsed_json)

        if "arpEntity" in self.url:
            with open('ARP Entity/JSON/ARP Entity.json', 'w' ) as f:
                f.write(parsed_json)

        if "arpIf" in self.url:
            with open('ARP Interfaces/JSON/ARP Interfaces.json', 'w' ) as f:
                f.write(parsed_json)

        if "arpInst" in self.url:
            with open('ARP Instances/JSON/ARP Instances.json', 'w' ) as f:
                f.write(parsed_json)

        if "bgpDom" in self.url:
            if "Af" in self.url:
                with open('BGP Domain Address Families/JSON/BGP Domain Address Families.json', 'w' ) as f:
                    f.write(parsed_json)
            else:
                with open('BGP Domains/JSON/BGP Domains.json', 'w' ) as f:
                    f.write(parsed_json)

        if "bgpEntity" in self.url:
            with open('BGP Entities/JSON/BGP Entities.json', 'w' ) as f:
                f.write(parsed_json)

        if "bgpInst" in self.url:
            if "InstPol" in self.url:
                with open('BGP Instances Policy/JSON/BGP Instances Policy.json', 'w' ) as f:
                    f.write(parsed_json)
            else:
                with open('BGP Instances/JSON/BGP Instances.json', 'w' ) as f:
                    f.write(parsed_json)

        if "bgpPeer" in self.url:
            if "bgpPeerAf" in self.url:
                with open('BGP Peers AF Entries/JSON/BGP Peers AF Entries.json', 'w' ) as f:
                    f.write(parsed_json)
            elif "bgpPeerEntry" in self.url:
                with open('BGP Peers Entries/JSON/BGP Peers Entries.json', 'w' ) as f:
                    f.write(parsed_json)
            else:
                with open('BGP Peers/JSON/BGP Peers.json', 'w' ) as f:
                    f.write(parsed_json)

        if "bgpRRP" in self.url:
            with open('BGP Route Reflector Policies/JSON/BGP Route Reflector Policies.json', 'w' ) as f:
                f.write(parsed_json)

        if "cdpAdjEp" in self.url:
            with open('CDP Adjacency Endpoints/JSON/CDP Adjacency Endpoints.json', 'w' ) as f:
                f.write(parsed_json)

        if "cdpEntity" in self.url:
            with open('CDP Entities/JSON/CDP Entities.json', 'w' ) as f:
                f.write(parsed_json)

        if "cdpIf" in self.url:
            with open('CDP Interfaces/JSON/CDP Interfaces.json', 'w' ) as f:
                f.write(parsed_json)

        if "cdpInst" in self.url:
            with open('CDP Instances/JSON/CDP Instances.json', 'w' ) as f:
                f.write(parsed_json)

        if "cdpIntfAddr" in self.url:
            with open('CDP Interface Addresses/JSON/CDP Interface Addresses.json', 'w' ) as f:
                f.write(parsed_json)

        if "cdpMgmtAddr" in self.url:
            with open('CDP Management Addresses/JSON/CDP Management Addresses.json', 'w' ) as f:
                f.write(parsed_json)

        if "cnwRsMbrIfs" in self.url:
            with open('Cluster RS Member Interfaces/JSON/Cluster RS Member Interfaces.json', 'w' ) as f:
                f.write(parsed_json)

        if "compRsDomP" in self.url:
            with open('Compute RS Domain Policies/JSON/Compute RS Domain Policies.json', 'w' ) as f:
                f.write(parsed_json)

        if "eqptBSlot" in self.url:
            with open('Equipment Board Slots/JSON/Equipment Board Slots.json', 'w' ) as f:
                f.write(parsed_json)

        if "eqptBoard" in self.url:
            with open('Equipment Boards/JSON/Equipment Boards.json', 'w' ) as f:
                f.write(parsed_json)

        if "eqptCPU" in self.url:
            with open('Equipment CPUs/JSON/Equipment CPUs.json', 'w' ) as f:
                f.write(parsed_json)

        if "eqptCh" in self.url:
            with open('Equipment Chassis/JSON/Equipment Chassis.json', 'w' ) as f:
                f.write(parsed_json)

        if "eqptDimm" in self.url:
            with open('Equipment DIMMs/JSON/Equipment DIMMs.json', 'w' ) as f:
                f.write(parsed_json)

        if "eqptExtCh" in self.url:
            with open('Equipment Fabric Extenders/JSON/Equipment Fabric Extenders.json', 'w' ) as f:
                f.write(parsed_json)

        if "eqptFabP" in self.url:
            with open('Equipment Fabric Ports/JSON/Equipment Fabric Ports.json', 'w' ) as f:
                f.write(parsed_json)

        if "eqptFan" in self.url:
            with open('Equipment Fans/JSON/Equipment Fans.json', 'w' ) as f:
                f.write(parsed_json)

        if "eqptFpga" in self.url:
            with open('Equipment Field Programmable Gate Arrays/JSON/Equipment Field Programmable Gate Arrays.json', 'w' ) as f:
                f.write(parsed_json)

        if "eqptFt" in self.url:
            if "Slot" in self.url:
                with open('Equipment Fan Tray Slots/JSON/Equipment Fan Tray Slots.json', 'w' ) as f:
                    f.write(parsed_json)
            else:
                with open('Equipment Fan Trays/JSON/Equipment Fan Trays.json', 'w' ) as f:
                    f.write(parsed_json)

        if "eqptIndLed" in self.url:
            with open('Equipment Indicator LEDs/JSON/Equipment Indicator LEDs.json', 'w' ) as f:
                f.write(parsed_json)

        if "eqptLC" in self.url:
            if "Slot" in self.url:
                with open('Equipment Line Card Slots/JSON/Equipment Line Card Slots.json', 'w' ) as f:
                    f.write(parsed_json)
            else:
                with open('Equipment Line Cards/JSON/Equipment Line Cards.json', 'w' ) as f:
                    f.write(parsed_json)

        if "eqptLeafP" in self.url:
            with open('Equipment Leaf Ports/JSON/Equipment Leaf Ports.json', 'w' ) as f:
                f.write(parsed_json)

        if "eqptLocLed" in self.url:
            with open('Equipment Port Locator LEDs/JSON/Equipment Port Locator LEDs.json', 'w' ) as f:
                f.write(parsed_json)

        if "eqptPsu" in self.url:
            if "Slot" in self.url:
                with open('Equipment Power Supply Slots/JSON/Equipment Power Supply Slots.json', 'w' ) as f:
                    f.write(parsed_json)
            else:
                with open('Equipment Power Supplies/JSON/Equipment Power Supplies.json', 'w' ) as f:
                    f.write(parsed_json)

        if "eqptRsIoPPhysConf" in self.url:
            with open('Equipment RS IO Port Physical Configs/JSON/Equipment RS IO Port Physical Configs.json', 'w' ) as f:
                f.write(parsed_json)

        if "eqptSensor" in self.url:
            with open('Equipment Sensors/JSON/Equipment Sensors.json', 'w' ) as f:
                f.write(parsed_json)

        if "eqptSpCmnBlk" in self.url:
            with open('Equipment SP Common Blocks/JSON/Equipment SP Common Blocks.json', 'w' ) as f:
                f.write(parsed_json)

        if "eqptSpromLc" in self.url:
            with open('Equipment SPROM LCs/JSON/Equipment SPROM LCs.json', 'w' ) as f:
                f.write(parsed_json)

    def yaml_file(self, parsed_json):
        clean_yaml = yaml.dump(json.loads(parsed_json), default_flow_style=False)
        if "Tenant" in self.url:
            with open('Tenant/YAML/Tenants.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "AEPg" in self.url:
            with open('EPG/YAML/EPGs.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "BD" in self.url:
            with open('Bridge Domains/YAML/Bridge Domains.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "Ctx" in self.url:
            with open('Contexts/YAML/Contexts.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "Ap" in self.url:
            with open('Application Profiles/YAML/Application Profiles.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "l3extOut" in self.url:
            with open('L3Outs/YAML/L3Outs.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "l2extOut" in self.url:
            with open('L2Outs/YAML/L2Outs.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "topSystem" in self.url:
            if "?" not in self.url:
                with open('Top System/YAML/Top System.yaml', 'w' ) as f:
                    f.write(clean_yaml)

        if "Subnet" in self.url:
            with open('Subnets/YAML/Subnets.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "CEp" in self.url:
            with open('Endpoints/YAML/Endpoints.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "fabricNode" in self.url:
            with open('Fabric Nodes/YAML/Fabric Nodes.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "l1PhysIf" in self.url:
            with open('Physical Interfaces/YAML/Physical Interfaces.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "infraAccPortP" in self.url:
            with open('Leaf Interface Profiles/YAML/Leaf Interface Profiles.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "infraSpAccPortP" in self.url:
            with open('Spine Interface Profiles/YAML/Spine Interface Profiles.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "infraNodeP" in self.url:
            with open('Leaf Switch Profiles/YAML/Leaf Switch Profiles.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "infraSpineP" in self.url:
            with open('Spine Switch Profiles/YAML/Spine Switch Profiles.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "fvnsVlanInstP" in self.url:
            with open('VLAN Pools/YAML/VLAN Pools.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "infraAttEntityP" in self.url:
            with open('Attachable Access Entity Profiles/YAML/Attachable Access Entity Profiles.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "vzBrCP" in self.url:
            with open('Contracts/YAML/Contracts.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "vzEntry" in self.url:
            with open('Filters/YAML/Filters.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "physDomP" in self.url:
            with open('Physical Domains/YAML/Physical Domains.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "l3extDomP" in self.url:
            with open('L3 Domains/YAML/L3 Domains.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "qosClass" in self.url:
            with open('QOS Classes/YAML/QOS Classes.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "faultSummary" in self.url:
            with open('Fault Summary/YAML/Fault Summary.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "aaaModLR" in self.url:
            with open('Audit Log/YAML/Audit Log.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "fvIp" in self.url:
            with open('IP Addresses/YAML/IP Addresses.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "eventRecord" in self.url:
            with open('Events/YAML/Events.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "licenseEntitlement" in self.url:
            with open('License Entitlements/YAML/License Entitlements.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "bgpRRNodePEp" in self.url:
            with open('BGP Route Reflectors/YAML/BGP Route Reflectors.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "infraPortS" in self.url:
            with open('Interface Policies/YAML/Interface Policies.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "infraProfile" in self.url:
            with open('Interface Profiles/YAML/Interface Profiles.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "fabricPod" in self.url:
            with open('Fabric Pods/YAML/Fabric Pods.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "fabricPath" in self.url:
            with open('Fabric Paths/YAML/Fabric Paths.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "rtctrlSubjP" in self.url:
            with open('Prefix List/YAML/Prefix List.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "rtctrlMatchRtDest" in self.url:
            with open('Prefix List Detailed/YAML/Prefix List Detailed.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "aaaUser" in self.url:
            with open('Users/YAML/Users.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "aaaDomain" in self.url:
            with open('Security Domains/YAML/Security Domains.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "vzSubj" in self.url:
            with open('Contract Subjects/YAML/Contract Subjects.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "health" in self.url:
            with open('Health/YAML/Health.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "pkiFabricNodeSSLCertificate" in self.url:
            with open('Fabric Node SSL Certificates/YAML/Fabric Node SSL Certificates.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "tn-" and "health" in self.url:
            with open('Tenant Health/YAML/Tenant Health.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "firmwareCtrlrRunning" in self.url:
            with open('Fabric Membership/YAML/Fabric Membership.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "infraWiNode" in self.url:
            with open('Cluster Health/YAML/Cluster Health.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "vnsMDev" in self.url:
            with open('Device Packages/YAML/Device Packages.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "cnwAggrIf" in self.url:
            with open('Cluster Aggregate Interfaces/YAML/Cluster Aggregate Interfaces.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "l3Inst" in self.url:
            with open('L3 Interfaces/YAML/L3 Interfaces.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "actrlEntity" in self.url:
            with open('Access Control Entities/YAML/Access Control Entities.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "actrlInst" in self.url:
            with open('Access Control Instances/YAML/Access Control Instances.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "actrlRule" in self.url:
            with open('Access Control Rules/YAML/Access Control Rules.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "actrlScope" in self.url:
            with open('Access Control Scopes/YAML/Access Control Scopes.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "cnwPhysIf" in self.url:
            with open('Cluster Physical Interfaces/YAML/Cluster Physical Interfaces.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "compCtrlr" in self.url:
            with open('Compute Controllers/YAML/Compute Controllers.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "compDom" in self.url:
            with open('Compute Domains/YAML/Compute Domains.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "compEpPD" in self.url:
            with open('Compute Endpoint Policy Descriptions/YAML/Compute Endpoint Policy Descriptions.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "compProv" in self.url:
            with open('Compute Providers/YAML/Compute Providers.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "arpAdjEp" in self.url:
            with open('ARP Adjacency Endpoints/YAML/ARP Adjacency Endpoints.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "arpDb" in self.url:
            with open('ARP Database/YAML/ARP Database.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "arpDom" in self.url:
            with open('ARP Domain/YAML/ARP Domain.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "arpEntity" in self.url:
            with open('ARP Entity/YAML/ARP Entity.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "arpIf" in self.url:
            with open('ARP Interfaces/YAML/ARP Interfaces.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "arpInst" in self.url:
            with open('ARP Instances/YAML/ARP Instances.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "bgpDom" in self.url:
            if "Af" in self.url:
                with open('BGP Domain Address Families/YAML/BGP Domain Address Families.yaml', 'w' ) as f:
                    f.write(clean_yaml)
            else:
                with open('BGP Domains/YAML/BGP Domains.yaml', 'w' ) as f:
                    f.write(clean_yaml)

        if "bgpEntity" in self.url:
            with open('BGP Entities/YAML/BGP Entities.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "bgpInst" in self.url:
            if "InstPol" in self.url:
                with open('BGP Instances Policy/YAML/BGP Instances Policy.yaml', 'w' ) as f:
                    f.write(clean_yaml)
            else:
                with open('BGP Instances/YAML/BGP Instances.yaml', 'w' ) as f:
                    f.write(clean_yaml)

        if "bgpPeer" in self.url:
            if "bgpPeerAf" in self.url:
                with open('BGP Peers AF Entries/YAML/BGP Peers AF Entries.yaml', 'w' ) as f:
                    f.write(clean_yaml)
            elif "bgpPeerEntry" in self.url:
                with open('BGP Peers Entries/YAML/BGP Peers Entries.yaml', 'w' ) as f:
                    f.write(clean_yaml)
            else:
                with open('BGP Peers/YAML/BGP Peers.yaml', 'w' ) as f:
                    f.write(clean_yaml)

        if "bgpRRP" in self.url:
            with open('BGP Route Reflector Policies/YAML/BGP Route Reflector Policies.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "cdpAdjEp" in self.url:
            with open('CDP Adjacency Endpoints/YAML/CDP Adjacency Endpoints.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "cdpEntity" in self.url:
            with open('CDP Entities/YAML/CDP Entities.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "cdpIf" in self.url:
            with open('CDP Interfaces/YAML/CDP Interfaces.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "cdpInst" in self.url:
            with open('CDP Instances/YAML/CDP Instances.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "cdpIntfAddr" in self.url:
            with open('CDP Interface Addresses/YAML/CDP Interface Addresses.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "cdpMgmtAddr" in self.url:
            with open('CDP Management Addresses/YAML/CDP Management Addresses.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "cnwRsMbrIfs" in self.url:
            with open('Cluster RS Member Interfaces/YAML/Cluster RS Member Interfaces.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "compRsDomP" in self.url:
            with open('Compute RS Domain Policies/YAML/Compute RS Domain Policies.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "eqptBSlot" in self.url:
            with open('Equipment Board Slots/YAML/Equipment Board Slots.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "eqptBoard" in self.url:
            with open('Equipment Boards/YAML/Equipment Boards.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "eqptCPU" in self.url:
            with open('Equipment CPUs/YAML/Equipment CPUs.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "eqptCh" in self.url:
            with open('Equipment Chassis/YAML/Equipment Chassis.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "eqptDimm" in self.url:
            with open('Equipment DIMMs/YAML/Equipment DIMMs.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "eqptExtCh" in self.url:
            with open('Equipment Fabric Extenders/YAML/Equipment Fabric Extenders.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "eqptFabP" in self.url:
            with open('Equipment Fabric Ports/YAML/Equipment Fabric Ports.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "eqptFan" in self.url:
            with open('Equipment Fans/YAML/Equipment Fans.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "eqptFpga" in self.url:
            with open('Equipment Field Programmable Gate Arrays/YAML/Equipment Field Programmable Gate Arrays.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "eqptFt" in self.url:
            if "Slot" in self.url:
                with open('Equipment Fan Tray Slots/YAML/Equipment Fan Tray Slots.yaml', 'w' ) as f:
                    f.write(clean_yaml)
            else:
                with open('Equipment Fan Trays/YAML/Equipment Fan Trays.yaml', 'w' ) as f:
                    f.write(clean_yaml)

        if "eqptIndLed" in self.url:
            with open('Equipment Indicator LEDs/YAML/Equipment Indicator LEDs.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "eqptLC" in self.url:
            if "Slot" in self.url:
                with open('Equipment Line Card Slots/YAML/Equipment Line Card Slots.yaml', 'w' ) as f:
                    f.write(clean_yaml)
            else:
                with open('Equipment Line Cards/YAML/Equipment Line Cards.yaml', 'w' ) as f:
                    f.write(clean_yaml)

        if "eqptLeafP" in self.url:
            with open('Equipment Leaf Ports/YAML/Equipment Leaf Ports.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "eqptLocLed" in self.url:
            with open('Equipment Port Locator LEDs/YAML/Equipment Port Locator LEDs.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "eqptPsu" in self.url:
            if "Slot" in self.url:
                with open('Equipment Power Supply Slots/YAML/Equipment Power Supply Slots.yaml', 'w' ) as f:
                    f.write(clean_yaml)
            else:
                with open('Equipment Power Supplies/YAML/Equipment Power Supplies.yaml', 'w' ) as f:
                    f.write(clean_yaml)

        if "eqptRsIoPPhysConf" in self.url:
            with open('Equipment RS IO Port Physical Configs/YAML/Equipment RS IO Port Physical Configs.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "eqptSensor" in self.url:
            with open('Equipment Sensors/YAML/Equipment Sensors.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "eqptSpCmnBlk" in self.url:
            with open('Equipment SP Common Blocks/YAML/Equipment SP Common Blocks.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "eqptSpromLc" in self.url:
            with open('Equipment SPROM LCs/YAML/Equipment SPROM LCs.yaml', 'w' ) as f:
                f.write(clean_yaml)

    def csv_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        csv_template = env.get_template('aci_csv.j2')
        csv_output = csv_template.render(api = self.url,
                                         data_to_template = json.loads(parsed_json))
        if "Tenant" in self.url:
            with open('Tenant/CSV/Tenants.csv', 'w' ) as f:
                f.write(csv_output)

        if "AEPg" in self.url:
            with open('EPG/CSV/EPGs.csv', 'w' ) as f:
                f.write(csv_output)

        if "BD" in self.url:
            with open('Bridge Domains/CSV/Bridge Domains.csv', 'w' ) as f:
                f.write(csv_output)

        if "Ctx" in self.url:
            with open('Contexts/CSV/Contexts.csv', 'w' ) as f:
                f.write(csv_output)

        if "Ap" in self.url:
            with open('Application Profiles/CSV/Application Profiles.csv', 'w' ) as f:
                f.write(csv_output)

        if "l3extOut" in self.url:
            with open('L3Outs/CSV/L3Outs.csv', 'w' ) as f:
                f.write(csv_output)

        if "l2extOut" in self.url:
            with open('L2Outs/CSV/L2Outs.csv', 'w' ) as f:
                f.write(csv_output)

        if "topSystem" in self.url:
            if "?" not in self.url:
                with open('Top System/CSV/Top System.csv', 'w' ) as f:
                    f.write(csv_output)

        if "Subnet" in self.url:
            with open('Subnets/CSV/Subnets.csv', 'w' ) as f:
                f.write(csv_output)

        if "CEp" in self.url:
            with open('Endpoints/CSV/Endpoints.csv', 'w' ) as f:
                f.write(csv_output)

        if "fabricNode" in self.url:
            with open('Fabric Nodes/CSV/Fabric Nodes.csv', 'w' ) as f:
                f.write(csv_output)

        if "l1PhysIf" in self.url:
            with open('Physical Interfaces/CSV/Physical Interfaces.csv', 'w' ) as f:
                f.write(csv_output)

        if "infraAccPortP" in self.url:
            with open('Leaf Interface Profiles/CSV/Leaf Interface Profiles.csv', 'w' ) as f:
                f.write(csv_output)

        if "infraSpAccPortP" in self.url:
            with open('Spine Interface Profiles/CSV/Spine Interface Profiles.csv', 'w' ) as f:
                f.write(csv_output)

        if "infraNodeP" in self.url:
            with open('Leaf Switch Profiles/CSV/Leaf Switch Profiles.csv', 'w' ) as f:
                f.write(csv_output)

        if "infraSpineP" in self.url:
            with open('Spine Switch Profiles/CSV/Spine Switch Profiles.csv', 'w' ) as f:
                f.write(csv_output)

        if "fvnsVlanInstP" in self.url:
            with open('VLAN Pools/CSV/VLAN Pools.csv', 'w' ) as f:
                f.write(csv_output)

        if "infraAttEntityP" in self.url:
            with open('Attachable Access Entity Profiles/CSV/Attachable Access Entity Profiles.csv', 'w' ) as f:
                f.write(csv_output)

        if "vzBrCP" in self.url:
            with open('Contracts/CSV/Contracts.csv', 'w' ) as f:
                f.write(csv_output)

        if "vzEntry" in self.url:
            with open('Filters/CSV/Filters.csv', 'w' ) as f:
                f.write(csv_output)

        if "physDomP" in self.url:
            with open('Physical Domains/CSV/Physical Domains.csv', 'w' ) as f:
                f.write(csv_output)

        if "l3extDomP" in self.url:
            with open('L3 Domains/CSV/L3 Domains.csv', 'w' ) as f:
                f.write(csv_output)

        if "qosClass" in self.url:
            with open('QOS Classes/CSV/QOS Classes.csv', 'w' ) as f:
                f.write(csv_output)

        if "faultSummary" in self.url:
            with open('Fault Summary/CSV/Fault Summary.csv', 'w' ) as f:
                f.write(csv_output)

        if "aaaModLR" in self.url:
            with open('Audit Log/CSV/Audit Log.csv', 'w' ) as f:
                f.write(csv_output)

        if "fvIp" in self.url:
            with open('IP Addresses/CSV/IP Addresses.csv', 'w' ) as f:
                f.write(csv_output)

        if "eventRecord" in self.url:
            with open('Events/CSV/Events.csv', 'w' ) as f:
                f.write(csv_output)

        if "licenseEntitlement" in self.url:
            with open('License Entitlements/CSV/License Entitlements.csv', 'w' ) as f:
                f.write(csv_output)

        if "bgpRRNodePEp" in self.url:
            with open('BGP Route Reflectors/CSV/BGP Route Reflectors.csv', 'w' ) as f:
                f.write(csv_output)

        if "infraPortS" in self.url:
            with open('Interface Policies/CSV/Interface Policies.csv', 'w' ) as f:
                f.write(csv_output)

        if "infraProfile" in self.url:
            with open('Interface Profiles/CSV/Interface Profiles.csv', 'w' ) as f:
                f.write(csv_output)

        if "fabricPod" in self.url:
            with open('Fabric Pods/CSV/Fabric Pods.csv', 'w' ) as f:
                f.write(csv_output)

        if "fabricPath" in self.url:
            with open('Fabric Paths/CSV/Fabric Paths.csv', 'w' ) as f:
                f.write(csv_output)

        if "rtctrlSubjP" in self.url:
            with open('Prefix List/CSV/Prefix List.csv', 'w' ) as f:
                f.write(csv_output)

        if "rtctrlMatchRtDest" in self.url:
            with open('Prefix List Detailed/CSV/Prefix List Detailed.csv', 'w' ) as f:
                f.write(csv_output)

        if "aaaUser" in self.url:
            with open('Users/CSV/Users.csv', 'w' ) as f:
                f.write(csv_output)

        if "aaaDomain" in self.url:
            with open('Security Domains/CSV/Security Domains.csv', 'w' ) as f:
                f.write(csv_output)

        if "vzSubj" in self.url:
            with open('Contract Subjects/CSV/Contract Subjects.csv', 'w' ) as f:
                f.write(csv_output)

        if "health" in self.url:
            with open('Health/CSV/Health.csv', 'w' ) as f:
                f.write(csv_output)

        if "pkiFabricNodeSSLCertificate" in self.url:
            with open('Fabric Node SSL Certificates/CSV/Fabric Node SSL Certificates.csv', 'w' ) as f:
                f.write(csv_output)

        if "tn-" and "health" in self.url:
            with open('Tenant Health/CSV/Tenant Health.csv', 'w' ) as f:
                f.write(csv_output)

        if "firmwareCtrlrRunning" in self.url:
            with open('Fabric Membership/CSV/Fabric Membership.csv', 'w' ) as f:
                f.write(csv_output)

        if "infraWiNode" in self.url:
            with open('Cluster Health/CSV/Cluster Health.csv', 'w' ) as f:
                f.write(csv_output)

        if "vnsMDev" in self.url:
            with open('Device Packages/CSV/Device Packages.csv', 'w' ) as f:
                f.write(csv_output)

        if "cnwAggrIf" in self.url:
            with open('Cluster Aggregate Interfaces/CSV/Cluster Aggregate Interfaces.csv', 'w' ) as f:
                f.write(csv_output)

        if "l3Inst" in self.url:
            with open('L3 Interfaces/CSV/L3 Interfaces.csv', 'w' ) as f:
                f.write(csv_output)

        if "actrlEntity" in self.url:
            with open('Access Control Entities/CSV/Access Control Entities.csv', 'w' ) as f:
                f.write(csv_output)

        if "actrlInst" in self.url:
            with open('Access Control Instances/CSV/Access Control Instances.csv', 'w' ) as f:
                f.write(csv_output)

        if "actrlRule" in self.url:
            with open('Access Control Rules/CSV/Access Control Rules.csv', 'w' ) as f:
                f.write(csv_output)

        if "actrlScope" in self.url:
            with open('Access Control Scopes/CSV/Access Control Scopes.csv', 'w' ) as f:
                f.write(csv_output)

        if "cnwPhysIf" in self.url:
            with open('Cluster Physical Interfaces/CSV/Cluster Physical Interfaces.csv', 'w' ) as f:
                f.write(csv_output)

        if "compCtrlr" in self.url:
            with open('Compute Controllers/CSV/Compute Controllers.csv', 'w' ) as f:
                f.write(csv_output)

        if "compDom" in self.url:
            with open('Compute Domains/CSV/Compute Domains.csv', 'w' ) as f:
                f.write(csv_output)

        if "compEpPD" in self.url:
            with open('Compute Endpoint Policy Descriptions/CSV/Compute Endpoint Policy Descriptions.csv', 'w' ) as f:
                f.write(csv_output)

        if "compProv" in self.url:
            with open('Compute Providers/CSV/Compute Providers.csv', 'w' ) as f:
                f.write(csv_output)

        if "arpAdjEp" in self.url:
            with open('ARP Adjacency Endpoints/CSV/ARP Adjacency Endpoints.csv', 'w' ) as f:
                f.write(csv_output)

        if "arpDb" in self.url:
            with open('ARP Database/CSV/ARP Database.csv', 'w' ) as f:
                f.write(csv_output)

        if "arpDom" in self.url:
            with open('ARP Domain/CSV/ARP Domain.csv', 'w' ) as f:
                f.write(csv_output)

        if "arpEntity" in self.url:
            with open('ARP Entity/CSV/ARP Entity.csv', 'w' ) as f:
                f.write(csv_output)

        if "arpIf" in self.url:
            with open('ARP Interfaces/CSV/ARP Interfaces.csv', 'w' ) as f:
                f.write(csv_output)

        if "arpInst" in self.url:
            with open('ARP Instances/CSV/ARP Instances.csv', 'w' ) as f:
                f.write(csv_output)

        if "bgpDom" in self.url:
            if "Af" in self.url:
                with open('BGP Domain Address Families/CSV/BGP Domain Address Families.csv', 'w' ) as f:
                    f.write(csv_output)
            else:
                with open('BGP Domains/CSV/BGP Domains.csv', 'w' ) as f:
                    f.write(csv_output)

        if "bgpEntity" in self.url:
            with open('BGP Entities/CSV/BGP Entities.csv', 'w' ) as f:
                f.write(csv_output)

        if "bgpInst" in self.url:
            if "InstPol" in self.url:
                with open('BGP Instances Policy/CSV/BGP Instances Policy.csv', 'w' ) as f:
                    f.write(csv_output)
            else:
                with open('BGP Instances/CSV/BGP Instances.csv', 'w' ) as f:
                    f.write(csv_output)

        if "bgpPeer" in self.url:
            if "bgpPeerAf" in self.url:
                with open('BGP Peers AF Entries/CSV/BGP Peers AF Entries.csv', 'w' ) as f:
                    f.write(csv_output)
            elif "bgpPeerEntry" in self.url:
                with open('BGP Peers Entries/CSV/BGP Peers Entries.csv', 'w' ) as f:
                    f.write(csv_output)
            else:
                with open('BGP Peers/CSV/BGP Peers.csv', 'w' ) as f:
                    f.write(csv_output)

        if "bgpRRP" in self.url:
            with open('BGP Route Reflector Policies/CSV/BGP Route Reflector Policies.csv', 'w' ) as f:
                f.write(csv_output)

        if "cdpAdjEp" in self.url:
            with open('CDP Adjacency Endpoints/CSV/CDP Adjacency Endpoints.csv', 'w' ) as f:
                f.write(csv_output)

        if "cdpEntity" in self.url:
            with open('CDP Entities/CSV/CDP Entities.csv', 'w' ) as f:
                f.write(csv_output)

        if "cdpIf" in self.url:
            with open('CDP Interfaces/CSV/CDP Interfaces.csv', 'w' ) as f:
                f.write(csv_output)

        if "cdpInst" in self.url:
            with open('CDP Instances/CSV/CDP Instances.csv', 'w' ) as f:
                f.write(csv_output)

        if "cdpIntfAddr" in self.url:
            with open('CDP Interface Addresses/CSV/CDP Interface Addresses.csv', 'w' ) as f:
                f.write(csv_output)

        if "cdpMgmtAddr" in self.url:
            with open('CDP Management Addresses/CSV/CDP Management Addresses.csv', 'w' ) as f:
                f.write(csv_output)

        if "cnwRsMbrIfs" in self.url:
            with open('Cluster RS Member Interfaces/CSV/Cluster RS Member Interfaces.csv', 'w' ) as f:
                f.write(csv_output)

        if "compRsDomP" in self.url:
            with open('Compute RS Domain Policies/CSV/Compute RS Domain Policies.csv', 'w' ) as f:
                f.write(csv_output)

        if "eqptBSlot" in self.url:
            with open('Equipment Board Slots/CSV/Equipment Board Slots.csv', 'w' ) as f:
                f.write(csv_output)

        if "eqptBoard" in self.url:
            with open('Equipment Boards/CSV/Equipment Boards.csv', 'w' ) as f:
                f.write(csv_output)

        if "eqptCPU" in self.url:
            with open('Equipment CPUs/CSV/Equipment CPUs.csv', 'w' ) as f:
                f.write(csv_output)

        if "eqptCh" in self.url:
            with open('Equipment Chassis/CSV/Equipment Chassis.csv', 'w' ) as f:
                f.write(csv_output)

        if "eqptDimm" in self.url:
            with open('Equipment DIMMs/CSV/Equipment DIMMs.csv', 'w' ) as f:
                f.write(csv_output)

        if "eqptExtCh" in self.url:
            with open('Equipment Fabric Extenders/CSV/Equipment Fabric Extenders.csv', 'w' ) as f:
                f.write(csv_output)

        if "eqptFabP" in self.url:
            with open('Equipment Fabric Ports/CSV/Equipment Fabric Ports.csv', 'w' ) as f:
                f.write(csv_output)

        if "eqptFan" in self.url:
            with open('Equipment Fans/CSV/Equipment Fans.csv', 'w' ) as f:
                f.write(csv_output)

        if "eqptFpga" in self.url:
            with open('Equipment Field Programmable Gate Arrays/CSV/Equipment Field Programmable Gate Arrays.csv', 'w' ) as f:
                f.write(csv_output)

        if "eqptFt" in self.url:
            if "Slot" in self.url:
                with open('Equipment Fan Tray Slots/CSV/Equipment Fan Tray Slots.csv', 'w' ) as f:
                    f.write(csv_output)
            else:
                with open('Equipment Fan Trays/CSV/Equipment Fan Trays.csv', 'w' ) as f:
                    f.write(csv_output)

        if "eqptIndLed" in self.url:
            with open('Equipment Indicator LEDs/CSV/Equipment Indicator LEDs.csv', 'w' ) as f:
                f.write(csv_output)

        if "eqptLC" in self.url:
            if "Slot" in self.url:
                with open('Equipment Line Card Slots/CSV/Equipment Line Card Slots.csv', 'w' ) as f:
                    f.write(csv_output)
            else:
                with open('Equipment Line Cards/CSV/Equipment Line Cards.csv', 'w' ) as f:
                    f.write(csv_output)

        if "eqptLeafP" in self.url:
            with open('Equipment Leaf Ports/CSV/Equipment Leaf Ports.csv', 'w' ) as f:
                f.write(csv_output)

        if "eqptLocLed" in self.url:
            with open('Equipment Port Locator LEDs/CSV/Equipment Port Locator LEDs.csv', 'w' ) as f:
                f.write(csv_output)

        if "eqptPsu" in self.url:
            if "Slot" in self.url:
                with open('Equipment Power Supply Slots/CSV/Equipment Power Supply Slots.csv', 'w' ) as f:
                    f.write(csv_output)
            else:
                with open('Equipment Power Supplies/CSV/Equipment Power Supplies.csv', 'w' ) as f:
                    f.write(csv_output)

        if "eqptRsIoPPhysConf" in self.url:
            with open('Equipment RS IO Port Physical Configs/CSV/Equipment RS IO Port Physical Configs.csv', 'w' ) as f:
                f.write(csv_output)

        if "eqptSensor" in self.url:
            with open('Equipment Sensors/CSV/Equipment Sensors.csv', 'w' ) as f:
                f.write(csv_output)

        if "eqptSpCmnBlk" in self.url:
            with open('Equipment SP Common Blocks/CSV/Equipment SP Common Blocks.csv', 'w' ) as f:
                f.write(csv_output)

        if "eqptSpromLc" in self.url:
            with open('Equipment SPROM LCs/CSV/Equipment SPROM LCs.csv', 'w' ) as f:
                f.write(csv_output)

    def markdown_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        markdown_template = env.get_template('aci_markdown.j2')
        markdown_output = markdown_template.render(api = self.url,
                                         data_to_template = json.loads(parsed_json),
                                         url = self.aci)
        if "Tenant" in self.url:
            with open('Tenant/Markdown/Tenants.md', 'w' ) as f:
                f.write(markdown_output)

        if "AEPg" in self.url:
            with open('EPG/Markdown/EPGs.md', 'w' ) as f:
                f.write(markdown_output)

        if "BD" in self.url:
            with open('Bridge Domains/Markdown/Bridge Domains.md', 'w' ) as f:
                f.write(markdown_output)

        if "Ctx" in self.url:
            with open('Contexts/Markdown/Contexts.md', 'w' ) as f:
                f.write(markdown_output)

        if "Ap" in self.url:
            with open('Application Profiles/Markdown/Application Profiles.md', 'w' ) as f:
                f.write(markdown_output)

        if "l3extOut" in self.url:
            with open('L3Outs/Markdown/L3Outs.md', 'w' ) as f:
                f.write(markdown_output)

        if "l2extOut" in self.url:
            with open('L2Outs/Markdown/L2Outs.md', 'w' ) as f:
                f.write(markdown_output)

        if "topSystem" in self.url:
            if "?" not in self.url:
                with open('Top System/Markdown/Top System.md', 'w' ) as f:
                    f.write(markdown_output)

        if "Subnet" in self.url:
            with open('Subnets/Markdown/Subnets.md', 'w' ) as f:
                f.write(markdown_output)

        if "CEp" in self.url:
            with open('Endpoints/Markdown/Endpoints.md', 'w' ) as f:
                f.write(markdown_output)

        if "fabricNode" in self.url:
            with open('Fabric Nodes/Markdown/Fabric Nodes.md', 'w' ) as f:
                f.write(markdown_output)

        if "l1PhysIf" in self.url:
            with open('Physical Interfaces/Markdown/Physical Interfaces.md', 'w' ) as f:
                f.write(markdown_output)

        if "infraAccPortP" in self.url:
            with open('Leaf Interface Profiles/Markdown/Leaf Interface Profiles.md', 'w' ) as f:
                f.write(markdown_output)

        if "infraSpAccPortP" in self.url:
            with open('Spine Interface Profiles/Markdown/Spine Interface Profiles.md', 'w' ) as f:
                f.write(markdown_output)

        if "infraNodeP" in self.url:
            with open('Leaf Switch Profiles/Markdown/Leaf Switch Profiles.md', 'w' ) as f:
                f.write(markdown_output)

        if "infraSpineP" in self.url:
            with open('Spine Switch Profiles/Markdown/Spine Switch Profiles.md', 'w' ) as f:
                f.write(markdown_output)

        if "fvnsVlanInstP" in self.url:
            with open('VLAN Pools/Markdown/VLAN Pools.md', 'w' ) as f:
                f.write(markdown_output)

        if "infraAttEntityP" in self.url:
            with open('Attachable Access Entity Profiles/Markdown/Attachable Access Entity Profiles.md', 'w' ) as f:
                f.write(markdown_output)

        if "vzBrCP" in self.url:
            with open('Contracts/Markdown/Contracts.md', 'w' ) as f:
                f.write(markdown_output)

        if "vzEntry" in self.url:
            with open('Filters/Markdown/Filters.md', 'w' ) as f:
                f.write(markdown_output)

        if "physDomP" in self.url:
            with open('Physical Domains/Markdown/Physical Domains.md', 'w' ) as f:
                f.write(markdown_output)

        if "l3extDomP" in self.url:
            with open('L3 Domains/Markdown/L3 Domains.md', 'w' ) as f:
                f.write(markdown_output)

        if "qosClass" in self.url:
            with open('QOS Classes/Markdown/QOS Classes.md', 'w' ) as f:
                f.write(markdown_output)

        if "faultSummary" in self.url:
            with open('Fault Summary/Markdown/Fault Summary.md', 'w' ) as f:
                f.write(markdown_output)

        if "aaaModLR" in self.url:
            with open('Audit Log/Markdown/Audit Log.md', 'w' ) as f:
                f.write(markdown_output)

        if "fvIp" in self.url:
            with open('IP Addresses/Markdown/IP Addresses.md', 'w' ) as f:
                f.write(markdown_output)

        if "eventRecord" in self.url:
            with open('Events/Markdown/Events.md', 'w' ) as f:
                f.write(markdown_output)

        if "licenseEntitlement" in self.url:
            with open('License Entitlements/Markdown/License Entitlements.md', 'w' ) as f:
                f.write(markdown_output)

        if "bgpRRNodePEp" in self.url:
            with open('BGP Route Reflectors/Markdown/BGP Route Reflectors.md', 'w' ) as f:
                f.write(markdown_output)

        if "infraPortS" in self.url:
            with open('Interface Policies/Markdown/Interface Policies.md', 'w' ) as f:
                f.write(markdown_output)

        if "infraProfile" in self.url:
            with open('Interface Profiles/Markdown/Interface Profiles.md', 'w' ) as f:
                f.write(markdown_output)

        if "fabricPod" in self.url:
            with open('Fabric Pods/Markdown/Fabric Pods.md', 'w' ) as f:
                f.write(markdown_output)

        if "fabricPath" in self.url:
            with open('Fabric Paths/Markdown/Fabric Paths.md', 'w' ) as f:
                f.write(markdown_output)

        if "rtctrlSubjP" in self.url:
            with open('Prefix List/Markdown/Prefix List.md', 'w' ) as f:
                f.write(markdown_output)

        if "rtctrlMatchRtDest" in self.url:
            with open('Prefix List Detailed/Markdown/Prefix List Detailed.md', 'w' ) as f:
                f.write(markdown_output)

        if "aaaUser" in self.url:
            with open('Users/Markdown/Users.md', 'w' ) as f:
                f.write(markdown_output)

        if "aaaDomain" in self.url:
            with open('Security Domains/Markdown/Security Domains.md', 'w' ) as f:
                f.write(markdown_output)

        if "vzSubj" in self.url:
            with open('Contract Subjects/Markdown/Contract Subjects.md', 'w' ) as f:
                f.write(markdown_output)

        if "health" in self.url:
            with open('Health/Markdown/Health.md', 'w' ) as f:
                f.write(markdown_output)

        if "pkiFabricNodeSSLCertificate" in self.url:
            with open('Fabric Node SSL Certificates/Markdown/Fabric Node SSL Certificates.md', 'w' ) as f:
                f.write(markdown_output)

        if "tn-" and "health" in self.url:
            with open('Tenant Health/Markdown/Tenant Health.md', 'w' ) as f:
                f.write(markdown_output)

        if "firmwareCtrlrRunning" in self.url:
            with open('Fabric Membership/Markdown/Fabric Membership.md', 'w' ) as f:
                f.write(markdown_output)

        if "infraWiNode" in self.url:
            with open('Cluster Health/Markdown/Cluster Health.md', 'w' ) as f:
                f.write(markdown_output)

        if "vnsMDev" in self.url:
            with open('Device Packages/Markdown/Device Packages.md', 'w' ) as f:
                f.write(markdown_output)

        if "cnwAggrIf" in self.url:
            with open('Cluster Aggregate Interfaces/Markdown/Cluster Aggregate Interfaces.md', 'w' ) as f:
                f.write(markdown_output)

        if "l3Inst" in self.url:
            with open('L3 Interfaces/Markdown/L3 Interfaces.md', 'w' ) as f:
                f.write(markdown_output)

        if "actrlEntity" in self.url:
            with open('Access Control Entities/Markdown/Access Control Entities.md', 'w' ) as f:
                f.write(markdown_output)

        if "actrlInst" in self.url:
            with open('Access Control Instances/Markdown/Access Control Instances.md', 'w' ) as f:
                f.write(markdown_output)

        if "actrlRule" in self.url:
            with open('Access Control Rules/Markdown/Access Control Rules.md', 'w' ) as f:
                f.write(markdown_output)

        if "actrlScope" in self.url:
            with open('Access Control Scopes/Markdown/Access Control Scopes.md', 'w' ) as f:
                f.write(markdown_output)

        if "cnwPhysIf" in self.url:
            with open('Cluster Physical Interfaces/Markdown/Cluster Physical Interfaces.md', 'w' ) as f:
                f.write(markdown_output)

        if "compCtrlr" in self.url:
            with open('Compute Controllers/Markdown/Compute Controllers.md', 'w' ) as f:
                f.write(markdown_output)

        if "compDom" in self.url:
            with open('Compute Domains/Markdown/Compute Domains.md', 'w' ) as f:
                f.write(markdown_output)

        if "compEpPD" in self.url:
            with open('Compute Endpoint Policy Descriptions/Markdown/Compute Endpoint Policy Descriptions.md', 'w' ) as f:
                f.write(markdown_output)

        if "compProv" in self.url:
            with open('Compute Providers/Markdown/Compute Providers.md', 'w' ) as f:
                f.write(markdown_output)

        if "arpAdjEp" in self.url:
            with open('ARP Adjacency Endpoints/Markdown/ARP Adjacency Endpoints.md', 'w' ) as f:
                f.write(markdown_output)

        if "arpDb" in self.url:
            with open('ARP Database/Markdown/ARP Database.md', 'w' ) as f:
                f.write(markdown_output)

        if "arpDom" in self.url:
            with open('ARP Domain/Markdown/ARP Domain.md', 'w' ) as f:
                f.write(markdown_output)

        if "arpEntity" in self.url:
            with open('ARP Entity/Markdown/ARP Entity.md', 'w' ) as f:
                f.write(markdown_output)

        if "arpIf" in self.url:
            with open('ARP Interfaces/Markdown/ARP Interfaces.md', 'w' ) as f:
                f.write(markdown_output)

        if "arpInst" in self.url:
            with open('ARP Instances/Markdown/ARP Instances.md', 'w' ) as f:
                f.write(markdown_output)

        if "bgpDom" in self.url:
            if "Af" in self.url:
                with open('BGP Domain Address Families/Markdown/BGP Domain Address Families.md', 'w' ) as f:
                    f.write(markdown_output)
            else:
                with open('BGP Domains/Markdown/BGP Domains.md', 'w' ) as f:
                    f.write(markdown_output)

        if "bgpEntity" in self.url:
            with open('BGP Entities/Markdown/BGP Entities.md', 'w' ) as f:
                f.write(markdown_output)

        if "bgpInst" in self.url:
            if "InstPol" in self.url:
                with open('BGP Instances Policy/Markdown/BGP Instances Policy.md', 'w' ) as f:
                    f.write(markdown_output)
            else:
                with open('BGP Instances/Markdown/BGP Instances.md', 'w' ) as f:
                    f.write(markdown_output)

        if "bgpPeer" in self.url:
            if "bgpPeerAf" in self.url:
                with open('BGP Peers AF Entries/Markdown/BGP Peers AF Entries.md', 'w' ) as f:
                    f.write(markdown_output)
            elif "bgpPeerEntry" in self.url:
                with open('BGP Peers Entries/Markdown/BGP Peers Entries.md', 'w' ) as f:
                    f.write(markdown_output)
            else:
                with open('BGP Peers/Markdown/BGP Peers.md', 'w' ) as f:
                    f.write(markdown_output)

        if "bgpRRP" in self.url:
            with open('BGP Route Reflector Policies/Markdown/BGP Route Reflector Policies.md', 'w' ) as f:
                f.write(markdown_output)

        if "cdpAdjEp" in self.url:
            with open('CDP Adjacency Endpoints/Markdown/CDP Adjacency Endpoints.md', 'w' ) as f:
                f.write(markdown_output)

        if "cdpEntity" in self.url:
            with open('CDP Entities/Markdown/CDP Entities.md', 'w' ) as f:
                f.write(markdown_output)

        if "cdpIf" in self.url:
            with open('CDP Interfaces/Markdown/CDP Interfaces.md', 'w' ) as f:
                f.write(markdown_output)

        if "cdpInst" in self.url:
            with open('CDP Instances/Markdown/CDP Instances.md', 'w' ) as f:
                f.write(markdown_output)

        if "cdpIntfAddr" in self.url:
            with open('CDP Interface Addresses/Markdown/CDP Interface Addresses.md', 'w' ) as f:
                f.write(markdown_output)

        if "cdpMgmtAddr" in self.url:
            with open('CDP Management Addresses/Markdown/CDP Management Addresses.md', 'w' ) as f:
                f.write(markdown_output)

        if "cnwRsMbrIfs" in self.url:
            with open('Cluster RS Member Interfaces/Markdown/Cluster RS Member Interfaces.md', 'w' ) as f:
                f.write(markdown_output)

        if "compRsDomP" in self.url:
            with open('Compute RS Domain Policies/Markdown/Compute RS Domain Policies.md', 'w' ) as f:
                f.write(markdown_output)

        if "eqptBSlot" in self.url:
            with open('Equipment Board Slots/Markdown/Equipment Board Slots.md', 'w' ) as f:
                f.write(markdown_output)

        if "eqptBoard" in self.url:
            with open('Equipment Boards/Markdown/Equipment Boards.md', 'w' ) as f:
                f.write(markdown_output)

        if "eqptCPU" in self.url:
            with open('Equipment CPUs/Markdown/Equipment CPUs.md', 'w' ) as f:
                f.write(markdown_output)

        if "eqptCh" in self.url:
            with open('Equipment Chassis/Markdown/Equipment Chassis.md', 'w' ) as f:
                f.write(markdown_output)

        if "eqptDimm" in self.url:
            with open('Equipment DIMMs/Markdown/Equipment DIMMs.md', 'w' ) as f:
                f.write(markdown_output)

        if "eqptExtCh" in self.url:
            with open('Equipment Fabric Extenders/Markdown/Equipment Fabric Extenders.md', 'w' ) as f:
                f.write(markdown_output)

        if "eqptFabP" in self.url:
            with open('Equipment Fabric Ports/Markdown/Equipment Fabric Ports.md', 'w' ) as f:
                f.write(markdown_output)

        if "eqptFan" in self.url:
            with open('Equipment Fans/Markdown/Equipment Fans.md', 'w' ) as f:
                f.write(markdown_output)

        if "eqptFpga" in self.url:
            with open('Equipment Field Programmable Gate Arrays/Markdown/Equipment Field Programmable Gate Arrays.md', 'w' ) as f:
                f.write(markdown_output)

        if "eqptFt" in self.url:
            if "Slot" in self.url:
                with open('Equipment Fan Tray Slots/Markdown/Equipment Fan Tray Slots.md', 'w' ) as f:
                    f.write(markdown_output)
            else:
                with open('Equipment Fan Trays/Markdown/Equipment Fan Trays.md', 'w' ) as f:
                    f.write(markdown_output)

        if "eqptIndLed" in self.url:
            with open('Equipment Indicator LEDs/Markdown/Equipment Indicator LEDs.md', 'w' ) as f:
                f.write(markdown_output)

        if "eqptLC" in self.url:
            if "Slot" in self.url:
                with open('Equipment Line Card Slots/Markdown/Equipment Line Card Slots.md', 'w' ) as f:
                    f.write(markdown_output)
            else:
                with open('Equipment Line Cards/Markdown/Equipment Line Cards.md', 'w' ) as f:
                    f.write(markdown_output)

        if "eqptLeafP" in self.url:
            with open('Equipment Leaf Ports/Markdown/Equipment Leaf Ports.md', 'w' ) as f:
                f.write(markdown_output)

        if "eqptLocLed" in self.url:
            with open('Equipment Port Locator LEDs/Markdown/Equipment Port Locator LEDs.md', 'w' ) as f:
                f.write(markdown_output)

        if "eqptPsu" in self.url:
            if "Slot" in self.url:
                with open('Equipment Power Supply Slots/Markdown/Equipment Power Supply Slots.md', 'w' ) as f:
                    f.write(markdown_output)
            else:
                with open('Equipment Power Supplies/Markdown/Equipment Power Supplies.md', 'w' ) as f:
                    f.write(markdown_output)

        if "eqptRsIoPPhysConf" in self.url:
            with open('Equipment RS IO Port Physical Configs/Markdown/Equipment RS IO Port Physical Configs.md', 'w' ) as f:
                f.write(markdown_output)

        if "eqptSensor" in self.url:
            with open('Equipment Sensors/Markdown/Equipment Sensors.md', 'w' ) as f:
                f.write(markdown_output)

        if "eqptSpCmnBlk" in self.url:
            with open('Equipment SP Common Blocks/Markdown/Equipment SP Common Blocks.md', 'w' ) as f:
                f.write(markdown_output)

        if "eqptSpromLc" in self.url:
            with open('Equipment SPROM LCs/Markdown/Equipment SPROM LCs.md', 'w' ) as f:
                f.write(markdown_output)

    def html_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        html_template = env.get_template('aci_html.j2')
        html_output = html_template.render(api = self.url,
                                         data_to_template = json.loads(parsed_json),
                                         url = self.aci)
        if "Tenant" in self.url:
            with open('Tenant/HTML/Tenants.html', 'w' ) as f:
                f.write(html_output)

        if "AEPg" in self.url:
            with open('EPG/HTML/EPGs.html', 'w' ) as f:
                f.write(html_output)

        if "BD" in self.url:
            with open('Bridge Domains/HTML/Bridge Domains.html', 'w' ) as f:
                f.write(html_output)

        if "Ctx" in self.url:
            with open('Contexts/HTML/Contexts.html', 'w' ) as f:
                f.write(html_output)

        if "Ap" in self.url:
            with open('Application Profiles/HTML/Application Profiles.html', 'w' ) as f:
                f.write(html_output)

        if "l3extOut" in self.url:
            with open('L3Outs/HTML/L3Outs.html', 'w' ) as f:
                f.write(html_output)

        if "l2extOut" in self.url:
            with open('L2Outs/HTML/L2Outs.html', 'w' ) as f:
                f.write(html_output)

        if "topSystem" in self.url:
            if "?" not in self.url:
                with open('Top System/HTML/Top System.html', 'w' ) as f:
                    f.write(html_output)

        if "Subnet" in self.url:
            with open('Subnets/HTML/Subnets.html', 'w' ) as f:
                f.write(html_output)

        if "CEp" in self.url:
            with open('Endpoints/HTML/Endpoints.html', 'w' ) as f:
                f.write(html_output)

        if "fabricNode" in self.url:
            with open('Fabric Nodes/HTML/Fabric Nodes.html', 'w' ) as f:
                f.write(html_output)

        if "l1PhysIf" in self.url:
            with open('Physical Interfaces/HTML/Physical Interfaces.html', 'w' ) as f:
                f.write(html_output)

        if "infraAccPortP" in self.url:
            with open('Leaf Interface Profiles/HTML/Leaf Interface Profiles.html', 'w' ) as f:
                f.write(html_output)

        if "infraSpAccPortP" in self.url:
            with open('Spine Interface Profiles/HTML/Spine Interface Profiles.html', 'w' ) as f:
                f.write(html_output)

        if "infraNodeP" in self.url:
            with open('Leaf Switch Profiles/HTML/Leaf Switch Profiles.html', 'w' ) as f:
                f.write(html_output)

        if "infraSpineP" in self.url:
            with open('Spine Switch Profiles/HTML/Spine Switch Profiles.html', 'w' ) as f:
                f.write(html_output)

        if "fvnsVlanInstP" in self.url:
            with open('VLAN Pools/HTML/VLAN Pools.html', 'w' ) as f:
                f.write(html_output)

        if "infraAttEntityP" in self.url:
            with open('Attachable Access Entity Profiles/HTML/Attachable Access Entity Profiles.html', 'w' ) as f:
                f.write(html_output)

        if "vzBrCP" in self.url:
            with open('Contracts/HTML/Contracts.html', 'w' ) as f:
                f.write(html_output)

        if "vzEntry" in self.url:
            with open('Filters/HTML/Filters.html', 'w' ) as f:
                f.write(html_output)

        if "physDomP" in self.url:
            with open('Physical Domains/HTML/Physical Domains.html', 'w' ) as f:
                f.write(html_output)

        if "l3extDomP" in self.url:
            with open('L3 Domains/HTML/L3 Domains.html', 'w' ) as f:
                f.write(html_output)

        if "qosClass" in self.url:
            with open('QOS Classes/HTML/QOS Classes.html', 'w' ) as f:
                f.write(html_output)

        if "faultSummary" in self.url:
            with open('Fault Summary/HTML/Fault Summary.html', 'w' ) as f:
                f.write(html_output)

        if "aaaModLR" in self.url:
            with open('Audit Log/HTML/Audit Log.html', 'w' ) as f:
                f.write(html_output)

        if "fvIp" in self.url:
            with open('IP Addresses/HTML/IP Addresses.html', 'w' ) as f:
                f.write(html_output)

        if "eventRecord" in self.url:
            with open('Events/HTML/Events.html', 'w' ) as f:
                f.write(html_output)

        if "licenseEntitlement" in self.url:
            with open('License Entitlements/HTML/License Entitlements.html', 'w' ) as f:
                f.write(html_output)

        if "bgpRRNodePEp" in self.url:
            with open('BGP Route Reflectors/HTML/BGP Route Reflectors.html', 'w' ) as f:
                f.write(html_output)

        if "infraPortS" in self.url:
            with open('Interface Policies/HTML/Interface Policies.html', 'w' ) as f:
                f.write(html_output)

        if "infraProfile" in self.url:
            with open('Interface Profiles/HTML/Interface Profiles.html', 'w' ) as f:
                f.write(html_output)

        if "fabricPod" in self.url:
            with open('Fabric Pods/HTML/Fabric Pods.html', 'w' ) as f:
                f.write(html_output)

        if "fabricPath" in self.url:
            with open('Fabric Paths/HTML/Fabric Paths.html', 'w' ) as f:
                f.write(html_output)

        if "rtctrlSubjP" in self.url:
            with open('Prefix List/HTML/Prefix List.html', 'w' ) as f:
                f.write(html_output)

        if "rtctrlMatchRtDest" in self.url:
            with open('Prefix List Detailed/HTML/Prefix List Detailed.html', 'w' ) as f:
                f.write(html_output)

        if "aaaUser" in self.url:
            with open('Users/HTML/Users.html', 'w' ) as f:
                f.write(html_output)

        if "aaaDomain" in self.url:
            with open('Security Domains/HTML/Security Domains.html', 'w' ) as f:
                f.write(html_output)

        if "vzSubj" in self.url:
            with open('Contract Subjects/HTML/Contract Subjects.html', 'w' ) as f:
                f.write(html_output)

        if "health" in self.url:
            with open('Health/HTML/Health.html', 'w' ) as f:
                f.write(html_output)

        if "pkiFabricNodeSSLCertificate" in self.url:
            with open('Fabric Node SSL Certificates/HTML/Fabric Node SSL Certificates.html', 'w' ) as f:
                f.write(html_output)

        if "tn-" and "health" in self.url:
            with open('Tenant Health/HTML/Tenant Health.html', 'w' ) as f:
                f.write(html_output)

        if "firmwareCtrlrRunning" in self.url:
            with open('Fabric Membership/HTML/Fabric Membership.html', 'w' ) as f:
                f.write(html_output)

        if "infraWiNode" in self.url:
            with open('Cluster Health/HTML/Cluster Health.html', 'w' ) as f:
                f.write(html_output)

        if "vnsMDev" in self.url:
            with open('Device Packages/HTML/Device Packages.html', 'w' ) as f:
                f.write(html_output)

        if "cnwAggrIf" in self.url:
            with open('Cluster Aggregate Interfaces/HTML/Cluster Aggregate Interfaces.html', 'w' ) as f:
                f.write(html_output)

        if "l3Inst" in self.url:
            with open('L3 Interfaces/HTML/L3 Interfaces.html', 'w' ) as f:
                f.write(html_output)

        if "actrlEntity" in self.url:
            with open('Access Control Entities/HTML/Access Control Entities.html', 'w' ) as f:
                f.write(html_output)

        if "actrlInst" in self.url:
            with open('Access Control Instances/HTML/Access Control Instances.html', 'w' ) as f:
                f.write(html_output)

        if "actrlRule" in self.url:
            with open('Access Control Rules/HTML/Access Control Rules.html', 'w' ) as f:
                f.write(html_output)

        if "actrlScope" in self.url:
            with open('Access Control Scopes/HTML/Access Control Scopes.html', 'w' ) as f:
                f.write(html_output)

        if "cnwPhysIf" in self.url:
            with open('Cluster Physical Interfaces/HTML/Cluster Physical Interfaces.html', 'w' ) as f:
                f.write(html_output)

        if "compCtrlr" in self.url:
            with open('Compute Controllers/HTML/Compute Controllers.html', 'w' ) as f:
                f.write(html_output)

        if "compDom" in self.url:
            with open('Compute Domains/HTML/Compute Domains.html', 'w' ) as f:
                f.write(html_output)

        if "compEpPD" in self.url:
            with open('Compute Endpoint Policy Descriptions/HTML/Compute Endpoint Policy Descriptions.html', 'w' ) as f:
                f.write(html_output)

        if "compProv" in self.url:
            with open('Compute Providers/HTML/Compute Providers.html', 'w' ) as f:
                f.write(html_output)

        if "arpAdjEp" in self.url:
            with open('ARP Adjacency Endpoints/HTML/ARP Adjacency Endpoints.html', 'w' ) as f:
                f.write(html_output)

        if "arpDb" in self.url:
            with open('ARP Database/HTML/ARP Database.html', 'w' ) as f:
                f.write(html_output)

        if "arpDom" in self.url:
            with open('ARP Domain/HTML/ARP Domain.html', 'w' ) as f:
                f.write(html_output)

        if "arpEntity" in self.url:
            with open('ARP Entity/HTML/ARP Entity.html', 'w' ) as f:
                f.write(html_output)

        if "arpIf" in self.url:
            with open('ARP Interfaces/HTML/ARP Interfaces.html', 'w' ) as f:
                f.write(html_output)

        if "arpInst" in self.url:
            with open('ARP Instances/HTML/ARP Instances.html', 'w' ) as f:
                f.write(html_output)

        if "bgpDom" in self.url:
            if "Af" in self.url:
                with open('BGP Domain Address Families/HTML/BGP Domain Address Families.html', 'w' ) as f:
                    f.write(html_output)
            else:
                with open('BGP Domains/HTML/BGP Domains.html', 'w' ) as f:
                    f.write(html_output)

        if "bgpEntity" in self.url:
            with open('BGP Entities/HTML/BGP Entities.html', 'w' ) as f:
                f.write(html_output)

        if "bgpInst" in self.url:
            if "InstPol" in self.url:
                with open('BGP Instances Policy/HTML/BGP Instances Policy.html', 'w' ) as f:
                    f.write(html_output)
            else:
                with open('BGP Instances/HTML/BGP Instances.html', 'w' ) as f:
                    f.write(html_output)

        if "bgpPeer" in self.url:
            if "bgpPeerAf" in self.url:
                with open('BGP Peers AF Entries/HTML/BGP Peers AF Entries.html', 'w' ) as f:
                    f.write(html_output)
            elif "bgpPeerEntry" in self.url:
                with open('BGP Peers Entries/HTML/BGP Peers Entries.html', 'w' ) as f:
                    f.write(html_output)
            else:
                with open('BGP Peers/HTML/BGP Peers.html', 'w' ) as f:
                    f.write(html_output)

        if "bgpRRP" in self.url:
            with open('BGP Route Reflector Policies/HTML/BGP Route Reflector Policies.html', 'w' ) as f:
                f.write(html_output)

        if "cdpAdjEp" in self.url:
            with open('CDP Adjacency Endpoints/HTML/CDP Adjacency Endpoints.html', 'w' ) as f:
                f.write(html_output)

        if "cdpEntity" in self.url:
            with open('CDP Entities/HTML/CDP Entities.html', 'w' ) as f:
                f.write(html_output)

        if "cdpIf" in self.url:
            with open('CDP Interfaces/HTML/CDP Interfaces.html', 'w' ) as f:
                f.write(html_output)

        if "cdpInst" in self.url:
            with open('CDP Instances/HTML/CDP Instances.html', 'w' ) as f:
                f.write(html_output)

        if "cdpIntfAddr" in self.url:
            with open('CDP Interface Addresses/HTML/CDP Interface Addresses.html', 'w' ) as f:
                f.write(html_output)

        if "cdpMgmtAddr" in self.url:
            with open('CDP Management Addresses/HTML/CDP Management Addresses.html', 'w' ) as f:
                f.write(html_output)

        if "cnwRsMbrIfs" in self.url:
            with open('Cluster RS Member Interfaces/HTML/Cluster RS Member Interfaces.html', 'w' ) as f:
                f.write(html_output)

        if "compRsDomP" in self.url:
            with open('Compute RS Domain Policies/HTML/Compute RS Domain Policies.html', 'w' ) as f:
                f.write(html_output)

        if "eqptBSlot" in self.url:
            with open('Equipment Board Slots/HTML/Equipment Board Slots.html', 'w' ) as f:
                f.write(html_output)

        if "eqptBoard" in self.url:
            with open('Equipment Boards/HTML/Equipment Boards.html', 'w' ) as f:
                f.write(html_output)

        if "eqptCPU" in self.url:
            with open('Equipment CPUs/HTML/Equipment CPUs.html', 'w' ) as f:
                f.write(html_output)

        if "eqptCh" in self.url:
            with open('Equipment Chassis/HTML/Equipment Chassis.html', 'w' ) as f:
                f.write(html_output)

        if "eqptDimm" in self.url:
            with open('Equipment DIMMs/HTML/Equipment DIMMs.html', 'w' ) as f:
                f.write(html_output)

        if "eqptExtCh" in self.url:
            with open('Equipment Fabric Extenders/HTML/Equipment Fabric Extenders.html', 'w' ) as f:
                f.write(html_output)

        if "eqptFabP" in self.url:
            with open('Equipment Fabric Ports/HTML/Equipment Fabric Ports.html', 'w' ) as f:
                f.write(html_output)

        if "eqptFan" in self.url:
            with open('Equipment Fans/HTML/Equipment Fans.html', 'w' ) as f:
                f.write(html_output)

        if "eqptFpga" in self.url:
            with open('Equipment Field Programmable Gate Arrays/HTML/Equipment Field Programmable Gate Arrays.html', 'w' ) as f:
                f.write(html_output)

        if "eqptFt" in self.url:
            if "Slot" in self.url:
                with open('Equipment Fan Tray Slots/HTML/Equipment Fan Tray Slots.html', 'w' ) as f:
                    f.write(html_output)
            else:
                with open('Equipment Fan Trays/HTML/Equipment Fan Trays.html', 'w' ) as f:
                    f.write(html_output)

        if "eqptIndLed" in self.url:
            with open('Equipment Indicator LEDs/HTML/Equipment Indicator LEDs.html', 'w' ) as f:
                f.write(html_output)

        if "eqptLC" in self.url:
            if "Slot" in self.url:
                with open('Equipment Line Card Slots/HTML/Equipment Line Card Slots.html', 'w' ) as f:
                    f.write(html_output)
            else:
                with open('Equipment Line Cards/HTML/Equipment Line Cards.html', 'w' ) as f:
                    f.write(html_output)

        if "eqptLeafP" in self.url:
            with open('Equipment Leaf Ports/HTML/Equipment Leaf Ports.html', 'w' ) as f:
                f.write(html_output)

        if "eqptLocLed" in self.url:
            with open('Equipment Port Locator LEDs/HTML/Equipment Port Locator LEDs.html', 'w' ) as f:
                f.write(html_output)

        if "eqptPsu" in self.url:
            if "Slot" in self.url:
                with open('Equipment Power Supply Slots/HTML/Equipment Power Supply Slots.html', 'w' ) as f:
                    f.write(html_output)
            else:            
                with open('Equipment Power Supplies/HTML/Equipment Power Supplies.html', 'w' ) as f:
                    f.write(html_output)

        if "eqptRsIoPPhysConf" in self.url:
            with open('Equipment RS IO Port Physical Configs/HTML/Equipment RS IO Port Physical Configs.html', 'w' ) as f:
                f.write(html_output)

        if "eqptSensor" in self.url:
            with open('Equipment Sensors/HTML/Equipment Sensors.html', 'w' ) as f:
                f.write(html_output)

        if "eqptSpCmnBlk" in self.url:
            with open('Equipment SP Common Blocks/HTML/Equipment SP Common Blocks.html', 'w' ) as f:
                f.write(html_output)

        if "eqptSpromLc" in self.url:
            with open('Equipment SPROM LCs/HTML/Equipment SPROM LCs.html', 'w' ) as f:
                f.write(html_output)

    def mindmap_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        mindmap_template = env.get_template('aci_mindmap.j2')
        mindmap_output = mindmap_template.render(api = self.url,
                                         data_to_template = json.loads(parsed_json),
                                         url = self.aci)
        if "Tenant" in self.url:
            with open('Tenant/Mindmap/Tenants.md', 'w' ) as f:
                f.write(mindmap_output)

        if "AEPg" in self.url:
            with open('EPG/Mindmap/EPGs.md', 'w' ) as f:
                f.write(mindmap_output)

        if "BD" in self.url:
            with open('Bridge Domains/Mindmap/Bridge Domains.md', 'w' ) as f:
                f.write(mindmap_output)

        if "Ctx" in self.url:
            with open('Contexts/Mindmap/Contexts.md', 'w' ) as f:
                f.write(mindmap_output)

        if "Ap" in self.url:
            with open('Application Profiles/Mindmap/Application Profiles.md', 'w' ) as f:
                f.write(mindmap_output)

        if "l3extOut" in self.url:
            with open('L3Outs/Mindmap/L3Outs.md', 'w' ) as f:
                f.write(mindmap_output)

        if "l2extOut" in self.url:
            with open('L2Outs/Mindmap/L2Outs.md', 'w' ) as f:
                f.write(mindmap_output)

        if "topSystem" in self.url:
            if "?" not in self.url:
                with open('Top System/Mindmap/Top System.md', 'w' ) as f:
                    f.write(mindmap_output)

        if "Subnet" in self.url:
            with open('Subnets/Mindmap/Subnets.md', 'w' ) as f:
                f.write(mindmap_output)

        if "CEp" in self.url:
            with open('Endpoints/Mindmap/Endpoints.md', 'w' ) as f:
                f.write(mindmap_output)

        if "fabricNode" in self.url:
            with open('Fabric Nodes/Mindmap/Fabric Nodes.md', 'w' ) as f:
                f.write(mindmap_output)

        if "l1PhysIf" in self.url:
            with open('Physical Interfaces/Mindmap/Physical Interfaces.md', 'w' ) as f:
                f.write(mindmap_output)

        if "infraAccPortP" in self.url:
            with open('Leaf Interface Profiles/Mindmap/Leaf Interface Profiles.md', 'w' ) as f:
                f.write(mindmap_output)

        if "infraSpAccPortP" in self.url:
            with open('Spine Interface Profiles/Mindmap/Spine Interface Profiles.md', 'w' ) as f:
                f.write(mindmap_output)

        if "infraNodeP" in self.url:
            with open('Leaf Switch Profiles/Mindmap/Leaf Switch Profiles.md', 'w' ) as f:
                f.write(mindmap_output)

        if "infraSpineP" in self.url:
            with open('Spine Switch Profiles/Mindmap/Spine Switch Profiles.md', 'w' ) as f:
                f.write(mindmap_output)

        if "fvnsVlanInstP" in self.url:
            with open('VLAN Pools/Mindmap/VLAN Pools.md', 'w' ) as f:
                f.write(mindmap_output)

        if "infraAttEntityP" in self.url:
            with open('Attachable Access Entity Profiles/Mindmap/Attachable Access Entity Profiles.md', 'w' ) as f:
                f.write(mindmap_output)

        if "vzBrCP" in self.url:
            with open('Contracts/Mindmap/Contracts.md', 'w' ) as f:
                f.write(mindmap_output)

        if "vzEntry" in self.url:
            with open('Filters/Mindmap/Filters.md', 'w' ) as f:
                f.write(mindmap_output)

        if "physDomP" in self.url:
            with open('Physical Domains/Mindmap/Physical Domains.md', 'w' ) as f:
                f.write(mindmap_output)

        if "l3extDomP" in self.url:
            with open('L3 Domains/Mindmap/L3 Domains.md', 'w' ) as f:
                f.write(mindmap_output)

        if "qosClass" in self.url:
            with open('QOS Classes/Mindmap/QOS Classes.md', 'w' ) as f:
                f.write(mindmap_output)

        if "faultSummary" in self.url:
            with open('Fault Summary/Mindmap/Fault Summary.md', 'w' ) as f:
                f.write(mindmap_output)

        if "aaaModLR" in self.url:
            with open('Audit Log/Mindmap/Audit Log.md', 'w' ) as f:
                f.write(mindmap_output)

        if "fvIp" in self.url:
            with open('IP Addresses/Mindmap/IP Addresses.md', 'w' ) as f:
                f.write(mindmap_output)

        if "eventRecord" in self.url:
            with open('Events/Mindmap/Events.md', 'w' ) as f:
                f.write(mindmap_output)

        if "licenseEntitlement" in self.url:
            with open('License Entitlements/Mindmap/License Entitlements.md', 'w' ) as f:
                f.write(mindmap_output)

        if "bgpRRNodePEp" in self.url:
            with open('BGP Route Reflectors/Mindmap/BGP Route Reflectors.md', 'w' ) as f:
                f.write(mindmap_output)

        if "infraPortS" in self.url:
            with open('Interface Policies/Mindmap/Interface Policies.md', 'w' ) as f:
                f.write(mindmap_output)

        if "infraProfile" in self.url:
            with open('Interface Profiles/Mindmap/Interface Profiles.md', 'w' ) as f:
                f.write(mindmap_output)

        if "fabricPod" in self.url:
            with open('Fabric Pods/Mindmap/Fabric Pods.md', 'w' ) as f:
                f.write(mindmap_output)

        if "fabricPath" in self.url:
            with open('Fabric Paths/Mindmap/Fabric Paths.md', 'w' ) as f:
                f.write(mindmap_output)

        if "rtctrlSubjP" in self.url:
            with open('Prefix List/Mindmap/Prefix List.md', 'w' ) as f:
                f.write(mindmap_output)

        if "rtctrlMatchRtDest" in self.url:
            with open('Prefix List Detailed/Mindmap/Prefix List Detailed.md', 'w' ) as f:
                f.write(mindmap_output)

        if "aaaUser" in self.url:
            with open('Users/Mindmap/Users.md', 'w' ) as f:
                f.write(mindmap_output)

        if "aaaDomain" in self.url:
            with open('Security Domains/Mindmap/Security Domains.md', 'w' ) as f:
                f.write(mindmap_output)

        if "vzSubj" in self.url:
            with open('Contract Subjects/Mindmap/Contract Subjects.md', 'w' ) as f:
                f.write(mindmap_output)

        if "health" in self.url:
            with open('Health/Mindmap/Health.md', 'w' ) as f:
                f.write(mindmap_output)

        if "pkiFabricNodeSSLCertificate" in self.url:
            with open('Fabric Node SSL Certificates/Mindmap/Fabric Node SSL Certificates.md', 'w' ) as f:
                f.write(mindmap_output)

        if "tn-" and "health" in self.url:
            with open('Tenant Health/Mindmap/Tenant Health.md', 'w' ) as f:
                f.write(mindmap_output)

        if "firmwareCtrlrRunning" in self.url:
            with open('Fabric Membership/Mindmap/Fabric Membership.md', 'w' ) as f:
                f.write(mindmap_output)

        if "infraWiNode" in self.url:
            with open('Cluster Health/Mindmap/Cluster Health.md', 'w' ) as f:
                f.write(mindmap_output)

        if "vnsMDev" in self.url:
            with open('Device Packages/Mindmap/Device Packages.md', 'w' ) as f:
                f.write(mindmap_output)

        if "cnwAggrIf" in self.url:
            with open('Cluster Aggregate Interfaces/Mindmap/Cluster Aggregate Interfaces.md', 'w' ) as f:
                f.write(mindmap_output)

        if "l3Inst" in self.url:
            with open('L3 Interfaces/Mindmap/L3 Interfaces.md', 'w' ) as f:
                f.write(mindmap_output)

        if "actrlEntity" in self.url:
            with open('Access Control Entities/Mindmap/Access Control Entities.md', 'w' ) as f:
                f.write(mindmap_output)

        if "actrlInst" in self.url:
            with open('Access Control Instances/Mindmap/Access Control Instances.md', 'w' ) as f:
                f.write(mindmap_output)

        if "actrlRule" in self.url:
            with open('Access Control Rules/Mindmap/Access Control Rules.md', 'w' ) as f:
                f.write(mindmap_output)

        if "actrlScope" in self.url:
            with open('Access Control Scopes/Mindmap/Access Control Scopes.md', 'w' ) as f:
                f.write(mindmap_output)

        if "cnwPhysIf" in self.url:
            with open('Cluster Physical Interfaces/Mindmap/Cluster Physical Interfaces.md', 'w' ) as f:
                f.write(mindmap_output)

        if "compCtrlr" in self.url:
            with open('Compute Controllers/Mindmap/Compute Controllers.md', 'w' ) as f:
                f.write(mindmap_output)

        if "compDom" in self.url:
            with open('Compute Domains/Mindmap/Compute Domains.md', 'w' ) as f:
                f.write(mindmap_output)

        if "compEpPD" in self.url:
            with open('Compute Endpoint Policy Descriptions/Mindmap/Compute Endpoint Policy Descriptions.md', 'w' ) as f:
                f.write(mindmap_output)

        if "compProv" in self.url:
            with open('Compute Providers/Mindmap/Compute Providers.md', 'w' ) as f:
                f.write(mindmap_output)

        if "arpAdjEp" in self.url:
            with open('ARP Adjacency Endpoints/Mindmap/ARP Adjacency Endpoints.md', 'w' ) as f:
                f.write(mindmap_output)

        if "arpDb" in self.url:
            with open('ARP Database/Mindmap/ARP Database.md', 'w' ) as f:
                f.write(mindmap_output)

        if "arpDom" in self.url:
            with open('ARP Domain/Mindmap/ARP Domain.md', 'w' ) as f:
                f.write(mindmap_output)

        if "arpEntity" in self.url:
            with open('ARP Entity/Mindmap/ARP Entity.md', 'w' ) as f:
                f.write(mindmap_output)

        if "arpIf" in self.url:
            with open('ARP Interfaces/Mindmap/ARP Interfaces.md', 'w' ) as f:
                f.write(mindmap_output)

        if "arpInst" in self.url:
            with open('ARP Instances/Mindmap/ARP Instances.md', 'w' ) as f:
                f.write(mindmap_output)

        if "bgpDom" in self.url:
            if "bgpDomAf" in self.url:
                with open('BGP Domain Address Families/Mindmap/BGP Domain Address Families.md', 'w' ) as f:
                    f.write(mindmap_output)
            else:
                with open('BGP Domains/Mindmap/BGP Domains.md', 'w' ) as f:
                    f.write(mindmap_output)

        if "bgpEntity" in self.url:
            with open('BGP Entities/Mindmap/BGP Entities.md', 'w' ) as f:
                f.write(mindmap_output)

        if "bgpInst" in self.url:
            if "InstPol" in self.url:
                with open('BGP Instances Policy/Mindmap/BGP Instances Policy.md', 'w' ) as f:
                    f.write(mindmap_output)
            else:
                with open('BGP Instances/Mindmap/BGP Instances.md', 'w' ) as f:
                    f.write(mindmap_output)

        if "bgpPeer" in self.url:
            if "bgpPeerAf" in self.url:
                with open('BGP Peers AF Entries/Mindmap/BGP Peers AF Entries.md', 'w' ) as f:
                    f.write(mindmap_output)
            elif "bgpPeerEntry" in self.url:
                with open('BGP Peers Entries/Mindmap/BGP Peers Entries.md', 'w' ) as f:
                    f.write(mindmap_output)
            else:
                with open('BGP Peers/Mindmap/BGP Peers.md', 'w' ) as f:
                    f.write(mindmap_output)

        if "bgpRRP" in self.url:
            with open('BGP Route Reflector Policies/Mindmap/BGP Route Reflector Policies.md', 'w' ) as f:
                f.write(mindmap_output)

        if "cdpAdjEp" in self.url:
            with open('CDP Adjacency Endpoints/Mindmap/CDP Adjacency Endpoints.md', 'w' ) as f:
                f.write(mindmap_output)

        if "cdpEntity" in self.url:
            with open('CDP Entities/Mindmap/CDP Entities.md', 'w' ) as f:
                f.write(mindmap_output)

        if "cdpIf" in self.url:
            with open('CDP Interfaces/Mindmap/CDP Interfaces.md', 'w' ) as f:
                f.write(mindmap_output)

        if "cdpInst" in self.url:
            with open('CDP Instances/Mindmap/CDP Instances.md', 'w' ) as f:
                f.write(mindmap_output)

        if "cdpIntfAddr" in self.url:
            with open('CDP Interface Addresses/Mindmap/CDP Interface Addresses.md', 'w' ) as f:
                f.write(mindmap_output)

        if "cdpMgmtAddr" in self.url:
            with open('CDP Management Addresses/Mindmap/CDP Management Addresses.md', 'w' ) as f:
                f.write(mindmap_output)

        if "cnwRsMbrIfs" in self.url:
            with open('Cluster RS Member Interfaces/Mindmap/Cluster RS Member Interfaces.md', 'w' ) as f:
                f.write(mindmap_output)

        if "compRsDomP" in self.url:
            with open('Compute RS Domain Policies/Mindmap/Compute RS Domain Policies.md', 'w' ) as f:
                f.write(mindmap_output)

        if "eqptBSlot" in self.url:
            with open('Equipment Board Slots/Mindmap/Equipment Board Slots.md', 'w' ) as f:
                f.write(mindmap_output)

        if "eqptBoard" in self.url:
            with open('Equipment Boards/Mindmap/Equipment Boards.md', 'w' ) as f:
                f.write(mindmap_output)

        if "eqptCPU" in self.url:
            with open('Equipment CPUs/Mindmap/Equipment CPUs.md', 'w' ) as f:
                f.write(mindmap_output)

        if "eqptCh" in self.url:
            with open('Equipment Chassis/Mindmap/Equipment Chassis.md', 'w' ) as f:
                f.write(mindmap_output)

        if "eqptDimm" in self.url:
            with open('Equipment DIMMs/Mindmap/Equipment DIMMs.md', 'w' ) as f:
                f.write(mindmap_output)

        if "eqptExtCh" in self.url:
            with open('Equipment Fabric Extenders/Mindmap/Equipment Fabric Extenders.md', 'w' ) as f:
                f.write(mindmap_output)

        if "eqptFabP" in self.url:
            with open('Equipment Fabric Ports/Mindmap/Equipment Fabric Ports.md', 'w' ) as f:
                f.write(mindmap_output)

        if "eqptFan" in self.url:
            with open('Equipment Fans/Mindmap/Equipment Fans.md', 'w' ) as f:
                f.write(mindmap_output)

        if "eqptFpga" in self.url:
            with open('Equipment Field Programmable Gate Arrays/Mindmap/Equipment Field Programmable Gate Arrays.md', 'w' ) as f:
                f.write(mindmap_output)

        if "eqptFt" in self.url:
            if "Slot" in self.url:
                with open('Equipment Fan Tray Slots/Mindmap/Equipment Fan Tray Slots.md', 'w' ) as f:
                    f.write(mindmap_output)
            else:
                with open('Equipment Fan Trays/Mindmap/Equipment Fan Trays.md', 'w' ) as f:
                    f.write(mindmap_output)

        if "eqptIndLed" in self.url:
            with open('Equipment Indicator LEDs/Mindmap/Equipment Indicator LEDs.md', 'w' ) as f:
                f.write(mindmap_output)

        if "eqptLC" in self.url:
            with open('Equipment Line Cards/Mindmap/Equipment Line Cards.md', 'w' ) as f:
                f.write(mindmap_output)

        if "eqptLeafP" in self.url:
            with open('Equipment Leaf Ports/Mindmap/Equipment Leaf Ports.md', 'w' ) as f:
                f.write(mindmap_output)

        if "eqptLocLed" in self.url:
            with open('Equipment Port Locator LEDs/Mindmap/Equipment Port Locator LEDs.md', 'w' ) as f:
                f.write(mindmap_output)

        if "eqptPsu" in self.url:
            if "Slot" in self.url:
                with open('Equipment Power Supply Slots/Mindmap/Equipment Power Supply Slots.md', 'w' ) as f:
                    f.write(mindmap_output)
            else:
                with open('Equipment Power Supplies/Mindmap/Equipment Power Supplies.md', 'w' ) as f:
                    f.write(mindmap_output)

        if "eqptRsIoPPhysConf" in self.url:
            with open('Equipment RS IO Port Physical Configs/Mindmap/Equipment RS IO Port Physical Configs.md', 'w' ) as f:
                f.write(mindmap_output)

        if "eqptSensor" in self.url:
            with open('Equipment Sensors/Mindmap/Equipment Sensors.md', 'w' ) as f:
                f.write(mindmap_output)

        if "eqptSpCmnBlk" in self.url:
            with open('Equipment SP Common Blocks/Mindmap/Equipment SP Common Blocks.md', 'w' ) as f:
                f.write(mindmap_output)

        if "eqptSpromLc" in self.url:
            with open('Equipment SPROM LCs/Mindmap/Equipment SPROM LCs.md', 'w' ) as f:
                f.write(mindmap_output)

    def all_files(self, parsed_json):
        self.json_file(parsed_json)
        self.yaml_file(parsed_json)
        self.csv_file(parsed_json)
        self.markdown_file(parsed_json)
        self.html_file(parsed_json)
        self.mindmap_file(parsed_json)

@click.command()
@click.option('--url',
    prompt="APIC URL",
    help="APIC URL",
    required=True,envvar="URL")
@click.option('--username',
    prompt="APIC Username",
    help="APIC Username",
    required=True,envvar="USERNAME")
@click.option('--password',
    prompt="APIC Password",
    help="APIC Password",
    required=True, hide_input=True,envvar="PASSWORD")
def cli(url,username,password):
    invoke_class = ACEye(url,username,password)
    invoke_class.aceye()

if __name__ == "__main__":
    cli()
