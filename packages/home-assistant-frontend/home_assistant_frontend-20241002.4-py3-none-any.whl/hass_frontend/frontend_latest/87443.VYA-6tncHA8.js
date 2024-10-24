export const id=87443;export const ids=[87443];export const modules={21863:(e,t,i)=>{function a(e){return void 0===e||Array.isArray(e)?e:[e]}i.d(t,{e:()=>a})},99890:(e,t,i)=>{i.d(t,{g:()=>a});const a=e=>(t,i)=>e.includes(t,i)},46875:(e,t,i)=>{i.d(t,{a:()=>n});var a=i(9883),o=i(213);function n(e,t){const i=(0,o.m)(e.entity_id),n=void 0!==t?t:e?.state;if(["button","event","input_button","scene"].includes(i))return n!==a.Hh;if((0,a.g0)(n))return!1;if(n===a.KF&&"alert"!==i)return!1;switch(i){case"alarm_control_panel":return"disarmed"!==n;case"alert":return"idle"!==n;case"cover":case"valve":return"closed"!==n;case"device_tracker":case"person":return"not_home"!==n;case"lawn_mower":return["mowing","error"].includes(n);case"lock":return"locked"!==n;case"media_player":return"standby"!==n;case"vacuum":return!["idle","docked","paused"].includes(n);case"plant":return"problem"===n;case"group":return["on","home","open","locked","problem"].includes(n);case"timer":return"active"===n;case"camera":return"streaming"===n}return!0}},5965:(e,t,i)=>{var a=i(36312),o=(i(89655),i(253),i(2075),i(54846),i(15112)),n=i(77706),s=i(94100),r=i(21863),d=i(34897),l=i(2682),c=i(4826),h=i(84976),u=(i(43536),i(88400),i(12675),i(55792));(0,a.A)([(0,n.EM)("ha-statistic-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"statistic-types"})],key:"statisticTypes",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"allow-custom-entity"})],key:"allowCustomEntity",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Array})],key:"statisticIds",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)({type:Array,attribute:"include-statistics-unit-of-measurement"})],key:"includeStatisticsUnitOfMeasurement",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"include-unit-class"})],key:"includeUnitClass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"include-device-class"})],key:"includeDeviceClass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"entities-only"})],key:"entitiesOnly",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)({type:Array,attribute:"exclude-statistics"})],key:"excludeStatistics",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helpMissingEntityUrl",value:()=>"/more-info/statistics/"},{kind:"field",decorators:[(0,n.wk)()],key:"_opened",value:void 0},{kind:"field",decorators:[(0,n.P)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"field",key:"_init",value:()=>!1},{kind:"field",key:"_statistics",value:()=>[]},{kind:"field",decorators:[(0,n.wk)()],key:"_filteredItems",value(){}},{kind:"field",key:"_rowRenderer",value(){return e=>o.qy`<mwc-list-item graphic="avatar" twoline> ${e.state?o.qy`<state-badge slot="graphic" .stateObj="${e.state}" .hass="${this.hass}"></state-badge>`:""} <span>${e.name}</span> <span slot="secondary">${""===e.id||"__missing"===e.id?o.qy`<a target="_blank" rel="noopener noreferrer" href="${(0,h.o)(this.hass,this.helpMissingEntityUrl)}">${this.hass.localize("ui.components.statistic-picker.learn_more")}</a>`:e.id}</span> </mwc-list-item>`}},{kind:"field",key:"_getStatistics",value(){return(0,s.A)(((e,t,i,a,o,n,s)=>{if(!e.length)return[{id:"",name:this.hass.localize("ui.components.statistic-picker.no_statistics"),strings:[]}];if(t){const i=(0,r.e)(t);e=e.filter((e=>i.includes(e.statistics_unit_of_measurement)))}if(i){const t=(0,r.e)(i);e=e.filter((e=>t.includes(e.unit_class)))}if(a){const t=(0,r.e)(a);e=e.filter((e=>{const i=this.hass.states[e.statistic_id];return!i||t.includes(i.attributes.device_class||"")}))}const d=[];return e.forEach((e=>{if(n&&e.statistic_id!==s&&n.includes(e.statistic_id))return;const t=this.hass.states[e.statistic_id];if(!t){if(!o){const t=e.statistic_id,i=(0,c.$O)(this.hass,e.statistic_id,e);d.push({id:t,name:i,strings:[t,i]})}return}const i=e.statistic_id,a=(0,c.$O)(this.hass,e.statistic_id,e);d.push({id:i,name:a,state:t,strings:[i,a]})})),d.length?(d.length>1&&d.sort(((e,t)=>(0,l.x)(e.name||"",t.name||"",this.hass.locale.language))),d.push({id:"__missing",name:this.hass.localize("ui.components.statistic-picker.missing_entity"),strings:[]}),d):[{id:"",name:this.hass.localize("ui.components.statistic-picker.no_match"),strings:[]}]}))}},{kind:"method",key:"open",value:function(){this.comboBox?.open()}},{kind:"method",key:"focus",value:function(){this.comboBox?.focus()}},{kind:"method",key:"willUpdate",value:function(e){(!this.hasUpdated&&!this.statisticIds||e.has("statisticTypes"))&&this._getStatisticIds(),(!this._init&&this.statisticIds||e.has("_opened")&&this._opened)&&(this._init=!0,this.hasUpdated?this._statistics=this._getStatistics(this.statisticIds,this.includeStatisticsUnitOfMeasurement,this.includeUnitClass,this.includeDeviceClass,this.entitiesOnly,this.excludeStatistics,this.value):this.updateComplete.then((()=>{this._statistics=this._getStatistics(this.statisticIds,this.includeStatisticsUnitOfMeasurement,this.includeUnitClass,this.includeDeviceClass,this.entitiesOnly,this.excludeStatistics,this.value)})))}},{kind:"method",key:"render",value:function(){return 0===this._statistics.length?o.s6:o.qy` <ha-combo-box .hass="${this.hass}" .label="${void 0===this.label&&this.hass?this.hass.localize("ui.components.statistic-picker.statistic"):this.label}" .value="${this._value}" .renderer="${this._rowRenderer}" .disabled="${this.disabled}" .allowCustomValue="${this.allowCustomEntity}" .items="${this._statistics}" .filteredItems="${this._filteredItems??this._statistics}" item-value-path="id" item-id-path="id" item-label-path="name" @opened-changed="${this._openedChanged}" @value-changed="${this._statisticChanged}" @filter-changed="${this._filterChanged}"></ha-combo-box> `}},{kind:"method",key:"_getStatisticIds",value:async function(){this.statisticIds=await(0,c.p3)(this.hass,this.statisticTypes)}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_statisticChanged",value:function(e){e.stopPropagation();let t=e.detail.value;"__missing"===t&&(t=""),t!==this._value&&this._setValue(t)}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_filterChanged",value:function(e){const t=e.detail.value.toLowerCase();this._filteredItems=t.length?(0,u.H)(t,this._statistics):void 0}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,d.r)(this,"value-changed",{value:e}),(0,d.r)(this,"change")}),0)}}]}}),o.WF)},88725:(e,t,i)=>{var a=i(36312),o=i(41204),n=i(15565),s=i(15112),r=i(77706);(0,a.A)([(0,r.EM)("ha-checkbox")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",static:!0,key:"styles",value:()=>[n.R,s.AH`:host{--mdc-theme-secondary:var(--primary-color)}`]}]}}),o.L)},43536:(e,t,i)=>{var a=i(36312),o=i(68689),n=(i(253),i(54846),i(64077)),s=(i(57597),i(68711)),r=i(15112),d=i(77706),l=i(10977),c=i(34897);i(28066),i(13830),i(90431);(0,s.SF)("vaadin-combo-box-item",r.AH`:host{padding:0!important}:host([focused]:not([disabled])){background-color:rgba(var(--rgb-primary-text-color,0,0,0),.12)}:host([selected]:not([disabled])){background-color:transparent;color:var(--mdc-theme-primary);--mdc-ripple-color:var(--mdc-theme-primary);--mdc-theme-text-primary-on-background:var(--mdc-theme-primary)}:host([selected]:not([disabled])):before{background-color:var(--mdc-theme-primary);opacity:.12;content:"";position:absolute;top:0;left:0;width:100%;height:100%}:host([selected][focused]:not([disabled])):before{opacity:.24}:host(:hover:not([disabled])){background-color:transparent}[part=content]{width:100%}[part=checkmark]{display:none}`);(0,a.A)([(0,d.EM)("ha-combo-box")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"validationMessage",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:"error-message"})],key:"errorMessage",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"invalid",value:()=>!1},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"icon",value:()=>!1},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"items",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"filteredItems",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"dataProvider",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:"allow-custom-value",type:Boolean})],key:"allowCustomValue",value:()=>!1},{kind:"field",decorators:[(0,d.MZ)({attribute:"item-value-path"})],key:"itemValuePath",value:()=>"value"},{kind:"field",decorators:[(0,d.MZ)({attribute:"item-label-path"})],key:"itemLabelPath",value:()=>"label"},{kind:"field",decorators:[(0,d.MZ)({attribute:"item-id-path"})],key:"itemIdPath",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"renderer",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"required",value:()=>!1},{kind:"field",decorators:[(0,d.MZ)({type:Boolean,reflect:!0})],key:"opened",value:()=>!1},{kind:"field",decorators:[(0,d.P)("vaadin-combo-box-light",!0)],key:"_comboBox",value:void 0},{kind:"field",decorators:[(0,d.P)("ha-textfield",!0)],key:"_inputElement",value:void 0},{kind:"field",key:"_overlayMutationObserver",value:void 0},{kind:"field",key:"_bodyMutationObserver",value:void 0},{kind:"method",key:"open",value:async function(){await this.updateComplete,this._comboBox?.open()}},{kind:"method",key:"focus",value:async function(){await this.updateComplete,await(this._inputElement?.updateComplete),this._inputElement?.focus()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.A)(i,"disconnectedCallback",this,3)([]),this._overlayMutationObserver&&(this._overlayMutationObserver.disconnect(),this._overlayMutationObserver=void 0),this._bodyMutationObserver&&(this._bodyMutationObserver.disconnect(),this._bodyMutationObserver=void 0)}},{kind:"get",key:"selectedItem",value:function(){return this._comboBox.selectedItem}},{kind:"method",key:"setInputValue",value:function(e){this._comboBox.value=e}},{kind:"method",key:"render",value:function(){return r.qy` <vaadin-combo-box-light .itemValuePath="${this.itemValuePath}" .itemIdPath="${this.itemIdPath}" .itemLabelPath="${this.itemLabelPath}" .items="${this.items}" .value="${this.value||""}" .filteredItems="${this.filteredItems}" .dataProvider="${this.dataProvider}" .allowCustomValue="${this.allowCustomValue}" .disabled="${this.disabled}" .required="${this.required}" ${(0,n.d)(this.renderer||this._defaultRowRenderer)} @opened-changed="${this._openedChanged}" @filter-changed="${this._filterChanged}" @value-changed="${this._valueChanged}" attr-for-value="value"> <ha-textfield label="${(0,l.J)(this.label)}" placeholder="${(0,l.J)(this.placeholder)}" ?disabled="${this.disabled}" ?required="${this.required}" validationMessage="${(0,l.J)(this.validationMessage)}" .errorMessage="${this.errorMessage}" class="input" autocapitalize="none" autocomplete="off" autocorrect="off" input-spellcheck="false" .suffix="${r.qy`<div style="width:28px" role="none presentation"></div>`}" .icon="${this.icon}" .invalid="${this.invalid}" .helper="${this.helper}" helperPersistent> <slot name="icon" slot="leadingIcon"></slot> </ha-textfield> ${this.value?r.qy`<ha-svg-icon role="button" tabindex="-1" aria-label="${(0,l.J)(this.hass?.localize("ui.common.clear"))}" class="clear-button" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}" @click="${this._clearValue}"></ha-svg-icon>`:""} <ha-svg-icon role="button" tabindex="-1" aria-label="${(0,l.J)(this.label)}" aria-expanded="${this.opened?"true":"false"}" class="toggle-button" .path="${this.opened?"M7,15L12,10L17,15H7Z":"M7,10L12,15L17,10H7Z"}" @click="${this._toggleOpen}"></ha-svg-icon> </vaadin-combo-box-light> `}},{kind:"field",key:"_defaultRowRenderer",value(){return e=>r.qy`<ha-list-item> ${this.itemLabelPath?e[this.itemLabelPath]:e} </ha-list-item>`}},{kind:"method",key:"_clearValue",value:function(e){e.stopPropagation(),(0,c.r)(this,"value-changed",{value:void 0})}},{kind:"method",key:"_toggleOpen",value:function(e){this.opened?(this._comboBox?.close(),e.stopPropagation()):this._comboBox?.inputElement.focus()}},{kind:"method",key:"_openedChanged",value:function(e){e.stopPropagation();const t=e.detail.value;if(setTimeout((()=>{this.opened=t}),0),(0,c.r)(this,"opened-changed",{value:e.detail.value}),t){const e=document.querySelector("vaadin-combo-box-overlay");e&&this._removeInert(e),this._observeBody()}else this._bodyMutationObserver?.disconnect(),this._bodyMutationObserver=void 0}},{kind:"method",key:"_observeBody",value:function(){"MutationObserver"in window&&!this._bodyMutationObserver&&(this._bodyMutationObserver=new MutationObserver((e=>{e.forEach((e=>{e.addedNodes.forEach((e=>{"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&this._removeInert(e)})),e.removedNodes.forEach((e=>{"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&(this._overlayMutationObserver?.disconnect(),this._overlayMutationObserver=void 0)}))}))})),this._bodyMutationObserver.observe(document.body,{childList:!0}))}},{kind:"method",key:"_removeInert",value:function(e){if(e.inert)return e.inert=!1,this._overlayMutationObserver?.disconnect(),void(this._overlayMutationObserver=void 0);"MutationObserver"in window&&!this._overlayMutationObserver&&(this._overlayMutationObserver=new MutationObserver((e=>{e.forEach((e=>{if("inert"===e.attributeName){const t=e.target;t.inert&&(this._overlayMutationObserver?.disconnect(),this._overlayMutationObserver=void 0,t.inert=!1)}}))})),this._overlayMutationObserver.observe(e,{attributes:!0}))}},{kind:"method",key:"_filterChanged",value:function(e){e.stopPropagation(),(0,c.r)(this,"filter-changed",{value:e.detail.value})}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation(),this.allowCustomValue||(this._comboBox._closeOnBlurIsPrevented=!0);const t=e.detail.value;t!==this.value&&(0,c.r)(this,"value-changed",{value:t||void 0})}},{kind:"get",static:!0,key:"styles",value:function(){return r.AH`:host{display:block;width:100%}vaadin-combo-box-light{position:relative;--vaadin-combo-box-overlay-max-height:calc(45vh - 56px)}ha-textfield{width:100%}ha-textfield>ha-icon-button{--mdc-icon-button-size:24px;padding:2px;color:var(--secondary-text-color)}ha-svg-icon{color:var(--input-dropdown-icon-color);position:absolute;cursor:pointer}.toggle-button{right:12px;top:-10px;inset-inline-start:initial;inset-inline-end:12px;direction:var(--direction)}:host([opened]) .toggle-button{color:var(--primary-color)}.clear-button{--mdc-icon-size:20px;top:-7px;right:36px;inset-inline-start:initial;inset-inline-end:36px;direction:var(--direction)}`}}]}}),r.WF)},3276:(e,t,i)=>{i.d(t,{l:()=>h});var a=i(36312),o=i(68689),n=i(54653),s=i(34599),r=i(15112),d=i(77706),l=i(90952);i(28066);const c=["button","ha-list-item"],h=(e,t)=>r.qy` <div class="header_title"> <span>${t}</span> <ha-icon-button .label="${e?.localize("ui.dialogs.generic.close")??"Close"}" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}" dialogAction="close" class="header_button"></ha-icon-button> </div> `;(0,a.A)([(0,d.EM)("ha-dialog")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:l.Xr,value:void 0},{kind:"method",key:"scrollToPos",value:function(e,t){this.contentElement?.scrollTo(e,t)}},{kind:"method",key:"renderHeading",value:function(){return r.qy`<slot name="heading"> ${(0,o.A)(i,"renderHeading",this,3)([])} </slot>`}},{kind:"method",key:"firstUpdated",value:function(){(0,o.A)(i,"firstUpdated",this,3)([]),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,c].join(", "),this._updateScrolledAttribute(),this.contentElement?.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.A)(i,"disconnectedCallback",this,3)([]),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value(){return()=>{this._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value:()=>[s.R,r.AH`:host([scrolled]) ::slotted(ha-dialog-header){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.mdc-dialog{--mdc-dialog-scroll-divider-color:var(
          --dialog-scroll-divider-color,
          var(--divider-color)
        );z-index:var(--dialog-z-index,8);-webkit-backdrop-filter:var(--ha-dialog-scrim-backdrop-filter,var(--dialog-backdrop-filter,none));backdrop-filter:var(--ha-dialog-scrim-backdrop-filter,var(--dialog-backdrop-filter,none));--mdc-dialog-box-shadow:var(--dialog-box-shadow, none);--mdc-typography-headline6-font-weight:400;--mdc-typography-headline6-font-size:1.574rem}.mdc-dialog__actions{justify-content:var(--justify-action-buttons,flex-end);padding-bottom:max(env(safe-area-inset-bottom),24px)}.mdc-dialog__actions span:first-child{flex:var(--secondary-action-button-flex,unset)}.mdc-dialog__actions span:nth-child(2){flex:var(--primary-action-button-flex,unset)}.mdc-dialog__container{align-items:var(--vertical-align-dialog,center)}.mdc-dialog__title{padding:24px 24px 0 24px}.mdc-dialog__actions{padding:12px 24px 12px 24px}.mdc-dialog__title::before{content:unset}.mdc-dialog .mdc-dialog__content{position:var(--dialog-content-position,relative);padding:var(--dialog-content-padding,24px)}:host([hideactions]) .mdc-dialog .mdc-dialog__content{padding-bottom:max(var(--dialog-content-padding,24px),env(safe-area-inset-bottom))}.mdc-dialog .mdc-dialog__surface{position:var(--dialog-surface-position,relative);top:var(--dialog-surface-top);margin-top:var(--dialog-surface-margin-top);min-height:var(--mdc-dialog-min-height,auto);border-radius:var(--ha-dialog-border-radius,28px);-webkit-backdrop-filter:var(--ha-dialog-surface-backdrop-filter,none);backdrop-filter:var(--ha-dialog-surface-backdrop-filter,none);background:var(--ha-dialog-surface-background,var(--mdc-theme-surface,#fff))}:host([flexContent]) .mdc-dialog .mdc-dialog__content{display:flex;flex-direction:column}.header_title{position:relative;padding-right:40px;padding-inline-end:40px;padding-inline-start:initial;direction:var(--direction)}.header_title span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:block}.header_button{position:absolute;right:-12px;top:-12px;text-decoration:none;color:inherit;inset-inline-start:initial;inset-inline-end:-12px;direction:var(--direction)}.dialog-actions{inset-inline-start:initial!important;inset-inline-end:0px!important;direction:var(--direction)}`]}]}}),n.u)},24284:(e,t,i)=>{var a=i(36312),o=i(37136),n=i(18881),s=i(15112),r=i(77706),d=i(85323),l=i(34897);(0,a.A)([(0,r.EM)("ha-formfield")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"method",key:"render",value:function(){const e={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return s.qy` <div class="mdc-form-field ${(0,d.H)(e)}"> <slot></slot> <label class="mdc-label" @click="${this._labelClick}"> <slot name="label">${this.label}</slot> </label> </div>`}},{kind:"method",key:"_labelClick",value:function(){const e=this.input;if(e&&(e.focus(),!e.disabled))switch(e.tagName){case"HA-CHECKBOX":e.checked=!e.checked,(0,l.r)(e,"change");break;case"HA-RADIO":e.checked=!0,(0,l.r)(e,"change");break;default:e.click()}}},{kind:"field",static:!0,key:"styles",value:()=>[n.R,s.AH`:host(:not([alignEnd])) ::slotted(ha-switch){margin-right:10px;margin-inline-end:10px;margin-inline-start:inline}.mdc-form-field{align-items:var(--ha-formfield-align-items,center);gap:4px}.mdc-form-field>label{direction:var(--direction);margin-inline-start:0;margin-inline-end:auto;padding:0}:host([disabled]) label{color:var(--disabled-text-color)}`]}]}}),o.M)},13830:(e,t,i)=>{i.d(t,{$:()=>l});var a=i(36312),o=i(68689),n=i(30116),s=i(43389),r=i(15112),d=i(77706);let l=(0,a.A)([(0,d.EM)("ha-list-item")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"renderRipple",value:function(){return this.noninteractive?"":(0,o.A)(i,"renderRipple",this,3)([])}},{kind:"get",static:!0,key:"styles",value:function(){return[s.R,r.AH`:host{padding-left:var(--mdc-list-side-padding-left,var(--mdc-list-side-padding,20px));padding-inline-start:var(--mdc-list-side-padding-left,var(--mdc-list-side-padding,20px));padding-right:var(--mdc-list-side-padding-right,var(--mdc-list-side-padding,20px));padding-inline-end:var(--mdc-list-side-padding-right,var(--mdc-list-side-padding,20px))}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:48px}span.material-icons:first-of-type{margin-inline-start:0px!important;margin-inline-end:var(--mdc-list-item-graphic-margin,16px)!important;direction:var(--direction)!important}span.material-icons:last-of-type{margin-inline-start:auto!important;margin-inline-end:0px!important;direction:var(--direction)!important}.mdc-deprecated-list-item__meta{display:var(--mdc-list-item-meta-display);align-items:center;flex-shrink:0}:host([graphic=icon]:not([twoline])) .mdc-deprecated-list-item__graphic{margin-inline-end:var(--mdc-list-item-graphic-margin,20px)!important}:host([multiline-secondary]){height:auto}:host([multiline-secondary]) .mdc-deprecated-list-item__text{padding:8px 0}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text{text-overflow:initial;white-space:normal;overflow:auto;display:inline-block;margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text{margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text::before{display:none}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text::before{display:none}:host([disabled]){color:var(--disabled-text-color)}:host([noninteractive]){pointer-events:unset}`,"rtl"===document.dir?r.AH`span.material-icons:first-of-type,span.material-icons:last-of-type{direction:rtl!important;--direction:rtl}`:r.AH``]}}]}}),n.J)},51513:(e,t,i)=>{var a=i(36312),o=i(35351),n=i(37749),s=i(15112),r=i(77706);(0,a.A)([(0,r.EM)("ha-radio")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",static:!0,key:"styles",value:()=>[n.R,s.AH`:host{--mdc-theme-secondary:var(--primary-color)}`]}]}}),o.F)},90431:(e,t,i)=>{var a=i(36312),o=i(68689),n=i(44331),s=i(67449),r=i(15112),d=i(77706),l=i(74005);(0,a.A)([(0,d.EM)("ha-textfield")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"invalid",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:"error-message"})],key:"errorMessage",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"icon",value:()=>!1},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"iconTrailing",value:()=>!1},{kind:"field",decorators:[(0,d.MZ)()],key:"autocomplete",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"autocorrect",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:"input-spellcheck"})],key:"inputSpellcheck",value:void 0},{kind:"field",decorators:[(0,d.P)("input")],key:"formElement",value:void 0},{kind:"method",key:"updated",value:function(e){(0,o.A)(i,"updated",this,3)([e]),(e.has("invalid")||e.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||this.validationMessage||"Invalid":""),(this.invalid||this.validateOnInitialRender||e.has("invalid")&&void 0!==e.get("invalid"))&&this.reportValidity()),e.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),e.has("autocorrect")&&(this.autocorrect?this.formElement.setAttribute("autocorrect",this.autocorrect):this.formElement.removeAttribute("autocorrect")),e.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}},{kind:"method",key:"renderIcon",value:function(e,t=!1){const i=t?"trailing":"leading";return r.qy` <span class="mdc-text-field__icon mdc-text-field__icon--${i}" tabindex="${t?1:-1}"> <slot name="${i}Icon"></slot> </span> `}},{kind:"field",static:!0,key:"styles",value:()=>[s.R,r.AH`.mdc-text-field__input{width:var(--ha-textfield-input-width,100%)}.mdc-text-field:not(.mdc-text-field--with-leading-icon){padding:var(--text-field-padding,0px 16px)}.mdc-text-field__affix--suffix{padding-left:var(--text-field-suffix-padding-left,12px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,12px);padding-inline-end:var(--text-field-suffix-padding-right,0px);direction:ltr}.mdc-text-field--with-leading-icon{padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,16px);direction:var(--direction)}.mdc-text-field--with-leading-icon.mdc-text-field--with-trailing-icon{padding-left:var(--text-field-suffix-padding-left,0px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,0px)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--suffix{color:var(--secondary-text-color)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__icon{color:var(--secondary-text-color)}.mdc-text-field__icon--leading{margin-inline-start:16px;margin-inline-end:8px;direction:var(--direction)}.mdc-text-field__icon--trailing{padding:var(--textfield-icon-trailing-padding,12px)}.mdc-floating-label:not(.mdc-floating-label--float-above){text-overflow:ellipsis;width:inherit;padding-right:30px;padding-inline-end:30px;padding-inline-start:initial;box-sizing:border-box;direction:var(--direction)}input{text-align:var(--text-field-text-align,start)}::-ms-reveal{display:none}:host([no-spinner]) input::-webkit-inner-spin-button,:host([no-spinner]) input::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}:host([no-spinner]) input[type=number]{-moz-appearance:textfield}.mdc-text-field__ripple{overflow:hidden}.mdc-text-field{overflow:var(--text-field-overflow)}.mdc-floating-label{inset-inline-start:16px!important;inset-inline-end:initial!important;transform-origin:var(--float-start);direction:var(--direction);text-align:var(--float-start)}.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label{max-width:calc(100% - 48px - var(--text-field-suffix-padding-left,0px));inset-inline-start:calc(48px + var(--text-field-suffix-padding-left,0px))!important;inset-inline-end:initial!important;direction:var(--direction)}.mdc-text-field__input[type=number]{direction:var(--direction)}.mdc-text-field__affix--prefix{padding-right:var(--text-field-prefix-padding-right,2px);padding-inline-end:var(--text-field-prefix-padding-right,2px);padding-inline-start:initial}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--prefix{color:var(--mdc-text-field-label-ink-color)}`,"rtl"===l.G.document.dir?r.AH`.mdc-floating-label,.mdc-text-field--with-leading-icon,.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label,.mdc-text-field__icon--leading,.mdc-text-field__input[type=number]{direction:rtl;--direction:rtl}`:r.AH``]}]}}),n.J)},94526:(e,t,i)=>{i.d(t,{Fy:()=>n,Gk:()=>d,Hg:()=>a,Y_:()=>l,ds:()=>r,e0:()=>o,ec:()=>s});i(16891);const a=e=>e.map((e=>{if("string"!==e.type)return e;switch(e.name){case"username":return{...e,autocomplete:"username"};case"password":return{...e,autocomplete:"current-password"};case"code":return{...e,autocomplete:"one-time-code"};default:return e}})),o=(e,t)=>e.callWS({type:"auth/sign_path",path:t}),n=async(e,t,i,a)=>e.callWS({type:"config/auth_provider/homeassistant/create",user_id:t,username:i,password:a}),s=(e,t,i)=>e.callWS({type:"config/auth_provider/homeassistant/change_password",current_password:t,new_password:i}),r=(e,t,i)=>e.callWS({type:"config/auth_provider/homeassistant/admin_change_password",user_id:t,password:i}),d=(e,t,i)=>e.callWS({type:"config/auth_provider/homeassistant/admin_change_username",user_id:t,username:i}),l=(e,t,i)=>e.callWS({type:"auth/delete_all_refresh_tokens",token_type:t,delete_current_token:i})},9883:(e,t,i)=>{i.d(t,{HV:()=>n,Hh:()=>o,KF:()=>r,ON:()=>s,g0:()=>c,s7:()=>d});var a=i(99890);const o="unavailable",n="unknown",s="on",r="off",d=[o,n],l=[o,n,r],c=(0,a.g)(d);(0,a.g)(l)},65960:(e,t,i)=>{i.a(e,(async(e,a)=>{try{i.r(t),i.d(t,{DialogEnergySolarSettings:()=>g});var o=i(36312),n=(i(89655),i(253),i(2075),i(16891),i(72606),i(15112)),s=i(77706),r=i(34897),d=(i(5965),i(88725),i(3276),i(24284),i(51513),i(31265)),l=i(47076),c=i(96778),h=i(30581),u=i(55321),p=i(51842),f=e([l]);l=(f.then?(await f)():f)[0];const m="M11.45,2V5.55L15,3.77L11.45,2M10.45,8L8,10.46L11.75,11.71L10.45,8M2,11.45L3.77,15L5.55,11.45H2M10,2H2V10C2.57,10.17 3.17,10.25 3.77,10.25C7.35,10.26 10.26,7.35 10.27,3.75C10.26,3.16 10.17,2.57 10,2M17,22V16H14L19,7V13H22L17,22Z",v=["energy"];let g=(0,o.A)([(0,s.EM)("dialog-energy-solar-settings")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_source",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_configEntries",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_forecast",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_energy_units",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_error",value:void 0},{kind:"field",key:"_excludeList",value:void 0},{kind:"method",key:"showDialog",value:async function(e){this._params=e,this._fetchSolarForecastConfigEntries(),this._source=e.source?{...e.source}:(0,l.Q4)(),this._forecast=null!==this._source.config_entry_solar_forecast,this._energy_units=(await(0,c.j4)(this.hass,"energy")).units,this._excludeList=this._params.solar_sources.map((e=>e.stat_energy_from)).filter((e=>e!==this._source?.stat_energy_from))}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this._source=void 0,this._error=void 0,this._excludeList=void 0,(0,r.r)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){if(!this._params||!this._source)return n.s6;const e=this._energy_units?.join(", ")||"";return n.qy` <ha-dialog open .heading="${n.qy`<ha-svg-icon .path="${m}" style="--mdc-icon-size:32px"></ha-svg-icon> ${this.hass.localize("ui.panel.config.energy.solar.dialog.header")}`}" @closed="${this.closeDialog}"> ${this._error?n.qy`<p class="error">${this._error}</p>`:""} <div> ${this.hass.localize("ui.panel.config.energy.solar.dialog.entity_para",{unit:e})} </div> <ha-statistic-picker .hass="${this.hass}" .helpMissingEntityUrl="${l.X4}" .includeUnitClass="${v}" .value="${this._source.stat_energy_from}" .label="${this.hass.localize("ui.panel.config.energy.solar.dialog.solar_production_energy")}" .excludeStatistics="${this._excludeList}" @value-changed="${this._statisticChanged}" dialogInitialFocus></ha-statistic-picker> <h3> ${this.hass.localize("ui.panel.config.energy.solar.dialog.solar_production_forecast")} </h3> <p> ${this.hass.localize("ui.panel.config.energy.solar.dialog.solar_production_forecast_description")} </p> <ha-formfield label="${this.hass.localize("ui.panel.config.energy.solar.dialog.dont_forecast_production")}"> <ha-radio value="false" name="forecast" .checked="${!this._forecast}" @change="${this._handleForecastChanged}"></ha-radio> </ha-formfield> <ha-formfield label="${this.hass.localize("ui.panel.config.energy.solar.dialog.forecast_production")}"> <ha-radio value="true" name="forecast" .checked="${this._forecast}" @change="${this._handleForecastChanged}"></ha-radio> </ha-formfield> ${this._forecast?n.qy`<div class="forecast-options"> ${this._configEntries?.map((e=>n.qy`<ha-formfield .label="${n.qy`<div style="display:flex;align-items:center"> <img alt="" crossorigin="anonymous" referrerpolicy="no-referrer" style="height:24px;margin-right:16px;margin-inline-end:16px;margin-inline-start:initial" src="${(0,p.MR)({domain:e.domain,type:"icon",darkOptimized:this.hass.themes?.darkMode})}">${e.title} </div>`}"> <ha-checkbox .entry="${e}" @change="${this._forecastCheckChanged}" .checked="${this._source?.config_entry_solar_forecast?.includes(e.entry_id)}"> </ha-checkbox> </ha-formfield>`))} <mwc-button @click="${this._addForecast}"> ${this.hass.localize("ui.panel.config.energy.solar.dialog.add_forecast")} </mwc-button> </div>`:""} <mwc-button @click="${this.closeDialog}" slot="secondaryAction"> ${this.hass.localize("ui.common.cancel")} </mwc-button> <mwc-button @click="${this._save}" .disabled="${!this._source.stat_energy_from}" slot="primaryAction"> ${this.hass.localize("ui.common.save")} </mwc-button> </ha-dialog> `}},{kind:"method",key:"_fetchSolarForecastConfigEntries",value:async function(){const e=this._params.info.solar_forecast_domains;this._configEntries=0===e.length?[]:1===e.length?await(0,d.VN)(this.hass,{type:["service"],domain:e[0]}):(await(0,d.VN)(this.hass,{type:["service"]})).filter((t=>e.includes(t.domain)))}},{kind:"method",key:"_handleForecastChanged",value:function(e){const t=e.currentTarget;this._forecast="true"===t.value}},{kind:"method",key:"_forecastCheckChanged",value:function(e){const t=e.currentTarget,i=t.entry;t.checked?(null===this._source.config_entry_solar_forecast&&(this._source.config_entry_solar_forecast=[]),this._source.config_entry_solar_forecast.push(i.entry_id)):this._source.config_entry_solar_forecast.splice(this._source.config_entry_solar_forecast.indexOf(i.entry_id),1)}},{kind:"method",key:"_addForecast",value:function(){(0,h.W)(this,{startFlowHandler:"forecast_solar",dialogClosedCallback:e=>{e.entryId&&(null===this._source.config_entry_solar_forecast&&(this._source.config_entry_solar_forecast=[]),this._source.config_entry_solar_forecast.push(e.entryId),this._fetchSolarForecastConfigEntries())}})}},{kind:"method",key:"_statisticChanged",value:function(e){this._source={...this._source,stat_energy_from:e.detail.value}}},{kind:"method",key:"_save",value:async function(){try{this._forecast||(this._source.config_entry_solar_forecast=null),await this._params.saveCallback(this._source),this.closeDialog()}catch(e){this._error=e.message}}},{kind:"get",static:!0,key:"styles",value:function(){return[u.RF,u.nA,n.AH`ha-dialog{--mdc-dialog-max-width:430px}img{height:24px;margin-right:16px;margin-inline-end:16px;margin-inline-start:initial}ha-formfield{display:block}ha-statistic-picker{width:100%}.forecast-options{padding-left:32px;padding-inline-start:32px;padding-inline-end:initial}.forecast-options mwc-button{padding-left:8px;padding-inline-start:8px;padding-inline-end:initial}`]}}]}}),n.WF);a()}catch(e){a(e)}}))}};
//# sourceMappingURL=87443.VYA-6tncHA8.js.map