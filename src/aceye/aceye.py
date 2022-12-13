import os
import json
import requests
import aiohttp
import asyncio
import aiofiles
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
        asyncio.run(self.main())

    def make_directories(self):
        api_list = ['Access Bundle Groups',
                    'Access Control Entities',
                    'Access Control Instances',
                    'Access Control Rules',
                    'Access Control Scopes',
                    'Access Policy Group Source Relationships',
                    'Access Port Groups',
                    'Access Port Profiles',
                    'Application Profiles',
                    'ARP Adjacency Endpoints',
                    'ARP Database',
                    'ARP Domain',
                    'ARP Entity',
                    'ARP Instances',
                    'ARP Interfaces',
                    'Attachable Access Entity Profiles',
                    'Attachable Access Entity Profiles Source Relationships',
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
                    'Bridge Domains Target Relationships',
                    'Bridge Domains To Outside',                    
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
                    'Context Source Relationships',
                    'Contexts',
                    'Contexts Target Relationships',
                    'Contract Consumer Interfaces',
                    'Contract Consumers',
                    'Contract Consumers Root',
                    'Contract Providers',
                    'Contract Providers Root',
                    'Contract Subjects',
                    'Contract Subjects Filter Attributes',
                    'Contracts',
                    'Controllers',
                    'Device Packages',
                    'Domain Attachments',
                    'Domain Profile Source Relationships',
                    'Endpoint Profile Containers',
                    'Endpoints',
                    'Endpoints To Paths',
                    'EPG Bridge Domain Links',
                    'EPGs',
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
                    'Equipment SPROM Power Supplies',
                    'Equipment SPROM Power Supply Blocks',
                    'Equipment SPROM Supervisors',
                    'Equipment Storage',
                    'Equipment Supervisor Slots',
                    'Equipment Supervisors',
                    'Ethernet Port Manager Physical Interfaces',
                    'Events',
                    'External Unmanaged Nodes',
                    'External Unmanaged Nodes Interfaces',
                    'Fabric Extended Path Endpoint Containers',
                    'Fabric Instances',
                    'Fabric Link Containers',
                    'Fabric Links',
                    'Fabric Loose Links',
                    'Fabric Loose Nodes',
                    'Fabric Membership',
                    'Fabric Nodes',
                    'Fabric Node SSL Certificates',
                    'Fabric Path Endpoint Containers',
                    'Fabric Path Endpoints',
                    'Fabric Paths',
                    'Fabric Pods',
                    'Fabric Protected Path Endpoint Containers',
                    'Fault Summary',
                    'FEX Policies',
                    'Fibre Channel Entities',
                    'Firmware Card Running',
                    'Firmware Compute Running',
                    'Firmware Running',
                    'Function Policies',
                    'Health',
                    'Host Port Selectors',
                    'Interface Policies',
                    'Interface Profiles',
                    'IP Addresses',
                    'IPv4 Addresses',
                    'IPv4 Domains',
                    'IPv4 Entities',
                    'IPv4 Instances',
                    'IPv4 Interfaces',
                    'IPv4 Next Hop',
                    'IPv4 Routes',
                    'ISIS Adjacency Endpoints',
                    'ISIS Discovered Tunnel Endpoints',
                    'ISIS Domains',
                    'ISIS Domains Level',
                    'ISIS Entities',
                    'ISIS Instances',
                    'ISIS Interfaces',
                    'ISIS Interfaces Level',
                    'ISIS Next Hop',
                    'ISIS Routes',
                    'L2 Bridge Domains',
                    'L2 EPG Bridge Domain Source Relationships',
                    'L2 External Instance Profiles',
                    'L2 External Interfaces',
                    'L2 External Logical Interface Profiles',
                    'L2 External Logical Node Profiles',
                    'L2 Interface Source Relationships',
                    'L2Out Paths',
                    'L2Outs',
                    'L3 Contexts',
                    'L3 Contexts Source Relationships',
                    'L3 Domains',
                    'L3 Domains Source Relationships',
                    'L3 Instances',
                    'L3 Interfaces',
                    'L3 Logical Interface Profiles',
                    'L3 Logical Node Profiles',
                    'L3 Physical Interface Source Relationships',
                    'L3 Routed Interfaces',
                    'L3 Routed Loopback Interfaces',
                    'L3 Subinterfaces',
                    'L3 Subnets',
                    'L3Out IP Addresses',
                    'L3Out Members',
                    'L3Out Node Source Relationships',
                    'L3Out Path Source Relationships',
                    'L3Out Profiles',
                    'L3Outs',
                    'LACP Entities',
                    'LACP Instances',
                    'LACP Interfaces',
                    'Leaf Interface Profiles',
                    'Leaf Switch Profiles',
                    'License Entitlements',
                    'LLDP Adjacency Endpoints',
                    'LLDP Entities',
                    'LLDP Instances',
                    'LLDP Interfaces',
                    'Locales',
                    'Management Interfaces',
                    'OSPF Adjacency Endpoints',
                    'OSPF Areas',
                    'OSPF Database',
                    'OSPF Domains',
                    'OSPF Entities',
                    'OSPF External Profiles',
                    'OSPF Instances',
                    'OSPF Interfaces',
                    'OSPF Routes',
                    'OSPF Unicast Next Hop',
                    'Path Attachments',
                    'Physical Domains',
                    'Physical Interfaces',
                    'Port Blocks',
                    'Port Channel Aggregate Interfaces',
                    'Port Channel Member Interfaces',
                    'Prefix List',
                    'Prefix List Detailed',
                    'QOS Classes',
                    'Route Policies',
                    'Security Domains',
                    'Spine Access Policy Groups',
                    'Spine Access Port Profiles',
                    'Spine Host Port Selectors',
                    'Spine Interface Profiles',
                    'Spine Switch Profiles',
                    'Static Route Next Hop Policies',
                    'Subnets',
                    'SVIs',
                    'Tenant',
                    'Tenant Health',
                    'Top System',
                    'Tunnel Interfaces',
                    'Unicast Route Database',
                    'Unicast Route Domains',
                    'Unicast Route Entities',
                    'Unicast Route Next Hop',
                    'Unicast Routes',
                    'Users',
                    'VLAN Encapsulation Blocks',
                    'VLAN Endpoint Group Encapsulation',
                    'VLAN Namespace Policies',
                    'VLAN Namespace Source Relationships',
                    'VLAN Pools',
                    'VMM Controller Profiles',
                    'VMM Domain Profiles',
                    'VMM Provider Profiles',
                    'VMM User Profiles',
                    'VPC Configurations',
                    'VPC Domains',
                    'VPC Entities',
                    'VPC Instances',
                    'VPC Interfaces',
                    'vzAny',
                    'vzAny To Consumers',
                    'vzAny To Providers',
                    'vzDeny Rules',
                    'vzEntries',
                    'vzFilters',
                    'vzInterface Source Relationships',
                    'vzRule Owner',
                    'vzTaboo',
                    'Wired Nodes']
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

    api_list = ["/api/node/class/fvTenant.json",
                "/api/node/class/fvAEPg.json",
                "/api/node/class/fvBD.json",
                '/api/node/class/fvCtx.json',
                '/api/node/class/fvAp.json',
                '/api/node/class/l3extOut.json',
                '/api/node/class/l2extOut.json',
                '/api/node/class/topSystem.json',
                '/api/node/class/fvSubnet.json',
                '/api/node/class/fvCEp.json',
                '/api/node/class/fabricNode.json',
                '/api/node/class/infraAccPortP.json',
                '/api/node/class/infraSpAccPortP.json',
                '/api/node/class/infraNodeP.json',
                '/api/node/class/infraSpineP.json',
                '/api/node/class/fvnsVlanInstP.json',
                '/api/node/class/infraAttEntityP.json',
                '/api/node/class/vzBrCP.json',
                '/api/node/class/vzEntry.json',
                '/api/node/class/physDomP.json',
                '/api/node/class/l3extDomP.json',
                '/api/node/class/qosClass.json',
                '/api/node/class/faultSummary.json',
                '/api/node/class/aaaModLR.json',
                '/api/node/class/fvIp.json',
                #'/api/node/class/eventRecord.json',
                '/api/node/class/licenseEntitlement.json',
                '/api/node/class/bgpRRNodePEp.json',
                '/api/node/class/infraPortS.json',
                '/api/node/class/infraProfile.json',
                '/api/node/class/fabricPod.json',
                '/api/node/class/fabricPath.json',
                '/api/node/class/fvTenant.json',
                '/api/node/class/aaaUser.json',
                '/api/node/class/aaaDomain.json',
                '/api/node/class/vzSubj.json',
                '/api/node/mo/topology/health.json',
                '/api/node/class/pkiFabricNodeSSLCertificate.json',
                '/api/node/class/topSystem.json?query-target=subtree&target-subtree-class=firmwareCtrlrRunning',
                '/api/node/mo/topology/pod-1/node-1/av.json?query-target=children&target-subtree-class=infraWiNode',
                '/api/node/class/vnsMDev.json',
                '/api/node/class/cnwAggrIf.json',
                '/api/node/class/l3Inst.json',
                '/api/node/class/actrlEntity.json',
                '/api/node/class/actrlInst.json',
                '/api/node/class/actrlRule.json',
                '/api/node/class/actrlScope.json',
                '/api/node/class/cnwPhysIf.json',
                '/api/node/class/compCtrlr.json',
                '/api/node/class/compDom.json',
                '/api/node/class/compEpPD.json',
                '/api/node/class/compProv.json',
                '/api/node/class/arpAdjEp.json',
                '/api/node/class/arpDb.json',
                '/api/node/class/arpDom.json',
                '/api/node/class/arpEntity.json',
                '/api/node/class/arpIf.json',
                '/api/node/class/arpInst.json',
                '/api/node/class/bgpDom.json',
                '/api/node/class/bgpDomAf.json',
                '/api/node/class/bgpEntity.json',
                '/api/node/class/bgpInst.json',
                '/api/node/class/bgpInstPol.json',
                '/api/node/class/bgpPeer.json',
                '/api/node/class/bgpPeerAfEntry.json',
                '/api/node/class/bgpPeerEntry.json',
                '/api/node/class/bgpRRP.json',
                '/api/node/class/cdpAdjEp.json',
                '/api/node/class/cdpEntity.json',
                '/api/node/class/cdpIf.json',
                '/api/node/class/cdpInst.json',
                '/api/node/class/cdpIntfAddr.json',
                '/api/node/class/cdpMgmtAddr.json',
                '/api/node/class/cnwRsMbrIfs.json',
                '/api/node/class/compRsDomP.json',
                '/api/node/class/eqptBSlot.json',
                '/api/node/class/eqptBoard.json',
                '/api/node/class/eqptCPU.json',
                '/api/node/class/eqptCh.json',
                '/api/node/class/eqptDimm.json',
                '/api/node/class/eqptExtCh.json',
                '/api/node/class/eqptFabP.json',
                '/api/node/class/eqptFan.json',
                '/api/node/class/eqptFpga.json',
                '/api/node/class/eqptFt.json',
                '/api/node/class/eqptFtSlot.json',
                '/api/node/class/eqptIndLed.json',
                '/api/node/class/eqptLC.json',
                '/api/node/class/eqptLCSlot.json',
                '/api/node/class/eqptLeafP.json',
                '/api/node/class/eqptLocLed.json',
                '/api/node/class/eqptPsu.json',
                '/api/node/class/eqptPsuSlot.json',
                '/api/node/class/eqptRsIoPPhysConf.json',
                '/api/node/class/eqptSensor.json',
                '/api/node/class/eqptSpCmnBlk.json',
                '/api/node/class/eqptSpromLc.json',
                '/api/node/class/eqptSpromPsu.json',
                '/api/node/class/eqptSpromPsuBlk.json',
                '/api/node/class/eqptSpromSup.json',
                '/api/node/class/eqptStorage.json',
                '/api/node/class/eqptSupC.json',
                '/api/node/class/eqptSupCSlot.json',
                '/api/node/class/ethpmPhysIf.json',
                '/api/node/class/fabricExtPathEpCont.json',
                '/api/node/class/fabricInst.json',
                '/api/node/class/fabricLink.json',
                '/api/node/class/fabricLinkCont.json',
                '/api/node/class/fabricLooseLink.json',
                '/api/node/class/fabricLooseNode.json',
                '/api/node/class/fabricPathEp.json',
                '/api/node/class/fabricPathEpCont.json',
                '/api/node/class/fabricProtPathEpCont.json',
                '/api/node/class/fcEntity.json',
                '/api/node/class/firmwareCardRunning.json',
                '/api/node/class/firmwareCompRunning.json',
                '/api/node/class/firmwareRunning.json',
                '/api/node/class/fvEpPCont.json',
                '/api/node/class/fvLocale.json',
                '/api/node/class/fvRsBDToOut.json',
                '/api/node/class/fvRsBd.json',
                '/api/node/class/fvRsCEpToPathEp.json',
                '/api/node/class/fvRsCons.json',
                '/api/node/class/fvRsConsIf.json',
                '/api/node/class/fvRsCtx.json',
                '/api/node/class/fvRsDomAtt.json',
                '/api/node/class/fvRsPathAtt.json',
                '/api/node/class/fvRsProv.json',
                '/api/node/class/fvRtBd.json',
                '/api/node/class/fvRtCtx.json',
                '/api/node/class/fvnsEncapBlk.json',
                '/api/node/class/fvnsVlanInstP.json',
                '/api/node/class/infraAccBndlGrp.json',
                '/api/node/class/infraAccPortGrp.json',
                '/api/node/class/infraAccPortP.json',
                '/api/node/class/infraCont.json',
                '/api/node/class/infraFexP.json',
                '/api/node/class/infraFuncP.json',
                '/api/node/class/infraHPortS.json',
                '/api/node/class/infraPortBlk.json',
                '/api/node/class/infraRsAccBaseGrp.json',
                '/api/node/class/infraRsAttEntP.json',
                '/api/node/class/infraRsDomP.json',
                '/api/node/class/infraRsSpAccGrp.json',
                '/api/node/class/infraRsVlanNs.json',
                '/api/node/class/infraSHPortS.json',
                '/api/node/class/infraSpAccPortP.json',
                '/api/node/class/infraWiNode.json',
                '/api/node/class/ipNexthopP.json',
                '/api/node/class/ipRouteP.json',
                '/api/node/class/ipv4Addr.json',
                '/api/node/class/ipv4Dom.json',
                '/api/node/class/ipv4Entity.json',
                '/api/node/class/ipv4If.json',
                '/api/node/class/ipv4Inst.json',
                '/api/node/class/ipv4Nexthop.json',
                '/api/node/class/ipv4Route.json',
                '/api/node/class/isisAdjEp.json',
                '/api/node/class/isisDTEp.json',
                '/api/node/class/isisDom.json',
                '/api/node/class/isisDomLvl.json',
                '/api/node/class/isisEntity.json',
                '/api/node/class/isisIf.json',
                '/api/node/class/isisIfLvl.json',
                '/api/node/class/isisInst.json',
                '/api/node/class/isisNexthop.json',
                '/api/node/class/isisRoute.json',
                '/api/node/class/l2BD.json',
                '/api/node/class/l2ExtIf.json',
                '/api/node/class/l2RsEthIf.json',
                '/api/node/class/l2extInstP.json',
                '/api/node/class/l2extLIfP.json',
                '/api/node/class/l2extLNodeP.json',
                '/api/node/class/l2extRsEBd.json',
                '/api/node/class/l2extRsPathL2OutAtt.json',
                '/api/node/class/l3Ctx.json',
                '/api/node/class/l3EncRtdIf.json',
                '/api/node/class/l3Inst.json',
                '/api/node/class/l3LbRtdIf.json',
                '/api/node/class/l3RsEncPhysRtdConf.json',
                '/api/node/class/l3RtdIf.json',
                '/api/node/class/l3extInstP.json',
                '/api/node/class/l3extIp.json',
                '/api/node/class/l3extLIfP.json',
                '/api/node/class/l3extLNodeP.json',
                '/api/node/class/l3extMember.json',
                '/api/node/class/l3extRsEctx.json',
                '/api/node/class/l3extRsL3DomAtt.json',
                '/api/node/class/l3extRsNodeL3OutAtt.json',
                '/api/node/class/l3extRsPathL3OutAtt.json',
                '/api/node/class/l3extSubnet.json',
                '/api/node/class/lacpEntity.json',
                '/api/node/class/lacpIf.json',
                '/api/node/class/lacpInst.json',
                '/api/node/class/leqptLooseNode.json',
                '/api/node/class/leqptRsLsNodeToIf.json',
                '/api/node/class/lldpAdjEp.json',
                '/api/node/class/lldpEntity.json',
                '/api/node/class/lldpIf.json',
                '/api/node/class/lldpInst.json',
                '/api/node/class/mgmtMgmtIf.json',
                '/api/node/class/ospfAdjEp.json',
                '/api/node/class/ospfArea.json',
                '/api/node/class/ospfDb.json',
                '/api/node/class/ospfDom.json',
                '/api/node/class/ospfEntity.json',
                '/api/node/class/ospfExtP.json',
                '/api/node/class/ospfIf.json',
                '/api/node/class/ospfInst.json',
                '/api/node/class/ospfRoute.json',
                '/api/node/class/ospfUcNexthop.json',
                '/api/node/class/pcAggrIf.json',
                '/api/node/class/pcRsMbrIfs.json',
                '/api/node/class/sviIf.json',
                '/api/node/class/tunnelIf.json',
                '/api/node/class/uribv4Db.json',
                '/api/node/class/uribv4Dom.json',
                '/api/node/class/uribv4Entity.json',
                '/api/node/class/uribv4Nexthop.json',
                '/api/node/class/uribv4Route.json',
                '/api/node/class/vlanCktEp.json',
                '/api/node/class/vmmCtrlrP.json',
                '/api/node/class/vmmDomP.json',
                '/api/node/class/vmmProvP.json',
                '/api/node/class/vmmUsrAccP.json',
                '/api/node/class/vpcDom.json',
                '/api/node/class/vpcEntity.json',
                '/api/node/class/vpcIf.json',
                '/api/node/class/vpcInst.json',
                '/api/node/class/vpcRsVpcConf.json',
                '/api/node/class/vzAny.json',
                '/api/node/class/vzFilter.json',
                '/api/node/class/vzRsAnyToCons.json',
                '/api/node/class/vzRsAnyToProv.json',
                '/api/node/class/vzRsDenyRule.json',
                '/api/node/class/vzRsIf.json',
                '/api/node/class/vzRsSubjFiltAtt.json',
                '/api/node/class/vzRtCons.json',
                '/api/node/class/vzRtProv.json',
                '/api/node/class/vzRuleOwner.json',
                '/api/node/class/vzTaboo.json'
            ]

    async def get_api(self, api_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.aci}{api_url}",cookies = self.cookie, verify_ssl=False) as resp:
                response_dict = await resp.json()
                print(f"{api_url} Status Code {resp.status}")
                return (api_url,response_dict)

    async def main(self):
        results = await asyncio.gather(*(self.get_api(api_url) for api_url in self.api_list))
        await self.all_files(json.dumps(results, indent=4, sort_keys=True))
        results = await asyncio.gather((self.physical_interfaces()))
        await self.all_files(json.dumps(results, indent=4, sort_keys=True))        
        results = await asyncio.gather((self.prefix_list()))
        await self.all_files(json.dumps(results, indent=4, sort_keys=True))        
        results = await asyncio.gather((self.prefix_list_detailed()))
        await self.all_files(json.dumps(results, indent=4, sort_keys=True))        
        results = await asyncio.gather((self.tenant_health()))
        await self.all_files(json.dumps(results, indent=4, sort_keys=True))


    async def physical_interfaces(self):

        async with aiohttp.ClientSession() as session:
            api_url = f"{ self.aci }/api/node/class/fabricNode.json"
            async with session.get(api_url,cookies = self.cookie, verify_ssl=False) as resp:
                node_response_dict = await resp.json()
                print(f"{api_url} Status Code {resp.status}")
                physical_interfaces = []
                for node in node_response_dict['imdata']:
                    api_url = f"{self.aci}/api/node/class/{ node['fabricNode']['attributes']['dn']}/l1PhysIf.json"
                    async with session.get(f"{self.aci}/api/node/class/{ node['fabricNode']['attributes']['dn']}/l1PhysIf.json",cookies = self.cookie, verify_ssl=False) as resp:                        
                        print(f"{api_url} Status Code {resp.status}")
                        response_dict  = await resp.json()
                        physical_interfaces.append(response_dict['imdata'])
                return(api_url,physical_interfaces)

    async def prefix_list(self):

        async with aiohttp.ClientSession() as session:
            api_url = f"{ self.aci }/api/node/class/fvTenant.json"
            async with session.get(api_url,cookies = self.cookie, verify_ssl=False) as resp:
                print(f"{api_url} Status Code {resp.status}")
                tenants  = await resp.json()
                prefix_lists = []
                for tenant in tenants['imdata']:
                    api_url = f"{ self.aci }/api/node/mo/uni/tn-{ tenant['fvTenant']['attributes']['name'] }.json?query-target=subtree&target-subtree-class=rtctrlSubjP"
                    async with session.get(f"{ self.aci }/api/node/mo/uni/tn-{ tenant['fvTenant']['attributes']['name'] }.json?query-target=subtree&target-subtree-class=rtctrlSubjP", cookies = self.cookie, verify_ssl=False) as resp:
                        print(f"{api_url} Status Code {resp.status}")
                        response_dict  = await resp.json()
                        prefix_lists.append(response_dict['imdata'])
                return(api_url,prefix_lists)

    async def prefix_list_detailed(self):

        async with aiohttp.ClientSession() as session:
            api_url = f"{ self.aci }/api/node/class/fvTenant.json"
            async with session.get(api_url,cookies = self.cookie, verify_ssl=False) as resp:
                tenants  = await resp.json()
                prefix_lists = []
                ip_prefix_list_details = []
                for tenant in tenants['imdata']:
                    api_url = f"{ self.aci }/api/node/mo/uni/tn-{ tenant['fvTenant']['attributes']['name'] }.json?query-target=subtree&target-subtree-class=rtctrlSubjP"
                    async with session.get(f"{ self.aci }/api/node/mo/uni/tn-{ tenant['fvTenant']['attributes']['name'] }.json?query-target=subtree&target-subtree-class=rtctrlSubjP", cookies = self.cookie, verify_ssl=False) as resp:
                        response_dict  = await resp.json()
                        prefix_lists.append(response_dict['imdata'])
                        for item in prefix_lists:
                            if item:
                                for prefix in item:
                                    api_url = f"{ self.aci }/api/node/mo/uni/tn-{ tenant['fvTenant']['attributes']['name'] }/subj-{ prefix['rtctrlSubjP']['attributes']['name']}.json?query-target=children&target-subtree-class=rtctrlMatchRtDest"
                                    async with session.get(f"{ self.aci }/api/node/mo/uni/tn-{ tenant['fvTenant']['attributes']['name'] }/subj-{ prefix['rtctrlSubjP']['attributes']['name']}.json?query-target=children&target-subtree-class=rtctrlMatchRtDest", cookies = self.cookie, verify_ssl=False) as resp:
                                        print(f"{api_url} Status Code {resp.status}")
                                        response_dict  = await resp.json()
                                        ip_prefix_list_details.append(response_dict['imdata'])
                            else:
                                print("No prefix lists")
                        return(api_url,ip_prefix_list_details)

    async def tenant_health(self):

        async with aiohttp.ClientSession() as session:
            api_url = f"{ self.aci }/api/node/class/fvTenant.json"
            async with session.get(api_url,cookies = self.cookie, verify_ssl=False) as resp:
                print(f"{api_url} Status Code {resp.status}")
                tenants  = await resp.json()
                tenant_health = []
                for tenant in tenants['imdata']:
                    api_url = f"{ self.aci }/api/mo/uni/tn-{ tenant['fvTenant']['attributes']['name'] }/health.json"
                    async with session.get(f"{ self.aci }/api/mo/uni/tn-{ tenant['fvTenant']['attributes']['name'] }/health.json", cookies = self.cookie, verify_ssl=False) as resp:
                        print(f"{api_url} Status Code {resp.status}")
                        response_dict  = await resp.json()
                        tenant_health.append(response_dict['imdata'])
                        print(api_url)
                return(api_url,tenant_health)

    async def json_file(self, parsed_json):
        for api, payload in json.loads(parsed_json):
            if "Tenant" in api:
                async with aiofiles.open('Tenant/JSON/Tenants.json', mode='w') as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "AEPg" in api:
                async with aiofiles.open('EPGs/JSON/EPGs.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvBD" in api:
                async with aiofiles.open('Bridge Domains/JSON/Bridge Domains.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvCtx" in api:
                async with aiofiles.open('Contexts/JSON/Contexts.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "Ap" in api:
                async with aiofiles.open('Application Profiles/JSON/Application Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3extOut" in api:
                async with aiofiles.open('L3Outs/JSON/L3Outs.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l2extOut" in api:
                async with aiofiles.open('L2Outs/JSON/L2Outs.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "topSystem" in api:
                if "?" not in api:
                    async with aiofiles.open('Top System/JSON/Top System.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvSubnet" in api:
                async with aiofiles.open('Subnets/JSON/Subnets.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvCEp" in api:
                async with aiofiles.open('Endpoints/JSON/Endpoints.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fabricNode" in api:
                async with aiofiles.open('Fabric Nodes/JSON/Fabric Nodes.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l1PhysIf" in api:
                async with aiofiles.open('Physical Interfaces/JSON/Physical Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if "infraAccPortP" in api:
                async with aiofiles.open('Leaf Interface Profiles/JSON/Leaf Interface Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraSpAccPortP" in api:
                async with aiofiles.open('Spine Interface Profiles/JSON/Spine Interface Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraNodeP" in api:
                async with aiofiles.open('Leaf Switch Profiles/JSON/Leaf Switch Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraSpineP" in api:
                async with aiofiles.open('Spine Switch Profiles/JSON/Spine Switch Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvnsVlanInstP" in api:
                async with aiofiles.open('VLAN Pools/JSON/VLAN Pools.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraAttEntityP" in api:
                async with aiofiles.open('Attachable Access Entity Profiles/JSON/Attachable Access Entity Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vzBrCP" in api:
                async with aiofiles.open('Contracts/JSON/Contracts.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vzEntry" in api:
                async with aiofiles.open('vzEntries/JSON/vzEntries.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "physDomP" in api:
                async with aiofiles.open('Physical Domains/JSON/Physical Domains.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3extDomP" in api:
                async with aiofiles.open('L3 Domains/JSON/L3 Domains.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "qosClass" in api:
                async with aiofiles.open('QOS Classes/JSON/QOS Classes.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "faultSummary" in api:
                async with aiofiles.open('Fault Summary/JSON/Fault Summary.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "aaaModLR" in api:
                async with aiofiles.open('Audit Log/JSON/Audit Log.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvIp" in api:
                async with aiofiles.open('IP Addresses/JSON/IP Addresses.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eventRecord" in api:
                async with aiofiles.open('Events/JSON/Events.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "licenseEntitlement" in api:
                async with aiofiles.open('License Entitlements/JSON/License Entitlements.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "bgpRRNodePEp" in api:
                async with aiofiles.open('BGP Route Reflectors/JSON/BGP Route Reflectors.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraPortS" in api:
                async with aiofiles.open('Interface Policies/JSON/Interface Policies.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraProfile" in api:
                async with aiofiles.open('Interface Profiles/JSON/Interface Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fabricPod" in api:
                async with aiofiles.open('Fabric Pods/JSON/Fabric Pods.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fabricPath" in api:
                if "fabricPathEp" in api:
                    if "Cont" in api:
                        async with aiofiles.open('Fabric Path Endpoint Containers/JSON/Fabric Path Endpoint Containers.json', mode='w' ) as f:
                            await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))
                    else:
                        async with aiofiles.open('Fabric Path Endpoints/JSON/Fabric Path Endpoints.json', mode='w' ) as f:
                            await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))
                else:
                    async with aiofiles.open('Fabric Paths/JSON/Fabric Paths.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "rtctrlSubjP" in api:
                async with aiofiles.open('Prefix List/JSON/Prefix List.json', mode='w' ) as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if "rtctrlMatchRtDest" in api:
                async with aiofiles.open('Prefix List Detailed/JSON/Prefix List Detailed.json', mode='w' ) as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if "aaaUser" in api:
                async with aiofiles.open('Users/JSON/Users.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "aaaDomain" in api:
                async with aiofiles.open('Security Domains/JSON/Security Domains.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vzSubj" in api:
                async with aiofiles.open('Contract Subjects/JSON/Contract Subjects.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "topology/health" in api:
                async with aiofiles.open('Health/JSON/Health.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "pkiFabricNodeSSLCertificate" in api:
                async with aiofiles.open('Fabric Node SSL Certificates/JSON/Fabric Node SSL Certificates.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "tn-" in api:
                if "health" in api:
                    async with aiofiles.open('Tenant Health/JSON/Tenant Health.json', mode='w' ) as f:
                        await f.write(json.dumps(payload, indent=4, sort_keys=True))

            if "firmwareCtrlrRunning" in api:
                async with aiofiles.open('Fabric Membership/JSON/Fabric Membership.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraWiNode" in api:
                async with aiofiles.open('Cluster Health/JSON/Cluster Health.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vnsMDev" in api:
                async with aiofiles.open('Device Packages/JSON/Device Packages.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "cnwAggrIf" in api:
                async with aiofiles.open('Cluster Aggregate Interfaces/JSON/Cluster Aggregate Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3Inst" in api:
                async with aiofiles.open('L3 Interfaces/JSON/L3 Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "actrlEntity" in api:
                async with aiofiles.open('Access Control Entities/JSON/Access Control Entities.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "actrlInst" in api:
                async with aiofiles.open('Access Control Instances/JSON/Access Control Instances.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "actrlRule" in api:
                async with aiofiles.open('Access Control Rules/JSON/Access Control Rules.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "actrlScope" in api:
                async with aiofiles.open('Access Control Scopes/JSON/Access Control Scopes.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "cnwPhysIf" in api:
                async with aiofiles.open('Cluster Physical Interfaces/JSON/Cluster Physical Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "compCtrlr" in api:
                async with aiofiles.open('Compute Controllers/JSON/Compute Controllers.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "compDom" in api:
                async with aiofiles.open('Compute Domains/JSON/Compute Domains.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "compEpPD" in api:
                async with aiofiles.open('Compute Endpoint Policy Descriptions/JSON/Compute Endpoint Policy Descriptions.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "compProv" in api:
                async with aiofiles.open('Compute Providers/JSON/Compute Providers.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "arpAdjEp" in api:
                async with aiofiles.open('ARP Adjacency Endpoints/JSON/ARP Adjacency Endpoints.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "arpDb" in api:
                async with aiofiles.open('ARP Database/JSON/ARP Database.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "arpDom" in api:
                async with aiofiles.open('ARP Domain/JSON/ARP Domain.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "arpEntity" in api:
                async with aiofiles.open('ARP Entity/JSON/ARP Entity.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "arpIf" in api:
                async with aiofiles.open('ARP Interfaces/JSON/ARP Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "arpInst" in api:
                async with aiofiles.open('ARP Instances/JSON/ARP Instances.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "bgpDom" in api:
                if "Af" in api:
                    async with aiofiles.open('BGP Domain Address Families/JSON/BGP Domain Address Families.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))
                else:
                    async with aiofiles.open('BGP Domains/JSON/BGP Domains.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "bgpEntity" in api:
                async with aiofiles.open('BGP Entities/JSON/BGP Entities.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "bgpInst" in api:
                if "InstPol" in api:
                    async with aiofiles.open('BGP Instances Policy/JSON/BGP Instances Policy.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))
                else:
                    async with aiofiles.open('BGP Instances/JSON/BGP Instances.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "bgpPeer" in api:
                if "bgpPeerAf" in api:
                    async with aiofiles.open('BGP Peers AF Entries/JSON/BGP Peers AF Entries.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))
                elif "bgpPeerEntry" in api:
                    async with aiofiles.open('BGP Peers Entries/JSON/BGP Peers Entries.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))
                else:
                    async with aiofiles.open('BGP Peers/JSON/BGP Peers.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "bgpRRP" in api:
                async with aiofiles.open('BGP Route Reflector Policies/JSON/BGP Route Reflector Policies.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "cdpAdjEp" in api:
                async with aiofiles.open('CDP Adjacency Endpoints/JSON/CDP Adjacency Endpoints.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "cdpEntity" in api:
                async with aiofiles.open('CDP Entities/JSON/CDP Entities.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "cdpIf" in api:
                async with aiofiles.open('CDP Interfaces/JSON/CDP Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "cdpInst" in api:
                async with aiofiles.open('CDP Instances/JSON/CDP Instances.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "cdpIntfAddr" in api:
                async with aiofiles.open('CDP Interface Addresses/JSON/CDP Interface Addresses.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "cdpMgmtAddr" in api:
                async with aiofiles.open('CDP Management Addresses/JSON/CDP Management Addresses.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "cnwRsMbrIfs" in api:
                async with aiofiles.open('Cluster RS Member Interfaces/JSON/Cluster RS Member Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "compRsDomP" in api:
                async with aiofiles.open('Compute RS Domain Policies/JSON/Compute RS Domain Policies.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptBSlot" in api:
                async with aiofiles.open('Equipment Board Slots/JSON/Equipment Board Slots.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptBoard" in api:
                async with aiofiles.open('Equipment Boards/JSON/Equipment Boards.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptCPU" in api:
                async with aiofiles.open('Equipment CPUs/JSON/Equipment CPUs.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptCh" in api:
                async with aiofiles.open('Equipment Chassis/JSON/Equipment Chassis.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptDimm" in api:
                async with aiofiles.open('Equipment DIMMs/JSON/Equipment DIMMs.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptExtCh" in api:
                async with aiofiles.open('Equipment Fabric Extenders/JSON/Equipment Fabric Extenders.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptFabP" in api:
                async with aiofiles.open('Equipment Fabric Ports/JSON/Equipment Fabric Ports.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptFan" in api:
                async with aiofiles.open('Equipment Fans/JSON/Equipment Fans.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptFpga" in api:
                async with aiofiles.open('Equipment Field Programmable Gate Arrays/JSON/Equipment Field Programmable Gate Arrays.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptFt" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Fan Tray Slots/JSON/Equipment Fan Tray Slots.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))
                else:
                    async with aiofiles.open('Equipment Fan Trays/JSON/Equipment Fan Trays.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptIndLed" in api:
                async with aiofiles.open('Equipment Indicator LEDs/JSON/Equipment Indicator LEDs.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptLC" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Line Card Slots/JSON/Equipment Line Card Slots.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))
                else:
                    async with aiofiles.open('Equipment Line Cards/JSON/Equipment Line Cards.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptLeafP" in api:
                async with aiofiles.open('Equipment Leaf Ports/JSON/Equipment Leaf Ports.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptLocLed" in api:
                async with aiofiles.open('Equipment Port Locator LEDs/JSON/Equipment Port Locator LEDs.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptPsu" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Power Supply Slots/JSON/Equipment Power Supply Slots.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))
                else:
                    async with aiofiles.open('Equipment Power Supplies/JSON/Equipment Power Supplies.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptRsIoPPhysConf" in api:
                async with aiofiles.open('Equipment RS IO Port Physical Configs/JSON/Equipment RS IO Port Physical Configs.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptSensor" in api:
                async with aiofiles.open('Equipment Sensors/JSON/Equipment Sensors.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptSpCmnBlk" in api:
                async with aiofiles.open('Equipment SP Common Blocks/JSON/Equipment SP Common Blocks.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptSpromLc" in api:
                async with aiofiles.open('Equipment SPROM LCs/JSON/Equipment SPROM LCs.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptSpromPsu" in api:
                if "Blk" in api:
                    async with aiofiles.open('Equipment SPROM Power Supply Blocks/JSON/Equipment SPROM Power Supply Blocks.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))
                else: 
                    async with aiofiles.open('Equipment SPROM Power Supplies/JSON/Equipment SPROM Power Supplies.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptSpromSup" in api:
                async with aiofiles.open('Equipment SPROM Supervisors/JSON/Equipment SPROM Supervisors.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptStorage" in api:
                async with aiofiles.open('Equipment Storage/JSON/Equipment Storage.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "eqptSupC" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Supervisor Slots/JSON/Equipment Supervisor Slots.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))
                else:
                    async with aiofiles.open('Equipment Supervisors/JSON/Equipment Supervisors.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ethpmPhysIf" in api:
                async with aiofiles.open('Ethernet Port Manager Physical Interfaces/JSON/Ethernet Port Manager Physical Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fabricExtPathEpCont" in api:
                async with aiofiles.open('Fabric Extended Path Endpoint Containers/JSON/Fabric Extended Path Endpoint Containers.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fabricInst" in api:
                async with aiofiles.open('Fabric Instances/JSON/Fabric Instances.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fabricLink" in api:
                if "Cont" in api:
                    async with aiofiles.open('Fabric Link Containers/JSON/Fabric Link Containers.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))
                else:
                    async with aiofiles.open('Fabric Links/JSON/Fabric Links.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fabricLooseLink" in api:
                async with aiofiles.open('Fabric Loose Links/JSON/Fabric Loose Links.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fabricLooseNode" in api:
                async with aiofiles.open('Fabric Loose Nodes/JSON/Fabric Loose Nodes.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fabricProtPathEpCont" in api:
                async with aiofiles.open('Fabric Protected Path Endpoint Containers/JSON/Fabric Protected Path Endpoint Containers.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fcEntity" in api:
                async with aiofiles.open('Fibre Channel Entities/JSON/Fibre Channel Entities.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "firmwareCardRunning" in api:
                async with aiofiles.open('Firmware Card Running/JSON/Firmware Card Running.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "firmwareCompRunning" in api:
                async with aiofiles.open('Firmware Compute Running/JSON/Firmware Compute Running.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "firmwareRunning" in api:
                async with aiofiles.open('Firmware Running/JSON/Firmware Running.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvEpPCont" in api:
                async with aiofiles.open('Endpoint Profile Containers/JSON/Endpoint Profile Containers.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvLocale" in api:
                async with aiofiles.open('Locales/JSON/Locales.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvRsBDToOut" in api:
                async with aiofiles.open('Bridge Domains To Outside/JSON/Bridge Domains To Outside.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvRsBd" in api:
                async with aiofiles.open('EPG Bridge Domain Links/JSON/EPG Bridge Domain Links.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvRsCons" in api:
                if "If" in api:
                    async with aiofiles.open('Contract Consumer Interfaces/JSON/Contract Consumer Interfaces.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))
                else:
                    async with aiofiles.open('Contract Consumers/JSON/Contract Consumers.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvRsCtx" in api:
                async with aiofiles.open('Context Source Relationships/JSON/Context Source Relationships.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvRsDomAtt" in api:
                async with aiofiles.open('Domain Attachments/JSON/Domain Attachments.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvRsPathAtt" in api:
                async with aiofiles.open('Path Attachments/JSON/Path Attachments.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvRsProv" in api:
                async with aiofiles.open('Contract Providers/JSON/Contract Providers.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvRtBd" in api:
                async with aiofiles.open('Bridge Domains Target Relationships/JSON/Bridge Domains Target Relationships.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvRtCtx" in api:
                async with aiofiles.open('Contexts Target Relationships/JSON/Contexts Target Relationships.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvnsEncapBlk" in api:
                async with aiofiles.open('VLAN Encapsulation Blocks/JSON/VLAN Encapsulation Blocks.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "fvnsVlanInstP" in api:
                async with aiofiles.open('VLAN Namespace Policies/JSON/VLAN Namespace Policies.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraAccBndlGrp" in api:
                async with aiofiles.open('Access Bundle Groups/JSON/Access Bundle Groups.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraAccPortGrp" in api:
                async with aiofiles.open('Access Port Groups/JSON/Access Port Groups.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraAccPortP" in api:
                async with aiofiles.open('Access Port Profiles/JSON/Access Port Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraContr" in api:
                async with aiofiles.open('Controllers/JSON/Controllers.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraFexP" in api:
                async with aiofiles.open('FEX Policies/JSON/FEX Policies.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraFuncP" in api:
                async with aiofiles.open('Function Policies/JSON/Function Policies.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraHPortS" in api:
                async with aiofiles.open('Host Port Selectors/JSON/Host Port Selectors.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraPortBlk" in api:
                async with aiofiles.open('Port Blocks/JSON/Port Blocks.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraRsAccBaseGrp" in api:
                async with aiofiles.open('Access Policy Group Source Relationships/JSON/Access Policy Group Source Relationships.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraRsAttEntP" in api:
                async with aiofiles.open('Attachable Access Entity Profiles Source Relationships/JSON/Attachable Access Entity Profiles Source Relationships.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraRsDomP" in api:
                async with aiofiles.open('Domain Profile Source Relationships/JSON/Domain Profile Source Relationships.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraRsSpAccGrp" in api:
                async with aiofiles.open('Spine Access Policy Groups/JSON/Spine Access Policy Groups.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraRsVlanNs" in api:
                async with aiofiles.open('VLAN Namespace Source Relationships/JSON/VLAN Namespace Source Relationships.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraSHPortS" in api:
                async with aiofiles.open('Spine Host Port Selectors/JSON/Spine Host Port Selectors.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraSpAccPortP" in api:
                async with aiofiles.open('Spine Access Port Profiles/JSON/Spine Access Port Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "infraWiNode" in api:
                async with aiofiles.open('Wired Nodes/JSON/Wired Nodes.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ipNexthopP" in api:
                async with aiofiles.open('Static Route Next Hop Policies/JSON/Static Route Next Hop Policies.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ipRouteP" in api:
                async with aiofiles.open('Route Policies/JSON/Route Policies.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ipv4Addr" in api:
                async with aiofiles.open('IPv4 Addresses/JSON/IPv4 Addresses.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ipv4Dom" in api:
                async with aiofiles.open('IPv4 Domains/JSON/IPv4 Domains.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ipv4Entity" in api:
                async with aiofiles.open('IPv4 Entities/JSON/IPv4 Entities.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ipv4If" in api:
                async with aiofiles.open('IPv4 Interfaces/JSON/IPv4 Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ipv4Inst" in api:
                async with aiofiles.open('IPv4 Instances/JSON/IPv4 Instances.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ipv4Nexthop" in api:
                async with aiofiles.open('IPv4 Next Hop/JSON/IPv4 Next Hop.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ipv4Route" in api:
                async with aiofiles.open('IPv4 Routes/JSON/IPv4 Routes.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "isisAdjEp" in api:
                async with aiofiles.open('ISIS Adjacency Endpoints/JSON/ISIS Adjacency Endpoints.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "isisDTEp" in api:
                async with aiofiles.open('ISIS Discovered Tunnel Endpoints/JSON/ISIS Discovered Tunnel Endpoints.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "isisDom" in api:
                if "Lvl" in api:
                    async with aiofiles.open('ISIS Domains Level/JSON/ISIS Domains Level.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))
                else:
                    async with aiofiles.open('ISIS Domains/JSON/ISIS Domains.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "isisEntity" in api:
                async with aiofiles.open('ISIS Entities/JSON/ISIS Entities.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "isisIf" in api:
                if "Lvl" in api:
                    async with aiofiles.open('ISIS Interfaces Level/JSON/ISIS Interfaces Level.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))
                else:
                    async with aiofiles.open('ISIS Interfaces/JSON/ISIS Interfaces.json', mode='w' ) as f:
                        await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "isisInst" in api:
                async with aiofiles.open('ISIS Instances/JSON/ISIS Instances.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "isisNexthop" in api:
                async with aiofiles.open('ISIS Next Hop/JSON/ISIS Next Hop.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "isisRoute" in api:
                async with aiofiles.open('ISIS Routes/JSON/ISIS Routes.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l2BD" in api:
                async with aiofiles.open('L2 Bridge Domains/JSON/L2 Bridge Domains.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l2ExtIf" in api:
                async with aiofiles.open('L2 External Interfaces/JSON/L2 External Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l2RsEthIf" in api:
                async with aiofiles.open('L2 Interface Source Relationships/JSON/L2 Interface Source Relationships.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l2extInstP" in api:
                async with aiofiles.open('L2 External Instance Profiles/JSON/L2 External Instance Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l2extLIfP" in api:
                async with aiofiles.open('L2 External Logical Interface Profiles/JSON/L2 External Logical Interface Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l2extLNodeP" in api:
                async with aiofiles.open('L2 External Logical Node Profiles/JSON/L2 External Logical Node Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l2extRsEBd" in api:
                async with aiofiles.open('L2 EPG Bridge Domain Source Relationships/JSON/L2 EPG Bridge Domain Source Relationships.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l2extRsPathL2OutAtt" in api:
                async with aiofiles.open('L2Out Paths/JSON/L2Out Paths.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3Ctx" in api:
                async with aiofiles.open('L3 Contexts/JSON/L3 Contexts.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3EncRtdIf" in api:
                async with aiofiles.open('L3 Subinterfaces/JSON/L3 Subinterfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3Inst" in api:
                async with aiofiles.open('L3 Instances/JSON/L3 Instances.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3LbRtdIf" in api:
                async with aiofiles.open('L3 Routed Loopback Interfaces/JSON/L3 Routed Loopback Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3RsEncPhysRtdConf" in api:
                async with aiofiles.open('L3 Physical Interface Source Relationships/JSON/L3 Physical Interface Source Relationships.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3RtdIf" in api:
                async with aiofiles.open('L3 Routed Interfaces/JSON/L3 Routed Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3extInstP" in api:
                async with aiofiles.open('L3Out Profiles/JSON/L3Out Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3extIp" in api:
                async with aiofiles.open('L3Out IP Addresses/JSON/L3Out IP Addresses.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3extLIfP" in api:
                async with aiofiles.open('L3 Logical Interface Profiles/JSON/L3 Logical Interface Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3extLNodeP" in api:
                async with aiofiles.open('L3 Logical Node Profiles/JSON/L3 Logical Node Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3extMember" in api:
                async with aiofiles.open('L3Out Members/JSON/L3Out Members.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3extRsEctx" in api:
                async with aiofiles.open('L3 Contexts Source Relationships/JSON/L3 Contexts Source Relationships.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3extRsL3DomAtt" in api:
                async with aiofiles.open('L3 Domains Source Relationships/JSON/L3 Domains Source Relationships.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3extRsNodeL3OutAtt" in api:
                async with aiofiles.open('L3Out Node Source Relationships/JSON/L3Out Node Source Relationships.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3extRsPathL3OutAtt" in api:
                async with aiofiles.open('L3Out Path Source Relationships/JSON/L3Out Path Source Relationships.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "l3extSubnet" in api:
                async with aiofiles.open('L3 Subnets/JSON/L3 Subnets.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "lacpEntity" in api:
                async with aiofiles.open('LACP Entities/JSON/LACP Entities.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "lacpIf" in api:
                async with aiofiles.open('LACP Interfaces/JSON/LACP Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "lacpInst" in api:
                async with aiofiles.open('LACP Instances/JSON/LACP Instances.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "leqptLooseNode" in api:
                async with aiofiles.open('External Unmanaged Nodes/JSON/External Unmanaged Nodes.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "leqptRsLsNodeToIf" in api:
                async with aiofiles.open('External Unmanaged Nodes Interfaces/JSON/External Unmanaged Nodes Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "lldpAdjEp" in api:
                async with aiofiles.open('LLDP Adjacency Endpoints/JSON/LLDP Adjacency Endpoints.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "lldpEntity" in api:
                async with aiofiles.open('LLDP Entities/JSON/LLDP Entities.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "lldpIf" in api:
                async with aiofiles.open('LLDP Interfaces/JSON/LLDP Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "lldpInst" in api:
                async with aiofiles.open('LLDP Instances/JSON/LLDP Instances.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "mgmtMgmtIf" in api:
                async with aiofiles.open('Management Interfaces/JSON/Management Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ospfAdjEp" in api:
                async with aiofiles.open('OSPF Adjacency Endpoints/JSON/OSPF Adjacency Endpoints.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ospfArea" in api:
                async with aiofiles.open('OSPF Areas/JSON/OSPF Areas.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ospfDb" in api:
                async with aiofiles.open('OSPF Database/JSON/OSPF Database.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ospfDom" in api:
                async with aiofiles.open('OSPF Domains/JSON/OSPF Domains.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ospfEntity" in api:
                async with aiofiles.open('OSPF Entities/JSON/OSPF Entities.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ospfExtP" in api:
                async with aiofiles.open('OSPF External Profiles/JSON/OSPF External Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ospfIf" in api:
                async with aiofiles.open('OSPF Interfaces/JSON/OSPF Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ospfInst" in api:
                async with aiofiles.open('OSPF Instances/JSON/OSPF Instances.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ospfRoute" in api:
                async with aiofiles.open('OSPF Routes/JSON/OSPF Routes.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "ospfUcNexthop" in api:
                async with aiofiles.open('OSPF Unicast Next Hop/JSON/OSPF Unicast Next Hop.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "pcAggrIf" in api:
                async with aiofiles.open('Port Channel Aggregate Interfaces/JSON/Port Channel Aggregate Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "pcRsMbrIfs" in api:
                async with aiofiles.open('Port Channel Member Interfaces/JSON/Port Channel Member Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "sviIf" in api:
                async with aiofiles.open('SVIs/JSON/SVIs.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "tunnelIf" in api:
                async with aiofiles.open('Tunnel Interfaces/JSON/Tunnel Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "uribv4Db" in api:
                async with aiofiles.open('Unicast Route Database/JSON/Unicast Route Database.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "uribv4Dom" in api:
                async with aiofiles.open('Unicast Route Domains/JSON/Unicast Route Domains.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "uribv4Entity" in api:
                async with aiofiles.open('Unicast Route Entities/JSON/Unicast Route Entities.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "uribv4Nexthop" in api:
                async with aiofiles.open('Unicast Route Next Hop/JSON/Unicast Route Next Hop.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "uribv4Route" in api:
                async with aiofiles.open('Unicast Routes/JSON/Unicast Routes.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vlanCktEp" in api:
                async with aiofiles.open('VLAN Endpoint Group Encapsulation/JSON/VLAN Endpoint Group Encapsulation.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vmmCtrlrP" in api:
                async with aiofiles.open('VMM Controller Profiles/JSON/VMM Controller Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vmmDomP" in api:
                async with aiofiles.open('VMM Domain Profiles/JSON/VMM Domain Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vmmProvP" in api:
                async with aiofiles.open('VMM Provider Profiles/JSON/VMM Provider Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vmmUsrAccP" in api:
                async with aiofiles.open('VMM User Profiles/JSON/VMM User Profiles.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vpcDom" in api:
                async with aiofiles.open('VPC Domains/JSON/VPC Domains.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vpcEntity" in api:
                async with aiofiles.open('VPC Entities/JSON/VPC Entities.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vpcIf" in api:
                async with aiofiles.open('VPC Interfaces/JSON/VPC Interfaces.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vpcInst" in api:
                async with aiofiles.open('VPC Instances/JSON/VPC Instances.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vpcRsVpcConf" in api:
                async with aiofiles.open('VPC Configurations/JSON/VPC Configurations.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vzAny" in api:
                async with aiofiles.open('vzAny/JSON/vzAny.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vzFilter" in api:
                async with aiofiles.open('vzFilters/JSON/vzFilters.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vzRsAnyToCons" in api:
                async with aiofiles.open('vzAny To Consumers/JSON/vzAny To Consumers.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vzRsAnyToProv" in api:
                async with aiofiles.open('vzAny To Providers/JSON/vzAny To Providers.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vzRsDenyRule" in api:
                async with aiofiles.open('vzDeny Rules/JSON/vzDeny Rules.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vzRsIf" in api:
                async with aiofiles.open('vzInterface Source Relationships/JSON/vzInterface Source Relationships.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vzRsSubjFiltAtt" in api:
                async with aiofiles.open('Contract Subjects Filter Attributes/JSON/Contract Subjects Filter Attributes.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vzRtCons" in api:
                async with aiofiles.open('Contract Consumers Root/JSON/Contract Consumers Root.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vzRtProv" in api:
                async with aiofiles.open('Contract Providers Root/JSON/Contract Providers Root.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vzRuleOwner" in api:
                async with aiofiles.open('vzRule Owner/JSON/vzRule Owner.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

            if "vzTaboo" in api:
                async with aiofiles.open('vzTaboo/JSON/vzTaboo.json', mode='w' ) as f:
                    await f.write(json.dumps(payload['imdata'], indent=4, sort_keys=True))

    async def yaml_file(self, parsed_json):
        for api, payload in json.loads(parsed_json):
            clean_yaml = yaml.dump(payload, default_flow_style=False)
            if "Tenant" in api:
                async with aiofiles.open('Tenant/YAML/Tenants.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "AEPg" in api:
                async with aiofiles.open('EPGs/YAML/EPGs.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fvBD" in api:
                async with aiofiles.open('Bridge Domains/YAML/Bridge Domains.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fvCtx" in api:
                async with aiofiles.open('Contexts/YAML/Contexts.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "Ap" in api:
                async with aiofiles.open('Application Profiles/YAML/Application Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3extOut" in api:
                async with aiofiles.open('L3Outs/YAML/L3Outs.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l2extOut" in api:
                async with aiofiles.open('L2Outs/YAML/L2Outs.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "topSystem" in api:
                if "?" not in api:
                    async with aiofiles.open('Top System/YAML/Top System.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)

            if "fvSubnet" in api:
                async with aiofiles.open('Subnets/YAML/Subnets.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fvCEp" in api:
                async with aiofiles.open('Endpoints/YAML/Endpoints.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fabricNode" in api:
                async with aiofiles.open('Fabric Nodes/YAML/Fabric Nodes.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l1PhysIf" in api:
                async with aiofiles.open('Physical Interfaces/YAML/Physical Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraAccPortP" in api:
                async with aiofiles.open('Leaf Interface Profiles/YAML/Leaf Interface Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraSpAccPortP" in api:
                async with aiofiles.open('Spine Interface Profiles/YAML/Spine Interface Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraNodeP" in api:
                async with aiofiles.open('Leaf Switch Profiles/YAML/Leaf Switch Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraSpineP" in api:
                async with aiofiles.open('Spine Switch Profiles/YAML/Spine Switch Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fvnsVlanInstP" in api:
                async with aiofiles.open('VLAN Pools/YAML/VLAN Pools.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraAttEntityP" in api:
                async with aiofiles.open('Attachable Access Entity Profiles/YAML/Attachable Access Entity Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vzBrCP" in api:
                async with aiofiles.open('Contracts/YAML/Contracts.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vzEntry" in api:
                async with aiofiles.open('vzEntries/YAML/vzEntries.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "physDomP" in api:
                async with aiofiles.open('Physical Domains/YAML/Physical Domains.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3extDomP" in api:
                async with aiofiles.open('L3 Domains/YAML/L3 Domains.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "qosClass" in api:
                async with aiofiles.open('QOS Classes/YAML/QOS Classes.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "faultSummary" in api:
                async with aiofiles.open('Fault Summary/YAML/Fault Summary.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "aaaModLR" in api:
                async with aiofiles.open('Audit Log/YAML/Audit Log.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fvIp" in api:
                async with aiofiles.open('IP Addresses/YAML/IP Addresses.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eventRecord" in api:
                async with aiofiles.open('Events/YAML/Events.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "licenseEntitlement" in api:
                async with aiofiles.open('License Entitlements/YAML/License Entitlements.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "bgpRRNodePEp" in api:
                async with aiofiles.open('BGP Route Reflectors/YAML/BGP Route Reflectors.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraPortS" in api:
                async with aiofiles.open('Interface Policies/YAML/Interface Policies.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraProfile" in api:
                async with aiofiles.open('Interface Profiles/YAML/Interface Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fabricPod" in api:
                async with aiofiles.open('Fabric Pods/YAML/Fabric Pods.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fabricPath" in api:
                if "fabricPathEp" in api:
                    if "Cont" in api:
                        async with aiofiles.open('Fabric Path Endpoint Containers/YAML/Fabric Path Endpoint Containers.yaml', mode='w' ) as f:
                            await f.write(clean_yaml)
                    else:
                        async with aiofiles.open('Fabric Path Endpoints/YAML/Fabric Path Endpoints.yaml', mode='w' ) as f:
                            await f.write(clean_yaml)
                else:
                    async with aiofiles.open('Fabric Paths/YAML/Fabric Paths.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)

            if "rtctrlSubjP" in api:
                async with aiofiles.open('Prefix List/YAML/Prefix List.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "rtctrlMatchRtDest" in api:
                async with aiofiles.open('Prefix List Detailed/YAML/Prefix List Detailed.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "aaaUser" in api:
                async with aiofiles.open('Users/YAML/Users.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "aaaDomain" in api:
                async with aiofiles.open('Security Domains/YAML/Security Domains.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vzSubj" in api:
                async with aiofiles.open('Contract Subjects/YAML/Contract Subjects.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "topology/health" in api:
                async with aiofiles.open('Health/YAML/Health.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "pkiFabricNodeSSLCertificate" in api:
                async with aiofiles.open('Fabric Node SSL Certificates/YAML/Fabric Node SSL Certificates.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "tn-" in api:
                if "health" in api:
                    async with aiofiles.open('Tenant Health/YAML/Tenant Health.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)

            if "firmwareCtrlrRunning" in api:
                async with aiofiles.open('Fabric Membership/YAML/Fabric Membership.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraWiNode" in api:
                async with aiofiles.open('Cluster Health/YAML/Cluster Health.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vnsMDev" in api:
                async with aiofiles.open('Device Packages/YAML/Device Packages.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "cnwAggrIf" in api:
                async with aiofiles.open('Cluster Aggregate Interfaces/YAML/Cluster Aggregate Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3Inst" in api:
                async with aiofiles.open('L3 Interfaces/YAML/L3 Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "actrlEntity" in api:
                async with aiofiles.open('Access Control Entities/YAML/Access Control Entities.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "actrlInst" in api:
                async with aiofiles.open('Access Control Instances/YAML/Access Control Instances.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "actrlRule" in api:
                async with aiofiles.open('Access Control Rules/YAML/Access Control Rules.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "actrlScope" in api:
                async with aiofiles.open('Access Control Scopes/YAML/Access Control Scopes.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "cnwPhysIf" in api:
                async with aiofiles.open('Cluster Physical Interfaces/YAML/Cluster Physical Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "compCtrlr" in api:
                async with aiofiles.open('Compute Controllers/YAML/Compute Controllers.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "compDom" in api:
                async with aiofiles.open('Compute Domains/YAML/Compute Domains.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "compEpPD" in api:
                async with aiofiles.open('Compute Endpoint Policy Descriptions/YAML/Compute Endpoint Policy Descriptions.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "compProv" in api:
                async with aiofiles.open('Compute Providers/YAML/Compute Providers.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "arpAdjEp" in api:
                async with aiofiles.open('ARP Adjacency Endpoints/YAML/ARP Adjacency Endpoints.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "arpDb" in api:
                async with aiofiles.open('ARP Database/YAML/ARP Database.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "arpDom" in api:
                async with aiofiles.open('ARP Domain/YAML/ARP Domain.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "arpEntity" in api:
                async with aiofiles.open('ARP Entity/YAML/ARP Entity.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "arpIf" in api:
                async with aiofiles.open('ARP Interfaces/YAML/ARP Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "arpInst" in api:
                async with aiofiles.open('ARP Instances/YAML/ARP Instances.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "bgpDom" in api:
                if "Af" in api:
                    async with aiofiles.open('BGP Domain Address Families/YAML/BGP Domain Address Families.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)
                else:
                    async with aiofiles.open('BGP Domains/YAML/BGP Domains.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)

            if "bgpEntity" in api:
                async with aiofiles.open('BGP Entities/YAML/BGP Entities.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "bgpInst" in api:
                if "InstPol" in api:
                    async with aiofiles.open('BGP Instances Policy/YAML/BGP Instances Policy.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)
                else:
                    async with aiofiles.open('BGP Instances/YAML/BGP Instances.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)

            if "bgpPeer" in api:
                if "bgpPeerAf" in api:
                    async with aiofiles.open('BGP Peers AF Entries/YAML/BGP Peers AF Entries.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)
                elif "bgpPeerEntry" in api:
                    async with aiofiles.open('BGP Peers Entries/YAML/BGP Peers Entries.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)
                else:
                    async with aiofiles.open('BGP Peers/YAML/BGP Peers.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)

            if "bgpRRP" in api:
                async with aiofiles.open('BGP Route Reflector Policies/YAML/BGP Route Reflector Policies.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "cdpAdjEp" in api:
                async with aiofiles.open('CDP Adjacency Endpoints/YAML/CDP Adjacency Endpoints.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "cdpEntity" in api:
                async with aiofiles.open('CDP Entities/YAML/CDP Entities.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "cdpIf" in api:
                async with aiofiles.open('CDP Interfaces/YAML/CDP Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "cdpInst" in api:
                async with aiofiles.open('CDP Instances/YAML/CDP Instances.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "cdpIntfAddr" in api:
                async with aiofiles.open('CDP Interface Addresses/YAML/CDP Interface Addresses.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "cdpMgmtAddr" in api:
                async with aiofiles.open('CDP Management Addresses/YAML/CDP Management Addresses.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "cnwRsMbrIfs" in api:
                async with aiofiles.open('Cluster RS Member Interfaces/YAML/Cluster RS Member Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "compRsDomP" in api:
                async with aiofiles.open('Compute RS Domain Policies/YAML/Compute RS Domain Policies.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptBSlot" in api:
                async with aiofiles.open('Equipment Board Slots/YAML/Equipment Board Slots.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptBoard" in api:
                async with aiofiles.open('Equipment Boards/YAML/Equipment Boards.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptCPU" in api:
                async with aiofiles.open('Equipment CPUs/YAML/Equipment CPUs.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptCh" in api:
                async with aiofiles.open('Equipment Chassis/YAML/Equipment Chassis.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptDimm" in api:
                async with aiofiles.open('Equipment DIMMs/YAML/Equipment DIMMs.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptExtCh" in api:
                async with aiofiles.open('Equipment Fabric Extenders/YAML/Equipment Fabric Extenders.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptFabP" in api:
                async with aiofiles.open('Equipment Fabric Ports/YAML/Equipment Fabric Ports.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptFan" in api:
                async with aiofiles.open('Equipment Fans/YAML/Equipment Fans.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptFpga" in api:
                async with aiofiles.open('Equipment Field Programmable Gate Arrays/YAML/Equipment Field Programmable Gate Arrays.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptFt" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Fan Tray Slots/YAML/Equipment Fan Tray Slots.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)
                else:
                    async with aiofiles.open('Equipment Fan Trays/YAML/Equipment Fan Trays.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)

            if "eqptIndLed" in api:
                async with aiofiles.open('Equipment Indicator LEDs/YAML/Equipment Indicator LEDs.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptLC" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Line Card Slots/YAML/Equipment Line Card Slots.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)
                else:
                    async with aiofiles.open('Equipment Line Cards/YAML/Equipment Line Cards.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)

            if "eqptLeafP" in api:
                async with aiofiles.open('Equipment Leaf Ports/YAML/Equipment Leaf Ports.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptLocLed" in api:
                async with aiofiles.open('Equipment Port Locator LEDs/YAML/Equipment Port Locator LEDs.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptPsu" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Power Supply Slots/YAML/Equipment Power Supply Slots.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)
                else:
                    async with aiofiles.open('Equipment Power Supplies/YAML/Equipment Power Supplies.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)

            if "eqptRsIoPPhysConf" in api:
                async with aiofiles.open('Equipment RS IO Port Physical Configs/YAML/Equipment RS IO Port Physical Configs.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptSensor" in api:
                async with aiofiles.open('Equipment Sensors/YAML/Equipment Sensors.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptSpCmnBlk" in api:
                async with aiofiles.open('Equipment SP Common Blocks/YAML/Equipment SP Common Blocks.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptSpromLc" in api:
                async with aiofiles.open('Equipment SPROM LCs/YAML/Equipment SPROM LCs.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptSpromPsu" in api:
                if "Blk" in api:
                    async with aiofiles.open('Equipment SPROM Power Supply Blocks/YAML/Equipment SPROM Power Supply Blocks.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)
                else:            
                    async with aiofiles.open('Equipment SPROM Power Supplies/YAML/Equipment SPROM Power Supplies.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)

            if "eqptSpromSup" in api:
                async with aiofiles.open('Equipment SPROM Supervisors/YAML/Equipment SPROM Supervisors.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptStorage" in api:
                async with aiofiles.open('Equipment Storage/YAML/Equipment Storage.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "eqptSupC" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Supervisor Slots/YAML/Equipment Supervisor Slots.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)
                else:
                    async with aiofiles.open('Equipment Supervisors/YAML/Equipment Supervisors.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)

            if "ethpmPhysIf" in api:
                async with aiofiles.open('Ethernet Port Manager Physical Interfaces/YAML/Ethernet Port Manager Physical Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fabricExtPathEpCont" in api:
                async with aiofiles.open('Fabric Extended Path Endpoint Containers/YAML/Fabric Extended Path Endpoint Containers.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fabricInst" in api:
                async with aiofiles.open('Fabric Instances/YAML/Fabric Instances.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fabricLink" in api:
                if "Cont" in api:
                    async with aiofiles.open('Fabric Link Containers/YAML/Fabric Link Containers.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)
                else:
                    async with aiofiles.open('Fabric Links/YAML/Fabric Links.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)

            if "fabricLooseLink" in api:
                async with aiofiles.open('Fabric Loose Links/YAML/Fabric Loose Links.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fabricLooseNode" in api:
                async with aiofiles.open('Fabric Loose Nodes/YAML/Fabric Loose Nodes.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fabricProtPathEpCont" in api:
                async with aiofiles.open('Fabric Protected Path Endpoint Containers/YAML/Fabric Protected Path Endpoint Containers.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fcEntity" in api:
                async with aiofiles.open('Fibre Channel Entities/YAML/Fibre Channel Entities.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "firmwareCardRunning" in api:
                async with aiofiles.open('Firmware Card Running/YAML/Firmware Card Running.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "firmwareCompRunning" in api:
                async with aiofiles.open('Firmware Compute Running/YAML/Firmware Compute Running.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "firmwareRunning" in api:
                async with aiofiles.open('Firmware Running/YAML/Firmware Running.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fvEpPCont" in api:
                async with aiofiles.open('Endpoint Profile Containers/YAML/Endpoint Profile Containers.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fvLocale" in api:
                async with aiofiles.open('Locales/YAML/Locales.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fvRsBDToOut" in api:
                async with aiofiles.open('Bridge Domains To Outside/YAML/Bridge Domains To Outside.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fvRsBd" in api:
                async with aiofiles.open('EPG Bridge Domain Links/YAML/EPG Bridge Domain Links.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fvRsCEpToPathEp" in api:
                async with aiofiles.open('Endpoints To Paths/YAML/Endpoints To Paths.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fvRsCons" in api:
                if "If" in api:
                    async with aiofiles.open('Contract Consumer Interfaces/YAML/Contract Consumer Interfaces.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)
                else:
                    async with aiofiles.open('Contract Consumers/YAML/Contract Consumers.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)

            if "fvRsCtx" in api:
                async with aiofiles.open('Context Source Relationships/YAML/Context Source Relationships.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fvRsDomAtt" in api:
                async with aiofiles.open('Domain Attachments/YAML/Domain Attachments.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fvRsPathAtt" in api:
                async with aiofiles.open('Path Attachments/YAML/Path Attachments.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fvRsProv" in api:
                async with aiofiles.open('Contract Providers/YAML/Contract Providers.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fvRtBd" in api:
                async with aiofiles.open('Bridge Domains Target Relationships/YAML/Bridge Domains Target Relationships.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fvRtCtx" in api:
                async with aiofiles.open('Contexts Target Relationships/YAML/Contexts Target Relationships.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fvnsEncapBlk" in api:
                async with aiofiles.open('VLAN Encapsulation Blocks/YAML/VLAN Encapsulation Blocks.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "fvnsVlanInstP" in api:
                async with aiofiles.open('VLAN Namespace Policies/YAML/VLAN Namespace Policies.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraAccBndlGrp" in api:
                async with aiofiles.open('Access Bundle Groups/YAML/Access Bundle Groups.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraAccPortGrp" in api:
                async with aiofiles.open('Access Port Groups/YAML/Access Port Groups.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraAccPortP" in api:
                async with aiofiles.open('Access Port Profiles/YAML/Access Port Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraContr" in api:
                async with aiofiles.open('Controllers/YAML/Controllers.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraFexP" in api:
                async with aiofiles.open('FEX Policies/YAML/FEX Policies.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraFuncP" in api:
                async with aiofiles.open('Function Policies/YAML/Function Policies.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraHPortS" in api:
                async with aiofiles.open('Host Port Selectors/YAML/Host Port Selectors.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraPortBlk" in api:
                async with aiofiles.open('Port Blocks/YAML/Port Blocks.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraRsAccBaseGrp" in api:
                async with aiofiles.open('Access Policy Group Source Relationships/YAML/Access Policy Group Source Relationships.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraRsAttEntP" in api:
                async with aiofiles.open('Attachable Access Entity Profiles Source Relationships/YAML/Attachable Access Entity Profiles Source Relationships.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraRsDomP" in api:
                async with aiofiles.open('Domain Profile Source Relationships/YAML/Domain Profile Source Relationships.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraRsSpAccGrp" in api:
                async with aiofiles.open('Spine Access Policy Groups/YAML/Spine Access Policy Groups.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraRsVlanNs" in api:
                async with aiofiles.open('VLAN Namespace Source Relationships/YAML/VLAN Namespace Source Relationships.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraSHPortS" in api:
                async with aiofiles.open('Spine Host Port Selectors/YAML/Spine Host Port Selectors.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraSpAccPortP" in api:
                async with aiofiles.open('Spine Access Port Profiles/YAML/Spine Access Port Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "infraWiNode" in api:
                async with aiofiles.open('Wired Nodes/YAML/Wired Nodes.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ipNexthopP" in api:
                async with aiofiles.open('Static Route Next Hop Policies/YAML/Static Route Next Hop Policies.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ipRouteP" in api:
                async with aiofiles.open('Route Policies/YAML/Route Policies.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ipv4Addr" in api:
                async with aiofiles.open('IPv4 Addresses/YAML/IPv4 Addresses.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ipv4Dom" in api:
                async with aiofiles.open('IPv4 Domains/YAML/IPv4 Domains.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ipv4Entity" in api:
                async with aiofiles.open('IPv4 Entities/YAML/IPv4 Entities.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ipv4If" in api:
                async with aiofiles.open('IPv4 Interfaces/YAML/IPv4 Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ipv4Inst" in api:
                async with aiofiles.open('IPv4 Instances/YAML/IPv4 Instances.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ipv4Nexthop" in api:
                async with aiofiles.open('IPv4 Next Hop/YAML/IPv4 Next Hop.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ipv4Route" in api:
                async with aiofiles.open('IPv4 Routes/YAML/IPv4 Routes.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "isisAdjEp" in api:
                async with aiofiles.open('ISIS Adjacency Endpoints/YAML/ISIS Adjacency Endpoints.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "isisDTEp" in api:
                async with aiofiles.open('ISIS Discovered Tunnel Endpoints/YAML/ISIS Discovered Tunnel Endpoints.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "isisDom" in api:
                if "Lvl" in api:
                    async with aiofiles.open('ISIS Domains Level/YAML/ISIS Domains Level.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)
                else:
                    async with aiofiles.open('ISIS Domains/YAML/ISIS Domains.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)

            if "isisEntity" in api:
                async with aiofiles.open('ISIS Entities/YAML/ISIS Entities.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "isisIf" in api:
                if "Lvl" in api:
                    async with aiofiles.open('ISIS Interfaces Level/YAML/ISIS Interfaces Level.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)
                else:
                    async with aiofiles.open('ISIS Interfaces/YAML/ISIS Interfaces.yaml', mode='w' ) as f:
                        await f.write(clean_yaml)

            if "isisInst" in api:
                async with aiofiles.open('ISIS Instances/YAML/ISIS Instances.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "isisNexthop" in api:
                async with aiofiles.open('ISIS Next Hop/YAML/ISIS Next Hop.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "isisRoute" in api:
                async with aiofiles.open('ISIS Routes/YAML/ISIS Routes.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l2BD" in api:
                async with aiofiles.open('L2 Bridge Domains/YAML/L2 Bridge Domains.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l2ExtIf" in api:
                async with aiofiles.open('L2 External Interfaces/YAML/L2 External Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l2RsEthIf" in api:
                async with aiofiles.open('L2 Interface Source Relationships/YAML/L2 Interface Source Relationships.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l2extInstP" in api:
                async with aiofiles.open('L2 External Instance Profiles/YAML/L2 External Instance Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l2extLIfP" in api:
                async with aiofiles.open('L2 External Logical Interface Profiles/YAML/L2 External Logical Interface Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l2extLNodeP" in api:
                async with aiofiles.open('L2 External Logical Node Profiles/YAML/L2 External Logical Node Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l2extRsEBd" in api:
                async with aiofiles.open('L2 EPG Bridge Domain Source Relationships/YAML/L2 EPG Bridge Domain Source Relationships.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l2extRsPathL2OutAtt" in api:
                async with aiofiles.open('L2Out Paths/YAML/L2Out Paths.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3Ctx" in api:
                async with aiofiles.open('L3 Contexts/YAML/L3 Contexts.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3EncRtdIf" in api:
                async with aiofiles.open('L3 Subinterfaces/YAML/L3 Subinterfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3Inst" in api:
                async with aiofiles.open('L3 Instances/YAML/L3 Instances.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3LbRtdIf" in api:
                async with aiofiles.open('L3 Routed Loopback Interfaces/YAML/L3 Routed Loopback Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3RsEncPhysRtdConf" in api:
                async with aiofiles.open('L3 Physical Interface Source Relationships/YAML/L3 Physical Interface Source Relationships.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3RtdIf" in api:
                async with aiofiles.open('L3 Routed Interfaces/YAML/L3 Routed Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3extInstP" in api:
                async with aiofiles.open('L3Out Profiles/YAML/L3Out Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3extIp" in api:
                async with aiofiles.open('L3Out IP Addresses/YAML/L3Out IP Addresses.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3extLIfP" in api:
                async with aiofiles.open('L3 Logical Interface Profiles/YAML/L3 Logical Interface Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3extLNodeP" in api:
                async with aiofiles.open('L3 Logical Node Profiles/YAML/L3 Logical Node Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3extMember" in api:
                async with aiofiles.open('L3Out Members/YAML/L3Out Members.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3extRsEctx" in api:
                async with aiofiles.open('L3 Contexts Source Relationships/YAML/L3 Contexts Source Relationships.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3extRsL3DomAtt" in api:
                async with aiofiles.open('L3 Domains Source Relationships/YAML/L3 Domains Source Relationships.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3extRsNodeL3OutAtt" in api:
                async with aiofiles.open('L3Out Node Source Relationships/YAML/L3Out Node Source Relationships.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3extRsPathL3OutAtt" in api:
                async with aiofiles.open('L3Out Path Source Relationships/YAML/L3Out Path Source Relationships.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "l3extSubnet" in api:
                async with aiofiles.open('L3 Subnets/YAML/L3 Subnets.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "lacpEntity" in api:
                async with aiofiles.open('LACP Entities/YAML/LACP Entities.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "lacpIf" in api:
                async with aiofiles.open('LACP Interfaces/YAML/LACP Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "lacpInst" in api:
                async with aiofiles.open('LACP Instances/YAML/LACP Instances.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "leqptLooseNode" in api:
                async with aiofiles.open('External Unmanaged Nodes/YAML/External Unmanaged Nodes.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "leqptRsLsNodeToIf" in api:
                async with aiofiles.open('External Unmanaged Nodes Interfaces/YAML/External Unmanaged Nodes Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "lldpAdjEp" in api:
                async with aiofiles.open('LLDP Adjacency Endpoints/YAML/LLDP Adjacency Endpoints.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "lldpEntity" in api:
                async with aiofiles.open('LLDP Entities/YAML/LLDP Entities.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "lldpIf" in api:
                async with aiofiles.open('LLDP Interfaces/YAML/LLDP Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "lldpInst" in api:
                async with aiofiles.open('LLDP Instances/YAML/LLDP Instances.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "mgmtMgmtIf" in api:
                async with aiofiles.open('Management Interfaces/YAML/Management Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ospfAdjEp" in api:
                async with aiofiles.open('OSPF Adjacency Endpoints/YAML/OSPF Adjacency Endpoints.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ospfArea" in api:
                async with aiofiles.open('OSPF Areas/YAML/OSPF Areas.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ospfDb" in api:
                async with aiofiles.open('OSPF Database/YAML/OSPF Database.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ospfDom" in api:
                async with aiofiles.open('OSPF Domains/YAML/OSPF Domains.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ospfEntity" in api:
                async with aiofiles.open('OSPF Entities/YAML/OSPF Entities.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ospfExtP" in api:
                async with aiofiles.open('OSPF External Profiles/YAML/OSPF External Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ospfIf" in api:
                async with aiofiles.open('OSPF Interfaces/YAML/OSPF Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ospfInst" in api:
                async with aiofiles.open('OSPF Instances/YAML/OSPF Instances.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ospfRoute" in api:
                async with aiofiles.open('OSPF Routes/YAML/OSPF Routes.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "ospfUcNexthop" in api:
                async with aiofiles.open('OSPF Unicast Next Hop/YAML/OSPF Unicast Next Hop.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "pcAggrIf" in api:
                async with aiofiles.open('Port Channel Aggregate Interfaces/YAML/Port Channel Aggregate Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "pcRsMbrIfs" in api:
                async with aiofiles.open('Port Channel Member Interfaces/YAML/Port Channel Member Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "sviIf" in api:
                async with aiofiles.open('SVIs/YAML/SVIs.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "tunnelIf" in api:
                async with aiofiles.open('Tunnel Interfaces/YAML/Tunnel Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "uribv4Db" in api:
                async with aiofiles.open('Unicast Route Database/YAML/Unicast Route Database.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "uribv4Dom" in api:
                async with aiofiles.open('Unicast Route Domains/YAML/Unicast Route Domains.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "uribv4Entity" in api:
                async with aiofiles.open('Unicast Route Entities/YAML/Unicast Route Entities.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "uribv4Nexthop" in api:
                async with aiofiles.open('Unicast Route Next Hop/YAML/Unicast Route Next Hop.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "uribv4Route" in api:
                async with aiofiles.open('Unicast Routes/YAML/Unicast Routes.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vlanCktEp" in api:
                async with aiofiles.open('VLAN Endpoint Group Encapsulation/YAML/VLAN Endpoint Group Encapsulation.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vmmCtrlrP" in api:
                async with aiofiles.open('VMM Controller Profiles/YAML/VMM Controller Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vmmDomP" in api:
                async with aiofiles.open('VMM Domain Profiles/YAML/VMM Domain Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vmmProvP" in api:
                async with aiofiles.open('VMM Provider Profiles/YAML/VMM Provider Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vmmUsrAccP" in api:
                async with aiofiles.open('VMM User Profiles/YAML/VMM User Profiles.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vpcDom" in api:
                async with aiofiles.open('VPC Domains/YAML/VPC Domains.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vpcEntity" in api:
                async with aiofiles.open('VPC Entities/YAML/VPC Entities.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vpcIf" in api:
                async with aiofiles.open('VPC Interfaces/YAML/VPC Interfaces.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vpcInst" in api:
                async with aiofiles.open('VPC Instances/YAML/VPC Instances.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vpcRsVpcConf" in api:
                async with aiofiles.open('VPC Configurations/YAML/VPC Configurations.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vzAny" in api:
                async with aiofiles.open('vzAny/YAML/vzAny.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vzFilter" in api:
                async with aiofiles.open('vzFilters/YAML/vzFilters.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vzRsAnyToCons" in api:
                async with aiofiles.open('vzAny To Consumers/YAML/vzAny To Consumers.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vzRsAnyToProv" in api:
                async with aiofiles.open('vzAny To Providers/YAML/vzAny To Providers.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vzRsDenyRule" in api:
                async with aiofiles.open('vzDeny Rules/YAML/vzDeny Rules.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vzRsIf" in api:
                async with aiofiles.open('vzInterface Source Relationships/YAML/vzInterface Source Relationships.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vzRsSubjFiltAtt" in api:
                async with aiofiles.open('Contract Subjects Filter Attributes/YAML/Contract Subjects Filter Attributes.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vzRtCons" in api:
                async with aiofiles.open('Contract Consumers Root/YAML/Contract Consumers Root.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vzRtProv" in api:
                async with aiofiles.open('Contract Providers Root/YAML/Contract Providers Root.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vzRuleOwner" in api:
                async with aiofiles.open('vzRule Owner/YAML/vzRule Owner.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

            if "vzTaboo" in api:
                async with aiofiles.open('vzTaboo/YAML/vzTaboo.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

    async def csv_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        csv_template = env.get_template('aci_csv.j2')
        for api, payload in json.loads(parsed_json):        
            csv_output = await csv_template.render_async(api = api,
                                         data_to_template = payload)
            if "Tenant" in api:
                async with aiofiles.open('Tenant/CSV/Tenants.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "AEPg" in api:
                async with aiofiles.open('EPGs/CSV/EPGs.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fvBD" in api:
                async with aiofiles.open('Bridge Domains/CSV/Bridge Domains.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fvCtx" in api:
                async with aiofiles.open('Contexts/CSV/Contexts.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "Ap" in api:
                async with aiofiles.open('Application Profiles/CSV/Application Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3extOut" in api:
                async with aiofiles.open('L3Outs/CSV/L3Outs.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l2extOut" in api:
                async with aiofiles.open('L2Outs/CSV/L2Outs.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "topSystem" in api:
                if "?" not in api:
                    async with aiofiles.open('Top System/CSV/Top System.csv', mode='w' ) as f:
                        await f.write(csv_output)

            if "fvSubnet" in api:
                async with aiofiles.open('Subnets/CSV/Subnets.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fvCEp" in api:
                async with aiofiles.open('Endpoints/CSV/Endpoints.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fabricNode" in api:
                async with aiofiles.open('Fabric Nodes/CSV/Fabric Nodes.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l1PhysIf" in api:
                async with aiofiles.open('Physical Interfaces/CSV/Physical Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraAccPortP" in api:
                async with aiofiles.open('Leaf Interface Profiles/CSV/Leaf Interface Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraSpAccPortP" in api:
                async with aiofiles.open('Spine Interface Profiles/CSV/Spine Interface Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraNodeP" in api:
                async with aiofiles.open('Leaf Switch Profiles/CSV/Leaf Switch Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraSpineP" in api:
                async with aiofiles.open('Spine Switch Profiles/CSV/Spine Switch Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fvnsVlanInstP" in api:
                async with aiofiles.open('VLAN Pools/CSV/VLAN Pools.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraAttEntityP" in api:
                async with aiofiles.open('Attachable Access Entity Profiles/CSV/Attachable Access Entity Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vzBrCP" in api:
                async with aiofiles.open('Contracts/CSV/Contracts.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vzEntry" in api:
                async with aiofiles.open('vzEntries/CSV/vzEntries.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "physDomP" in api:
                async with aiofiles.open('Physical Domains/CSV/Physical Domains.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3extDomP" in api:
                async with aiofiles.open('L3 Domains/CSV/L3 Domains.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "qosClass" in api:
                async with aiofiles.open('QOS Classes/CSV/QOS Classes.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "faultSummary" in api:
                async with aiofiles.open('Fault Summary/CSV/Fault Summary.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "aaaModLR" in api:
                async with aiofiles.open('Audit Log/CSV/Audit Log.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fvIp" in api:
                async with aiofiles.open('IP Addresses/CSV/IP Addresses.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eventRecord" in api:
                async with aiofiles.open('Events/CSV/Events.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "licenseEntitlement" in api:
                async with aiofiles.open('License Entitlements/CSV/License Entitlements.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "bgpRRNodePEp" in api:
                async with aiofiles.open('BGP Route Reflectors/CSV/BGP Route Reflectors.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraPortS" in api:
                async with aiofiles.open('Interface Policies/CSV/Interface Policies.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraProfile" in api:
                async with aiofiles.open('Interface Profiles/CSV/Interface Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fabricPod" in api:
                async with aiofiles.open('Fabric Pods/CSV/Fabric Pods.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fabricPath" in api:
                if "fabricPathEp" in api:
                    if "Cont" in api:
                        async with aiofiles.open('Fabric Path Endpoint Containers/CSV/Fabric Path Endpoint Containers.csv', mode='w' ) as f:
                            await f.write(csv_output)
                    else:
                        async with aiofiles.open('Fabric Path Endpoints/CSV/Fabric Path Endpoints.csv', mode='w' ) as f:
                            await f.write(csv_output)
                else:
                    async with aiofiles.open('Fabric Paths/CSV/Fabric Paths.csv', mode='w' ) as f:
                        await f.write(csv_output)

            if "rtctrlSubjP" in api:
                async with aiofiles.open('Prefix List/CSV/Prefix List.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "rtctrlMatchRtDest" in api:
                async with aiofiles.open('Prefix List Detailed/CSV/Prefix List Detailed.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "aaaUser" in api:
                async with aiofiles.open('Users/CSV/Users.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "aaaDomain" in api:
                async with aiofiles.open('Security Domains/CSV/Security Domains.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vzSubj" in api:
                async with aiofiles.open('Contract Subjects/CSV/Contract Subjects.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "topology/health" in api:
                async with aiofiles.open('Health/CSV/Health.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "pkiFabricNodeSSLCertificate" in api:
                async with aiofiles.open('Fabric Node SSL Certificates/CSV/Fabric Node SSL Certificates.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "tn-" in api:
                if "health" in api:
                    async with aiofiles.open('Tenant Health/CSV/Tenant Health.csv', mode='w' ) as f:
                        await f.write(csv_output)

            if "firmwareCtrlrRunning" in api:
                async with aiofiles.open('Fabric Membership/CSV/Fabric Membership.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraWiNode" in api:
                async with aiofiles.open('Cluster Health/CSV/Cluster Health.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vnsMDev" in api:
                async with aiofiles.open('Device Packages/CSV/Device Packages.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "cnwAggrIf" in api:
                async with aiofiles.open('Cluster Aggregate Interfaces/CSV/Cluster Aggregate Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3Inst" in api:
                async with aiofiles.open('L3 Interfaces/CSV/L3 Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "actrlEntity" in api:
                async with aiofiles.open('Access Control Entities/CSV/Access Control Entities.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "actrlInst" in api:
                async with aiofiles.open('Access Control Instances/CSV/Access Control Instances.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "actrlRule" in api:
                async with aiofiles.open('Access Control Rules/CSV/Access Control Rules.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "actrlScope" in api:
                async with aiofiles.open('Access Control Scopes/CSV/Access Control Scopes.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "cnwPhysIf" in api:
                async with aiofiles.open('Cluster Physical Interfaces/CSV/Cluster Physical Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "compCtrlr" in api:
                async with aiofiles.open('Compute Controllers/CSV/Compute Controllers.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "compDom" in api:
                async with aiofiles.open('Compute Domains/CSV/Compute Domains.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "compEpPD" in api:
                async with aiofiles.open('Compute Endpoint Policy Descriptions/CSV/Compute Endpoint Policy Descriptions.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "compProv" in api:
                async with aiofiles.open('Compute Providers/CSV/Compute Providers.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "arpAdjEp" in api:
                async with aiofiles.open('ARP Adjacency Endpoints/CSV/ARP Adjacency Endpoints.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "arpDb" in api:
                async with aiofiles.open('ARP Database/CSV/ARP Database.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "arpDom" in api:
                async with aiofiles.open('ARP Domain/CSV/ARP Domain.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "arpEntity" in api:
                async with aiofiles.open('ARP Entity/CSV/ARP Entity.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "arpIf" in api:
                async with aiofiles.open('ARP Interfaces/CSV/ARP Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "arpInst" in api:
                async with aiofiles.open('ARP Instances/CSV/ARP Instances.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "bgpDom" in api:
                if "Af" in api:
                    async with aiofiles.open('BGP Domain Address Families/CSV/BGP Domain Address Families.csv', mode='w' ) as f:
                        await f.write(csv_output)
                else:
                    async with aiofiles.open('BGP Domains/CSV/BGP Domains.csv', mode='w' ) as f:
                        await f.write(csv_output)

            if "bgpEntity" in api:
                async with aiofiles.open('BGP Entities/CSV/BGP Entities.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "bgpInst" in api:
                if "InstPol" in api:
                    async with aiofiles.open('BGP Instances Policy/CSV/BGP Instances Policy.csv', mode='w' ) as f:
                        await f.write(csv_output)
                else:
                    async with aiofiles.open('BGP Instances/CSV/BGP Instances.csv', mode='w' ) as f:
                        await f.write(csv_output)

            if "bgpPeer" in api:
                if "bgpPeerAf" in api:
                    async with aiofiles.open('BGP Peers AF Entries/CSV/BGP Peers AF Entries.csv', mode='w' ) as f:
                        await f.write(csv_output)
                elif "bgpPeerEntry" in api:
                    async with aiofiles.open('BGP Peers Entries/CSV/BGP Peers Entries.csv', mode='w' ) as f:
                        await f.write(csv_output)
                else:
                    async with aiofiles.open('BGP Peers/CSV/BGP Peers.csv', mode='w' ) as f:
                        await f.write(csv_output)

            if "bgpRRP" in api:
                async with aiofiles.open('BGP Route Reflector Policies/CSV/BGP Route Reflector Policies.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "cdpAdjEp" in api:
                async with aiofiles.open('CDP Adjacency Endpoints/CSV/CDP Adjacency Endpoints.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "cdpEntity" in api:
                async with aiofiles.open('CDP Entities/CSV/CDP Entities.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "cdpIf" in api:
                async with aiofiles.open('CDP Interfaces/CSV/CDP Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "cdpInst" in api:
                async with aiofiles.open('CDP Instances/CSV/CDP Instances.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "cdpIntfAddr" in api:
                async with aiofiles.open('CDP Interface Addresses/CSV/CDP Interface Addresses.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "cdpMgmtAddr" in api:
                async with aiofiles.open('CDP Management Addresses/CSV/CDP Management Addresses.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "cnwRsMbrIfs" in api:
                async with aiofiles.open('Cluster RS Member Interfaces/CSV/Cluster RS Member Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "compRsDomP" in api:
                async with aiofiles.open('Compute RS Domain Policies/CSV/Compute RS Domain Policies.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptBSlot" in api:
                async with aiofiles.open('Equipment Board Slots/CSV/Equipment Board Slots.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptBoard" in api:
                async with aiofiles.open('Equipment Boards/CSV/Equipment Boards.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptCPU" in api:
                async with aiofiles.open('Equipment CPUs/CSV/Equipment CPUs.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptCh" in api:
                async with aiofiles.open('Equipment Chassis/CSV/Equipment Chassis.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptDimm" in api:
                async with aiofiles.open('Equipment DIMMs/CSV/Equipment DIMMs.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptExtCh" in api:
                async with aiofiles.open('Equipment Fabric Extenders/CSV/Equipment Fabric Extenders.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptFabP" in api:
                async with aiofiles.open('Equipment Fabric Ports/CSV/Equipment Fabric Ports.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptFan" in api:
                async with aiofiles.open('Equipment Fans/CSV/Equipment Fans.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptFpga" in api:
                async with aiofiles.open('Equipment Field Programmable Gate Arrays/CSV/Equipment Field Programmable Gate Arrays.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptFt" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Fan Tray Slots/CSV/Equipment Fan Tray Slots.csv', mode='w' ) as f:
                        await f.write(csv_output)
                else:
                    async with aiofiles.open('Equipment Fan Trays/CSV/Equipment Fan Trays.csv', mode='w' ) as f:
                        await f.write(csv_output)

            if "eqptIndLed" in api:
                async with aiofiles.open('Equipment Indicator LEDs/CSV/Equipment Indicator LEDs.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptLC" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Line Card Slots/CSV/Equipment Line Card Slots.csv', mode='w' ) as f:
                        await f.write(csv_output)
                else:
                    async with aiofiles.open('Equipment Line Cards/CSV/Equipment Line Cards.csv', mode='w' ) as f:
                        await f.write(csv_output)

            if "eqptLeafP" in api:
                async with aiofiles.open('Equipment Leaf Ports/CSV/Equipment Leaf Ports.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptLocLed" in api:
                async with aiofiles.open('Equipment Port Locator LEDs/CSV/Equipment Port Locator LEDs.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptPsu" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Power Supply Slots/CSV/Equipment Power Supply Slots.csv', mode='w' ) as f:
                        await f.write(csv_output)
                else:
                    async with aiofiles.open('Equipment Power Supplies/CSV/Equipment Power Supplies.csv', mode='w' ) as f:
                        await f.write(csv_output)

            if "eqptRsIoPPhysConf" in api:
                async with aiofiles.open('Equipment RS IO Port Physical Configs/CSV/Equipment RS IO Port Physical Configs.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptSensor" in api:
                async with aiofiles.open('Equipment Sensors/CSV/Equipment Sensors.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptSpCmnBlk" in api:
                async with aiofiles.open('Equipment SP Common Blocks/CSV/Equipment SP Common Blocks.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptSpromLc" in api:
                async with aiofiles.open('Equipment SPROM LCs/CSV/Equipment SPROM LCs.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptSpromPsu" in api:
                if "Blk" in api:
                    async with aiofiles.open('Equipment SPROM Power Supply Blocks/CSV/Equipment SPROM Power Supply Blocks.csv', mode='w' ) as f:
                        await f.write(csv_output)
                else:
                    async with aiofiles.open('Equipment SPROM Power Supplies/CSV/Equipment SPROM Power Supplies.csv', mode='w' ) as f:
                        await f.write(csv_output)

            if "eqptSpromSup" in api:
                async with aiofiles.open('Equipment SPROM Supervisors/CSV/Equipment SPROM Supervisors.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptStorage" in api:
                async with aiofiles.open('Equipment Storage/CSV/Equipment Storage.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "eqptSupC" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Supervisor Slots/CSV/Equipment Supervisor Slots.csv', mode='w' ) as f:
                        await f.write(csv_output)
                else:
                    async with aiofiles.open('Equipment Supervisors/CSV/Equipment Supervisors.csv', mode='w' ) as f:
                        await f.write(csv_output)

            if "ethpmPhysIf" in api:
                async with aiofiles.open('Ethernet Port Manager Physical Interfaces/CSV/Ethernet Port Manager Physical Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fabricExtPathEpCont" in api:
                async with aiofiles.open('Fabric Extended Path Endpoint Containers/CSV/Fabric Extended Path Endpoint Containers.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fabricInst" in api:
                async with aiofiles.open('Fabric Instances/CSV/Fabric Instances.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fabricLink" in api:
                if "Cont" in api:
                    async with aiofiles.open('Fabric Link Containers/CSV/Fabric Link Containers.csv', mode='w' ) as f:
                        await f.write(csv_output)
                else:
                    async with aiofiles.open('Fabric Links/CSV/Fabric Links.csv', mode='w' ) as f:
                        await f.write(csv_output)

            if "fabricLooseLink" in api:
                async with aiofiles.open('Fabric Loose Links/CSV/Fabric Loose Links.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fabricLooseNode" in api:
                async with aiofiles.open('Fabric Loose Nodes/CSV/Fabric Loose Nodes.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fabricProtPathEpCont" in api:
                async with aiofiles.open('Fabric Protected Path Endpoint Containers/CSV/Fabric Protected Path Endpoint Containers.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fcEntity" in api:
                async with aiofiles.open('Fibre Channel Entities/CSV/Fibre Channel Entities.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "firmwareCardRunning" in api:
                async with aiofiles.open('Firmware Card Running/CSV/Firmware Card Running.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "firmwareCompRunning" in api:
                async with aiofiles.open('Firmware Compute Running/CSV/Firmware Compute Running.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "firmwareRunning" in api:
                async with aiofiles.open('Firmware Running/CSV/Firmware Running.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fvEpPCont" in api:
                async with aiofiles.open('Endpoint Profile Containers/CSV/Endpoint Profile Containers.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fvLocale" in api:
                async with aiofiles.open('Locales/CSV/Locales.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fvRsBDToOut" in api:
                async with aiofiles.open('Bridge Domains To Outside/CSV/Bridge Domains To Outside.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fvRsBd" in api:
                async with aiofiles.open('EPG Bridge Domain Links/CSV/EPG Bridge Domain Links.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fvRsCEpToPathEp" in api:
                async with aiofiles.open('Endpoints To Paths/CSV/Endpoints To Paths.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fvRsCons" in api:
                if "If" in api:
                    async with aiofiles.open('Contract Consumer Interfaces/CSV/Contract Consumer Interfaces.csv', mode='w' ) as f:
                        await f.write(csv_output)
                else:
                    async with aiofiles.open('Contract Consumers/CSV/Contract Consumers.csv', mode='w' ) as f:
                        await f.write(csv_output)

            if "fvRsCtx" in api:
                async with aiofiles.open('Context Source Relationships/CSV/Context Source Relationships.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fvRsDomAtt" in api:
                async with aiofiles.open('Domain Attachments/CSV/Domain Attachments.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fvRsPathAtt" in api:
                async with aiofiles.open('Path Attachments/CSV/Path Attachments.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fvRsProv" in api:
                async with aiofiles.open('Contract Providers/CSV/Contract Providers.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fvRtBd" in api:
                async with aiofiles.open('Bridge Domains Target Relationships/CSV/Bridge Domains Target Relationships.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fvRtCtx" in api:
                async with aiofiles.open('Contexts Target Relationships/CSV/Contexts Target Relationships.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fvnsEncapBlk" in api:
                async with aiofiles.open('VLAN Encapsulation Blocks/CSV/VLAN Encapsulation Blocks.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "fvnsVlanInstP" in api:
                async with aiofiles.open('VLAN Namespace Policies/CSV/VLAN Namespace Policies.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraAccBndlGrp" in api:
                async with aiofiles.open('Access Bundle Groups/CSV/Access Bundle Groups.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraAccPortGrp" in api:
                async with aiofiles.open('Access Port Groups/CSV/Access Port Groups.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraAccPortP" in api:
                async with aiofiles.open('Access Port Profiles/CSV/Access Port Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraContr" in api:
                async with aiofiles.open('Controllers/CSV/Controllers.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraFexP" in api:
                async with aiofiles.open('FEX Policies/CSV/FEX Policies.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraFuncP" in api:
                async with aiofiles.open('Function Policies/CSV/Function Policies.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraHPortS" in api:
                async with aiofiles.open('Host Port Selectors/CSV/Host Port Selectors.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraPortBlk" in api:
                async with aiofiles.open('Port Blocks/CSV/Port Blocks.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraRsAccBaseGrp" in api:
                async with aiofiles.open('Access Policy Group Source Relationships/CSV/Access Policy Group Source Relationships.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraRsAttEntP" in api:
                async with aiofiles.open('Attachable Access Entity Profiles Source Relationships/CSV/Attachable Access Entity Profiles Source Relationships.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraRsDomP" in api:
                async with aiofiles.open('Domain Profile Source Relationships/CSV/Domain Profile Source Relationships.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraRsSpAccGrp" in api:
                async with aiofiles.open('Spine Access Policy Groups/CSV/Spine Access Policy Groups.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraRsVlanNs" in api:
                async with aiofiles.open('VLAN Namespace Source Relationships/CSV/VLAN Namespace Source Relationships.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraSHPortS" in api:
                async with aiofiles.open('Spine Host Port Selectors/CSV/Spine Host Port Selectors.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraSpAccPortP" in api:
                async with aiofiles.open('Spine Access Port Profiles/CSV/Spine Access Port Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "infraWiNode" in api:
                async with aiofiles.open('Wired Nodes/CSV/Wired Nodes.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ipNexthopP" in api:
                async with aiofiles.open('Static Route Next Hop Policies/CSV/Static Route Next Hop Policies.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ipRouteP" in api:
                async with aiofiles.open('Route Policies/CSV/Route Policies.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ipv4Addr" in api:
                async with aiofiles.open('IPv4 Addresses/CSV/IPv4 Addresses.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ipv4Dom" in api:
                async with aiofiles.open('IPv4 Domains/CSV/IPv4 Domains.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ipv4Entity" in api:
                async with aiofiles.open('IPv4 Entities/CSV/IPv4 Entities.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ipv4If" in api:
                async with aiofiles.open('IPv4 Interfaces/CSV/IPv4 Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ipv4Inst" in api:
                async with aiofiles.open('IPv4 Instances/CSV/IPv4 Instances.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ipv4Nexthop" in api:
                async with aiofiles.open('IPv4 Next Hop/CSV/IPv4 Next Hop.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ipv4Route" in api:
                async with aiofiles.open('IPv4 Routes/CSV/IPv4 Routes.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "isisAdjEp" in api:
                async with aiofiles.open('ISIS Adjacency Endpoints/CSV/ISIS Adjacency Endpoints.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "isisDTEp" in api:
                async with aiofiles.open('ISIS Discovered Tunnel Endpoints/CSV/ISIS Discovered Tunnel Endpoints.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "isisDom" in api:
                if "Lvl" in api:
                    async with aiofiles.open('ISIS Domains Level/CSV/ISIS Domains Level.csv', mode='w' ) as f:
                        await f.write(csv_output)
                else:
                    async with aiofiles.open('ISIS Domains/CSV/ISIS Domains.csv', mode='w' ) as f:
                        await f.write(csv_output)

            if "isisEntity" in api:
                async with aiofiles.open('ISIS Entities/CSV/ISIS Entities.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "isisIf" in api:
                if "Lvl" in api:
                    async with aiofiles.open('ISIS Interfaces Level/CSV/ISIS Interfaces Level.csv', mode='w' ) as f:
                        await f.write(csv_output)
                else:
                    async with aiofiles.open('ISIS Interfaces/CSV/ISIS Interfaces.csv', mode='w' ) as f:
                        await f.write(csv_output)

            if "isisInst" in api:
                async with aiofiles.open('ISIS Instances/CSV/ISIS Instances.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "isisNexthop" in api:
                async with aiofiles.open('ISIS Next Hop/CSV/ISIS Next Hop.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "isisRoute" in api:
                async with aiofiles.open('ISIS Routes/CSV/ISIS Routes.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l2BD" in api:
                async with aiofiles.open('L2 Bridge Domains/CSV/L2 Bridge Domains.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l2ExtIf" in api:
                async with aiofiles.open('L2 External Interfaces/CSV/L2 External Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l2RsEthIf" in api:
                async with aiofiles.open('L2 Interface Source Relationships/CSV/L2 Interface Source Relationships.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l2extInstP" in api:
                async with aiofiles.open('L2 External Instance Profiles/CSV/L2 External Instance Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l2extLIfP" in api:
                async with aiofiles.open('L2 External Logical Interface Profiles/CSV/L2 External Logical Interface Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l2extLNodeP" in api:
                async with aiofiles.open('L2 External Logical Node Profiles/CSV/L2 External Logical Node Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l2extRsEBd" in api:
                async with aiofiles.open('L2 EPG Bridge Domain Source Relationships/CSV/L2 EPG Bridge Domain Source Relationships.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l2extRsPathL2OutAtt" in api:
                async with aiofiles.open('L2Out Paths/CSV/L2Out Paths.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3Ctx" in api:
                async with aiofiles.open('L3 Contexts/CSV/L3 Contexts.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3EncRtdIf" in api:
                async with aiofiles.open('L3 Subinterfaces/CSV/L3 Subinterfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3Inst" in api:
                async with aiofiles.open('L3 Instances/CSV/L3 Instances.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3LbRtdIf" in api:
                async with aiofiles.open('L3 Routed Loopback Interfaces/CSV/L3 Routed Loopback Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3RsEncPhysRtdConf" in api:
                async with aiofiles.open('L3 Physical Interface Source Relationships/CSV/L3 Physical Interface Source Relationships.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3RtdIf" in api:
                async with aiofiles.open('L3 Routed Interfaces/CSV/L3 Routed Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3extInstP" in api:
                async with aiofiles.open('L3Out Profiles/CSV/L3Out Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3extIp" in api:
                async with aiofiles.open('L3Out IP Addresses/CSV/L3Out IP Addresses.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3extLIfP" in api:
                async with aiofiles.open('L3 Logical Interface Profiles/CSV/L3 Logical Interface Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3extLNodeP" in api:
                async with aiofiles.open('L3 Logical Node Profiles/CSV/L3 Logical Node Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3extMember" in api:
                async with aiofiles.open('L3Out Members/CSV/L3Out Members.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3extRsEctx" in api:
                async with aiofiles.open('L3 Contexts Source Relationships/CSV/L3 Contexts Source Relationships.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3extRsL3DomAtt" in api:
                async with aiofiles.open('L3 Domains Source Relationships/CSV/L3 Domains Source Relationships.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3extRsNodeL3OutAtt" in api:
                async with aiofiles.open('L3Out Node Source Relationships/CSV/L3Out Node Source Relationships.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3extRsPathL3OutAtt" in api:
                async with aiofiles.open('L3Out Path Source Relationships/CSV/L3Out Path Source Relationships.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "l3extSubnet" in api:
                async with aiofiles.open('L3 Subnets/CSV/L3 Subnets.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "lacpEntity" in api:
                async with aiofiles.open('LACP Entities/CSV/LACP Entities.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "lacpIf" in api:
                async with aiofiles.open('LACP Interfaces/CSV/LACP Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "lacpInst" in api:
                async with aiofiles.open('LACP Instances/CSV/LACP Instances.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "leqptLooseNode" in api:
                async with aiofiles.open('External Unmanaged Nodes/CSV/External Unmanaged Nodes.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "leqptRsLsNodeToIf" in api:
                async with aiofiles.open('External Unmanaged Nodes Interfaces/CSV/External Unmanaged Nodes Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "lldpAdjEp" in api:
                async with aiofiles.open('LLDP Adjacency Endpoints/CSV/LLDP Adjacency Endpoints.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "lldpEntity" in api:
                async with aiofiles.open('LLDP Entities/CSV/LLDP Entities.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "lldpIf" in api:
                async with aiofiles.open('LLDP Interfaces/CSV/LLDP Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "lldpInst" in api:
                async with aiofiles.open('LLDP Instances/CSV/LLDP Instances.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "mgmtMgmtIf" in api:
                async with aiofiles.open('Management Interfaces/CSV/Management Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ospfAdjEp" in api:
                async with aiofiles.open('OSPF Adjacency Endpoints/CSV/OSPF Adjacency Endpoints.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ospfArea" in api:
                async with aiofiles.open('OSPF Areas/CSV/OSPF Areas.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ospfDb" in api:
                async with aiofiles.open('OSPF Database/CSV/OSPF Database.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ospfDom" in api:
                async with aiofiles.open('OSPF Domains/CSV/OSPF Domains.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ospfEntity" in api:
                async with aiofiles.open('OSPF Entities/CSV/OSPF Entities.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ospfExtP" in api:
                async with aiofiles.open('OSPF External Profiles/CSV/OSPF External Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ospfIf" in api:
                async with aiofiles.open('OSPF Interfaces/CSV/OSPF Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ospfInst" in api:
                async with aiofiles.open('OSPF Instances/CSV/OSPF Instances.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ospfRoute" in api:
                async with aiofiles.open('OSPF Routes/CSV/OSPF Routes.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "ospfUcNexthop" in api:
                async with aiofiles.open('OSPF Unicast Next Hop/CSV/OSPF Unicast Next Hop.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "pcAggrIf" in api:
                async with aiofiles.open('Port Channel Aggregate Interfaces/CSV/Port Channel Aggregate Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "pcRsMbrIfs" in api:
                async with aiofiles.open('Port Channel Member Interfaces/CSV/Port Channel Member Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "sviIf" in api:
                async with aiofiles.open('SVIs/CSV/SVIs.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "tunnelIf" in api:
                async with aiofiles.open('Tunnel Interfaces/CSV/Tunnel Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "uribv4Db" in api:
                async with aiofiles.open('Unicast Route Database/CSV/Unicast Route Database.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "uribv4Dom" in api:
                async with aiofiles.open('Unicast Route Domains/CSV/Unicast Route Domains.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "uribv4Entity" in api:
                async with aiofiles.open('Unicast Route Entities/CSV/Unicast Route Entities.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "uribv4Nexthop" in api:
                async with aiofiles.open('Unicast Route Next Hop/CSV/Unicast Route Next Hop.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "uribv4Route" in api:
                async with aiofiles.open('Unicast Routes/CSV/Unicast Routes.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vlanCktEp" in api:
                async with aiofiles.open('VLAN Endpoint Group Encapsulation/CSV/VLAN Endpoint Group Encapsulation.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vmmCtrlrP" in api:
                async with aiofiles.open('VMM Controller Profiles/CSV/VMM Controller Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vmmDomP" in api:
                async with aiofiles.open('VMM Domain Profiles/CSV/VMM Domain Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vmmProvP" in api:
                async with aiofiles.open('VMM Provider Profiles/CSV/VMM Provider Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vmmUsrAccP" in api:
                async with aiofiles.open('VMM User Profiles/CSV/VMM User Profiles.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vpcDom" in api:
                async with aiofiles.open('VPC Domains/CSV/VPC Domains.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vpcEntity" in api:
                async with aiofiles.open('VPC Entities/CSV/VPC Entities.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vpcIf" in api:
                async with aiofiles.open('VPC Interfaces/CSV/VPC Interfaces.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vpcInst" in api:
                async with aiofiles.open('VPC Instances/CSV/VPC Instances.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vpcRsVpcConf" in api:
                async with aiofiles.open('VPC Configurations/CSV/VPC Configurations.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vzAny" in api:
                async with aiofiles.open('vzAny/CSV/vzAny.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vzFilter" in api:
                async with aiofiles.open('vzFilters/CSV/vzFilters.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vzRsAnyToCons" in api:
                async with aiofiles.open('vzAny To Consumers/CSV/vzAny To Consumers.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vzRsAnyToProv" in api:
                async with aiofiles.open('vzAny To Providers/CSV/vzAny To Providers.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vzRsDenyRule" in api:
                async with aiofiles.open('vzDeny Rules/CSV/vzDeny Rules.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vzRsIf" in api:
                async with aiofiles.open('vzInterface Source Relationships/CSV/vzInterface Source Relationships.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vzRsSubjFiltAtt" in api:
                async with aiofiles.open('Contract Subjects Filter Attributes/CSV/Contract Subjects Filter Attributes.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vzRtCons" in api:
                async with aiofiles.open('Contract Consumers Root/CSV/Contract Consumers Root.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vzRtProv" in api:
                async with aiofiles.open('Contract Providers Root/CSV/Contract Providers Root.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vzRuleOwner" in api:
                async with aiofiles.open('vzRule Owner/CSV/vzRule Owner.csv', mode='w' ) as f:
                    await f.write(csv_output)

            if "vzTaboo" in api:
                async with aiofiles.open('vzTaboo/CSV/vzTaboo.csv', mode='w' ) as f:
                    await f.write(csv_output)

    async def markdown_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        markdown_template = env.get_template('aci_markdown.j2')
        for api, payload in json.loads(parsed_json):        
            markdown_output = await markdown_template.render_async(api = api,
                                         data_to_template = payload)
            if "Tenant" in api:
                async with aiofiles.open('Tenant/CSV/Tenants.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "AEPg" in api:
                async with aiofiles.open('EPGs/Markdown/EPGs.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fvBD" in api:
                async with aiofiles.open('Bridge Domains/Markdown/Bridge Domains.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fvCtx" in api:
                async with aiofiles.open('Contexts/Markdown/Contexts.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "Ap" in api:
                async with aiofiles.open('Application Profiles/Markdown/Application Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3extOut" in api:
                async with aiofiles.open('L3Outs/Markdown/L3Outs.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l2extOut" in api:
                async with aiofiles.open('L2Outs/Markdown/L2Outs.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "topSystem" in api:
                if "?" not in api:
                    async with aiofiles.open('Top System/Markdown/Top System.md', mode='w' ) as f:
                        await f.write(markdown_output)

            if "fvSubnet" in api:
                async with aiofiles.open('Subnets/Markdown/Subnets.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fvCEp" in api:
                async with aiofiles.open('Endpoints/Markdown/Endpoints.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fabricNode" in api:
                async with aiofiles.open('Fabric Nodes/Markdown/Fabric Nodes.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l1PhysIf" in api:
                async with aiofiles.open('Physical Interfaces/Markdown/Physical Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraAccPortP" in api:
                async with aiofiles.open('Leaf Interface Profiles/Markdown/Leaf Interface Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraSpAccPortP" in api:
                async with aiofiles.open('Spine Interface Profiles/Markdown/Spine Interface Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraNodeP" in api:
                async with aiofiles.open('Leaf Switch Profiles/Markdown/Leaf Switch Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraSpineP" in api:
                async with aiofiles.open('Spine Switch Profiles/Markdown/Spine Switch Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fvnsVlanInstP" in api:
                async with aiofiles.open('VLAN Pools/Markdown/VLAN Pools.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraAttEntityP" in api:
                async with aiofiles.open('Attachable Access Entity Profiles/Markdown/Attachable Access Entity Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vzBrCP" in api:
                async with aiofiles.open('Contracts/Markdown/Contracts.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vzEntry" in api:
                async with aiofiles.open('vzEntries/Markdown/vzEntries.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "physDomP" in api:
                async with aiofiles.open('Physical Domains/Markdown/Physical Domains.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3extDomP" in api:
                async with aiofiles.open('L3 Domains/Markdown/L3 Domains.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "qosClass" in api:
                async with aiofiles.open('QOS Classes/Markdown/QOS Classes.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "faultSummary" in api:
                async with aiofiles.open('Fault Summary/Markdown/Fault Summary.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "aaaModLR" in api:
                async with aiofiles.open('Audit Log/Markdown/Audit Log.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fvIp" in api:
                async with aiofiles.open('IP Addresses/Markdown/IP Addresses.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eventRecord" in api:
                async with aiofiles.open('Events/Markdown/Events.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "licenseEntitlement" in api:
                async with aiofiles.open('License Entitlements/Markdown/License Entitlements.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "bgpRRNodePEp" in api:
                async with aiofiles.open('BGP Route Reflectors/Markdown/BGP Route Reflectors.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraPortS" in api:
                async with aiofiles.open('Interface Policies/Markdown/Interface Policies.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraProfile" in api:
                async with aiofiles.open('Interface Profiles/Markdown/Interface Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fabricPod" in api:
                async with aiofiles.open('Fabric Pods/Markdown/Fabric Pods.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fabricPath" in api:
                if "fabricPathEp" in api:
                    if "Cont" in api:
                        async with aiofiles.open('Fabric Path Endpoint Containers/Markdown/Fabric Path Endpoint Containers.md', mode='w' ) as f:
                            await f.write(markdown_output)
                    else:
                        async with aiofiles.open('Fabric Path Endpoints/Markdown/Fabric Path Endpoints.md', mode='w' ) as f:
                            await f.write(markdown_output)
                else:
                    async with aiofiles.open('Fabric Paths/Markdown/Fabric Paths.md', mode='w' ) as f:
                        await f.write(markdown_output)

            if "rtctrlSubjP" in api:
                async with aiofiles.open('Prefix List/Markdown/Prefix List.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "rtctrlMatchRtDest" in api:
                async with aiofiles.open('Prefix List Detailed/Markdown/Prefix List Detailed.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "aaaUser" in api:
                async with aiofiles.open('Users/Markdown/Users.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "aaaDomain" in api:
                async with aiofiles.open('Security Domains/Markdown/Security Domains.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vzSubj" in api:
                async with aiofiles.open('Contract Subjects/Markdown/Contract Subjects.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "topology/health" in api:
                async with aiofiles.open('Health/Markdown/Health.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "pkiFabricNodeSSLCertificate" in api:
                async with aiofiles.open('Fabric Node SSL Certificates/Markdown/Fabric Node SSL Certificates.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "tn-" in api:
                if "health" in api:
                    async with aiofiles.open('Tenant Health/Markdown/Tenant Health.md', mode='w' ) as f:
                        await f.write(markdown_output)

            if "firmwareCtrlrRunning" in api:
                async with aiofiles.open('Fabric Membership/Markdown/Fabric Membership.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraWiNode" in api:
                async with aiofiles.open('Cluster Health/Markdown/Cluster Health.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vnsMDev" in api:
                async with aiofiles.open('Device Packages/Markdown/Device Packages.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "cnwAggrIf" in api:
                async with aiofiles.open('Cluster Aggregate Interfaces/Markdown/Cluster Aggregate Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3Inst" in api:
                async with aiofiles.open('L3 Interfaces/Markdown/L3 Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "actrlEntity" in api:
                async with aiofiles.open('Access Control Entities/Markdown/Access Control Entities.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "actrlInst" in api:
                async with aiofiles.open('Access Control Instances/Markdown/Access Control Instances.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "actrlRule" in api:
                async with aiofiles.open('Access Control Rules/Markdown/Access Control Rules.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "actrlScope" in api:
                async with aiofiles.open('Access Control Scopes/Markdown/Access Control Scopes.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "cnwPhysIf" in api:
                async with aiofiles.open('Cluster Physical Interfaces/Markdown/Cluster Physical Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "compCtrlr" in api:
                async with aiofiles.open('Compute Controllers/Markdown/Compute Controllers.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "compDom" in api:
                async with aiofiles.open('Compute Domains/Markdown/Compute Domains.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "compEpPD" in api:
                async with aiofiles.open('Compute Endpoint Policy Descriptions/Markdown/Compute Endpoint Policy Descriptions.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "compProv" in api:
                async with aiofiles.open('Compute Providers/Markdown/Compute Providers.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "arpAdjEp" in api:
                async with aiofiles.open('ARP Adjacency Endpoints/Markdown/ARP Adjacency Endpoints.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "arpDb" in api:
                async with aiofiles.open('ARP Database/Markdown/ARP Database.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "arpDom" in api:
                async with aiofiles.open('ARP Domain/Markdown/ARP Domain.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "arpEntity" in api:
                async with aiofiles.open('ARP Entity/Markdown/ARP Entity.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "arpIf" in api:
                async with aiofiles.open('ARP Interfaces/Markdown/ARP Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "arpInst" in api:
                async with aiofiles.open('ARP Instances/Markdown/ARP Instances.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "bgpDom" in api:
                if "Af" in api:
                    async with aiofiles.open('BGP Domain Address Families/Markdown/BGP Domain Address Families.md', mode='w' ) as f:
                        await f.write(markdown_output)
                else:
                    async with aiofiles.open('BGP Domains/Markdown/BGP Domains.md', mode='w' ) as f:
                        await f.write(markdown_output)

            if "bgpEntity" in api:
                async with aiofiles.open('BGP Entities/Markdown/BGP Entities.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "bgpInst" in api:
                if "InstPol" in api:
                    async with aiofiles.open('BGP Instances Policy/Markdown/BGP Instances Policy.md', mode='w' ) as f:
                        await f.write(markdown_output)
                else:
                    async with aiofiles.open('BGP Instances/Markdown/BGP Instances.md', mode='w' ) as f:
                        await f.write(markdown_output)

            if "bgpPeer" in api:
                if "bgpPeerAf" in api:
                    async with aiofiles.open('BGP Peers AF Entries/Markdown/BGP Peers AF Entries.md', mode='w' ) as f:
                        await f.write(markdown_output)
                elif "bgpPeerEntry" in api:
                    async with aiofiles.open('BGP Peers Entries/Markdown/BGP Peers Entries.md', mode='w' ) as f:
                        await f.write(markdown_output)
                else:
                    async with aiofiles.open('BGP Peers/Markdown/BGP Peers.md', mode='w' ) as f:
                        await f.write(markdown_output)

            if "bgpRRP" in api:
                async with aiofiles.open('BGP Route Reflector Policies/Markdown/BGP Route Reflector Policies.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "cdpAdjEp" in api:
                async with aiofiles.open('CDP Adjacency Endpoints/Markdown/CDP Adjacency Endpoints.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "cdpEntity" in api:
                async with aiofiles.open('CDP Entities/Markdown/CDP Entities.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "cdpIf" in api:
                async with aiofiles.open('CDP Interfaces/Markdown/CDP Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "cdpInst" in api:
                async with aiofiles.open('CDP Instances/Markdown/CDP Instances.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "cdpIntfAddr" in api:
                async with aiofiles.open('CDP Interface Addresses/Markdown/CDP Interface Addresses.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "cdpMgmtAddr" in api:
                async with aiofiles.open('CDP Management Addresses/Markdown/CDP Management Addresses.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "cnwRsMbrIfs" in api:
                async with aiofiles.open('Cluster RS Member Interfaces/Markdown/Cluster RS Member Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "compRsDomP" in api:
                async with aiofiles.open('Compute RS Domain Policies/Markdown/Compute RS Domain Policies.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptBSlot" in api:
                async with aiofiles.open('Equipment Board Slots/Markdown/Equipment Board Slots.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptBoard" in api:
                async with aiofiles.open('Equipment Boards/Markdown/Equipment Boards.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptCPU" in api:
                async with aiofiles.open('Equipment CPUs/Markdown/Equipment CPUs.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptCh" in api:
                async with aiofiles.open('Equipment Chassis/Markdown/Equipment Chassis.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptDimm" in api:
                async with aiofiles.open('Equipment DIMMs/Markdown/Equipment DIMMs.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptExtCh" in api:
                async with aiofiles.open('Equipment Fabric Extenders/Markdown/Equipment Fabric Extenders.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptFabP" in api:
                async with aiofiles.open('Equipment Fabric Ports/Markdown/Equipment Fabric Ports.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptFan" in api:
                async with aiofiles.open('Equipment Fans/Markdown/Equipment Fans.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptFpga" in api:
                async with aiofiles.open('Equipment Field Programmable Gate Arrays/Markdown/Equipment Field Programmable Gate Arrays.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptFt" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Fan Tray Slots/Markdown/Equipment Fan Tray Slots.md', mode='w' ) as f:
                        await f.write(markdown_output)
                else:
                    async with aiofiles.open('Equipment Fan Trays/Markdown/Equipment Fan Trays.md', mode='w' ) as f:
                        await f.write(markdown_output)

            if "eqptIndLed" in api:
                async with aiofiles.open('Equipment Indicator LEDs/Markdown/Equipment Indicator LEDs.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptLC" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Line Card Slots/Markdown/Equipment Line Card Slots.md', mode='w' ) as f:
                        await f.write(markdown_output)
                else:
                    async with aiofiles.open('Equipment Line Cards/Markdown/Equipment Line Cards.md', mode='w' ) as f:
                        await f.write(markdown_output)

            if "eqptLeafP" in api:
                async with aiofiles.open('Equipment Leaf Ports/Markdown/Equipment Leaf Ports.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptLocLed" in api:
                async with aiofiles.open('Equipment Port Locator LEDs/Markdown/Equipment Port Locator LEDs.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptPsu" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Power Supply Slots/Markdown/Equipment Power Supply Slots.md', mode='w' ) as f:
                        await f.write(markdown_output)
                else:
                    async with aiofiles.open('Equipment Power Supplies/Markdown/Equipment Power Supplies.md', mode='w' ) as f:
                        await f.write(markdown_output)

            if "eqptRsIoPPhysConf" in api:
                async with aiofiles.open('Equipment RS IO Port Physical Configs/Markdown/Equipment RS IO Port Physical Configs.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptSensor" in api:
                async with aiofiles.open('Equipment Sensors/Markdown/Equipment Sensors.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptSpCmnBlk" in api:
                async with aiofiles.open('Equipment SP Common Blocks/Markdown/Equipment SP Common Blocks.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptSpromLc" in api:
                async with aiofiles.open('Equipment SPROM LCs/Markdown/Equipment SPROM LCs.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptSpromPsu" in api:
                if "Blk" in api:
                    async with aiofiles.open('Equipment SPROM Power Supply Blocks/Markdown/Equipment SPROM Power Supply Blocks.md', mode='w' ) as f:
                        await f.write(markdown_output)
                else:
                    async with aiofiles.open('Equipment SPROM Power Supplies/Markdown/Equipment SPROM Power Supplies.md', mode='w' ) as f:
                        await f.write(markdown_output)

            if "eqptSpromSup" in api:
                async with aiofiles.open('Equipment SPROM Supervisors/Markdown/Equipment SPROM Supervisors.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptStorage" in api:
                async with aiofiles.open('Equipment Storage/Markdown/Equipment Storage.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "eqptSupC" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Supervisor Slots/Markdown/Equipment Supervisor Slots.md', mode='w' ) as f:
                        await f.write(markdown_output)
                else:
                    async with aiofiles.open('Equipment Supervisors/Markdown/Equipment Supervisors.md', mode='w' ) as f:
                        await f.write(markdown_output)

            if "ethpmPhysIf" in api:
                async with aiofiles.open('Ethernet Port Manager Physical Interfaces/Markdown/Ethernet Port Manager Physical Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fabricExtPathEpCont" in api:
                async with aiofiles.open('Fabric Extended Path Endpoint Containers/Markdown/Fabric Extended Path Endpoint Containers.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fabricInst" in api:
                async with aiofiles.open('Fabric Instances/Markdown/Fabric Instances.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fabricLink" in api:
                if "Cont" in api:
                    async with aiofiles.open('Fabric Link Containers/Markdown/Fabric Link Containers.md', mode='w' ) as f:
                        await f.write(markdown_output)
                else:
                    async with aiofiles.open('Fabric Links/Markdown/Fabric Links.md', mode='w' ) as f:
                        await f.write(markdown_output)

            if "fabricLooseLink" in api:
                async with aiofiles.open('Fabric Loose Links/Markdown/Fabric Loose Links.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fabricLooseNode" in api:
                async with aiofiles.open('Fabric Loose Nodes/Markdown/Fabric Loose Nodes.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fabricProtPathEpCont" in api:
                async with aiofiles.open('Fabric Protected Path Endpoint Containers/Markdown/Fabric Protected Path Endpoint Containers.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fcEntity" in api:
                async with aiofiles.open('Fibre Channel Entities/Markdown/Fibre Channel Entities.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "firmwareCardRunning" in api:
                async with aiofiles.open('Firmware Card Running/Markdown/Firmware Card Running.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "firmwareCompRunning" in api:
                async with aiofiles.open('Firmware Compute Running/Markdown/Firmware Compute Running.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "firmwareRunning" in api:
                async with aiofiles.open('Firmware Running/Markdown/Firmware Running.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fvEpPCont" in api:
                async with aiofiles.open('Endpoint Profile Containers/Markdown/Endpoint Profile Containers.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fvLocale" in api:
                async with aiofiles.open('Locales/Markdown/Locales.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fvRsBDToOut" in api:
                async with aiofiles.open('Bridge Domains To Outside/Markdown/Bridge Domains To Outside.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fvRsBd" in api:
                async with aiofiles.open('EPG Bridge Domain Links/Markdown/EPG Bridge Domain Links.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fvRsCEpToPathEp" in api:
                async with aiofiles.open('Endpoints To Paths/Markdown/Endpoints To Paths.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fvRsCons" in api:
                if "If" in api:
                    async with aiofiles.open('Contract Consumer Interfaces/Markdown/Contract Consumer Interfaces.md', mode='w' ) as f:
                        await f.write(markdown_output)
                else:
                    async with aiofiles.open('Contract Consumers/Markdown/Contract Consumers.md', mode='w' ) as f:
                        await f.write(markdown_output)

            if "fvRsCtx" in api:
                async with aiofiles.open('Context Source Relationships/Markdown/Context Source Relationships.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fvRsDomAtt" in api:
                async with aiofiles.open('Domain Attachments/Markdown/Domain Attachments.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fvRsPathAtt" in api:
                async with aiofiles.open('Path Attachments/Markdown/Path Attachments.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fvRsProv" in api:
                async with aiofiles.open('Contract Providers/Markdown/Contract Providers.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fvRtBd" in api:
                async with aiofiles.open('Bridge Domains Target Relationships/Markdown/Bridge Domains Target Relationships.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fvRtCtx" in api:
                async with aiofiles.open('Contexts Target Relationships/Markdown/Contexts Target Relationships.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fvnsEncapBlk" in api:
                async with aiofiles.open('VLAN Encapsulation Blocks/Markdown/VLAN Encapsulation Blocks.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "fvnsVlanInstP" in api:
                async with aiofiles.open('VLAN Namespace Policies/Markdown/VLAN Namespace Policies.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraAccBndlGrp" in api:
                async with aiofiles.open('Access Bundle Groups/Markdown/Access Bundle Groups.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraAccPortGrp" in api:
                async with aiofiles.open('Access Port Groups/Markdown/Access Port Groups.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraAccPortP" in api:
                async with aiofiles.open('Access Port Profiles/Markdown/Access Port Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraContr" in api:
                async with aiofiles.open('Controllers/Markdown/Controllers.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraFexP" in api:
                async with aiofiles.open('FEX Policies/Markdown/FEX Policies.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraFuncP" in api:
                async with aiofiles.open('Function Policies/Markdown/Function Policies.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraHPortS" in api:
                async with aiofiles.open('Host Port Selectors/Markdown/Host Port Selectors.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraPortBlk" in api:
                async with aiofiles.open('Port Blocks/Markdown/Port Blocks.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraRsAccBaseGrp" in api:
                async with aiofiles.open('Access Policy Group Source Relationships/Markdown/Access Policy Group Source Relationships.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraRsAttEntP" in api:
                async with aiofiles.open('Attachable Access Entity Profiles Source Relationships/Markdown/Attachable Access Entity Profiles Source Relationships.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraRsDomP" in api:
                async with aiofiles.open('Domain Profile Source Relationships/Markdown/Domain Profile Source Relationships.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraRsSpAccGrp" in api:
                async with aiofiles.open('Spine Access Policy Groups/Markdown/Spine Access Policy Groups.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraRsVlanNs" in api:
                async with aiofiles.open('VLAN Namespace Source Relationships/Markdown/VLAN Namespace Source Relationships.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraSHPortS" in api:
                async with aiofiles.open('Spine Host Port Selectors/Markdown/Spine Host Port Selectors.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraSpAccPortP" in api:
                async with aiofiles.open('Spine Access Port Profiles/Markdown/Spine Access Port Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "infraWiNode" in api:
                async with aiofiles.open('Wired Nodes/Markdown/Wired Nodes.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ipNexthopP" in api:
                async with aiofiles.open('Static Route Next Hop Policies/Markdown/Static Route Next Hop Policies.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ipRouteP" in api:
                async with aiofiles.open('Route Policies/Markdown/Route Policies.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ipv4Addr" in api:
                async with aiofiles.open('IPv4 Addresses/Markdown/IPv4 Addresses.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ipv4Dom" in api:
                async with aiofiles.open('IPv4 Domains/Markdown/IPv4 Domains.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ipv4Entity" in api:
                async with aiofiles.open('IPv4 Entities/Markdown/IPv4 Entities.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ipv4If" in api:
                async with aiofiles.open('IPv4 Interfaces/Markdown/IPv4 Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ipv4Inst" in api:
                async with aiofiles.open('IPv4 Instances/Markdown/IPv4 Instances.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ipv4Nexthop" in api:
                async with aiofiles.open('IPv4 Next Hop/Markdown/IPv4 Next Hop.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ipv4Route" in api:
                async with aiofiles.open('IPv4 Routes/Markdown/IPv4 Routes.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "isisAdjEp" in api:
                async with aiofiles.open('ISIS Adjacency Endpoints/Markdown/ISIS Adjacency Endpoints.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "isisDTEp" in api:
                async with aiofiles.open('ISIS Discovered Tunnel Endpoints/Markdown/ISIS Discovered Tunnel Endpoints.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "isisDom" in api:
                if "Lvl" in api:
                    async with aiofiles.open('ISIS Domains Level/Markdown/ISIS Domains Level.md', mode='w' ) as f:
                        await f.write(markdown_output)
                else:
                    async with aiofiles.open('ISIS Domains/Markdown/ISIS Domains.md', mode='w' ) as f:
                        await f.write(markdown_output)

            if "isisEntity" in api:
                async with aiofiles.open('ISIS Entities/Markdown/ISIS Entities.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "isisIf" in api:
                if "Lvl" in api:
                    async with aiofiles.open('ISIS Interfaces Level/Markdown/ISIS Interfaces Level.md', mode='w' ) as f:
                        await f.write(markdown_output)
                else:
                    async with aiofiles.open('ISIS Interfaces/Markdown/ISIS Interfaces.md', mode='w' ) as f:
                        await f.write(markdown_output)

            if "isisInst" in api:
                async with aiofiles.open('ISIS Instances/Markdown/ISIS Instances.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "isisNexthop" in api:
                async with aiofiles.open('ISIS Next Hop/Markdown/ISIS Next Hop.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "isisRoute" in api:
                async with aiofiles.open('ISIS Routes/Markdown/ISIS Routes.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l2BD" in api:
                async with aiofiles.open('L2 Bridge Domains/Markdown/L2 Bridge Domains.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l2ExtIf" in api:
                async with aiofiles.open('L2 External Interfaces/Markdown/L2 External Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l2RsEthIf" in api:
                async with aiofiles.open('L2 Interface Source Relationships/Markdown/L2 Interface Source Relationships.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l2extInstP" in api:
                async with aiofiles.open('L2 External Instance Profiles/Markdown/L2 External Instance Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l2extLIfP" in api:
                async with aiofiles.open('L2 External Logical Interface Profiles/Markdown/L2 External Logical Interface Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l2extLNodeP" in api:
                async with aiofiles.open('L2 External Logical Node Profiles/Markdown/L2 External Logical Node Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l2extRsEBd" in api:
                async with aiofiles.open('L2 EPG Bridge Domain Source Relationships/Markdown/L2 EPG Bridge Domain Source Relationships.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l2extRsPathL2OutAtt" in api:
                async with aiofiles.open('L2Out Paths/Markdown/L2Out Paths.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3Ctx" in api:
                async with aiofiles.open('L3 Contexts/Markdown/L3 Contexts.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3EncRtdIf" in api:
                async with aiofiles.open('L3 Subinterfaces/Markdown/L3 Subinterfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3Inst" in api:
                async with aiofiles.open('L3 Instances/Markdown/L3 Instances.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3LbRtdIf" in api:
                async with aiofiles.open('L3 Routed Loopback Interfaces/Markdown/L3 Routed Loopback Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3RsEncPhysRtdConf" in api:
                async with aiofiles.open('L3 Physical Interface Source Relationships/Markdown/L3 Physical Interface Source Relationships.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3RtdIf" in api:
                async with aiofiles.open('L3 Routed Interfaces/Markdown/L3 Routed Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3extInstP" in api:
                async with aiofiles.open('L3Out Profiles/Markdown/L3Out Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3extIp" in api:
                async with aiofiles.open('L3Out IP Addresses/Markdown/L3Out IP Addresses.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3extLIfP" in api:
                async with aiofiles.open('L3 Logical Interface Profiles/Markdown/L3 Logical Interface Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3extLNodeP" in api:
                async with aiofiles.open('L3 Logical Node Profiles/Markdown/L3 Logical Node Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3extMember" in api:
                async with aiofiles.open('L3Out Members/Markdown/L3Out Members.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3extRsEctx" in api:
                async with aiofiles.open('L3 Contexts Source Relationships/Markdown/L3 Contexts Source Relationships.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3extRsL3DomAtt" in api:
                async with aiofiles.open('L3 Domains Source Relationships/Markdown/L3 Domains Source Relationships.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3extRsNodeL3OutAtt" in api:
                async with aiofiles.open('L3Out Node Source Relationships/Markdown/L3Out Node Source Relationships.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3extRsPathL3OutAtt" in api:
                async with aiofiles.open('L3Out Path Source Relationships/Markdown/L3Out Path Source Relationships.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "l3extSubnet" in api:
                async with aiofiles.open('L3 Subnets/Markdown/L3 Subnets.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "lacpEntity" in api:
                async with aiofiles.open('LACP Entities/Markdown/LACP Entities.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "lacpIf" in api:
                async with aiofiles.open('LACP Interfaces/Markdown/LACP Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "lacpInst" in api:
                async with aiofiles.open('LACP Instances/Markdown/LACP Instances.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "leqptLooseNode" in api:
                async with aiofiles.open('External Unmanaged Nodes/Markdown/External Unmanaged Nodes.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "leqptRsLsNodeToIf" in api:
                async with aiofiles.open('External Unmanaged Nodes Interfaces/Markdown/External Unmanaged Nodes Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "lldpAdjEp" in api:
                async with aiofiles.open('LLDP Adjacency Endpoints/Markdown/LLDP Adjacency Endpoints.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "lldpEntity" in api:
                async with aiofiles.open('LLDP Entities/Markdown/LLDP Entities.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "lldpIf" in api:
                async with aiofiles.open('LLDP Interfaces/Markdown/LLDP Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "lldpInst" in api:
                async with aiofiles.open('LLDP Instances/Markdown/LLDP Instances.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "mgmtMgmtIf" in api:
                async with aiofiles.open('Management Interfaces/Markdown/Management Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ospfAdjEp" in api:
                async with aiofiles.open('OSPF Adjacency Endpoints/Markdown/OSPF Adjacency Endpoints.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ospfArea" in api:
                async with aiofiles.open('OSPF Areas/Markdown/OSPF Areas.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ospfDb" in api:
                async with aiofiles.open('OSPF Database/Markdown/OSPF Database.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ospfDom" in api:
                async with aiofiles.open('OSPF Domains/Markdown/OSPF Domains.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ospfEntity" in api:
                async with aiofiles.open('OSPF Entities/Markdown/OSPF Entities.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ospfExtP" in api:
                async with aiofiles.open('OSPF External Profiles/Markdown/OSPF External Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ospfIf" in api:
                async with aiofiles.open('OSPF Interfaces/Markdown/OSPF Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ospfInst" in api:
                async with aiofiles.open('OSPF Instances/Markdown/OSPF Instances.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ospfRoute" in api:
                async with aiofiles.open('OSPF Routes/Markdown/OSPF Routes.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "ospfUcNexthop" in api:
                async with aiofiles.open('OSPF Unicast Next Hop/Markdown/OSPF Unicast Next Hop.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "pcAggrIf" in api:
                async with aiofiles.open('Port Channel Aggregate Interfaces/Markdown/Port Channel Aggregate Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "pcRsMbrIfs" in api:
                async with aiofiles.open('Port Channel Member Interfaces/Markdown/Port Channel Member Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "sviIf" in api:
                async with aiofiles.open('SVIs/Markdown/SVIs.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "tunnelIf" in api:
                async with aiofiles.open('Tunnel Interfaces/Markdown/Tunnel Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "uribv4Db" in api:
                async with aiofiles.open('Unicast Route Database/Markdown/Unicast Route Database.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "uribv4Dom" in api:
                async with aiofiles.open('Unicast Route Domains/Markdown/Unicast Route Domains.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "uribv4Entity" in api:
                async with aiofiles.open('Unicast Route Entities/Markdown/Unicast Route Entities.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "uribv4Nexthop" in api:
                async with aiofiles.open('Unicast Route Next Hop/Markdown/Unicast Route Next Hop.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "uribv4Route" in api:
                async with aiofiles.open('Unicast Routes/Markdown/Unicast Routes.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vlanCktEp" in api:
                async with aiofiles.open('VLAN Endpoint Group Encapsulation/Markdown/VLAN Endpoint Group Encapsulation.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vmmCtrlrP" in api:
                async with aiofiles.open('VMM Controller Profiles/Markdown/VMM Controller Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vmmDomP" in api:
                async with aiofiles.open('VMM Domain Profiles/Markdown/VMM Domain Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vmmProvP" in api:
                async with aiofiles.open('VMM Provider Profiles/Markdown/VMM Provider Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vmmUsrAccP" in api:
                async with aiofiles.open('VMM User Profiles/Markdown/VMM User Profiles.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vpcDom" in api:
                async with aiofiles.open('VPC Domains/Markdown/VPC Domains.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vpcEntity" in api:
                async with aiofiles.open('VPC Entities/Markdown/VPC Entities.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vpcIf" in api:
                async with aiofiles.open('VPC Interfaces/Markdown/VPC Interfaces.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vpcInst" in api:
                async with aiofiles.open('VPC Instances/Markdown/VPC Instances.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vpcRsVpcConf" in api:
                async with aiofiles.open('VPC Configurations/Markdown/VPC Configurations.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vzAny" in api:
                async with aiofiles.open('vzAny/Markdown/vzAny.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vzFilter" in api:
                async with aiofiles.open('vzFilters/Markdown/vzFilters.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vzRsAnyToCons" in api:
                async with aiofiles.open('vzAny To Consumers/Markdown/vzAny To Consumers.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vzRsAnyToProv" in api:
                async with aiofiles.open('vzAny To Providers/Markdown/vzAny To Providers.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vzRsDenyRule" in api:
                async with aiofiles.open('vzDeny Rules/Markdown/vzDeny Rules.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vzRsIf" in api:
                async with aiofiles.open('vzInterface Source Relationships/Markdown/vzInterface Source Relationships.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vzRsSubjFiltAtt" in api:
                async with aiofiles.open('Contract Subjects Filter Attributes/Markdown/Contract Subjects Filter Attributes.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vzRtCons" in api:
                async with aiofiles.open('Contract Consumers Root/Markdown/Contract Consumers Root.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vzRtProv" in api:
                async with aiofiles.open('Contract Providers Root/Markdown/Contract Providers Root.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vzRuleOwner" in api:
                async with aiofiles.open('vzRule Owner/Markdown/vzRule Owner.md', mode='w' ) as f:
                    await f.write(markdown_output)

            if "vzTaboo" in api:
                async with aiofiles.open('vzTaboo/Markdown/vzTaboo.md', mode='w' ) as f:
                    await f.write(markdown_output)

    async def html_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        html_template = env.get_template('aci_html.j2')
        for api, payload in json.loads(parsed_json):
            html_output = await html_template.render_async(api = api,
                                             data_to_template = payload)
            if "Tenant" in api:
                async with aiofiles.open('Tenant/HTML/Tenants.html', mode='w' ) as f:
                    await f.write(html_output)

            if "AEPg" in api:
                async with aiofiles.open('EPGs/HTML/EPGs.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fvBD" in api:
                async with aiofiles.open('Bridge Domains/HTML/Bridge Domains.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fvCtx" in api:
                async with aiofiles.open('Contexts/HTML/Contexts.html', mode='w' ) as f:
                    await f.write(html_output)

            if "Ap" in api:
                async with aiofiles.open('Application Profiles/HTML/Application Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3extOut" in api:
                async with aiofiles.open('L3Outs/HTML/L3Outs.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l2extOut" in api:
                async with aiofiles.open('L2Outs/HTML/L2Outs.html', mode='w' ) as f:
                    await f.write(html_output)

            if "topSystem" in api:
                if "?" not in api:
                    async with aiofiles.open('Top System/HTML/Top System.html', mode='w' ) as f:
                        await f.write(html_output)

            if "fvSubnet" in api:
                async with aiofiles.open('Subnets/HTML/Subnets.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fvCEp" in api:
                async with aiofiles.open('Endpoints/HTML/Endpoints.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fabricNode" in api:
                async with aiofiles.open('Fabric Nodes/HTML/Fabric Nodes.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l1PhysIf" in api:
                async with aiofiles.open('Physical Interfaces/HTML/Physical Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraAccPortP" in api:
                async with aiofiles.open('Leaf Interface Profiles/HTML/Leaf Interface Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraSpAccPortP" in api:
                async with aiofiles.open('Spine Interface Profiles/HTML/Spine Interface Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraNodeP" in api:
                async with aiofiles.open('Leaf Switch Profiles/HTML/Leaf Switch Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraSpineP" in api:
                async with aiofiles.open('Spine Switch Profiles/HTML/Spine Switch Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fvnsVlanInstP" in api:
                async with aiofiles.open('VLAN Pools/HTML/VLAN Pools.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraAttEntityP" in api:
                async with aiofiles.open('Attachable Access Entity Profiles/HTML/Attachable Access Entity Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vzBrCP" in api:
                async with aiofiles.open('Contracts/HTML/Contracts.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vzEntry" in api:
                async with aiofiles.open('vzEntries/HTML/vzEntries.html', mode='w' ) as f:
                    await f.write(html_output)

            if "physDomP" in api:
                async with aiofiles.open('Physical Domains/HTML/Physical Domains.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3extDomP" in api:
                async with aiofiles.open('L3 Domains/HTML/L3 Domains.html', mode='w' ) as f:
                    await f.write(html_output)

            if "qosClass" in api:
                async with aiofiles.open('QOS Classes/HTML/QOS Classes.html', mode='w' ) as f:
                    await f.write(html_output)

            if "faultSummary" in api:
                async with aiofiles.open('Fault Summary/HTML/Fault Summary.html', mode='w' ) as f:
                    await f.write(html_output)

            if "aaaModLR" in api:
                async with aiofiles.open('Audit Log/HTML/Audit Log.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fvIp" in api:
                async with aiofiles.open('IP Addresses/HTML/IP Addresses.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eventRecord" in api:
                async with aiofiles.open('Events/HTML/Events.html', mode='w' ) as f:
                    await f.write(html_output)

            if "licenseEntitlement" in api:
                async with aiofiles.open('License Entitlements/HTML/License Entitlements.html', mode='w' ) as f:
                    await f.write(html_output)

            if "bgpRRNodePEp" in api:
                async with aiofiles.open('BGP Route Reflectors/HTML/BGP Route Reflectors.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraPortS" in api:
                async with aiofiles.open('Interface Policies/HTML/Interface Policies.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraProfile" in api:
                async with aiofiles.open('Interface Profiles/HTML/Interface Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fabricPod" in api:
                async with aiofiles.open('Fabric Pods/HTML/Fabric Pods.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fabricPath" in api:
                if "fabricPathEp" in api:
                    if "Cont" in api:
                        async with aiofiles.open('Fabric Path Endpoint Containers/HTML/Fabric Path Endpoint Containers.html', mode='w' ) as f:
                            await f.write(html_output)
                    else:
                        async with aiofiles.open('Fabric Path Endpoints/HTML/Fabric Path Endpoints.html', mode='w' ) as f:
                            await f.write(html_output)
                else:
                    async with aiofiles.open('Fabric Paths/HTML/Fabric Paths.html', mode='w' ) as f:
                        await f.write(html_output)

            if "rtctrlSubjP" in api:
                async with aiofiles.open('Prefix List/HTML/Prefix List.html', mode='w' ) as f:
                    await f.write(html_output)

            if "rtctrlMatchRtDest" in api:
                async with aiofiles.open('Prefix List Detailed/HTML/Prefix List Detailed.html', mode='w' ) as f:
                    await f.write(html_output)

            if "aaaUser" in api:
                async with aiofiles.open('Users/HTML/Users.html', mode='w' ) as f:
                    await f.write(html_output)

            if "aaaDomain" in api:
                async with aiofiles.open('Security Domains/HTML/Security Domains.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vzSubj" in api:
                async with aiofiles.open('Contract Subjects/HTML/Contract Subjects.html', mode='w' ) as f:
                    await f.write(html_output)

            if "topology/health" in api:
                async with aiofiles.open('Health/HTML/Health.html', mode='w' ) as f:
                    await f.write(html_output)

            if "pkiFabricNodeSSLCertificate" in api:
                async with aiofiles.open('Fabric Node SSL Certificates/HTML/Fabric Node SSL Certificates.html', mode='w' ) as f:
                    await f.write(html_output)

            if "tn-" in api:
                if "health" in api:
                    async with aiofiles.open('Tenant Health/HTML/Tenant Health.html', mode='w' ) as f:
                        await f.write(html_output)

            if "firmwareCtrlrRunning" in api:
                async with aiofiles.open('Fabric Membership/HTML/Fabric Membership.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraWiNode" in api:
                async with aiofiles.open('Cluster Health/HTML/Cluster Health.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vnsMDev" in api:
                async with aiofiles.open('Device Packages/HTML/Device Packages.html', mode='w' ) as f:
                    await f.write(html_output)

            if "cnwAggrIf" in api:
                async with aiofiles.open('Cluster Aggregate Interfaces/HTML/Cluster Aggregate Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3Inst" in api:
                async with aiofiles.open('L3 Interfaces/HTML/L3 Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "actrlEntity" in api:
                async with aiofiles.open('Access Control Entities/HTML/Access Control Entities.html', mode='w' ) as f:
                    await f.write(html_output)

            if "actrlInst" in api:
                async with aiofiles.open('Access Control Instances/HTML/Access Control Instances.html', mode='w' ) as f:
                    await f.write(html_output)

            if "actrlRule" in api:
                async with aiofiles.open('Access Control Rules/HTML/Access Control Rules.html', mode='w' ) as f:
                    await f.write(html_output)

            if "actrlScope" in api:
                async with aiofiles.open('Access Control Scopes/HTML/Access Control Scopes.html', mode='w' ) as f:
                    await f.write(html_output)

            if "cnwPhysIf" in api:
                async with aiofiles.open('Cluster Physical Interfaces/HTML/Cluster Physical Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "compCtrlr" in api:
                async with aiofiles.open('Compute Controllers/HTML/Compute Controllers.html', mode='w' ) as f:
                    await f.write(html_output)

            if "compDom" in api:
                async with aiofiles.open('Compute Domains/HTML/Compute Domains.html', mode='w' ) as f:
                    await f.write(html_output)

            if "compEpPD" in api:
                async with aiofiles.open('Compute Endpoint Policy Descriptions/HTML/Compute Endpoint Policy Descriptions.html', mode='w' ) as f:
                    await f.write(html_output)

            if "compProv" in api:
                async with aiofiles.open('Compute Providers/HTML/Compute Providers.html', mode='w' ) as f:
                    await f.write(html_output)

            if "arpAdjEp" in api:
                async with aiofiles.open('ARP Adjacency Endpoints/HTML/ARP Adjacency Endpoints.html', mode='w' ) as f:
                    await f.write(html_output)

            if "arpDb" in api:
                async with aiofiles.open('ARP Database/HTML/ARP Database.html', mode='w' ) as f:
                    await f.write(html_output)

            if "arpDom" in api:
                async with aiofiles.open('ARP Domain/HTML/ARP Domain.html', mode='w' ) as f:
                    await f.write(html_output)

            if "arpEntity" in api:
                async with aiofiles.open('ARP Entity/HTML/ARP Entity.html', mode='w' ) as f:
                    await f.write(html_output)

            if "arpIf" in api:
                async with aiofiles.open('ARP Interfaces/HTML/ARP Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "arpInst" in api:
                async with aiofiles.open('ARP Instances/HTML/ARP Instances.html', mode='w' ) as f:
                    await f.write(html_output)

            if "bgpDom" in api:
                if "Af" in api:
                    async with aiofiles.open('BGP Domain Address Families/HTML/BGP Domain Address Families.html', mode='w' ) as f:
                        await f.write(html_output)
                else:
                    async with aiofiles.open('BGP Domains/HTML/BGP Domains.html', mode='w' ) as f:
                        await f.write(html_output)

            if "bgpEntity" in api:
                async with aiofiles.open('BGP Entities/HTML/BGP Entities.html', mode='w' ) as f:
                    await f.write(html_output)

            if "bgpInst" in api:
                if "InstPol" in api:
                    async with aiofiles.open('BGP Instances Policy/HTML/BGP Instances Policy.html', mode='w' ) as f:
                        await f.write(html_output)
                else:
                    async with aiofiles.open('BGP Instances/HTML/BGP Instances.html', mode='w' ) as f:
                        await f.write(html_output)

            if "bgpPeer" in api:
                if "bgpPeerAf" in api:
                    async with aiofiles.open('BGP Peers AF Entries/HTML/BGP Peers AF Entries.html', mode='w' ) as f:
                        await f.write(html_output)
                elif "bgpPeerEntry" in api:
                    async with aiofiles.open('BGP Peers Entries/HTML/BGP Peers Entries.html', mode='w' ) as f:
                        await f.write(html_output)
                else:
                    async with aiofiles.open('BGP Peers/HTML/BGP Peers.html', mode='w' ) as f:
                        await f.write(html_output)

            if "bgpRRP" in api:
                async with aiofiles.open('BGP Route Reflector Policies/HTML/BGP Route Reflector Policies.html', mode='w' ) as f:
                    await f.write(html_output)

            if "cdpAdjEp" in api:
                async with aiofiles.open('CDP Adjacency Endpoints/HTML/CDP Adjacency Endpoints.html', mode='w' ) as f:
                    await f.write(html_output)

            if "cdpEntity" in api:
                async with aiofiles.open('CDP Entities/HTML/CDP Entities.html', mode='w' ) as f:
                    await f.write(html_output)

            if "cdpIf" in api:
                async with aiofiles.open('CDP Interfaces/HTML/CDP Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "cdpInst" in api:
                async with aiofiles.open('CDP Instances/HTML/CDP Instances.html', mode='w' ) as f:
                    await f.write(html_output)

            if "cdpIntfAddr" in api:
                async with aiofiles.open('CDP Interface Addresses/HTML/CDP Interface Addresses.html', mode='w' ) as f:
                    await f.write(html_output)

            if "cdpMgmtAddr" in api:
                async with aiofiles.open('CDP Management Addresses/HTML/CDP Management Addresses.html', mode='w' ) as f:
                    await f.write(html_output)

            if "cnwRsMbrIfs" in api:
                async with aiofiles.open('Cluster RS Member Interfaces/HTML/Cluster RS Member Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "compRsDomP" in api:
                async with aiofiles.open('Compute RS Domain Policies/HTML/Compute RS Domain Policies.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptBSlot" in api:
                async with aiofiles.open('Equipment Board Slots/HTML/Equipment Board Slots.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptBoard" in api:
                async with aiofiles.open('Equipment Boards/HTML/Equipment Boards.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptCPU" in api:
                async with aiofiles.open('Equipment CPUs/HTML/Equipment CPUs.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptCh" in api:
                async with aiofiles.open('Equipment Chassis/HTML/Equipment Chassis.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptDimm" in api:
                async with aiofiles.open('Equipment DIMMs/HTML/Equipment DIMMs.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptExtCh" in api:
                async with aiofiles.open('Equipment Fabric Extenders/HTML/Equipment Fabric Extenders.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptFabP" in api:
                async with aiofiles.open('Equipment Fabric Ports/HTML/Equipment Fabric Ports.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptFan" in api:
                async with aiofiles.open('Equipment Fans/HTML/Equipment Fans.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptFpga" in api:
                async with aiofiles.open('Equipment Field Programmable Gate Arrays/HTML/Equipment Field Programmable Gate Arrays.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptFt" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Fan Tray Slots/HTML/Equipment Fan Tray Slots.html', mode='w' ) as f:
                        await f.write(html_output)
                else:
                    async with aiofiles.open('Equipment Fan Trays/HTML/Equipment Fan Trays.html', mode='w' ) as f:
                        await f.write(html_output)

            if "eqptIndLed" in api:
                async with aiofiles.open('Equipment Indicator LEDs/HTML/Equipment Indicator LEDs.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptLC" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Line Card Slots/HTML/Equipment Line Card Slots.html', mode='w' ) as f:
                        await f.write(html_output)
                else:
                    async with aiofiles.open('Equipment Line Cards/HTML/Equipment Line Cards.html', mode='w' ) as f:
                        await f.write(html_output)

            if "eqptLeafP" in api:
                async with aiofiles.open('Equipment Leaf Ports/HTML/Equipment Leaf Ports.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptLocLed" in api:
                async with aiofiles.open('Equipment Port Locator LEDs/HTML/Equipment Port Locator LEDs.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptPsu" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Power Supply Slots/HTML/Equipment Power Supply Slots.html', mode='w' ) as f:
                        await f.write(html_output)
                else:            
                    async with aiofiles.open('Equipment Power Supplies/HTML/Equipment Power Supplies.html', mode='w' ) as f:
                        await f.write(html_output)

            if "eqptRsIoPPhysConf" in api:
                async with aiofiles.open('Equipment RS IO Port Physical Configs/HTML/Equipment RS IO Port Physical Configs.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptSensor" in api:
                async with aiofiles.open('Equipment Sensors/HTML/Equipment Sensors.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptSpCmnBlk" in api:
                async with aiofiles.open('Equipment SP Common Blocks/HTML/Equipment SP Common Blocks.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptSpromLc" in api:
                async with aiofiles.open('Equipment SPROM LCs/HTML/Equipment SPROM LCs.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptSpromPsu" in api:
                if "Blk" in api:
                    async with aiofiles.open('Equipment SPROM Power Supply Blocks/HTML/Equipment SPROM Power Supply Blocks.html', mode='w' ) as f:
                        await f.write(html_output)
                else:
                    async with aiofiles.open('Equipment SPROM Power Supplies/HTML/Equipment SPROM Power Supplies.html', mode='w' ) as f:
                        await f.write(html_output)

            if "eqptSpromSup" in api:
                async with aiofiles.open('Equipment SPROM Supervisors/HTML/Equipment SPROM Supervisors.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptStorage" in api:
                async with aiofiles.open('Equipment Storage/HTML/Equipment Storage.html', mode='w' ) as f:
                    await f.write(html_output)

            if "eqptSupC" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Supervisor Slots/HTML/Equipment Supervisor Slots.html', mode='w' ) as f:
                        await f.write(html_output)
                else:
                    async with aiofiles.open('Equipment Supervisors/HTML/Equipment Supervisors.html', mode='w' ) as f:
                        await f.write(html_output)

            if "ethpmPhysIf" in api:
                async with aiofiles.open('Ethernet Port Manager Physical Interfaces/HTML/Ethernet Port Manager Physical Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fabricExtPathEpCont" in api:
                async with aiofiles.open('Fabric Extended Path Endpoint Containers/HTML/Fabric Extended Path Endpoint Containers.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fabricInst" in api:
                async with aiofiles.open('Fabric Instances/HTML/Fabric Instances.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fabricLink" in api:
                if "Cont" in api:
                    async with aiofiles.open('Fabric Link Containers/HTML/Fabric Link Containers.html', mode='w' ) as f:
                        await f.write(html_output)
                else:
                    async with aiofiles.open('Fabric Links/HTML/Fabric Links.html', mode='w' ) as f:
                        await f.write(html_output)

            if "fabricLooseLink" in api:
                async with aiofiles.open('Fabric Loose Links/HTML/Fabric Loose Links.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fabricLooseNode" in api:
                async with aiofiles.open('Fabric Loose Nodes/HTML/Fabric Loose Nodes.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fabricProtPathEpCont" in api:
                async with aiofiles.open('Fabric Protected Path Endpoint Containers/HTML/Fabric Protected Path Endpoint Containers.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fcEntity" in api:
                async with aiofiles.open('Fibre Channel Entities/HTML/Fibre Channel Entities.html', mode='w' ) as f:
                    await f.write(html_output)

            if "firmwareCardRunning" in api:
                async with aiofiles.open('Firmware Card Running/HTML/Firmware Card Running.html', mode='w' ) as f:
                    await f.write(html_output)

            if "firmwareCompRunning" in api:
                async with aiofiles.open('Firmware Compute Running/HTML/Firmware Compute Running.html', mode='w' ) as f:
                    await f.write(html_output)

            if "firmwareRunning" in api:
                async with aiofiles.open('Firmware Running/HTML/Firmware Running.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fvEpPCont" in api:
                async with aiofiles.open('Endpoint Profile Containers/HTML/Endpoint Profile Containers.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fvLocale" in api:
                async with aiofiles.open('Locales/HTML/Locales.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fvRsBDToOut" in api:
                async with aiofiles.open('Bridge Domains To Outside/HTML/Bridge Domains To Outside.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fvRsBd" in api:
                async with aiofiles.open('EPG Bridge Domain Links/HTML/EPG Bridge Domain Links.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fvRsCEpToPathEp" in api:
                async with aiofiles.open('Endpoints To Paths/HTML/Endpoints To Paths.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fvRsCons" in api:
                if "If" in api:
                    async with aiofiles.open('Contract Consumer Interfaces/HTML/Contract Consumer Interfaces.html', mode='w' ) as f:
                        await f.write(html_output)
                else:
                    async with aiofiles.open('Contract Consumers/HTML/Contract Consumers.html', mode='w' ) as f:
                        await f.write(html_output)

            if "fvRsCtx" in api:
                async with aiofiles.open('Context Source Relationships/HTML/Context Source Relationships.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fvRsDomAtt" in api:
                async with aiofiles.open('Domain Attachments/HTML/Domain Attachments.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fvRsPathAtt" in api:
                async with aiofiles.open('Path Attachments/HTML/Path Attachments.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fvRsProv" in api:
                async with aiofiles.open('Contract Providers/HTML/Contract Providers.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fvRtBd" in api:
                async with aiofiles.open('Bridge Domains Target Relationships/HTML/Bridge Domains Target Relationships.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fvRtCtx" in api:
                async with aiofiles.open('Contexts Target Relationships/HTML/Contexts Target Relationships.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fvnsEncapBlk" in api:
                async with aiofiles.open('VLAN Encapsulation Blocks/HTML/VLAN Encapsulation Blocks.html', mode='w' ) as f:
                    await f.write(html_output)

            if "fvnsVlanInstP" in api:
                async with aiofiles.open('VLAN Namespace Policies/HTML/VLAN Namespace Policies.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraAccBndlGrp" in api:
                async with aiofiles.open('Access Bundle Groups/HTML/Access Bundle Groups.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraAccPortGrp" in api:
                async with aiofiles.open('Access Port Groups/HTML/Access Port Groups.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraAccPortP" in api:
                async with aiofiles.open('Access Port Profiles/HTML/Access Port Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraContr" in api:
                async with aiofiles.open('Controllers/HTML/Controllers.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraFexP" in api:
                async with aiofiles.open('FEX Policies/HTML/FEX Policies.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraFuncP" in api:
                async with aiofiles.open('Function Policies/HTML/Function Policies.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraHPortS" in api:
                async with aiofiles.open('Host Port Selectors/HTML/Host Port Selectors.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraPortBlk" in api:
                async with aiofiles.open('Port Blocks/HTML/Port Blocks.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraRsAccBaseGrp" in api:
                async with aiofiles.open('Access Policy Group Source Relationships/HTML/Access Policy Group Source Relationships.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraRsAttEntP" in api:
                async with aiofiles.open('Attachable Access Entity Profiles Source Relationships/HTML/Attachable Access Entity Profiles Source Relationships.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraRsDomP" in api:
                async with aiofiles.open('Domain Profile Source Relationships/HTML/Domain Profile Source Relationships.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraRsSpAccGrp" in api:
                async with aiofiles.open('Spine Access Policy Groups/HTML/Spine Access Policy Groups.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraRsVlanNs" in api:
                async with aiofiles.open('VLAN Namespace Source Relationships/HTML/VLAN Namespace Source Relationships.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraSHPortS" in api:
                async with aiofiles.open('Spine Host Port Selectors/HTML/Spine Host Port Selectors.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraSpAccPortP" in api:
                async with aiofiles.open('Spine Access Port Profiles/HTML/Spine Access Port Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "infraWiNode" in api:
                async with aiofiles.open('Wired Nodes/HTML/Wired Nodes.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ipNexthopP" in api:
                async with aiofiles.open('Static Route Next Hop Policies/HTML/Static Route Next Hop Policies.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ipRouteP" in api:
                async with aiofiles.open('Route Policies/HTML/Route Policies.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ipv4Addr" in api:
                async with aiofiles.open('IPv4 Addresses/HTML/IPv4 Addresses.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ipv4Dom" in api:
                async with aiofiles.open('IPv4 Domains/HTML/IPv4 Domains.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ipv4Entity" in api:
                async with aiofiles.open('IPv4 Entities/HTML/IPv4 Entities.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ipv4If" in api:
                async with aiofiles.open('IPv4 Interfaces/HTML/IPv4 Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ipv4Inst" in api:
                async with aiofiles.open('IPv4 Instances/HTML/IPv4 Instances.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ipv4Nexthop" in api:
                async with aiofiles.open('IPv4 Next Hop/HTML/IPv4 Next Hop.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ipv4Route" in api:
                async with aiofiles.open('IPv4 Routes/HTML/IPv4 Routes.html', mode='w' ) as f:
                    await f.write(html_output)

            if "isisAdjEp" in api:
                async with aiofiles.open('ISIS Adjacency Endpoints/HTML/ISIS Adjacency Endpoints.html', mode='w' ) as f:
                    await f.write(html_output)

            if "isisDTEp" in api:
                async with aiofiles.open('ISIS Discovered Tunnel Endpoints/HTML/ISIS Discovered Tunnel Endpoints.html', mode='w' ) as f:
                    await f.write(html_output)

            if "isisDom" in api:
                if "Lvl" in api:
                    async with aiofiles.open('ISIS Domains Level/HTML/ISIS Domains Level.html', mode='w' ) as f:
                        await f.write(html_output)
                else:
                    async with aiofiles.open('ISIS Domains/HTML/ISIS Domains.html', mode='w' ) as f:
                        await f.write(html_output)

            if "isisEntity" in api:
                async with aiofiles.open('ISIS Entities/HTML/ISIS Entities.html', mode='w' ) as f:
                    await f.write(html_output)

            if "isisIf" in api:
                if "Lvl" in api:
                    async with aiofiles.open('ISIS Interfaces Level/HTML/ISIS Interfaces Level.html', mode='w' ) as f:
                        await f.write(html_output)
                else:
                    async with aiofiles.open('ISIS Interfaces/HTML/ISIS Interfaces.html', mode='w' ) as f:
                        await f.write(html_output)

            if "isisInst" in api:
                async with aiofiles.open('ISIS Instances/HTML/ISIS Instances.html', mode='w' ) as f:
                    await f.write(html_output)

            if "isisNexthop" in api:
                async with aiofiles.open('ISIS Next Hop/HTML/ISIS Next Hop.html', mode='w' ) as f:
                    await f.write(html_output)

            if "isisRoute" in api:
                async with aiofiles.open('ISIS Routes/HTML/ISIS Routes.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l2BD" in api:
                async with aiofiles.open('L2 Bridge Domains/HTML/L2 Bridge Domains.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l2ExtIf" in api:
                async with aiofiles.open('L2 External Interfaces/HTML/L2 External Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l2RsEthIf" in api:
                async with aiofiles.open('L2 Interface Source Relationships/HTML/L2 Interface Source Relationships.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l2extInstP" in api:
                async with aiofiles.open('L2 External Instance Profiles/HTML/L2 External Instance Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l2extLIfP" in api:
                async with aiofiles.open('L2 External Logical Interface Profiles/HTML/L2 External Logical Interface Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l2extLNodeP" in api:
                async with aiofiles.open('L2 External Logical Node Profiles/HTML/L2 External Logical Node Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l2extRsEBd" in api:
                async with aiofiles.open('L2 EPG Bridge Domain Source Relationships/HTML/L2 EPG Bridge Domain Source Relationships.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l2extRsPathL2OutAtt" in api:
                async with aiofiles.open('L2Out Paths/HTML/L2Out Paths.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3Ctx" in api:
                async with aiofiles.open('L3 Contexts/HTML/L3 Contexts.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3EncRtdIf" in api:
                async with aiofiles.open('L3 Subinterfaces/HTML/L3 Subinterfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3Inst" in api:
                async with aiofiles.open('L3 Instances/HTML/L3 Instances.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3LbRtdIf" in api:
                async with aiofiles.open('L3 Routed Loopback Interfaces/HTML/L3 Routed Loopback Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3RsEncPhysRtdConf" in api:
                async with aiofiles.open('L3 Physical Interface Source Relationships/HTML/L3 Physical Interface Source Relationships.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3RtdIf" in api:
                async with aiofiles.open('L3 Routed Interfaces/HTML/L3 Routed Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3extInstP" in api:
                async with aiofiles.open('L3Out Profiles/HTML/L3Out Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3extIp" in api:
                async with aiofiles.open('L3Out IP Addresses/HTML/L3Out IP Addresses.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3extLIfP" in api:
                async with aiofiles.open('L3 Logical Interface Profiles/HTML/L3 Logical Interface Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3extLNodeP" in api:
                async with aiofiles.open('L3 Logical Node Profiles/HTML/L3 Logical Node Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3extMember" in api:
                async with aiofiles.open('L3Out Members/HTML/L3Out Members.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3extRsEctx" in api:
                async with aiofiles.open('L3 Contexts Source Relationships/HTML/L3 Contexts Source Relationships.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3extRsL3DomAtt" in api:
                async with aiofiles.open('L3 Domains Source Relationships/HTML/L3 Domains Source Relationships.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3extRsNodeL3OutAtt" in api:
                async with aiofiles.open('L3Out Node Source Relationships/HTML/L3Out Node Source Relationships.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3extRsPathL3OutAtt" in api:
                async with aiofiles.open('L3Out Path Source Relationships/HTML/L3Out Path Source Relationships.html', mode='w' ) as f:
                    await f.write(html_output)

            if "l3extSubnet" in api:
                async with aiofiles.open('L3 Subnets/HTML/L3 Subnets.html', mode='w' ) as f:
                    await f.write(html_output)

            if "lacpEntity" in api:
                async with aiofiles.open('LACP Entities/HTML/LACP Entities.html', mode='w' ) as f:
                    await f.write(html_output)

            if "lacpIf" in api:
                async with aiofiles.open('LACP Interfaces/HTML/LACP Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "lacpInst" in api:
                async with aiofiles.open('LACP Instances/HTML/LACP Instances.html', mode='w' ) as f:
                    await f.write(html_output)

            if "leqptLooseNode" in api:
                async with aiofiles.open('External Unmanaged Nodes/HTML/External Unmanaged Nodes.html', mode='w' ) as f:
                    await f.write(html_output)

            if "leqptRsLsNodeToIf" in api:
                async with aiofiles.open('External Unmanaged Nodes Interfaces/HTML/External Unmanaged Nodes Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "lldpAdjEp" in api:
                async with aiofiles.open('LLDP Adjacency Endpoints/HTML/LLDP Adjacency Endpoints.html', mode='w' ) as f:
                    await f.write(html_output)

            if "lldpEntity" in api:
                async with aiofiles.open('LLDP Entities/HTML/LLDP Entities.html', mode='w' ) as f:
                    await f.write(html_output)

            if "lldpIf" in api:
                async with aiofiles.open('LLDP Interfaces/HTML/LLDP Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "lldpInst" in api:
                async with aiofiles.open('LLDP Instances/HTML/LLDP Instances.html', mode='w' ) as f:
                    await f.write(html_output)

            if "mgmtMgmtIf" in api:
                async with aiofiles.open('Management Interfaces/HTML/Management Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ospfAdjEp" in api:
                async with aiofiles.open('OSPF Adjacency Endpoints/HTML/OSPF Adjacency Endpoints.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ospfArea" in api:
                async with aiofiles.open('OSPF Areas/HTML/OSPF Areas.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ospfDb" in api:
                async with aiofiles.open('OSPF Database/HTML/OSPF Database.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ospfDom" in api:
                async with aiofiles.open('OSPF Domains/HTML/OSPF Domains.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ospfEntity" in api:
                async with aiofiles.open('OSPF Entities/HTML/OSPF Entities.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ospfExtP" in api:
                async with aiofiles.open('OSPF External Profiles/HTML/OSPF External Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ospfIf" in api:
                async with aiofiles.open('OSPF Interfaces/HTML/OSPF Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ospfInst" in api:
                async with aiofiles.open('OSPF Instances/HTML/OSPF Instances.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ospfRoute" in api:
                async with aiofiles.open('OSPF Routes/HTML/OSPF Routes.html', mode='w' ) as f:
                    await f.write(html_output)

            if "ospfUcNexthop" in api:
                async with aiofiles.open('OSPF Unicast Next Hop/HTML/OSPF Unicast Next Hop.html', mode='w' ) as f:
                    await f.write(html_output)

            if "pcAggrIf" in api:
                async with aiofiles.open('Port Channel Aggregate Interfaces/HTML/Port Channel Aggregate Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "pcRsMbrIfs" in api:
                async with aiofiles.open('Port Channel Member Interfaces/HTML/Port Channel Member Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "sviIf" in api:
                async with aiofiles.open('SVIs/HTML/SVIs.html', mode='w' ) as f:
                    await f.write(html_output)

            if "tunnelIf" in api:
                async with aiofiles.open('Tunnel Interfaces/HTML/Tunnel Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "uribv4Db" in api:
                async with aiofiles.open('Unicast Route Database/HTML/Unicast Route Database.html', mode='w' ) as f:
                    await f.write(html_output)

            if "uribv4Dom" in api:
                async with aiofiles.open('Unicast Route Domains/HTML/Unicast Route Domains.html', mode='w' ) as f:
                    await f.write(html_output)

            if "uribv4Entity" in api:
                async with aiofiles.open('Unicast Route Entities/HTML/Unicast Route Entities.html', mode='w' ) as f:
                    await f.write(html_output)

            if "uribv4Nexthop" in api:
                async with aiofiles.open('Unicast Route Next Hop/HTML/Unicast Route Next Hop.html', mode='w' ) as f:
                    await f.write(html_output)

            if "uribv4Route" in api:
                async with aiofiles.open('Unicast Routes/HTML/Unicast Routes.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vlanCktEp" in api:
                async with aiofiles.open('VLAN Endpoint Group Encapsulation/HTML/VLAN Endpoint Group Encapsulation.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vmmCtrlrP" in api:
                async with aiofiles.open('VMM Controller Profiles/HTML/VMM Controller Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vmmDomP" in api:
                async with aiofiles.open('VMM Domain Profiles/HTML/VMM Domain Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vmmProvP" in api:
                async with aiofiles.open('VMM Provider Profiles/HTML/VMM Provider Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vmmUsrAccP" in api:
                async with aiofiles.open('VMM User Profiles/HTML/VMM User Profiles.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vpcDom" in api:
                async with aiofiles.open('VPC Domains/HTML/VPC Domains.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vpcEntity" in api:
                async with aiofiles.open('VPC Entities/HTML/VPC Entities.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vpcIf" in api:
                async with aiofiles.open('VPC Interfaces/HTML/VPC Interfaces.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vpcInst" in api:
                async with aiofiles.open('VPC Instances/HTML/VPC Instances.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vpcRsVpcConf" in api:
                async with aiofiles.open('VPC Configurations/HTML/VPC Configurations.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vzAny" in api:
                async with aiofiles.open('vzAny/HTML/vzAny.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vzFilter" in api:
                async with aiofiles.open('vzFilters/HTML/vzFilters.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vzRsAnyToCons" in api:
                async with aiofiles.open('vzAny To Consumers/HTML/vzAny To Consumers.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vzRsAnyToProv" in api:
                async with aiofiles.open('vzAny To Providers/HTML/vzAny To Providers.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vzRsDenyRule" in api:
                async with aiofiles.open('vzDeny Rules/HTML/vzDeny Rules.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vzRsIf" in api:
                async with aiofiles.open('vzInterface Source Relationships/HTML/vzInterface Source Relationships.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vzRsSubjFiltAtt" in api:
                async with aiofiles.open('Contract Subjects Filter Attributes/HTML/Contract Subjects Filter Attributes.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vzRtCons" in api:
                async with aiofiles.open('Contract Consumers Root/HTML/Contract Consumers Root.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vzRtProv" in api:
                async with aiofiles.open('Contract Providers Root/HTML/Contract Providers Root.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vzRuleOwner" in api:
                async with aiofiles.open('vzRule Owner/HTML/vzRule Owner.html', mode='w' ) as f:
                    await f.write(html_output)

            if "vzTaboo" in api:
                async with aiofiles.open('vzTaboo/HTML/vzTaboo.html', mode='w' ) as f:
                    await f.write(html_output)

    async def mindmap_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        mindmap_template = env.get_template('aci_mindmap.j2')
        for api, payload in json.loads(parsed_json):
            mindmap_output = await mindmap_template.render_async(api = api,
                                             data_to_template = payload)
            if "Tenant" in api:
                async with aiofiles.open('Tenant/Mindmap/Tenants.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "AEPg" in api:
                async with aiofiles.open('EPGs/Mindmap/EPGs.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fvBD" in api:
                async with aiofiles.open('Bridge Domains/Mindmap/Bridge Domains.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fvCtx" in api:
                async with aiofiles.open('Contexts/Mindmap/Contexts.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "Ap" in api:
                async with aiofiles.open('Application Profiles/Mindmap/Application Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3extOut" in api:
                async with aiofiles.open('L3Outs/Mindmap/L3Outs.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l2extOut" in api:
                async with aiofiles.open('L2Outs/Mindmap/L2Outs.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "topSystem" in api:
                if "?" not in api:
                    async with aiofiles.open('Top System/Mindmap/Top System.md', mode='w' ) as f:
                        await f.write(mindmap_output)

            if "fvSubnet" in api:
                async with aiofiles.open('Subnets/Mindmap/Subnets.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fvCEp" in api:
                async with aiofiles.open('Endpoints/Mindmap/Endpoints.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fabricNode" in api:
                async with aiofiles.open('Fabric Nodes/Mindmap/Fabric Nodes.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l1PhysIf" in api:
                async with aiofiles.open('Physical Interfaces/Mindmap/Physical Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraAccPortP" in api:
                async with aiofiles.open('Leaf Interface Profiles/Mindmap/Leaf Interface Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraSpAccPortP" in api:
                async with aiofiles.open('Spine Interface Profiles/Mindmap/Spine Interface Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraNodeP" in api:
                async with aiofiles.open('Leaf Switch Profiles/Mindmap/Leaf Switch Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraSpineP" in api:
                async with aiofiles.open('Spine Switch Profiles/Mindmap/Spine Switch Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fvnsVlanInstP" in api:
                async with aiofiles.open('VLAN Pools/Mindmap/VLAN Pools.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraAttEntityP" in api:
                async with aiofiles.open('Attachable Access Entity Profiles/Mindmap/Attachable Access Entity Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vzBrCP" in api:
                async with aiofiles.open('Contracts/Mindmap/Contracts.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vzEntry" in api:
                async with aiofiles.open('vzEntries/Mindmap/vzEntries.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "physDomP" in api:
                async with aiofiles.open('Physical Domains/Mindmap/Physical Domains.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3extDomP" in api:
                async with aiofiles.open('L3 Domains/Mindmap/L3 Domains.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "qosClass" in api:
                async with aiofiles.open('QOS Classes/Mindmap/QOS Classes.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "faultSummary" in api:
                async with aiofiles.open('Fault Summary/Mindmap/Fault Summary.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "aaaModLR" in api:
                async with aiofiles.open('Audit Log/Mindmap/Audit Log.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fvIp" in api:
                async with aiofiles.open('IP Addresses/Mindmap/IP Addresses.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eventRecord" in api:
                async with aiofiles.open('Events/Mindmap/Events.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "licenseEntitlement" in api:
                async with aiofiles.open('License Entitlements/Mindmap/License Entitlements.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "bgpRRNodePEp" in api:
                async with aiofiles.open('BGP Route Reflectors/Mindmap/BGP Route Reflectors.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraPortS" in api:
                async with aiofiles.open('Interface Policies/Mindmap/Interface Policies.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraProfile" in api:
                async with aiofiles.open('Interface Profiles/Mindmap/Interface Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fabricPod" in api:
                async with aiofiles.open('Fabric Pods/Mindmap/Fabric Pods.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fabricPath" in api:
                if "fabricPathEp" in api:
                    if "Cont" in api:
                        async with aiofiles.open('Fabric Path Endpoint Containers/Mindmap/Fabric Path Endpoint Containers.md', mode='w' ) as f:
                            await f.write(mindmap_output)
                    else:
                        async with aiofiles.open('Fabric Path Endpoints/Mindmap/Fabric Path Endpoints.md', mode='w' ) as f:
                            await f.write(mindmap_output)
                else:
                    async with aiofiles.open('Fabric Paths/Mindmap/Fabric Paths.md', mode='w' ) as f:
                        await f.write(mindmap_output)

            if "rtctrlSubjP" in api:
                async with aiofiles.open('Prefix List/Mindmap/Prefix List.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "rtctrlMatchRtDest" in api:
                async with aiofiles.open('Prefix List Detailed/Mindmap/Prefix List Detailed.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "aaaUser" in api:
                async with aiofiles.open('Users/Mindmap/Users.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "aaaDomain" in api:
                async with aiofiles.open('Security Domains/Mindmap/Security Domains.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vzSubj" in api:
                async with aiofiles.open('Contract Subjects/Mindmap/Contract Subjects.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "topology/health" in api:
                async with aiofiles.open('Health/Mindmap/Health.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "pkiFabricNodeSSLCertificate" in api:
                async with aiofiles.open('Fabric Node SSL Certificates/Mindmap/Fabric Node SSL Certificates.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "tn-" in api:
                if "health" in api:
                    async with aiofiles.open('Tenant Health/Mindmap/Tenant Health.md', mode='w' ) as f:
                        await f.write(mindmap_output)

            if "firmwareCtrlrRunning" in api:
                async with aiofiles.open('Fabric Membership/Mindmap/Fabric Membership.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraWiNode" in api:
                async with aiofiles.open('Cluster Health/Mindmap/Cluster Health.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vnsMDev" in api:
                async with aiofiles.open('Device Packages/Mindmap/Device Packages.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "cnwAggrIf" in api:
                async with aiofiles.open('Cluster Aggregate Interfaces/Mindmap/Cluster Aggregate Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3Inst" in api:
                async with aiofiles.open('L3 Interfaces/Mindmap/L3 Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "actrlEntity" in api:
                async with aiofiles.open('Access Control Entities/Mindmap/Access Control Entities.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "actrlInst" in api:
                async with aiofiles.open('Access Control Instances/Mindmap/Access Control Instances.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "actrlRule" in api:
                async with aiofiles.open('Access Control Rules/Mindmap/Access Control Rules.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "actrlScope" in api:
                async with aiofiles.open('Access Control Scopes/Mindmap/Access Control Scopes.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "cnwPhysIf" in api:
                async with aiofiles.open('Cluster Physical Interfaces/Mindmap/Cluster Physical Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "compCtrlr" in api:
                async with aiofiles.open('Compute Controllers/Mindmap/Compute Controllers.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "compDom" in api:
                async with aiofiles.open('Compute Domains/Mindmap/Compute Domains.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "compEpPD" in api:
                async with aiofiles.open('Compute Endpoint Policy Descriptions/Mindmap/Compute Endpoint Policy Descriptions.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "compProv" in api:
                async with aiofiles.open('Compute Providers/Mindmap/Compute Providers.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "arpAdjEp" in api:
                async with aiofiles.open('ARP Adjacency Endpoints/Mindmap/ARP Adjacency Endpoints.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "arpDb" in api:
                async with aiofiles.open('ARP Database/Mindmap/ARP Database.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "arpDom" in api:
                async with aiofiles.open('ARP Domain/Mindmap/ARP Domain.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "arpEntity" in api:
                async with aiofiles.open('ARP Entity/Mindmap/ARP Entity.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "arpIf" in api:
                async with aiofiles.open('ARP Interfaces/Mindmap/ARP Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "arpInst" in api:
                async with aiofiles.open('ARP Instances/Mindmap/ARP Instances.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "bgpDom" in api:
                if "bgpDomAf" in api:
                    async with aiofiles.open('BGP Domain Address Families/Mindmap/BGP Domain Address Families.md', mode='w' ) as f:
                        await f.write(mindmap_output)
                else:
                    async with aiofiles.open('BGP Domains/Mindmap/BGP Domains.md', mode='w' ) as f:
                        await f.write(mindmap_output)

            if "bgpEntity" in api:
                async with aiofiles.open('BGP Entities/Mindmap/BGP Entities.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "bgpInst" in api:
                if "InstPol" in api:
                    async with aiofiles.open('BGP Instances Policy/Mindmap/BGP Instances Policy.md', mode='w' ) as f:
                        await f.write(mindmap_output)
                else:
                    async with aiofiles.open('BGP Instances/Mindmap/BGP Instances.md', mode='w' ) as f:
                        await f.write(mindmap_output)

            if "bgpPeer" in api:
                if "bgpPeerAf" in api:
                    async with aiofiles.open('BGP Peers AF Entries/Mindmap/BGP Peers AF Entries.md', mode='w' ) as f:
                        await f.write(mindmap_output)
                elif "bgpPeerEntry" in api:
                    async with aiofiles.open('BGP Peers Entries/Mindmap/BGP Peers Entries.md', mode='w' ) as f:
                        await f.write(mindmap_output)
                else:
                    async with aiofiles.open('BGP Peers/Mindmap/BGP Peers.md', mode='w' ) as f:
                        await f.write(mindmap_output)

            if "bgpRRP" in api:
                async with aiofiles.open('BGP Route Reflector Policies/Mindmap/BGP Route Reflector Policies.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "cdpAdjEp" in api:
                async with aiofiles.open('CDP Adjacency Endpoints/Mindmap/CDP Adjacency Endpoints.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "cdpEntity" in api:
                async with aiofiles.open('CDP Entities/Mindmap/CDP Entities.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "cdpIf" in api:
                async with aiofiles.open('CDP Interfaces/Mindmap/CDP Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "cdpInst" in api:
                async with aiofiles.open('CDP Instances/Mindmap/CDP Instances.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "cdpIntfAddr" in api:
                async with aiofiles.open('CDP Interface Addresses/Mindmap/CDP Interface Addresses.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "cdpMgmtAddr" in api:
                async with aiofiles.open('CDP Management Addresses/Mindmap/CDP Management Addresses.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "cnwRsMbrIfs" in api:
                async with aiofiles.open('Cluster RS Member Interfaces/Mindmap/Cluster RS Member Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "compRsDomP" in api:
                async with aiofiles.open('Compute RS Domain Policies/Mindmap/Compute RS Domain Policies.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptBSlot" in api:
                async with aiofiles.open('Equipment Board Slots/Mindmap/Equipment Board Slots.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptBoard" in api:
                async with aiofiles.open('Equipment Boards/Mindmap/Equipment Boards.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptCPU" in api:
                async with aiofiles.open('Equipment CPUs/Mindmap/Equipment CPUs.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptCh" in api:
                async with aiofiles.open('Equipment Chassis/Mindmap/Equipment Chassis.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptDimm" in api:
                async with aiofiles.open('Equipment DIMMs/Mindmap/Equipment DIMMs.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptExtCh" in api:
                async with aiofiles.open('Equipment Fabric Extenders/Mindmap/Equipment Fabric Extenders.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptFabP" in api:
                async with aiofiles.open('Equipment Fabric Ports/Mindmap/Equipment Fabric Ports.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptFan" in api:
                async with aiofiles.open('Equipment Fans/Mindmap/Equipment Fans.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptFpga" in api:
                async with aiofiles.open('Equipment Field Programmable Gate Arrays/Mindmap/Equipment Field Programmable Gate Arrays.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptFt" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Fan Tray Slots/Mindmap/Equipment Fan Tray Slots.md', mode='w' ) as f:
                        await f.write(mindmap_output)
                else:
                    async with aiofiles.open('Equipment Fan Trays/Mindmap/Equipment Fan Trays.md', mode='w' ) as f:
                        await f.write(mindmap_output)

            if "eqptIndLed" in api:
                async with aiofiles.open('Equipment Indicator LEDs/Mindmap/Equipment Indicator LEDs.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptLC" in api:
                async with aiofiles.open('Equipment Line Cards/Mindmap/Equipment Line Cards.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptLeafP" in api:
                async with aiofiles.open('Equipment Leaf Ports/Mindmap/Equipment Leaf Ports.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptLocLed" in api:
                async with aiofiles.open('Equipment Port Locator LEDs/Mindmap/Equipment Port Locator LEDs.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptPsu" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Power Supply Slots/Mindmap/Equipment Power Supply Slots.md', mode='w' ) as f:
                        await f.write(mindmap_output)
                else:
                    async with aiofiles.open('Equipment Power Supplies/Mindmap/Equipment Power Supplies.md', mode='w' ) as f:
                        await f.write(mindmap_output)

            if "eqptRsIoPPhysConf" in api:
                async with aiofiles.open('Equipment RS IO Port Physical Configs/Mindmap/Equipment RS IO Port Physical Configs.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptSensor" in api:
                async with aiofiles.open('Equipment Sensors/Mindmap/Equipment Sensors.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptSpCmnBlk" in api:
                async with aiofiles.open('Equipment SP Common Blocks/Mindmap/Equipment SP Common Blocks.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptSpromLc" in api:
                async with aiofiles.open('Equipment SPROM LCs/Mindmap/Equipment SPROM LCs.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptSpromPsu" in api:
                if "Blk" in api:
                    async with aiofiles.open('Equipment SPROM Power Supply Blocks/Mindmap/Equipment SPROM Power Supply Blocks.md', mode='w' ) as f:
                        await f.write(mindmap_output)
                else:
                    async with aiofiles.open('Equipment SPROM Power Supplies/Mindmap/Equipment SPROM Power Supplies.md', mode='w' ) as f:
                        await f.write(mindmap_output)

            if "eqptSpromSup" in api:
                async with aiofiles.open('Equipment SPROM Supervisors/Mindmap/Equipment SPROM Supervisors.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptStorage" in api:
                async with aiofiles.open('Equipment Storage/Mindmap/Equipment Storage.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "eqptSupC" in api:
                if "Slot" in api:
                    async with aiofiles.open('Equipment Supervisor Slots/Mindmap/Equipment Supervisor Slots.md', mode='w' ) as f:
                        await f.write(mindmap_output)
                else:
                    async with aiofiles.open('Equipment Supervisors/Mindmap/Equipment Supervisors.md', mode='w' ) as f:
                        await f.write(mindmap_output)

            if "ethpmPhysIf" in api:
                async with aiofiles.open('Ethernet Port Manager Physical Interfaces/Mindmap/Ethernet Port Manager Physical Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fabricExtPathEpCont" in api:
                async with aiofiles.open('Fabric Extended Path Endpoint Containers/Mindmap/Fabric Extended Path Endpoint Containers.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fabricInst" in api:
                async with aiofiles.open('Fabric Instances/Mindmap/Fabric Instances.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fabricLink" in api:
                if "Cont" in api:
                    async with aiofiles.open('Fabric Link Containers/Mindmap/Fabric Link Containers.md', mode='w' ) as f:
                        await f.write(mindmap_output)
                else:
                    async with aiofiles.open('Fabric Links/Mindmap/Fabric Links.md', mode='w' ) as f:
                        await f.write(mindmap_output)

            if "fabricLooseLink" in api:
                async with aiofiles.open('Fabric Loose Links/Mindmap/Fabric Loose Links.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fabricLooseNode" in api:
                async with aiofiles.open('Fabric Loose Nodes/Mindmap/Fabric Loose Nodes.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fabricProtPathEpCont" in api:
                async with aiofiles.open('Fabric Protected Path Endpoint Containers/Mindmap/Fabric Protected Path Endpoint Containers.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fcEntity" in api:
                async with aiofiles.open('Fibre Channel Entities/Mindmap/Fibre Channel Entities.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "firmwareCardRunning" in api:
                async with aiofiles.open('Firmware Card Running/Mindmap/Firmware Card Running.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "firmwareCompRunning" in api:
                async with aiofiles.open('Firmware Compute Running/Mindmap/Firmware Compute Running.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "firmwareRunning" in api:
                async with aiofiles.open('Firmware Running/Mindmap/Firmware Running.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fvEpPCont" in api:
                async with aiofiles.open('Endpoint Profile Containers/Mindmap/Endpoint Profile Containers.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fvLocale" in api:
                async with aiofiles.open('Locales/Mindmap/Locales.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fvRsBDToOut" in api:
                async with aiofiles.open('Bridge Domains To Outside/Mindmap/Bridge Domains To Outside.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fvRsBd" in api:
                async with aiofiles.open('EPG Bridge Domain Links/Mindmap/EPG Bridge Domain Links.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fvRsCEpToPathEp" in api:
                async with aiofiles.open('Endpoints To Paths/Mindmap/Endpoints To Paths.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fvRsCons" in api:
                if "If" in api:
                    async with aiofiles.open('Contract Consumer Interfaces/Mindmap/Contract Consumer Interfaces.md', mode='w' ) as f:
                        await f.write(mindmap_output)
                else:
                    async with aiofiles.open('Contract Consumers/Mindmap/Contract Consumers.md', mode='w' ) as f:
                        await f.write(mindmap_output)

            if "fvRsCtx" in api:
                async with aiofiles.open('Context Source Relationships/Mindmap/Context Source Relationships.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fvRsDomAtt" in api:
                async with aiofiles.open('Domain Attachments/Mindmap/Domain Attachments.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fvRsPathAtt" in api:
                async with aiofiles.open('Path Attachments/Mindmap/Path Attachments.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fvRsProv" in api:
                async with aiofiles.open('Contract Providers/Mindmap/Contract Providers.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fvRtBd" in api:
                async with aiofiles.open('Bridge Domains Target Relationships/Mindmap/Bridge Domains Target Relationships.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fvRtCtx" in api:
                async with aiofiles.open('Contexts Target Relationships/Mindmap/Contexts Target Relationships.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fvnsEncapBlk" in api:
                async with aiofiles.open('VLAN Encapsulation Blocks/Mindmap/VLAN Encapsulation Blocks.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "fvnsVlanInstP" in api:
                async with aiofiles.open('VLAN Namespace Policies/Mindmap/VLAN Namespace Policies.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraAccBndlGrp" in api:
                async with aiofiles.open('Access Bundle Groups/Mindmap/Access Bundle Groups.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraAccPortGrp" in api:
                async with aiofiles.open('Access Port Groups/Mindmap/Access Port Groups.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraAccPortP" in api:
                async with aiofiles.open('Access Port Profiles/Mindmap/Access Port Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraContr" in api:
                async with aiofiles.open('Controllers/Mindmap/Controllers.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraFexP" in api:
                async with aiofiles.open('FEX Policies/Mindmap/FEX Policies.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraFuncP" in api:
                async with aiofiles.open('Function Policies/Mindmap/Function Policies.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraHPortS" in api:
                async with aiofiles.open('Host Port Selectors/Mindmap/Host Port Selectors.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraPortBlk" in api:
                async with aiofiles.open('Port Blocks/Mindmap/Port Blocks.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraRsAccBaseGrp" in api:
                async with aiofiles.open('Access Policy Group Source Relationships/Mindmap/Access Policy Group Source Relationships.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraRsAttEntP" in api:
                async with aiofiles.open('Attachable Access Entity Profiles Source Relationships/Mindmap/Attachable Access Entity Profiles Source Relationships.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraRsDomP" in api:
                async with aiofiles.open('Domain Profile Source Relationships/Mindmap/Domain Profile Source Relationships.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraRsSpAccGrp" in api:
                async with aiofiles.open('Spine Access Policy Groups/Mindmap/Spine Access Policy Groups.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraRsVlanNs" in api:
                async with aiofiles.open('VLAN Namespace Source Relationships/Mindmap/VLAN Namespace Source Relationships.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraSHPortS" in api:
                async with aiofiles.open('Spine Host Port Selectors/Mindmap/Spine Host Port Selectors.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraSpAccPortP" in api:
                async with aiofiles.open('Spine Access Port Profiles/Mindmap/Spine Access Port Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "infraWiNode" in api:
                async with aiofiles.open('Wired Nodes/Mindmap/Wired Nodes.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ipNexthopP" in api:
                async with aiofiles.open('Static Route Next Hop Policies/Mindmap/Static Route Next Hop Policies.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ipRouteP" in api:
                async with aiofiles.open('Route Policies/Mindmap/Route Policies.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ipv4Addr" in api:
                async with aiofiles.open('IPv4 Addresses/Mindmap/IPv4 Addresses.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ipv4Dom" in api:
                async with aiofiles.open('IPv4 Domains/Mindmap/IPv4 Domains.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ipv4Entity" in api:
                async with aiofiles.open('IPv4 Entities/Mindmap/IPv4 Entities.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ipv4If" in api:
                async with aiofiles.open('IPv4 Interfaces/Mindmap/IPv4 Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ipv4Inst" in api:
                async with aiofiles.open('IPv4 Instances/Mindmap/IPv4 Instances.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ipv4Nexthop" in api:
                async with aiofiles.open('IPv4 Next Hop/Mindmap/IPv4 Next Hop.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ipv4Route" in api:
                async with aiofiles.open('IPv4 Routes/Mindmap/IPv4 Routes.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "isisAdjEp" in api:
                async with aiofiles.open('ISIS Adjacency Endpoints/Mindmap/ISIS Adjacency Endpoints.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "isisDTEp" in api:
                async with aiofiles.open('ISIS Discovered Tunnel Endpoints/Mindmap/ISIS Discovered Tunnel Endpoints.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "isisDom" in api:
                if "Lvl" in api:
                    async with aiofiles.open('ISIS Domains Level/Mindmap/ISIS Domains Level.md', mode='w' ) as f:
                        await f.write(mindmap_output)
                else:
                    async with aiofiles.open('ISIS Domains/Mindmap/ISIS Domains.md', mode='w' ) as f:
                        await f.write(mindmap_output)

            if "isisEntity" in api:
                async with aiofiles.open('ISIS Entities/Mindmap/ISIS Entities.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "isisIf" in api:
                if "Lvl" in api:
                    async with aiofiles.open('ISIS Interfaces Level/Mindmap/ISIS Interfaces Level.md', mode='w' ) as f:
                        await f.write(mindmap_output)
                else:
                    async with aiofiles.open('ISIS Interfaces/Mindmap/ISIS Interfaces.md', mode='w' ) as f:
                        await f.write(mindmap_output)

            if "isisInst" in api:
                async with aiofiles.open('ISIS Instances/Mindmap/ISIS Instances.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "isisNexthop" in api:
                async with aiofiles.open('ISIS Next Hop/Mindmap/ISIS Next Hop.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "isisRoute" in api:
                async with aiofiles.open('ISIS Routes/Mindmap/ISIS Routes.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l2BD" in api:
                async with aiofiles.open('L2 Bridge Domains/Mindmap/L2 Bridge Domains.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l2ExtIf" in api:
                async with aiofiles.open('L2 External Interfaces/Mindmap/L2 External Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l2RsEthIf" in api:
                async with aiofiles.open('L2 Interface Source Relationships/Mindmap/L2 Interface Source Relationships.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l2extInstP" in api:
                async with aiofiles.open('L2 External Instance Profiles/Mindmap/L2 External Instance Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l2extLIfP" in api:
                async with aiofiles.open('L2 External Logical Interface Profiles/Mindmap/L2 External Logical Interface Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l2extLNodeP" in api:
                async with aiofiles.open('L2 External Logical Node Profiles/Mindmap/L2 External Logical Node Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l2extRsEBd" in api:
                async with aiofiles.open('L2 EPG Bridge Domain Source Relationships/Mindmap/L2 EPG Bridge Domain Source Relationships.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l2extRsPathL2OutAtt" in api:
                async with aiofiles.open('L2Out Paths/Mindmap/L2Out Paths.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3Ctx" in api:
                async with aiofiles.open('L3 Contexts/Mindmap/L3 Contexts.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3EncRtdIf" in api:
                async with aiofiles.open('L3 Subinterfaces/Mindmap/L3 Subinterfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3Inst" in api:
                async with aiofiles.open('L3 Instances/Mindmap/L3 Instances.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3LbRtdIf" in api:
                async with aiofiles.open('L3 Routed Loopback Interfaces/Mindmap/L3 Routed Loopback Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3RsEncPhysRtdConf" in api:
                async with aiofiles.open('L3 Physical Interface Source Relationships/Mindmap/L3 Physical Interface Source Relationships.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3RtdIf" in api:
                async with aiofiles.open('L3 Routed Interfaces/Mindmap/L3 Routed Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3extInstP" in api:
                async with aiofiles.open('L3Out Profiles/Mindmap/L3Out Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3extIp" in api:
                async with aiofiles.open('L3Out IP Addresses/Mindmap/L3Out IP Addresses.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3extLIfP" in api:
                async with aiofiles.open('L3 Logical Interface Profiles/Mindmap/L3 Logical Interface Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3extLNodeP" in api:
                async with aiofiles.open('L3 Logical Node Profiles/Mindmap/L3 Logical Node Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3extMember" in api:
                async with aiofiles.open('L3Out Members/Mindmap/L3Out Members.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3extRsEctx" in api:
                async with aiofiles.open('L3 Contexts Source Relationships/Mindmap/L3 Contexts Source Relationships.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3extRsL3DomAtt" in api:
                async with aiofiles.open('L3 Domains Source Relationships/Mindmap/L3 Domains Source Relationships.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3extRsNodeL3OutAtt" in api:
                async with aiofiles.open('L3Out Node Source Relationships/Mindmap/L3Out Node Source Relationships.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3extRsPathL3OutAtt" in api:
                async with aiofiles.open('L3Out Path Source Relationships/Mindmap/L3Out Path Source Relationships.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "l3extSubnet" in api:
                async with aiofiles.open('L3 Subnets/Mindmap/L3 Subnets.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "lacpEntity" in api:
                async with aiofiles.open('LACP Entities/Mindmap/LACP Entities.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "lacpIf" in api:
                async with aiofiles.open('LACP Interfaces/Mindmap/LACP Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "lacpInst" in api:
                async with aiofiles.open('LACP Instances/Mindmap/LACP Instances.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "leqptLooseNode" in api:
                async with aiofiles.open('External Unmanaged Nodes/Mindmap/External Unmanaged Nodes.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "leqptRsLsNodeToIf" in api:
                async with aiofiles.open('External Unmanaged Nodes Interfaces/Mindmap/External Unmanaged Nodes Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "lldpAdjEp" in api:
                async with aiofiles.open('LLDP Adjacency Endpoints/Mindmap/LLDP Adjacency Endpoints.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "lldpEntity" in api:
                async with aiofiles.open('LLDP Entities/Mindmap/LLDP Entities.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "lldpIf" in api:
                async with aiofiles.open('LLDP Interfaces/Mindmap/LLDP Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "lldpInst" in api:
                async with aiofiles.open('LLDP Instances/Mindmap/LLDP Instances.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "mgmtMgmtIf" in api:
                async with aiofiles.open('Management Interfaces/Mindmap/Management Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ospfAdjEp" in api:
                async with aiofiles.open('OSPF Adjacency Endpoints/Mindmap/OSPF Adjacency Endpoints.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ospfArea" in api:
                async with aiofiles.open('OSPF Areas/Mindmap/OSPF Areas.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ospfDb" in api:
                async with aiofiles.open('OSPF Database/Mindmap/OSPF Database.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ospfDom" in api:
                async with aiofiles.open('OSPF Domains/Mindmap/OSPF Domains.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ospfEntity" in api:
                async with aiofiles.open('OSPF Entities/Mindmap/OSPF Entities.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ospfExtP" in api:
                async with aiofiles.open('OSPF External Profiles/Mindmap/OSPF External Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ospfIf" in api:
                async with aiofiles.open('OSPF Interfaces/Mindmap/OSPF Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ospfInst" in api:
                async with aiofiles.open('OSPF Instances/Mindmap/OSPF Instances.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ospfRoute" in api:
                async with aiofiles.open('OSPF Routes/Mindmap/OSPF Routes.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "ospfUcNexthop" in api:
                async with aiofiles.open('OSPF Unicast Next Hop/Mindmap/OSPF Unicast Next Hop.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "pcAggrIf" in api:
                async with aiofiles.open('Port Channel Aggregate Interfaces/Mindmap/Port Channel Aggregate Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "pcRsMbrIfs" in api:
                async with aiofiles.open('Port Channel Member Interfaces/Mindmap/Port Channel Member Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "sviIf" in api:
                async with aiofiles.open('SVIs/Mindmap/SVIs.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "tunnelIf" in api:
                async with aiofiles.open('Tunnel Interfaces/Mindmap/Tunnel Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "uribv4Db" in api:
                async with aiofiles.open('Unicast Route Database/Mindmap/Unicast Route Database.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "uribv4Dom" in api:
                async with aiofiles.open('Unicast Route Domains/Mindmap/Unicast Route Domains.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "uribv4Entity" in api:
                async with aiofiles.open('Unicast Route Entities/Mindmap/Unicast Route Entities.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "uribv4Nexthop" in api:
                async with aiofiles.open('Unicast Route Next Hop/Mindmap/Unicast Route Next Hop.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "uribv4Route" in api:
                async with aiofiles.open('Unicast Routes/Mindmap/Unicast Routes.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vlanCktEp" in api:
                async with aiofiles.open('VLAN Endpoint Group Encapsulation/Mindmap/VLAN Endpoint Group Encapsulation.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vmmCtrlrP" in api:
                async with aiofiles.open('VMM Controller Profiles/Mindmap/VMM Controller Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vmmDomP" in api:
                async with aiofiles.open('VMM Domain Profiles/Mindmap/VMM Domain Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vmmProvP" in api:
                async with aiofiles.open('VMM Provider Profiles/Mindmap/VMM Provider Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vmmUsrAccP" in api:
                async with aiofiles.open('VMM User Profiles/Mindmap/VMM User Profiles.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vpcDom" in api:
                async with aiofiles.open('VPC Domains/Mindmap/VPC Domains.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vpcEntity" in api:
                async with aiofiles.open('VPC Entities/Mindmap/VPC Entities.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vpcIf" in api:
                async with aiofiles.open('VPC Interfaces/Mindmap/VPC Interfaces.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vpcInst" in api:
                async with aiofiles.open('VPC Instances/Mindmap/VPC Instances.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vpcRsVpcConf" in api:
                async with aiofiles.open('VPC Configurations/Mindmap/VPC Configurations.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vzAny" in api:
                async with aiofiles.open('vzAny/Mindmap/vzAny.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vzFilter" in api:
                async with aiofiles.open('vzFilters/Mindmap/vzFilters.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vzRsAnyToCons" in api:
                async with aiofiles.open('vzAny To Consumers/Mindmap/vzAny To Consumers.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vzRsAnyToProv" in api:
                async with aiofiles.open('vzAny To Providers/Mindmap/vzAny To Providers.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vzRsDenyRule" in api:
                async with aiofiles.open('vzDeny Rules/Mindmap/vzDeny Rules.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vzRsIf" in api:
                async with aiofiles.open('vzInterface Source Relationships/Mindmap/vzInterface Source Relationships.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vzRsSubjFiltAtt" in api:
                async with aiofiles.open('Contract Subjects Filter Attributes/Mindmap/Contract Subjects Filter Attributes.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vzRtCons" in api:
                async with aiofiles.open('Contract Consumers Root/Mindmap/Contract Consumers Root.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vzRtProv" in api:
                async with aiofiles.open('Contract Providers Root/Mindmap/Contract Providers Root.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vzRuleOwner" in api:
                async with aiofiles.open('vzRule Owner/Mindmap/vzRule Owner.md', mode='w' ) as f:
                    await f.write(mindmap_output)

            if "vzTaboo" in api:
                async with aiofiles.open('vzTaboo/Mindmap/vzTaboo.md', mode='w' ) as f:
                    await f.write(mindmap_output)

    async def all_files(self, parsed_json):
        await asyncio.gather(self.json_file(parsed_json), self.yaml_file(parsed_json), self.csv_file(parsed_json), self.markdown_file(parsed_json), self.html_file(parsed_json), self.mindmap_file(parsed_json))

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
