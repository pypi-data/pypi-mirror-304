(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[83178],{54838:function(t,e,i){"use strict";i.r(e),i.d(e,{Button:function(){return u}});var n=i(35806),r=i(71008),o=i(62193),a=i(2816),d=i(79192),s=i(29818),l=i(3238),c=i(49141),u=function(t){function e(){return(0,r.A)(this,e),(0,o.A)(this,e,arguments)}return(0,a.A)(e,t),(0,n.A)(e)}(l.u);u.styles=[c.R],u=(0,d.__decorate)([(0,s.EM)("mwc-button")],u)},67056:function(t,e,i){"use strict";var n=i(35806),r=i(71008),o=i(62193),a=i(2816),d=i(79192),s=i(29818),l=i(30116),c=i(43389),u=function(t){function e(){return(0,r.A)(this,e),(0,o.A)(this,e,arguments)}return(0,a.A)(e,t),(0,n.A)(e)}(l.J);u.styles=[c.R],u=(0,d.__decorate)([(0,s.EM)("mwc-list-item")],u)},26207:function(t,e,i){"use strict";var n,r,o,a,d=i(64599),s=i(35806),l=i(71008),c=i(62193),u=i(2816),h=i(27927),p=i(35890),f=(i(81027),i(15112)),m=i(29818),v=i(13830);(0,h.A)([(0,m.EM)("ha-clickable-list-item")],(function(t,e){var i=function(e){function i(){var e;(0,l.A)(this,i);for(var n=arguments.length,r=new Array(n),o=0;o<n;o++)r[o]=arguments[o];return e=(0,c.A)(this,i,[].concat(r)),t(e),e}return(0,u.A)(i,e),(0,s.A)(i)}(e);return{F:i,d:[{kind:"field",decorators:[(0,m.MZ)()],key:"href",value:void 0},{kind:"field",decorators:[(0,m.MZ)({type:Boolean})],key:"disableHref",value:function(){return!1}},{kind:"field",decorators:[(0,m.MZ)({type:Boolean,reflect:!0})],key:"openNewTab",value:function(){return!1}},{kind:"field",decorators:[(0,m.P)("a")],key:"_anchor",value:void 0},{kind:"method",key:"render",value:function(){var t=(0,p.A)(i,"render",this,3)([]),e=this.href||"";return(0,f.qy)(n||(n=(0,d.A)(["",""])),this.disableHref?(0,f.qy)(r||(r=(0,d.A)(["<a>","</a>"])),t):(0,f.qy)(o||(o=(0,d.A)(['<a target="','" href="','">',"</a>"])),this.openNewTab?"_blank":"",e,t))}},{kind:"method",key:"firstUpdated",value:function(){var t=this;(0,p.A)(i,"firstUpdated",this,3)([]),this.addEventListener("keydown",(function(e){"Enter"!==e.key&&" "!==e.key||t._anchor.click()}))}},{kind:"get",static:!0,key:"styles",value:function(){return[(0,p.A)(i,"styles",this),(0,f.AH)(a||(a=(0,d.A)(["a{width:100%;height:100%;display:flex;align-items:center;overflow:hidden}"])))]}}]}}),v.$)},3276:function(t,e,i){"use strict";i.d(e,{l:function(){return k}});var n,r,o,a=i(35806),d=i(71008),s=i(62193),l=i(2816),c=i(27927),u=i(35890),h=i(64599),p=(i(71522),i(81027),i(79243),i(54653)),f=i(34599),m=i(15112),v=i(29818),g=i(90952),y=(i(28066),["button","ha-list-item"]),k=function(t,e){var i;return(0,m.qy)(n||(n=(0,h.A)([' <div class="header_title"> <span>','</span> <ha-icon-button .label="','" .path="','" dialogAction="close" class="header_button"></ha-icon-button> </div> '])),e,null!==(i=null==t?void 0:t.localize("ui.dialogs.generic.close"))&&void 0!==i?i:"Close","M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z")};(0,c.A)([(0,v.EM)("ha-dialog")],(function(t,e){var i=function(e){function i(){var e;(0,d.A)(this,i);for(var n=arguments.length,r=new Array(n),o=0;o<n;o++)r[o]=arguments[o];return e=(0,s.A)(this,i,[].concat(r)),t(e),e}return(0,l.A)(i,e),(0,a.A)(i)}(e);return{F:i,d:[{kind:"field",key:g.Xr,value:void 0},{kind:"method",key:"scrollToPos",value:function(t,e){var i;null===(i=this.contentElement)||void 0===i||i.scrollTo(t,e)}},{kind:"method",key:"renderHeading",value:function(){return(0,m.qy)(r||(r=(0,h.A)(['<slot name="heading"> '," </slot>"])),(0,u.A)(i,"renderHeading",this,3)([]))}},{kind:"method",key:"firstUpdated",value:function(){var t;(0,u.A)(i,"firstUpdated",this,3)([]),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,y].join(", "),this._updateScrolledAttribute(),null===(t=this.contentElement)||void 0===t||t.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,u.A)(i,"disconnectedCallback",this,3)([]),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value:function(){var t=this;return function(){t._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value:function(){return[f.R,(0,m.AH)(o||(o=(0,h.A)([":host([scrolled]) ::slotted(ha-dialog-header){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.mdc-dialog{--mdc-dialog-scroll-divider-color:var(\n          --dialog-scroll-divider-color,\n          var(--divider-color)\n        );z-index:var(--dialog-z-index,8);-webkit-backdrop-filter:var(--ha-dialog-scrim-backdrop-filter,var(--dialog-backdrop-filter,none));backdrop-filter:var(--ha-dialog-scrim-backdrop-filter,var(--dialog-backdrop-filter,none));--mdc-dialog-box-shadow:var(--dialog-box-shadow, none);--mdc-typography-headline6-font-weight:400;--mdc-typography-headline6-font-size:1.574rem}.mdc-dialog__actions{justify-content:var(--justify-action-buttons,flex-end);padding-bottom:max(env(safe-area-inset-bottom),24px)}.mdc-dialog__actions span:first-child{flex:var(--secondary-action-button-flex,unset)}.mdc-dialog__actions span:nth-child(2){flex:var(--primary-action-button-flex,unset)}.mdc-dialog__container{align-items:var(--vertical-align-dialog,center)}.mdc-dialog__title{padding:24px 24px 0 24px}.mdc-dialog__actions{padding:12px 24px 12px 24px}.mdc-dialog__title::before{content:unset}.mdc-dialog .mdc-dialog__content{position:var(--dialog-content-position,relative);padding:var(--dialog-content-padding,24px)}:host([hideactions]) .mdc-dialog .mdc-dialog__content{padding-bottom:max(var(--dialog-content-padding,24px),env(safe-area-inset-bottom))}.mdc-dialog .mdc-dialog__surface{position:var(--dialog-surface-position,relative);top:var(--dialog-surface-top);margin-top:var(--dialog-surface-margin-top);min-height:var(--mdc-dialog-min-height,auto);border-radius:var(--ha-dialog-border-radius,28px);-webkit-backdrop-filter:var(--ha-dialog-surface-backdrop-filter,none);backdrop-filter:var(--ha-dialog-surface-backdrop-filter,none);background:var(--ha-dialog-surface-background,var(--mdc-theme-surface,#fff))}:host([flexContent]) .mdc-dialog .mdc-dialog__content{display:flex;flex-direction:column}.header_title{position:relative;padding-right:40px;padding-inline-end:40px;padding-inline-start:initial;direction:var(--direction)}.header_title span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:block}.header_button{position:absolute;right:-12px;top:-12px;text-decoration:none;color:inherit;inset-inline-start:initial;inset-inline-end:-12px;direction:var(--direction)}.dialog-actions{inset-inline-start:initial!important;inset-inline-end:0px!important;direction:var(--direction)}"])))]}}]}}),p.u)},13830:function(t,e,i){"use strict";i.d(e,{$:function(){return g}});var n,r,o,a=i(64599),d=i(35806),s=i(71008),l=i(62193),c=i(2816),u=i(27927),h=i(35890),p=(i(81027),i(30116)),f=i(43389),m=i(15112),v=i(29818),g=(0,u.A)([(0,v.EM)("ha-list-item")],(function(t,e){var i=function(e){function i(){var e;(0,s.A)(this,i);for(var n=arguments.length,r=new Array(n),o=0;o<n;o++)r[o]=arguments[o];return e=(0,l.A)(this,i,[].concat(r)),t(e),e}return(0,c.A)(i,e),(0,d.A)(i)}(e);return{F:i,d:[{kind:"method",key:"renderRipple",value:function(){return this.noninteractive?"":(0,h.A)(i,"renderRipple",this,3)([])}},{kind:"get",static:!0,key:"styles",value:function(){return[f.R,(0,m.AH)(n||(n=(0,a.A)([":host{padding-left:var(--mdc-list-side-padding-left,var(--mdc-list-side-padding,20px));padding-inline-start:var(--mdc-list-side-padding-left,var(--mdc-list-side-padding,20px));padding-right:var(--mdc-list-side-padding-right,var(--mdc-list-side-padding,20px));padding-inline-end:var(--mdc-list-side-padding-right,var(--mdc-list-side-padding,20px))}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:48px}span.material-icons:first-of-type{margin-inline-start:0px!important;margin-inline-end:var(--mdc-list-item-graphic-margin,16px)!important;direction:var(--direction)!important}span.material-icons:last-of-type{margin-inline-start:auto!important;margin-inline-end:0px!important;direction:var(--direction)!important}.mdc-deprecated-list-item__meta{display:var(--mdc-list-item-meta-display);align-items:center;flex-shrink:0}:host([graphic=icon]:not([twoline])) .mdc-deprecated-list-item__graphic{margin-inline-end:var(--mdc-list-item-graphic-margin,20px)!important}:host([multiline-secondary]){height:auto}:host([multiline-secondary]) .mdc-deprecated-list-item__text{padding:8px 0}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text{text-overflow:initial;white-space:normal;overflow:auto;display:inline-block;margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text{margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text::before{display:none}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text::before{display:none}:host([disabled]){color:var(--disabled-text-color)}:host([noninteractive]){pointer-events:unset}"]))),"rtl"===document.dir?(0,m.AH)(r||(r=(0,a.A)(["span.material-icons:first-of-type,span.material-icons:last-of-type{direction:rtl!important;--direction:rtl}"]))):(0,m.AH)(o||(o=(0,a.A)([""])))]}}]}}),p.J)},61429:function(t,e,i){"use strict";var n,r,o,a,d,s,l=i(64599),c=i(35806),u=i(71008),h=i(62193),p=i(2816),f=i(27927),m=(i(81027),i(54838),i(15112)),v=i(29818),g=i(34897),y=(i(13082),i(3276)),k=i(55321),A=i(33994),_=i(64782),b=i(22858),x=i(35890),w=(i(97741),i(33231),i(82115),i(16891),i(63893),i(26207),i(46092)),E=i(51842),M=i(84976);(0,f.A)([(0,v.EM)("integrations-startup-time")],(function(t,e){var i,d,s=function(e){function i(){var e;(0,u.A)(this,i);for(var n=arguments.length,r=new Array(n),o=0;o<n;o++)r[o]=arguments[o];return e=(0,h.A)(this,i,[].concat(r)),t(e),e}return(0,p.A)(i,e),(0,c.A)(i)}(e);return{F:s,d:[{kind:"field",decorators:[(0,v.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,v.MZ)({type:Boolean})],key:"narrow",value:function(){return!1}},{kind:"field",decorators:[(0,v.wk)()],key:"_manifests",value:void 0},{kind:"field",decorators:[(0,v.wk)()],key:"_setups",value:void 0},{kind:"method",key:"firstUpdated",value:function(t){(0,x.A)(s,"firstUpdated",this,3)([t]),this._fetchManifests(),this._fetchSetups()}},{kind:"method",key:"render",value:function(){var t,e=this;return this._setups?(0,m.qy)(n||(n=(0,l.A)([" <mwc-list> "," </mwc-list> "])),null===(t=this._setups)||void 0===t?void 0:t.map((function(t){var i,n,a=e._manifests&&e._manifests[t.domain],d=a?a.is_built_in?(0,M.o)(e.hass,"/integrations/".concat(a.domain)):a.documentation:"",s=null===(i=t.seconds)||void 0===i?void 0:i.toFixed(2);return(0,m.qy)(r||(r=(0,l.A)([' <ha-clickable-list-item graphic="avatar" twoline hasMeta openNewTab href="','"> <img alt="" loading="lazy" src="','" crossorigin="anonymous" referrerpolicy="no-referrer" slot="graphic"> <span> ',' </span> <span slot="secondary">','</span> <div slot="meta"> '," </div> </ha-clickable-list-item> "])),d,(0,E.MR)({domain:t.domain,type:"icon",useFallback:!0,darkOptimized:null===(n=e.hass.themes)||void 0===n?void 0:n.darkMode}),(0,w.p$)(e.hass.localize,t.domain,a),t.domain,s?(0,m.qy)(o||(o=(0,l.A)([""," s"])),s):"")}))):m.s6}},{kind:"method",key:"_fetchManifests",value:(d=(0,b.A)((0,A.A)().mark((function t(){var e,i,n,r;return(0,A.A)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return e={},t.t0=_.A,t.next=4,(0,w.fK)(this.hass);case 4:t.t1=t.sent,i=(0,t.t0)(t.t1);try{for(i.s();!(n=i.n()).done;)r=n.value,e[r.domain]=r}catch(o){i.e(o)}finally{i.f()}this._manifests=e;case 8:case"end":return t.stop()}}),t,this)}))),function(){return d.apply(this,arguments)})},{kind:"method",key:"_fetchSetups",value:(i=(0,b.A)((0,A.A)().mark((function t(){var e;return(0,A.A)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,(0,w.$h)(this.hass);case 2:e=t.sent,this._setups=e.sort((function(t,e){return t.seconds===e.seconds?0:void 0===t.seconds||void 0===e.seconds?1:e.seconds-t.seconds}));case 4:case"end":return t.stop()}}),t,this)}))),function(){return i.apply(this,arguments)})},{kind:"get",static:!0,key:"styles",value:function(){return(0,m.AH)(a||(a=(0,l.A)(["ha-clickable-list-item{--mdc-list-item-meta-size:64px;--mdc-typography-caption-font-size:12px}img{display:block;max-height:40px;max-width:40px}div[slot=meta]{display:flex;justify-content:center;align-items:center}"])))}}]}}),m.WF),(0,f.A)([(0,v.EM)("dialog-integration-startup")],(function(t,e){var i=function(e){function i(){var e;(0,u.A)(this,i);for(var n=arguments.length,r=new Array(n),o=0;o<n;o++)r[o]=arguments[o];return e=(0,h.A)(this,i,[].concat(r)),t(e),e}return(0,p.A)(i,e),(0,c.A)(i)}(e);return{F:i,d:[{kind:"field",decorators:[(0,v.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,v.wk)()],key:"_opened",value:function(){return!1}},{kind:"method",key:"showDialog",value:function(){this._opened=!0}},{kind:"method",key:"closeDialog",value:function(){this._opened=!1,(0,g.r)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return this._opened?(0,m.qy)(d||(d=(0,l.A)([' <ha-dialog open hideActions .heading="','" @closed="','"> <integrations-startup-time .hass="','" narrow></integrations-startup-time> </ha-dialog> '])),(0,y.l)(this.hass,this.hass.localize("ui.panel.config.repairs.integration_startup_time")),this.closeDialog,this.hass):m.s6}},{kind:"field",static:!0,key:"styles",value:function(){return[k.nA,(0,m.AH)(s||(s=(0,l.A)(["ha-dialog{--dialog-content-padding:0}"])))]}}]}}),m.WF)},71522:function(){Element.prototype.toggleAttribute||(Element.prototype.toggleAttribute=function(t,e){return void 0!==e&&(e=!!e),this.hasAttribute(t)?!!e||(this.removeAttribute(t),!1):!1!==e&&(this.setAttribute(t,""),!0)})},84976:function(t,e,i){"use strict";i.d(e,{o:function(){return n}});i(81027),i(82386),i(36604);var n=function(t,e){return"https://".concat(t.config.version.includes("b")?"rc":t.config.version.includes("dev")?"next":"www",".home-assistant.io").concat(e)}},90924:function(t,e,i){"use strict";var n=i(33616),r=i(53138),o=i(22669),a=RangeError;t.exports=function(t){var e=r(o(this)),i="",d=n(t);if(d<0||d===1/0)throw new a("Wrong number of repetitions");for(;d>0;(d>>>=1)&&(e+=e))1&d&&(i+=e);return i}},82115:function(t,e,i){"use strict";var n=i(41765),r=i(13113),o=i(33616),a=i(64849),d=i(90924),s=i(26906),l=RangeError,c=String,u=Math.floor,h=r(d),p=r("".slice),f=r(1..toFixed),m=function(t,e,i){return 0===e?i:e%2==1?m(t,e-1,i*t):m(t*t,e/2,i)},v=function(t,e,i){for(var n=-1,r=i;++n<6;)r+=e*t[n],t[n]=r%1e7,r=u(r/1e7)},g=function(t,e){for(var i=6,n=0;--i>=0;)n+=t[i],t[i]=u(n/e),n=n%e*1e7},y=function(t){for(var e=6,i="";--e>=0;)if(""!==i||0===e||0!==t[e]){var n=c(t[e]);i=""===i?n:i+h("0",7-n.length)+n}return i};n({target:"Number",proto:!0,forced:s((function(){return"0.000"!==f(8e-5,3)||"1"!==f(.9,0)||"1.25"!==f(1.255,2)||"1000000000000000128"!==f(0xde0b6b3a7640080,0)}))||!s((function(){f({})}))},{toFixed:function(t){var e,i,n,r,d=a(this),s=o(t),u=[0,0,0,0,0,0],f="",k="0";if(s<0||s>20)throw new l("Incorrect fraction digits");if(d!=d)return"NaN";if(d<=-1e21||d>=1e21)return c(d);if(d<0&&(f="-",d=-d),d>1e-21)if(i=(e=function(t){for(var e=0,i=t;i>=4096;)e+=12,i/=4096;for(;i>=2;)e+=1,i/=2;return e}(d*m(2,69,1))-69)<0?d*m(2,-e,1):d/m(2,e,1),i*=4503599627370496,(e=52-e)>0){for(v(u,0,i),n=s;n>=7;)v(u,1e7,0),n-=7;for(v(u,m(10,n,1),0),n=e-1;n>=23;)g(u,1<<23),n-=23;g(u,1<<n),v(u,1,1),g(u,2),k=y(u)}else v(u,0,i),v(u,1<<-e,0),k=y(u)+h("0",s);return k=s>0?f+((r=k.length)<=s?"0."+h("0",s-r)+k:p(k,0,r-s)+"."+p(k,r-s)):f+k}})}}]);
//# sourceMappingURL=83178.GlntvF89Uhs.js.map