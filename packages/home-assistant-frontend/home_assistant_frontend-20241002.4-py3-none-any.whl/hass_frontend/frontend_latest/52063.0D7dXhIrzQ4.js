export const id=52063;export const ids=[52063,45346];export const modules={37456:(e,t,a)=>{a.d(t,{a:()=>o});const i=(0,a(58034).n)((e=>{history.replaceState({scrollPosition:e},"")}),300),o=e=>t=>({kind:"method",placement:"prototype",key:t.key,descriptor:{set(e){i(e),this[`__${String(t.key)}`]=e},get(){return this[`__${String(t.key)}`]||history.state?.scrollPosition},enumerable:!0,configurable:!0},finisher(a){const i=a.prototype.connectedCallback;a.prototype.connectedCallback=function(){i.call(this);const a=this[t.key];a&&this.updateComplete.then((()=>{const t=this.renderRoot.querySelector(e);t&&setTimeout((()=>{t.scrollTop=a}),0)}))}}})},58034:(e,t,a)=>{a.d(t,{n:()=>i});const i=(e,t,a=!0,i=!0)=>{let o,r=0;const n=(...n)=>{const s=()=>{r=!1===a?0:Date.now(),o=void 0,e(...n)},l=Date.now();r||!1!==a||(r=l);const c=t-(l-r);c<=0||c>t?(o&&(clearTimeout(o),o=void 0),r=l,e(...n)):o||!1===i||(o=window.setTimeout(s,c))};return n.cancel=()=>{clearTimeout(o),o=void 0,r=0},n}},13082:(e,t,a)=>{var i=a(36312),o=a(15112),r=a(77706);(0,i.A)([(0,r.EM)("ha-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)()],key:"header",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"raised",value:()=>!1},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`:host{background:var(--ha-card-background,var(--card-background-color,#fff));-webkit-backdrop-filter:var(--ha-card-backdrop-filter,none);backdrop-filter:var(--ha-card-backdrop-filter,none);box-shadow:var(--ha-card-box-shadow,none);box-sizing:border-box;border-radius:var(--ha-card-border-radius,12px);border-width:var(--ha-card-border-width,1px);border-style:solid;border-color:var(--ha-card-border-color,var(--divider-color,#e0e0e0));color:var(--primary-text-color);display:block;transition:all .3s ease-out;position:relative}:host([raised]){border:none;box-shadow:var(--ha-card-box-shadow,0px 2px 1px -1px rgba(0,0,0,.2),0px 1px 1px 0px rgba(0,0,0,.14),0px 1px 3px 0px rgba(0,0,0,.12))}.card-header,:host ::slotted(.card-header){color:var(--ha-card-header-color,--primary-text-color);font-family:var(--ha-card-header-font-family, inherit);font-size:var(--ha-card-header-font-size, 24px);letter-spacing:-.012em;line-height:48px;padding:12px 16px 16px;display:block;margin-block-start:0px;margin-block-end:0px;font-weight:400}:host ::slotted(.card-content:not(:first-child)),slot:not(:first-child)::slotted(.card-content){padding-top:0px;margin-top:-8px}:host ::slotted(.card-content){padding:16px}:host ::slotted(.card-actions){border-top:1px solid var(--divider-color,#e8e8e8);padding:5px 16px}`}},{kind:"method",key:"render",value:function(){return o.qy` ${this.header?o.qy`<h1 class="card-header">${this.header}</h1>`:o.s6} <slot></slot> `}}]}}),o.WF)},88725:(e,t,a)=>{var i=a(36312),o=a(41204),r=a(15565),n=a(15112),s=a(77706);(0,i.A)([(0,s.EM)("ha-checkbox")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",static:!0,key:"styles",value:()=>[r.R,n.AH`:host{--mdc-theme-secondary:var(--primary-color)}`]}]}}),o.L)},45346:(e,t,a)=>{a.r(t),a.d(t,{HaIconButtonArrowPrev:()=>s});var i=a(36312),o=a(15112),r=a(77706),n=a(74005);a(28066);let s=(0,i.A)([(0,r.EM)("ha-icon-button-arrow-prev")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_icon",value:()=>"rtl"===n.G.document.dir?"M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z":"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"},{kind:"method",key:"render",value:function(){return o.qy` <ha-icon-button .disabled="${this.disabled}" .label="${this.label||this.hass?.localize("ui.common.back")||"Back"}" .path="${this._icon}"></ha-icon-button> `}}]}}),o.WF)},28066:(e,t,a)=>{a.r(t),a.d(t,{HaIconButton:()=>s});var i=a(36312),o=(a(20931),a(15112)),r=a(77706),n=a(10977);a(88400);let s=(0,i.A)([(0,r.EM)("ha-icon-button")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,r.MZ)({type:String})],key:"path",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:String})],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:String,attribute:"aria-haspopup"})],key:"ariaHasPopup",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"hideTitle",value:()=>!1},{kind:"field",decorators:[(0,r.P)("mwc-icon-button",!0)],key:"_button",value:void 0},{kind:"method",key:"focus",value:function(){this._button?.focus()}},{kind:"field",static:!0,key:"shadowRootOptions",value:()=>({mode:"open",delegatesFocus:!0})},{kind:"method",key:"render",value:function(){return o.qy` <mwc-icon-button aria-label="${(0,n.J)(this.label)}" title="${(0,n.J)(this.hideTitle?void 0:this.label)}" aria-haspopup="${(0,n.J)(this.ariaHasPopup)}" .disabled="${this.disabled}"> ${this.path?o.qy`<ha-svg-icon .path="${this.path}"></ha-svg-icon>`:o.qy`<slot></slot>`} </mwc-icon-button> `}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`:host{display:inline-block;outline:0}:host([disabled]){pointer-events:none}mwc-icon-button{--mdc-theme-on-primary:currentColor;--mdc-theme-text-disabled-on-light:var(--disabled-text-color)}`}}]}}),o.WF)},11804:(e,t,a)=>{var i=a(36312),o=a(68689),r=a(15112),n=a(77706),s=a(34897),l=a(77679);a(28066);(0,i.A)([(0,n.EM)("ha-menu-button")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"hassio",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_hasNotifications",value:()=>!1},{kind:"field",decorators:[(0,n.wk)()],key:"_show",value:()=>!1},{kind:"field",key:"_alwaysVisible",value:()=>!1},{kind:"field",key:"_attachNotifOnConnect",value:()=>!1},{kind:"field",key:"_unsubNotifications",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,o.A)(a,"connectedCallback",this,3)([]),this._attachNotifOnConnect&&(this._attachNotifOnConnect=!1,this._subscribeNotifications())}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.A)(a,"disconnectedCallback",this,3)([]),this._unsubNotifications&&(this._attachNotifOnConnect=!0,this._unsubNotifications(),this._unsubNotifications=void 0)}},{kind:"method",key:"render",value:function(){if(!this._show)return r.s6;const e=this._hasNotifications&&(this.narrow||"always_hidden"===this.hass.dockedSidebar);return r.qy` <ha-icon-button .label="${this.hass.localize("ui.sidebar.sidebar_toggle")}" .path="${"M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z"}" @click="${this._toggleMenu}"></ha-icon-button> ${e?r.qy`<div class="dot"></div>`:""} `}},{kind:"method",key:"firstUpdated",value:function(e){(0,o.A)(a,"firstUpdated",this,3)([e]),this.hassio&&(this._alwaysVisible=(Number(window.parent.frontendVersion)||0)<20190710)}},{kind:"method",key:"willUpdate",value:function(e){if((0,o.A)(a,"willUpdate",this,3)([e]),!e.has("narrow")&&!e.has("hass"))return;const t=e.has("hass")?e.get("hass"):this.hass,i=(e.has("narrow")?e.get("narrow"):this.narrow)||"always_hidden"===t?.dockedSidebar,r=this.narrow||"always_hidden"===this.hass.dockedSidebar;this.hasUpdated&&i===r||(this._show=r||this._alwaysVisible,r?this._subscribeNotifications():this._unsubNotifications&&(this._unsubNotifications(),this._unsubNotifications=void 0))}},{kind:"method",key:"_subscribeNotifications",value:function(){if(this._unsubNotifications)throw new Error("Already subscribed");this._unsubNotifications=(0,l.V)(this.hass.connection,(e=>{this._hasNotifications=e.length>0}))}},{kind:"method",key:"_toggleMenu",value:function(){(0,s.r)(this,"hass-toggle-menu")}},{kind:"get",static:!0,key:"styles",value:function(){return r.AH`:host{position:relative}.dot{pointer-events:none;position:absolute;background-color:var(--accent-color);width:12px;height:12px;top:9px;right:7px;inset-inline-end:7px;inset-inline-start:initial;border-radius:50%;border:2px solid var(--app-header-background-color)}`}}]}}),r.WF)},24640:(e,t,a)=>{var i=a(36312),o=a(15112),r=a(77706);(0,i.A)([(0,r.EM)("ha-settings-row")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,attribute:"three-line"})],key:"threeLine",value:()=>!1},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,attribute:"wrap-heading",reflect:!0})],key:"wrapHeading",value:()=>!1},{kind:"method",key:"render",value:function(){return o.qy` <div class="prefix-wrap"> <slot name="prefix"></slot> <div class="body" ?two-line="${!this.threeLine}" ?three-line="${this.threeLine}"> <slot name="heading"></slot> <div class="secondary"><slot name="description"></slot></div> </div> </div> <div class="content"><slot></slot></div> `}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`:host{display:flex;padding:0 16px;align-content:normal;align-self:auto;align-items:center}.body{padding-top:8px;padding-bottom:8px;padding-left:0;padding-inline-start:0;padding-right:16x;padding-inline-end:16px;overflow:hidden;display:var(--layout-vertical_-_display);flex-direction:var(--layout-vertical_-_flex-direction);justify-content:var(--layout-center-justified_-_justify-content);flex:var(--layout-flex_-_flex);flex-basis:var(--layout-flex_-_flex-basis)}.body[three-line]{min-height:var(--paper-item-body-three-line-min-height,88px)}:host(:not([wrap-heading])) body>*{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.body>.secondary{display:block;padding-top:4px;font-family:var(
          --mdc-typography-body2-font-family,
          var(--mdc-typography-font-family, Roboto, sans-serif)
        );-webkit-font-smoothing:antialiased;font-size:var(--mdc-typography-body2-font-size, .875rem);font-weight:var(--mdc-typography-body2-font-weight,400);line-height:normal;color:var(--secondary-text-color)}.body[two-line]{min-height:calc(var(--paper-item-body-two-line-min-height,72px) - 16px);flex:1}.content{display:contents}:host(:not([narrow])) .content{display:var(--settings-row-content-display,flex);justify-content:flex-end;flex:1;padding:16px 0}.content ::slotted(*){width:var(--settings-row-content-width)}:host([narrow]){align-items:normal;flex-direction:column;border-top:1px solid var(--divider-color);padding-bottom:8px}::slotted(ha-switch){padding:16px 0}.secondary{white-space:normal}.prefix-wrap{display:var(--settings-row-prefix-display)}:host([narrow]) .prefix-wrap{display:flex;align-items:center}`}}]}}),o.WF)},88400:(e,t,a)=>{a.r(t),a.d(t,{HaSvgIcon:()=>n});var i=a(36312),o=a(15112),r=a(77706);let n=(0,i.A)([(0,r.EM)("ha-svg-icon")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)()],key:"path",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"secondaryPath",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"viewBox",value:void 0},{kind:"method",key:"render",value:function(){return o.JW` <svg viewBox="${this.viewBox||"0 0 24 24"}" preserveAspectRatio="xMidYMid meet" focusable="false" role="img" aria-hidden="true"> <g> ${this.path?o.JW`<path class="primary-path" d="${this.path}"></path>`:o.s6} ${this.secondaryPath?o.JW`<path class="secondary-path" d="${this.secondaryPath}"></path>`:o.s6} </g> </svg>`}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`:host{display:var(--ha-icon-display,inline-flex);align-items:center;justify-content:center;position:relative;vertical-align:middle;fill:var(--icon-primary-color,currentcolor);width:var(--mdc-icon-size,24px);height:var(--mdc-icon-size,24px)}svg{width:100%;height:100%;pointer-events:none;display:block}path.primary-path{opacity:var(--icon-primary-opactity, 1)}path.secondary-path{fill:var(--icon-secondary-color,currentcolor);opacity:var(--icon-secondary-opactity, .5)}`}}]}}),o.WF)},59588:(e,t,a)=>{var i=a(36312),o=a(68689),r=a(71204),n=a(15031),s=a(15112),l=a(77706),c=a(39914);(0,i.A)([(0,l.EM)("ha-switch")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"haptic",value:()=>!1},{kind:"method",key:"firstUpdated",value:function(){(0,o.A)(a,"firstUpdated",this,3)([]),this.addEventListener("change",(()=>{this.haptic&&(0,c.j)("light")}))}},{kind:"field",static:!0,key:"styles",value:()=>[n.R,s.AH`:host{--mdc-theme-secondary:var(--switch-checked-color)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:var(--switch-checked-button-color);border-color:var(--switch-checked-button-color)}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:var(--switch-checked-track-color);border-color:var(--switch-checked-track-color)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:var(--switch-unchecked-button-color);border-color:var(--switch-unchecked-button-color)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:var(--switch-unchecked-track-color);border-color:var(--switch-unchecked-track-color)}`]}]}}),r.U)},77679:(e,t,a)=>{a.d(t,{V:()=>i});const i=(e,t)=>{const a=new o,i=e.subscribeMessage((e=>t(a.processMessage(e))),{type:"persistent_notification/subscribe"});return()=>{i.then((e=>e?.()))}};class o{constructor(){this.notifications=void 0,this.notifications={}}processMessage(e){if("removed"===e.type)for(const t of Object.keys(e.notifications))delete this.notifications[t];else this.notifications={...this.notifications,...e.notifications};return Object.values(this.notifications)}}},77980:(e,t,a)=>{var i=a(36312),o=a(15112),r=a(77706),n=a(37456),s=(a(45346),a(11804),a(55321));(0,i.A)([(0,r.EM)("hass-subpage")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"header",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,attribute:"main-page"})],key:"mainPage",value:()=>!1},{kind:"field",decorators:[(0,r.MZ)({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"backCallback",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"supervisor",value:()=>!1},{kind:"field",decorators:[(0,n.a)(".content")],key:"_savedScrollPos",value:void 0},{kind:"method",key:"render",value:function(){return o.qy` <div class="toolbar"> ${this.mainPage||history.state?.root?o.qy` <ha-menu-button .hassio="${this.supervisor}" .hass="${this.hass}" .narrow="${this.narrow}"></ha-menu-button> `:this.backPath?o.qy` <a href="${this.backPath}"> <ha-icon-button-arrow-prev .hass="${this.hass}"></ha-icon-button-arrow-prev> </a> `:o.qy` <ha-icon-button-arrow-prev .hass="${this.hass}" @click="${this._backTapped}"></ha-icon-button-arrow-prev> `} <div class="main-title"><slot name="header">${this.header}</slot></div> <slot name="toolbar-icon"></slot> </div> <div class="content ha-scrollbar" @scroll="${this._saveScrollPos}"> <slot></slot> </div> <div id="fab"> <slot name="fab"></slot> </div> `}},{kind:"method",decorators:[(0,r.Ls)({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"method",key:"_backTapped",value:function(){this.backCallback?this.backCallback():history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return[s.dp,o.AH`:host{display:block;height:100%;background-color:var(--primary-background-color);overflow:hidden;position:relative}:host([narrow]){width:100%;position:fixed}.toolbar{display:flex;align-items:center;font-size:20px;height:var(--header-height);padding:8px 12px;background-color:var(--app-header-background-color);font-weight:400;color:var(--app-header-text-color,#fff);border-bottom:var(--app-header-border-bottom,none);box-sizing:border-box}@media (max-width:599px){.toolbar{padding:4px}}.toolbar a{color:var(--sidebar-text-color);text-decoration:none}::slotted([slot=toolbar-icon]),ha-icon-button-arrow-prev,ha-menu-button{pointer-events:auto;color:var(--sidebar-icon-color)}.main-title{margin:var(--margin-title);line-height:20px;flex-grow:1}.content{position:relative;width:100%;height:calc(100% - 1px - var(--header-height));overflow-y:auto;overflow:auto;-webkit-overflow-scrolling:touch}#fab{position:absolute;right:calc(16px + env(safe-area-inset-right));inset-inline-end:calc(16px + env(safe-area-inset-right));inset-inline-start:initial;bottom:calc(16px + env(safe-area-inset-bottom));z-index:1;display:flex;flex-wrap:wrap;justify-content:flex-end;gap:8px}:host([narrow]) #fab.tabs{bottom:calc(84px + env(safe-area-inset-bottom))}#fab[is-wide]{bottom:24px;right:24px;inset-inline-end:24px;inset-inline-start:initial}`]}}]}}),o.WF)},63836:(e,t,a)=>{var i=a(36312),o=a(68689),r=(a(72606),a(15112)),n=a(77706),s=a(33922),l=(a(253),a(54846),a(7986),a(34897)),c=a(55321);a(24640),a(59588);const d=["usage","statistics"];(0,i.A)([(0,n.EM)("ha-analytics")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"localize",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"analytics",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"translation_key_panel"})],key:"translationKeyPanel",value:()=>"config"},{kind:"method",key:"render",value:function(){const e=void 0===this.analytics,t=!e&&this.analytics.preferences.base;return r.qy` <ha-settings-row> <span slot="heading" data-for="base"> ${this.localize(`ui.panel.${this.translationKeyPanel}.analytics.preferences.base.title`)} </span> <span slot="description" data-for="base"> ${this.localize(`ui.panel.${this.translationKeyPanel}.analytics.preferences.base.description`)} </span> <ha-switch @change="${this._handleRowClick}" .checked="${t}" .preference="${"base"}" .disabled="${e}" name="base"> </ha-switch> </ha-settings-row> ${d.map((e=>r.qy` <ha-settings-row> <span slot="heading" data-for="${e}"> ${this.localize(`ui.panel.${this.translationKeyPanel}.analytics.preferences.${e}.title`)} </span> <span slot="description" data-for="${e}"> ${this.localize(`ui.panel.${this.translationKeyPanel}.analytics.preferences.${e}.description`)} </span> <span> <ha-switch @change="${this._handleRowClick}" .checked="${this.analytics?.preferences[e]}" .preference="${e}" name="${e}"> </ha-switch> ${t?"":r.qy` <simple-tooltip animation-delay="0" position="right"> ${this.localize(`ui.panel.${this.translationKeyPanel}.analytics.need_base_enabled`)} </simple-tooltip> `} </span> </ha-settings-row> `))} <ha-settings-row> <span slot="heading" data-for="diagnostics"> ${this.localize(`ui.panel.${this.translationKeyPanel}.analytics.preferences.diagnostics.title`)} </span> <span slot="description" data-for="diagnostics"> ${this.localize(`ui.panel.${this.translationKeyPanel}.analytics.preferences.diagnostics.description`)} </span> <ha-switch @change="${this._handleRowClick}" .checked="${this.analytics?.preferences.diagnostics}" .preference="${"diagnostics"}" .disabled="${e}" name="diagnostics"> </ha-switch> </ha-settings-row> `}},{kind:"method",key:"updated",value:function(e){(0,o.A)(a,"updated",this,3)([e]),this.shadowRoot.querySelectorAll("*[data-for]").forEach((e=>{const t=e.dataset.for;delete e.dataset.for,e.addEventListener("click",(()=>{const e=this.shadowRoot.querySelector(`*[name=${t}]`);e&&(e.focus(),e.click())}))}))}},{kind:"method",key:"_handleRowClick",value:function(e){const t=e.currentTarget,a=t.preference,i=this.analytics?{...this.analytics.preferences}:{};i[a]!==t.checked&&(i[a]=t.checked,d.some((e=>e===a))&&t.checked?i.base=!0:"base"!==a||t.checked||(i.usage=!1,i.statistics=!1),(0,l.r)(this,"analytics-preferences-changed",{preferences:i}))}},{kind:"get",static:!0,key:"styles",value:function(){return[c.RF,r.AH`.error{color:var(--error-color)}ha-settings-row{padding:0}span[slot=description],span[slot=heading]{cursor:pointer}`]}}]}}),r.WF);a(13082),a(88725);var h=a(84976);(0,i.A)([(0,n.EM)("ha-config-analytics")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_analyticsDetails",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_error",value:void 0},{kind:"method",key:"render",value:function(){const e=this._error?this._error:(0,s.x)(this.hass,"analytics")?void 0:"Analytics integration not loaded";return r.qy` <ha-card outlined> <div class="card-content"> ${e?r.qy`<div class="error">${e}</div>`:""} <p>${this.hass.localize("ui.panel.config.analytics.intro")}</p> <ha-analytics translation_key_panel="config" @analytics-preferences-changed="${this._preferencesChanged}" .localize="${this.hass.localize}" .analytics="${this._analyticsDetails}"></ha-analytics> </div> <div class="card-actions"> <mwc-button @click="${this._save}"> ${this.hass.localize("ui.panel.config.core.section.core.core_config.save_button")} </mwc-button> </div> </ha-card> <div class="footer"> <a .href="${(0,h.o)(this.hass,"/integrations/analytics/")}" target="_blank" rel="noreferrer"> ${this.hass.localize("ui.panel.config.analytics.learn_more")} </a> </div> `}},{kind:"method",key:"firstUpdated",value:function(e){(0,o.A)(a,"firstUpdated",this,3)([e]),(0,s.x)(this.hass,"analytics")&&this._load()}},{kind:"method",key:"_load",value:async function(){this._error=void 0;try{this._analyticsDetails=await(e=this.hass,e.callWS({type:"analytics"}))}catch(e){this._error=e.message||e}var e}},{kind:"method",key:"_save",value:async function(){this._error=void 0;try{await(e=this.hass,t=this._analyticsDetails?.preferences||{},e.callWS({type:"analytics/preferences",preferences:t}))}catch(e){this._error=e.message||e}var e,t}},{kind:"method",key:"_preferencesChanged",value:function(e){this._analyticsDetails={...this._analyticsDetails,preferences:e.detail.preferences}}},{kind:"get",static:!0,key:"styles",value:function(){return[c.RF,r.AH`.error{color:var(--error-color)}ha-settings-row{padding:0}p{margin-top:0}.card-actions{display:flex;flex-direction:row-reverse;justify-content:space-between;align-items:center}.footer{padding:32px 0 16px;text-align:center}`]}}]}}),r.WF)},55321:(e,t,a)=>{a.d(t,{RF:()=>r,dp:()=>s,nA:()=>n,og:()=>o});var i=a(15112);const o=i.AH`button.link{background:0 0;color:inherit;border:none;padding:0;font:inherit;text-align:left;text-decoration:underline;cursor:pointer;outline:0}`,r=i.AH`:host{font-family:var(--paper-font-body1_-_font-family);-webkit-font-smoothing:var(--paper-font-body1_-_-webkit-font-smoothing);font-size:var(--paper-font-body1_-_font-size);font-weight:var(--paper-font-body1_-_font-weight);line-height:var(--paper-font-body1_-_line-height)}app-header div[sticky]{height:48px}app-toolbar [main-title]{margin-left:20px;margin-inline-start:20px;margin-inline-end:initial}h1{font-family:var(--paper-font-headline_-_font-family);-webkit-font-smoothing:var(--paper-font-headline_-_-webkit-font-smoothing);white-space:var(--paper-font-headline_-_white-space);overflow:var(--paper-font-headline_-_overflow);text-overflow:var(--paper-font-headline_-_text-overflow);font-size:var(--paper-font-headline_-_font-size);font-weight:var(--paper-font-headline_-_font-weight);line-height:var(--paper-font-headline_-_line-height)}h2{font-family:var(--paper-font-title_-_font-family);-webkit-font-smoothing:var(--paper-font-title_-_-webkit-font-smoothing);white-space:var(--paper-font-title_-_white-space);overflow:var(--paper-font-title_-_overflow);text-overflow:var(--paper-font-title_-_text-overflow);font-size:var(--paper-font-title_-_font-size);font-weight:var(--paper-font-title_-_font-weight);line-height:var(--paper-font-title_-_line-height)}h3{font-family:var(--paper-font-subhead_-_font-family);-webkit-font-smoothing:var(--paper-font-subhead_-_-webkit-font-smoothing);white-space:var(--paper-font-subhead_-_white-space);overflow:var(--paper-font-subhead_-_overflow);text-overflow:var(--paper-font-subhead_-_text-overflow);font-size:var(--paper-font-subhead_-_font-size);font-weight:var(--paper-font-subhead_-_font-weight);line-height:var(--paper-font-subhead_-_line-height)}a{color:var(--primary-color)}.secondary{color:var(--secondary-text-color)}.error{color:var(--error-color)}.warning{color:var(--error-color)}ha-button.warning,mwc-button.warning{--mdc-theme-primary:var(--error-color)}${o} .card-actions a{text-decoration:none}.card-actions .warning{--mdc-theme-primary:var(--error-color)}.layout.horizontal,.layout.vertical{display:flex}.layout.inline{display:inline-flex}.layout.horizontal{flex-direction:row}.layout.vertical{flex-direction:column}.layout.wrap{flex-wrap:wrap}.layout.no-wrap{flex-wrap:nowrap}.layout.center,.layout.center-center{align-items:center}.layout.bottom{align-items:flex-end}.layout.center-center,.layout.center-justified{justify-content:center}.flex{flex:1;flex-basis:0.000000001px}.flex-auto{flex:1 1 auto}.flex-none{flex:none}.layout.justified{justify-content:space-between}`,n=i.AH`ha-dialog{--mdc-dialog-min-width:400px;--mdc-dialog-max-width:600px;--mdc-dialog-max-width:min(600px, 95vw);--justify-action-buttons:space-between}ha-dialog .form{color:var(--primary-text-color)}a{color:var(--primary-color)}@media all and (max-width:450px),all and (max-height:500px){ha-dialog{--mdc-dialog-min-width:calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );--mdc-dialog-max-width:calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );--mdc-dialog-min-height:100%;--mdc-dialog-max-height:100%;--vertical-align-dialog:flex-end;--ha-dialog-border-radius:0}}ha-button.warning,mwc-button.warning{--mdc-theme-primary:var(--error-color)}.error{color:var(--error-color)}`,s=i.AH`.ha-scrollbar::-webkit-scrollbar{width:.4rem;height:.4rem}.ha-scrollbar::-webkit-scrollbar-thumb{-webkit-border-radius:4px;border-radius:4px;background:var(--scrollbar-thumb-color)}.ha-scrollbar{overflow-y:auto;scrollbar-color:var(--scrollbar-thumb-color) transparent;scrollbar-width:thin}`;i.AH`body{background-color:var(--primary-background-color);color:var(--primary-text-color);height:calc(100vh - 32px);width:100vw}`},84976:(e,t,a)=>{a.d(t,{o:()=>i});const i=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`}};
//# sourceMappingURL=52063.0D7dXhIrzQ4.js.map