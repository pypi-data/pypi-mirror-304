"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[56476,77708],{90410:function(e,t,n){n.d(t,{ZS:function(){return f},is:function(){return v.i}});var i,r,a=n(71008),o=n(35806),d=n(62193),s=n(35890),l=n(2816),c=(n(52427),n(99019),n(79192)),u=n(29818),v=n(19637),h=null!==(r=null===(i=window.ShadyDOM)||void 0===i?void 0:i.inUse)&&void 0!==r&&r,f=function(e){function t(){var e;return(0,a.A)(this,t),(e=(0,d.A)(this,t,arguments)).disabled=!1,e.containingForm=null,e.formDataListener=function(t){e.disabled||e.setFormData(t.formData)},e}return(0,l.A)(t,e),(0,o.A)(t,[{key:"findFormElement",value:function(){if(!this.shadowRoot||h)return null;for(var e=this.getRootNode().querySelectorAll("form"),t=0,n=Array.from(e);t<n.length;t++){var i=n[t];if(i.contains(this))return i}return null}},{key:"connectedCallback",value:function(){var e;(0,s.A)(t,"connectedCallback",this,3)([]),this.containingForm=this.findFormElement(),null===(e=this.containingForm)||void 0===e||e.addEventListener("formdata",this.formDataListener)}},{key:"disconnectedCallback",value:function(){var e;(0,s.A)(t,"disconnectedCallback",this,3)([]),null===(e=this.containingForm)||void 0===e||e.removeEventListener("formdata",this.formDataListener),this.containingForm=null}},{key:"click",value:function(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}},{key:"firstUpdated",value:function(){var e=this;(0,s.A)(t,"firstUpdated",this,3)([]),this.shadowRoot&&this.mdcRoot.addEventListener("change",(function(t){e.dispatchEvent(new Event("change",t))}))}}])}(v.O);f.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,c.__decorate)([(0,u.MZ)({type:Boolean})],f.prototype,"disabled",void 0)},67056:function(e,t,n){var i=n(35806),r=n(71008),a=n(62193),o=n(2816),d=n(79192),s=n(29818),l=n(30116),c=n(43389),u=function(e){function t(){return(0,r.A)(this,t),(0,a.A)(this,t,arguments)}return(0,o.A)(t,e),(0,i.A)(t)}(l.J);u.styles=[c.R],u=(0,d.__decorate)([(0,s.EM)("mwc-list-item")],u)},79051:function(e,t,n){n.d(t,{d:function(){return i}});var i=function(e){return e.stopPropagation()}},18409:function(e,t,n){n.d(t,{s:function(){return i}});var i=function(e,t){var n,i=arguments.length>2&&void 0!==arguments[2]&&arguments[2],r=function(){for(var r=arguments.length,a=new Array(r),o=0;o<r;o++)a[o]=arguments[o];var d=i&&!n;clearTimeout(n),n=window.setTimeout((function(){n=void 0,i||e.apply(void 0,a)}),t),d&&e.apply(void 0,a)};return r.cancel=function(){clearTimeout(n)},r}},61441:function(e,t,n){n.d(t,{E:function(){return r},m:function(){return i}});n(39790),n(66457);var i=function(e){requestAnimationFrame((function(){return setTimeout(e,0)}))},r=function(){return new Promise((function(e){i(e)}))}},13830:function(e,t,n){n.d(t,{$:function(){return g}});var i,r,a,o=n(64599),d=n(35806),s=n(71008),l=n(62193),c=n(2816),u=n(27927),v=n(35890),h=(n(81027),n(30116)),f=n(43389),p=n(15112),m=n(29818),g=(0,u.A)([(0,m.EM)("ha-list-item")],(function(e,t){var n=function(t){function n(){var t;(0,s.A)(this,n);for(var i=arguments.length,r=new Array(i),a=0;a<i;a++)r[a]=arguments[a];return t=(0,l.A)(this,n,[].concat(r)),e(t),t}return(0,c.A)(n,t),(0,d.A)(n)}(t);return{F:n,d:[{kind:"method",key:"renderRipple",value:function(){return this.noninteractive?"":(0,v.A)(n,"renderRipple",this,3)([])}},{kind:"get",static:!0,key:"styles",value:function(){return[f.R,(0,p.AH)(i||(i=(0,o.A)([":host{padding-left:var(--mdc-list-side-padding-left,var(--mdc-list-side-padding,20px));padding-inline-start:var(--mdc-list-side-padding-left,var(--mdc-list-side-padding,20px));padding-right:var(--mdc-list-side-padding-right,var(--mdc-list-side-padding,20px));padding-inline-end:var(--mdc-list-side-padding-right,var(--mdc-list-side-padding,20px))}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:48px}span.material-icons:first-of-type{margin-inline-start:0px!important;margin-inline-end:var(--mdc-list-item-graphic-margin,16px)!important;direction:var(--direction)!important}span.material-icons:last-of-type{margin-inline-start:auto!important;margin-inline-end:0px!important;direction:var(--direction)!important}.mdc-deprecated-list-item__meta{display:var(--mdc-list-item-meta-display);align-items:center;flex-shrink:0}:host([graphic=icon]:not([twoline])) .mdc-deprecated-list-item__graphic{margin-inline-end:var(--mdc-list-item-graphic-margin,20px)!important}:host([multiline-secondary]){height:auto}:host([multiline-secondary]) .mdc-deprecated-list-item__text{padding:8px 0}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text{text-overflow:initial;white-space:normal;overflow:auto;display:inline-block;margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text{margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text::before{display:none}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text::before{display:none}:host([disabled]){color:var(--disabled-text-color)}:host([noninteractive]){pointer-events:unset}"]))),"rtl"===document.dir?(0,p.AH)(r||(r=(0,o.A)(["span.material-icons:first-of-type,span.material-icons:last-of-type{direction:rtl!important;--direction:rtl}"]))):(0,p.AH)(a||(a=(0,o.A)([""])))]}}]}}),h.J)},77312:function(e,t,n){var i,r,a,o,d=n(33994),s=n(22858),l=n(64599),c=n(35806),u=n(71008),v=n(62193),h=n(2816),f=n(27927),p=n(35890),m=(n(81027),n(24500)),g=n(14691),k=n(15112),y=n(29818),_=n(18409),A=n(61441);n(28066),(0,f.A)([(0,y.EM)("ha-select")],(function(e,t){var n=function(t){function n(){var t;(0,u.A)(this,n);for(var i=arguments.length,r=new Array(i),a=0;a<i;a++)r[a]=arguments[a];return t=(0,v.A)(this,n,[].concat(r)),e(t),t}return(0,h.A)(n,t),(0,c.A)(n)}(t);return{F:n,d:[{kind:"field",decorators:[(0,y.MZ)({type:Boolean})],key:"icon",value:function(){return!1}},{kind:"field",decorators:[(0,y.MZ)({type:Boolean,reflect:!0})],key:"clearable",value:function(){return!1}},{kind:"method",key:"render",value:function(){return(0,k.qy)(i||(i=(0,l.A)([" "," "," "])),(0,p.A)(n,"render",this,3)([]),this.clearable&&!this.required&&!this.disabled&&this.value?(0,k.qy)(r||(r=(0,l.A)(['<ha-icon-button label="clear" @click="','" .path="','"></ha-icon-button>'])),this._clearValue,"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"):k.s6)}},{kind:"method",key:"renderLeadingIcon",value:function(){return this.icon?(0,k.qy)(a||(a=(0,l.A)(['<span class="mdc-select__icon"><slot name="icon"></slot></span>']))):k.s6}},{kind:"method",key:"connectedCallback",value:function(){(0,p.A)(n,"connectedCallback",this,3)([]),window.addEventListener("translations-updated",this._translationsUpdated)}},{kind:"method",key:"disconnectedCallback",value:function(){(0,p.A)(n,"disconnectedCallback",this,3)([]),window.removeEventListener("translations-updated",this._translationsUpdated)}},{kind:"method",key:"_clearValue",value:function(){!this.disabled&&this.value&&(this.valueSetDirectly=!0,this.select(-1),this.mdcFoundation.handleChange())}},{kind:"field",key:"_translationsUpdated",value:function(){var e=this;return(0,_.s)((0,s.A)((0,d.A)().mark((function t(){return(0,d.A)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,(0,A.E)();case 2:e.layoutOptions();case 3:case"end":return t.stop()}}),t)}))),500)}},{kind:"field",static:!0,key:"styles",value:function(){return[g.R,(0,k.AH)(o||(o=(0,l.A)([":host([clearable]){position:relative}.mdc-select:not(.mdc-select--disabled) .mdc-select__icon{color:var(--secondary-text-color)}.mdc-select__anchor{width:var(--ha-select-min-width,200px)}.mdc-select--filled .mdc-select__anchor{height:var(--ha-select-height,56px)}.mdc-select--filled .mdc-floating-label{inset-inline-start:12px;inset-inline-end:initial;direction:var(--direction)}.mdc-select--filled.mdc-select--with-leading-icon .mdc-floating-label{inset-inline-start:48px;inset-inline-end:initial;direction:var(--direction)}.mdc-select .mdc-select__anchor{padding-inline-start:12px;padding-inline-end:0px;direction:var(--direction)}.mdc-select__anchor .mdc-floating-label--float-above{transform-origin:var(--float-start)}.mdc-select__selected-text-container{padding-inline-end:var(--select-selected-text-padding-end,0px)}:host([clearable]) .mdc-select__selected-text-container{padding-inline-end:var(--select-selected-text-padding-end,12px)}ha-icon-button{position:absolute;top:10px;right:28px;--mdc-icon-button-size:36px;--mdc-icon-size:20px;color:var(--secondary-text-color);inset-inline-start:initial;inset-inline-end:28px;direction:var(--direction)}"])))]}}]}}),m.o)},89218:function(e,t,n){n.r(t),n.d(t,{HaTTSVoiceSelector:function(){return h}});var i,r,a=n(64599),o=n(35806),d=n(71008),s=n(62193),l=n(2816),c=n(27927),u=(n(81027),n(15112)),v=n(29818),h=(n(82083),(0,c.A)([(0,v.EM)("ha-selector-tts_voice")],(function(e,t){var n=function(t){function n(){var t;(0,d.A)(this,n);for(var i=arguments.length,r=new Array(i),a=0;a<i;a++)r[a]=arguments[a];return t=(0,s.A)(this,n,[].concat(r)),e(t),t}return(0,l.A)(n,t),(0,o.A)(n)}(t);return{F:n,d:[{kind:"field",decorators:[(0,v.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,v.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,v.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,v.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,v.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,v.MZ)({type:Boolean})],key:"disabled",value:function(){return!1}},{kind:"field",decorators:[(0,v.MZ)({type:Boolean})],key:"required",value:function(){return!0}},{kind:"field",decorators:[(0,v.MZ)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){var e,t,n,r;return(0,u.qy)(i||(i=(0,a.A)(['<ha-tts-voice-picker .hass="','" .value="','" .label="','" .helper="','" .language="','" .engineId="','" .disabled="','" .required="','"></ha-tts-voice-picker>'])),this.hass,this.value,this.label,this.helper,(null===(e=this.selector.tts_voice)||void 0===e?void 0:e.language)||(null===(t=this.context)||void 0===t?void 0:t.language),(null===(n=this.selector.tts_voice)||void 0===n?void 0:n.engineId)||(null===(r=this.context)||void 0===r?void 0:r.engineId),this.disabled,this.required)}},{kind:"field",static:!0,key:"styles",value:function(){return(0,u.AH)(r||(r=(0,a.A)(["ha-tts-picker{width:100%}"])))}}]}}),u.WF))},82083:function(e,t,n){var i,r,a,o,d=n(33994),s=n(22858),l=n(64599),c=n(35806),u=n(71008),v=n(62193),h=n(2816),f=n(27927),p=n(35890),m=(n(81027),n(44124),n(97741),n(50693),n(39790),n(253),n(94438),n(16891),n(15112)),g=n(29818),k=n(34897),y=n(79051),_=n(18409),A=n(12803),x=(n(13830),n(77312),"__NONE_OPTION__");(0,f.A)([(0,g.EM)("ha-tts-voice-picker")],(function(e,t){var n,f=function(t){function n(){var t;(0,u.A)(this,n);for(var i=arguments.length,r=new Array(i),a=0;a<i;a++)r[a]=arguments[a];return t=(0,v.A)(this,n,[].concat(r)),e(t),t}return(0,h.A)(n,t),(0,c.A)(n)}(t);return{F:f,d:[{kind:"field",decorators:[(0,g.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,g.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,g.MZ)()],key:"engineId",value:void 0},{kind:"field",decorators:[(0,g.MZ)()],key:"language",value:void 0},{kind:"field",decorators:[(0,g.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,g.MZ)({type:Boolean,reflect:!0})],key:"disabled",value:function(){return!1}},{kind:"field",decorators:[(0,g.MZ)({type:Boolean})],key:"required",value:function(){return!1}},{kind:"field",decorators:[(0,g.wk)()],key:"_voices",value:void 0},{kind:"field",decorators:[(0,g.P)("ha-select")],key:"_select",value:void 0},{kind:"method",key:"render",value:function(){var e,t;if(!this._voices)return m.s6;var n=null!==(e=this.value)&&void 0!==e?e:this.required?null===(t=this._voices[0])||void 0===t?void 0:t.voice_id:x;return(0,m.qy)(i||(i=(0,l.A)([' <ha-select .label="','" .value="','" .required="','" .disabled="','" @selected="','" @closed="','" fixedMenuPosition naturalMenuWidth> '," "," </ha-select> "])),this.label||this.hass.localize("ui.components.tts-voice-picker.voice"),n,this.required,this.disabled,this._changed,y.d,this.required?m.s6:(0,m.qy)(r||(r=(0,l.A)(['<ha-list-item .value="','"> '," </ha-list-item>"])),x,this.hass.localize("ui.components.tts-voice-picker.none")),this._voices.map((function(e){return(0,m.qy)(a||(a=(0,l.A)(['<ha-list-item .value="','"> '," </ha-list-item>"])),e.voice_id,e.name)})))}},{kind:"method",key:"willUpdate",value:function(e){(0,p.A)(f,"willUpdate",this,3)([e]),this.hasUpdated?(e.has("language")||e.has("engineId"))&&this._debouncedUpdateVoices():this._updateVoices()}},{kind:"field",key:"_debouncedUpdateVoices",value:function(){var e=this;return(0,_.s)((function(){return e._updateVoices()}),500)}},{kind:"method",key:"_updateVoices",value:(n=(0,s.A)((0,d.A)().mark((function e(){var t=this;return(0,d.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(this.engineId&&this.language){e.next=3;break}return this._voices=void 0,e.abrupt("return");case 3:return e.next=5,(0,A.z3)(this.hass,this.engineId,this.language);case 5:if(this._voices=e.sent.voices,this.value){e.next=8;break}return e.abrupt("return");case 8:this._voices&&this._voices.find((function(e){return e.voice_id===t.value}))||(this.value=void 0,(0,k.r)(this,"value-changed",{value:this.value}));case 9:case"end":return e.stop()}}),e,this)}))),function(){return n.apply(this,arguments)})},{kind:"method",key:"updated",value:function(e){var t,n,i;((0,p.A)(f,"updated",this,3)([e]),e.has("_voices")&&(null===(t=this._select)||void 0===t?void 0:t.value)!==this.value)&&(null===(n=this._select)||void 0===n||n.layoutOptions(),(0,k.r)(this,"value-changed",{value:null===(i=this._select)||void 0===i?void 0:i.value}))}},{kind:"get",static:!0,key:"styles",value:function(){return(0,m.AH)(o||(o=(0,l.A)(["ha-select{width:100%}"])))}},{kind:"method",key:"_changed",value:function(e){var t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===x||(this.value=t.value===x?void 0:t.value,(0,k.r)(this,"value-changed",{value:this.value}))}}]}}),m.WF)},12803:function(e,t,n){n.d(t,{EF:function(){return o},S_:function(){return i},Xv:function(){return d},ni:function(){return a},u1:function(){return s},z3:function(){return l}});n(92765);var i=function(e,t){return e.callApi("POST","tts_get_url",t)},r="media-source://tts/",a=function(e){return e.startsWith(r)},o=function(e){return e.substring(19)},d=function(e,t,n){return e.callWS({type:"tts/engine/list",language:t,country:n})},s=function(e,t){return e.callWS({type:"tts/engine/get",engine_id:t})},l=function(e,t,n){return e.callWS({type:"tts/engine/voices",engine_id:t,language:n})}},14767:function(e,t,n){var i=n(36565);e.exports=function(e,t,n){for(var r=0,a=arguments.length>2?n:i(t),o=new e(a);a>r;)o[r]=t[r++];return o}},88124:function(e,t,n){var i=n(66293),r=n(13113),a=n(88680),o=n(49940),d=n(80896),s=n(36565),l=n(82337),c=n(14767),u=Array,v=r([].push);e.exports=function(e,t,n,r){for(var h,f,p,m=o(e),g=a(m),k=i(t,n),y=l(null),_=s(g),A=0;_>A;A++)p=g[A],(f=d(k(p,A,m)))in y?v(y[f],p):y[f]=[p];if(r&&(h=r(m))!==u)for(f in y)y[f]=c(h,y[f]);return y}},32350:function(e,t,n){var i=n(32174),r=n(23444),a=n(33616),o=n(36565),d=n(87149),s=Math.min,l=[].lastIndexOf,c=!!l&&1/[1].lastIndexOf(1,-0)<0,u=d("lastIndexOf"),v=c||!u;e.exports=v?function(e){if(c)return i(l,this,arguments)||0;var t=r(this),n=o(t);if(0===n)return-1;var d=n-1;for(arguments.length>1&&(d=s(d,a(arguments[1]))),d<0&&(d=n+d);d>=0;d--)if(d in t&&t[d]===e)return d||0;return-1}:l},73909:function(e,t,n){var i=n(13113),r=n(22669),a=n(53138),o=/"/g,d=i("".replace);e.exports=function(e,t,n,i){var s=a(r(e)),l="<"+t;return""!==n&&(l+=" "+n+'="'+d(a(i),o,"&quot;")+'"'),l+">"+s+"</"+t+">"}},75022:function(e,t,n){var i=n(26906);e.exports=function(e){return i((function(){var t=""[e]('"');return t!==t.toLowerCase()||t.split('"').length>3}))}},34465:function(e,t,n){var i=n(54935).PROPER,r=n(26906),a=n(69329);e.exports=function(e){return r((function(){return!!a[e]()||"​᠎"!=="​᠎"[e]()||i&&a[e].name!==e}))}},15814:function(e,t,n){var i=n(41765),r=n(32350);i({target:"Array",proto:!0,forced:r!==[].lastIndexOf},{lastIndexOf:r})},33628:function(e,t,n){var i=n(41765),r=n(73909);i({target:"String",proto:!0,forced:n(75022)("anchor")},{anchor:function(e){return r(this,"a","name",e)}})},79641:function(e,t,n){var i=n(41765),r=n(38971).trim;i({target:"String",proto:!0,forced:n(34465)("trim")},{trim:function(){return r(this)}})},12073:function(e,t,n){var i=n(41765),r=n(88124),a=n(2586);i({target:"Array",proto:!0},{group:function(e){return r(this,e,arguments.length>1?arguments[1]:void 0)}}),a("group")}}]);
//# sourceMappingURL=56476.b5ZnCpysnUU.js.map