"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[12511,13292],{69678:function(t,e,n){n.d(e,{O:function(){return i},q:function(){return r}});var r=function(t,e,n){return Math.min(Math.max(t,e),n)},i=function(t,e,n){var r;return r=null!=e?Math.max(t,e):t,r=null!=n?Math.min(r,n):r}},57636:function(t,e,n){var r=n(22858).A,i=n(33994).A;n.a(t,function(){var t=r(i().mark((function t(r,a){var o,s,c,l,d,u,p,h,f,m,y,v,g,b,w,_,k,x,A,L;return i().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(t.prev=0,n.d(e,{Yf:function(){return k},ZQ:function(){return A},ZV:function(){return x},ty:function(){return _},x:function(){return w}}),o=n(13265),s=n(81027),c=n(82386),l=n(39805),d=n(29193),u=n(63030),p=n(49445),h=n(26098),f=n(39790),m=n(7760),y=n(36604),v=n(45269),g=n(53249),!(b=r([o])).then){t.next=33;break}return t.next=29,b;case 29:t.t1=t.sent,t.t0=(0,t.t1)(),t.next=34;break;case 33:t.t0=b;case 34:o=t.t0[0],w=function(t){return _(t.attributes)},_=function(t,e){return!!t.unit_of_measurement||!!t.state_class||(e||[]).includes(t.device_class||"")},k=function(t){switch(t.number_format){case v.jG.comma_decimal:return["en-US","en"];case v.jG.decimal_comma:return["de","es","it"];case v.jG.space_comma:return["fr","sv","cs"];case v.jG.system:return;default:return t.language}},x=function(t,e,n){var r=e?k(e):void 0;return Number.isNaN=Number.isNaN||function t(e){return"number"==typeof e&&t(e)},(null==e?void 0:e.number_format)===v.jG.none||Number.isNaN(Number(t))?Number.isNaN(Number(t))||""===t||(null==e?void 0:e.number_format)!==v.jG.none?"string"==typeof t?t:"".concat((0,g.L)(t,null==n?void 0:n.maximumFractionDigits).toString()).concat("currency"===(null==n?void 0:n.style)?" ".concat(n.currency):""):new Intl.NumberFormat("en-US",L(t,Object.assign(Object.assign({},n),{},{useGrouping:!1}))).format(Number(t)):new Intl.NumberFormat(r,L(t,n)).format(Number(t))},A=function(t,e){var n,r=null==e?void 0:e.display_precision;return null!=r?{maximumFractionDigits:r,minimumFractionDigits:r}:Number.isInteger(Number(null==t||null===(n=t.attributes)||void 0===n?void 0:n.step))&&Number.isInteger(Number(null==t?void 0:t.state))?{maximumFractionDigits:0}:void 0},L=function(t,e){var n=Object.assign({maximumFractionDigits:2},e);if("string"!=typeof t)return n;if(!e||void 0===e.minimumFractionDigits&&void 0===e.maximumFractionDigits){var r=t.indexOf(".")>-1?t.split(".")[1].length:0;n.minimumFractionDigits=r,n.maximumFractionDigits=r}return n},a(),t.next=47;break;case 44:t.prev=44,t.t2=t.catch(0),a(t.t2);case 47:case"end":return t.stop()}}),t,null,[[0,44]])})));return function(e,n){return t.apply(this,arguments)}}())},53249:function(t,e,n){n.d(e,{L:function(){return r}});var r=function(t){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:2;return Math.round(t*Math.pow(10,e))/Math.pow(10,e)}},68690:function(t,e,n){var r,i,a,o,s,c,l=n(64599),d=n(35806),u=n(71008),p=n(62193),h=n(2816),f=n(27927),m=(n(81027),n(54838),n(15112)),y=n(29818);n(37629),n(88400),(0,f.A)([(0,y.EM)("ha-progress-button")],(function(t,e){var n=function(e){function n(){var e;(0,u.A)(this,n);for(var r=arguments.length,i=new Array(r),a=0;a<r;a++)i[a]=arguments[a];return e=(0,p.A)(this,n,[].concat(i)),t(e),e}return(0,h.A)(n,e),(0,d.A)(n)}(e);return{F:n,d:[{kind:"field",decorators:[(0,y.MZ)({type:Boolean})],key:"disabled",value:function(){return!1}},{kind:"field",decorators:[(0,y.MZ)({type:Boolean})],key:"progress",value:function(){return!1}},{kind:"field",decorators:[(0,y.MZ)({type:Boolean})],key:"raised",value:function(){return!1}},{kind:"field",decorators:[(0,y.wk)()],key:"_result",value:void 0},{kind:"method",key:"render",value:function(){var t=this._result||this.progress;return(0,m.qy)(r||(r=(0,l.A)([' <mwc-button ?raised="','" .disabled="','" @click="','" class="','"> <slot></slot> </mwc-button> '," "])),this.raised,this.disabled||this.progress,this._buttonTapped,this._result||"",t?(0,m.qy)(i||(i=(0,l.A)([' <div class="progress"> '," </div> "])),"success"===this._result?(0,m.qy)(a||(a=(0,l.A)(['<ha-svg-icon .path="','"></ha-svg-icon>'])),"M9,20.42L2.79,14.21L5.62,11.38L9,14.77L18.88,4.88L21.71,7.71L9,20.42Z"):"error"===this._result?(0,m.qy)(o||(o=(0,l.A)(['<ha-svg-icon .path="','"></ha-svg-icon>'])),"M2.2,16.06L3.88,12L2.2,7.94L6.26,6.26L7.94,2.2L12,3.88L16.06,2.2L17.74,6.26L21.8,7.94L20.12,12L21.8,16.06L17.74,17.74L16.06,21.8L12,20.12L7.94,21.8L6.26,17.74L2.2,16.06M13,17V15H11V17H13M13,13V7H11V13H13Z"):this.progress?(0,m.qy)(s||(s=(0,l.A)([' <ha-circular-progress size="small" indeterminate></ha-circular-progress> ']))):""):m.s6)}},{kind:"method",key:"actionSuccess",value:function(){this._setResult("success")}},{kind:"method",key:"actionError",value:function(){this._setResult("error")}},{kind:"method",key:"_setResult",value:function(t){var e=this;this._result=t,setTimeout((function(){e._result=void 0}),2e3)}},{kind:"method",key:"_buttonTapped",value:function(t){this.progress&&t.stopPropagation()}},{kind:"get",static:!0,key:"styles",value:function(){return(0,m.AH)(c||(c=(0,l.A)([":host{outline:0;display:inline-block;position:relative}mwc-button{transition:all 1s}mwc-button.success{--mdc-theme-primary:white;background-color:var(--success-color);transition:none;border-radius:4px;pointer-events:none}mwc-button[raised].success{--mdc-theme-primary:var(--success-color);--mdc-theme-on-primary:white}mwc-button.error{--mdc-theme-primary:white;background-color:var(--error-color);transition:none;border-radius:4px;pointer-events:none}mwc-button[raised].error{--mdc-theme-primary:var(--error-color);--mdc-theme-on-primary:white}.progress{bottom:4px;position:absolute;text-align:center;top:4px;width:100%}ha-svg-icon{color:#fff}mwc-button.error slot,mwc-button.success slot{visibility:hidden}"])))}}]}}),m.WF)},13292:function(t,e,n){n.r(e);var r,i,a,o,s=n(14842),c=n(64599),l=n(35806),d=n(71008),u=n(62193),p=n(2816),h=n(27927),f=(n(81027),n(15112)),m=n(29818),y=n(85323),v=n(34897),g=(n(28066),n(88400),{info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"});(0,h.A)([(0,m.EM)("ha-alert")],(function(t,e){var n=function(e){function n(){var e;(0,d.A)(this,n);for(var r=arguments.length,i=new Array(r),a=0;a<r;a++)i[a]=arguments[a];return e=(0,u.A)(this,n,[].concat(i)),t(e),e}return(0,p.A)(n,e),(0,l.A)(n)}(e);return{F:n,d:[{kind:"field",decorators:[(0,m.MZ)()],key:"title",value:function(){return""}},{kind:"field",decorators:[(0,m.MZ)({attribute:"alert-type"})],key:"alertType",value:function(){return"info"}},{kind:"field",decorators:[(0,m.MZ)({type:Boolean})],key:"dismissable",value:function(){return!1}},{kind:"method",key:"render",value:function(){return(0,f.qy)(r||(r=(0,c.A)([' <div class="issue-type ','" role="alert"> <div class="icon ','"> <slot name="icon"> <ha-svg-icon .path="','"></ha-svg-icon> </slot> </div> <div class="content"> <div class="main-content"> ',' <slot></slot> </div> <div class="action"> <slot name="action"> '," </slot> </div> </div> </div> "])),(0,y.H)((0,s.A)({},this.alertType,!0)),this.title?"":"no-title",g[this.alertType],this.title?(0,f.qy)(i||(i=(0,c.A)(['<div class="title">',"</div>"])),this.title):"",this.dismissable?(0,f.qy)(a||(a=(0,c.A)(['<ha-icon-button @click="','" label="Dismiss alert" .path="','"></ha-icon-button>'])),this._dismiss_clicked,"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"):"")}},{kind:"method",key:"_dismiss_clicked",value:function(){(0,v.r)(this,"alert-dismissed-clicked")}},{kind:"field",static:!0,key:"styles",value:function(){return(0,f.AH)(o||(o=(0,c.A)(['.issue-type{position:relative;padding:8px;display:flex}.issue-type::after{position:absolute;top:0;right:0;bottom:0;left:0;opacity:.12;pointer-events:none;content:"";border-radius:4px}.icon{z-index:1}.icon.no-title{align-self:center}.content{display:flex;justify-content:space-between;align-items:center;width:100%;text-align:var(--float-start)}.action{z-index:1;width:min-content;--mdc-theme-primary:var(--primary-text-color)}.main-content{overflow-wrap:anywhere;word-break:break-word;margin-left:8px;margin-right:0;margin-inline-start:8px;margin-inline-end:0}.title{margin-top:2px;font-weight:700}.action ha-icon-button,.action mwc-button{--mdc-theme-primary:var(--primary-text-color);--mdc-icon-button-size:36px}.issue-type.info>.icon{color:var(--info-color)}.issue-type.info::after{background-color:var(--info-color)}.issue-type.warning>.icon{color:var(--warning-color)}.issue-type.warning::after{background-color:var(--warning-color)}.issue-type.error>.icon{color:var(--error-color)}.issue-type.error::after{background-color:var(--error-color)}.issue-type.success>.icon{color:var(--success-color)}.issue-type.success::after{background-color:var(--success-color)}:host ::slotted(ul){margin:0;padding-inline-start:20px}'])))}}]}}),f.WF)},37629:function(t,e,n){n.r(e),n.d(e,{HaCircularProgress:function(){return m}});var r,i=n(64599),a=n(41981),o=n(35806),s=n(71008),c=n(62193),l=n(2816),d=n(27927),u=n(35890),p=(n(81027),n(99322)),h=n(15112),f=n(29818),m=(0,d.A)([(0,f.EM)("ha-circular-progress")],(function(t,e){var n=function(e){function n(){var e;(0,s.A)(this,n);for(var r=arguments.length,i=new Array(r),a=0;a<r;a++)i[a]=arguments[a];return e=(0,c.A)(this,n,[].concat(i)),t(e),e}return(0,l.A)(n,e),(0,o.A)(n)}(e);return{F:n,d:[{kind:"field",decorators:[(0,f.MZ)({attribute:"aria-label",type:String})],key:"ariaLabel",value:function(){return"Loading"}},{kind:"field",decorators:[(0,f.MZ)()],key:"size",value:function(){return"medium"}},{kind:"method",key:"updated",value:function(t){if((0,u.A)(n,"updated",this,3)([t]),t.has("size"))switch(this.size){case"tiny":this.style.setProperty("--md-circular-progress-size","16px");break;case"small":this.style.setProperty("--md-circular-progress-size","28px");break;case"medium":this.style.setProperty("--md-circular-progress-size","48px");break;case"large":this.style.setProperty("--md-circular-progress-size","68px")}}},{kind:"field",static:!0,key:"styles",value:function(){return[].concat((0,a.A)((0,u.A)(n,"styles",this)),[(0,h.AH)(r||(r=(0,i.A)([":host{--md-sys-color-primary:var(--primary-color);--md-circular-progress-size:48px}"])))])}}]}}),p.U)},26207:function(t,e,n){var r,i,a,o,s=n(64599),c=n(35806),l=n(71008),d=n(62193),u=n(2816),p=n(27927),h=n(35890),f=(n(81027),n(15112)),m=n(29818),y=n(13830);(0,p.A)([(0,m.EM)("ha-clickable-list-item")],(function(t,e){var n=function(e){function n(){var e;(0,l.A)(this,n);for(var r=arguments.length,i=new Array(r),a=0;a<r;a++)i[a]=arguments[a];return e=(0,d.A)(this,n,[].concat(i)),t(e),e}return(0,u.A)(n,e),(0,c.A)(n)}(e);return{F:n,d:[{kind:"field",decorators:[(0,m.MZ)()],key:"href",value:void 0},{kind:"field",decorators:[(0,m.MZ)({type:Boolean})],key:"disableHref",value:function(){return!1}},{kind:"field",decorators:[(0,m.MZ)({type:Boolean,reflect:!0})],key:"openNewTab",value:function(){return!1}},{kind:"field",decorators:[(0,m.P)("a")],key:"_anchor",value:void 0},{kind:"method",key:"render",value:function(){var t=(0,h.A)(n,"render",this,3)([]),e=this.href||"";return(0,f.qy)(r||(r=(0,s.A)(["",""])),this.disableHref?(0,f.qy)(i||(i=(0,s.A)(["<a>","</a>"])),t):(0,f.qy)(a||(a=(0,s.A)(['<a target="','" href="','">',"</a>"])),this.openNewTab?"_blank":"",e,t))}},{kind:"method",key:"firstUpdated",value:function(){var t=this;(0,h.A)(n,"firstUpdated",this,3)([]),this.addEventListener("keydown",(function(e){"Enter"!==e.key&&" "!==e.key||t._anchor.click()}))}},{kind:"get",static:!0,key:"styles",value:function(){return[(0,h.A)(n,"styles",this),(0,f.AH)(o||(o=(0,s.A)(["a{width:100%;height:100%;display:flex;align-items:center;overflow:hidden}"])))]}}]}}),y.$)},24640:function(t,e,n){var r,i,a=n(64599),o=n(35806),s=n(71008),c=n(62193),l=n(2816),d=n(27927),u=(n(81027),n(15112)),p=n(29818);(0,d.A)([(0,p.EM)("ha-settings-row")],(function(t,e){var n=function(e){function n(){var e;(0,s.A)(this,n);for(var r=arguments.length,i=new Array(r),a=0;a<r;a++)i[a]=arguments[a];return e=(0,c.A)(this,n,[].concat(i)),t(e),e}return(0,l.A)(n,e),(0,o.A)(n)}(e);return{F:n,d:[{kind:"field",decorators:[(0,p.MZ)({type:Boolean,reflect:!0})],key:"narrow",value:function(){return!1}},{kind:"field",decorators:[(0,p.MZ)({type:Boolean,attribute:"three-line"})],key:"threeLine",value:function(){return!1}},{kind:"field",decorators:[(0,p.MZ)({type:Boolean,attribute:"wrap-heading",reflect:!0})],key:"wrapHeading",value:function(){return!1}},{kind:"method",key:"render",value:function(){return(0,u.qy)(r||(r=(0,a.A)([' <div class="prefix-wrap"> <slot name="prefix"></slot> <div class="body" ?two-line="','" ?three-line="','"> <slot name="heading"></slot> <div class="secondary"><slot name="description"></slot></div> </div> </div> <div class="content"><slot></slot></div> '])),!this.threeLine,this.threeLine)}},{kind:"get",static:!0,key:"styles",value:function(){return(0,u.AH)(i||(i=(0,a.A)([":host{display:flex;padding:0 16px;align-content:normal;align-self:auto;align-items:center}.body{padding-top:8px;padding-bottom:8px;padding-left:0;padding-inline-start:0;padding-right:16x;padding-inline-end:16px;overflow:hidden;display:var(--layout-vertical_-_display);flex-direction:var(--layout-vertical_-_flex-direction);justify-content:var(--layout-center-justified_-_justify-content);flex:var(--layout-flex_-_flex);flex-basis:var(--layout-flex_-_flex-basis)}.body[three-line]{min-height:var(--paper-item-body-three-line-min-height,88px)}:host(:not([wrap-heading])) body>*{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.body>.secondary{display:block;padding-top:4px;font-family:var(\n          --mdc-typography-body2-font-family,\n          var(--mdc-typography-font-family, Roboto, sans-serif)\n        );-webkit-font-smoothing:antialiased;font-size:var(--mdc-typography-body2-font-size, .875rem);font-weight:var(--mdc-typography-body2-font-weight,400);line-height:normal;color:var(--secondary-text-color)}.body[two-line]{min-height:calc(var(--paper-item-body-two-line-min-height,72px) - 16px);flex:1}.content{display:contents}:host(:not([narrow])) .content{display:var(--settings-row-content-display,flex);justify-content:flex-end;flex:1;padding:16px 0}.content ::slotted(*){width:var(--settings-row-content-width)}:host([narrow]){align-items:normal;flex-direction:column;border-top:1px solid var(--divider-color);padding-bottom:8px}::slotted(ha-switch){padding:16px 0}.secondary{white-space:normal}.prefix-wrap{display:var(--settings-row-prefix-display)}:host([narrow]) .prefix-wrap{display:flex;align-items:center}"])))}}]}}),u.WF)},31265:function(t,e,n){n.d(e,{JW:function(){return f},TC:function(){return o},VN:function(){return s},Vx:function(){return c},XQ:function(){return p},eM:function(){return d},iH:function(){return l},k3:function(){return h},m4:function(){return i},qf:function(){return a},yv:function(){return u}});var r=n(41981),i=(n(81027),n(13025),n(44124),n(26098),n(39790),n(253),n(2075),n(94438),["migration_error","setup_error","setup_retry"]),a=["not_loaded","loaded","setup_error","setup_retry"],o=function(t,e,n){var r={type:"config_entries/subscribe"};return n&&n.type&&(r.type_filter=n.type),t.connection.subscribeMessage((function(t){return e(t)}),r)},s=function(t,e){var n={};return e&&(e.type&&(n.type_filter=e.type),e.domain&&(n.domain=e.domain)),t.callWS(Object.assign({type:"config_entries/get"},n))},c=function(t,e){return t.callWS({type:"config_entries/get_single",entry_id:e})},l=function(t,e,n){return t.callWS(Object.assign({type:"config_entries/update",entry_id:e},n))},d=function(t,e){return t.callApi("DELETE","config/config_entries/entry/".concat(e))},u=function(t,e){return t.callApi("POST","config/config_entries/entry/".concat(e,"/reload"))},p=function(t,e){return t.callWS({type:"config_entries/disable",entry_id:e,disabled_by:"user"})},h=function(t,e){return t.callWS({type:"config_entries/disable",entry_id:e,disabled_by:null})},f=function(t,e){if(!e)return t;var n=t.find((function(t){return t.entry_id===e}));if(!n)return t;var i=t.filter((function(t){return t.entry_id!==e}));return[n].concat((0,r.A)(i))}},70747:function(t,e,n){n.d(e,{HH:function(){return r},TY:function(){return i},lu:function(){return a},mu:function(){return o}});var r=function(t,e){var n;return t.callApi("POST","config/config_entries/options/flow",{handler:e,show_advanced_options:Boolean(null===(n=t.userData)||void 0===n?void 0:n.showAdvanced)})},i=function(t,e){return t.callApi("GET","config/config_entries/options/flow/".concat(e))},a=function(t,e,n){return t.callApi("POST","config/config_entries/options/flow/".concat(e),n)},o=function(t,e){return t.callApi("DELETE","config/config_entries/options/flow/".concat(e))}},98736:function(t,e,n){n.d(e,{$:function(){return r}});var r=function(t){return t.callWS({type:"usb/scan"})}},41572:function(t,e,n){n.d(e,{g:function(){return a}});n(95737),n(26098),n(39790),n(66457),n(99019),n(96858);var r=n(34897),i=function(){return Promise.all([n.e(94131),n.e(14121),n.e(33810),n.e(92106),n.e(10963),n.e(40319),n.e(7726),n.e(7986),n.e(89059),n.e(21689),n.e(55792),n.e(9421),n.e(25756),n.e(83319)]).then(n.bind(n,93608))},a=function(t,e,n){(0,r.r)(t,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:i,dialogParams:Object.assign(Object.assign({},e),{},{flowConfig:n,dialogParentElement:t})})}},22619:function(t,e,n){n.d(e,{Q:function(){return v}});var r,i,a,o,s,c,l=n(64599),d=n(33994),u=n(658),p=n(22858),h=(n(81027),n(95737),n(50693),n(26098),n(39790),n(66457),n(99019),n(96858),n(15112)),f=n(46092),m=n(70747),y=n(41572),v=function(t,e,n){return(0,y.g)(t,Object.assign({startFlowHandler:e.entry_id,domain:e.domain},n),{flowType:"options_flow",showDevices:!1,createFlow:(g=(0,p.A)((0,d.A)().mark((function t(n,r){var i,a,o;return(0,d.A)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,Promise.all([(0,m.HH)(n,r),n.loadFragmentTranslation("config"),n.loadBackendTranslation("options",e.domain),n.loadBackendTranslation("selector",e.domain)]);case 2:return i=t.sent,a=(0,u.A)(i,1),o=a[0],t.abrupt("return",o);case 6:case"end":return t.stop()}}),t)}))),function(t,e){return g.apply(this,arguments)}),fetchFlow:(v=(0,p.A)((0,d.A)().mark((function t(n,r){var i,a,o;return(0,d.A)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,Promise.all([(0,m.TY)(n,r),n.loadFragmentTranslation("config"),n.loadBackendTranslation("options",e.domain),n.loadBackendTranslation("selector",e.domain)]);case 2:return i=t.sent,a=(0,u.A)(i,1),o=a[0],t.abrupt("return",o);case 6:case"end":return t.stop()}}),t)}))),function(t,e){return v.apply(this,arguments)}),handleFlowStep:m.lu,deleteFlow:m.mu,renderAbortDescription:function(t,n){var i=t.localize("component.".concat(n.translation_domain||e.domain,".options.abort.").concat(n.reason),n.description_placeholders);return i?(0,h.qy)(r||(r=(0,l.A)([' <ha-markdown breaks allowsvg .content="','"></ha-markdown> '])),i):n.reason},renderShowFormStepHeader:function(t,n){return t.localize("component.".concat(n.translation_domain||e.domain,".options.step.").concat(n.step_id,".title"),n.description_placeholders)||t.localize("ui.dialogs.options_flow.form.header")},renderShowFormStepDescription:function(t,n){var r=t.localize("component.".concat(n.translation_domain||e.domain,".options.step.").concat(n.step_id,".description"),n.description_placeholders);return r?(0,h.qy)(i||(i=(0,l.A)([' <ha-markdown allowsvg breaks .content="','"></ha-markdown> '])),r):""},renderShowFormStepFieldLabel:function(t,n,r,i){var a;if("expandable"===r.type)return t.localize("component.".concat(e.domain,".options.step.").concat(n.step_id,".sections.").concat(r.name,".name"));var o=null!=i&&null!==(a=i.path)&&void 0!==a&&a[0]?"sections.".concat(i.path[0],"."):"";return t.localize("component.".concat(e.domain,".options.step.").concat(n.step_id,".").concat(o,"data.").concat(r.name))||r.name},renderShowFormStepFieldHelper:function(t,n,r,i){var o;if("expandable"===r.type)return t.localize("component.".concat(n.translation_domain||e.domain,".options.step.").concat(n.step_id,".sections.").concat(r.name,".description"));var s=null!=i&&null!==(o=i.path)&&void 0!==o&&o[0]?"sections.".concat(i.path[0],"."):"",c=t.localize("component.".concat(n.translation_domain||e.domain,".options.step.").concat(n.step_id,".").concat(s,"data_description.").concat(r.name),n.description_placeholders);return c?(0,h.qy)(a||(a=(0,l.A)(['<ha-markdown breaks .content="','"></ha-markdown>'])),c):""},renderShowFormStepFieldError:function(t,n,r){return t.localize("component.".concat(n.translation_domain||e.domain,".options.error.").concat(r),n.description_placeholders)||r},renderShowFormStepFieldLocalizeValue:function(t,n,r){return t.localize("component.".concat(e.domain,".selector.").concat(r))},renderShowFormStepSubmitButton:function(t,n){return t.localize("component.".concat(e.domain,".options.step.").concat(n.step_id,".submit"))||t.localize("ui.panel.config.integrations.config_flow.".concat(!1===n.last_step?"next":"submit"))},renderExternalStepHeader:function(t,e){return""},renderExternalStepDescription:function(t,e){return""},renderCreateEntryDescription:function(t,e){return(0,h.qy)(o||(o=(0,l.A)([" <p>","</p> "])),t.localize("ui.dialogs.options_flow.success.description"))},renderShowFormProgressHeader:function(t,n){return t.localize("component.".concat(e.domain,".options.step.").concat(n.step_id,".title"))||t.localize("component.".concat(e.domain,".title"))},renderShowFormProgressDescription:function(t,n){var r=t.localize("component.".concat(n.translation_domain||e.domain,".options.progress.").concat(n.progress_action),n.description_placeholders);return r?(0,h.qy)(s||(s=(0,l.A)([' <ha-markdown allowsvg breaks .content="','"></ha-markdown> '])),r):""},renderMenuHeader:function(t,n){return t.localize("component.".concat(e.domain,".options.step.").concat(n.step_id,".title"))||t.localize("component.".concat(e.domain,".title"))},renderMenuDescription:function(t,n){var r=t.localize("component.".concat(n.translation_domain||e.domain,".options.step.").concat(n.step_id,".description"),n.description_placeholders);return r?(0,h.qy)(c||(c=(0,l.A)([' <ha-markdown allowsvg breaks .content="','"></ha-markdown> '])),r):""},renderMenuOption:function(t,n,r){return t.localize("component.".concat(n.translation_domain||e.domain,".options.step.").concat(n.step_id,".menu_options.").concat(r),n.description_placeholders)},renderLoadingDescription:function(t,n){return t.localize("component.".concat(e.domain,".options.loading"))||("loading_flow"===n||"loading_step"===n?t.localize("ui.dialogs.options_flow.loading.".concat(n),{integration:(0,f.p$)(t.localize,e.domain)}):"")}});var v,g}},30838:function(t,e,n){var r=n(22858).A,i=n(33994).A;n.a(t,function(){var t=r(i().mark((function t(r,a){var o,s,c,l,d,u,p,h,f,m,y,v,g,b,w,_,k,x,A,L,z,M,S,F,E,H,D,T,q,O,j,N,Z,V,P,B,C,W,R,I,G,U,Q,Y,$,J,X,K,tt,et,nt,rt,it,at,ot,st,ct,lt,dt,ut,pt,ht;return i().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(t.prev=0,n.r(e),o=n(33994),s=n(22858),c=n(64599),l=n(64782),d=n(41981),u=n(35806),p=n(71008),h=n(62193),f=n(2816),m=n(27927),y=n(35890),v=n(81027),g=n(13025),b=n(44124),w=n(97741),_=n(89655),k=n(50693),x=n(26098),A=n(39790),L=n(9241),z=n(253),M=n(2075),S=n(94438),F=n(54846),E=n(16891),H=n(4525),D=n(66555),n(63893),n(67056),T=n(15112),q=n(29818),O=n(33922),j=n(57636),N=n(53249),Z=n(33984),n(68690),n(90701),n(13292),n(13082),n(26207),n(28066),n(46163),n(24640),V=n(31265),P=n(760),B=n(37266),C=n(98736),W=n(22619),R=n(86997),n(77980),I=n(20712),G=n(83102),U=n(55321),Q=n(51842),Y=n(42276),!($=r([j])).then){t.next=81;break}return t.next=77,$;case 77:t.t1=t.sent,t.t0=(0,t.t1)(),t.next=82;break;case 81:t.t0=$;case 82:j=t.t0[0],ht={fill:"origin",borderColor:G.hx,backgroundColor:G.hx+"2B",pointRadius:0,lineTension:.2,borderWidth:1},(0,m.A)([(0,q.EM)("ha-config-hardware")],(function(t,e){var n,r,i,a,m=function(e){function n(){var e;(0,p.A)(this,n);for(var r=arguments.length,i=new Array(r),a=0;a<r;a++)i[a]=arguments[a];return e=(0,h.A)(this,n,[].concat(i)),t(e),e}return(0,f.A)(n,e),(0,u.A)(n)}(e);return{F:m,d:[{kind:"field",decorators:[(0,q.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,q.MZ)({type:Boolean})],key:"narrow",value:function(){return!1}},{kind:"field",decorators:[(0,q.wk)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,q.wk)()],key:"_OSData",value:void 0},{kind:"field",decorators:[(0,q.wk)()],key:"_hardwareInfo",value:void 0},{kind:"field",decorators:[(0,q.wk)()],key:"_chartOptions",value:void 0},{kind:"field",decorators:[(0,q.wk)()],key:"_systemStatusData",value:void 0},{kind:"field",decorators:[(0,q.wk)()],key:"_configEntries",value:void 0},{kind:"field",key:"_memoryEntries",value:function(){return[]}},{kind:"field",key:"_cpuEntries",value:function(){return[]}},{kind:"method",key:"hassSubscribe",value:function(){var t=this,e=[(0,V.TC)(this.hass,(function(e){var n=!1,r=[];if(e.forEach((function(e){if(null===e.type||"added"===e.type)r.push(e.entry),null===e.type&&(n=!0);else if("removed"===e.type)t._configEntries&&delete t._configEntries[e.entry.entry_id];else if("updated"===e.type&&t._configEntries){var i=e.entry;t._configEntries[e.entry.entry_id]=i}})),r.length||n){var i,a=[].concat((0,d.A)(n?[]:Object.values(t._configEntries||{})),r),o={},s=(0,l.A)(a);try{for(s.s();!(i=s.n()).done;){var c=i.value;o[c.entry_id]=c}}catch(u){s.e(u)}finally{s.f()}t._configEntries=o}}),{type:["hardware"]})];return(0,O.x)(this.hass,"hardware")&&e.push(this.hass.connection.subscribeMessage((function(e){t._memoryEntries.shift(),t._cpuEntries.shift(),t._memoryEntries.push({x:new Date(e.timestamp).getTime(),y:e.memory_used_percent}),t._cpuEntries.push({x:new Date(e.timestamp).getTime(),y:e.cpu_percent}),t._systemStatusData=e}),{type:"hardware/subscribe_system_status"})),e}},{kind:"method",key:"willUpdate",value:function(){var t=this;this.hasUpdated||(this._chartOptions={animation:!1,responsive:!0,scales:{y:{gridLines:{drawTicks:!1},ticks:{maxTicksLimit:7,fontSize:10,max:100,min:0,stepSize:1,callback:function(e){return e+(0,Z.d)(t.hass.locale)+"%"}}},x:{type:"time",adapters:{date:{locale:this.hass.locale,config:this.hass.config}},gridLines:{display:!0,drawTicks:!1},ticks:{maxRotation:0,sampleSize:5,autoSkipPadding:20,major:{enabled:!0},fontSize:10,autoSkip:!0,maxTicksLimit:5}}},locale:(0,j.Yf)(this.hass.locale)})}},{kind:"method",key:"firstUpdated",value:function(t){(0,y.A)(m,"firstUpdated",this,3)([t]),this._load();for(var e=new Date,n=0;n<60;n++){var r=new Date(e);r.setSeconds(r.getSeconds()-5*(60-n)),this._memoryEntries.push({x:r.getTime(),y:null}),this._cpuEntries.push({x:r.getTime(),y:null})}}},{kind:"method",key:"render",value:function(){var t,e,n,r,i,a,o,s,l=this,d=[],u=null===(t=this._hardwareInfo)||void 0===t?void 0:t.hardware.find((function(t){return null!==t.board})),p=null===(e=this._hardwareInfo)||void 0===e?void 0:e.hardware.filter((function(t){return null!==t.dongle&&(!t.config_entries.length||t.config_entries.some((function(t){var e;return(null===(e=l._configEntries)||void 0===e?void 0:e[t])&&!l._configEntries[t].disabled_by})))}));u?(d=u.config_entries.map((function(t){var e;return null===(e=l._configEntries)||void 0===e?void 0:e[t]})).filter((function(t){return(null==t?void 0:t.supports_options)&&!t.disabled_by})),r=u.board.hassio_board_id,i=u.name,o=u.url,a=(0,Q.QR)({category:"boards",manufacturer:u.board.manufacturer,model:u.board.model,darkOptimized:null===(s=this.hass.themes)||void 0===s?void 0:s.darkMode})):null!==(n=this._OSData)&&void 0!==n&&n.board&&(r=this._OSData.board,i=P.S[this._OSData.board]);return(0,T.qy)(J||(J=(0,c.A)([' <hass-subpage back-path="/config/system" .hass="','" .narrow="','" .header="','"> '," ",' <div class="content"> '," "," "," </div> </hass-subpage> "])),this.hass,this.narrow,this.hass.localize("ui.panel.config.hardware.caption"),(0,O.x)(this.hass,"hassio")?(0,T.qy)(X||(X=(0,c.A)([' <ha-icon-button slot="toolbar-icon" .path="','" .label="','" @click="','"></ha-icon-button> '])),"M16.56,5.44L15.11,6.89C16.84,7.94 18,9.83 18,12A6,6 0 0,1 12,18A6,6 0 0,1 6,12C6,9.83 7.16,7.94 8.88,6.88L7.44,5.44C5.36,6.88 4,9.28 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12C20,9.28 18.64,6.88 16.56,5.44M13,3H11V13H13",this.hass.localize("ui.panel.config.hardware.restart_homeassistant"),this._showRestartDialog):"",this._error?(0,T.qy)(K||(K=(0,c.A)([' <ha-alert alert-type="error">',"</ha-alert> "])),this._error.message||this._error.code):"",i||(0,O.x)(this.hass,"hassio")?(0,T.qy)(tt||(tt=(0,c.A)([' <ha-card outlined> <div class="card-content"> ',' <div class="board-info"> <p class="primary-text"> '," </p> "," </div> </div> "," "," </ha-card> "])),a?(0,T.qy)(et||(et=(0,c.A)(['<img alt="" src="','" crossorigin="anonymous" referrerpolicy="no-referrer">'])),a):"",i||this.hass.localize("ui.panel.config.hardware.generic_hardware"),r?(0,T.qy)(nt||(nt=(0,c.A)(['<p class="secondary-text">',"</p>"])),r):"",o?(0,T.qy)(rt||(rt=(0,c.A)([' <mwc-list> <ha-clickable-list-item .href="','" openNewTab twoline hasMeta> <span>','</span> <span slot="secondary">','</span> <ha-icon-next slot="meta"></ha-icon-next> </ha-clickable-list-item> </mwc-list> '])),o,this.hass.localize("ui.panel.config.hardware.documentation"),this.hass.localize("ui.panel.config.hardware.documentation_description")):"",d.length||(0,O.x)(this.hass,"hassio")?(0,T.qy)(it||(it=(0,c.A)(['<div class="card-actions"> '," "," </div>"])),d.length?(0,T.qy)(at||(at=(0,c.A)([' <mwc-button .entry="','" @click="','"> '," </mwc-button> "])),d[0],this._openOptionsFlow,this.hass.localize("ui.panel.config.hardware.configure")):T.s6,(0,O.x)(this.hass,"hassio")?(0,T.qy)(ot||(ot=(0,c.A)([' <mwc-button @click="','"> '," </mwc-button> "])),this._openHardware,this.hass.localize("ui.panel.config.hardware.available_hardware.title")):T.s6):""):"",null!=p&&p.length?(0,T.qy)(st||(st=(0,c.A)(["<ha-card outlined> "," </ha-card>"])),p.map((function(t){var e=t.config_entries.map((function(t){var e;return null===(e=l._configEntries)||void 0===e?void 0:e[t]})).filter((function(t){return(null==t?void 0:t.supports_options)&&!t.disabled_by}))[0];return(0,T.qy)(ct||(ct=(0,c.A)(['<div class="row"> ',""," </div>"])),t.name,e?(0,T.qy)(lt||(lt=(0,c.A)(['<mwc-button .entry="','" @click="','"> '," </mwc-button>"])),e,l._openOptionsFlow,l.hass.localize("ui.panel.config.hardware.configure")):"")}))):"",this._systemStatusData?(0,T.qy)(dt||(dt=(0,c.A)(['<ha-card outlined> <div class="header"> <div class="title"> ',' </div> <div class="value"> ',"",'% </div> </div> <div class="card-content"> <ha-chart-base .hass="','" .data="','" .options="','"></ha-chart-base> </div> </ha-card> <ha-card outlined> <div class="header"> <div class="title"> ',' </div> <div class="value"> '," GB / ",' GB </div> </div> <div class="card-content"> <ha-chart-base .hass="','" .data="','" .options="','"></ha-chart-base> </div> </ha-card>'])),this.hass.localize("ui.panel.config.hardware.processor"),this._systemStatusData.cpu_percent||"-",(0,Z.d)(this.hass.locale),this.hass,{datasets:[Object.assign(Object.assign({},ht),{},{data:this._cpuEntries})]},this._chartOptions,this.hass.localize("ui.panel.config.hardware.memory"),(0,N.L)(this._systemStatusData.memory_used_mb/1024,1),(0,N.L)((this._systemStatusData.memory_used_mb+this._systemStatusData.memory_free_mb)/1024,0),this.hass,{datasets:[Object.assign(Object.assign({},ht),{},{data:this._memoryEntries})]},this._chartOptions):(0,O.x)(this.hass,"hardware")?(0,T.qy)(ut||(ut=(0,c.A)(['<ha-card outlined> <div class="card-content"> <div class="value"> '," </div> </div> </ha-card>"])),this.hass.localize("ui.panel.config.hardware.loading_system_data")):"")}},{kind:"method",key:"_load",value:(a=(0,s.A)((0,o.A)().mark((function t(){var e,n;return(0,o.A)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(!(0,O.x)(this.hass,"usb")){t.next=3;break}return t.next=3,(0,C.$)(this.hass);case 3:if(e=(0,O.x)(this.hass,"hassio"),t.prev=4,!(0,O.x)(this.hass,"hardware")){t.next=9;break}return t.next=8,this.hass.callWS({type:"hardware/info"});case 8:this._hardwareInfo=t.sent;case 9:if(!e||null!==(n=this._hardwareInfo)&&void 0!==n&&n.hardware.length){t.next=13;break}return t.next=12,(0,B.PB)(this.hass);case 12:this._OSData=t.sent;case 13:t.next=18;break;case 15:t.prev=15,t.t0=t.catch(4),this._error=t.t0.message||t.t0;case 18:case"end":return t.stop()}}),t,this,[[4,15]])}))),function(){return a.apply(this,arguments)})},{kind:"method",key:"_openOptionsFlow",value:(i=(0,s.A)((0,o.A)().mark((function t(e){var n;return(0,o.A)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(n=e.currentTarget.entry){t.next=3;break}return t.abrupt("return");case 3:(0,W.Q)(this,n);case 4:case"end":return t.stop()}}),t,this)}))),function(t){return i.apply(this,arguments)})},{kind:"method",key:"_openHardware",value:(r=(0,s.A)((0,o.A)().mark((function t(){return(0,o.A)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:(0,Y.V)(this);case 1:case"end":return t.stop()}}),t,this)}))),function(){return r.apply(this,arguments)})},{kind:"method",key:"_showRestartDialog",value:(n=(0,s.A)((0,o.A)().mark((function t(){return(0,o.A)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:(0,R.l)(this);case 1:case"end":return t.stop()}}),t,this)}))),function(){return n.apply(this,arguments)})},{kind:"field",static:!0,key:"styles",value:function(){return[U.RF,(0,T.AH)(pt||(pt=(0,c.A)([".content{padding:28px 20px 0;max-width:1040px;margin:0 auto;--mdc-list-side-padding:24px;--mdc-list-vertical-padding:0}ha-card{max-width:600px;margin:0 auto;height:100%;justify-content:space-between;flex-direction:column;display:flex;margin-bottom:16px}.card-content{display:flex;justify-content:space-between;flex-direction:column;padding:16px}.card-content img{max-width:300px;margin:auto}.board-info{text-align:center}.primary-text{font-size:16px;margin:0}.secondary-text{font-size:14px;margin-bottom:0;color:var(--secondary-text-color)}.header{padding:16px;display:flex;justify-content:space-between}.header .title{color:var(--secondary-text-color);font-size:18px}.header .value{font-size:16px}.row{display:flex;justify-content:space-between;align-items:center;height:48px;padding:8px 16px}.card-actions{display:flex;justify-content:space-between}"])))]}}]}}),(0,I.E)(T.WF)),a(),t.next=93;break;case 90:t.prev=90,t.t2=t.catch(0),a(t.t2);case 93:case"end":return t.stop()}}),t,null,[[0,90]])})));return function(e,n){return t.apply(this,arguments)}}())},42276:function(t,e,n){n.d(e,{V:function(){return a}});n(95737),n(39790),n(66457),n(99019),n(96858);var r=n(34897),i=function(){return Promise.all([n.e(94131),n.e(14121),n.e(10963),n.e(72915),n.e(51431),n.e(47371)]).then(n.bind(n,37035))},a=function(t){(0,r.r)(t,"show-dialog",{dialogTag:"ha-dialog-hardware-available",dialogImport:i,dialogParams:{}})}},51842:function(t,e,n){n.d(e,{MR:function(){return r},QR:function(){return i},a_:function(){return a},bg:function(){return o}});n(81027),n(92765);var r=function(t){return"https://brands.home-assistant.io/".concat(t.brand?"brands/":"").concat(t.useFallback?"_/":"").concat(t.domain,"/").concat(t.darkOptimized?"dark_":"").concat(t.type,".png")},i=function(t){return"https://brands.home-assistant.io/hardware/".concat(t.category,"/").concat(t.darkOptimized?"dark_":"").concat(t.manufacturer).concat(t.model?"_".concat(t.model):"",".png")},a=function(t){return t.split("/")[4]},o=function(t){return t.startsWith("https://brands.home-assistant.io/")}}}]);
//# sourceMappingURL=12511.fUO5MvUyjJo.js.map