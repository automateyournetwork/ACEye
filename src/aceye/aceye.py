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
        parsed_json = json.dumps(self.cluster_physical_interfaces(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.compute_controllers(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.compute_domains(), indent=4, sort_keys=True)
        self.all_files(parsed_json)

    def make_directories(self):
        api_list = ['Access Control Entities',
                    'Access Control Instances',
                    'Access Control Rules',
                    'Application Profiles',
                    'Attachable Access Entity Profiles',
                    'Audit Log',
                    'BGP Route Reflectors',
                    'Bridge Domains',
                    'Cluster Aggregate Interfaces',
                    'Cluster Health',
                    'Cluster Physical Interfaces',
                    'Compute Controllers',
                    'Compute Domains',
                    'Contexts',
                    'Contracts',
                    'Contract Subjects',
                    'Device Packages',
                    'Endpoints',
                    'EPG',
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
        return(response_dict)

    def epgs(self):
        self.url = f"{ self.aci }/api/node/class/fvAEPg.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<EPG Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def bridge_domains(self):
        self.url = f"{ self.aci }/api/node/class/fvBD.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Bridge Domains Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def contexts(self):
        self.url = f"{ self.aci }/api/node/class/fvCtx.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Contexts Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)        

    def application_profiles(self):
        self.url = f"{ self.aci }/api/node/class/fvAp.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Application Profiles Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)    
    
    def l3outs(self):
        self.url = f"{ self.aci }/api/node/class/l3extOut.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<L3Outs Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)     

    def l2outs(self):
        self.url = f"{ self.aci }/api/node/class/l2extOut.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<L2Outs Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def topSystem(self):
        self.url = f"{ self.aci }/api/node/class/topSystem.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Top System Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def subnets(self):
        self.url = f"{ self.aci }/api/node/class/fvSubnet.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Subnet Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def endpoints(self):
        self.url = f"{ self.aci }/api/node/class/fvCEp.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Connected Endpoints Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def fabric_nodes(self):
        self.url = f"{ self.aci }/api/node/class/fabricNode.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Fabric Nodes Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

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
        return(physical_interfaces)

    def leaf_interface_profiles(self):
        self.url = f"{ self.aci }/api/node/class/infraAccPortP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Leaf Interface Profiles Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def spine_interface_profiles(self):
        self.url = f"{ self.aci }/api/node/class/infraSpAccPortP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Spine Interface Profiles Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def leaf_switch_profiles(self):
        self.url = f"{ self.aci }/api/node/class/infraNodeP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Leaf Switch Profiles Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def spine_switch_profiles(self):
        self.url = f"{ self.aci }/api/node/class/infraSpineP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Spine Switch Profiles Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def vlan_pools(self):
        self.url = f"{ self.aci }/api/node/class/fvnsVlanInstP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<VLAN Pools Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def attachable_access_entity_profiles(self):
        self.url = f"{ self.aci }/api/node/class/infraAttEntityP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Attachable Access Entity Profiles Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def contracts(self):
        self.url = f"{ self.aci }/api/node/class/vzBrCP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Contracts Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def filters(self):
        self.url = f"{ self.aci }/api/node/class/vzEntry.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Filters Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def physical_domains(self):
        self.url = f"{ self.aci }/api/node/class/physDomP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Physical Domains Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def l3_domains(self):
        self.url = f"{ self.aci }/api/node/class/l3extDomP.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<L3 Domains Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def qos_classes(self):
        self.url = f"{ self.aci }/api/node/class/qosClass.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<QOS Classes Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def fault_summary(self):
        self.url = f"{ self.aci }/api/node/class/faultSummary.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Fault Summary Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def audit_log(self):
        self.url = f"{ self.aci }/api/node/class/aaaModLR.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Audit Log Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def ip_addresses(self):
        self.url = f"{ self.aci }/api/node/class/fvIp.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<IP Addresses Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def events(self):
        self.url = f"{ self.aci }/api/node/class/eventRecord.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Events Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def licenses(self):
        self.url = f"{ self.aci }/api/node/class/licenseEntitlement.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<License Entitlements Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def bgp_rr(self):
        self.url = f"{ self.aci }/api/node/class/bgpRRNodePEp.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<BGP Route Reflectors Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def interface_policies(self):
        self.url = f"{ self.aci }/api/node/class/infraPortS.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Interface Policies Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def interface_profiles(self):
        self.url = f"{ self.aci }/api/node/class/infraProfile.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Interface Profiles Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def fabric_pods(self):
        self.url = f"{ self.aci }/api/node/class/fabricPod.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Fabric Pods Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def fabric_paths(self):
        self.url = f"{ self.aci }/api/node/class/fabricPath.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Fabric Paths Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

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
        return(prefix_lists)
        
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
        return(ip_prefix_list_details)

    def users(self):
        self.url = f"{ self.aci }/api/node/class/aaaUser.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Users Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def security_domains(self):
        self.url = f"{ self.aci }/api/node/class/aaaDomain.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Security Domains Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def contract_subjects(self):
        self.url = f"{ self.aci }/api/node/class/vzSubj.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Contract Subjects Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def health(self):
        self.url = f"{ self.aci }/api/node/mo/topology/health.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Health Status code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def fabric_node_ssl_certificate(self):
        self.url = f"{ self.aci }/api/node/class/pkiFabricNodeSSLCertificate.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<PKI Fabric Node SSL Certificate code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

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
        return(tenant_health)

    def fabric_membership(self):
        self.url = f"{ self.aci }/api/node/class/topSystem.json?query-target=subtree&target-subtree-class=firmwareCtrlrRunning"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Fabric Membership code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def cluster_health(self):
        self.url = f"{ self.aci }/api/node/mo/topology/pod-1/node-1/av.json?query-target=children&target-subtree-class=infraWiNode"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Cluster Health code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def device_packages(self):
        self.url = f"{ self.aci }/api/node/class/vnsMDev.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Device Packages code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def cluster_aggregate_interfaces(self):
        self.url = f"{ self.aci }/api/node/class/cnwAggrIf.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Cluster Aggregate Interfaces code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def l3_interfaces(self):
        self.url = f"{ self.aci }/api/node/class/l3Inst.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<L3 Interfaces code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def access_control_entities(self):
        self.url = f"{ self.aci }/api/node/class/actrlEntity.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Access Control Entities code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def access_control_instances(self):
        self.url = f"{ self.aci }/api/node/class/actrlInst.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Access Control Instances code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def access_control_rules(self):
        self.url = f"{ self.aci }/api/node/class/actrlRule.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Access Control Rules code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def cluster_physical_interfaces(self):
        self.url = f"{ self.aci }/api/node/class/cnwPhysIf.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Cluster Physical Interfaces code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def compute_controllers(self):
        self.url = f"{ self.aci }/api/node/class/compCtrlr.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Compute Controllers code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

    def compute_domains(self):
        self.url = f"{ self.aci }/api/node/class/compDom.json"
        response = requests.request("GET", self.url, cookies = self.cookie, verify=False)
        print(f"<Compute Domains code { response.status_code } for { self.url }>")
        response_dict  = response.json()
        return(response_dict)

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

        if "cnwPhysIf" in self.url:
            with open('Cluster Physical Interfaces/JSON/Cluster Physical Interfaces.json', 'w' ) as f:
                f.write(parsed_json)

        if "compCtrlr" in self.url:
            with open('Compute Controllers/JSON/Compute Controllers.json', 'w' ) as f:
                f.write(parsed_json)

        if "compDom" in self.url:
            with open('Compute Domains/JSON/Compute Domains.json', 'w' ) as f:
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

        if "cnwPhysIf" in self.url:
            with open('Cluster Physical Interfaces/YAML/Cluster Physical Interfaces.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "compCtrlr" in self.url:
            with open('Compute Controllers/YAML/Compute Controllers.yaml', 'w' ) as f:
                f.write(clean_yaml)

        if "compDom" in self.url:
            with open('Compute Domains/YAML/Compute Domains.yaml', 'w' ) as f:
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

        if "cnwPhysIf" in self.url:
            with open('Cluster Physical Interfaces/CSV/Cluster Physical Interfaces.csv', 'w' ) as f:
                f.write(csv_output)

        if "compCtrlr" in self.url:
            with open('Compute Controllers/CSV/Compute Controllers.csv', 'w' ) as f:
                f.write(csv_output)

        if "compDom" in self.url:
            with open('Compute Domains/CSV/Compute Domains.csv', 'w' ) as f:
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

        if "cnwPhysIf" in self.url:
            with open('Cluster Physical Interfaces/Markdown/Cluster Physical Interfaces.md', 'w' ) as f:
                f.write(markdown_output)

        if "compCtrlr" in self.url:
            with open('Compute Controllers/Markdown/Compute Controllers.md', 'w' ) as f:
                f.write(markdown_output)

        if "compDom" in self.url:
            with open('Compute Domains/Markdown/Compute Domains.md', 'w' ) as f:
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

        if "cnwPhysIf" in self.url:
            with open('Cluster Physical Interfaces/HTML/Cluster Physical Interfaces.html', 'w' ) as f:
                f.write(html_output)

        if "compCtrlr" in self.url:
            with open('Compute Controllers/HTML/Compute Controllers.html', 'w' ) as f:
                f.write(html_output)

        if "compDom" in self.url:
            with open('Compute Domains/HTML/Compute Domains.html', 'w' ) as f:
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

        if "cnwPhysIf" in self.url:
            with open('Cluster Physical Interfaces/Mindmap/Cluster Physical Interfaces.md', 'w' ) as f:
                f.write(mindmap_output)

        if "compCtrlr" in self.url:
            with open('Compute Controllers/Mindmap/Compute Controllers.md', 'w' ) as f:
                f.write(mindmap_output)

        if "compDom" in self.url:
            with open('Compute Domains/Mindmap/Compute Domains.md', 'w' ) as f:
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
