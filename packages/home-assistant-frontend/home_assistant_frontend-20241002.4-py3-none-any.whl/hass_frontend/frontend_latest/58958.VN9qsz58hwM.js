/*! For license information please see 58958.VN9qsz58hwM.js.LICENSE.txt */
export const id=58958;export const ids=[58958,37629];export const modules={79051:(e,t,r)=>{r.d(t,{d:()=>i});const i=e=>e.stopPropagation()},37629:(e,t,r)=>{r.r(t),r.d(t,{HaCircularProgress:()=>n});var i=r(36312),a=r(68689),o=r(99322),s=r(15112),c=r(77706);let n=(0,i.A)([(0,c.EM)("ha-circular-progress")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,c.MZ)({attribute:"aria-label",type:String})],key:"ariaLabel",value:()=>"Loading"},{kind:"field",decorators:[(0,c.MZ)()],key:"size",value:()=>"medium"},{kind:"method",key:"updated",value:function(e){if((0,a.A)(r,"updated",this,3)([e]),e.has("size"))switch(this.size){case"tiny":this.style.setProperty("--md-circular-progress-size","16px");break;case"small":this.style.setProperty("--md-circular-progress-size","28px");break;case"medium":this.style.setProperty("--md-circular-progress-size","48px");break;case"large":this.style.setProperty("--md-circular-progress-size","68px")}}},{kind:"field",static:!0,key:"styles",value(){return[...(0,a.A)(r,"styles",this),s.AH`:host{--md-sys-color-primary:var(--primary-color);--md-circular-progress-size:48px}`]}}]}}),o.U)},77312:(e,t,r)=>{var i=r(36312),a=r(68689),o=r(24500),s=r(14691),c=r(15112),n=r(77706),l=r(18409),d=r(61441);r(28066);(0,i.A)([(0,n.EM)("ha-select")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"icon",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"clearable",value:()=>!1},{kind:"method",key:"render",value:function(){return c.qy` ${(0,a.A)(r,"render",this,3)([])} ${this.clearable&&!this.required&&!this.disabled&&this.value?c.qy`<ha-icon-button label="clear" @click="${this._clearValue}" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}"></ha-icon-button>`:c.s6} `}},{kind:"method",key:"renderLeadingIcon",value:function(){return this.icon?c.qy`<span class="mdc-select__icon"><slot name="icon"></slot></span>`:c.s6}},{kind:"method",key:"connectedCallback",value:function(){(0,a.A)(r,"connectedCallback",this,3)([]),window.addEventListener("translations-updated",this._translationsUpdated)}},{kind:"method",key:"disconnectedCallback",value:function(){(0,a.A)(r,"disconnectedCallback",this,3)([]),window.removeEventListener("translations-updated",this._translationsUpdated)}},{kind:"method",key:"_clearValue",value:function(){!this.disabled&&this.value&&(this.valueSetDirectly=!0,this.select(-1),this.mdcFoundation.handleChange())}},{kind:"field",key:"_translationsUpdated",value(){return(0,l.s)((async()=>{await(0,d.E)(),this.layoutOptions()}),500)}},{kind:"field",static:!0,key:"styles",value:()=>[s.R,c.AH`:host([clearable]){position:relative}.mdc-select:not(.mdc-select--disabled) .mdc-select__icon{color:var(--secondary-text-color)}.mdc-select__anchor{width:var(--ha-select-min-width,200px)}.mdc-select--filled .mdc-select__anchor{height:var(--ha-select-height,56px)}.mdc-select--filled .mdc-floating-label{inset-inline-start:12px;inset-inline-end:initial;direction:var(--direction)}.mdc-select--filled.mdc-select--with-leading-icon .mdc-floating-label{inset-inline-start:48px;inset-inline-end:initial;direction:var(--direction)}.mdc-select .mdc-select__anchor{padding-inline-start:12px;padding-inline-end:0px;direction:var(--direction)}.mdc-select__anchor .mdc-floating-label--float-above{transform-origin:var(--float-start)}.mdc-select__selected-text-container{padding-inline-end:var(--select-selected-text-padding-end,0px)}:host([clearable]) .mdc-select__selected-text-container{padding-inline-end:var(--select-selected-text-padding-end,12px)}ha-icon-button{position:absolute;top:10px;right:28px;--mdc-icon-button-size:36px;--mdc-icon-size:20px;color:var(--secondary-text-color);inset-inline-start:initial;inset-inline-end:28px;direction:var(--direction)}`]}]}}),o.o)},15416:(e,t,r)=>{r.r(t);var i=r(36312),a=(r(16891),r(67056),r(15112)),o=r(77706),s=r(94100),c=r(34897),n=r(79051),l=(r(37629),r(77312),r(26025)),d=r(37266),u=r(6121),h=r(55321),v=r(88441);const p=(0,s.A)((e=>{const t=""!==e.disk_life_time?30:10,r=1e3*e.disk_used/60/t,i=4*e.startup_time/60;return 10*Math.ceil((r+i)/10)}));(0,i.A)([(0,o.EM)("dialog-move-datadisk")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_hostInfo",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_selectedDevice",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_disks",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_osInfo",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_moving",value:()=>!1},{kind:"method",key:"showDialog",value:async function(e){this._hostInfo=e.hostInfo;try{this._osInfo=await(0,d.PB)(this.hass);const e=await(0,d.xY)(this.hass);e.devices.length>0?this._disks=e.disks:(this.closeDialog(),await(0,u.showAlertDialog)(this,{title:this.hass.localize("ui.panel.config.storage.datadisk.no_devices_title"),text:this.hass.localize("ui.panel.config.storage.datadisk.no_devices_text")}))}catch(e){this.closeDialog(),await(0,u.showAlertDialog)(this,{title:this.hass.localize("ui.panel.config.hardware.available_hardware.failed_to_get"),text:(0,l.VR)(e)})}}},{kind:"method",key:"closeDialog",value:function(){this._selectedDevice=void 0,this._disks=void 0,this._moving=!1,this._hostInfo=void 0,this._osInfo=void 0,(0,c.r)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return this._hostInfo&&this._osInfo&&this._disks?a.qy` <ha-dialog open scrimClickAction escapeKeyAction .heading="${this._moving?this.hass.localize("ui.panel.config.storage.datadisk.moving"):this.hass.localize("ui.panel.config.storage.datadisk.title")}" @closed="${this.closeDialog}" ?hideActions="${this._moving}"> ${this._moving?a.qy` <ha-circular-progress aria-label="Moving" size="large" indeterminate> </ha-circular-progress> <p class="progress-text"> ${this.hass.localize("ui.panel.config.storage.datadisk.moving_desc")} </p> `:a.qy` ${this.hass.localize("ui.panel.config.storage.datadisk.description",{current_path:this._osInfo.data_disk,time:p(this._hostInfo)})} <br><br> <ha-select .label="${this.hass.localize("ui.panel.config.storage.datadisk.select_device")}" @selected="${this._select_device}" @closed="${n.d}" dialogInitialFocus fixedMenuPosition> ${this._disks.map((e=>a.qy`<mwc-list-item twoline .value="${e.id}"> <span>${e.vendor} ${e.model}</span> <span slot="secondary"> ${this.hass.localize("ui.panel.config.storage.datadisk.extra_information",{size:(0,v.A)(e.size),serial:e.serial})} </span> </mwc-list-item>`))} </ha-select> <mwc-button slot="secondaryAction" @click="${this.closeDialog}" dialogInitialFocus> ${this.hass.localize("ui.panel.config.storage.datadisk.cancel")} </mwc-button> <mwc-button .disabled="${!this._selectedDevice}" slot="primaryAction" @click="${this._moveDatadisk}"> ${this.hass.localize("ui.panel.config.storage.datadisk.move")} </mwc-button> `} </ha-dialog> `:a.s6}},{kind:"method",key:"_select_device",value:function(e){this._selectedDevice=e.target.value}},{kind:"method",key:"_moveDatadisk",value:async function(){this._moving=!0;try{await(0,d.v9)(this.hass,this._selectedDevice)}catch(e){this.hass.connection.connected&&!(0,l.Tv)(e)&&(0,u.showAlertDialog)(this,{title:this.hass.localize("ui.panel.config.storage.datadisk.failed_to_move"),text:(0,l.VR)(e)})}finally{this.closeDialog()}}},{kind:"get",static:!0,key:"styles",value:function(){return[h.RF,h.nA,a.AH`ha-select{width:100%}ha-circular-progress{display:block;margin:32px;text-align:center}.progress-text{text-align:center}`]}}]}}),a.WF)},88441:(e,t,r)=>{r.d(t,{A:()=>i});const i=(e=0,t=2)=>{if(0===e)return"0 Bytes";t=t<0?0:t;const r=Math.floor(Math.log(e)/Math.log(1024));return`${parseFloat((e/1024**r).toFixed(t))} ${["Bytes","KB","MB","GB","TB","PB","EB","ZB","YB"][r]}`}},26604:(e,t,r)=>{r.d(t,{n:()=>l});r(24545),r(51855),r(82130),r(31743),r(22328),r(4959),r(62435);var i=r(15112);const a=["role","ariaAtomic","ariaAutoComplete","ariaBusy","ariaChecked","ariaColCount","ariaColIndex","ariaColSpan","ariaCurrent","ariaDisabled","ariaExpanded","ariaHasPopup","ariaHidden","ariaInvalid","ariaKeyShortcuts","ariaLabel","ariaLevel","ariaLive","ariaModal","ariaMultiLine","ariaMultiSelectable","ariaOrientation","ariaPlaceholder","ariaPosInSet","ariaPressed","ariaReadOnly","ariaRequired","ariaRoleDescription","ariaRowCount","ariaRowIndex","ariaRowSpan","ariaSelected","ariaSetSize","ariaSort","ariaValueMax","ariaValueMin","ariaValueNow","ariaValueText"],o=a.map(c);function s(e){return o.includes(e)}function c(e){return e.replace("aria","aria-").replace(/Elements?/g,"").toLowerCase()}const n=Symbol("privateIgnoreAttributeChangesFor");function l(e){var t;if(i.S$)return e;class r extends e{constructor(){super(...arguments),this[t]=new Set}attributeChangedCallback(e,t,r){if(!s(e))return void super.attributeChangedCallback(e,t,r);if(this[n].has(e))return;this[n].add(e),this.removeAttribute(e),this[n].delete(e);const i=u(e);null===r?delete this.dataset[i]:this.dataset[i]=r,this.requestUpdate(u(e),t)}getAttribute(e){return s(e)?super.getAttribute(d(e)):super.getAttribute(e)}removeAttribute(e){super.removeAttribute(e),s(e)&&(super.removeAttribute(d(e)),this.requestUpdate())}}return t=n,function(e){for(const t of a){const r=c(t),i=d(r),a=u(r);e.createProperty(t,{attribute:r,noAccessor:!0}),e.createProperty(Symbol(i),{attribute:i,noAccessor:!0}),Object.defineProperty(e.prototype,t,{configurable:!0,enumerable:!0,get(){return this.dataset[a]??null},set(e){const r=this.dataset[a]??null;e!==r&&(null===e?delete this.dataset[a]:this.dataset[a]=e,this.requestUpdate(t,r))}})}}(r),r}function d(e){return`data-${e}`}function u(e){return e.replace(/-\w/,(e=>e[1].toUpperCase()))}},99322:(e,t,r)=>{r.d(t,{U:()=>u});var i=r(79192),a=r(77706),o=r(15112),s=r(85323);const c=(0,r(26604).n)(o.WF);class n extends c{constructor(){super(...arguments),this.value=0,this.max=1,this.indeterminate=!1,this.fourColor=!1}render(){const{ariaLabel:e}=this;return o.qy` <div class="progress ${(0,s.H)(this.getRenderClasses())}" role="progressbar" aria-label="${e||o.s6}" aria-valuemin="0" aria-valuemax="${this.max}" aria-valuenow="${this.indeterminate?o.s6:this.value}">${this.renderIndicator()}</div> `}getRenderClasses(){return{indeterminate:this.indeterminate,"four-color":this.fourColor}}}(0,i.__decorate)([(0,a.MZ)({type:Number})],n.prototype,"value",void 0),(0,i.__decorate)([(0,a.MZ)({type:Number})],n.prototype,"max",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean})],n.prototype,"indeterminate",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean,attribute:"four-color"})],n.prototype,"fourColor",void 0);class l extends n{renderIndicator(){return this.indeterminate?this.renderIndeterminateContainer():this.renderDeterminateContainer()}renderDeterminateContainer(){const e=100*(1-this.value/this.max);return o.qy` <svg viewBox="0 0 4800 4800"> <circle class="track" pathLength="100"></circle> <circle class="active-track" pathLength="100" stroke-dashoffset="${e}"></circle> </svg> `}renderIndeterminateContainer(){return o.qy` <div class="spinner"> <div class="left"> <div class="circle"></div> </div> <div class="right"> <div class="circle"></div> </div> </div>`}}const d=o.AH`:host{--_active-indicator-color:var(--md-circular-progress-active-indicator-color, var(--md-sys-color-primary, #6750a4));--_active-indicator-width:var(--md-circular-progress-active-indicator-width, 10);--_four-color-active-indicator-four-color:var(--md-circular-progress-four-color-active-indicator-four-color, var(--md-sys-color-tertiary-container, #ffd8e4));--_four-color-active-indicator-one-color:var(--md-circular-progress-four-color-active-indicator-one-color, var(--md-sys-color-primary, #6750a4));--_four-color-active-indicator-three-color:var(--md-circular-progress-four-color-active-indicator-three-color, var(--md-sys-color-tertiary, #7d5260));--_four-color-active-indicator-two-color:var(--md-circular-progress-four-color-active-indicator-two-color, var(--md-sys-color-primary-container, #eaddff));--_size:var(--md-circular-progress-size, 48px);display:inline-flex;vertical-align:middle;width:var(--_size);height:var(--_size);position:relative;align-items:center;justify-content:center;contain:strict;content-visibility:auto}.progress{flex:1;align-self:stretch;margin:4px}.active-track,.circle,.left,.progress,.right,.spinner,.track,svg{position:absolute;inset:0}svg{transform:rotate(-90deg)}circle{cx:50%;cy:50%;r:calc(50%*(1 - var(--_active-indicator-width)/ 100));stroke-width:calc(var(--_active-indicator-width)*1%);stroke-dasharray:100;fill:rgba(0,0,0,0)}.active-track{transition:stroke-dashoffset .5s cubic-bezier(0, 0, .2, 1);stroke:var(--_active-indicator-color)}.track{stroke:rgba(0,0,0,0)}.progress.indeterminate{animation:linear infinite linear-rotate;animation-duration:1.568s}.spinner{animation:infinite both rotate-arc;animation-duration:5332ms;animation-timing-function:cubic-bezier(0.4,0,0.2,1)}.left{overflow:hidden;inset:0 50% 0 0}.right{overflow:hidden;inset:0 0 0 50%}.circle{box-sizing:border-box;border-radius:50%;border:solid calc(var(--_active-indicator-width)/ 100*(var(--_size) - 8px));border-color:var(--_active-indicator-color) var(--_active-indicator-color) transparent transparent;animation:expand-arc;animation-iteration-count:infinite;animation-fill-mode:both;animation-duration:1333ms,5332ms;animation-timing-function:cubic-bezier(0.4,0,0.2,1)}.four-color .circle{animation-name:expand-arc,four-color}.left .circle{rotate:135deg;inset:0 -100% 0 0}.right .circle{rotate:100deg;inset:0 0 0 -100%;animation-delay:-.666s,0s}@media(forced-colors:active){.active-track{stroke:CanvasText}.circle{border-color:CanvasText CanvasText Canvas Canvas}}@keyframes expand-arc{0%{transform:rotate(265deg)}50%{transform:rotate(130deg)}100%{transform:rotate(265deg)}}@keyframes rotate-arc{12.5%{transform:rotate(135deg)}25%{transform:rotate(270deg)}37.5%{transform:rotate(405deg)}50%{transform:rotate(540deg)}62.5%{transform:rotate(675deg)}75%{transform:rotate(810deg)}87.5%{transform:rotate(945deg)}100%{transform:rotate(1080deg)}}@keyframes linear-rotate{to{transform:rotate(360deg)}}@keyframes four-color{0%{border-top-color:var(--_four-color-active-indicator-one-color);border-right-color:var(--_four-color-active-indicator-one-color)}15%{border-top-color:var(--_four-color-active-indicator-one-color);border-right-color:var(--_four-color-active-indicator-one-color)}25%{border-top-color:var(--_four-color-active-indicator-two-color);border-right-color:var(--_four-color-active-indicator-two-color)}40%{border-top-color:var(--_four-color-active-indicator-two-color);border-right-color:var(--_four-color-active-indicator-two-color)}50%{border-top-color:var(--_four-color-active-indicator-three-color);border-right-color:var(--_four-color-active-indicator-three-color)}65%{border-top-color:var(--_four-color-active-indicator-three-color);border-right-color:var(--_four-color-active-indicator-three-color)}75%{border-top-color:var(--_four-color-active-indicator-four-color);border-right-color:var(--_four-color-active-indicator-four-color)}90%{border-top-color:var(--_four-color-active-indicator-four-color);border-right-color:var(--_four-color-active-indicator-four-color)}100%{border-top-color:var(--_four-color-active-indicator-one-color);border-right-color:var(--_four-color-active-indicator-one-color)}}`;let u=class extends l{};u.styles=[d],u=(0,i.__decorate)([(0,a.EM)("md-circular-progress")],u)},67089:(e,t,r)=>{r.d(t,{OA:()=>i.OA,WL:()=>i.WL,u$:()=>i.u$});var i=r(68063)}};
//# sourceMappingURL=58958.VN9qsz58hwM.js.map