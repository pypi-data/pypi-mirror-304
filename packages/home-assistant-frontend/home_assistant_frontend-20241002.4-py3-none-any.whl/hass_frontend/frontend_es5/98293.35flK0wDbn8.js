"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[98293,77708],{90410:function(e,t,n){n.d(t,{ZS:function(){return v},is:function(){return h.i}});var i,r,a=n(71008),o=n(35806),s=n(62193),d=n(35890),l=n(2816),c=(n(52427),n(99019),n(79192)),u=n(29818),h=n(19637),f=null!==(r=null===(i=window.ShadyDOM)||void 0===i?void 0:i.inUse)&&void 0!==r&&r,v=function(e){function t(){var e;return(0,a.A)(this,t),(e=(0,s.A)(this,t,arguments)).disabled=!1,e.containingForm=null,e.formDataListener=function(t){e.disabled||e.setFormData(t.formData)},e}return(0,l.A)(t,e),(0,o.A)(t,[{key:"findFormElement",value:function(){if(!this.shadowRoot||f)return null;for(var e=this.getRootNode().querySelectorAll("form"),t=0,n=Array.from(e);t<n.length;t++){var i=n[t];if(i.contains(this))return i}return null}},{key:"connectedCallback",value:function(){var e;(0,d.A)(t,"connectedCallback",this,3)([]),this.containingForm=this.findFormElement(),null===(e=this.containingForm)||void 0===e||e.addEventListener("formdata",this.formDataListener)}},{key:"disconnectedCallback",value:function(){var e;(0,d.A)(t,"disconnectedCallback",this,3)([]),null===(e=this.containingForm)||void 0===e||e.removeEventListener("formdata",this.formDataListener),this.containingForm=null}},{key:"click",value:function(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}},{key:"firstUpdated",value:function(){var e=this;(0,d.A)(t,"firstUpdated",this,3)([]),this.shadowRoot&&this.mdcRoot.addEventListener("change",(function(t){e.dispatchEvent(new Event("change",t))}))}}])}(h.O);v.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,c.__decorate)([(0,u.MZ)({type:Boolean})],v.prototype,"disabled",void 0)},67056:function(e,t,n){var i=n(35806),r=n(71008),a=n(62193),o=n(2816),s=n(79192),d=n(29818),l=n(30116),c=n(43389),u=function(e){function t(){return(0,r.A)(this,t),(0,a.A)(this,t,arguments)}return(0,o.A)(t,e),(0,i.A)(t)}(l.J);u.styles=[c.R],u=(0,s.__decorate)([(0,d.EM)("mwc-list-item")],u)},79051:function(e,t,n){n.d(t,{d:function(){return i}});var i=function(e){return e.stopPropagation()}},18409:function(e,t,n){n.d(t,{s:function(){return i}});var i=function(e,t){var n,i=arguments.length>2&&void 0!==arguments[2]&&arguments[2],r=function(){for(var r=arguments.length,a=new Array(r),o=0;o<r;o++)a[o]=arguments[o];var s=i&&!n;clearTimeout(n),n=window.setTimeout((function(){n=void 0,i||e.apply(void 0,a)}),t),s&&e.apply(void 0,a)};return r.cancel=function(){clearTimeout(n)},r}},61441:function(e,t,n){n.d(t,{E:function(){return r},m:function(){return i}});n(39790),n(66457);var i=function(e){requestAnimationFrame((function(){return setTimeout(e,0)}))},r=function(){return new Promise((function(e){i(e)}))}},13830:function(e,t,n){n.d(t,{$:function(){return g}});var i,r,a,o=n(64599),s=n(35806),d=n(71008),l=n(62193),c=n(2816),u=n(27927),h=n(35890),f=(n(81027),n(30116)),v=n(43389),p=n(15112),m=n(29818),g=(0,u.A)([(0,m.EM)("ha-list-item")],(function(e,t){var n=function(t){function n(){var t;(0,d.A)(this,n);for(var i=arguments.length,r=new Array(i),a=0;a<i;a++)r[a]=arguments[a];return t=(0,l.A)(this,n,[].concat(r)),e(t),t}return(0,c.A)(n,t),(0,s.A)(n)}(t);return{F:n,d:[{kind:"method",key:"renderRipple",value:function(){return this.noninteractive?"":(0,h.A)(n,"renderRipple",this,3)([])}},{kind:"get",static:!0,key:"styles",value:function(){return[v.R,(0,p.AH)(i||(i=(0,o.A)([":host{padding-left:var(--mdc-list-side-padding-left,var(--mdc-list-side-padding,20px));padding-inline-start:var(--mdc-list-side-padding-left,var(--mdc-list-side-padding,20px));padding-right:var(--mdc-list-side-padding-right,var(--mdc-list-side-padding,20px));padding-inline-end:var(--mdc-list-side-padding-right,var(--mdc-list-side-padding,20px))}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:48px}span.material-icons:first-of-type{margin-inline-start:0px!important;margin-inline-end:var(--mdc-list-item-graphic-margin,16px)!important;direction:var(--direction)!important}span.material-icons:last-of-type{margin-inline-start:auto!important;margin-inline-end:0px!important;direction:var(--direction)!important}.mdc-deprecated-list-item__meta{display:var(--mdc-list-item-meta-display);align-items:center;flex-shrink:0}:host([graphic=icon]:not([twoline])) .mdc-deprecated-list-item__graphic{margin-inline-end:var(--mdc-list-item-graphic-margin,20px)!important}:host([multiline-secondary]){height:auto}:host([multiline-secondary]) .mdc-deprecated-list-item__text{padding:8px 0}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text{text-overflow:initial;white-space:normal;overflow:auto;display:inline-block;margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text{margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text::before{display:none}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text::before{display:none}:host([disabled]){color:var(--disabled-text-color)}:host([noninteractive]){pointer-events:unset}"]))),"rtl"===document.dir?(0,p.AH)(r||(r=(0,o.A)(["span.material-icons:first-of-type,span.material-icons:last-of-type{direction:rtl!important;--direction:rtl}"]))):(0,p.AH)(a||(a=(0,o.A)([""])))]}}]}}),f.J)},77312:function(e,t,n){var i,r,a,o,s=n(33994),d=n(22858),l=n(64599),c=n(35806),u=n(71008),h=n(62193),f=n(2816),v=n(27927),p=n(35890),m=(n(81027),n(24500)),g=n(14691),y=n(15112),k=n(29818),_=n(18409),A=n(61441);n(28066),(0,v.A)([(0,k.EM)("ha-select")],(function(e,t){var n=function(t){function n(){var t;(0,u.A)(this,n);for(var i=arguments.length,r=new Array(i),a=0;a<i;a++)r[a]=arguments[a];return t=(0,h.A)(this,n,[].concat(r)),e(t),t}return(0,f.A)(n,t),(0,c.A)(n)}(t);return{F:n,d:[{kind:"field",decorators:[(0,k.MZ)({type:Boolean})],key:"icon",value:function(){return!1}},{kind:"field",decorators:[(0,k.MZ)({type:Boolean,reflect:!0})],key:"clearable",value:function(){return!1}},{kind:"method",key:"render",value:function(){return(0,y.qy)(i||(i=(0,l.A)([" "," "," "])),(0,p.A)(n,"render",this,3)([]),this.clearable&&!this.required&&!this.disabled&&this.value?(0,y.qy)(r||(r=(0,l.A)(['<ha-icon-button label="clear" @click="','" .path="','"></ha-icon-button>'])),this._clearValue,"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"):y.s6)}},{kind:"method",key:"renderLeadingIcon",value:function(){return this.icon?(0,y.qy)(a||(a=(0,l.A)(['<span class="mdc-select__icon"><slot name="icon"></slot></span>']))):y.s6}},{kind:"method",key:"connectedCallback",value:function(){(0,p.A)(n,"connectedCallback",this,3)([]),window.addEventListener("translations-updated",this._translationsUpdated)}},{kind:"method",key:"disconnectedCallback",value:function(){(0,p.A)(n,"disconnectedCallback",this,3)([]),window.removeEventListener("translations-updated",this._translationsUpdated)}},{kind:"method",key:"_clearValue",value:function(){!this.disabled&&this.value&&(this.valueSetDirectly=!0,this.select(-1),this.mdcFoundation.handleChange())}},{kind:"field",key:"_translationsUpdated",value:function(){var e=this;return(0,_.s)((0,d.A)((0,s.A)().mark((function t(){return(0,s.A)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,(0,A.E)();case 2:e.layoutOptions();case 3:case"end":return t.stop()}}),t)}))),500)}},{kind:"field",static:!0,key:"styles",value:function(){return[g.R,(0,y.AH)(o||(o=(0,l.A)([":host([clearable]){position:relative}.mdc-select:not(.mdc-select--disabled) .mdc-select__icon{color:var(--secondary-text-color)}.mdc-select__anchor{width:var(--ha-select-min-width,200px)}.mdc-select--filled .mdc-select__anchor{height:var(--ha-select-height,56px)}.mdc-select--filled .mdc-floating-label{inset-inline-start:12px;inset-inline-end:initial;direction:var(--direction)}.mdc-select--filled.mdc-select--with-leading-icon .mdc-floating-label{inset-inline-start:48px;inset-inline-end:initial;direction:var(--direction)}.mdc-select .mdc-select__anchor{padding-inline-start:12px;padding-inline-end:0px;direction:var(--direction)}.mdc-select__anchor .mdc-floating-label--float-above{transform-origin:var(--float-start)}.mdc-select__selected-text-container{padding-inline-end:var(--select-selected-text-padding-end,0px)}:host([clearable]) .mdc-select__selected-text-container{padding-inline-end:var(--select-selected-text-padding-end,12px)}ha-icon-button{position:absolute;top:10px;right:28px;--mdc-icon-button-size:36px;--mdc-icon-size:20px;color:var(--secondary-text-color);inset-inline-start:initial;inset-inline-end:28px;direction:var(--direction)}"])))]}}]}}),m.o)},22051:function(e,t,n){n.r(t),n.d(t,{HaTTSSelector:function(){return q}});var i,r,a,o,s,d,l=n(64599),c=n(35806),u=n(71008),h=n(62193),f=n(2816),v=n(27927),p=(n(81027),n(15112)),m=n(29818),g=n(33994),y=n(22858),k=n(64782),_=n(35890),A=(n(44124),n(82386),n(97741),n(50693),n(39790),n(9241),n(36604),n(253),n(94438),n(16891),n(34897)),b=n(79051),x=n(19244),w=n(18409),E=n(12803),M=(n(13830),n(77312),n(213)),L="__NONE_OPTION__",q=((0,v.A)([(0,m.EM)("ha-tts-picker")],(function(e,t){var n,s=function(t){function n(){var t;(0,u.A)(this,n);for(var i=arguments.length,r=new Array(i),a=0;a<i;a++)r[a]=arguments[a];return t=(0,h.A)(this,n,[].concat(r)),e(t),t}return(0,f.A)(n,t),(0,c.A)(n)}(t);return{F:s,d:[{kind:"field",decorators:[(0,m.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,m.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,m.MZ)()],key:"language",value:void 0},{kind:"field",decorators:[(0,m.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,m.MZ)({type:Boolean,reflect:!0})],key:"disabled",value:function(){return!1}},{kind:"field",decorators:[(0,m.MZ)({type:Boolean})],key:"required",value:function(){return!1}},{kind:"field",decorators:[(0,m.wk)()],key:"_engines",value:void 0},{kind:"method",key:"render",value:function(){var e=this;if(!this._engines)return p.s6;var t=this.value;if(!t&&this.required){for(var n=0,o=Object.values(this.hass.entities);n<o.length;n++){var s=o[n];if("cloud"===s.platform&&"tts"===(0,M.m)(s.entity_id)){t=s.entity_id;break}}if(!t){var d,c=(0,k.A)(this._engines);try{for(c.s();!(d=c.n()).done;){var u,h=d.value;if(0!==(null==h||null===(u=h.supported_languages)||void 0===u?void 0:u.length)){t=h.engine_id;break}}}catch(f){c.e(f)}finally{c.f()}}}return t||(t=L),(0,p.qy)(i||(i=(0,l.A)([' <ha-select .label="','" .value="','" .required="','" .disabled="','" @selected="','" @closed="','" fixedMenuPosition naturalMenuWidth> '," "," </ha-select> "])),this.label||this.hass.localize("ui.components.tts-picker.tts"),t,this.required,this.disabled,this._changed,b.d,this.required?p.s6:(0,p.qy)(r||(r=(0,l.A)(['<ha-list-item .value="','"> '," </ha-list-item>"])),L,this.hass.localize("ui.components.tts-picker.none")),this._engines.map((function(n){var i,r;if(n.deprecated&&n.engine_id!==t)return p.s6;if(n.engine_id.includes(".")){var o=e.hass.states[n.engine_id];r=o?(0,x.u)(o):n.engine_id}else r=n.name||n.engine_id;return(0,p.qy)(a||(a=(0,l.A)(['<ha-list-item .value="','" .disabled="','"> '," </ha-list-item>"])),n.engine_id,0===(null===(i=n.supported_languages)||void 0===i?void 0:i.length),r)})))}},{kind:"method",key:"willUpdate",value:function(e){(0,_.A)(s,"willUpdate",this,3)([e]),this.hasUpdated?e.has("language")&&this._debouncedUpdateEngines():this._updateEngines()}},{kind:"field",key:"_debouncedUpdateEngines",value:function(){var e=this;return(0,w.s)((function(){return e._updateEngines()}),500)}},{kind:"method",key:"_updateEngines",value:(n=(0,y.A)((0,g.A)().mark((function e(){var t,n,i=this;return(0,g.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,(0,E.Xv)(this.hass,this.language,this.hass.config.country||void 0);case 2:if(this._engines=e.sent.providers,this.value){e.next=5;break}return e.abrupt("return");case 5:n=this._engines.find((function(e){return e.engine_id===i.value})),(0,A.r)(this,"supported-languages-changed",{value:null==n?void 0:n.supported_languages}),n&&0!==(null===(t=n.supported_languages)||void 0===t?void 0:t.length)||(this.value=void 0,(0,A.r)(this,"value-changed",{value:this.value}));case 8:case"end":return e.stop()}}),e,this)}))),function(){return n.apply(this,arguments)})},{kind:"get",static:!0,key:"styles",value:function(){return(0,p.AH)(o||(o=(0,l.A)(["ha-select{width:100%}"])))}},{kind:"method",key:"_changed",value:function(e){var t,n=this,i=e.target;!this.hass||""===i.value||i.value===this.value||void 0===this.value&&i.value===L||(this.value=i.value===L?void 0:i.value,(0,A.r)(this,"value-changed",{value:this.value}),(0,A.r)(this,"supported-languages-changed",{value:null===(t=this._engines.find((function(e){return e.engine_id===n.value})))||void 0===t?void 0:t.supported_languages}))}}]}}),p.WF),(0,v.A)([(0,m.EM)("ha-selector-tts")],(function(e,t){var n=function(t){function n(){var t;(0,u.A)(this,n);for(var i=arguments.length,r=new Array(i),a=0;a<i;a++)r[a]=arguments[a];return t=(0,h.A)(this,n,[].concat(r)),e(t),t}return(0,f.A)(n,t),(0,c.A)(n)}(t);return{F:n,d:[{kind:"field",decorators:[(0,m.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,m.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,m.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,m.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,m.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,m.MZ)({type:Boolean})],key:"disabled",value:function(){return!1}},{kind:"field",decorators:[(0,m.MZ)({type:Boolean})],key:"required",value:function(){return!0}},{kind:"field",decorators:[(0,m.MZ)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){var e,t;return(0,p.qy)(s||(s=(0,l.A)(['<ha-tts-picker .hass="','" .value="','" .label="','" .helper="','" .language="','" .disabled="','" .required="','"></ha-tts-picker>'])),this.hass,this.value,this.label,this.helper,(null===(e=this.selector.tts)||void 0===e?void 0:e.language)||(null===(t=this.context)||void 0===t?void 0:t.language),this.disabled,this.required)}},{kind:"field",static:!0,key:"styles",value:function(){return(0,p.AH)(d||(d=(0,l.A)(["ha-tts-picker{width:100%}"])))}}]}}),p.WF))},12803:function(e,t,n){n.d(t,{EF:function(){return o},S_:function(){return i},Xv:function(){return s},ni:function(){return a},u1:function(){return d},z3:function(){return l}});n(92765);var i=function(e,t){return e.callApi("POST","tts_get_url",t)},r="media-source://tts/",a=function(e){return e.startsWith(r)},o=function(e){return e.substring(19)},s=function(e,t,n){return e.callWS({type:"tts/engine/list",language:t,country:n})},d=function(e,t){return e.callWS({type:"tts/engine/get",engine_id:t})},l=function(e,t,n){return e.callWS({type:"tts/engine/voices",engine_id:t,language:n})}},14767:function(e,t,n){var i=n(36565);e.exports=function(e,t,n){for(var r=0,a=arguments.length>2?n:i(t),o=new e(a);a>r;)o[r]=t[r++];return o}},88124:function(e,t,n){var i=n(66293),r=n(13113),a=n(88680),o=n(49940),s=n(80896),d=n(36565),l=n(82337),c=n(14767),u=Array,h=r([].push);e.exports=function(e,t,n,r){for(var f,v,p,m=o(e),g=a(m),y=i(t,n),k=l(null),_=d(g),A=0;_>A;A++)p=g[A],(v=s(y(p,A,m)))in k?h(k[v],p):k[v]=[p];if(r&&(f=r(m))!==u)for(v in k)k[v]=c(f,k[v]);return k}},32350:function(e,t,n){var i=n(32174),r=n(23444),a=n(33616),o=n(36565),s=n(87149),d=Math.min,l=[].lastIndexOf,c=!!l&&1/[1].lastIndexOf(1,-0)<0,u=s("lastIndexOf"),h=c||!u;e.exports=h?function(e){if(c)return i(l,this,arguments)||0;var t=r(this),n=o(t);if(0===n)return-1;var s=n-1;for(arguments.length>1&&(s=d(s,a(arguments[1]))),s<0&&(s=n+s);s>=0;s--)if(s in t&&t[s]===e)return s||0;return-1}:l},73909:function(e,t,n){var i=n(13113),r=n(22669),a=n(53138),o=/"/g,s=i("".replace);e.exports=function(e,t,n,i){var d=a(r(e)),l="<"+t;return""!==n&&(l+=" "+n+'="'+s(a(i),o,"&quot;")+'"'),l+">"+d+"</"+t+">"}},75022:function(e,t,n){var i=n(26906);e.exports=function(e){return i((function(){var t=""[e]('"');return t!==t.toLowerCase()||t.split('"').length>3}))}},34465:function(e,t,n){var i=n(54935).PROPER,r=n(26906),a=n(69329);e.exports=function(e){return r((function(){return!!a[e]()||"​᠎"!=="​᠎"[e]()||i&&a[e].name!==e}))}},15814:function(e,t,n){var i=n(41765),r=n(32350);i({target:"Array",proto:!0,forced:r!==[].lastIndexOf},{lastIndexOf:r})},33628:function(e,t,n){var i=n(41765),r=n(73909);i({target:"String",proto:!0,forced:n(75022)("anchor")},{anchor:function(e){return r(this,"a","name",e)}})},79641:function(e,t,n){var i=n(41765),r=n(38971).trim;i({target:"String",proto:!0,forced:n(34465)("trim")},{trim:function(){return r(this)}})},12073:function(e,t,n){var i=n(41765),r=n(88124),a=n(2586);i({target:"Array",proto:!0},{group:function(e){return r(this,e,arguments.length>1?arguments[1]:void 0)}}),a("group")}}]);
//# sourceMappingURL=98293.35flK0wDbn8.js.map