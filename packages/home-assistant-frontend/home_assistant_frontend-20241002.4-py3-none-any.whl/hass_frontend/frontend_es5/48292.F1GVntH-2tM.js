(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[48292],{88725:function(e,t,i){"use strict";var n,r=i(64599),a=i(35806),o=i(71008),d=i(62193),s=i(2816),l=i(27927),c=(i(81027),i(41204)),u=i(15565),h=i(15112),p=i(29818);(0,l.A)([(0,p.EM)("ha-checkbox")],(function(e,t){var i=function(t){function i(){var t;(0,o.A)(this,i);for(var n=arguments.length,r=new Array(n),a=0;a<n;a++)r[a]=arguments[a];return t=(0,d.A)(this,i,[].concat(r)),e(t),t}return(0,s.A)(i,t),(0,a.A)(i)}(t);return{F:i,d:[{kind:"field",static:!0,key:"styles",value:function(){return[u.R,(0,h.AH)(n||(n=(0,r.A)([":host{--mdc-theme-secondary:var(--primary-color)}"])))]}}]}}),c.L)},32172:function(e,t,i){"use strict";var n,r=i(33994),a=i(41981),o=i(22858),d=i(35806),s=i(71008),l=i(62193),c=i(2816),u=i(27927),h=i(35890),p=i(14369),f=(i(64017),i(81027),i(13025),i(52427),i(82386),i(95737),i(79243),i(97741),i(46469),i(18193),i(39790),i(66457),i(36016),i(36604),i(99019),i(253),i(2075),i(16891),i(37679),i(96858),i(15112)),m=i(29818),v=i(34897),g=(i(84341),i(49365),i(38389),i(74860),i(71011),i(71174),i(36575)),k=function(){var e=(0,o.A)((0,r.A)().mark((function e(t,a,o){return(0,r.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return n||(n=(0,g.LV)(new Worker(new URL(i.p+i.u(17131),i.b)))),e.abrupt("return",n.renderMarkdown(t,a,o));case 2:case"end":return e.stop()}}),e)})));return function(t,i,n){return e.apply(this,arguments)}}(),y={reType:(0,p.A)(/((\[!(caution|important|note|tip|warning)\])(?:\s|\\n)?)/i,{input:1,type:3}),typeToHaAlert:{caution:"error",important:"info",note:"info",tip:"success",warning:"warning"}};(0,u.A)([(0,m.EM)("ha-markdown-element")],(function(e,t){var n,u=function(t){function i(){var t;(0,s.A)(this,i);for(var n=arguments.length,r=new Array(n),a=0;a<n;a++)r[a]=arguments[a];return t=(0,l.A)(this,i,[].concat(r)),e(t),t}return(0,c.A)(i,t),(0,d.A)(i)}(t);return{F:u,d:[{kind:"field",decorators:[(0,m.MZ)()],key:"content",value:void 0},{kind:"field",decorators:[(0,m.MZ)({type:Boolean})],key:"allowSvg",value:function(){return!1}},{kind:"field",decorators:[(0,m.MZ)({type:Boolean})],key:"breaks",value:function(){return!1}},{kind:"field",decorators:[(0,m.MZ)({type:Boolean,attribute:"lazy-images"})],key:"lazyImages",value:function(){return!1}},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"method",key:"update",value:function(e){(0,h.A)(u,"update",this,3)([e]),void 0!==this.content&&this._render()}},{kind:"method",key:"_render",value:(n=(0,o.A)((0,r.A)().mark((function e(){var t,n,o=this;return(0,r.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,k(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg});case 2:this.innerHTML=e.sent,this._resize(),t=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null),n=(0,r.A)().mark((function e(){var n,d,s,l,c,u;return(0,r.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:(n=t.currentNode)instanceof HTMLAnchorElement&&n.host!==document.location.host?(n.target="_blank",n.rel="noreferrer noopener"):n instanceof HTMLImageElement?(o.lazyImages&&(n.loading="lazy"),n.addEventListener("load",o._resize)):n instanceof HTMLQuoteElement?(s=(null===(d=n.firstElementChild)||void 0===d||null===(d=d.firstChild)||void 0===d?void 0:d.textContent)&&y.reType.exec(n.firstElementChild.firstChild.textContent))&&(l=s.groups,c=l.type,(u=document.createElement("ha-alert")).alertType=y.typeToHaAlert[c.toLowerCase()],u.append.apply(u,(0,a.A)(Array.from(n.childNodes).map((function(e){var t=Array.from(e.childNodes);if(!o.breaks&&t.length){var i,n=t[0];n.nodeType===Node.TEXT_NODE&&n.textContent===s.input&&null!==(i=n.textContent)&&void 0!==i&&i.includes("\n")&&(n.textContent=n.textContent.split("\n").slice(1).join("\n"))}return t})).reduce((function(e,t){return e.concat(t)}),[]).filter((function(e){return e.textContent&&e.textContent!==s.input})))),t.parentNode().replaceChild(u,n)):n instanceof HTMLElement&&["ha-alert","ha-qr-code","ha-icon","ha-svg-icon"].includes(n.localName)&&i(75402)("./".concat(n.localName));case 2:case"end":return e.stop()}}),e)}));case 6:if(!t.nextNode()){e.next=10;break}return e.delegateYield(n(),"t0",8);case 8:e.next=6;break;case 10:case"end":return e.stop()}}),e,this)}))),function(){return n.apply(this,arguments)})},{kind:"field",key:"_resize",value:function(){var e=this;return function(){return(0,v.r)(e,"content-resize")}}}]}}),f.mN)},77312:function(e,t,i){"use strict";var n,r,a,o,d=i(33994),s=i(22858),l=i(64599),c=i(35806),u=i(71008),h=i(62193),p=i(2816),f=i(27927),m=i(35890),v=(i(81027),i(24500)),g=i(14691),k=i(15112),y=i(29818),_=i(18409),x=i(61441);i(28066),(0,f.A)([(0,y.EM)("ha-select")],(function(e,t){var i=function(t){function i(){var t;(0,u.A)(this,i);for(var n=arguments.length,r=new Array(n),a=0;a<n;a++)r[a]=arguments[a];return t=(0,h.A)(this,i,[].concat(r)),e(t),t}return(0,p.A)(i,t),(0,c.A)(i)}(t);return{F:i,d:[{kind:"field",decorators:[(0,y.MZ)({type:Boolean})],key:"icon",value:function(){return!1}},{kind:"field",decorators:[(0,y.MZ)({type:Boolean,reflect:!0})],key:"clearable",value:function(){return!1}},{kind:"method",key:"render",value:function(){return(0,k.qy)(n||(n=(0,l.A)([" "," "," "])),(0,m.A)(i,"render",this,3)([]),this.clearable&&!this.required&&!this.disabled&&this.value?(0,k.qy)(r||(r=(0,l.A)(['<ha-icon-button label="clear" @click="','" .path="','"></ha-icon-button>'])),this._clearValue,"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"):k.s6)}},{kind:"method",key:"renderLeadingIcon",value:function(){return this.icon?(0,k.qy)(a||(a=(0,l.A)(['<span class="mdc-select__icon"><slot name="icon"></slot></span>']))):k.s6}},{kind:"method",key:"connectedCallback",value:function(){(0,m.A)(i,"connectedCallback",this,3)([]),window.addEventListener("translations-updated",this._translationsUpdated)}},{kind:"method",key:"disconnectedCallback",value:function(){(0,m.A)(i,"disconnectedCallback",this,3)([]),window.removeEventListener("translations-updated",this._translationsUpdated)}},{kind:"method",key:"_clearValue",value:function(){!this.disabled&&this.value&&(this.valueSetDirectly=!0,this.select(-1),this.mdcFoundation.handleChange())}},{kind:"field",key:"_translationsUpdated",value:function(){var e=this;return(0,_.s)((0,s.A)((0,d.A)().mark((function t(){return(0,d.A)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,(0,x.E)();case 2:e.layoutOptions();case 3:case"end":return t.stop()}}),t)}))),500)}},{kind:"field",static:!0,key:"styles",value:function(){return[g.R,(0,k.AH)(o||(o=(0,l.A)([":host([clearable]){position:relative}.mdc-select:not(.mdc-select--disabled) .mdc-select__icon{color:var(--secondary-text-color)}.mdc-select__anchor{width:var(--ha-select-min-width,200px)}.mdc-select--filled .mdc-select__anchor{height:var(--ha-select-height,56px)}.mdc-select--filled .mdc-floating-label{inset-inline-start:12px;inset-inline-end:initial;direction:var(--direction)}.mdc-select--filled.mdc-select--with-leading-icon .mdc-floating-label{inset-inline-start:48px;inset-inline-end:initial;direction:var(--direction)}.mdc-select .mdc-select__anchor{padding-inline-start:12px;padding-inline-end:0px;direction:var(--direction)}.mdc-select__anchor .mdc-floating-label--float-above{transform-origin:var(--float-start)}.mdc-select__selected-text-container{padding-inline-end:var(--select-selected-text-padding-end,0px)}:host([clearable]) .mdc-select__selected-text-container{padding-inline-end:var(--select-selected-text-padding-end,12px)}ha-icon-button{position:absolute;top:10px;right:28px;--mdc-icon-button-size:36px;--mdc-icon-size:20px;color:var(--secondary-text-color);inset-inline-start:initial;inset-inline-end:28px;direction:var(--direction)}"])))]}}]}}),v.o)},24260:function(e,t,i){"use strict";var n,r=i(33994),a=i(22858),o=i(64599),d=i(35806),s=i(71008),l=i(62193),c=i(2816),u=i(27927),h=i(35890),p=(i(81027),i(13025),i(95737),i(79243),i(26098),i(39790),i(66457),i(99019),i(12073),i(253),i(2075),i(96858),i(15112)),f=i(29818),m=i(34897);(0,u.A)([(0,f.EM)("ha-sortable")],(function(e,t){var u,v=function(t){function i(){var t;(0,s.A)(this,i);for(var n=arguments.length,r=new Array(n),a=0;a<n;a++)r[a]=arguments[a];return t=(0,l.A)(this,i,[].concat(r)),e(t),t}return(0,c.A)(i,t),(0,d.A)(i)}(t);return{F:v,d:[{kind:"field",key:"_sortable",value:void 0},{kind:"field",decorators:[(0,f.MZ)({type:Boolean})],key:"disabled",value:function(){return!1}},{kind:"field",decorators:[(0,f.MZ)({type:Array})],key:"path",value:void 0},{kind:"field",decorators:[(0,f.MZ)({type:Boolean,attribute:"no-style"})],key:"noStyle",value:function(){return!1}},{kind:"field",decorators:[(0,f.MZ)({type:String,attribute:"draggable-selector"})],key:"draggableSelector",value:void 0},{kind:"field",decorators:[(0,f.MZ)({type:String,attribute:"handle-selector"})],key:"handleSelector",value:void 0},{kind:"field",decorators:[(0,f.MZ)({type:String,attribute:"filter"})],key:"filter",value:void 0},{kind:"field",decorators:[(0,f.MZ)({type:String})],key:"group",value:void 0},{kind:"field",decorators:[(0,f.MZ)({type:Boolean,attribute:"invert-swap"})],key:"invertSwap",value:function(){return!1}},{kind:"field",decorators:[(0,f.MZ)({attribute:!1})],key:"options",value:void 0},{kind:"field",decorators:[(0,f.MZ)({type:Boolean})],key:"rollback",value:function(){return!0}},{kind:"method",key:"updated",value:function(e){e.has("disabled")&&(this.disabled?this._destroySortable():this._createSortable())}},{kind:"field",key:"_shouldBeDestroy",value:function(){return!1}},{kind:"method",key:"disconnectedCallback",value:function(){var e=this;(0,h.A)(v,"disconnectedCallback",this,3)([]),this._shouldBeDestroy=!0,setTimeout((function(){e._shouldBeDestroy&&(e._destroySortable(),e._shouldBeDestroy=!1)}),1)}},{kind:"method",key:"connectedCallback",value:function(){(0,h.A)(v,"connectedCallback",this,3)([]),this._shouldBeDestroy=!1,this.hasUpdated&&!this.disabled&&this._createSortable()}},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"method",key:"render",value:function(){return this.noStyle?p.s6:(0,p.qy)(n||(n=(0,o.A)([" <style>.sortable-fallback{display:none!important}.sortable-ghost{box-shadow:0 0 0 2px var(--primary-color);background:rgba(var(--rgb-primary-color),.25);border-radius:4px;opacity:.4}.sortable-drag{border-radius:4px;opacity:1;background:var(--card-background-color);box-shadow:0px 4px 8px 3px #00000026;cursor:grabbing}</style> "])))}},{kind:"method",key:"_createSortable",value:(u=(0,a.A)((0,r.A)().mark((function e(){var t,n,a;return(0,r.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!this._sortable){e.next=2;break}return e.abrupt("return");case 2:if(t=this.children[0]){e.next=5;break}return e.abrupt("return");case 5:return e.next=7,Promise.all([i.e(35436),i.e(44515)]).then(i.bind(i,44515));case 7:n=e.sent.default,a=Object.assign(Object.assign({animation:150},this.options),{},{onChoose:this._handleChoose,onStart:this._handleStart,onEnd:this._handleEnd}),this.draggableSelector&&(a.draggable=this.draggableSelector),this.handleSelector&&(a.handle=this.handleSelector),void 0!==this.invertSwap&&(a.invertSwap=this.invertSwap),this.group&&(a.group=this.group),this.filter&&(a.filter=this.filter),this._sortable=new n(t,a);case 15:case"end":return e.stop()}}),e,this)}))),function(){return u.apply(this,arguments)})},{kind:"field",key:"_handleEnd",value:function(){var e=this;return function(){var t=(0,a.A)((0,r.A)().mark((function t(i){var n,a,o,d;return(0,r.A)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if((0,m.r)(e,"drag-end"),e.rollback&&i.item.placeholder&&(i.item.placeholder.replaceWith(i.item),delete i.item.placeholder),n=i.oldIndex,a=i.from.parentElement.path,o=i.newIndex,d=i.to.parentElement.path,void 0!==n&&void 0!==o&&(n!==o||(null==a?void 0:a.join("."))!==(null==d?void 0:d.join(".")))){t.next=8;break}return t.abrupt("return");case 8:(0,m.r)(e,"item-moved",{oldIndex:n,newIndex:o,oldPath:a,newPath:d});case 9:case"end":return t.stop()}}),t)})));return function(e){return t.apply(this,arguments)}}()}},{kind:"field",key:"_handleStart",value:function(){var e=this;return function(){(0,m.r)(e,"drag-start")}}},{kind:"field",key:"_handleChoose",value:function(){var e=this;return function(t){e.rollback&&(t.item.placeholder=document.createComment("sort-placeholder"),t.item.after(t.item.placeholder))}}},{kind:"method",key:"_destroySortable",value:function(){this._sortable&&(this._sortable.destroy(),this._sortable=void 0)}}]}}),p.WF)},90431:function(e,t,i){"use strict";var n,r,a,o,d=i(64599),s=i(35806),l=i(71008),c=i(62193),u=i(2816),h=i(27927),p=i(35890),f=(i(81027),i(44331)),m=i(67449),v=i(15112),g=i(29818),k=i(74005);(0,h.A)([(0,g.EM)("ha-textfield")],(function(e,t){var i=function(t){function i(){var t;(0,l.A)(this,i);for(var n=arguments.length,r=new Array(n),a=0;a<n;a++)r[a]=arguments[a];return t=(0,c.A)(this,i,[].concat(r)),e(t),t}return(0,u.A)(i,t),(0,s.A)(i)}(t);return{F:i,d:[{kind:"field",decorators:[(0,g.MZ)({type:Boolean})],key:"invalid",value:void 0},{kind:"field",decorators:[(0,g.MZ)({attribute:"error-message"})],key:"errorMessage",value:void 0},{kind:"field",decorators:[(0,g.MZ)({type:Boolean})],key:"icon",value:function(){return!1}},{kind:"field",decorators:[(0,g.MZ)({type:Boolean})],key:"iconTrailing",value:function(){return!1}},{kind:"field",decorators:[(0,g.MZ)()],key:"autocomplete",value:void 0},{kind:"field",decorators:[(0,g.MZ)()],key:"autocorrect",value:void 0},{kind:"field",decorators:[(0,g.MZ)({attribute:"input-spellcheck"})],key:"inputSpellcheck",value:void 0},{kind:"field",decorators:[(0,g.P)("input")],key:"formElement",value:void 0},{kind:"method",key:"updated",value:function(e){(0,p.A)(i,"updated",this,3)([e]),(e.has("invalid")||e.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||this.validationMessage||"Invalid":""),(this.invalid||this.validateOnInitialRender||e.has("invalid")&&void 0!==e.get("invalid"))&&this.reportValidity()),e.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),e.has("autocorrect")&&(this.autocorrect?this.formElement.setAttribute("autocorrect",this.autocorrect):this.formElement.removeAttribute("autocorrect")),e.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}},{kind:"method",key:"renderIcon",value:function(e){var t=arguments.length>1&&void 0!==arguments[1]&&arguments[1],i=t?"trailing":"leading";return(0,v.qy)(n||(n=(0,d.A)([' <span class="mdc-text-field__icon mdc-text-field__icon--','" tabindex="','"> <slot name="','Icon"></slot> </span> '])),i,t?1:-1,i)}},{kind:"field",static:!0,key:"styles",value:function(){return[m.R,(0,v.AH)(r||(r=(0,d.A)([".mdc-text-field__input{width:var(--ha-textfield-input-width,100%)}.mdc-text-field:not(.mdc-text-field--with-leading-icon){padding:var(--text-field-padding,0px 16px)}.mdc-text-field__affix--suffix{padding-left:var(--text-field-suffix-padding-left,12px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,12px);padding-inline-end:var(--text-field-suffix-padding-right,0px);direction:ltr}.mdc-text-field--with-leading-icon{padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,16px);direction:var(--direction)}.mdc-text-field--with-leading-icon.mdc-text-field--with-trailing-icon{padding-left:var(--text-field-suffix-padding-left,0px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,0px)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--suffix{color:var(--secondary-text-color)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__icon{color:var(--secondary-text-color)}.mdc-text-field__icon--leading{margin-inline-start:16px;margin-inline-end:8px;direction:var(--direction)}.mdc-text-field__icon--trailing{padding:var(--textfield-icon-trailing-padding,12px)}.mdc-floating-label:not(.mdc-floating-label--float-above){text-overflow:ellipsis;width:inherit;padding-right:30px;padding-inline-end:30px;padding-inline-start:initial;box-sizing:border-box;direction:var(--direction)}input{text-align:var(--text-field-text-align,start)}::-ms-reveal{display:none}:host([no-spinner]) input::-webkit-inner-spin-button,:host([no-spinner]) input::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}:host([no-spinner]) input[type=number]{-moz-appearance:textfield}.mdc-text-field__ripple{overflow:hidden}.mdc-text-field{overflow:var(--text-field-overflow)}.mdc-floating-label{inset-inline-start:16px!important;inset-inline-end:initial!important;transform-origin:var(--float-start);direction:var(--direction);text-align:var(--float-start)}.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label{max-width:calc(100% - 48px - var(--text-field-suffix-padding-left,0px));inset-inline-start:calc(48px + var(--text-field-suffix-padding-left,0px))!important;inset-inline-end:initial!important;direction:var(--direction)}.mdc-text-field__input[type=number]{direction:var(--direction)}.mdc-text-field__affix--prefix{padding-right:var(--text-field-prefix-padding-right,2px);padding-inline-end:var(--text-field-prefix-padding-right,2px);padding-inline-start:initial}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--prefix{color:var(--mdc-text-field-label-ink-color)}"]))),"rtl"===k.G.document.dir?(0,v.AH)(a||(a=(0,d.A)([".mdc-floating-label,.mdc-text-field--with-leading-icon,.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label,.mdc-text-field__icon--leading,.mdc-text-field__input[type=number]{direction:rtl;--direction:rtl}"]))):(0,v.AH)(o||(o=(0,d.A)([""])))]}}]}}),f.J)},38204:function(e,t,i){"use strict";i.d(t,{Ed:function(){return s},K1:function(){return p},Pe:function(){return f},Xf:function(){return c},aO:function(){return d},fk:function(){return u},wE:function(){return h},yU:function(){return l}});i(33994),i(22858),i(42942),i(48062),i(13025),i(82386),i(97741),i(33231),i(50693),i(26098),i(10507),i(39790),i(36604),i(253),i(2075),i(16891);var n=i(213),r=i(19244),a=i(9883),o=i(2682),d=function(e){return e.NeedsAction="needs_action",e.Completed="completed",e}({}),s=function(e){return e[e.CREATE_TODO_ITEM=1]="CREATE_TODO_ITEM",e[e.DELETE_TODO_ITEM=2]="DELETE_TODO_ITEM",e[e.UPDATE_TODO_ITEM=4]="UPDATE_TODO_ITEM",e[e.MOVE_TODO_ITEM=8]="MOVE_TODO_ITEM",e[e.SET_DUE_DATE_ON_ITEM=16]="SET_DUE_DATE_ON_ITEM",e[e.SET_DUE_DATETIME_ON_ITEM=32]="SET_DUE_DATETIME_ON_ITEM",e[e.SET_DESCRIPTION_ON_ITEM=64]="SET_DESCRIPTION_ON_ITEM",e}({}),l=function(e){return Object.keys(e.states).filter((function(t){return"todo"===(0,n.m)(t)&&!(0,a.g0)(e.states[t].state)})).map((function(t){return Object.assign(Object.assign({},e.states[t]),{},{entity_id:t,name:(0,r.u)(e.states[t])})})).sort((function(t,i){return(0,o.x)(t.name,i.name,e.locale.language)}))},c=function(e,t,i){return e.connection.subscribeMessage(i,{type:"todo/item/subscribe",entity_id:t})},u=function(e,t,i){var n,r;return e.callService("todo","update_item",{item:i.uid,rename:i.summary,status:i.status,description:i.description,due_datetime:null!==(n=i.due)&&void 0!==n&&n.includes("T")?i.due:void 0,due_date:void 0===i.due||null!==(r=i.due)&&void 0!==r&&r.includes("T")?void 0:i.due},{entity_id:t})},h=function(e,t,i){var n,r;return e.callService("todo","add_item",{item:i.summary,description:i.description||void 0,due_datetime:null!==(n=i.due)&&void 0!==n&&n.includes("T")?i.due:void 0,due_date:void 0===i.due||null!==(r=i.due)&&void 0!==r&&r.includes("T")?void 0:i.due},{entity_id:t})},p=function(e,t,i){return e.callService("todo","remove_item",{item:i},{entity_id:t})},f=function(e,t,i,n){return e.callWS({type:"todo/item/move",entity_id:t,uid:i,previous_uid:n})}},48292:function(e,t,i){"use strict";var n=i(22858).A,r=i(33994).A;i.a(e,function(){var e=n(r().mark((function e(n,a){var o,d,s,l,c,u,h,p,f,m,v,g,k,y,_,x,b,A,w,E,I,M,T,H,O,C,S,V,L,D,z,Z,q,N,B,R,P,U,F,j,K,W,X,Q,G,J,Y,$,ee,te,ie,ne,re,ae,oe,de,se,le,ce,ue,he,pe,fe,me,ve,ge,ke;return r().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(e.prev=0,i.r(t),i.d(t,{HuiTodoListCard:function(){return ke}}),o=i(41981),d=i(64599),s=i(33994),l=i(22858),c=i(35806),u=i(71008),h=i(62193),p=i(2816),f=i(27927),m=i(35890),v=i(42942),g=i(48062),k=i(71499),y=i(81027),_=i(13025),x=i(44124),b=i(88557),A=i(82386),w=i(95737),E=i(97741),I=i(97099),M=i(54774),T=i(39790),H=i(66457),O=i(36604),C=i(99019),S=i(253),V=i(2075),L=i(94438),D=i(16891),z=i(96858),i(63893),Z=i(31077),q=i(78635),N=i(15112),B=i(29818),R=i(85323),P=i(66066),U=i(94100),F=i(38962),j=i(42496),K=i(79051),i(13082),i(98515),i(88725),i(28066),i(13830),i(32172),W=i(13740),i(77312),i(24260),i(88400),i(90431),X=i(9883),Q=i(38204),G=i(6121),J=i(24137),Y=i(18102),$=i(46645),!(ee=n([W])).then){e.next=91;break}return e.next=87,ee;case 87:e.t1=e.sent,e.t0=(0,e.t1)(),e.next=92;break;case 91:e.t0=ee;case 92:W=e.t0[0],ge="M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z",ke=(0,f.A)([(0,B.EM)("hui-todo-list-card")],(function(e,t){var n,r,a,f,v,g,k,y=function(t){function i(){var t;(0,u.A)(this,i);for(var n=arguments.length,r=new Array(n),a=0;a<n;a++)r[a]=arguments[a];return t=(0,h.A)(this,i,[].concat(r)),e(t),t}return(0,p.A)(i,t),(0,c.A)(i)}(t);return{F:y,d:[{kind:"method",static:!0,key:"getConfigElement",value:(k=(0,l.A)((0,s.A)().mark((function e(){return(0,s.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,i.e(82656).then(i.bind(i,82656));case 2:return e.abrupt("return",document.createElement("hui-todo-list-card-editor"));case 3:case"end":return e.stop()}}),e)}))),function(){return k.apply(this,arguments)})},{kind:"method",static:!0,key:"getStubConfig",value:function(e,t,i){return{type:"todo-list",entity:(0,Y.B)(e,1,t,i,["todo"])[0]||""}}},{kind:"field",decorators:[(0,B.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,B.wk)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,B.wk)()],key:"_entityId",value:void 0},{kind:"field",decorators:[(0,B.wk)()],key:"_items",value:void 0},{kind:"field",decorators:[(0,B.wk)()],key:"_reordering",value:function(){return!1}},{kind:"field",key:"_unsubItems",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,m.A)(y,"connectedCallback",this,3)([]),this.hasUpdated&&this._subscribeItems()}},{kind:"method",key:"disconnectedCallback",value:function(){var e;(0,m.A)(y,"disconnectedCallback",this,3)([]),null===(e=this._unsubItems)||void 0===e||e.then((function(e){return e()})),this._unsubItems=void 0}},{kind:"method",key:"getCardSize",value:function(){return 3+(this._config&&this._config.title?2:0)}},{kind:"method",key:"setConfig",value:function(e){this.checkConfig(e),this._config=e,this._entityId=e.entity}},{kind:"method",key:"checkConfig",value:function(e){if(!e.entity||"todo"!==e.entity.split(".")[0])throw new Error("Specify an entity from within the todo domain")}},{kind:"method",key:"getEntityId",value:function(){}},{kind:"field",key:"_getCheckedItems",value:function(){return(0,U.A)((function(e){return e?e.filter((function(e){return e.status===Q.aO.Completed})):[]}))}},{kind:"field",key:"_getUncheckedItems",value:function(){return(0,U.A)((function(e){return e?e.filter((function(e){return e.status===Q.aO.NeedsAction})):[]}))}},{kind:"method",key:"willUpdate",value:function(e){this.hasUpdated?!e.has("_entityId")&&this._items||(this._items=void 0,this._subscribeItems()):(this._entityId||(this._entityId=this.getEntityId()),this._subscribeItems())}},{kind:"method",key:"updated",value:function(e){if((0,m.A)(y,"updated",this,3)([e]),this._config&&this.hass){var t=e.get("hass"),i=e.get("_config");(e.has("hass")&&(null==t?void 0:t.themes)!==this.hass.themes||e.has("_config")&&(null==i?void 0:i.theme)!==this._config.theme)&&(0,F.Q)(this,this.hass.themes,this._config.theme)}}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass||!this._entityId)return N.s6;var e=this.hass.states[this._entityId];if(!e)return(0,N.qy)(te||(te=(0,d.A)([" <hui-warning> "," </hui-warning> "])),(0,$.j)(this.hass,this._entityId));var t=(0,X.g0)(e.state),i=this._getCheckedItems(this._items),n=this._getUncheckedItems(this._items);return(0,N.qy)(ie||(ie=(0,d.A)([' <ha-card .header="','" class="','"> <div class="addRow"> ',' </div> <ha-sortable handle-selector="ha-svg-icon" draggable-selector=".draggable" .disabled="','" @item-moved="','"> <mwc-list wrapFocus multi> '," "," </mwc-list> </ha-sortable> </ha-card> "])),this._config.title,(0,R.H)({"has-header":"title"in this._config}),this.todoListSupportsFeature(Q.Ed.CREATE_TODO_ITEM)?(0,N.qy)(ne||(ne=(0,d.A)([' <ha-textfield class="addBox" .placeholder="','" @keydown="','" .disabled="','"></ha-textfield> <ha-icon-button class="addButton" .path="','" .title="','" .disabled="','" @click="','"> </ha-icon-button> '])),this.hass.localize("ui.panel.lovelace.cards.todo-list.add_item"),this._addKeyPress,t,"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z",this.hass.localize("ui.panel.lovelace.cards.todo-list.add_item"),t,this._addItem):N.s6,!this._reordering,this._itemMoved,n.length?(0,N.qy)(re||(re=(0,d.A)([' <div class="header" role="seperator"> <h2> '," </h2> "," </div> "," "])),this.hass.localize("ui.panel.lovelace.cards.todo-list.unchecked_items"),this.todoListSupportsFeature(Q.Ed.MOVE_TODO_ITEM)?(0,N.qy)(ae||(ae=(0,d.A)(['<ha-button-menu @closed="','"> <ha-icon-button slot="trigger" .path="','"></ha-icon-button> <ha-list-item @click="','" graphic="icon"> ',' <ha-svg-icon slot="graphic" .path="','" .disabled="','"> </ha-svg-icon> </ha-list-item> </ha-button-menu>'])),K.d,ge,this._toggleReorder,this.hass.localize(this._reordering?"ui.panel.lovelace.cards.todo-list.exit_reorder_items":"ui.panel.lovelace.cards.todo-list.reorder_items"),"M18 21L14 17H17V7H14L18 3L22 7H19V17H22M2 19V17H12V19M2 13V11H9V13M2 7V5H6V7H2Z",t):N.s6,this._renderItems(n,t)):(0,N.qy)(oe||(oe=(0,d.A)(['<p class="empty"> '," </p>"])),this.hass.localize("ui.panel.lovelace.cards.todo-list.no_unchecked_items")),i.length?(0,N.qy)(de||(de=(0,d.A)([' <div role="separator"> <div class="divider"></div> <div class="header"> <h2> '," </h2> "," </div> </div> "," "])),this.hass.localize("ui.panel.lovelace.cards.todo-list.checked_items"),this.todoListSupportsFeature(Q.Ed.DELETE_TODO_ITEM)?(0,N.qy)(se||(se=(0,d.A)(['<ha-button-menu @closed="','"> <ha-icon-button slot="trigger" .path="','"></ha-icon-button> <ha-list-item @click="','" graphic="icon" class="warning"> ',' <ha-svg-icon class="warning" slot="graphic" .path="','" .disabled="','"> </ha-svg-icon> </ha-list-item> </ha-button-menu>'])),K.d,ge,this._clearCompletedItems,this.hass.localize("ui.panel.lovelace.cards.todo-list.clear_items"),"M15,16H19V18H15V16M15,8H22V10H15V8M15,12H21V14H15V12M3,18A2,2 0 0,0 5,20H11A2,2 0 0,0 13,18V8H3V18M14,5H11L10,4H6L5,5H2V7H14V5Z",t):N.s6,this._renderItems(i,t)):"")}},{kind:"method",key:"_renderItems",value:function(e){var t=this,i=arguments.length>1&&void 0!==arguments[1]&&arguments[1];return(0,N.qy)(le||(le=(0,d.A)([" "," "])),(0,P.u)(e,(function(e){return e.uid}),(function(e){var n=t.todoListSupportsFeature(Q.Ed.DELETE_TODO_ITEM)&&!t.todoListSupportsFeature(Q.Ed.UPDATE_TODO_ITEM),r=e.status!==Q.aO.Completed&&t._reordering,a=e.due?e.due.includes("T")?new Date(e.due):(0,Z.D)(new Date("".concat(e.due,"T00:00:00"))):void 0,o=a&&!e.due.includes("T")&&(0,q.r)(new Date,a);return(0,N.qy)(ce||(ce=(0,d.A)([' <ha-check-list-item left .hasMeta="','" class="editRow ','" .selected="','" .disabled="','" item-id="','" .itemId="','" @change="','" @click="','" @request-selected="','" @keydown="','"> <div class="column"> <span class="summary">',"</span> "," "," </div> "," </ha-check-list-item> "])),r||n,(0,R.H)({draggable:e.status===Q.aO.NeedsAction,completed:e.status===Q.aO.Completed,multiline:Boolean(e.description||e.due)}),e.status===Q.aO.Completed,i||!t.todoListSupportsFeature(Q.Ed.UPDATE_TODO_ITEM),e.uid,e.uid,t._completeItem,t._openItem,t._requestSelected,t._handleKeydown,e.summary,e.description?(0,N.qy)(ue||(ue=(0,d.A)(['<ha-markdown-element class="description" .content="','"></ha-markdown-element>'])),e.description):N.s6,a?(0,N.qy)(he||(he=(0,d.A)(['<div class="due ','"> <ha-svg-icon .path="','"></ha-svg-icon>'," </div>"])),a<new Date?"overdue":"","M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M16.2,16.2L11,13V7H12.5V12.2L17,14.9L16.2,16.2Z",o?t.hass.localize("ui.panel.lovelace.cards.todo-list.today"):(0,N.qy)(pe||(pe=(0,d.A)(['<ha-relative-time capitalize .hass="','" .datetime="','"></ha-relative-time>'])),t.hass,a)):N.s6,r?(0,N.qy)(fe||(fe=(0,d.A)([' <ha-svg-icon .title="','" class="reorderButton handle" .path="','" slot="meta"> </ha-svg-icon> '])),t.hass.localize("ui.panel.lovelace.cards.todo-list.drag_and_drop"),"M7,19V17H9V19H7M11,19V17H13V19H11M15,19V17H17V19H15M7,15V13H9V15H7M11,15V13H13V15H11M15,15V13H17V15H15M7,11V9H9V11H7M11,11V9H13V11H11M15,11V9H17V11H15M7,7V5H9V7H7M11,7V5H13V7H11M15,7V5H17V7H15Z"):n?(0,N.qy)(me||(me=(0,d.A)(['<ha-icon-button .title="','" class="deleteItemButton" .path="','" .itemId="','" slot="meta" @click="','"> </ha-icon-button>'])),t.hass.localize("ui.panel.lovelace.cards.todo-list.delete_item"),"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z",e.uid,t._deleteItem):N.s6)})))}},{kind:"method",key:"todoListSupportsFeature",value:function(e){var t=this.hass.states[this._entityId];return t&&(0,j.$)(t,e)}},{kind:"method",key:"_subscribeItems",value:(g=(0,l.A)((0,s.A)().mark((function e(){var t=this;return(0,s.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(this._unsubItems&&(this._unsubItems.then((function(e){return e()})),this._unsubItems=void 0),this.hass&&this._entityId){e.next=3;break}return e.abrupt("return");case 3:if(this._entityId in this.hass.states){e.next=5;break}return e.abrupt("return");case 5:this._unsubItems=(0,Q.Xf)(this.hass,this._entityId,(function(e){t._items=e.items}));case 6:case"end":return e.stop()}}),e,this)}))),function(){return g.apply(this,arguments)})},{kind:"method",key:"_getItem",value:function(e){var t;return null===(t=this._items)||void 0===t?void 0:t.find((function(t){return t.uid===e}))}},{kind:"method",key:"_requestSelected",value:function(e){e.stopPropagation()}},{kind:"method",key:"_handleKeydown",value:function(e){" "!==e.key?"Enter"===e.key&&this._openItem(e):this._completeItem(e)}},{kind:"method",key:"_openItem",value:function(e){if(e.stopPropagation(),!e.composedPath().find((function(e){return["input","a","button"].includes(e.localName)}))){var t=this._getItem(e.currentTarget.itemId);(0,J.X)(this,{entity:this._entityId,item:t})}}},{kind:"method",key:"_completeItem",value:(v=(0,l.A)((0,s.A)().mark((function e(t){var i,n,r;return(0,s.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if("keydown"===t.type&&(n=this.renderRoot.querySelector("mwc-list"),i=n.getFocusedItemIndex()),r=this._getItem(t.currentTarget.itemId)){e.next=4;break}return e.abrupt("return");case 4:return e.next=6,(0,Q.fk)(this.hass,this._entityId,{uid:r.uid,summary:r.summary,status:r.status===Q.aO.NeedsAction?Q.aO.Completed:Q.aO.NeedsAction});case 6:if(void 0===i||!n){e.next=12;break}return e.next=9,this.updateComplete;case 9:return e.next=11,n.updateComplete;case 11:n.focusItemAtIndex(i);case 12:case"end":return e.stop()}}),e,this)}))),function(e){return v.apply(this,arguments)})},{kind:"method",key:"_clearCompletedItems",value:(f=(0,l.A)((0,s.A)().mark((function e(){var t,i,n=this;return(0,s.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(this.hass){e.next=2;break}return e.abrupt("return");case 2:t=this._getCheckedItems(this._items),i=t.map((function(e){return e.uid})),(0,G.showConfirmationDialog)(this,{title:this.hass.localize("ui.panel.lovelace.cards.todo-list.delete_confirm_title"),text:this.hass.localize("ui.panel.lovelace.cards.todo-list.delete_confirm_text",{number:i.length}),dismissText:this.hass.localize("ui.common.cancel"),confirmText:this.hass.localize("ui.common.delete"),destructive:!0,confirm:function(){(0,Q.K1)(n.hass,n._entityId,i)}});case 5:case"end":return e.stop()}}),e,this)}))),function(){return f.apply(this,arguments)})},{kind:"get",key:"_newItem",value:function(){return this.shadowRoot.querySelector(".addBox")}},{kind:"method",key:"_addItem",value:function(e){var t=this._newItem;t.value.length>0&&(0,Q.wE)(this.hass,this._entityId,{summary:t.value}),t.value="",e&&t.focus()}},{kind:"method",key:"_deleteItem",value:function(e){var t=this._getItem(e.target.itemId);t&&(0,Q.K1)(this.hass,this._entityId,[t.uid])}},{kind:"method",key:"_addKeyPress",value:function(e){"Enter"===e.key&&this._addItem(null)}},{kind:"method",key:"_toggleReorder",value:(a=(0,l.A)((0,s.A)().mark((function e(){return(0,s.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:this._reordering=!this._reordering;case 1:case"end":return e.stop()}}),e,this)}))),function(){return a.apply(this,arguments)})},{kind:"method",key:"_itemMoved",value:(r=(0,l.A)((0,s.A)().mark((function e(t){var i,n,r;return(0,s.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:t.stopPropagation(),i=t.detail,n=i.oldIndex,r=i.newIndex,this._moveItem(n,r);case 3:case"end":return e.stop()}}),e,this)}))),function(e){return r.apply(this,arguments)})},{kind:"method",key:"_moveItem",value:(n=(0,l.A)((0,s.A)().mark((function e(t,i){var n,r,a,d,l,c;return(0,s.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return t-=1,i-=1,r=this._getUncheckedItems(this._items),a=r[t],i>0&&(d=i<t?r[i-1]:r[i]),l=this._items.findIndex((function(e){return e.uid===a.uid})),this._items.splice(l,1),0===i?this._items.unshift(a):(c=this._items.findIndex((function(e){return e.uid===d.uid})),this._items.splice(c+1,0,a)),this._items=(0,o.A)(this._items),e.next=11,(0,Q.Pe)(this.hass,this._entityId,a.uid,null===(n=d)||void 0===n?void 0:n.uid);case 11:case"end":return e.stop()}}),e,this)}))),function(e,t){return n.apply(this,arguments)})},{kind:"get",static:!0,key:"styles",value:function(){return(0,N.AH)(ve||(ve=(0,d.A)(["ha-card{height:100%;box-sizing:border-box}.has-header{padding-top:0}.addRow{padding:16px;padding-bottom:0;position:relative}.addRow ha-icon-button{position:absolute;right:16px;inset-inline-start:initial;inset-inline-end:16px}.addRow,.header{display:flex;flex-direction:row;align-items:center}.header{padding-left:30px;padding-right:16px;padding-inline-start:30px;padding-inline-end:16px;margin-top:8px;justify-content:space-between;direction:var(--direction)}.header h2{color:var(--primary-text-color);font-size:inherit;font-weight:500}.empty{padding:16px 32px;display:inline-block}.item{margin-top:8px}ha-check-list-item{--mdc-list-item-meta-size:56px;min-height:56px;height:auto}ha-check-list-item.multiline{align-items:flex-start;--check-list-item-graphic-margin-top:8px}.row{display:flex;justify-content:space-between}.multiline .column{display:flex;flex-direction:column;margin-top:18px;margin-bottom:12px}.completed .summary{text-decoration:line-through}.description,.due{font-size:12px;color:var(--secondary-text-color)}.description{white-space:initial;overflow:hidden;display:-webkit-box;-webkit-line-clamp:3;line-clamp:3;-webkit-box-orient:vertical}.description p{margin:0}.description a{color:var(--primary-color)}.due{display:flex;align-items:center}.due ha-svg-icon{margin-right:4px;margin-inline-end:4px;margin-inline-start:initial;--mdc-icon-size:14px}.due.overdue{color:var(--warning-color)}.completed .due.overdue{color:var(--secondary-text-color)}.handle{cursor:move;cursor:grab;height:24px;padding:16px 4px}.deleteItemButton{position:relative;left:8px;inset-inline-start:8px;inset-inline-end:initial}ha-textfield{flex-grow:1}.divider{height:1px;background-color:var(--divider-color);margin:10px 0}.clearall{cursor:pointer}.todoList{display:block;padding:8px}.warning{color:var(--error-color)}"])))}}]}}),N.WF),a(),e.next=107;break;case 104:e.prev=104,e.t2=e.catch(0),a(e.t2);case 107:case"end":return e.stop()}}),e,null,[[0,104]])})));return function(t,i){return e.apply(this,arguments)}}())},24137:function(e,t,i){"use strict";i.d(t,{X:function(){return a}});i(95737),i(39790),i(66457),i(99019),i(96858);var n=i(34897),r=function(){return Promise.all([i.e(94131),i.e(10963),i.e(14691),i.e(59089),i.e(35193),i.e(76994),i.e(36561)]).then(i.bind(i,93423))},a=function(e,t){(0,n.r)(e,"show-dialog",{dialogTag:"dialog-todo-item-editor",dialogImport:r,dialogParams:t})}},75402:function(e,t,i){var n={"./ha-alert":[13292,13292],"./ha-alert.ts":[13292,13292],"./ha-icon":[20144,20144,13696],"./ha-icon-button":[28066],"./ha-icon-button-arrow-next":[99682,99682],"./ha-icon-button-arrow-next.ts":[99682,99682],"./ha-icon-button-arrow-prev":[45346,45346],"./ha-icon-button-arrow-prev.ts":[45346,45346],"./ha-icon-button-group":[33871,56252],"./ha-icon-button-group.ts":[33871,56252],"./ha-icon-button-next":[63606,63606],"./ha-icon-button-next.ts":[63606,63606],"./ha-icon-button-prev":[40462,40462],"./ha-icon-button-prev.ts":[40462,40462],"./ha-icon-button-toggle":[28803,28803],"./ha-icon-button-toggle.ts":[28803,28803],"./ha-icon-button.ts":[28066],"./ha-icon-next":[46163,46163],"./ha-icon-next.ts":[46163,46163],"./ha-icon-overflow-menu":[16850,33810,63893,23766,29654,7986,37387],"./ha-icon-overflow-menu.ts":[16850,33810,63893,23766,29654,7986,37387],"./ha-icon-picker":[85288,94131,14121,33810,40319,7726,20144,41127],"./ha-icon-picker.ts":[85288,94131,14121,33810,40319,7726,20144,41127],"./ha-icon-prev":[36119,36119],"./ha-icon-prev.ts":[36119,36119],"./ha-icon.ts":[20144,20144,13696],"./ha-qr-code":[33209,72915,50240,21080],"./ha-qr-code.ts":[33209,72915,50240,21080],"./ha-svg-icon":[88400],"./ha-svg-icon.ts":[88400]};function r(e){if(!i.o(n,e))return Promise.resolve().then((function(){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t}));var t=n[e],r=t[0];return Promise.all(t.slice(1).map(i.e)).then((function(){return i(r)}))}r.keys=function(){return Object.keys(n)},r.id=75402,e.exports=r}}]);
//# sourceMappingURL=48292.F1GVntH-2tM.js.map