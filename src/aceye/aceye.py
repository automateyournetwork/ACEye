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
        parsed_json = json.dumps(self.audit_log(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.ip_addresses(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.events(), indent=4, sort_keys=True)
        self.all_files(parsed_json)

    def make_directories(self):
        api_list = ['Tenant',
                    'Application Profiles',
                    'Attachable Access Entity Profiles',
                    'Audit Log',
                    'Bridge Domains',
                    'Contexts',
                    'Contracts',
                    'Endpoints',
                    'EPG',
                    'Events',
                    'Fabric Nodes',
                    'Fault Summary',
                    'Filters',
                    'IP Addresses',
                    'L2Outs',
                    'L3 Domains',
                    'L3Outs',
                    'Leaf Interface Profiles',
                    'Leaf Switch Profiles',
                    'Physical Domains',
                    'Physical Interfaces',
                    'QOS Classes',
                    'Spine Interface Profiles',
                    'Spine Switch Profiles',
                    'Subnets',
                    'Tenant',
                    'Top System',
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
