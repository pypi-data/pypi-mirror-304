"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[58308],{58308:function(e,t,a){a.r(t),a.d(t,{HuiAlarmPanelCardEditor:function(){return g}});var n,i=a(64599),s=a(35806),l=a(71008),r=a(62193),o=a(2816),c=a(27927),u=(a(81027),a(13025),a(82386),a(97741),a(50693),a(26098),a(10507),a(39790),a(36604),a(253),a(2075),a(16891),a(15112)),d=a(29818),h=a(94100),f=a(66419),m=a(34897),v=(a(36185),a(56124)),_=a(34971),p=a(42496),k=a(84540),y=(0,f.kp)(v.H,(0,f.Ik)({entity:(0,f.lq)((0,f.Yj)()),name:(0,f.lq)((0,f.Yj)()),states:(0,f.lq)((0,f.YO)()),theme:(0,f.lq)((0,f.Yj)())})),A=Object.keys(_.ALARM_MODE_STATE_MAP),g=(0,c.A)([(0,d.EM)("hui-alarm-panel-card-editor")],(function(e,t){var a=function(t){function a(){var t;(0,l.A)(this,a);for(var n=arguments.length,i=new Array(n),s=0;s<n;s++)i[s]=arguments[s];return t=(0,r.A)(this,a,[].concat(i)),e(t),t}return(0,o.A)(a,t),(0,s.A)(a)}(t);return{F:a,d:[{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.wk)()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(e){(0,f.vA)(e,y),this._config=e}},{kind:"field",key:"_schema",value:function(){return(0,h.A)((function(e,t,a){return[{name:"entity",required:!0,selector:{entity:{domain:"alarm_control_panel"}}},{type:"grid",name:"",schema:[{name:"name",selector:{text:{}}},{name:"theme",selector:{theme:{}}}]},{name:"states",selector:{select:{multiple:!0,mode:"list",options:A.map((function(n){return{value:n,label:e("ui.card.alarm_control_panel.".concat(n)),disabled:!(a.includes(n)||t&&(0,p.$)(t,k.t[_.ALARM_MODE_STATE_MAP[n]].feature||0))}}))}}}]}))}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return u.s6;var e=this.hass.states[this._config.entity],t=(0,_.filterSupportedAlarmStates)(e,_.DEFAULT_STATES),a=Object.assign({states:t},this._config);return(0,u.qy)(n||(n=(0,i.A)([' <ha-form .hass="','" .data="','" .schema="','" .computeLabel="','" @value-changed="','"></ha-form> '])),this.hass,a,this._schema(this.hass.localize,e,a.states),this._computeLabelCallback,this._valueChanged)}},{kind:"method",key:"_valueChanged",value:function(e){var t,a=e.detail.value;if(a.states){var n=A.filter((function(e){return a.states.includes(e)}));a.states=n}if(a.states&&a.entity!==(null===(t=this._config)||void 0===t?void 0:t.entity)){var i,s=null===(i=this.hass)||void 0===i?void 0:i.states[a.entity];s&&(a.states=(0,_.filterSupportedAlarmStates)(s,a.states))}(0,m.r)(this,"config-changed",{config:a})}},{kind:"field",key:"_computeLabelCallback",value:function(){var e=this;return function(t){switch(t.name){case"entity":return e.hass.localize("ui.panel.lovelace.editor.card.generic.entity");case"name":return e.hass.localize("ui.panel.lovelace.editor.card.generic.name");case"theme":return"".concat(e.hass.localize("ui.panel.lovelace.editor.card.generic.theme")," (").concat(e.hass.localize("ui.panel.lovelace.editor.card.config.optional"),")");default:return e.hass.localize("ui.panel.lovelace.editor.card.alarm-panel.available_states")}}}}]}}),u.WF)},56124:function(e,t,a){a.d(t,{H:function(){return i}});var n=a(66419),i=(0,n.Ik)({type:(0,n.Yj)(),view_layout:(0,n.bz)(),layout_options:(0,n.bz)(),visibility:(0,n.bz)()})}}]);
//# sourceMappingURL=58308.PQprTKb0mEM.js.map