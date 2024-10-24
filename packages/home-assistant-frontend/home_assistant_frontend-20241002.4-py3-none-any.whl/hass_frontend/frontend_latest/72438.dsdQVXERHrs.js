export const id=72438;export const ids=[72438];export const modules={64541:(e,t,o)=>{o.d(t,{E:()=>a});o(24545),o(51855),o(82130),o(31743),o(22328),o(4959),o(62435);const i=(e,t,o=true)=>{if(!e||e===document.body)return null;if((e=e.assignedSlot??e).parentElement)e=e.parentElement;else{const t=e.getRootNode();e=t instanceof ShadowRoot?t.host:null}return(o?Object.prototype.hasOwnProperty.call(e,t):e&&t in e)?e:i(e,t,o)},a=(e,t,o=true)=>{const a=new Set;for(;e;)a.add(e),e=i(e,t,o);return a}},16582:(e,t,o)=>{o.d(t,{n:()=>i});const i=(e=document)=>e.activeElement?.shadowRoot?.activeElement?i(e.activeElement.shadowRoot):e.activeElement},61441:(e,t,o)=>{o.d(t,{E:()=>a,m:()=>i});const i=e=>{requestAnimationFrame((()=>setTimeout(e,0)))},a=()=>new Promise((e=>{i(e)}))},3276:(e,t,o)=>{o.d(t,{l:()=>p});var i=o(36312),a=o(68689),n=o(54653),r=o(34599),d=o(15112),s=o(77706),l=o(90952);o(28066);const c=["button","ha-list-item"],p=(e,t)=>d.qy` <div class="header_title"> <span>${t}</span> <ha-icon-button .label="${e?.localize("ui.dialogs.generic.close")??"Close"}" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}" dialogAction="close" class="header_button"></ha-icon-button> </div> `;(0,i.A)([(0,s.EM)("ha-dialog")],(function(e,t){class o extends t{constructor(...t){super(...t),e(this)}}return{F:o,d:[{kind:"field",key:l.Xr,value:void 0},{kind:"method",key:"scrollToPos",value:function(e,t){this.contentElement?.scrollTo(e,t)}},{kind:"method",key:"renderHeading",value:function(){return d.qy`<slot name="heading"> ${(0,a.A)(o,"renderHeading",this,3)([])} </slot>`}},{kind:"method",key:"firstUpdated",value:function(){(0,a.A)(o,"firstUpdated",this,3)([]),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,c].join(", "),this._updateScrolledAttribute(),this.contentElement?.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,a.A)(o,"disconnectedCallback",this,3)([]),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value(){return()=>{this._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value:()=>[r.R,d.AH`:host([scrolled]) ::slotted(ha-dialog-header){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.mdc-dialog{--mdc-dialog-scroll-divider-color:var(
          --dialog-scroll-divider-color,
          var(--divider-color)
        );z-index:var(--dialog-z-index,8);-webkit-backdrop-filter:var(--ha-dialog-scrim-backdrop-filter,var(--dialog-backdrop-filter,none));backdrop-filter:var(--ha-dialog-scrim-backdrop-filter,var(--dialog-backdrop-filter,none));--mdc-dialog-box-shadow:var(--dialog-box-shadow, none);--mdc-typography-headline6-font-weight:400;--mdc-typography-headline6-font-size:1.574rem}.mdc-dialog__actions{justify-content:var(--justify-action-buttons,flex-end);padding-bottom:max(env(safe-area-inset-bottom),24px)}.mdc-dialog__actions span:first-child{flex:var(--secondary-action-button-flex,unset)}.mdc-dialog__actions span:nth-child(2){flex:var(--primary-action-button-flex,unset)}.mdc-dialog__container{align-items:var(--vertical-align-dialog,center)}.mdc-dialog__title{padding:24px 24px 0 24px}.mdc-dialog__actions{padding:12px 24px 12px 24px}.mdc-dialog__title::before{content:unset}.mdc-dialog .mdc-dialog__content{position:var(--dialog-content-position,relative);padding:var(--dialog-content-padding,24px)}:host([hideactions]) .mdc-dialog .mdc-dialog__content{padding-bottom:max(var(--dialog-content-padding,24px),env(safe-area-inset-bottom))}.mdc-dialog .mdc-dialog__surface{position:var(--dialog-surface-position,relative);top:var(--dialog-surface-top);margin-top:var(--dialog-surface-margin-top);min-height:var(--mdc-dialog-min-height,auto);border-radius:var(--ha-dialog-border-radius,28px);-webkit-backdrop-filter:var(--ha-dialog-surface-backdrop-filter,none);backdrop-filter:var(--ha-dialog-surface-backdrop-filter,none);background:var(--ha-dialog-surface-background,var(--mdc-theme-surface,#fff))}:host([flexContent]) .mdc-dialog .mdc-dialog__content{display:flex;flex-direction:column}.header_title{position:relative;padding-right:40px;padding-inline-end:40px;padding-inline-start:initial;direction:var(--direction)}.header_title span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:block}.header_button{position:absolute;right:-12px;top:-12px;text-decoration:none;color:inherit;inset-inline-start:initial;inset-inline-end:-12px;direction:var(--direction)}.dialog-actions{inset-inline-start:initial!important;inset-inline-end:0px!important;direction:var(--direction)}`]}]}}),n.u)},72438:(e,t,o)=>{o.r(t),o.d(t,{HaImagecropperDialog:()=>p});var i=o(36312),a=(o(74860),o(71011),o(71174),o(72606),o(49048)),n=o.n(a),r=o(32609),d=o(15112),s=o(77706),l=o(85323),c=(o(3276),o(55321));let p=(0,i.A)([(0,s.EM)("image-cropper-dialog")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_open",value:()=>!1},{kind:"field",decorators:[(0,s.P)("img",!0)],key:"_image",value:void 0},{kind:"field",key:"_cropper",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._open=!0}},{kind:"method",key:"closeDialog",value:function(){this._open=!1,this._params=void 0,this._cropper?.destroy(),this._cropper=void 0}},{kind:"method",key:"updated",value:function(e){e.has("_params")&&this._params&&(this._cropper?this._cropper.replace(URL.createObjectURL(this._params.file)):(this._image.src=URL.createObjectURL(this._params.file),this._cropper=new(n())(this._image,{aspectRatio:this._params.options.aspectRatio,viewMode:1,dragMode:"move",minCropBoxWidth:50,ready:()=>{URL.revokeObjectURL(this._image.src)}})))}},{kind:"method",key:"render",value:function(){return d.qy`<ha-dialog @closed="${this.closeDialog}" scrimClickAction escapeKeyAction .open="${this._open}"> <div class="container ${(0,l.H)({round:Boolean(this._params?.options.round)})}"> <img alt="${this.hass.localize("ui.dialogs.image_cropper.crop_image")}"> </div> <mwc-button slot="secondaryAction" @click="${this.closeDialog}"> ${this.hass.localize("ui.common.cancel")} </mwc-button> <mwc-button slot="primaryAction" @click="${this._cropImage}"> ${this.hass.localize("ui.dialogs.image_cropper.crop")} </mwc-button> </ha-dialog>`}},{kind:"method",key:"_cropImage",value:function(){this._cropper.getCroppedCanvas().toBlob((e=>{if(!e)return;const t=new File([e],this._params.file.name,{type:this._params.options.type||this._params.file.type});this._params.croppedCallback(t),this.closeDialog()}),this._params.options.type||this._params.file.type,this._params.options.quality)}},{kind:"get",static:!0,key:"styles",value:function(){return[c.nA,d.AH`${(0,d.iz)(r)} .container{max-width:640px}img{max-width:100%}.container.round .cropper-face,.container.round .cropper-view-box{border-radius:50%}.cropper-line,.cropper-point,.cropper-point.point-se::before{background-color:var(--primary-color)}`]}}]}}),d.WF)},90952:(e,t,o)=>{o.d(t,{Xr:()=>s,oO:()=>p,ui:()=>l,zU:()=>c});var i=o(74005),a=o(64541);if(26240!=o.j)var n=o(16582);if(26240!=o.j)var r=o(61441);const d={},s=Symbol.for("HA focus target"),l=async(e,t,o,r,l,c=!0)=>{if(!(o in d)){if(!l)return!1;d[o]={element:l().then((()=>{const t=document.createElement(o);return e.provideHass(t),t}))}}if(i.G.history.state?.replaced?(d[o].closedFocusTargets=d[i.G.history.state.dialog].closedFocusTargets,delete d[i.G.history.state.dialog].closedFocusTargets):d[o].closedFocusTargets=(0,a.E)((0,n.n)(),s),c){i.G.history.replaceState({dialog:o,open:!1,oldState:i.G.history.state?.open&&i.G.history.state?.dialog!==o?i.G.history.state:null},"");try{i.G.history.pushState({dialog:o,dialogParams:r,open:!0},"")}catch(e){i.G.history.pushState({dialog:o,dialogParams:null,open:!0},"")}}const p=await d[o].element;return p.addEventListener("dialog-closed",h),t.appendChild(p),p.showDialog(r),!0},c=async e=>{if(!(e in d))return!0;const t=await d[e].element;return!t.closeDialog||!1!==t.closeDialog()},p=(e,t)=>{e.addEventListener("show-dialog",(o=>{const{dialogTag:i,dialogImport:a,dialogParams:n,addHistory:r}=o.detail;l(e,t,i,n,a,r)}))},h=async e=>{const t=d[e.detail.dialog].closedFocusTargets;if(delete d[e.detail.dialog].closedFocusTargets,!t)return;let o=(0,n.n)();o instanceof HTMLElement&&o.blur(),await(0,r.E)();for(const e of t)if(e instanceof HTMLElement&&(e.focus(),o=(0,n.n)(),o&&o!==document.body))return}}};
//# sourceMappingURL=72438.dsdQVXERHrs.js.map