/*! For license information please see 71893.Ph5LlUfy5jw.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[71893],{40141:function(e,t,i){i.d(t,{v:function(){return _}});var a,r,o,n,l,s,c=i(64599),d=i(71008),u=i(35806),h=i(62193),v=i(35890),p=i(2816),b=(i(26098),i(79192)),f=(i(39299),i(70252),i(15112)),g=i(29818),y=i(85323),_=function(e){function t(){var e;return(0,d.A)(this,t),(e=(0,h.A)(this,t)).disabled=!1,e.softDisabled=!1,e.alwaysFocusable=!1,e.label="",e.hasIcon=!1,f.S$||e.addEventListener("click",e.handleClick.bind(e)),e}return(0,p.A)(t,e),(0,u.A)(t,[{key:"rippleDisabled",get:function(){return this.disabled||this.softDisabled}},{key:"focus",value:function(e){this.disabled&&!this.alwaysFocusable||(0,v.A)(t,"focus",this,3)([e])}},{key:"render",value:function(){return(0,f.qy)(a||(a=(0,c.A)([' <div class="container ','"> '," </div> "])),(0,y.H)(this.getContainerClasses()),this.renderContainerContent())}},{key:"updated",value:function(e){e.has("disabled")&&void 0!==e.get("disabled")&&this.dispatchEvent(new Event("update-focus",{bubbles:!0}))}},{key:"getContainerClasses",value:function(){return{disabled:this.disabled||this.softDisabled,"has-icon":this.hasIcon}}},{key:"renderContainerContent",value:function(){return(0,f.qy)(r||(r=(0,c.A)([" ",' <md-focus-ring part="focus-ring" for="','"></md-focus-ring> <md-ripple for="','" ?disabled="','"></md-ripple> '," "])),this.renderOutline(),this.primaryId,this.primaryId,this.rippleDisabled,this.renderPrimaryAction(this.renderPrimaryContent()))}},{key:"renderOutline",value:function(){return(0,f.qy)(o||(o=(0,c.A)(['<span class="outline"></span>'])))}},{key:"renderLeadingIcon",value:function(){return(0,f.qy)(n||(n=(0,c.A)(['<slot name="icon" @slotchange="','"></slot>'])),this.handleIconChange)}},{key:"renderPrimaryContent",value:function(){return(0,f.qy)(l||(l=(0,c.A)([' <span class="leading icon" aria-hidden="true"> ',' </span> <span class="label"> <span class="label-text" id="label"> ',' </span> </span> <span class="touch"></span> '])),this.renderLeadingIcon(),this.label?this.label:(0,f.qy)(s||(s=(0,c.A)(["<slot></slot>"]))))}},{key:"handleIconChange",value:function(e){var t=e.target;this.hasIcon=t.assignedElements({flatten:!0}).length>0}},{key:"handleClick",value:function(e){if(this.softDisabled||this.disabled&&this.alwaysFocusable)return e.stopImmediatePropagation(),void e.preventDefault()}}])}((0,i(26604).n)(f.WF));_.shadowRootOptions=Object.assign(Object.assign({},f.WF.shadowRootOptions),{},{delegatesFocus:!0}),(0,b.__decorate)([(0,g.MZ)({type:Boolean,reflect:!0})],_.prototype,"disabled",void 0),(0,b.__decorate)([(0,g.MZ)({type:Boolean,attribute:"soft-disabled",reflect:!0})],_.prototype,"softDisabled",void 0),(0,b.__decorate)([(0,g.MZ)({type:Boolean,attribute:"always-focusable"})],_.prototype,"alwaysFocusable",void 0),(0,b.__decorate)([(0,g.MZ)()],_.prototype,"label",void 0),(0,b.__decorate)([(0,g.MZ)({type:Boolean,reflect:!0,attribute:"has-icon"})],_.prototype,"hasIcon",void 0)},52116:function(e,t,i){i.d(t,{M:function(){return v}});var a,r=i(64599),o=i(71008),n=i(35806),l=i(62193),s=i(35890),c=i(2816),d=i(15112),u=i(40141),h="aria-label-remove",v=function(e){function t(){var e;return(0,o.A)(this,t),(e=(0,l.A)(this,t)).handleTrailingActionFocus=e.handleTrailingActionFocus.bind(e),d.S$||e.addEventListener("keydown",e.handleKeyDown.bind(e)),e}return(0,c.A)(t,e),(0,n.A)(t,[{key:"ariaLabelRemove",get:function(){if(this.hasAttribute(h))return this.getAttribute(h);var e=this.ariaLabel;return e||this.label?"Remove ".concat(e||this.label):null},set:function(e){e!==this.ariaLabelRemove&&(null===e?this.removeAttribute(h):this.setAttribute(h,e),this.requestUpdate())}},{key:"focus",value:function(e){(this.alwaysFocusable||!this.disabled)&&null!=e&&e.trailing&&this.trailingAction?this.trailingAction.focus(e):(0,s.A)(t,"focus",this,3)([e])}},{key:"renderContainerContent",value:function(){return(0,d.qy)(a||(a=(0,r.A)([" "," "," "])),(0,s.A)(t,"renderContainerContent",this,3)([]),this.renderTrailingAction(this.handleTrailingActionFocus))}},{key:"handleKeyDown",value:function(e){var t,i,a="ArrowLeft"===e.key,r="ArrowRight"===e.key;if((a||r)&&this.primaryAction&&this.trailingAction){var o="rtl"===getComputedStyle(this).direction?a:r,n=null===(t=this.primaryAction)||void 0===t?void 0:t.matches(":focus-within"),l=null===(i=this.trailingAction)||void 0===i?void 0:i.matches(":focus-within");if(!(o&&l||!o&&n))e.preventDefault(),e.stopPropagation(),(o?this.trailingAction:this.primaryAction).focus()}}},{key:"handleTrailingActionFocus",value:function(){var e=this.primaryAction,t=this.trailingAction;e&&t&&(e.tabIndex=-1,t.addEventListener("focusout",(function(){e.tabIndex=0}),{once:!0}))}}])}(u.v)},46898:function(e,t,i){i.d(t,{R:function(){return o}});var a,r=i(64599),o=(0,i(15112).AH)(a||(a=(0,r.A)([".selected{--md-ripple-hover-color:var(--_selected-hover-state-layer-color);--md-ripple-hover-opacity:var(--_selected-hover-state-layer-opacity);--md-ripple-pressed-color:var(--_selected-pressed-state-layer-color);--md-ripple-pressed-opacity:var(--_selected-pressed-state-layer-opacity)}:where(.selected)::before{background:var(--_selected-container-color)}:where(.selected) .outline{border-width:var(--_selected-outline-width)}:where(.selected.disabled)::before{background:var(--_disabled-selected-container-color);opacity:var(--_disabled-selected-container-opacity)}:where(.selected) .label{color:var(--_selected-label-text-color)}:where(.selected:hover) .label{color:var(--_selected-hover-label-text-color)}:where(.selected:focus) .label{color:var(--_selected-focus-label-text-color)}:where(.selected:active) .label{color:var(--_selected-pressed-label-text-color)}:where(.selected) .leading.icon{color:var(--_selected-leading-icon-color)}:where(.selected:hover) .leading.icon{color:var(--_selected-hover-leading-icon-color)}:where(.selected:focus) .leading.icon{color:var(--_selected-focus-leading-icon-color)}:where(.selected:active) .leading.icon{color:var(--_selected-pressed-leading-icon-color)}@media(forced-colors:active){:where(.selected:not(.elevated))::before{border:1px solid CanvasText}:where(.selected) .outline{border-width:1px}}"])))},89325:function(e,t,i){i.d(t,{R:function(){return o}});var a,r=i(64599),o=(0,i(15112).AH)(a||(a=(0,r.A)([':host{border-start-start-radius:var(--_container-shape-start-start);border-start-end-radius:var(--_container-shape-start-end);border-end-start-radius:var(--_container-shape-end-start);border-end-end-radius:var(--_container-shape-end-end);display:inline-flex;height:var(--_container-height);cursor:pointer;-webkit-tap-highlight-color:transparent;--md-ripple-hover-color:var(--_hover-state-layer-color);--md-ripple-hover-opacity:var(--_hover-state-layer-opacity);--md-ripple-pressed-color:var(--_pressed-state-layer-color);--md-ripple-pressed-opacity:var(--_pressed-state-layer-opacity)}:host(:is([disabled],[soft-disabled])){pointer-events:none}:host([touch-target=wrapper]){margin:max(0px,(48px - var(--_container-height))/2) 0}md-focus-ring{--md-focus-ring-shape-start-start:var(--_container-shape-start-start);--md-focus-ring-shape-start-end:var(--_container-shape-start-end);--md-focus-ring-shape-end-end:var(--_container-shape-end-end);--md-focus-ring-shape-end-start:var(--_container-shape-end-start)}.container{border-radius:inherit;box-sizing:border-box;display:flex;height:100%;position:relative;width:100%}.container::before{border-radius:inherit;content:"";inset:0;pointer-events:none;position:absolute}.container:not(.disabled){cursor:pointer}.container.disabled{pointer-events:none}.cell{display:flex}.action{align-items:baseline;appearance:none;background:0 0;border:none;border-radius:inherit;display:flex;outline:0;padding:0;position:relative;text-decoration:none}.primary.action{min-width:0;padding-inline-start:var(--_leading-space);padding-inline-end:var(--_trailing-space)}.has-icon .primary.action{padding-inline-start:var(--_with-leading-icon-leading-space)}.touch{height:48px;inset:50% 0 0;position:absolute;transform:translateY(-50%);width:100%}:host([touch-target=none]) .touch{display:none}.outline{border:var(--_outline-width) solid var(--_outline-color);border-radius:inherit;inset:0;pointer-events:none;position:absolute}:where(:focus) .outline{border-color:var(--_focus-outline-color)}:where(.disabled) .outline{border-color:var(--_disabled-outline-color);opacity:var(--_disabled-outline-opacity)}md-ripple{border-radius:inherit}.icon,.label,.touch{z-index:1}.label{align-items:center;color:var(--_label-text-color);display:flex;font-family:var(--_label-text-font);font-size:var(--_label-text-size);font-weight:var(--_label-text-weight);height:100%;line-height:var(--_label-text-line-height);overflow:hidden;user-select:none}.label-text{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}:where(:hover) .label{color:var(--_hover-label-text-color)}:where(:focus) .label{color:var(--_focus-label-text-color)}:where(:active) .label{color:var(--_pressed-label-text-color)}:where(.disabled) .label{color:var(--_disabled-label-text-color);opacity:var(--_disabled-label-text-opacity)}.icon{align-self:center;display:flex;fill:currentColor;position:relative}.icon ::slotted(:first-child){font-size:var(--_icon-size);height:var(--_icon-size);width:var(--_icon-size)}.leading.icon{color:var(--_leading-icon-color)}.leading.icon ::slotted(*),.leading.icon svg{margin-inline-end:var(--_icon-label-space)}:where(:hover) .leading.icon{color:var(--_hover-leading-icon-color)}:where(:focus) .leading.icon{color:var(--_focus-leading-icon-color)}:where(:active) .leading.icon{color:var(--_pressed-leading-icon-color)}:where(.disabled) .leading.icon{color:var(--_disabled-leading-icon-color);opacity:var(--_disabled-leading-icon-opacity)}@media(forced-colors:active){:where(.disabled) :is(.label,.outline,.leading.icon){color:GrayText;opacity:1}}a,button{text-transform:inherit}a,button:not(:disabled,[aria-disabled=true]){cursor:inherit}'])))},19260:function(e,t,i){i.d(t,{R:function(){return o}});var a,r=i(64599),o=(0,i(15112).AH)(a||(a=(0,r.A)([".trailing.action{align-items:center;justify-content:center;padding-inline-start:var(--_icon-label-space);padding-inline-end:var(--_with-trailing-icon-trailing-space)}.trailing.action :is(md-ripple,md-focus-ring){border-radius:50%;height:calc(1.3333333333*var(--_icon-size));width:calc(1.3333333333*var(--_icon-size))}.trailing.action md-focus-ring{inset:unset}.has-trailing .primary.action{padding-inline-end:0}.trailing.icon{color:var(--_trailing-icon-color);height:var(--_icon-size);width:var(--_icon-size)}:where(:hover) .trailing.icon{color:var(--_hover-trailing-icon-color)}:where(:focus) .trailing.icon{color:var(--_focus-trailing-icon-color)}:where(:active) .trailing.icon{color:var(--_pressed-trailing-icon-color)}:where(.disabled) .trailing.icon{color:var(--_disabled-trailing-icon-color);opacity:var(--_disabled-trailing-icon-opacity)}:where(.selected) .trailing.icon{color:var(--_selected-trailing-icon-color)}:where(.selected:hover) .trailing.icon{color:var(--_selected-hover-trailing-icon-color)}:where(.selected:focus) .trailing.icon{color:var(--_selected-focus-trailing-icon-color)}:where(.selected:active) .trailing.icon{color:var(--_selected-pressed-trailing-icon-color)}@media(forced-colors:active){.trailing.icon{color:ButtonText}:where(.disabled) .trailing.icon{color:GrayText;opacity:1}}"])))},6288:function(e,t,i){i.d(t,{h:function(){return n}});var a,r=i(64599),o=(i(39299),i(70252),i(15112));function n(e){var t=e.ariaLabel,i=e.disabled,n=e.focusListener,s=e.tabbable,c=void 0!==s&&s;return(0,o.qy)(a||(a=(0,r.A)([' <span id="remove-label" hidden aria-hidden="true">Remove</span> <button class="trailing action" aria-label="','" aria-labelledby="','" tabindex="','" @click="','" @focus="','"> <md-focus-ring part="trailing-focus-ring"></md-focus-ring> <md-ripple ?disabled="','"></md-ripple> <span class="trailing icon" aria-hidden="true"> <slot name="remove-trailing-icon"> <svg viewBox="0 96 960 960"> <path d="m249 849-42-42 231-231-231-231 42-42 231 231 231-231 42 42-231 231 231 231-42 42-231-231-231 231Z"/> </svg> </slot> </span> <span class="touch"></span> </button> '])),t||o.s6,t?o.s6:"remove-label label",c?o.s6:-1,l,n,i)}function l(e){this.disabled||this.softDisabled||(e.stopPropagation(),!this.dispatchEvent(new Event("remove",{cancelable:!0}))||this.remove())}},26604:function(e,t,i){i.d(t,{n:function(){return b}});var a=i(64782),r=i(71008),o=i(35806),n=i(62193),l=i(35890),s=i(2816),c=(i(42942),i(48062),i(95737),i(39790),i(36016),i(74268),i(24545),i(51855),i(82130),i(31743),i(22328),i(4959),i(62435),i(99019),i(43037),i(96858),i(15112)),d=(i(82386),i(97741),i(36604),["role","ariaAtomic","ariaAutoComplete","ariaBusy","ariaChecked","ariaColCount","ariaColIndex","ariaColSpan","ariaCurrent","ariaDisabled","ariaExpanded","ariaHasPopup","ariaHidden","ariaInvalid","ariaKeyShortcuts","ariaLabel","ariaLevel","ariaLive","ariaModal","ariaMultiLine","ariaMultiSelectable","ariaOrientation","ariaPlaceholder","ariaPosInSet","ariaPressed","ariaReadOnly","ariaRequired","ariaRoleDescription","ariaRowCount","ariaRowIndex","ariaRowSpan","ariaSelected","ariaSetSize","ariaSort","ariaValueMax","ariaValueMin","ariaValueNow","ariaValueText"]),u=d.map(v);function h(e){return u.includes(e)}function v(e){return e.replace("aria","aria-").replace(/Elements?/g,"").toLowerCase()}var p=Symbol("privateIgnoreAttributeChangesFor");function b(e){var t;if(c.S$)return e;var i=function(e){function i(){var e;return(0,r.A)(this,i),(e=(0,n.A)(this,i,arguments))[t]=new Set,e}return(0,s.A)(i,e),(0,o.A)(i,[{key:"attributeChangedCallback",value:function(e,t,a){if(h(e)){if(!this[p].has(e)){this[p].add(e),this.removeAttribute(e),this[p].delete(e);var r=g(e);null===a?delete this.dataset[r]:this.dataset[r]=a,this.requestUpdate(g(e),t)}}else(0,l.A)(i,"attributeChangedCallback",this,3)([e,t,a])}},{key:"getAttribute",value:function(e){return h(e)?(0,l.A)(i,"getAttribute",this,3)([f(e)]):(0,l.A)(i,"getAttribute",this,3)([e])}},{key:"removeAttribute",value:function(e){(0,l.A)(i,"removeAttribute",this,3)([e]),h(e)&&((0,l.A)(i,"removeAttribute",this,3)([f(e)]),this.requestUpdate())}}])}(e);return t=p,function(e){var t,i=(0,a.A)(d);try{var r=function(){var i=t.value,a=v(i),r=f(a),o=g(a);e.createProperty(i,{attribute:a,noAccessor:!0}),e.createProperty(Symbol(r),{attribute:r,noAccessor:!0}),Object.defineProperty(e.prototype,i,{configurable:!0,enumerable:!0,get:function(){var e;return null!==(e=this.dataset[o])&&void 0!==e?e:null},set:function(e){var t,a=null!==(t=this.dataset[o])&&void 0!==t?t:null;e!==a&&(null===e?delete this.dataset[o]:this.dataset[o]=e,this.requestUpdate(i,a))}})};for(i.s();!(t=i.n()).done;)r()}catch(o){i.e(o)}finally{i.f()}}(i),i}function f(e){return"data-".concat(e)}function g(e){return e.replace(/-\w/,(function(e){return e[1].toUpperCase()}))}}}]);
//# sourceMappingURL=71893.Ph5LlUfy5jw.js.map