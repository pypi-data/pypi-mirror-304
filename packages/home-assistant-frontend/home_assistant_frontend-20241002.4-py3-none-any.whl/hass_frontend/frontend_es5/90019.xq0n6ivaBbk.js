(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[90019],{3276:function(t,i,e){"use strict";e.d(i,{l:function(){return k}});var a,o,n,r=e(35806),l=e(71008),d=e(62193),c=e(2816),s=e(27927),u=e(35890),p=e(64599),h=(e(71522),e(81027),e(79243),e(54653)),g=e(34599),f=e(15112),v=e(29818),m=e(90952),b=(e(28066),["button","ha-list-item"]),k=function(t,i){var e;return(0,f.qy)(a||(a=(0,p.A)([' <div class="header_title"> <span>','</span> <ha-icon-button .label="','" .path="','" dialogAction="close" class="header_button"></ha-icon-button> </div> '])),i,null!==(e=null==t?void 0:t.localize("ui.dialogs.generic.close"))&&void 0!==e?e:"Close","M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z")};(0,s.A)([(0,v.EM)("ha-dialog")],(function(t,i){var e=function(i){function e(){var i;(0,l.A)(this,e);for(var a=arguments.length,o=new Array(a),n=0;n<a;n++)o[n]=arguments[n];return i=(0,d.A)(this,e,[].concat(o)),t(i),i}return(0,c.A)(e,i),(0,r.A)(e)}(i);return{F:e,d:[{kind:"field",key:m.Xr,value:void 0},{kind:"method",key:"scrollToPos",value:function(t,i){var e;null===(e=this.contentElement)||void 0===e||e.scrollTo(t,i)}},{kind:"method",key:"renderHeading",value:function(){return(0,f.qy)(o||(o=(0,p.A)(['<slot name="heading"> '," </slot>"])),(0,u.A)(e,"renderHeading",this,3)([]))}},{kind:"method",key:"firstUpdated",value:function(){var t;(0,u.A)(e,"firstUpdated",this,3)([]),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,b].join(", "),this._updateScrolledAttribute(),null===(t=this.contentElement)||void 0===t||t.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,u.A)(e,"disconnectedCallback",this,3)([]),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value:function(){var t=this;return function(){t._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value:function(){return[g.R,(0,f.AH)(n||(n=(0,p.A)([":host([scrolled]) ::slotted(ha-dialog-header){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.mdc-dialog{--mdc-dialog-scroll-divider-color:var(\n          --dialog-scroll-divider-color,\n          var(--divider-color)\n        );z-index:var(--dialog-z-index,8);-webkit-backdrop-filter:var(--ha-dialog-scrim-backdrop-filter,var(--dialog-backdrop-filter,none));backdrop-filter:var(--ha-dialog-scrim-backdrop-filter,var(--dialog-backdrop-filter,none));--mdc-dialog-box-shadow:var(--dialog-box-shadow, none);--mdc-typography-headline6-font-weight:400;--mdc-typography-headline6-font-size:1.574rem}.mdc-dialog__actions{justify-content:var(--justify-action-buttons,flex-end);padding-bottom:max(env(safe-area-inset-bottom),24px)}.mdc-dialog__actions span:first-child{flex:var(--secondary-action-button-flex,unset)}.mdc-dialog__actions span:nth-child(2){flex:var(--primary-action-button-flex,unset)}.mdc-dialog__container{align-items:var(--vertical-align-dialog,center)}.mdc-dialog__title{padding:24px 24px 0 24px}.mdc-dialog__actions{padding:12px 24px 12px 24px}.mdc-dialog__title::before{content:unset}.mdc-dialog .mdc-dialog__content{position:var(--dialog-content-position,relative);padding:var(--dialog-content-padding,24px)}:host([hideactions]) .mdc-dialog .mdc-dialog__content{padding-bottom:max(var(--dialog-content-padding,24px),env(safe-area-inset-bottom))}.mdc-dialog .mdc-dialog__surface{position:var(--dialog-surface-position,relative);top:var(--dialog-surface-top);margin-top:var(--dialog-surface-margin-top);min-height:var(--mdc-dialog-min-height,auto);border-radius:var(--ha-dialog-border-radius,28px);-webkit-backdrop-filter:var(--ha-dialog-surface-backdrop-filter,none);backdrop-filter:var(--ha-dialog-surface-backdrop-filter,none);background:var(--ha-dialog-surface-background,var(--mdc-theme-surface,#fff))}:host([flexContent]) .mdc-dialog .mdc-dialog__content{display:flex;flex-direction:column}.header_title{position:relative;padding-right:40px;padding-inline-end:40px;padding-inline-start:initial;direction:var(--direction)}.header_title span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:block}.header_button{position:absolute;right:-12px;top:-12px;text-decoration:none;color:inherit;inset-inline-start:initial;inset-inline-end:-12px;direction:var(--direction)}.dialog-actions{inset-inline-start:initial!important;inset-inline-end:0px!important;direction:var(--direction)}"])))]}}]}}),h.u)},90019:function(t,i,e){"use strict";var a=e(22858).A,o=e(33994).A;e.a(t,function(){var t=a(o().mark((function t(a,n){var r,l,d,c,s,u,p,h,g,f,v,m,b,k,_,x,A,y,w;return o().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(t.prev=0,e.r(i),r=e(64599),l=e(35806),d=e(71008),c=e(62193),s=e(2816),u=e(27927),p=e(81027),h=e(97741),g=e(16891),e(54838),f=e(15112),v=e(29818),m=e(8581),b=e(34897),k=e(3276),_=e(55321),!(x=a([m])).then){t.next=29;break}return t.next=25,x;case 25:t.t1=t.sent,t.t0=(0,t.t1)(),t.next=30;break;case 29:t.t0=x;case 30:m=t.t0[0],(0,u.A)([(0,v.EM)("dialog-cloud-certificate")],(function(t,i){var e=function(i){function e(){var i;(0,d.A)(this,e);for(var a=arguments.length,o=new Array(a),n=0;n<a;n++)o[n]=arguments[n];return i=(0,c.A)(this,e,[].concat(o)),t(i),i}return(0,s.A)(e,i),(0,l.A)(e)}(i);return{F:e,d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,v.wk)()],key:"_params",value:void 0},{kind:"method",key:"showDialog",value:function(t){this._params=t}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,(0,b.r)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){if(!this._params)return f.s6;var t=this._params.certificateInfo;return(0,f.qy)(A||(A=(0,r.A)([' <ha-dialog open hideActions @closed="','" .heading="','"> <div> <p> '," ","<br> (",') </p> <p class="break-word"> '," ",' </p> <p class="break-word"> '," </p> <ul> ",' </ul> </div> <mwc-button @click="','" slot="primaryAction"> '," </mwc-button> </ha-dialog> "])),this.closeDialog,(0,k.l)(this.hass,this.hass.localize("ui.panel.config.cloud.dialog_certificate.certificate_information")),this.hass.localize("ui.panel.config.cloud.dialog_certificate.certificate_expiration_date"),(0,m.r6)(new Date(t.expire_date),this.hass.locale,this.hass.config),this.hass.localize("ui.panel.config.cloud.dialog_certificate.will_be_auto_renewed"),this.hass.localize("ui.panel.config.cloud.dialog_certificate.fingerprint"),t.fingerprint,this.hass.localize("ui.panel.config.cloud.dialog_certificate.alternative_names"),t.alternative_names.map((function(t){return(0,f.qy)(y||(y=(0,r.A)(["<li><code>","</code></li>"])),t)})),this.closeDialog,this.hass.localize("ui.panel.config.cloud.dialog_certificate.close"))}},{kind:"get",static:!0,key:"styles",value:function(){return[_.nA,(0,f.AH)(w||(w=(0,r.A)(["ha-dialog{--mdc-dialog-max-width:535px}.break-word{overflow-wrap:break-word}p{margin-top:0;margin-bottom:12px}p:last-child{margin-bottom:0}"])))]}}]}}),f.WF),n(),t.next=38;break;case 35:t.prev=35,t.t2=t.catch(0),n(t.t2);case 38:case"end":return t.stop()}}),t,null,[[0,35]])})));return function(i,e){return t.apply(this,arguments)}}())},71522:function(){Element.prototype.toggleAttribute||(Element.prototype.toggleAttribute=function(t,i){return void 0!==i&&(i=!!i),this.hasAttribute(t)?!!i||(this.removeAttribute(t),!1):!1!==i&&(this.setAttribute(t,""),!0)})}}]);
//# sourceMappingURL=90019.xq0n6ivaBbk.js.map