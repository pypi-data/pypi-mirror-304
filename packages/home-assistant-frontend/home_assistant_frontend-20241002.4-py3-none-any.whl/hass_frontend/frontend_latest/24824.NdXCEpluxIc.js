export const id=24824;export const ids=[24824];export const modules={2443:(e,t,a)=>{a.r(t),a.d(t,{HuiStateBadgeElementEditor:()=>u});var i=a(36312),n=a(15112),o=a(77706),l=a(66419),s=a(34897),c=(a(36185),a(76914));const d=(0,l.Ik)({type:(0,l.eu)("state-badge"),entity:(0,l.lq)((0,l.Yj)()),style:(0,l.lq)((0,l.bz)()),title:(0,l.lq)((0,l.Yj)()),tap_action:(0,l.lq)(c.k),hold_action:(0,l.lq)(c.k),double_tap_action:(0,l.lq)(c.k)}),r=[{name:"entity",required:!0,selector:{entity:{}}},{name:"title",selector:{text:{}}},{name:"tap_action",selector:{ui_action:{}}},{name:"hold_action",selector:{ui_action:{}}},{name:"style",selector:{object:{}}}];let u=(0,i.A)([(0,o.EM)("hui-state-badge-element-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(e){(0,l.vA)(e,d),this._config=e}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?n.qy` <ha-form .hass="${this.hass}" .data="${this._config}" .schema="${r}" .computeLabel="${this._computeLabelCallback}" @value-changed="${this._valueChanged}"></ha-form> `:n.s6}},{kind:"method",key:"_valueChanged",value:function(e){(0,s.r)(this,"config-changed",{config:e.detail.value})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.lovelace.editor.card.generic.${e.name}`)||this.hass.localize(`ui.panel.lovelace.editor.elements.${e.name}`)||e.name}}]}}),n.WF)}};
//# sourceMappingURL=24824.NdXCEpluxIc.js.map