export const id=48878;export const ids=[48878];export const modules={96979:(e,t,i)=>{i.d(t,{I:()=>o});i(89655),i(253),i(54846),i(78266);class s{constructor(e=window.localStorage){this.storage=void 0,this._storage={},this._listeners={},this.storage=e,e===window.localStorage&&window.addEventListener("storage",(e=>{e.key&&this.hasKey(e.key)&&(this._storage[e.key]=e.newValue?JSON.parse(e.newValue):e.newValue,this._listeners[e.key]&&this._listeners[e.key].forEach((t=>t(e.oldValue?JSON.parse(e.oldValue):e.oldValue,this._storage[e.key]))))}))}addFromStorage(e){if(!this._storage[e]){const t=this.storage.getItem(e);t&&(this._storage[e]=JSON.parse(t))}}subscribeChanges(e,t){return this._listeners[e]?this._listeners[e].push(t):this._listeners[e]=[t],()=>{this.unsubscribeChanges(e,t)}}unsubscribeChanges(e,t){if(!(e in this._listeners))return;const i=this._listeners[e].indexOf(t);-1!==i&&this._listeners[e].splice(i,1)}hasKey(e){return e in this._storage}getValue(e){return this._storage[e]}setValue(e,t){const i=this._storage[e];this._storage[e]=t;try{void 0===t?this.storage.removeItem(e):this.storage.setItem(e,JSON.stringify(t))}catch(e){}finally{this._listeners[e]&&this._listeners[e].forEach((e=>e(i,t)))}}}const a={},o=e=>t=>{const i=e.storage||"localStorage";let o;i&&i in a?o=a[i]:(o=new s(window[i]),a[i]=o);const n=String(t.key),r=e.key||String(t.key),l=t.initializer?t.initializer():void 0;o.addFromStorage(r);const d=!1!==e.subscribe?e=>o.subscribeChanges(r,((i,s)=>{e.requestUpdate(t.key,i)})):void 0,c=()=>o.hasKey(r)?e.deserializer?e.deserializer(o.getValue(r)):o.getValue(r):l;return{kind:"method",placement:"prototype",key:t.key,descriptor:{set(i){((i,s)=>{let a;e.state&&(a=c()),o.setValue(r,e.serializer?e.serializer(s):s),e.state&&i.requestUpdate(t.key,a)})(this,i)},get:()=>c(),enumerable:!0,configurable:!0},finisher(i){if(e.state&&e.subscribe){const e=i.prototype.connectedCallback,t=i.prototype.disconnectedCallback;i.prototype.connectedCallback=function(){e.call(this),this[`__unbsubLocalStorage${n}`]=d?.(this)},i.prototype.disconnectedCallback=function(){t.call(this),this[`__unbsubLocalStorage${n}`]?.(),this[`__unbsubLocalStorage${n}`]=void 0}}e.state&&i.createProperty(t.key,{noAccessor:!0,...e.stateOptions})}}}},45395:(e,t,i)=>{var s=i(36312),a=i(68689),o=i(46724),n=i(38973),r=i(77706),l=i(15112),d=i(74005);(0,s.A)([(0,r.EM)("ha-fab")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"firstUpdated",value:function(e){(0,a.A)(i,"firstUpdated",this,3)([e]),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)")}},{kind:"field",static:!0,key:"styles",value:()=>[n.R,l.AH`:host .mdc-fab--extended .mdc-fab__icon{margin-inline-start:-8px;margin-inline-end:12px;direction:var(--direction)}`,"rtl"===d.G.document.dir?l.AH`:host .mdc-fab--extended .mdc-fab__icon{direction:rtl}`:l.AH``]}]}}),o.n)},77661:(e,t,i)=>{var s=i(36312),a=(i(7986),i(15112)),o=i(77706);i(88400);(0,s.A)([(0,o.EM)("ha-help-tooltip")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"position",value:()=>"top"},{kind:"method",key:"render",value:function(){return a.qy` <ha-svg-icon .path="${"M15.07,11.25L14.17,12.17C13.45,12.89 13,13.5 13,15H11V14.5C11,13.39 11.45,12.39 12.17,11.67L13.41,10.41C13.78,10.05 14,9.55 14,9C14,7.89 13.1,7 12,7A2,2 0 0,0 10,9H8A4,4 0 0,1 12,5A4,4 0 0,1 16,9C16,9.88 15.64,10.67 15.07,11.25M13,19H11V17H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12C22,6.47 17.5,2 12,2Z"}"></ha-svg-icon> <simple-tooltip offset="4" .position="${this.position}" .fitToVisibleBounds="${!0}">${this.label}</simple-tooltip> `}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`ha-svg-icon{--mdc-icon-size:var(--ha-help-tooltip-size, 14px);color:var(--ha-help-tooltip-color,var(--disabled-text-color))}`}}]}}),a.WF)},71443:(e,t,i)=>{i.d(t,{TK:()=>r,_2:()=>d,eR:()=>a,hG:()=>l,hU:()=>o,kg:()=>n,wj:()=>s,xg:()=>c});i(89655),i(16891);const s="system-admin",a="system-users",o=async e=>e.callWS({type:"config/auth/list"}),n=async(e,t,i,s)=>e.callWS({type:"config/auth/create",name:t,group_ids:i,local_only:s}),r=async(e,t,i)=>e.callWS({...i,type:"config/auth/update",user_id:t}),l=async(e,t)=>e.callWS({type:"config/auth/delete",user_id:t}),d=e=>e?e.trim().split(" ").slice(0,3).map((e=>e.substring(0,1))).join(""):"?",c=(e,t,i)=>{const s=[],a=t=>e.localize(`ui.panel.config.users.${t}`);return t.is_owner&&s.push(["M12 2C6.47 2 2 6.5 2 12C2 17.5 6.5 22 12 22S22 17.5 22 12 17.5 2 12 2M12 20C7.58 20 4 16.42 4 12C4 7.58 7.58 4 12 4S20 7.58 20 12C20 16.42 16.42 20 12 20M8 14L7 8L10 10L12 7L14 10L17 8L16 14H8M8.56 16C8.22 16 8 15.78 8 15.44V15H16V15.44C16 15.78 15.78 16 15.44 16H8.56Z",a("is_owner")]),i&&t.system_generated&&s.push(["M11,7H15V9H11V11H13A2,2 0 0,1 15,13V15A2,2 0 0,1 13,17H9V15H13V13H11A2,2 0 0,1 9,11V9A2,2 0 0,1 11,7M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4Z",a("is_system")]),t.local_only&&s.push(["M12 20C7.6 20 4 16.4 4 12S7.6 4 12 4 20 7.6 20 12 16.4 20 12 20M12 2C6.5 2 2 6.5 2 12S6.5 22 12 22 22 17.5 22 12 17.5 2 12 2M11 14H13V17H16V12H18L12 7L6 12H8V17H11V14",a("is_local")]),t.is_active||s.push(["M12 2C17.5 2 22 6.5 22 12S17.5 22 12 22 2 17.5 2 12 6.5 2 12 2M12 4C10.1 4 8.4 4.6 7.1 5.7L18.3 16.9C19.3 15.5 20 13.8 20 12C20 7.6 16.4 4 12 4M16.9 18.3L5.7 7.1C4.6 8.4 4 10.1 4 12C4 16.4 7.6 20 12 20C13.9 20 15.6 19.4 16.9 18.3Z",a("is_not_active")]),s}},48878:(e,t,i)=>{i.r(t),i.d(t,{HaConfigUsers:()=>y});var s=i(36312),a=i(68689),o=(i(54774),i(253),i(2075),i(94438),i(54846),i(16891),i(15112)),n=i(77706),r=i(94100);i(88400);(0,s.A)([(0,n.EM)("ha-data-table-icon")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)()],key:"tooltip",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"path",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_hovered",value:()=>!1},{kind:"method",key:"render",value:function(){return o.qy` ${this._hovered?o.qy`<div>${this.tooltip}</div>`:""} <ha-svg-icon .path="${this.path}"></ha-svg-icon> `}},{kind:"method",key:"firstUpdated",value:function(e){(0,a.A)(i,"firstUpdated",this,3)([e]);const t=()=>{this._hovered=!0},s=()=>{this._hovered=!1};this.addEventListener("mouseenter",t),this.addEventListener("focus",t),this.addEventListener("mouseleave",s),this.addEventListener("blur",s),this.addEventListener("tap",s)}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`:host{display:inline-block;position:relative}ha-svg-icon{color:var(--secondary-text-color)}div{position:absolute;right:28px;inset-inline-end:28px;inset-inline-start:initial;z-index:1002;outline:0;font-size:10px;line-height:1;background-color:var(--simple-tooltip-background,#616161);color:var(--simple-tooltip-text-color,#fff);padding:8px;border-radius:2px}`}}]}}),o.WF);i(45395),i(77661);var l=i(71443),d=i(6121),c=(i(35579),i(25473)),h=i(65045),u=i(34897);const p=()=>Promise.all([i.e(17590),i.e(40821)]).then(i.bind(i,40821));var g=i(96979);const v="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z";let y=(0,s.A)([(0,n.EM)("ha-config-users")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"isWide",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_users",value:()=>[]},{kind:"field",decorators:[(0,g.I)({key:"users-table-sort",state:!1,subscribe:!1})],key:"_activeSorting",value:void 0},{kind:"field",decorators:[(0,g.I)({key:"users-table-grouping",state:!1,subscribe:!1})],key:"_activeGrouping",value:void 0},{kind:"field",decorators:[(0,g.I)({key:"users-table-column-order",state:!1,subscribe:!1})],key:"_activeColumnOrder",value:void 0},{kind:"field",decorators:[(0,g.I)({key:"users-table-hidden-columns",state:!1,subscribe:!1})],key:"_activeHiddenColumns",value:void 0},{kind:"field",decorators:[(0,g.I)({storage:"sessionStorage",key:"users-table-search",state:!0,subscribe:!1})],key:"_filter",value:()=>""},{kind:"field",decorators:[(0,g.I)({key:"users-table-collapsed",state:!1,subscribe:!1})],key:"_activeCollapsed",value:void 0},{kind:"field",key:"_columns",value(){return(0,r.A)(((e,t)=>({name:{title:t("ui.panel.config.users.picker.headers.name"),main:!0,sortable:!0,filterable:!0,direction:"asc",flex:2},username:{title:t("ui.panel.config.users.picker.headers.username"),sortable:!0,filterable:!0,direction:"asc",template:e=>o.qy`${e.username||"—"}`},group:{title:t("ui.panel.config.users.picker.headers.group"),sortable:!0,filterable:!0,groupable:!0,direction:"asc"},is_active:{title:this.hass.localize("ui.panel.config.users.picker.headers.is_active"),type:"icon",sortable:!0,filterable:!0,hidden:e,template:e=>e.is_active?o.qy`<ha-svg-icon .path="${v}"></ha-svg-icon>`:""},system_generated:{title:this.hass.localize("ui.panel.config.users.picker.headers.system"),type:"icon",sortable:!0,filterable:!0,hidden:e,template:e=>e.system_generated?o.qy`<ha-svg-icon .path="${v}"></ha-svg-icon>`:""},local_only:{title:this.hass.localize("ui.panel.config.users.picker.headers.local"),type:"icon",sortable:!0,filterable:!0,hidden:e,template:e=>e.local_only?o.qy`<ha-svg-icon .path="${v}"></ha-svg-icon>`:""},icons:{title:"",label:this.hass.localize("ui.panel.config.users.picker.headers.icon"),type:"icon",sortable:!1,filterable:!1,minWidth:"104px",hidden:!e,showNarrow:!0,template:e=>{const t=(0,l.xg)(this.hass,e,!1);return o.qy`${t.map((([e,t])=>o.qy`<ha-data-table-icon .path="${e}" .tooltip="${t}"></ha-data-table-icon>`))}`}}})))}},{kind:"method",key:"firstUpdated",value:function(e){(0,a.A)(i,"firstUpdated",this,3)([e]),this._fetchUsers()}},{kind:"method",key:"render",value:function(){return o.qy` <hass-tabs-subpage-data-table .hass="${this.hass}" .narrow="${this.narrow}" .route="${this.route}" back-path="/config" .tabs="${c.configSections.persons}" .columns="${this._columns(this.narrow,this.hass.localize)}" .data="${this._userData(this._users,this.hass.localize)}" .columnOrder="${this._activeColumnOrder}" .hiddenColumns="${this._activeHiddenColumns}" @columns-changed="${this._handleColumnsChanged}" .initialGroupColumn="${this._activeGrouping}" .initialCollapsedGroups="${this._activeCollapsed}" .initialSorting="${this._activeSorting}" @sorting-changed="${this._handleSortingChanged}" @grouping-changed="${this._handleGroupingChanged}" @collapsed-changed="${this._handleCollapseChanged}" .filter="${this._filter}" @search-changed="${this._handleSearchChange}" @row-click="${this._editUser}" hasFab clickable> <ha-fab slot="fab" .label="${this.hass.localize("ui.panel.config.users.picker.add_user")}" extended @click="${this._addUser}"> <ha-svg-icon slot="icon" .path="${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}"></ha-svg-icon> </ha-fab> </hass-tabs-subpage-data-table> `}},{kind:"field",key:"_userData",value:()=>(0,r.A)(((e,t)=>e.map((e=>({...e,name:e.name||t("ui.panel.config.users.editor.unnamed_user"),group:t(`groups.${e.group_ids[0]}`)})))))},{kind:"method",key:"_fetchUsers",value:async function(){this._users=await(0,l.hU)(this.hass),this._users.forEach((e=>{e.is_owner&&e.group_ids.unshift("owner")}))}},{kind:"method",key:"_editUser",value:function(e){const t=e.detail.id,i=this._users.find((e=>e.id===t));var s,a;i&&(s=this,a={entry:i,replaceEntry:e=>{this._users=this._users.map((t=>t.id===e.id?e:t))},updateEntry:async e=>{const t=await(0,l.TK)(this.hass,i.id,e);this._users=this._users.map((e=>e===i?t.user:e))},removeEntry:async()=>{if(!await(0,d.showConfirmationDialog)(this,{title:this.hass.localize("ui.panel.config.users.editor.confirm_user_deletion_title",{name:i.name}),text:this.hass.localize("ui.panel.config.users.editor.confirm_user_deletion_text"),dismissText:this.hass.localize("ui.common.cancel"),confirmText:this.hass.localize("ui.common.delete"),destructive:!0}))return!1;try{return await(0,l.hG)(this.hass,i.id),this._users=this._users.filter((e=>e!==i)),!0}catch(e){return!1}}},(0,u.r)(s,"show-dialog",{dialogTag:"dialog-user-detail",dialogImport:p,dialogParams:a}))}},{kind:"method",key:"_addUser",value:function(){(0,h.E)(this,{userAddedCallback:async e=>{e&&(this._users=[...this._users,e])}})}},{kind:"method",key:"_handleSortingChanged",value:function(e){this._activeSorting=e.detail}},{kind:"method",key:"_handleGroupingChanged",value:function(e){this._activeGrouping=e.detail.value}},{kind:"method",key:"_handleCollapseChanged",value:function(e){this._activeCollapsed=e.detail.value}},{kind:"method",key:"_handleSearchChange",value:function(e){this._filter=e.detail.value}},{kind:"method",key:"_handleColumnsChanged",value:function(e){this._activeColumnOrder=e.detail.columnOrder,this._activeHiddenColumns=e.detail.hiddenColumns}}]}}),o.WF)},65045:(e,t,i)=>{i.d(t,{E:()=>o});var s=i(34897);const a=()=>Promise.all([i.e(24290),i.e(38081)]).then(i.bind(i,38081)),o=(e,t)=>{(0,s.r)(e,"show-dialog",{dialogTag:"dialog-add-user",dialogImport:a,dialogParams:t})}}};
//# sourceMappingURL=48878.x71repJB-ew.js.map