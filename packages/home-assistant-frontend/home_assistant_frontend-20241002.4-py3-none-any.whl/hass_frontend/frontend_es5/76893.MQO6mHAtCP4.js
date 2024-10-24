/*! For license information please see 76893.MQO6mHAtCP4.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[76893],{42072:function(e,i,t){var o=t(22711).default;t(72488),t(62635),t(95554),t(39790),t(253),t(54846),t(66555),e.exports=function e(i){return Object.freeze(i),Object.getOwnPropertyNames(i).forEach((function(t){!i.hasOwnProperty(t)||null===i[t]||"object"!==o(i[t])&&"function"!=typeof i[t]||Object.isFrozen(i[t])||e(i[t])})),i}},37629:function(e,i,t){"use strict";t.r(i),t.d(i,{HaCircularProgress:function(){return f}});var o,r=t(64599),a=t(41981),n=t(35806),d=t(71008),s=t(62193),c=t(2816),l=t(27927),u=t(35890),h=(t(81027),t(99322)),v=t(15112),g=t(29818),f=(0,l.A)([(0,g.EM)("ha-circular-progress")],(function(e,i){var t=function(i){function t(){var i;(0,d.A)(this,t);for(var o=arguments.length,r=new Array(o),a=0;a<o;a++)r[a]=arguments[a];return i=(0,s.A)(this,t,[].concat(r)),e(i),i}return(0,c.A)(t,i),(0,n.A)(t)}(i);return{F:t,d:[{kind:"field",decorators:[(0,g.MZ)({attribute:"aria-label",type:String})],key:"ariaLabel",value:function(){return"Loading"}},{kind:"field",decorators:[(0,g.MZ)()],key:"size",value:function(){return"medium"}},{kind:"method",key:"updated",value:function(e){if((0,u.A)(t,"updated",this,3)([e]),e.has("size"))switch(this.size){case"tiny":this.style.setProperty("--md-circular-progress-size","16px");break;case"small":this.style.setProperty("--md-circular-progress-size","28px");break;case"medium":this.style.setProperty("--md-circular-progress-size","48px");break;case"large":this.style.setProperty("--md-circular-progress-size","68px")}}},{kind:"field",static:!0,key:"styles",value:function(){return[].concat((0,a.A)((0,u.A)(t,"styles",this)),[(0,v.AH)(o||(o=(0,r.A)([":host{--md-sys-color-primary:var(--primary-color);--md-circular-progress-size:48px}"])))])}}]}}),h.U)},10900:function(e,i,t){"use strict";var o,r,a=t(64599),n=t(35806),d=t(71008),s=t(62193),c=t(2816),l=t(27927),u=(t(81027),t(15112)),h=t(29818);(0,l.A)([(0,h.EM)("ha-dialog-header")],(function(e,i){var t=function(i){function t(){var i;(0,d.A)(this,t);for(var o=arguments.length,r=new Array(o),a=0;a<o;a++)r[a]=arguments[a];return i=(0,s.A)(this,t,[].concat(r)),e(i),i}return(0,c.A)(t,i),(0,n.A)(t)}(i);return{F:t,d:[{kind:"method",key:"render",value:function(){return(0,u.qy)(o||(o=(0,a.A)([' <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> <div class="header-title"> <slot name="title"></slot> </div> <div class="header-subtitle"> <slot name="subtitle"></slot> </div> </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> '])))}},{kind:"get",static:!0,key:"styles",value:function(){return[(0,u.AH)(r||(r=(0,a.A)([":host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:flex-start;padding:4px;box-sizing:border-box}.header-content{flex:1;padding:10px 4px;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{font-size:22px;line-height:28px;font-weight:400}.header-subtitle{font-size:14px;line-height:20px;color:var(--secondary-text-color)}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:12px}}.header-navigation-icon{flex:none;min-width:8px;height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:8px;height:100%;display:flex;flex-direction:row}"])))]}}]}}),u.WF)},3276:function(e,i,t){"use strict";t.d(i,{l:function(){return _}});var o,r,a,n=t(35806),d=t(71008),s=t(62193),c=t(2816),l=t(27927),u=t(35890),h=t(64599),v=(t(71522),t(81027),t(79243),t(54653)),g=t(34599),f=t(15112),p=t(29818),m=t(90952),b=(t(28066),["button","ha-list-item"]),_=function(e,i){var t;return(0,f.qy)(o||(o=(0,h.A)([' <div class="header_title"> <span>','</span> <ha-icon-button .label="','" .path="','" dialogAction="close" class="header_button"></ha-icon-button> </div> '])),i,null!==(t=null==e?void 0:e.localize("ui.dialogs.generic.close"))&&void 0!==t?t:"Close","M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z")};(0,l.A)([(0,p.EM)("ha-dialog")],(function(e,i){var t=function(i){function t(){var i;(0,d.A)(this,t);for(var o=arguments.length,r=new Array(o),a=0;a<o;a++)r[a]=arguments[a];return i=(0,s.A)(this,t,[].concat(r)),e(i),i}return(0,c.A)(t,i),(0,n.A)(t)}(i);return{F:t,d:[{kind:"field",key:m.Xr,value:void 0},{kind:"method",key:"scrollToPos",value:function(e,i){var t;null===(t=this.contentElement)||void 0===t||t.scrollTo(e,i)}},{kind:"method",key:"renderHeading",value:function(){return(0,f.qy)(r||(r=(0,h.A)(['<slot name="heading"> '," </slot>"])),(0,u.A)(t,"renderHeading",this,3)([]))}},{kind:"method",key:"firstUpdated",value:function(){var e;(0,u.A)(t,"firstUpdated",this,3)([]),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,b].join(", "),this._updateScrolledAttribute(),null===(e=this.contentElement)||void 0===e||e.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,u.A)(t,"disconnectedCallback",this,3)([]),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value:function(){var e=this;return function(){e._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value:function(){return[g.R,(0,f.AH)(a||(a=(0,h.A)([":host([scrolled]) ::slotted(ha-dialog-header){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.mdc-dialog{--mdc-dialog-scroll-divider-color:var(\n          --dialog-scroll-divider-color,\n          var(--divider-color)\n        );z-index:var(--dialog-z-index,8);-webkit-backdrop-filter:var(--ha-dialog-scrim-backdrop-filter,var(--dialog-backdrop-filter,none));backdrop-filter:var(--ha-dialog-scrim-backdrop-filter,var(--dialog-backdrop-filter,none));--mdc-dialog-box-shadow:var(--dialog-box-shadow, none);--mdc-typography-headline6-font-weight:400;--mdc-typography-headline6-font-size:1.574rem}.mdc-dialog__actions{justify-content:var(--justify-action-buttons,flex-end);padding-bottom:max(env(safe-area-inset-bottom),24px)}.mdc-dialog__actions span:first-child{flex:var(--secondary-action-button-flex,unset)}.mdc-dialog__actions span:nth-child(2){flex:var(--primary-action-button-flex,unset)}.mdc-dialog__container{align-items:var(--vertical-align-dialog,center)}.mdc-dialog__title{padding:24px 24px 0 24px}.mdc-dialog__actions{padding:12px 24px 12px 24px}.mdc-dialog__title::before{content:unset}.mdc-dialog .mdc-dialog__content{position:var(--dialog-content-position,relative);padding:var(--dialog-content-padding,24px)}:host([hideactions]) .mdc-dialog .mdc-dialog__content{padding-bottom:max(var(--dialog-content-padding,24px),env(safe-area-inset-bottom))}.mdc-dialog .mdc-dialog__surface{position:var(--dialog-surface-position,relative);top:var(--dialog-surface-top);margin-top:var(--dialog-surface-margin-top);min-height:var(--mdc-dialog-min-height,auto);border-radius:var(--ha-dialog-border-radius,28px);-webkit-backdrop-filter:var(--ha-dialog-surface-backdrop-filter,none);backdrop-filter:var(--ha-dialog-surface-backdrop-filter,none);background:var(--ha-dialog-surface-background,var(--mdc-theme-surface,#fff))}:host([flexContent]) .mdc-dialog .mdc-dialog__content{display:flex;flex-direction:column}.header_title{position:relative;padding-right:40px;padding-inline-end:40px;padding-inline-start:initial;direction:var(--direction)}.header_title span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:block}.header_button{position:absolute;right:-12px;top:-12px;text-decoration:none;color:inherit;inset-inline-start:initial;inset-inline-end:-12px;direction:var(--direction)}.dialog-actions{inset-inline-start:initial!important;inset-inline-end:0px!important;direction:var(--direction)}"])))]}}]}}),v.u)},22959:function(e,i,t){"use strict";var o,r,a,n,d,s,c,l=t(64599),u=t(33994),h=t(22858),v=t(35806),g=t(71008),f=t(62193),p=t(2816),m=t(27927),b=t(35890),_=(t(81027),t(39805),t(97741),t(13618),t(34736),t(15112)),y=t(29818),k=t(34308),x=t(89403),w=(t(26098),t(34897)),A=(t(13292),t(89053),(0,m.A)([(0,y.EM)("hui-badge-visibility-editor")],(function(e,i){var t=function(i){function t(){var i;(0,g.A)(this,t);for(var o=arguments.length,r=new Array(o),a=0;a<o;a++)r[a]=arguments[a];return i=(0,f.A)(this,t,[].concat(r)),e(i),i}return(0,p.A)(t,i),(0,v.A)(t)}(i);return{F:t,d:[{kind:"field",decorators:[(0,y.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,y.MZ)({attribute:!1})],key:"config",value:void 0},{kind:"method",key:"render",value:function(){var e,i=null!==(e=this.config.visibility)&&void 0!==e?e:[];return(0,_.qy)(o||(o=(0,l.A)([' <p class="intro"> ',' </p> <ha-card-conditions-editor .hass="','" .conditions="','" @value-changed="','"> </ha-card-conditions-editor> '])),this.hass.localize("ui.panel.lovelace.editor.edit_badge.visibility.explanation"),this.hass,i,this._valueChanged)}},{kind:"method",key:"_valueChanged",value:function(e){var i;e.stopPropagation();var t=e.detail.value,o=Object.assign(Object.assign({},this.config),{},{visibility:t});0===(null===(i=o.visibility)||void 0===i?void 0:i.length)&&delete o.visibility,(0,w.r)(this,"value-changed",{value:o})}},{kind:"field",static:!0,key:"styles",value:function(){return(0,_.AH)(r||(r=(0,l.A)([".intro{margin:0;color:var(--secondary-text-color);margin-bottom:8px}"])))}}]}}),_.WF),["config","visibility"]);(0,m.A)([(0,y.EM)("hui-badge-element-editor")],(function(e,i){var t,o,r=function(i){function t(){var i;(0,g.A)(this,t);for(var o=arguments.length,r=new Array(o),a=0;a<o;a++)r[a]=arguments[a];return i=(0,f.A)(this,t,[].concat(r)),e(i),i}return(0,p.A)(t,i),(0,v.A)(t)}(i);return{F:r,d:[{kind:"field",decorators:[(0,y.wk)()],key:"_currTab",value:function(){return A[0]}},{kind:"method",key:"getConfigElement",value:(o=(0,h.A)((0,u.A)().mark((function e(){var i;return(0,u.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,(0,k.ww)(this.configElementType);case 2:if(!(i=e.sent)||!i.getConfigElement){e.next=5;break}return e.abrupt("return",i.getConfigElement());case 5:return e.abrupt("return",void 0);case 6:case"end":return e.stop()}}),e,this)}))),function(){return o.apply(this,arguments)})},{kind:"method",key:"getConfigForm",value:(t=(0,h.A)((0,u.A)().mark((function e(){var i;return(0,u.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,(0,k.ww)(this.configElementType);case 2:if(!(i=e.sent)||!i.getConfigForm){e.next=5;break}return e.abrupt("return",i.getConfigForm());case 5:return e.abrupt("return",void 0);case 6:case"end":return e.stop()}}),e,this)}))),function(){return t.apply(this,arguments)})},{kind:"method",key:"_handleTabChanged",value:function(e){var i=A[e.detail.index];i!==this._currTab&&(this._currTab=i)}},{kind:"method",key:"_configChanged",value:function(e){e.stopPropagation(),this.value=e.detail.value}},{kind:"method",key:"renderConfigElement",value:function(){var e=this,i=_.s6;switch(this._currTab){case"config":i=(0,_.qy)(a||(a=(0,l.A)(["",""])),(0,b.A)(r,"renderConfigElement",this,3)([]));break;case"visibility":i=(0,_.qy)(n||(n=(0,l.A)([' <hui-badge-visibility-editor .hass="','" .config="','" @value-changed="','"></hui-badge-visibility-editor> '])),this.hass,this.value,this._configChanged)}return(0,_.qy)(d||(d=(0,l.A)([' <mwc-tab-bar .activeIndex="','" @MDCTabBar:activated="','"> '," </mwc-tab-bar> "," "])),A.indexOf(this._currTab),this._handleTabChanged,A.map((function(i){return(0,_.qy)(s||(s=(0,l.A)([' <mwc-tab .label="','"> </mwc-tab> '])),e.hass.localize("ui.panel.lovelace.editor.edit_badge.tab_".concat(i)))})),i)}},{kind:"get",static:!0,key:"styles",value:function(){return[x.U.styles,(0,_.AH)(c||(c=(0,l.A)(["mwc-tab-bar{text-transform:uppercase;margin-bottom:16px;border-bottom:1px solid var(--divider-color)}"])))]}}]}}),x.U)},76893:function(e,i,t){"use strict";var o=t(22858).A,r=t(33994).A;t.a(e,function(){var e=o(r().mark((function e(o,a){var n,d,s,c,l,u,h,v,g,f,p,m,b,_,y,k,x,w,A,C,E,z,L,M,I,U,T,q,P,F,H,j,R,S,Z,D,K,O,G,B;return r().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(e.prev=0,t.r(i),t.d(i,{HuiDialogEditBadge:function(){return B}}),n=t(41981),d=t(64599),s=t(33994),c=t(22858),l=t(35806),u=t(71008),h=t(62193),v=t(2816),g=t(27927),f=t(71499),p=t(81027),m=t(50693),b=t(95554),_=t(39790),y=t(66457),k=t(55228),x=t(42072),w=t.n(x),A=t(15112),C=t(29818),E=t(34897),z=t(40368),t(37629),t(3276),t(10900),t(28066),L=t(28132),M=t(33257),I=t(6121),U=t(55321),T=t(50157),t(54494),q=t(26566),P=t(23754),F=t(42533),H=t(14182),t(22959),!(j=o([q])).then){e.next=55;break}return e.next=51,j;case 51:e.t1=e.sent,e.t0=(0,e.t1)(),e.next=56;break;case 55:e.t0=j;case 56:q=e.t0[0],B=(0,g.A)([(0,C.EM)("hui-dialog-edit-badge")],(function(e,i){var t,o,r,a=function(i){function t(){var i;(0,u.A)(this,t);for(var o=arguments.length,r=new Array(o),a=0;a<o;a++)r[a]=arguments[a];return i=(0,h.A)(this,t,[].concat(r)),e(i),i}return(0,v.A)(t,i),(0,l.A)(t)}(i);return{F:a,d:[{kind:"field",decorators:[(0,C.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,C.MZ)({type:Boolean,reflect:!0})],key:"large",value:function(){return!1}},{kind:"field",decorators:[(0,C.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,C.wk)()],key:"_badgeConfig",value:void 0},{kind:"field",decorators:[(0,C.wk)()],key:"_containerConfig",value:void 0},{kind:"field",decorators:[(0,C.wk)()],key:"_saving",value:function(){return!1}},{kind:"field",decorators:[(0,C.wk)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,C.wk)()],key:"_guiModeAvailable",value:function(){return!0}},{kind:"field",decorators:[(0,C.P)("hui-badge-element-editor")],key:"_badgeEditorEl",value:void 0},{kind:"field",decorators:[(0,C.wk)()],key:"_GUImode",value:function(){return!0}},{kind:"field",decorators:[(0,C.wk)()],key:"_documentationURL",value:void 0},{kind:"field",decorators:[(0,C.wk)()],key:"_dirty",value:function(){return!1}},{kind:"field",decorators:[(0,C.wk)()],key:"_isEscapeEnabled",value:function(){return!0}},{kind:"method",key:"showDialog",value:(r=(0,c.A)((0,s.A)().mark((function e(i){var t,o,r;return(0,s.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(this._params=i,this._GUImode=!0,this._guiModeAvailable=!0,!("strategy"in(t=(0,H.ys)(i.lovelaceConfig,i.path)))){e.next=6;break}throw new Error("Can't edit strategy");case 6:this._containerConfig=t,"badgeConfig"in i?(this._badgeConfig=i.badgeConfig,this._dirty=!0):(r=null===(o=this._containerConfig.badges)||void 0===o?void 0:o[i.badgeIndex],this._badgeConfig=null!=r?(0,L.q)(r):r),this.large=!1,this._badgeConfig&&!Object.isFrozen(this._badgeConfig)&&(this._badgeConfig=w()(this._badgeConfig));case 10:case"end":return e.stop()}}),e,this)}))),function(e){return r.apply(this,arguments)})},{kind:"method",key:"closeDialog",value:function(){return this._isEscapeEnabled=!0,window.removeEventListener("dialog-closed",this._enableEscapeKeyClose),window.removeEventListener("hass-more-info",this._disableEscapeKeyClose),this._dirty?(this._confirmCancel(),!1):(this._params=void 0,this._badgeConfig=void 0,this._error=void 0,this._documentationURL=void 0,this._dirty=!1,(0,E.r)(this,"dialog-closed",{dialog:this.localName}),!0)}},{kind:"method",key:"updated",value:function(e){if(this._badgeConfig&&void 0===this._documentationURL&&e.has("_badgeConfig")){var i=e.get("_badgeConfig");(null==i?void 0:i.type)!==this._badgeConfig.type&&(this._documentationURL=this._badgeConfig.type?(0,F.R)(this.hass,this._badgeConfig.type):void 0)}}},{kind:"field",key:"_enableEscapeKeyClose",value:function(){var e=this;return function(i){"ha-more-info-dialog"===i.detail.dialog&&(e._isEscapeEnabled=!0)}}},{kind:"field",key:"_disableEscapeKeyClose",value:function(){var e=this;return function(){e._isEscapeEnabled=!1}}},{kind:"method",key:"render",value:function(){if(!this._params)return A.s6;var e;if(this._badgeConfig&&this._badgeConfig.type){var i,t,o;if((0,M.c8)(this._badgeConfig.type))null!==(o=i=null===(t=(0,M.b$)((0,M.Iu)(this._badgeConfig.type)))||void 0===t?void 0:t.name)&&void 0!==o&&o.toLowerCase().endsWith(" badge")&&(i=i.substring(0,i.length-6));else i=this.hass.localize("ui.panel.lovelace.editor.badge.".concat(this._badgeConfig.type,".name"));e=this.hass.localize("ui.panel.lovelace.editor.edit_badge.typed_header",{type:i})}else e=this._badgeConfig?this.hass.localize("ui.panel.lovelace.editor.edit_badge.header"):this._containerConfig.title?this.hass.localize("ui.panel.lovelace.editor.edit_badge.pick_badge_view_title",{name:this._containerConfig.title}):this.hass.localize("ui.panel.lovelace.editor.edit_badge.pick_badge");return(0,A.qy)(R||(R=(0,d.A)([' <ha-dialog open scrimClickAction .escapeKeyAction="','" @keydown="','" @closed="','" @opened="','" .heading="','"> <ha-dialog-header slot="heading"> <ha-icon-button slot="navigationIcon" dialogAction="cancel" .label="','" .path="','"></ha-icon-button> <span slot="title" @click="','">',"</span> ",' </ha-dialog-header> <div class="content"> <div class="element-editor"> <hui-badge-element-editor .hass="','" .lovelace="','" .value="','" @config-changed="','" @GUImode-changed="','" @editor-save="','" dialogInitialFocus></hui-badge-element-editor> </div> <div class="element-preview"> <hui-badge .hass="','" .config="','" preview class="','"></hui-badge> '," </div> </div> ",' <div slot="primaryAction" @click="','"> <mwc-button @click="','" dialogInitialFocus> '," </mwc-button> "," </div> </ha-dialog> "])),this._isEscapeEnabled?void 0:"",this._ignoreKeydown,this._cancel,this._opened,e,this.hass.localize("ui.common.close"),"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",this._enlarge,e,void 0!==this._documentationURL?(0,A.qy)(S||(S=(0,d.A)([' <a slot="actionItems" href="','" title="','" target="_blank" rel="noreferrer" dir="','"> <ha-icon-button .path="','"></ha-icon-button> </a> '])),this._documentationURL,this.hass.localize("ui.panel.lovelace.menu.help"),(0,z.Vc)(this.hass),"M15.07,11.25L14.17,12.17C13.45,12.89 13,13.5 13,15H11V14.5C11,13.39 11.45,12.39 12.17,11.67L13.41,10.41C13.78,10.05 14,9.55 14,9C14,7.89 13.1,7 12,7A2,2 0 0,0 10,9H8A4,4 0 0,1 12,5A4,4 0 0,1 16,9C16,9.88 15.64,10.67 15.07,11.25M13,19H11V17H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12C22,6.47 17.5,2 12,2Z"):A.s6,this.hass,this._params.lovelaceConfig,this._badgeConfig,this._handleConfigChanged,this._handleGUIModeChanged,this._save,this.hass,this._badgeConfig,this._error?"blur":"",this._error?(0,A.qy)(Z||(Z=(0,d.A)([' <ha-circular-progress indeterminate aria-label="Can\'t update badge"></ha-circular-progress> ']))):"",void 0!==this._badgeConfig?(0,A.qy)(D||(D=(0,d.A)([' <mwc-button slot="secondaryAction" @click="','" .disabled="','" class="gui-mode-button"> '," </mwc-button> "])),this._toggleMode,!this._guiModeAvailable,this.hass.localize(!this._badgeEditorEl||this._GUImode?"ui.panel.lovelace.editor.edit_badge.show_code_editor":"ui.panel.lovelace.editor.edit_badge.show_visual_editor")):"",this._save,this._cancel,this.hass.localize("ui.common.cancel"),void 0!==this._badgeConfig&&this._dirty?(0,A.qy)(K||(K=(0,d.A)([' <mwc-button ?disabled="','" @click="','"> '," </mwc-button> "])),!this._canSave||this._saving,this._save,this._saving?(0,A.qy)(O||(O=(0,d.A)([' <ha-circular-progress indeterminate aria-label="Saving" size="small"></ha-circular-progress> ']))):this.hass.localize("ui.common.save")):"")}},{kind:"method",key:"_enlarge",value:function(){this.large=!this.large}},{kind:"method",key:"_ignoreKeydown",value:function(e){e.stopPropagation()}},{kind:"method",key:"_handleConfigChanged",value:function(e){this._badgeConfig=w()(e.detail.config),this._error=e.detail.error,this._guiModeAvailable=e.detail.guiModeAvailable,this._dirty=!0}},{kind:"method",key:"_handleGUIModeChanged",value:function(e){e.stopPropagation(),this._GUImode=e.detail.guiMode,this._guiModeAvailable=e.detail.guiModeAvailable}},{kind:"method",key:"_toggleMode",value:function(){var e;null===(e=this._badgeEditorEl)||void 0===e||e.toggleMode()}},{kind:"method",key:"_opened",value:function(){var e;window.addEventListener("dialog-closed",this._enableEscapeKeyClose),window.addEventListener("hass-more-info",this._disableEscapeKeyClose),null===(e=this._badgeEditorEl)||void 0===e||e.focusYamlEditor()}},{kind:"get",key:"_canSave",value:function(){return!this._saving&&(void 0!==this._badgeConfig&&(!this._badgeEditorEl||!this._badgeEditorEl.hasError))}},{kind:"method",key:"_confirmCancel",value:(o=(0,c.A)((0,s.A)().mark((function e(){return(0,s.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,new Promise((function(e){setTimeout(e,0)}));case 2:return e.next=4,(0,I.showConfirmationDialog)(this,{title:this.hass.localize("ui.panel.lovelace.editor.edit_badge.unsaved_changes"),text:this.hass.localize("ui.panel.lovelace.editor.edit_badge.confirm_cancel"),dismissText:this.hass.localize("ui.common.stay"),confirmText:this.hass.localize("ui.common.leave")});case 4:e.sent&&this._cancel();case 6:case"end":return e.stop()}}),e,this)}))),function(){return o.apply(this,arguments)})},{kind:"method",key:"_cancel",value:function(e){e&&e.stopPropagation(),this._dirty=!1,this.closeDialog()}},{kind:"method",key:"_save",value:(t=(0,c.A)((0,s.A)().mark((function e(){var i;return(0,s.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(this._canSave){e.next=2;break}return e.abrupt("return");case 2:if(this._dirty){e.next=5;break}return this.closeDialog(),e.abrupt("return");case 5:return this._saving=!0,i=this._params.path,e.next=9,this._params.saveConfig("badgeConfig"in this._params?(0,P.HQ)(this._params.lovelaceConfig,i,this._badgeConfig):(0,P.M)(this._params.lovelaceConfig,[].concat((0,n.A)(i),[this._params.badgeIndex]),this._badgeConfig));case 9:this._saving=!1,this._dirty=!1,(0,T.f)(this,this.hass),this.closeDialog();case 13:case"end":return e.stop()}}),e,this)}))),function(){return t.apply(this,arguments)})},{kind:"get",static:!0,key:"styles",value:function(){return[U.nA,(0,A.AH)(G||(G=(0,d.A)([":host{--code-mirror-max-height:calc(100vh - 176px)}ha-dialog{--mdc-dialog-max-width:100px;--dialog-z-index:6;--dialog-surface-position:fixed;--dialog-surface-top:40px;--mdc-dialog-max-width:90vw;--dialog-content-padding:24px 12px}.content{width:calc(90vw - 48px);max-width:1000px}@media all and (max-width:450px),all and (max-height:500px){ha-dialog{height:100%;--mdc-dialog-max-height:100%;--dialog-surface-top:0px;--mdc-dialog-max-width:100vw}.content{width:100%;max-width:100%}}@media all and (min-width:451px) and (min-height:501px){:host([large]) .content{max-width:none}}.center{margin-left:auto;margin-right:auto}.content{display:flex;flex-direction:column}.content .element-editor{margin:0 10px}@media (min-width:1000px){.content{flex-direction:row}.content>*{flex-basis:0;flex-grow:1;flex-shrink:1;min-width:0}}.hidden{display:none}.element-editor{margin-bottom:8px}.blur{filter:blur(2px) grayscale(100%)}.element-preview{position:relative;height:max-content;background:var(--primary-background-color);padding:10px;border-radius:4px;display:flex;flex-direction:column;justify-content:center;align-items:center}.element-preview ha-circular-progress{top:50%;left:50%;position:absolute;z-index:10}.gui-mode-button{margin-right:auto;margin-inline-end:auto;margin-inline-start:initial}.header{display:flex;align-items:center;justify-content:space-between}ha-dialog-header a{color:inherit;text-decoration:none}"])))]}}]}}),A.WF),a(),e.next=66;break;case 63:e.prev=63,e.t2=e.catch(0),a(e.t2);case 66:case"end":return e.stop()}}),e,null,[[0,63]])})));return function(i,t){return e.apply(this,arguments)}}())},42533:function(e,i,t){"use strict";t.d(i,{R:function(){return n},W:function(){return a}});t(81027);var o=t(33257),r=t(84976),a=function(e,i){var t;return(0,o.c8)(i)?null===(t=(0,o.wi)((0,o.Iu)(i)))||void 0===t?void 0:t.documentationURL:"".concat((0,r.o)(e,"/dashboards/")).concat(i)},n=function(e,i){var t;return(0,o.c8)(i)?null===(t=(0,o.b$)((0,o.Iu)(i)))||void 0===t?void 0:t.documentationURL:"".concat((0,r.o)(e,"/dashboards/badges"))}},84976:function(e,i,t){"use strict";t.d(i,{o:function(){return o}});t(81027),t(82386),t(36604);var o=function(e,i){return"https://".concat(e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www",".home-assistant.io").concat(i)}},50157:function(e,i,t){"use strict";t.d(i,{f:function(){return r}});var o=t(18589),r=function(e,i){return(0,o.P)(e,{message:i.localize("ui.common.successfully_saved")})}},99322:function(e,i,t){"use strict";t.d(i,{U:function(){return _}});var o,r,a,n=t(35806),d=t(71008),s=t(62193),c=t(2816),l=t(79192),u=t(29818),h=t(64599),v=t(15112),g=(t(29193),t(85323)),f=function(e){function i(){var e;return(0,d.A)(this,i),(e=(0,s.A)(this,i,arguments)).value=0,e.max=1,e.indeterminate=!1,e.fourColor=!1,e}return(0,c.A)(i,e),(0,n.A)(i,[{key:"render",value:function(){var e=this.ariaLabel;return(0,v.qy)(o||(o=(0,h.A)([' <div class="progress ','" role="progressbar" aria-label="','" aria-valuemin="0" aria-valuemax="','" aria-valuenow="','">',"</div> "])),(0,g.H)(this.getRenderClasses()),e||v.s6,this.max,this.indeterminate?v.s6:this.value,this.renderIndicator())}},{key:"getRenderClasses",value:function(){return{indeterminate:this.indeterminate,"four-color":this.fourColor}}}])}((0,t(26604).n)(v.WF));(0,l.__decorate)([(0,u.MZ)({type:Number})],f.prototype,"value",void 0),(0,l.__decorate)([(0,u.MZ)({type:Number})],f.prototype,"max",void 0),(0,l.__decorate)([(0,u.MZ)({type:Boolean})],f.prototype,"indeterminate",void 0),(0,l.__decorate)([(0,u.MZ)({type:Boolean,attribute:"four-color"})],f.prototype,"fourColor",void 0);var p,m=function(e){function i(){return(0,d.A)(this,i),(0,s.A)(this,i,arguments)}return(0,c.A)(i,e),(0,n.A)(i,[{key:"renderIndicator",value:function(){return this.indeterminate?this.renderIndeterminateContainer():this.renderDeterminateContainer()}},{key:"renderDeterminateContainer",value:function(){var e=100*(1-this.value/this.max);return(0,v.qy)(r||(r=(0,h.A)([' <svg viewBox="0 0 4800 4800"> <circle class="track" pathLength="100"></circle> <circle class="active-track" pathLength="100" stroke-dashoffset="','"></circle> </svg> '])),e)}},{key:"renderIndeterminateContainer",value:function(){return(0,v.qy)(a||(a=(0,h.A)([' <div class="spinner"> <div class="left"> <div class="circle"></div> </div> <div class="right"> <div class="circle"></div> </div> </div>'])))}}])}(f),b=(0,v.AH)(p||(p=(0,h.A)([":host{--_active-indicator-color:var(--md-circular-progress-active-indicator-color, var(--md-sys-color-primary, #6750a4));--_active-indicator-width:var(--md-circular-progress-active-indicator-width, 10);--_four-color-active-indicator-four-color:var(--md-circular-progress-four-color-active-indicator-four-color, var(--md-sys-color-tertiary-container, #ffd8e4));--_four-color-active-indicator-one-color:var(--md-circular-progress-four-color-active-indicator-one-color, var(--md-sys-color-primary, #6750a4));--_four-color-active-indicator-three-color:var(--md-circular-progress-four-color-active-indicator-three-color, var(--md-sys-color-tertiary, #7d5260));--_four-color-active-indicator-two-color:var(--md-circular-progress-four-color-active-indicator-two-color, var(--md-sys-color-primary-container, #eaddff));--_size:var(--md-circular-progress-size, 48px);display:inline-flex;vertical-align:middle;width:var(--_size);height:var(--_size);position:relative;align-items:center;justify-content:center;contain:strict;content-visibility:auto}.progress{flex:1;align-self:stretch;margin:4px}.active-track,.circle,.left,.progress,.right,.spinner,.track,svg{position:absolute;inset:0}svg{transform:rotate(-90deg)}circle{cx:50%;cy:50%;r:calc(50%*(1 - var(--_active-indicator-width)/ 100));stroke-width:calc(var(--_active-indicator-width)*1%);stroke-dasharray:100;fill:rgba(0,0,0,0)}.active-track{transition:stroke-dashoffset .5s cubic-bezier(0, 0, .2, 1);stroke:var(--_active-indicator-color)}.track{stroke:rgba(0,0,0,0)}.progress.indeterminate{animation:linear infinite linear-rotate;animation-duration:1.568s}.spinner{animation:infinite both rotate-arc;animation-duration:5332ms;animation-timing-function:cubic-bezier(0.4,0,0.2,1)}.left{overflow:hidden;inset:0 50% 0 0}.right{overflow:hidden;inset:0 0 0 50%}.circle{box-sizing:border-box;border-radius:50%;border:solid calc(var(--_active-indicator-width)/ 100*(var(--_size) - 8px));border-color:var(--_active-indicator-color) var(--_active-indicator-color) transparent transparent;animation:expand-arc;animation-iteration-count:infinite;animation-fill-mode:both;animation-duration:1333ms,5332ms;animation-timing-function:cubic-bezier(0.4,0,0.2,1)}.four-color .circle{animation-name:expand-arc,four-color}.left .circle{rotate:135deg;inset:0 -100% 0 0}.right .circle{rotate:100deg;inset:0 0 0 -100%;animation-delay:-.666s,0s}@media(forced-colors:active){.active-track{stroke:CanvasText}.circle{border-color:CanvasText CanvasText Canvas Canvas}}@keyframes expand-arc{0%{transform:rotate(265deg)}50%{transform:rotate(130deg)}100%{transform:rotate(265deg)}}@keyframes rotate-arc{12.5%{transform:rotate(135deg)}25%{transform:rotate(270deg)}37.5%{transform:rotate(405deg)}50%{transform:rotate(540deg)}62.5%{transform:rotate(675deg)}75%{transform:rotate(810deg)}87.5%{transform:rotate(945deg)}100%{transform:rotate(1080deg)}}@keyframes linear-rotate{to{transform:rotate(360deg)}}@keyframes four-color{0%{border-top-color:var(--_four-color-active-indicator-one-color);border-right-color:var(--_four-color-active-indicator-one-color)}15%{border-top-color:var(--_four-color-active-indicator-one-color);border-right-color:var(--_four-color-active-indicator-one-color)}25%{border-top-color:var(--_four-color-active-indicator-two-color);border-right-color:var(--_four-color-active-indicator-two-color)}40%{border-top-color:var(--_four-color-active-indicator-two-color);border-right-color:var(--_four-color-active-indicator-two-color)}50%{border-top-color:var(--_four-color-active-indicator-three-color);border-right-color:var(--_four-color-active-indicator-three-color)}65%{border-top-color:var(--_four-color-active-indicator-three-color);border-right-color:var(--_four-color-active-indicator-three-color)}75%{border-top-color:var(--_four-color-active-indicator-four-color);border-right-color:var(--_four-color-active-indicator-four-color)}90%{border-top-color:var(--_four-color-active-indicator-four-color);border-right-color:var(--_four-color-active-indicator-four-color)}100%{border-top-color:var(--_four-color-active-indicator-one-color);border-right-color:var(--_four-color-active-indicator-one-color)}}"]))),_=function(e){function i(){return(0,d.A)(this,i),(0,s.A)(this,i,arguments)}return(0,c.A)(i,e),(0,n.A)(i)}(m);_.styles=[b],_=(0,l.__decorate)([(0,u.EM)("md-circular-progress")],_)}}]);
//# sourceMappingURL=76893.MQO6mHAtCP4.js.map