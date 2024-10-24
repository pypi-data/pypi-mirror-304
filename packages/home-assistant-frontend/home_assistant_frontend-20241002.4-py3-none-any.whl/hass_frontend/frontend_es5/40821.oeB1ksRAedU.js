"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[40821,13292],{13292:function(e,t,n){n.r(t);var i,a,r,s,o=n(14842),c=n(64599),l=n(35806),d=n(71008),h=n(62193),u=n(2816),p=n(27927),f=(n(81027),n(15112)),g=n(29818),m=n(85323),v=n(34897),y=(n(28066),n(88400),{info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"});(0,p.A)([(0,g.EM)("ha-alert")],(function(e,t){var n=function(t){function n(){var t;(0,d.A)(this,n);for(var i=arguments.length,a=new Array(i),r=0;r<i;r++)a[r]=arguments[r];return t=(0,h.A)(this,n,[].concat(a)),e(t),t}return(0,u.A)(n,t),(0,l.A)(n)}(t);return{F:n,d:[{kind:"field",decorators:[(0,g.MZ)()],key:"title",value:function(){return""}},{kind:"field",decorators:[(0,g.MZ)({attribute:"alert-type"})],key:"alertType",value:function(){return"info"}},{kind:"field",decorators:[(0,g.MZ)({type:Boolean})],key:"dismissable",value:function(){return!1}},{kind:"method",key:"render",value:function(){return(0,f.qy)(i||(i=(0,c.A)([' <div class="issue-type ','" role="alert"> <div class="icon ','"> <slot name="icon"> <ha-svg-icon .path="','"></ha-svg-icon> </slot> </div> <div class="content"> <div class="main-content"> ',' <slot></slot> </div> <div class="action"> <slot name="action"> '," </slot> </div> </div> </div> "])),(0,m.H)((0,o.A)({},this.alertType,!0)),this.title?"":"no-title",y[this.alertType],this.title?(0,f.qy)(a||(a=(0,c.A)(['<div class="title">',"</div>"])),this.title):"",this.dismissable?(0,f.qy)(r||(r=(0,c.A)(['<ha-icon-button @click="','" label="Dismiss alert" .path="','"></ha-icon-button>'])),this._dismiss_clicked,"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"):"")}},{kind:"method",key:"_dismiss_clicked",value:function(){(0,v.r)(this,"alert-dismissed-clicked")}},{kind:"field",static:!0,key:"styles",value:function(){return(0,f.AH)(s||(s=(0,c.A)(['.issue-type{position:relative;padding:8px;display:flex}.issue-type::after{position:absolute;top:0;right:0;bottom:0;left:0;opacity:.12;pointer-events:none;content:"";border-radius:4px}.icon{z-index:1}.icon.no-title{align-self:center}.content{display:flex;justify-content:space-between;align-items:center;width:100%;text-align:var(--float-start)}.action{z-index:1;width:min-content;--mdc-theme-primary:var(--primary-text-color)}.main-content{overflow-wrap:anywhere;word-break:break-word;margin-left:8px;margin-right:0;margin-inline-start:8px;margin-inline-end:0}.title{margin-top:2px;font-weight:700}.action ha-icon-button,.action mwc-button{--mdc-theme-primary:var(--primary-text-color);--mdc-icon-button-size:36px}.issue-type.info>.icon{color:var(--info-color)}.issue-type.info::after{background-color:var(--info-color)}.issue-type.warning>.icon{color:var(--warning-color)}.issue-type.warning::after{background-color:var(--warning-color)}.issue-type.error>.icon{color:var(--error-color)}.issue-type.error::after{background-color:var(--error-color)}.issue-type.success>.icon{color:var(--success-color)}.issue-type.success::after{background-color:var(--success-color)}:host ::slotted(ul){margin:0;padding-inline-start:20px}'])))}}]}}),f.WF)},77372:function(e,t,n){var i,a=n(64599),r=n(35806),s=n(71008),o=n(62193),c=n(2816),l=n(27927),d=(n(81027),n(54838)),h=n(15112),u=n(29818),p=n(49141);(0,l.A)([(0,u.EM)("ha-button")],(function(e,t){var n=function(t){function n(){var t;(0,s.A)(this,n);for(var i=arguments.length,a=new Array(i),r=0;r<i;r++)a[r]=arguments[r];return t=(0,o.A)(this,n,[].concat(a)),e(t),t}return(0,c.A)(n,t),(0,r.A)(n)}(t);return{F:n,d:[{kind:"field",static:!0,key:"styles",value:function(){return[p.R,(0,h.AH)(i||(i=(0,a.A)(["::slotted([slot=icon]){margin-inline-start:0px;margin-inline-end:8px;direction:var(--direction);display:block}.mdc-button{height:var(--button-height,36px)}.trailing-icon{display:flex}.slot-container{overflow:var(--button-slot-container-overflow,visible)}"])))]}}]}}),d.Button)},24284:function(e,t,n){var i,a,r=n(64599),s=n(35806),o=n(71008),c=n(62193),l=n(2816),d=n(27927),h=(n(81027),n(37136)),u=n(18881),p=n(15112),f=n(29818),g=n(85323),m=n(34897);(0,d.A)([(0,f.EM)("ha-formfield")],(function(e,t){var n=function(t){function n(){var t;(0,o.A)(this,n);for(var i=arguments.length,a=new Array(i),r=0;r<i;r++)a[r]=arguments[r];return t=(0,c.A)(this,n,[].concat(a)),e(t),t}return(0,l.A)(n,t),(0,s.A)(n)}(t);return{F:n,d:[{kind:"field",decorators:[(0,f.MZ)({type:Boolean,reflect:!0})],key:"disabled",value:function(){return!1}},{kind:"method",key:"render",value:function(){var e={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return(0,p.qy)(i||(i=(0,r.A)([' <div class="mdc-form-field ','"> <slot></slot> <label class="mdc-label" @click="','"> <slot name="label">',"</slot> </label> </div>"])),(0,g.H)(e),this._labelClick,this.label)}},{kind:"method",key:"_labelClick",value:function(){var e=this.input;if(e&&(e.focus(),!e.disabled))switch(e.tagName){case"HA-CHECKBOX":e.checked=!e.checked,(0,m.r)(e,"change");break;case"HA-RADIO":e.checked=!0,(0,m.r)(e,"change");break;default:e.click()}}},{kind:"field",static:!0,key:"styles",value:function(){return[u.R,(0,p.AH)(a||(a=(0,r.A)([":host(:not([alignEnd])) ::slotted(ha-switch){margin-right:10px;margin-inline-end:10px;margin-inline-start:inline}.mdc-form-field{align-items:var(--ha-formfield-align-items,center);gap:4px}.mdc-form-field>label{direction:var(--direction);margin-inline-start:0;margin-inline-end:auto;padding:0}:host([disabled]) label{color:var(--disabled-text-color)}"])))]}}]}}),h.M)},27120:function(e,t,n){var i,a,r=n(64599),s=n(35806),o=n(71008),c=n(62193),l=n(2816),d=n(27927),h=(n(81027),n(15112)),u=n(29818);(0,d.A)([(0,u.EM)("ha-label")],(function(e,t){var n=function(t){function n(){var t;(0,o.A)(this,n);for(var i=arguments.length,a=new Array(i),r=0;r<i;r++)a[r]=arguments[r];return t=(0,c.A)(this,n,[].concat(a)),e(t),t}return(0,l.A)(n,t),(0,s.A)(n)}(t);return{F:n,d:[{kind:"field",decorators:[(0,u.MZ)({type:Boolean,reflect:!0})],key:"dense",value:function(){return!1}},{kind:"method",key:"render",value:function(){return(0,h.qy)(i||(i=(0,r.A)([' <span class="content"> <slot name="icon"></slot> <slot></slot> </span> '])))}},{kind:"get",static:!0,key:"styles",value:function(){return[(0,h.AH)(a||(a=(0,r.A)([':host{--ha-label-text-color:var(--primary-text-color);--ha-label-icon-color:var(--primary-text-color);--ha-label-background-color:rgba(\n            var(--rgb-primary-text-color),\n            0.15\n          );--ha-label-background-opacity:1;position:relative;box-sizing:border-box;display:inline-flex;flex-direction:row;align-items:center;font-size:12px;font-weight:500;line-height:16px;letter-spacing:.1px;vertical-align:middle;height:32px;padding:0 16px;border-radius:18px;color:var(--ha-label-text-color);--mdc-icon-size:12px;text-wrap:nowrap}.content>*{position:relative;display:inline-flex;flex-direction:row;align-items:center}:host:before{position:absolute;content:"";inset:0;border-radius:inherit;background-color:var(--ha-label-background-color);opacity:var(--ha-label-background-opacity)}::slotted([slot=icon]){margin-right:8px;margin-left:-8px;margin-inline-start:-8px;margin-inline-end:8px;display:flex}span{display:inline-flex}:host([dense]){height:20px;padding:0 12px;border-radius:10px}:host([dense]) ::slotted([slot=icon]){margin-right:4px;margin-left:-4px;margin-inline-start:-4px;margin-inline-end:4px}'])))]}}]}}),h.WF)},24640:function(e,t,n){var i,a,r=n(64599),s=n(35806),o=n(71008),c=n(62193),l=n(2816),d=n(27927),h=(n(81027),n(15112)),u=n(29818);(0,d.A)([(0,u.EM)("ha-settings-row")],(function(e,t){var n=function(t){function n(){var t;(0,o.A)(this,n);for(var i=arguments.length,a=new Array(i),r=0;r<i;r++)a[r]=arguments[r];return t=(0,c.A)(this,n,[].concat(a)),e(t),t}return(0,l.A)(n,t),(0,s.A)(n)}(t);return{F:n,d:[{kind:"field",decorators:[(0,u.MZ)({type:Boolean,reflect:!0})],key:"narrow",value:function(){return!1}},{kind:"field",decorators:[(0,u.MZ)({type:Boolean,attribute:"three-line"})],key:"threeLine",value:function(){return!1}},{kind:"field",decorators:[(0,u.MZ)({type:Boolean,attribute:"wrap-heading",reflect:!0})],key:"wrapHeading",value:function(){return!1}},{kind:"method",key:"render",value:function(){return(0,h.qy)(i||(i=(0,r.A)([' <div class="prefix-wrap"> <slot name="prefix"></slot> <div class="body" ?two-line="','" ?three-line="','"> <slot name="heading"></slot> <div class="secondary"><slot name="description"></slot></div> </div> </div> <div class="content"><slot></slot></div> '])),!this.threeLine,this.threeLine)}},{kind:"get",static:!0,key:"styles",value:function(){return(0,h.AH)(a||(a=(0,r.A)([":host{display:flex;padding:0 16px;align-content:normal;align-self:auto;align-items:center}.body{padding-top:8px;padding-bottom:8px;padding-left:0;padding-inline-start:0;padding-right:16x;padding-inline-end:16px;overflow:hidden;display:var(--layout-vertical_-_display);flex-direction:var(--layout-vertical_-_flex-direction);justify-content:var(--layout-center-justified_-_justify-content);flex:var(--layout-flex_-_flex);flex-basis:var(--layout-flex_-_flex-basis)}.body[three-line]{min-height:var(--paper-item-body-three-line-min-height,88px)}:host(:not([wrap-heading])) body>*{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.body>.secondary{display:block;padding-top:4px;font-family:var(\n          --mdc-typography-body2-font-family,\n          var(--mdc-typography-font-family, Roboto, sans-serif)\n        );-webkit-font-smoothing:antialiased;font-size:var(--mdc-typography-body2-font-size, .875rem);font-weight:var(--mdc-typography-body2-font-weight,400);line-height:normal;color:var(--secondary-text-color)}.body[two-line]{min-height:calc(var(--paper-item-body-two-line-min-height,72px) - 16px);flex:1}.content{display:contents}:host(:not([narrow])) .content{display:var(--settings-row-content-display,flex);justify-content:flex-end;flex:1;padding:16px 0}.content ::slotted(*){width:var(--settings-row-content-width)}:host([narrow]){align-items:normal;flex-direction:column;border-top:1px solid var(--divider-color);padding-bottom:8px}::slotted(ha-switch){padding:16px 0}.secondary{white-space:normal}.prefix-wrap{display:var(--settings-row-prefix-display)}:host([narrow]) .prefix-wrap{display:flex;align-items:center}"])))}}]}}),h.WF)},59588:function(e,t,n){var i,a=n(64599),r=n(35806),s=n(71008),o=n(62193),c=n(2816),l=n(27927),d=n(35890),h=(n(81027),n(71204)),u=n(15031),p=n(15112),f=n(29818),g=n(39914);(0,l.A)([(0,f.EM)("ha-switch")],(function(e,t){var n=function(t){function n(){var t;(0,s.A)(this,n);for(var i=arguments.length,a=new Array(i),r=0;r<i;r++)a[r]=arguments[r];return t=(0,o.A)(this,n,[].concat(a)),e(t),t}return(0,c.A)(n,t),(0,r.A)(n)}(t);return{F:n,d:[{kind:"field",decorators:[(0,f.MZ)({type:Boolean})],key:"haptic",value:function(){return!1}},{kind:"method",key:"firstUpdated",value:function(){var e=this;(0,d.A)(n,"firstUpdated",this,3)([]),this.addEventListener("change",(function(){e.haptic&&(0,g.j)("light")}))}},{kind:"field",static:!0,key:"styles",value:function(){return[u.R,(0,p.AH)(i||(i=(0,a.A)([":host{--mdc-theme-secondary:var(--switch-checked-color)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:var(--switch-checked-button-color);border-color:var(--switch-checked-button-color)}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:var(--switch-checked-track-color);border-color:var(--switch-checked-track-color)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:var(--switch-unchecked-button-color);border-color:var(--switch-unchecked-button-color)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:var(--switch-unchecked-track-color);border-color:var(--switch-unchecked-track-color)}"])))]}}]}}),h.U)},94526:function(e,t,n){n.d(t,{Fy:function(){return o},Gk:function(){return d},Hg:function(){return r},Y_:function(){return h},ds:function(){return l},e0:function(){return s},ec:function(){return c}});var i=n(33994),a=n(22858),r=(n(88871),n(81027),n(82386),n(97741),n(50693),n(72735),n(26098),n(39790),n(66457),n(55228),n(36604),n(16891),"".concat(location.protocol,"//").concat(location.host),function(e){return e.map((function(e){if("string"!==e.type)return e;switch(e.name){case"username":return Object.assign(Object.assign({},e),{},{autocomplete:"username"});case"password":return Object.assign(Object.assign({},e),{},{autocomplete:"current-password"});case"code":return Object.assign(Object.assign({},e),{},{autocomplete:"one-time-code"});default:return e}}))}),s=function(e,t){return e.callWS({type:"auth/sign_path",path:t})},o=function(){var e=(0,a.A)((0,i.A)().mark((function e(t,n,a,r){return(0,i.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.abrupt("return",t.callWS({type:"config/auth_provider/homeassistant/create",user_id:n,username:a,password:r}));case 1:case"end":return e.stop()}}),e)})));return function(t,n,i,a){return e.apply(this,arguments)}}(),c=function(e,t,n){return e.callWS({type:"config/auth_provider/homeassistant/change_password",current_password:t,new_password:n})},l=function(e,t,n){return e.callWS({type:"config/auth_provider/homeassistant/admin_change_password",user_id:t,password:n})},d=function(e,t,n){return e.callWS({type:"config/auth_provider/homeassistant/admin_change_username",user_id:t,username:n})},h=function(e,t,n){return e.callWS({type:"auth/delete_all_refresh_tokens",token_type:t,delete_current_token:n})}},40821:function(e,t,n){n.r(t);var i,a,r,s,o,c,l,d,h,u,p,f=n(658),g=n(64599),m=n(33994),v=n(22858),y=n(35806),k=n(71008),_=n(62193),w=n(2816),b=n(27927),A=(n(81027),n(44124),n(82386),n(97741),n(50693),n(26098),n(39790),n(36604),n(79641),n(253),n(94438),n(16891),n(15112)),x=n(29818),M=(n(13292),n(77372),n(3276)),L=(n(24284),n(28066),n(27120),n(24640),n(88400),n(59588),n(90431),n(94526)),z=n(71443),H=n(6121),C=n(55321),O=n(50070),j="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z";(0,b.A)([(0,x.EM)("dialog-user-detail")],(function(e,t){var n,b,E,q,Z,F=function(t){function n(){var t;(0,k.A)(this,n);for(var i=arguments.length,a=new Array(i),r=0;r<i;r++)a[r]=arguments[r];return t=(0,_.A)(this,n,[].concat(a)),e(t),t}return(0,w.A)(n,t),(0,y.A)(n)}(t);return{F:F,d:[{kind:"field",decorators:[(0,x.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,x.wk)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,x.wk)()],key:"_isAdmin",value:void 0},{kind:"field",decorators:[(0,x.wk)()],key:"_localOnly",value:void 0},{kind:"field",decorators:[(0,x.wk)()],key:"_isActive",value:void 0},{kind:"field",decorators:[(0,x.wk)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,x.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,x.wk)()],key:"_submitting",value:function(){return!1}},{kind:"method",key:"showDialog",value:(Z=(0,v.A)((0,m.A)().mark((function e(t){return(0,m.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return this._params=t,this._error=void 0,this._name=t.entry.name||"",this._isAdmin=t.entry.group_ids.includes(z.wj),this._localOnly=t.entry.local_only,this._isActive=t.entry.is_active,e.next=8,this.updateComplete;case 8:case"end":return e.stop()}}),e,this)}))),function(e){return Z.apply(this,arguments)})},{kind:"method",key:"render",value:function(){var e,t,n;if(!this._params)return A.s6;var p=this._params.entry,m=(0,z.xg)(this.hass,p,!0);return(0,A.qy)(i||(i=(0,g.A)([' <ha-dialog open @closed="','" scrimClickAction escapeKeyAction .heading="','"> <div> ',' <div class="secondary"> ',": ","<br> </div> ",' <div class="form"> '," ",' <ha-settings-row> <span slot="heading"> ',' </span> <span slot="description"> ',' </span> <ha-switch .disabled="','" .checked="','" @change="','"> </ha-switch> </ha-settings-row> <ha-settings-row> <span slot="heading"> ',' </span> <span slot="description"> ',' </span> <ha-switch .disabled="','" .checked="','" @change="','"> </ha-switch> </ha-settings-row> <ha-settings-row> <span slot="heading"> ',' </span> <span slot="description"> ',' </span> <ha-switch .disabled="','" .checked="','" @change="','"> </ha-switch> </ha-settings-row> '," </div> ",' </div> <div slot="secondaryAction"> <ha-button class="warning" @click="','" .disabled="','"> ',' </ha-button> </div> <div slot="primaryAction"> <ha-button @click="','" .disabled="','"> '," </ha-button> </div> </ha-dialog> "])),this._close,(0,M.l)(this.hass,p.name),this._error?(0,A.qy)(a||(a=(0,g.A)(['<div class="error">',"</div>"])),this._error):A.s6,this.hass.localize("ui.panel.config.users.editor.id"),p.id,0===m.length?A.s6:(0,A.qy)(r||(r=(0,g.A)([' <div class="badge-container"> '," </div> "])),m.map((function(e){var t=(0,f.A)(e,2),n=t[0],i=t[1];return(0,A.qy)(s||(s=(0,g.A)([' <ha-label> <ha-svg-icon slot="icon" .path="','"></ha-svg-icon> '," </ha-label> "])),n,i)}))),p.system_generated?A.s6:(0,A.qy)(o||(o=(0,g.A)([' <ha-textfield dialogInitialFocus .value="','" @input="','" .label="','"></ha-textfield> <ha-settings-row> <span slot="heading"> ',' </span> <span slot="description">',"</span> "," </ha-settings-row> "])),this._name,this._nameChanged,this.hass.localize("ui.panel.config.users.editor.name"),this.hass.localize("ui.panel.config.users.editor.username"),p.username,null!==(e=this.hass.user)&&void 0!==e&&e.is_owner?(0,A.qy)(c||(c=(0,g.A)([' <ha-icon-button .path="','" @click="','" .label="','"> </ha-icon-button> '])),j,this._changeUsername,this.hass.localize("ui.panel.config.users.editor.change_username")):A.s6),!p.system_generated&&null!==(t=this.hass.user)&&void 0!==t&&t.is_owner?(0,A.qy)(l||(l=(0,g.A)([' <ha-settings-row> <span slot="heading"> ',' </span> <span slot="description">************</span> '," </ha-settings-row> "])),this.hass.localize("ui.panel.config.users.editor.password"),null!==(n=this.hass.user)&&void 0!==n&&n.is_owner?(0,A.qy)(d||(d=(0,g.A)([' <ha-icon-button .path="','" @click="','" .label="','"> </ha-icon-button> '])),j,this._changePassword,this.hass.localize("ui.panel.config.users.editor.change_password")):A.s6):A.s6,this.hass.localize("ui.panel.config.users.editor.active"),this.hass.localize("ui.panel.config.users.editor.active_description"),p.system_generated||p.is_owner,this._isActive,this._activeChanged,this.hass.localize("ui.panel.config.users.editor.local_access_only"),this.hass.localize("ui.panel.config.users.editor.local_access_only_description"),p.system_generated,this._localOnly,this._localOnlyChanged,this.hass.localize("ui.panel.config.users.editor.admin"),this.hass.localize("ui.panel.config.users.editor.admin_description"),p.system_generated||p.is_owner,this._isAdmin,this._adminChanged,this._isAdmin||p.system_generated?A.s6:(0,A.qy)(h||(h=(0,g.A)([' <ha-alert alert-type="info"> '," </ha-alert> "])),this.hass.localize("ui.panel.config.users.users_privileges_note")),p.system_generated?(0,A.qy)(u||(u=(0,g.A)([' <ha-alert alert-type="info"> '," </ha-alert> "])),this.hass.localize("ui.panel.config.users.editor.system_generated_read_only_users")):A.s6,this._deleteEntry,this._submitting||p.system_generated||p.is_owner,this.hass.localize("ui.panel.config.users.editor.delete_user"),this._updateEntry,!this._name||this._submitting||p.system_generated,this.hass.localize("ui.panel.config.users.editor.update_user"))}},{kind:"method",key:"_nameChanged",value:function(e){this._error=void 0,this._name=e.target.value}},{kind:"method",key:"_adminChanged",value:function(e){this._isAdmin=e.target.checked}},{kind:"method",key:"_localOnlyChanged",value:function(e){this._localOnly=e.target.checked}},{kind:"method",key:"_activeChanged",value:function(e){this._isActive=e.target.checked}},{kind:"method",key:"_updateEntry",value:(q=(0,v.A)((0,m.A)().mark((function e(){return(0,m.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return this._submitting=!0,e.prev=1,e.next=4,this._params.updateEntry({name:this._name.trim(),is_active:this._isActive,group_ids:[this._isAdmin?z.wj:z.eR],local_only:this._localOnly});case 4:this._close(),e.next=10;break;case 7:e.prev=7,e.t0=e.catch(1),this._error=(null===e.t0||void 0===e.t0?void 0:e.t0.message)||"Unknown error";case 10:return e.prev=10,this._submitting=!1,e.finish(10);case 13:case"end":return e.stop()}}),e,this,[[1,7,10,13]])}))),function(){return q.apply(this,arguments)})},{kind:"method",key:"_deleteEntry",value:(E=(0,v.A)((0,m.A)().mark((function e(){return(0,m.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return this._submitting=!0,e.prev=1,e.next=4,this._params.removeEntry();case 4:if(!e.sent){e.next=6;break}this._params=void 0;case 6:return e.prev=6,this._submitting=!1,e.finish(6);case 9:case"end":return e.stop()}}),e,this,[[1,,6,9]])}))),function(){return E.apply(this,arguments)})},{kind:"method",key:"_changeUsername",value:(b=(0,v.A)((0,m.A)().mark((function e(){var t,n;return(0,m.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(null===(t=this._params)||void 0===t?void 0:t.entry.credentials.find((function(e){return"homeassistant"===e.type}))){e.next=4;break}return(0,H.showAlertDialog)(this,{title:"No Home Assistant credentials found."}),e.abrupt("return");case 4:return e.next=6,(0,H.showPromptDialog)(this,{inputLabel:this.hass.localize("ui.panel.config.users.change_username.new_username"),confirmText:this.hass.localize("ui.panel.config.users.change_username.change"),title:this.hass.localize("ui.panel.config.users.change_username.caption"),defaultValue:this._params.entry.username});case 6:if(!(n=e.sent)){e.next=19;break}return e.prev=8,e.next=11,(0,L.Gk)(this.hass,this._params.entry.id,n);case 11:this._params=Object.assign(Object.assign({},this._params),{},{entry:Object.assign(Object.assign({},this._params.entry),{},{username:n})}),this._params.replaceEntry(this._params.entry),(0,H.showAlertDialog)(this,{text:this.hass.localize("ui.panel.config.users.change_username.username_changed")}),e.next=19;break;case 16:e.prev=16,e.t0=e.catch(8),(0,H.showAlertDialog)(this,{title:this.hass.localize("ui.panel.config.users.change_username.failed"),text:e.t0.message});case 19:case"end":return e.stop()}}),e,this,[[8,16]])}))),function(){return b.apply(this,arguments)})},{kind:"method",key:"_changePassword",value:(n=(0,v.A)((0,m.A)().mark((function e(){var t;return(0,m.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(null===(t=this._params)||void 0===t?void 0:t.entry.credentials.find((function(e){return"homeassistant"===e.type}))){e.next=4;break}return(0,H.showAlertDialog)(this,{title:"No Home Assistant credentials found."}),e.abrupt("return");case 4:(0,O.M)(this,{userId:this._params.entry.id});case 5:case"end":return e.stop()}}),e,this)}))),function(){return n.apply(this,arguments)})},{kind:"method",key:"_close",value:function(){this._params=void 0}},{kind:"get",static:!0,key:"styles",value:function(){return[C.nA,(0,A.AH)(p||(p=(0,g.A)(["ha-dialog{--mdc-dialog-max-width:500px}.form{padding-top:16px}.secondary{color:var(--secondary-text-color)}ha-textfield{display:block}.badge-container{margin-top:4px}.badge-container>*{margin-top:4px;margin-bottom:4px;margin-right:4px;margin-left:0;margin-inline-end:4px;margin-inline-start:0}ha-settings-row{padding:0}"])))]}}]}}),A.WF)},50070:function(e,t,n){n.d(t,{M:function(){return r}});n(95737),n(39790),n(66457),n(99019),n(96858);var i=n(34897),a=function(){return Promise.all([n.e(9421),n.e(31524)]).then(n.bind(n,16442))},r=function(e,t){(0,i.r)(e,"show-dialog",{dialogTag:"dialog-admin-change-password",dialogImport:a,dialogParams:t})}}}]);
//# sourceMappingURL=40821.oeB1ksRAedU.js.map