export const id=73487;export const ids=[73487];export const modules={37456:(e,t,i)=>{i.d(t,{a:()=>s});const n=(0,i(58034).n)((e=>{history.replaceState({scrollPosition:e},"")}),300),s=e=>t=>({kind:"method",placement:"prototype",key:t.key,descriptor:{set(e){n(e),this[`__${String(t.key)}`]=e},get(){return this[`__${String(t.key)}`]||history.state?.scrollPosition},enumerable:!0,configurable:!0},finisher(i){const n=i.prototype.connectedCallback;i.prototype.connectedCallback=function(){n.call(this);const i=this[t.key];i&&this.updateComplete.then((()=>{const t=this.renderRoot.querySelector(e);t&&setTimeout((()=>{t.scrollTop=i}),0)}))}}})},7127:(e,t,i)=>{i.d(t,{p:()=>s});const n=[" ",": "],s=(e,t)=>{const i=e.toLowerCase();for(const s of n){const n=`${t}${s}`;if(i.startsWith(n)){const t=e.substring(n.length);if(t.length)return o(t.substr(0,t.indexOf(" ")))?t:t[0].toUpperCase()+t.slice(1)}}},o=e=>e.toLowerCase()!==e},45657:(e,t,i)=>{i.d(t,{KT:()=>_,Bi:()=>m,ZI:()=>f,Yp:()=>g});i(89655),i(54774),i(24545),i(51855),i(82130),i(31743),i(22328),i(4959),i(62435),i(253),i(2075),i(94438),i(54846),i(16891);var n=i(94872),s=i(213),o=i(65459),a=i(19244);var r=i(7127),l=i(2682),c=i(96915),d=i(46092),h=i(71443),u=i(57273);const p=new Set(["automation","configurator","device_tracker","event","geo_location","notify","persistent_notification","script","sun","tag","todo","zone",...n.gt]),y=new Set(["mobile_app"]),f=(e,t)=>({type:"grid",cards:e.map((e=>({type:"tile",entity:e,show_entity_picture:["camera","image","person"].includes((0,s.m)(e))||void 0}))),...t}),m=(e,t,i,o=!0)=>{const c=[],d=[],h=i.title?i.title.toLowerCase():void 0,u=[];for(const i of t){const t=e[i],n=(0,s.m)(i);if("alarm_control_panel"===n){const e={type:"alarm-panel",entity:i};c.push(e)}else if("camera"===n){const e={type:"picture-entity",entity:i};c.push(e)}else if("image"===n){const e={type:"picture",image_entity:i};c.push(e)}else if("climate"===n){const t={type:"thermostat",entity:i,features:(e[i]?.attributes?.hvac_modes?.length??0)>1?[{type:"climate-hvac-modes",hvac_modes:e[i]?.attributes?.hvac_modes}]:void 0};c.push(t)}else if("humidifier"===n){const e={type:"humidifier",entity:i,features:[{type:"humidifier-toggle"}]};c.push(e)}else if("media_player"===n){const e={type:"media-control",entity:i};c.push(e)}else if("plant"===n){const e={type:"plant-status",entity:i};c.push(e)}else if("weather"===n){const e={type:"weather-forecast",entity:i,show_forecast:!1};c.push(e)}else if(!o||"scene"!==n&&"script"!==n){let e;const n=h&&t&&(e=(0,r.p)((0,a.u)(t),h))?{entity:i,name:e}:i;d.push(n)}else{const e={entity:i,show_icon:!0,show_name:!0};let n;h&&t&&(n=(0,r.p)((0,a.u)(t),h))&&(e.name=n),u.push(e)}}if(d.sort(((t,i)=>{const o="string"==typeof t?t:t.entity,r="string"==typeof i?i:i.entity,c=n.JF.includes((0,s.m)(o))?"sensor":"control";return c!==(n.JF.includes((0,s.m)(r))?"sensor":"control")?"sensor"===c?1:-1:(0,l.x)("string"==typeof t?e[t]?(0,a.u)(e[t]):"":t.name||"","string"==typeof i?e[i]?(0,a.u)(e[i]):"":i.name||"")})),0===d.length&&u.length>0)return m(e,t,i,!1);if(d.length>0||u.length>0){const e={type:"entities",entities:d,...i};u.length>0&&(e.footer={type:"buttons",entities:u}),c.unshift(e)}return c.length<2?c:[{type:"grid",square:!1,columns:1,cards:c}]},_=(e,t)=>{const i=[];for(const e of t){const t={type:"entity",entity:e};i.push(t)}return i},g=(e,t,i,n,r,f,_,g,b)=>{const v=((e,t)=>{const i={},n=new Set(Object.values(t).filter((e=>e.entity_category||e.platform&&y.has(e.platform)||e.hidden)).map((e=>e.entity_id)));for(const t of Object.keys(e)){const s=e[t];p.has((0,o.t)(s))||n.has(s.entity_id)||(i[t]=e[t])}return i})(n,i),k={};for(const e of Object.keys(v)){const t=v[e];t.attributes.order&&(k[e]=t.attributes.order)}const w=((e,t,i,n)=>{const s={...n},o={},a={};for(const n of Object.values(i)){const i=n.area_id||n.device_id&&t[n.device_id]?.area_id;i&&i in e&&n.entity_id in s?(i in o||(o[i]=[]),o[i].push(s[n.entity_id]),delete s[n.entity_id]):n.device_id&&n.device_id in t&&n.entity_id in s&&(n.device_id in a||(a[n.device_id]=[]),a[n.device_id].push(s[n.entity_id]),delete s[n.entity_id])}for(const[e,t]of Object.entries(a))1===t.length&&(s[t[0].entity_id]=t[0],delete a[e]);return{areasWithEntities:o,devicesWithEntities:a,otherEntities:s}})(e,t,i,v);if(_?.hidden)for(const e of _.hidden)delete w.areasWithEntities[e];g&&(w.devicesWithEntities={},w.otherEntities={});const $=(e=>{const t=[],i={};return Object.keys(e).forEach((n=>{const o=e[n];"group"===(0,s.m)(n)?t.push(o):i[n]=o})),t.forEach((e=>e.attributes.entity_id.forEach((e=>{delete i[e]})))),{groups:t,ungrouped:i}})(w.otherEntities);$.groups.sort(((e,t)=>k[e.entity_id]-k[t.entity_id]));const E=[];for(const e of $.groups)E.push(...m(n,e.attributes.entity_id,{title:(0,a.u)(e),show_header_toggle:"hidden"!==e.attributes.control}));const C=((e,t,i,n,s)=>{const r={};for(const e of Object.keys(s)){const t=s[e],i=(0,o.t)(t);i in r||(r[i]=[]),r[i].push(t.entity_id)}const c=[];if("person"in r){const e=[];if(1===r.person.length)c.push({type:"entities",entities:r.person});else{let t,i="";for(const n of r.person){const o=s[n];let a=o.attributes.entity_picture;if(!a){if(void 0===t){const e=getComputedStyle(document.body);t=encodeURIComponent(e.getPropertyValue("--light-primary-color").trim()),i=encodeURIComponent((e.getPropertyValue("--text-light-primary-color")||e.getPropertyValue("--primary-text-color")).trim())}a=`data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 50 50' width='50' height='50' style='background-color:${t}'%3E%3Cg%3E%3Ctext font-family='roboto' x='50%25' y='50%25' text-anchor='middle' stroke='${i}' font-size='1.3em' dy='.3em'%3E${(0,h._2)(o.attributes.friendly_name||"")}%3C/text%3E%3C/g%3E%3C/svg%3E`}e.push({type:"picture-entity",entity:n,aspect_ratio:"1",show_name:!1,image:a})}c.push({type:"grid",square:!0,columns:3,cards:e})}delete r.person}const p=[];for(const e of u.L)e in r&&(p.push(...r[e]),delete r[e]);const y={};for(const t of Object.keys(r))y[t]=(0,d.p$)(e,t);p.length&&(r._helpers=p,y._helpers=e("ui.panel.lovelace.strategy.original-states.helpers")),Object.keys(r).sort(((e,t)=>(0,l.x)(y[e],y[t]))).forEach((e=>{c.push(...m(s,r[e].sort(((e,t)=>(0,l.x)((0,a.u)(s[e]),(0,a.u)(s[t])))),{title:y[e]}))}));const f={path:t,title:i,cards:c};return n&&(f.icon=n),f})(r,"default_view","Home",undefined,$.ungrouped),x=[],j=Object.keys(w.areasWithEntities).sort((0,c.dj)(e,_?.order));for(const t of j){const i=w.areasWithEntities[t],s=e[t];x.push(...m(n,i.map((e=>e.entity_id)),{title:s.name}))}const O=[],z=Object.entries(w.devicesWithEntities).sort(((e,i)=>{const n=t[e[0]],s=t[i[0]];return(0,l.x)(n.name_by_user||n.name||"",s.name_by_user||s.name||"")}));for(const[e,i]of z){const s=t[e];O.push(...m(n,i.map((e=>e.entity_id)),{title:s.name_by_user||s.name||r("ui.panel.config.devices.unnamed_device",{type:r(`ui.panel.config.devices.type.${s.entry_type||"device"}`)})}))}let S;if(f&&!b){const e=f.energy_sources.find((e=>"grid"===e.type));e&&e.flow_from.length>0&&(S={title:r("ui.panel.lovelace.cards.energy.energy_distribution.title_today"),type:"energy-distribution",link_dashboard:!0})}return C.cards.unshift(...x,...E,...S?[S]:[]),C.cards.push(...O),C}},4790:(e,t,i)=>{i.a(e,(async(e,t)=>{try{var n=i(36312),s=i(15112),o=i(77706),a=i(94100),r=i(34897),l=(i(28664),i(12675),i(13740)),c=e([l]);l=(c.then?(await c)():c)[0];(0,n.A)([(0,o.EM)("hui-entity-picker-table")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,o.MZ)({type:Boolean,attribute:"no-label-float"})],key:"noLabelFloat",value:()=>!1},{kind:"field",decorators:[(0,o.MZ)({type:Array})],key:"entities",value:void 0},{kind:"method",key:"render",value:function(){return s.qy` <ha-data-table .hass="${this.hass}" selectable .id="${"entity_id"}" .columns="${this._columns(this.narrow)}" .data="${this.entities}" .searchLabel="${this.hass.localize("ui.panel.lovelace.unused_entities.search")}" .noLabelFloat="${this.noLabelFloat}" .noDataText="${this.hass.localize("ui.panel.lovelace.unused_entities.no_data")}" @selection-changed="${this._handleSelectionChanged}"></ha-data-table> `}},{kind:"field",key:"_columns",value(){return(0,a.A)((e=>{const t={icon:{title:"",label:this.hass.localize("ui.panel.lovelace.unused_entities.state_icon"),type:"icon",template:e=>s.qy` <state-badge @click="${this._handleEntityClicked}" .hass="${this.hass}" .stateObj="${e.stateObj}"></state-badge> `},name:{title:this.hass.localize("ui.panel.lovelace.unused_entities.entity"),sortable:!0,filterable:!0,flex:2,main:!0,direction:"asc",template:t=>s.qy` <div @click="${this._handleEntityClicked}" style="cursor:pointer"> ${t.name} ${e?s.qy` <div class="secondary">${t.entity_id}</div> `:""} </div> `}};return t.entity_id={title:this.hass.localize("ui.panel.lovelace.unused_entities.entity_id"),sortable:!0,filterable:!0,hidden:e},t.domain={title:this.hass.localize("ui.panel.lovelace.unused_entities.domain"),sortable:!0,filterable:!0,hidden:e},t.last_changed={title:this.hass.localize("ui.panel.lovelace.unused_entities.last_changed"),type:"numeric",sortable:!0,hidden:e,template:e=>s.qy` <ha-relative-time .hass="${this.hass}" .datetime="${e.last_changed}" capitalize></ha-relative-time> `},t}))}},{kind:"method",key:"_handleSelectionChanged",value:function(e){const t=e.detail.value;(0,r.r)(this,"selected-changed",{selectedEntities:t})}},{kind:"method",key:"_handleEntityClicked",value:function(e){const t=e.target.closest(".mdc-data-table__row").rowId;(0,r.r)(this,"hass-more-info",{entityId:t})}},{kind:"get",static:!0,key:"styles",value:function(){return s.AH`ha-data-table{--data-table-border-width:0;height:100%}`}}]}}),s.WF);t()}catch(e){t(e)}}))}};
//# sourceMappingURL=73487.bx7FjH7KhpU.js.map