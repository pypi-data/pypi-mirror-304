/*! For license information please see 55386.YyQ_zW6O7cI.js.LICENSE.txt */
export const id=55386;export const ids=[55386];export const modules={90410:(e,t,i)=>{i.d(t,{ZS:()=>s,is:()=>r.i});var a,n,d=i(79192),o=i(77706),r=i(19637);const l=null!==(n=null===(a=window.ShadyDOM)||void 0===a?void 0:a.inUse)&&void 0!==n&&n;class s extends r.O{constructor(){super(...arguments),this.disabled=!1,this.containingForm=null,this.formDataListener=e=>{this.disabled||this.setFormData(e.formData)}}findFormElement(){if(!this.shadowRoot||l)return null;const e=this.getRootNode().querySelectorAll("form");for(const t of Array.from(e))if(t.contains(this))return t;return null}connectedCallback(){var e;super.connectedCallback(),this.containingForm=this.findFormElement(),null===(e=this.containingForm)||void 0===e||e.addEventListener("formdata",this.formDataListener)}disconnectedCallback(){var e;super.disconnectedCallback(),null===(e=this.containingForm)||void 0===e||e.removeEventListener("formdata",this.formDataListener),this.containingForm=null}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(e=>{this.dispatchEvent(new Event("change",e))}))}}s.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,d.__decorate)([(0,o.MZ)({type:Boolean})],s.prototype,"disabled",void 0)},45784:(e,t,i)=>{var a=i(36312),n=(i(253),i(5186),i(2075),i(16891),i(4525),i(15112)),d=i(77706),o=i(94100),r=i(34897),l=i(213),s=i(2682),c=i(55792),u=i(66754);i(43536),i(13830);const h=e=>n.qy`<ha-list-item .twoline="${!!e.area}"> <span>${e.name}</span> <span slot="secondary">${e.area}</span> </ha-list-item>`;(0,a.A)([(0,d.EM)("ha-device-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Array,attribute:"exclude-devices"})],key:"excludeDevices",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"deviceFilter",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"required",value:()=>!1},{kind:"field",decorators:[(0,d.wk)()],key:"_opened",value:void 0},{kind:"field",decorators:[(0,d.P)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"field",key:"_init",value:()=>!1},{kind:"field",key:"_getDevices",value(){return(0,o.A)(((e,t,i,a,n,d,o,r,c)=>{if(!e.length)return[{id:"no_devices",area:"",name:this.hass.localize("ui.components.device-picker.no_devices"),strings:[]}];let h={};(a||n||d||r)&&(h=(0,u.g2)(i));let v=e.filter((e=>e.id===this.value||!e.disabled_by));a&&(v=v.filter((e=>{const t=h[e.id];return!(!t||!t.length)&&h[e.id].some((e=>a.includes((0,l.m)(e.entity_id))))}))),n&&(v=v.filter((e=>{const t=h[e.id];return!t||!t.length||i.every((e=>!n.includes((0,l.m)(e.entity_id))))}))),c&&(v=v.filter((e=>!c.includes(e.id)))),d&&(v=v.filter((e=>{const t=h[e.id];return!(!t||!t.length)&&h[e.id].some((e=>{const t=this.hass.states[e.entity_id];return!!t&&(t.attributes.device_class&&d.includes(t.attributes.device_class))}))}))),r&&(v=v.filter((e=>{const t=h[e.id];return!(!t||!t.length)&&t.some((e=>{const t=this.hass.states[e.entity_id];return!!t&&r(t)}))}))),o&&(v=v.filter((e=>e.id===this.value||o(e))));const p=v.map((e=>{const i=(0,u.xn)(e,this.hass,h[e.id]);return{id:e.id,name:i,area:e.area_id&&t[e.area_id]?t[e.area_id].name:this.hass.localize("ui.components.device-picker.no_area"),strings:[i||""]}}));return p.length?1===p.length?p:p.sort(((e,t)=>(0,s.x)(e.name||"",t.name||"",this.hass.locale.language))):[{id:"no_devices",area:"",name:this.hass.localize("ui.components.device-picker.no_match"),strings:[]}]}))}},{kind:"method",key:"open",value:async function(){await this.updateComplete,await(this.comboBox?.open())}},{kind:"method",key:"focus",value:async function(){await this.updateComplete,await(this.comboBox?.focus())}},{kind:"method",key:"updated",value:function(e){if(!this._init&&this.hass||this._init&&e.has("_opened")&&this._opened){this._init=!0;const e=this._getDevices(Object.values(this.hass.devices),this.hass.areas,Object.values(this.hass.entities),this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.excludeDevices);this.comboBox.items=e,this.comboBox.filteredItems=e}}},{kind:"method",key:"render",value:function(){return n.qy` <ha-combo-box .hass="${this.hass}" .label="${void 0===this.label&&this.hass?this.hass.localize("ui.components.device-picker.device"):this.label}" .value="${this._value}" .helper="${this.helper}" .renderer="${h}" .disabled="${this.disabled}" .required="${this.required}" item-id-path="id" item-value-path="id" item-label-path="name" @opened-changed="${this._openedChanged}" @value-changed="${this._deviceChanged}" @filter-changed="${this._filterChanged}"></ha-combo-box> `}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_filterChanged",value:function(e){const t=e.target,i=e.detail.value.toLowerCase();t.filteredItems=i.length?(0,c.H)(i,t.items||[]):t.items}},{kind:"method",key:"_deviceChanged",value:function(e){e.stopPropagation();let t=e.detail.value;"no_devices"===t&&(t=""),t!==this._value&&this._setValue(t)}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,r.r)(this,"value-changed",{value:e}),(0,r.r)(this,"change")}),0)}}]}}),n.WF)},43536:(e,t,i)=>{var a=i(36312),n=i(68689),d=(i(253),i(54846),i(64077)),o=(i(57597),i(68711)),r=i(15112),l=i(77706),s=i(10977),c=i(34897);i(28066),i(13830),i(90431);(0,o.SF)("vaadin-combo-box-item",r.AH`:host{padding:0!important}:host([focused]:not([disabled])){background-color:rgba(var(--rgb-primary-text-color,0,0,0),.12)}:host([selected]:not([disabled])){background-color:transparent;color:var(--mdc-theme-primary);--mdc-ripple-color:var(--mdc-theme-primary);--mdc-theme-text-primary-on-background:var(--mdc-theme-primary)}:host([selected]:not([disabled])):before{background-color:var(--mdc-theme-primary);opacity:.12;content:"";position:absolute;top:0;left:0;width:100%;height:100%}:host([selected][focused]:not([disabled])):before{opacity:.24}:host(:hover:not([disabled])){background-color:transparent}[part=content]{width:100%}[part=checkmark]{display:none}`);(0,a.A)([(0,l.EM)("ha-combo-box")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"validationMessage",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:"error-message"})],key:"errorMessage",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"invalid",value:()=>!1},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"icon",value:()=>!1},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"items",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"filteredItems",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"dataProvider",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:"allow-custom-value",type:Boolean})],key:"allowCustomValue",value:()=>!1},{kind:"field",decorators:[(0,l.MZ)({attribute:"item-value-path"})],key:"itemValuePath",value:()=>"value"},{kind:"field",decorators:[(0,l.MZ)({attribute:"item-label-path"})],key:"itemLabelPath",value:()=>"label"},{kind:"field",decorators:[(0,l.MZ)({attribute:"item-id-path"})],key:"itemIdPath",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"renderer",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"required",value:()=>!1},{kind:"field",decorators:[(0,l.MZ)({type:Boolean,reflect:!0})],key:"opened",value:()=>!1},{kind:"field",decorators:[(0,l.P)("vaadin-combo-box-light",!0)],key:"_comboBox",value:void 0},{kind:"field",decorators:[(0,l.P)("ha-textfield",!0)],key:"_inputElement",value:void 0},{kind:"field",key:"_overlayMutationObserver",value:void 0},{kind:"field",key:"_bodyMutationObserver",value:void 0},{kind:"method",key:"open",value:async function(){await this.updateComplete,this._comboBox?.open()}},{kind:"method",key:"focus",value:async function(){await this.updateComplete,await(this._inputElement?.updateComplete),this._inputElement?.focus()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,n.A)(i,"disconnectedCallback",this,3)([]),this._overlayMutationObserver&&(this._overlayMutationObserver.disconnect(),this._overlayMutationObserver=void 0),this._bodyMutationObserver&&(this._bodyMutationObserver.disconnect(),this._bodyMutationObserver=void 0)}},{kind:"get",key:"selectedItem",value:function(){return this._comboBox.selectedItem}},{kind:"method",key:"setInputValue",value:function(e){this._comboBox.value=e}},{kind:"method",key:"render",value:function(){return r.qy` <vaadin-combo-box-light .itemValuePath="${this.itemValuePath}" .itemIdPath="${this.itemIdPath}" .itemLabelPath="${this.itemLabelPath}" .items="${this.items}" .value="${this.value||""}" .filteredItems="${this.filteredItems}" .dataProvider="${this.dataProvider}" .allowCustomValue="${this.allowCustomValue}" .disabled="${this.disabled}" .required="${this.required}" ${(0,d.d)(this.renderer||this._defaultRowRenderer)} @opened-changed="${this._openedChanged}" @filter-changed="${this._filterChanged}" @value-changed="${this._valueChanged}" attr-for-value="value"> <ha-textfield label="${(0,s.J)(this.label)}" placeholder="${(0,s.J)(this.placeholder)}" ?disabled="${this.disabled}" ?required="${this.required}" validationMessage="${(0,s.J)(this.validationMessage)}" .errorMessage="${this.errorMessage}" class="input" autocapitalize="none" autocomplete="off" autocorrect="off" input-spellcheck="false" .suffix="${r.qy`<div style="width:28px" role="none presentation"></div>`}" .icon="${this.icon}" .invalid="${this.invalid}" .helper="${this.helper}" helperPersistent> <slot name="icon" slot="leadingIcon"></slot> </ha-textfield> ${this.value?r.qy`<ha-svg-icon role="button" tabindex="-1" aria-label="${(0,s.J)(this.hass?.localize("ui.common.clear"))}" class="clear-button" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}" @click="${this._clearValue}"></ha-svg-icon>`:""} <ha-svg-icon role="button" tabindex="-1" aria-label="${(0,s.J)(this.label)}" aria-expanded="${this.opened?"true":"false"}" class="toggle-button" .path="${this.opened?"M7,15L12,10L17,15H7Z":"M7,10L12,15L17,10H7Z"}" @click="${this._toggleOpen}"></ha-svg-icon> </vaadin-combo-box-light> `}},{kind:"field",key:"_defaultRowRenderer",value(){return e=>r.qy`<ha-list-item> ${this.itemLabelPath?e[this.itemLabelPath]:e} </ha-list-item>`}},{kind:"method",key:"_clearValue",value:function(e){e.stopPropagation(),(0,c.r)(this,"value-changed",{value:void 0})}},{kind:"method",key:"_toggleOpen",value:function(e){this.opened?(this._comboBox?.close(),e.stopPropagation()):this._comboBox?.inputElement.focus()}},{kind:"method",key:"_openedChanged",value:function(e){e.stopPropagation();const t=e.detail.value;if(setTimeout((()=>{this.opened=t}),0),(0,c.r)(this,"opened-changed",{value:e.detail.value}),t){const e=document.querySelector("vaadin-combo-box-overlay");e&&this._removeInert(e),this._observeBody()}else this._bodyMutationObserver?.disconnect(),this._bodyMutationObserver=void 0}},{kind:"method",key:"_observeBody",value:function(){"MutationObserver"in window&&!this._bodyMutationObserver&&(this._bodyMutationObserver=new MutationObserver((e=>{e.forEach((e=>{e.addedNodes.forEach((e=>{"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&this._removeInert(e)})),e.removedNodes.forEach((e=>{"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&(this._overlayMutationObserver?.disconnect(),this._overlayMutationObserver=void 0)}))}))})),this._bodyMutationObserver.observe(document.body,{childList:!0}))}},{kind:"method",key:"_removeInert",value:function(e){if(e.inert)return e.inert=!1,this._overlayMutationObserver?.disconnect(),void(this._overlayMutationObserver=void 0);"MutationObserver"in window&&!this._overlayMutationObserver&&(this._overlayMutationObserver=new MutationObserver((e=>{e.forEach((e=>{if("inert"===e.attributeName){const t=e.target;t.inert&&(this._overlayMutationObserver?.disconnect(),this._overlayMutationObserver=void 0,t.inert=!1)}}))})),this._overlayMutationObserver.observe(e,{attributes:!0}))}},{kind:"method",key:"_filterChanged",value:function(e){e.stopPropagation(),(0,c.r)(this,"filter-changed",{value:e.detail.value})}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation(),this.allowCustomValue||(this._comboBox._closeOnBlurIsPrevented=!0);const t=e.detail.value;t!==this.value&&(0,c.r)(this,"value-changed",{value:t||void 0})}},{kind:"get",static:!0,key:"styles",value:function(){return r.AH`:host{display:block;width:100%}vaadin-combo-box-light{position:relative;--vaadin-combo-box-overlay-max-height:calc(45vh - 56px)}ha-textfield{width:100%}ha-textfield>ha-icon-button{--mdc-icon-button-size:24px;padding:2px;color:var(--secondary-text-color)}ha-svg-icon{color:var(--input-dropdown-icon-color);position:absolute;cursor:pointer}.toggle-button{right:12px;top:-10px;inset-inline-start:initial;inset-inline-end:12px;direction:var(--direction)}:host([opened]) .toggle-button{color:var(--primary-color)}.clear-button{--mdc-icon-size:20px;top:-7px;right:36px;inset-inline-start:initial;inset-inline-end:36px;direction:var(--direction)}`}}]}}),r.WF)},13830:(e,t,i)=>{i.d(t,{$:()=>s});var a=i(36312),n=i(68689),d=i(30116),o=i(43389),r=i(15112),l=i(77706);let s=(0,a.A)([(0,l.EM)("ha-list-item")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"renderRipple",value:function(){return this.noninteractive?"":(0,n.A)(i,"renderRipple",this,3)([])}},{kind:"get",static:!0,key:"styles",value:function(){return[o.R,r.AH`:host{padding-left:var(--mdc-list-side-padding-left,var(--mdc-list-side-padding,20px));padding-inline-start:var(--mdc-list-side-padding-left,var(--mdc-list-side-padding,20px));padding-right:var(--mdc-list-side-padding-right,var(--mdc-list-side-padding,20px));padding-inline-end:var(--mdc-list-side-padding-right,var(--mdc-list-side-padding,20px))}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:48px}span.material-icons:first-of-type{margin-inline-start:0px!important;margin-inline-end:var(--mdc-list-item-graphic-margin,16px)!important;direction:var(--direction)!important}span.material-icons:last-of-type{margin-inline-start:auto!important;margin-inline-end:0px!important;direction:var(--direction)!important}.mdc-deprecated-list-item__meta{display:var(--mdc-list-item-meta-display);align-items:center;flex-shrink:0}:host([graphic=icon]:not([twoline])) .mdc-deprecated-list-item__graphic{margin-inline-end:var(--mdc-list-item-graphic-margin,20px)!important}:host([multiline-secondary]){height:auto}:host([multiline-secondary]) .mdc-deprecated-list-item__text{padding:8px 0}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text{text-overflow:initial;white-space:normal;overflow:auto;display:inline-block;margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text{margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text::before{display:none}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text::before{display:none}:host([disabled]){color:var(--disabled-text-color)}:host([noninteractive]){pointer-events:unset}`,"rtl"===document.dir?r.AH`span.material-icons:first-of-type,span.material-icons:last-of-type{direction:rtl!important;--direction:rtl}`:r.AH``]}}]}}),d.J)},2595:(e,t,i)=>{i.r(t),i.d(t,{HaDeviceSelector:()=>p});var a=i(36312),n=i(68689),d=(i(253),i(2075),i(4525),i(15112)),o=i(77706),r=i(94100),l=i(21863),s=i(34897),c=i(66754),u=i(74229),h=i(31265),v=i(29829);i(45784),i(16891);(0,a.A)([(0,o.EM)("ha-devices-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Array})],key:"value",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"required",value:()=>!1},{kind:"field",decorators:[(0,o.MZ)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:"picked-device-label"})],key:"pickedDeviceLabel",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:"pick-device-label"})],key:"pickDeviceLabel",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"deviceFilter",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"method",key:"render",value:function(){if(!this.hass)return d.s6;const e=this._currentDevices;return d.qy` ${e.map((e=>d.qy` <div> <ha-device-picker allow-custom-entity .curValue="${e}" .hass="${this.hass}" .deviceFilter="${this.deviceFilter}" .entityFilter="${this.entityFilter}" .includeDomains="${this.includeDomains}" .excludeDomains="${this.excludeDomains}" .includeDeviceClasses="${this.includeDeviceClasses}" .value="${e}" .label="${this.pickedDeviceLabel}" .disabled="${this.disabled}" @value-changed="${this._deviceChanged}"></ha-device-picker> </div> `))} <div> <ha-device-picker allow-custom-entity .hass="${this.hass}" .helper="${this.helper}" .deviceFilter="${this.deviceFilter}" .entityFilter="${this.entityFilter}" .includeDomains="${this.includeDomains}" .excludeDomains="${this.excludeDomains}" .excludeDevices="${e}" .includeDeviceClasses="${this.includeDeviceClasses}" .label="${this.pickDeviceLabel}" .disabled="${this.disabled}" .required="${this.required&&!e.length}" @value-changed="${this._addDevice}"></ha-device-picker> </div> `}},{kind:"get",key:"_currentDevices",value:function(){return this.value||[]}},{kind:"method",key:"_updateDevices",value:async function(e){(0,s.r)(this,"value-changed",{value:e}),this.value=e}},{kind:"method",key:"_deviceChanged",value:function(e){e.stopPropagation();const t=e.currentTarget.curValue,i=e.detail.value;i!==t&&(void 0===i?this._updateDevices(this._currentDevices.filter((e=>e!==t))):this._updateDevices(this._currentDevices.map((e=>e===t?i:e))))}},{kind:"method",key:"_addDevice",value:async function(e){e.stopPropagation();const t=e.detail.value;if(e.currentTarget.value="",!t)return;const i=this._currentDevices;i.includes(t)||this._updateDevices([...i,t])}},{kind:"field",static:!0,key:"styles",value:()=>d.AH`div{margin-top:8px}`}]}}),d.WF);let p=(0,a.A)([(0,o.EM)("ha-selector-device")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_entitySources",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_configEntries",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"required",value:()=>!0},{kind:"field",key:"_deviceIntegrationLookup",value:()=>(0,r.A)(c.fk)},{kind:"method",key:"_hasIntegration",value:function(e){return e.device?.filter&&(0,l.e)(e.device.filter).some((e=>e.integration))||e.device?.entity&&(0,l.e)(e.device.entity).some((e=>e.integration))}},{kind:"method",key:"willUpdate",value:function(e){e.has("selector")&&void 0!==this.value&&(this.selector.device?.multiple&&!Array.isArray(this.value)?(this.value=[this.value],(0,s.r)(this,"value-changed",{value:this.value})):!this.selector.device?.multiple&&Array.isArray(this.value)&&(this.value=this.value[0],(0,s.r)(this,"value-changed",{value:this.value})))}},{kind:"method",key:"updated",value:function(e){(0,n.A)(i,"updated",this,3)([e]),e.has("selector")&&this._hasIntegration(this.selector)&&!this._entitySources&&(0,u.c)(this.hass).then((e=>{this._entitySources=e})),!this._configEntries&&this._hasIntegration(this.selector)&&(this._configEntries=[],(0,h.VN)(this.hass).then((e=>{this._configEntries=e})))}},{kind:"method",key:"render",value:function(){return this._hasIntegration(this.selector)&&!this._entitySources?d.s6:this.selector.device?.multiple?d.qy` ${this.label?d.qy`<label>${this.label}</label>`:""} <ha-devices-picker .hass="${this.hass}" .value="${this.value}" .helper="${this.helper}" .deviceFilter="${this._filterDevices}" .entityFilter="${this.selector.device?.entity?this._filterEntities:void 0}" .disabled="${this.disabled}" .required="${this.required}"></ha-devices-picker> `:d.qy` <ha-device-picker .hass="${this.hass}" .value="${this.value}" .label="${this.label}" .helper="${this.helper}" .deviceFilter="${this._filterDevices}" .entityFilter="${this.selector.device?.entity?this._filterEntities:void 0}" .disabled="${this.disabled}" .required="${this.required}" allow-custom-entity></ha-device-picker> `}},{kind:"field",key:"_filterDevices",value(){return e=>{if(!this.selector.device?.filter)return!0;const t=this._entitySources?this._deviceIntegrationLookup(this._entitySources,Object.values(this.hass.entities),Object.values(this.hass.devices),this._configEntries):void 0;return(0,l.e)(this.selector.device.filter).some((i=>(0,v.vX)(i,e,t)))}}},{kind:"field",key:"_filterEntities",value(){return e=>(0,l.e)(this.selector.device.entity).some((t=>(0,v.Ru)(t,e,this._entitySources)))}}]}}),d.WF)},90431:(e,t,i)=>{i.d(t,{h:()=>c});var a=i(36312),n=i(68689),d=i(44331),o=i(67449),r=i(15112),l=i(77706),s=i(74005);let c=(0,a.A)([(0,l.EM)("ha-textfield")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"invalid",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:"error-message"})],key:"errorMessage",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"icon",value:()=>!1},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"iconTrailing",value:()=>!1},{kind:"field",decorators:[(0,l.MZ)()],key:"autocomplete",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"autocorrect",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:"input-spellcheck"})],key:"inputSpellcheck",value:void 0},{kind:"field",decorators:[(0,l.P)("input")],key:"formElement",value:void 0},{kind:"method",key:"updated",value:function(e){(0,n.A)(i,"updated",this,3)([e]),(e.has("invalid")||e.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||this.validationMessage||"Invalid":""),(this.invalid||this.validateOnInitialRender||e.has("invalid")&&void 0!==e.get("invalid"))&&this.reportValidity()),e.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),e.has("autocorrect")&&(this.autocorrect?this.formElement.setAttribute("autocorrect",this.autocorrect):this.formElement.removeAttribute("autocorrect")),e.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}},{kind:"method",key:"renderIcon",value:function(e,t=!1){const i=t?"trailing":"leading";return r.qy` <span class="mdc-text-field__icon mdc-text-field__icon--${i}" tabindex="${t?1:-1}"> <slot name="${i}Icon"></slot> </span> `}},{kind:"field",static:!0,key:"styles",value:()=>[o.R,r.AH`.mdc-text-field__input{width:var(--ha-textfield-input-width,100%)}.mdc-text-field:not(.mdc-text-field--with-leading-icon){padding:var(--text-field-padding,0px 16px)}.mdc-text-field__affix--suffix{padding-left:var(--text-field-suffix-padding-left,12px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,12px);padding-inline-end:var(--text-field-suffix-padding-right,0px);direction:ltr}.mdc-text-field--with-leading-icon{padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,16px);direction:var(--direction)}.mdc-text-field--with-leading-icon.mdc-text-field--with-trailing-icon{padding-left:var(--text-field-suffix-padding-left,0px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,0px)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--suffix{color:var(--secondary-text-color)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__icon{color:var(--secondary-text-color)}.mdc-text-field__icon--leading{margin-inline-start:16px;margin-inline-end:8px;direction:var(--direction)}.mdc-text-field__icon--trailing{padding:var(--textfield-icon-trailing-padding,12px)}.mdc-floating-label:not(.mdc-floating-label--float-above){text-overflow:ellipsis;width:inherit;padding-right:30px;padding-inline-end:30px;padding-inline-start:initial;box-sizing:border-box;direction:var(--direction)}input{text-align:var(--text-field-text-align,start)}::-ms-reveal{display:none}:host([no-spinner]) input::-webkit-inner-spin-button,:host([no-spinner]) input::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}:host([no-spinner]) input[type=number]{-moz-appearance:textfield}.mdc-text-field__ripple{overflow:hidden}.mdc-text-field{overflow:var(--text-field-overflow)}.mdc-floating-label{inset-inline-start:16px!important;inset-inline-end:initial!important;transform-origin:var(--float-start);direction:var(--direction);text-align:var(--float-start)}.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label{max-width:calc(100% - 48px - var(--text-field-suffix-padding-left,0px));inset-inline-start:calc(48px + var(--text-field-suffix-padding-left,0px))!important;inset-inline-end:initial!important;direction:var(--direction)}.mdc-text-field__input[type=number]{direction:var(--direction)}.mdc-text-field__affix--prefix{padding-right:var(--text-field-prefix-padding-right,2px);padding-inline-end:var(--text-field-prefix-padding-right,2px);padding-inline-start:initial}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--prefix{color:var(--mdc-text-field-label-ink-color)}`,"rtl"===s.G.document.dir?r.AH`.mdc-floating-label,.mdc-text-field--with-leading-icon,.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label,.mdc-text-field__icon--leading,.mdc-text-field__input[type=number]{direction:rtl;--direction:rtl}`:r.AH``]}]}}),d.J)},31265:(e,t,i)=>{i.d(t,{JW:()=>v,TC:()=>d,VN:()=>o,Vx:()=>r,XQ:()=>u,eM:()=>s,iH:()=>l,k3:()=>h,m4:()=>a,qf:()=>n,yv:()=>c});i(253),i(2075),i(94438);const a=33524==i.j?["migration_error","setup_error","setup_retry"]:null,n=33524==i.j?["not_loaded","loaded","setup_error","setup_retry"]:null,d=(e,t,i)=>{const a={type:"config_entries/subscribe"};return i&&i.type&&(a.type_filter=i.type),e.connection.subscribeMessage((e=>t(e)),a)},o=(e,t)=>{const i={};return t&&(t.type&&(i.type_filter=t.type),t.domain&&(i.domain=t.domain)),e.callWS({type:"config_entries/get",...i})},r=(e,t)=>e.callWS({type:"config_entries/get_single",entry_id:t}),l=(e,t,i)=>e.callWS({type:"config_entries/update",entry_id:t,...i}),s=(e,t)=>e.callApi("DELETE",`config/config_entries/entry/${t}`),c=(e,t)=>e.callApi("POST",`config/config_entries/entry/${t}/reload`),u=(e,t)=>e.callWS({type:"config_entries/disable",entry_id:t,disabled_by:"user"}),h=(e,t)=>e.callWS({type:"config_entries/disable",entry_id:t,disabled_by:null}),v=(e,t)=>{if(!t)return e;const i=e.find((e=>e.entry_id===t));if(!i)return e;return[i,...e.filter((e=>e.entry_id!==t))]}},74229:(e,t,i)=>{i.d(t,{c:()=>d});const a=async(e,t,i,n,d,...o)=>{const r=d,l=r[e],s=l=>n&&n(d,l.result)!==l.cacheKey?(r[e]=void 0,a(e,t,i,n,d,...o)):l.result;if(l)return l instanceof Promise?l.then(s):s(l);const c=i(d,...o);return r[e]=c,c.then((i=>{r[e]={result:i,cacheKey:n?.(d,i)},setTimeout((()=>{r[e]=void 0}),t)}),(()=>{r[e]=void 0})),c},n=e=>e.callWS({type:"entity/source"}),d=e=>a("_entitySources",3e4,n,(e=>Object.keys(e.states).length),e)},2586:(e,t,i)=>{var a=i(80674),n=i(82337),d=i(88138).f,o=a("unscopables"),r=Array.prototype;void 0===r[o]&&d(r,o,{configurable:!0,value:n(null)}),e.exports=function(e){r[o][e]=!0}},14767:(e,t,i)=>{var a=i(36565);e.exports=function(e,t,i){for(var n=0,d=arguments.length>2?i:a(t),o=new e(d);d>n;)o[n]=t[n++];return o}},88124:(e,t,i)=>{var a=i(66293),n=i(13113),d=i(88680),o=i(49940),r=i(80896),l=i(36565),s=i(82337),c=i(14767),u=Array,h=n([].push);e.exports=function(e,t,i,n){for(var v,p,f,m=o(e),y=d(m),k=a(t,i),g=s(null),b=l(y),_=0;b>_;_++)f=y[_],(p=r(k(f,_,m)))in g?h(g[p],f):g[p]=[f];if(n&&(v=n(m))!==u)for(p in g)g[p]=c(v,g[p]);return g}},12073:(e,t,i)=>{var a=i(41765),n=i(88124),d=i(2586);a({target:"Array",proto:!0},{group:function(e){return n(this,e,arguments.length>1?arguments[1]:void 0)}}),d("group")},32559:(e,t,i)=>{i.d(t,{Dx:()=>c,Jz:()=>m,KO:()=>f,Rt:()=>l,cN:()=>p,lx:()=>u,mY:()=>v,ps:()=>r,qb:()=>o,sO:()=>d});var a=i(2501);const{I:n}=a.ge,d=e=>null===e||"object"!=typeof e&&"function"!=typeof e,o=(e,t)=>void 0===t?void 0!==(null==e?void 0:e._$litType$):(null==e?void 0:e._$litType$)===t,r=e=>{var t;return null!=(null===(t=null==e?void 0:e._$litType$)||void 0===t?void 0:t.h)},l=e=>void 0===e.strings,s=()=>document.createComment(""),c=(e,t,i)=>{var a;const d=e._$AA.parentNode,o=void 0===t?e._$AB:t._$AA;if(void 0===i){const t=d.insertBefore(s(),o),a=d.insertBefore(s(),o);i=new n(t,a,e,e.options)}else{const t=i._$AB.nextSibling,n=i._$AM,r=n!==e;if(r){let t;null===(a=i._$AQ)||void 0===a||a.call(i,e),i._$AM=e,void 0!==i._$AP&&(t=e._$AU)!==n._$AU&&i._$AP(t)}if(t!==o||r){let e=i._$AA;for(;e!==t;){const t=e.nextSibling;d.insertBefore(e,o),e=t}}}return i},u=(e,t,i=e)=>(e._$AI(t,i),e),h={},v=(e,t=h)=>e._$AH=t,p=e=>e._$AH,f=e=>{var t;null===(t=e._$AP)||void 0===t||t.call(e,!1,!0);let i=e._$AA;const a=e._$AB.nextSibling;for(;i!==a;){const e=i.nextSibling;i.remove(),i=e}},m=e=>{e._$AR()}}};
//# sourceMappingURL=55386.YyQ_zW6O7cI.js.map