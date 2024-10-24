export const id=44439;export const ids=[44439];export const modules={96961:(e,t,a)=>{a.d(t,{JW:()=>f,OW:()=>u,PO:()=>_,VN:()=>c,XG:()=>p,eB:()=>g,gZ:()=>m,hM:()=>l,k2:()=>s,lU:()=>v,nc:()=>C,vX:()=>h,z1:()=>n});a(24545),a(51855),a(82130),a(31743),a(22328),a(4959),a(62435),a(253),a(2075),a(94438),a(16891);var i=a(16312),r=a(66754),d=a(33922),o=a(23712);let n=function(e){return e.THREAD="thread",e.WIFI="wifi",e.ETHERNET="ethernet",e.UNKNOWN="unknown",e}({});const s=e=>e.auth.external?.config.canCommissionMatter,c=async e=>{if((0,d.x)(e,"thread")){const t=(await(0,o.sL)(e)).datasets.find((e=>e.preferred));if(t)return e.auth.external.fireMessage({type:"matter/commission",payload:{active_operational_dataset:(await(0,o.dy)(e,t.dataset_id)).tlv,border_agent_id:t.preferred_border_agent_id,mac_extended_address:t.preferred_extended_address,extended_pan_id:t.extended_pan_id}})}return e.auth.external.fireMessage({type:"matter/commission"})},l=(e,t)=>{let a;const d=(0,r.Ag)(e.connection,(e=>{if(!a)return void(a=new Set(Object.values(e).filter((e=>e.identifiers.find((e=>"matter"===e[0])))).map((e=>e.id))));const r=Object.values(e).filter((e=>e.identifiers.find((e=>"matter"===e[0]))&&!a.has(e.id)));r.length&&(d(),a=void 0,t?.(),(0,i.o)(`/config/devices/device/${r[0].id}`))}));return()=>{d(),a=void 0}},_=(e,t)=>e.callWS({type:"matter/commission",code:t}),p=(e,t)=>e.callWS({type:"matter/commission_on_network",pin:t}),v=(e,t,a)=>e.callWS({type:"matter/set_wifi_credentials",network_name:t,password:a}),m=(e,t)=>e.callWS({type:"matter/set_thread",thread_operation_dataset:t}),g=(e,t)=>e.callWS({type:"matter/node_diagnostics",device_id:t}),u=(e,t)=>e.callWS({type:"matter/ping_node",device_id:t}),C=(e,t)=>e.callWS({type:"matter/open_commissioning_window",device_id:t}),h=(e,t,a)=>e.callWS({type:"matter/remove_matter_fabric",device_id:t,fabric_index:a}),f=(e,t)=>e.callWS({type:"matter/interview_node",device_id:t})},23712:(e,t,a)=>{a.d(t,{It:()=>n,W4:()=>c,dy:()=>o,l1:()=>l,rY:()=>s,sL:()=>d,wm:()=>r});class i{constructor(){this.routers=void 0,this.routers={}}processEvent(e){return"router_discovered"===e.type?this.routers[e.key]=e.data:"router_removed"===e.type&&delete this.routers[e.key],Object.values(this.routers)}}const r=(e,t)=>{const a=new i;return e.connection.subscribeMessage((e=>t(a.processEvent(e))),{type:"thread/discover_routers"})},d=e=>e.callWS({type:"thread/list_datasets"}),o=(e,t)=>e.callWS({type:"thread/get_dataset_tlv",dataset_id:t}),n=(e,t,a)=>e.callWS({type:"thread/add_dataset_tlv",source:t,tlv:a}),s=(e,t)=>e.callWS({type:"thread/delete_dataset",dataset_id:t}),c=(e,t)=>e.callWS({type:"thread/set_preferred_dataset",dataset_id:t}),l=(e,t,a,i)=>e.callWS({type:"thread/set_preferred_border_agent",dataset_id:t,border_agent_id:a,extended_address:i})},44439:(e,t,a)=>{a.r(t),a.d(t,{getMatterDeviceActions:()=>p,getMatterDeviceDefaultActions:()=>_});a(89655);var i=a(96961),r=a(34897);const d=()=>a.e(58409).then(a.bind(a,58409)),o=()=>a.e(24387).then(a.bind(a,24387)),n=()=>Promise.all([a.e(61060),a.e(50240),a.e(68137)]).then(a.bind(a,68137)),s=()=>Promise.all([a.e(61060),a.e(50240),a.e(81650)]).then(a.bind(a,81650));var c=a(16312);const l="M12,1L8,5H11V14H13V5H16M18,23H6C4.89,23 4,22.1 4,21V9A2,2 0 0,1 6,7H9V9H6V21H18V9H15V7H18A2,2 0 0,1 20,9V21A2,2 0 0,1 18,23Z",_=(e,t,a)=>{if(null!==a.via_device_id)return[];const i=[];return i.push({label:t.localize("ui.panel.config.matter.device_actions.ping_device"),icon:"M12 3C6.5 3 2 6.6 2 11C2 13.1 3 15.1 4.8 16.5C4.8 17.1 4.4 18.7 2 21C2 21 5.5 21 8.5 18.5C9.6 18.8 10.8 19 12 19C17.5 19 22 15.4 22 11S17.5 3 12 3M13 15H11V13H13V15M14.8 10C14.5 10.4 14.1 10.6 13.7 10.8C13.4 11 13.3 11.1 13.2 11.3C13 11.5 13 11.7 13 12H11C11 11.5 11.1 11.2 11.3 10.9C11.5 10.7 11.9 10.4 12.4 10.1C12.7 10 12.9 9.8 13 9.6C13.1 9.4 13.2 9.1 13.2 8.9C13.2 8.6 13.1 8.4 12.9 8.2C12.7 8 12.4 7.9 12.1 7.9C11.8 7.9 11.6 8 11.4 8.1C11.2 8.2 11.1 8.4 11.1 8.7H9.1C9.2 8 9.5 7.4 10 7C10.5 6.6 11.2 6.5 12.1 6.5C13 6.5 13.8 6.7 14.3 7.1C14.8 7.5 15.1 8.1 15.1 8.8C15.2 9.2 15.1 9.6 14.8 10Z",action:()=>{return t=e,i={device_id:a.id},void(0,r.r)(t,"show-dialog",{dialogTag:"dialog-matter-ping-node",dialogImport:o,dialogParams:i});var t,i}}),i},p=async(e,t,a)=>{if(null!==a.via_device_id)return[];const o=await(0,i.eB)(t,a.id),_=[];return o.available&&(_.push({label:t.localize("ui.panel.config.matter.device_actions.open_commissioning_window"),icon:l,action:()=>{return t=e,i={device_id:a.id},void(0,r.r)(t,"show-dialog",{dialogTag:"dialog-matter-open-commissioning-window",dialogImport:n,dialogParams:i});var t,i}}),_.push({label:t.localize("ui.panel.config.matter.device_actions.manage_fabrics"),icon:l,action:()=>{return t=e,i={device_id:a.id},void(0,r.r)(t,"show-dialog",{dialogTag:"dialog-matter-manage-fabrics",dialogImport:s,dialogParams:i});var t,i}}),_.push({label:t.localize("ui.panel.config.matter.device_actions.reinterview_device"),icon:"M12,3C17.5,3 22,6.58 22,11C22,15.42 17.5,19 12,19C10.76,19 9.57,18.82 8.47,18.5C5.55,21 2,21 2,21C4.33,18.67 4.7,17.1 4.75,16.5C3.05,15.07 2,13.13 2,11C2,6.58 6.5,3 12,3M17,12V10H15V12H17M13,12V10H11V12H13M9,12V10H7V12H9Z",action:()=>{return t=e,i={device_id:a.id},void(0,r.r)(t,"show-dialog",{dialogTag:"dialog-matter-reinterview-node",dialogImport:d,dialogParams:i});var t,i}})),o.network_type===i.z1.THREAD&&_.push({label:t.localize("ui.panel.config.matter.device_actions.view_thread_network"),icon:"M4.93,4.93C3.12,6.74 2,9.24 2,12C2,14.76 3.12,17.26 4.93,19.07L6.34,17.66C4.89,16.22 4,14.22 4,12C4,9.79 4.89,7.78 6.34,6.34L4.93,4.93M19.07,4.93L17.66,6.34C19.11,7.78 20,9.79 20,12C20,14.22 19.11,16.22 17.66,17.66L19.07,19.07C20.88,17.26 22,14.76 22,12C22,9.24 20.88,6.74 19.07,4.93M7.76,7.76C6.67,8.85 6,10.35 6,12C6,13.65 6.67,15.15 7.76,16.24L9.17,14.83C8.45,14.11 8,13.11 8,12C8,10.89 8.45,9.89 9.17,9.17L7.76,7.76M16.24,7.76L14.83,9.17C15.55,9.89 16,10.89 16,12C16,13.11 15.55,14.11 14.83,14.83L16.24,16.24C17.33,15.15 18,13.65 18,12C18,10.35 17.33,8.85 16.24,7.76M12,10A2,2 0 0,0 10,12A2,2 0 0,0 12,14A2,2 0 0,0 14,12A2,2 0 0,0 12,10Z",action:()=>(0,c.o)("/config/thread")}),_}}};
//# sourceMappingURL=44439.LRCHFul-gX8.js.map