(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[94197],{90410:function(e,t,i){"use strict";i.d(t,{ZS:function(){return m},is:function(){return f.i}});var n,a,o=i(71008),r=i(35806),s=i(62193),l=i(35890),d=i(2816),c=(i(52427),i(99019),i(79192)),u=i(29818),f=i(19637),h=null!==(a=null===(n=window.ShadyDOM)||void 0===n?void 0:n.inUse)&&void 0!==a&&a,m=function(e){function t(){var e;return(0,o.A)(this,t),(e=(0,s.A)(this,t,arguments)).disabled=!1,e.containingForm=null,e.formDataListener=function(t){e.disabled||e.setFormData(t.formData)},e}return(0,d.A)(t,e),(0,r.A)(t,[{key:"findFormElement",value:function(){if(!this.shadowRoot||h)return null;for(var e=this.getRootNode().querySelectorAll("form"),t=0,i=Array.from(e);t<i.length;t++){var n=i[t];if(n.contains(this))return n}return null}},{key:"connectedCallback",value:function(){var e;(0,l.A)(t,"connectedCallback",this,3)([]),this.containingForm=this.findFormElement(),null===(e=this.containingForm)||void 0===e||e.addEventListener("formdata",this.formDataListener)}},{key:"disconnectedCallback",value:function(){var e;(0,l.A)(t,"disconnectedCallback",this,3)([]),null===(e=this.containingForm)||void 0===e||e.removeEventListener("formdata",this.formDataListener),this.containingForm=null}},{key:"click",value:function(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}},{key:"firstUpdated",value:function(){var e=this;(0,l.A)(t,"firstUpdated",this,3)([]),this.shadowRoot&&this.mdcRoot.addEventListener("change",(function(t){e.dispatchEvent(new Event("change",t))}))}}])}(f.O);m.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,c.__decorate)([(0,u.MZ)({type:Boolean})],m.prototype,"disabled",void 0)},54838:function(e,t,i){"use strict";i.r(t),i.d(t,{Button:function(){return u}});var n=i(35806),a=i(71008),o=i(62193),r=i(2816),s=i(79192),l=i(29818),d=i(3238),c=i(49141),u=function(e){function t(){return(0,a.A)(this,t),(0,o.A)(this,t,arguments)}return(0,r.A)(t,e),(0,n.A)(t)}(d.u);u.styles=[c.R],u=(0,s.__decorate)([(0,l.EM)("mwc-button")],u)},37136:function(e,t,i){"use strict";i.d(t,{M:function(){return A}});var n,a=i(64599),o=i(33994),r=i(22858),s=i(71008),l=i(35806),d=i(62193),c=i(2816),u=i(79192),f=i(11468),h={ROOT:"mdc-form-field"},m={LABEL_SELECTOR:".mdc-form-field > label"},p=function(e){function t(i){var n=e.call(this,(0,u.__assign)((0,u.__assign)({},t.defaultAdapter),i))||this;return n.click=function(){n.handleClick()},n}return(0,u.__extends)(t,e),Object.defineProperty(t,"cssClasses",{get:function(){return h},enumerable:!1,configurable:!0}),Object.defineProperty(t,"strings",{get:function(){return m},enumerable:!1,configurable:!0}),Object.defineProperty(t,"defaultAdapter",{get:function(){return{activateInputRipple:function(){},deactivateInputRipple:function(){},deregisterInteractionHandler:function(){},registerInteractionHandler:function(){}}},enumerable:!1,configurable:!0}),t.prototype.init=function(){this.adapter.registerInteractionHandler("click",this.click)},t.prototype.destroy=function(){this.adapter.deregisterInteractionHandler("click",this.click)},t.prototype.handleClick=function(){var e=this;this.adapter.activateInputRipple(),requestAnimationFrame((function(){e.adapter.deactivateInputRipple()}))},t}(f.I),g=i(19637),v=i(90410),y=i(54279),b=i(15112),k=i(29818),_=i(85323),A=function(e){function t(){var e;return(0,s.A)(this,t),(e=(0,d.A)(this,t,arguments)).alignEnd=!1,e.spaceBetween=!1,e.nowrap=!1,e.label="",e.mdcFoundationClass=p,e}return(0,c.A)(t,e),(0,l.A)(t,[{key:"createAdapter",value:function(){var e,t,i=this;return{registerInteractionHandler:function(e,t){i.labelEl.addEventListener(e,t)},deregisterInteractionHandler:function(e,t){i.labelEl.removeEventListener(e,t)},activateInputRipple:(t=(0,r.A)((0,o.A)().mark((function e(){var t,n;return(0,o.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!((t=i.input)instanceof v.ZS)){e.next=6;break}return e.next=4,t.ripple;case 4:(n=e.sent)&&n.startPress();case 6:case"end":return e.stop()}}),e)}))),function(){return t.apply(this,arguments)}),deactivateInputRipple:(e=(0,r.A)((0,o.A)().mark((function e(){var t,n;return(0,o.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!((t=i.input)instanceof v.ZS)){e.next=6;break}return e.next=4,t.ripple;case 4:(n=e.sent)&&n.endPress();case 6:case"end":return e.stop()}}),e)}))),function(){return e.apply(this,arguments)})}}},{key:"input",get:function(){var e,t;return null!==(t=null===(e=this.slottedInputs)||void 0===e?void 0:e[0])&&void 0!==t?t:null}},{key:"render",value:function(){var e={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return(0,b.qy)(n||(n=(0,a.A)([' <div class="mdc-form-field ','"> <slot></slot> <label class="mdc-label" @click="','">',"</label> </div>"])),(0,_.H)(e),this._labelClick,this.label)}},{key:"click",value:function(){this._labelClick()}},{key:"_labelClick",value:function(){var e=this.input;e&&(e.focus(),e.click())}}])}(g.O);(0,u.__decorate)([(0,k.MZ)({type:Boolean})],A.prototype,"alignEnd",void 0),(0,u.__decorate)([(0,k.MZ)({type:Boolean})],A.prototype,"spaceBetween",void 0),(0,u.__decorate)([(0,k.MZ)({type:Boolean})],A.prototype,"nowrap",void 0),(0,u.__decorate)([(0,k.MZ)({type:String}),(0,y.P)(function(){var e=(0,r.A)((0,o.A)().mark((function e(t){var i;return(0,o.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:null===(i=this.input)||void 0===i||i.setAttribute("aria-label",t);case 1:case"end":return e.stop()}}),e,this)})));return function(t){return e.apply(this,arguments)}}())],A.prototype,"label",void 0),(0,u.__decorate)([(0,k.P)(".mdc-form-field")],A.prototype,"mdcRoot",void 0),(0,u.__decorate)([(0,k.gZ)("",!0,"*")],A.prototype,"slottedInputs",void 0),(0,u.__decorate)([(0,k.P)("label")],A.prototype,"labelEl",void 0)},18881:function(e,t,i){"use strict";i.d(t,{R:function(){return o}});var n,a=i(64599),o=(0,i(15112).AH)(n||(n=(0,a.A)([".mdc-form-field{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto,sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:.875rem;font-size:var(--mdc-typography-body2-font-size, .875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight,400);letter-spacing:.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, .0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration,inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform,inherit);color:rgba(0,0,0,.87);color:var(--mdc-theme-text-primary-on-background,rgba(0,0,0,.87));display:inline-flex;align-items:center;vertical-align:middle}.mdc-form-field>label{margin-left:0;margin-right:auto;padding-left:4px;padding-right:0;order:0}.mdc-form-field>label[dir=rtl],[dir=rtl] .mdc-form-field>label{margin-left:auto;margin-right:0}.mdc-form-field>label[dir=rtl],[dir=rtl] .mdc-form-field>label{padding-left:0;padding-right:4px}.mdc-form-field--nowrap>label{text-overflow:ellipsis;overflow:hidden;white-space:nowrap}.mdc-form-field--align-end>label{margin-left:auto;margin-right:0;padding-left:0;padding-right:4px;order:-1}.mdc-form-field--align-end>label[dir=rtl],[dir=rtl] .mdc-form-field--align-end>label{margin-left:0;margin-right:auto}.mdc-form-field--align-end>label[dir=rtl],[dir=rtl] .mdc-form-field--align-end>label{padding-left:4px;padding-right:0}.mdc-form-field--space-between{justify-content:space-between}.mdc-form-field--space-between>label{margin:0}.mdc-form-field--space-between>label[dir=rtl],[dir=rtl] .mdc-form-field--space-between>label{margin:0}:host{display:inline-flex}.mdc-form-field{width:100%}::slotted(*){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto,sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:.875rem;font-size:var(--mdc-typography-body2-font-size, .875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight,400);letter-spacing:.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, .0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration,inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform,inherit);color:rgba(0,0,0,.87);color:var(--mdc-theme-text-primary-on-background,rgba(0,0,0,.87))}::slotted(mwc-switch){margin-right:10px}::slotted(mwc-switch[dir=rtl]),[dir=rtl] ::slotted(mwc-switch){margin-left:10px}"])))},68365:function(e,t,i){"use strict";i.d(t,{N:function(){return l}});var n=i(64782),a=i(35806),o=i(71008),r=(i(42942),i(48062),i(52427),i(39805),i(95737),i(33231),i(50693),i(39790),i(74268),i(24545),i(51855),i(82130),i(31743),i(22328),i(4959),i(62435),i(99019),i(96858),Symbol("selection controller")),s=(0,a.A)((function e(){(0,o.A)(this,e),this.selected=null,this.ordered=null,this.set=new Set})),l=function(){function e(t){var i=this;(0,o.A)(this,e),this.sets={},this.focusedSet=null,this.mouseIsDown=!1,this.updating=!1,t.addEventListener("keydown",(function(e){i.keyDownHandler(e)})),t.addEventListener("mousedown",(function(){i.mousedownHandler()})),t.addEventListener("mouseup",(function(){i.mouseupHandler()}))}return(0,a.A)(e,[{key:"keyDownHandler",value:function(e){var t=e.target;"checked"in t&&this.has(t)&&("ArrowRight"==e.key||"ArrowDown"==e.key?this.selectNext(t):"ArrowLeft"!=e.key&&"ArrowUp"!=e.key||this.selectPrevious(t))}},{key:"mousedownHandler",value:function(){this.mouseIsDown=!0}},{key:"mouseupHandler",value:function(){this.mouseIsDown=!1}},{key:"has",value:function(e){return this.getSet(e.name).set.has(e)}},{key:"selectPrevious",value:function(e){var t=this.getOrdered(e),i=t.indexOf(e),n=t[i-1]||t[t.length-1];return this.select(n),n}},{key:"selectNext",value:function(e){var t=this.getOrdered(e),i=t.indexOf(e),n=t[i+1]||t[0];return this.select(n),n}},{key:"select",value:function(e){e.click()}},{key:"focus",value:function(e){if(!this.mouseIsDown){var t=this.getSet(e.name),i=this.focusedSet;this.focusedSet=t,i!=t&&t.selected&&t.selected!=e&&t.selected.focus()}}},{key:"isAnySelected",value:function(e){var t,i=this.getSet(e.name),a=(0,n.A)(i.set);try{for(a.s();!(t=a.n()).done;){if(t.value.checked)return!0}}catch(o){a.e(o)}finally{a.f()}return!1}},{key:"getOrdered",value:function(e){var t=this.getSet(e.name);return t.ordered||(t.ordered=Array.from(t.set),t.ordered.sort((function(e,t){return e.compareDocumentPosition(t)==Node.DOCUMENT_POSITION_PRECEDING?1:0}))),t.ordered}},{key:"getSet",value:function(e){return this.sets[e]||(this.sets[e]=new s),this.sets[e]}},{key:"register",value:function(e){var t=e.name||e.getAttribute("name")||"",i=this.getSet(t);i.set.add(e),i.ordered=null}},{key:"unregister",value:function(e){var t=this.getSet(e.name);t.set.delete(e),t.ordered=null,t.selected==e&&(t.selected=null)}},{key:"update",value:function(e){if(!this.updating){this.updating=!0;var t=this.getSet(e.name);if(e.checked){var i,a=(0,n.A)(t.set);try{for(a.s();!(i=a.n()).done;){var o=i.value;o!=e&&(o.checked=!1)}}catch(d){a.e(d)}finally{a.f()}t.selected=e}if(this.isAnySelected(e)){var r,s=(0,n.A)(t.set);try{for(s.s();!(r=s.n()).done;){var l=r.value;if(void 0===l.formElementTabIndex)break;l.formElementTabIndex=l.checked?0:-1}}catch(d){s.e(d)}finally{s.f()}}this.updating=!1}}}],[{key:"getController",value:function(t){var i=!("global"in t)||"global"in t&&t.global?document:t.getRootNode(),n=i[r];return void 0===n&&(n=new e(i),i[r]=n),n}}])}()},3276:function(e,t,i){"use strict";i.d(t,{l:function(){return b}});var n,a,o,r=i(35806),s=i(71008),l=i(62193),d=i(2816),c=i(27927),u=i(35890),f=i(64599),h=(i(71522),i(81027),i(79243),i(54653)),m=i(34599),p=i(15112),g=i(29818),v=i(90952),y=(i(28066),["button","ha-list-item"]),b=function(e,t){var i;return(0,p.qy)(n||(n=(0,f.A)([' <div class="header_title"> <span>','</span> <ha-icon-button .label="','" .path="','" dialogAction="close" class="header_button"></ha-icon-button> </div> '])),t,null!==(i=null==e?void 0:e.localize("ui.dialogs.generic.close"))&&void 0!==i?i:"Close","M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z")};(0,c.A)([(0,g.EM)("ha-dialog")],(function(e,t){var i=function(t){function i(){var t;(0,s.A)(this,i);for(var n=arguments.length,a=new Array(n),o=0;o<n;o++)a[o]=arguments[o];return t=(0,l.A)(this,i,[].concat(a)),e(t),t}return(0,d.A)(i,t),(0,r.A)(i)}(t);return{F:i,d:[{kind:"field",key:v.Xr,value:void 0},{kind:"method",key:"scrollToPos",value:function(e,t){var i;null===(i=this.contentElement)||void 0===i||i.scrollTo(e,t)}},{kind:"method",key:"renderHeading",value:function(){return(0,p.qy)(a||(a=(0,f.A)(['<slot name="heading"> '," </slot>"])),(0,u.A)(i,"renderHeading",this,3)([]))}},{kind:"method",key:"firstUpdated",value:function(){var e;(0,u.A)(i,"firstUpdated",this,3)([]),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,y].join(", "),this._updateScrolledAttribute(),null===(e=this.contentElement)||void 0===e||e.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,u.A)(i,"disconnectedCallback",this,3)([]),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value:function(){var e=this;return function(){e._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value:function(){return[m.R,(0,p.AH)(o||(o=(0,f.A)([":host([scrolled]) ::slotted(ha-dialog-header){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.mdc-dialog{--mdc-dialog-scroll-divider-color:var(\n          --dialog-scroll-divider-color,\n          var(--divider-color)\n        );z-index:var(--dialog-z-index,8);-webkit-backdrop-filter:var(--ha-dialog-scrim-backdrop-filter,var(--dialog-backdrop-filter,none));backdrop-filter:var(--ha-dialog-scrim-backdrop-filter,var(--dialog-backdrop-filter,none));--mdc-dialog-box-shadow:var(--dialog-box-shadow, none);--mdc-typography-headline6-font-weight:400;--mdc-typography-headline6-font-size:1.574rem}.mdc-dialog__actions{justify-content:var(--justify-action-buttons,flex-end);padding-bottom:max(env(safe-area-inset-bottom),24px)}.mdc-dialog__actions span:first-child{flex:var(--secondary-action-button-flex,unset)}.mdc-dialog__actions span:nth-child(2){flex:var(--primary-action-button-flex,unset)}.mdc-dialog__container{align-items:var(--vertical-align-dialog,center)}.mdc-dialog__title{padding:24px 24px 0 24px}.mdc-dialog__actions{padding:12px 24px 12px 24px}.mdc-dialog__title::before{content:unset}.mdc-dialog .mdc-dialog__content{position:var(--dialog-content-position,relative);padding:var(--dialog-content-padding,24px)}:host([hideactions]) .mdc-dialog .mdc-dialog__content{padding-bottom:max(var(--dialog-content-padding,24px),env(safe-area-inset-bottom))}.mdc-dialog .mdc-dialog__surface{position:var(--dialog-surface-position,relative);top:var(--dialog-surface-top);margin-top:var(--dialog-surface-margin-top);min-height:var(--mdc-dialog-min-height,auto);border-radius:var(--ha-dialog-border-radius,28px);-webkit-backdrop-filter:var(--ha-dialog-surface-backdrop-filter,none);backdrop-filter:var(--ha-dialog-surface-backdrop-filter,none);background:var(--ha-dialog-surface-background,var(--mdc-theme-surface,#fff))}:host([flexContent]) .mdc-dialog .mdc-dialog__content{display:flex;flex-direction:column}.header_title{position:relative;padding-right:40px;padding-inline-end:40px;padding-inline-start:initial;direction:var(--direction)}.header_title span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:block}.header_button{position:absolute;right:-12px;top:-12px;text-decoration:none;color:inherit;inset-inline-start:initial;inset-inline-end:-12px;direction:var(--direction)}.dialog-actions{inset-inline-start:initial!important;inset-inline-end:0px!important;direction:var(--direction)}"])))]}}]}}),h.u)},24284:function(e,t,i){"use strict";var n,a,o=i(64599),r=i(35806),s=i(71008),l=i(62193),d=i(2816),c=i(27927),u=(i(81027),i(37136)),f=i(18881),h=i(15112),m=i(29818),p=i(85323),g=i(34897);(0,c.A)([(0,m.EM)("ha-formfield")],(function(e,t){var i=function(t){function i(){var t;(0,s.A)(this,i);for(var n=arguments.length,a=new Array(n),o=0;o<n;o++)a[o]=arguments[o];return t=(0,l.A)(this,i,[].concat(a)),e(t),t}return(0,d.A)(i,t),(0,r.A)(i)}(t);return{F:i,d:[{kind:"field",decorators:[(0,m.MZ)({type:Boolean,reflect:!0})],key:"disabled",value:function(){return!1}},{kind:"method",key:"render",value:function(){var e={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return(0,h.qy)(n||(n=(0,o.A)([' <div class="mdc-form-field ','"> <slot></slot> <label class="mdc-label" @click="','"> <slot name="label">',"</slot> </label> </div>"])),(0,p.H)(e),this._labelClick,this.label)}},{kind:"method",key:"_labelClick",value:function(){var e=this.input;if(e&&(e.focus(),!e.disabled))switch(e.tagName){case"HA-CHECKBOX":e.checked=!e.checked,(0,g.r)(e,"change");break;case"HA-RADIO":e.checked=!0,(0,g.r)(e,"change");break;default:e.click()}}},{kind:"field",static:!0,key:"styles",value:function(){return[f.R,(0,h.AH)(a||(a=(0,o.A)([":host(:not([alignEnd])) ::slotted(ha-switch){margin-right:10px;margin-inline-end:10px;margin-inline-start:inline}.mdc-form-field{align-items:var(--ha-formfield-align-items,center);gap:4px}.mdc-form-field>label{direction:var(--direction);margin-inline-start:0;margin-inline-end:auto;padding:0}:host([disabled]) label{color:var(--disabled-text-color)}"])))]}}]}}),u.M)},51513:function(e,t,i){"use strict";var n,a=i(64599),o=i(35806),r=i(71008),s=i(62193),l=i(2816),d=i(27927),c=(i(81027),i(35351)),u=i(37749),f=i(15112),h=i(29818);(0,d.A)([(0,h.EM)("ha-radio")],(function(e,t){var i=function(t){function i(){var t;(0,r.A)(this,i);for(var n=arguments.length,a=new Array(n),o=0;o<n;o++)a[o]=arguments[o];return t=(0,s.A)(this,i,[].concat(a)),e(t),t}return(0,l.A)(i,t),(0,o.A)(i)}(t);return{F:i,d:[{kind:"field",static:!0,key:"styles",value:function(){return[u.R,(0,f.AH)(n||(n=(0,a.A)([":host{--mdc-theme-secondary:var(--primary-color)}"])))]}}]}}),c.F)},55705:function(e,t,i){"use strict";i.r(t),i.d(t,{DialogStatisticsFixUnitsChanged:function(){return v}});var n,a=i(33994),o=i(22858),r=i(64599),s=i(35806),l=i(71008),d=i(62193),c=i(2816),u=i(27927),f=(i(81027),i(54838),i(15112)),h=i(29818),m=i(34897),p=(i(3276),i(24284),i(51513),i(4826)),g=i(55321),v=(0,u.A)([(0,h.EM)("dialog-statistics-fix-units-changed")],(function(e,t){var i,u=function(t){function i(){var t;(0,l.A)(this,i);for(var n=arguments.length,a=new Array(n),o=0;o<n;o++)a[o]=arguments[o];return t=(0,d.A)(this,i,[].concat(a)),e(t),t}return(0,c.A)(i,t),(0,s.A)(i)}(t);return{F:u,d:[{kind:"field",decorators:[(0,h.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,h.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,h.wk)()],key:"_action",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._action="update"}},{kind:"method",key:"closeDialog",value:function(){this._cancel()}},{kind:"method",key:"_closeDialog",value:function(){this._params=void 0,this._action=void 0,(0,m.r)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return this._params?(0,f.qy)(n||(n=(0,r.A)([' <ha-dialog open scrimClickAction escapeKeyAction @closed="','" .heading="','"> <p> ',"<br> ","<br> "," </p> <h3> ",' </h3> <ha-formfield .label="','"> <ha-radio value="update" name="action" .checked="','" @change="','" dialogInitialFocus></ha-radio> </ha-formfield> <ha-formfield .label="','"> <ha-radio value="clear" name="action" .checked="','" @change="','"></ha-radio> </ha-formfield> <mwc-button slot="primaryAction" @click="','"> ',' </mwc-button> <mwc-button slot="secondaryAction" @click="','"> '," </mwc-button> </ha-dialog> "])),this._closeDialog,this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.units_changed.title"),this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.units_changed.info_text_1",{name:(0,p.$O)(this.hass,this._params.issue.data.statistic_id,void 0),statistic_id:this._params.issue.data.statistic_id,current_unit:this._params.issue.data.state_unit,previous_unit:this._params.issue.data.metadata_unit}),this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.units_changed.info_text_2"),this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.units_changed.info_text_3"),this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.units_changed.how_to_fix"),this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.units_changed.update",this._params.issue.data),"update"===this._action,this._handleActionChanged,this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.units_changed.clear"),"clear"===this._action,this._handleActionChanged,this._fixIssue,this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.fix"),this._cancel,this.hass.localize("ui.common.close")):f.s6}},{kind:"method",key:"_handleActionChanged",value:function(e){this._action=e.target.value}},{kind:"method",key:"_cancel",value:function(){var e;null===(e=this._params)||void 0===e||e.cancelCallback(),this._closeDialog()}},{kind:"method",key:"_fixIssue",value:(i=(0,o.A)((0,a.A)().mark((function e(){var t;return(0,a.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if("clear"!==this._action){e.next=5;break}return e.next=3,(0,p.$3)(this.hass,[this._params.issue.data.statistic_id]);case 3:e.next=8;break;case 5:if("update"!==this._action){e.next=8;break}return e.next=8,(0,p.W1)(this.hass,this._params.issue.data.statistic_id,this._params.issue.data.state_unit);case 8:null===(t=this._params)||void 0===t||t.fixedCallback(),this._closeDialog();case 10:case"end":return e.stop()}}),e,this)}))),function(){return i.apply(this,arguments)})},{kind:"get",static:!0,key:"styles",value:function(){return[g.RF,g.nA]}}]}}),f.WF)},71522:function(){Element.prototype.toggleAttribute||(Element.prototype.toggleAttribute=function(e,t){return void 0!==t&&(t=!!t),this.hasAttribute(e)?!!t||(this.removeAttribute(e),!1):!1!==t&&(this.setAttribute(e,""),!0)})}}]);
//# sourceMappingURL=94197.vTrZDAAZ23A.js.map