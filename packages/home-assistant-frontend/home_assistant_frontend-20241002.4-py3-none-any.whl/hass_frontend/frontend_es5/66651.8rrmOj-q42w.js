"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[66651],{3276:function(e,i,t){t.d(i,{l:function(){return k}});var n,o,a,r=t(35806),s=t(71008),l=t(62193),d=t(2816),c=t(27927),h=t(35890),u=t(64599),g=(t(71522),t(81027),t(79243),t(54653)),m=t(34599),f=t(15112),p=t(29818),v=t(90952),_=(t(28066),["button","ha-list-item"]),k=function(e,i){var t;return(0,f.qy)(n||(n=(0,u.A)([' <div class="header_title"> <span>','</span> <ha-icon-button .label="','" .path="','" dialogAction="close" class="header_button"></ha-icon-button> </div> '])),i,null!==(t=null==e?void 0:e.localize("ui.dialogs.generic.close"))&&void 0!==t?t:"Close","M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z")};(0,c.A)([(0,p.EM)("ha-dialog")],(function(e,i){var t=function(i){function t(){var i;(0,s.A)(this,t);for(var n=arguments.length,o=new Array(n),a=0;a<n;a++)o[a]=arguments[a];return i=(0,l.A)(this,t,[].concat(o)),e(i),i}return(0,d.A)(t,i),(0,r.A)(t)}(i);return{F:t,d:[{kind:"field",key:v.Xr,value:void 0},{kind:"method",key:"scrollToPos",value:function(e,i){var t;null===(t=this.contentElement)||void 0===t||t.scrollTo(e,i)}},{kind:"method",key:"renderHeading",value:function(){return(0,f.qy)(o||(o=(0,u.A)(['<slot name="heading"> '," </slot>"])),(0,h.A)(t,"renderHeading",this,3)([]))}},{kind:"method",key:"firstUpdated",value:function(){var e;(0,h.A)(t,"firstUpdated",this,3)([]),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,_].join(", "),this._updateScrolledAttribute(),null===(e=this.contentElement)||void 0===e||e.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,h.A)(t,"disconnectedCallback",this,3)([]),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value:function(){var e=this;return function(){e._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value:function(){return[m.R,(0,f.AH)(a||(a=(0,u.A)([":host([scrolled]) ::slotted(ha-dialog-header){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.mdc-dialog{--mdc-dialog-scroll-divider-color:var(\n          --dialog-scroll-divider-color,\n          var(--divider-color)\n        );z-index:var(--dialog-z-index,8);-webkit-backdrop-filter:var(--ha-dialog-scrim-backdrop-filter,var(--dialog-backdrop-filter,none));backdrop-filter:var(--ha-dialog-scrim-backdrop-filter,var(--dialog-backdrop-filter,none));--mdc-dialog-box-shadow:var(--dialog-box-shadow, none);--mdc-typography-headline6-font-weight:400;--mdc-typography-headline6-font-size:1.574rem}.mdc-dialog__actions{justify-content:var(--justify-action-buttons,flex-end);padding-bottom:max(env(safe-area-inset-bottom),24px)}.mdc-dialog__actions span:first-child{flex:var(--secondary-action-button-flex,unset)}.mdc-dialog__actions span:nth-child(2){flex:var(--primary-action-button-flex,unset)}.mdc-dialog__container{align-items:var(--vertical-align-dialog,center)}.mdc-dialog__title{padding:24px 24px 0 24px}.mdc-dialog__actions{padding:12px 24px 12px 24px}.mdc-dialog__title::before{content:unset}.mdc-dialog .mdc-dialog__content{position:var(--dialog-content-position,relative);padding:var(--dialog-content-padding,24px)}:host([hideactions]) .mdc-dialog .mdc-dialog__content{padding-bottom:max(var(--dialog-content-padding,24px),env(safe-area-inset-bottom))}.mdc-dialog .mdc-dialog__surface{position:var(--dialog-surface-position,relative);top:var(--dialog-surface-top);margin-top:var(--dialog-surface-margin-top);min-height:var(--mdc-dialog-min-height,auto);border-radius:var(--ha-dialog-border-radius,28px);-webkit-backdrop-filter:var(--ha-dialog-surface-backdrop-filter,none);backdrop-filter:var(--ha-dialog-surface-backdrop-filter,none);background:var(--ha-dialog-surface-background,var(--mdc-theme-surface,#fff))}:host([flexContent]) .mdc-dialog .mdc-dialog__content{display:flex;flex-direction:column}.header_title{position:relative;padding-right:40px;padding-inline-end:40px;padding-inline-start:initial;direction:var(--direction)}.header_title span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:block}.header_button{position:absolute;right:-12px;top:-12px;text-decoration:none;color:inherit;inset-inline-start:initial;inset-inline-end:-12px;direction:var(--direction)}.dialog-actions{inset-inline-start:initial!important;inset-inline-end:0px!important;direction:var(--direction)}"])))]}}]}}),g.u)},24284:function(e,i,t){var n,o,a=t(64599),r=t(35806),s=t(71008),l=t(62193),d=t(2816),c=t(27927),h=(t(81027),t(37136)),u=t(18881),g=t(15112),m=t(29818),f=t(85323),p=t(34897);(0,c.A)([(0,m.EM)("ha-formfield")],(function(e,i){var t=function(i){function t(){var i;(0,s.A)(this,t);for(var n=arguments.length,o=new Array(n),a=0;a<n;a++)o[a]=arguments[a];return i=(0,l.A)(this,t,[].concat(o)),e(i),i}return(0,d.A)(t,i),(0,r.A)(t)}(i);return{F:t,d:[{kind:"field",decorators:[(0,m.MZ)({type:Boolean,reflect:!0})],key:"disabled",value:function(){return!1}},{kind:"method",key:"render",value:function(){var e={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return(0,g.qy)(n||(n=(0,a.A)([' <div class="mdc-form-field ','"> <slot></slot> <label class="mdc-label" @click="','"> <slot name="label">',"</slot> </label> </div>"])),(0,f.H)(e),this._labelClick,this.label)}},{kind:"method",key:"_labelClick",value:function(){var e=this.input;if(e&&(e.focus(),!e.disabled))switch(e.tagName){case"HA-CHECKBOX":e.checked=!e.checked,(0,p.r)(e,"change");break;case"HA-RADIO":e.checked=!0,(0,p.r)(e,"change");break;default:e.click()}}},{kind:"field",static:!0,key:"styles",value:function(){return[u.R,(0,g.AH)(o||(o=(0,a.A)([":host(:not([alignEnd])) ::slotted(ha-switch){margin-right:10px;margin-inline-end:10px;margin-inline-start:inline}.mdc-form-field{align-items:var(--ha-formfield-align-items,center);gap:4px}.mdc-form-field>label{direction:var(--direction);margin-inline-start:0;margin-inline-end:auto;padding:0}:host([disabled]) label{color:var(--disabled-text-color)}"])))]}}]}}),h.M)},59588:function(e,i,t){var n,o=t(64599),a=t(35806),r=t(71008),s=t(62193),l=t(2816),d=t(27927),c=t(35890),h=(t(81027),t(71204)),u=t(15031),g=t(15112),m=t(29818),f=t(39914);(0,d.A)([(0,m.EM)("ha-switch")],(function(e,i){var t=function(i){function t(){var i;(0,r.A)(this,t);for(var n=arguments.length,o=new Array(n),a=0;a<n;a++)o[a]=arguments[a];return i=(0,s.A)(this,t,[].concat(o)),e(i),i}return(0,l.A)(t,i),(0,a.A)(t)}(i);return{F:t,d:[{kind:"field",decorators:[(0,m.MZ)({type:Boolean})],key:"haptic",value:function(){return!1}},{kind:"method",key:"firstUpdated",value:function(){var e=this;(0,c.A)(t,"firstUpdated",this,3)([]),this.addEventListener("change",(function(){e.haptic&&(0,f.j)("light")}))}},{kind:"field",static:!0,key:"styles",value:function(){return[u.R,(0,g.AH)(n||(n=(0,o.A)([":host{--mdc-theme-secondary:var(--switch-checked-color)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:var(--switch-checked-button-color);border-color:var(--switch-checked-button-color)}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:var(--switch-checked-track-color);border-color:var(--switch-checked-track-color)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:var(--switch-unchecked-button-color);border-color:var(--switch-unchecked-button-color)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:var(--switch-unchecked-track-color);border-color:var(--switch-unchecked-track-color)}"])))]}}]}}),h.U)},89032:function(e,i,t){t.r(i);var n,o,a,r,s,l=t(64599),d=t(33994),c=t(22858),h=t(35806),u=t(71008),g=t(62193),m=t(2816),f=t(27927),p=(t(81027),t(54838),t(15112)),v=t(29818),_=t(34897),k=(t(3276),t(24284),t(59588),t(31265)),b=t(55321),y=t(6121);(0,f.A)([(0,v.EM)("dialog-config-entry-system-options")],(function(e,i){var t,f,w=function(i){function t(){var i;(0,u.A)(this,t);for(var n=arguments.length,o=new Array(n),a=0;a<n;a++)o[a]=arguments[a];return i=(0,g.A)(this,t,[].concat(o)),e(i),i}return(0,m.A)(t,i),(0,h.A)(t)}(i);return{F:w,d:[{kind:"field",decorators:[(0,v.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,v.wk)()],key:"_disableNewEntities",value:void 0},{kind:"field",decorators:[(0,v.wk)()],key:"_disablePolling",value:void 0},{kind:"field",decorators:[(0,v.wk)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,v.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,v.wk)()],key:"_submitting",value:function(){return!1}},{kind:"method",key:"showDialog",value:(f=(0,c.A)((0,d.A)().mark((function e(i){return(0,d.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:this._params=i,this._error=void 0,this._disableNewEntities=i.entry.pref_disable_new_entities,this._disablePolling=i.entry.pref_disable_polling;case 4:case"end":return e.stop()}}),e,this)}))),function(e){return f.apply(this,arguments)})},{kind:"method",key:"closeDialog",value:function(){this._error="",this._params=void 0,(0,_.r)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return this._params?(0,p.qy)(n||(n=(0,l.A)([' <ha-dialog open @closed="','" .heading="','"> ',' <ha-formfield .label="','"> <ha-switch .checked="','" @change="','" .disabled="','" dialogInitialFocus></ha-switch> </ha-formfield> <ha-formfield .label="','"> <ha-switch .checked="','" @change="','" .disabled="','"></ha-switch> </ha-formfield> <mwc-button slot="secondaryAction" @click="','" .disabled="','"> ',' </mwc-button> <mwc-button slot="primaryAction" @click="','" .disabled="','"> '," </mwc-button> </ha-dialog> "])),this.closeDialog,this.hass.localize("ui.dialogs.config_entry_system_options.title",{integration:this.hass.localize("component.".concat(this._params.entry.domain,".title"))||this._params.entry.domain}),this._error?(0,p.qy)(o||(o=(0,l.A)([' <div class="error">',"</div> "])),this._error):"",(0,p.qy)(a||(a=(0,l.A)(["<p> ",' </p> <p class="secondary"> '," </p>"])),this.hass.localize("ui.dialogs.config_entry_system_options.enable_new_entities_label"),this.hass.localize("ui.dialogs.config_entry_system_options.enable_new_entities_description",{integration:this.hass.localize("component.".concat(this._params.entry.domain,".title"))||this._params.entry.domain})),!this._disableNewEntities,this._disableNewEntitiesChanged,this._submitting,(0,p.qy)(r||(r=(0,l.A)(["<p> ",' </p> <p class="secondary"> '," </p>"])),this.hass.localize("ui.dialogs.config_entry_system_options.enable_polling_label"),this.hass.localize("ui.dialogs.config_entry_system_options.enable_polling_description",{integration:this.hass.localize("component.".concat(this._params.entry.domain,".title"))||this._params.entry.domain})),!this._disablePolling,this._disablePollingChanged,this._submitting,this.closeDialog,this._submitting,this.hass.localize("ui.common.cancel"),this._updateEntry,this._submitting,this.hass.localize("ui.dialogs.config_entry_system_options.update")):p.s6}},{kind:"method",key:"_disableNewEntitiesChanged",value:function(e){this._error=void 0,this._disableNewEntities=!e.target.checked}},{kind:"method",key:"_disablePollingChanged",value:function(e){this._error=void 0,this._disablePolling=!e.target.checked}},{kind:"method",key:"_updateEntry",value:(t=(0,c.A)((0,d.A)().mark((function e(){var i;return(0,d.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return this._submitting=!0,(i={pref_disable_new_entities:this._disableNewEntities}).pref_disable_polling=this._disablePolling,e.prev=3,e.next=6,(0,k.iH)(this.hass,this._params.entry.entry_id,i);case 6:if(!e.sent.require_restart){e.next=10;break}return e.next=10,(0,y.showAlertDialog)(this,{text:this.hass.localize("ui.dialogs.config_entry_system_options.restart_home_assistant")});case 10:this.closeDialog(),e.next=16;break;case 13:e.prev=13,e.t0=e.catch(3),this._error=e.t0.message||"Unknown error";case 16:return e.prev=16,this._submitting=!1,e.finish(16);case 19:case"end":return e.stop()}}),e,this,[[3,13,16,19]])}))),function(){return t.apply(this,arguments)})},{kind:"get",static:!0,key:"styles",value:function(){return[b.nA,(0,p.AH)(s||(s=(0,l.A)([".error{color:var(--error-color)}"])))]}}]}}),p.WF)}}]);
//# sourceMappingURL=66651.8rrmOj-q42w.js.map