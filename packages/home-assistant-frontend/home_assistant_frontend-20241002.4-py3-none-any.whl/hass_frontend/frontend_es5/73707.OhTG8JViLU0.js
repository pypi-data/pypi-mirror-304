"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[73707],{66018:function(e,t,i){var n=i(22858).A,a=i(33994).A;i.a(e,function(){var e=n(a().mark((function e(t,n){var r,c,s,o,l,d,u,h,v,f,y,g,k,p,m,_,b,H,x,A,M,V,q,j,w,Y;return a().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(e.prev=0,r=i(33994),c=i(22858),s=i(64599),o=i(35806),l=i(71008),d=i(62193),u=i(2816),h=i(27927),v=i(81027),f=i(95737),y=i(97099),g=i(26098),k=i(39790),p=i(7760),m=i(99019),_=i(15129),b=i(96858),H=i(15112),x=i(29818),A=i(66066),M=i(34897),V=i(94548),i(28066),i(24260),!(q=t([V])).then){e.next=42;break}return e.next=38,q;case 38:e.t1=e.sent,e.t0=(0,e.t1)(),e.next=43;break;case 42:e.t0=q;case 43:V=e.t0[0],(0,h.A)([(0,x.EM)("hui-entity-editor")],(function(e,t){var i,n=function(t){function i(){var t;(0,l.A)(this,i);for(var n=arguments.length,a=new Array(n),r=0;r<n;r++)a[r]=arguments[r];return t=(0,d.A)(this,i,[].concat(a)),e(t),t}return(0,u.A)(i,t),(0,o.A)(i)}(t);return{F:n,d:[{kind:"field",decorators:[(0,x.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,x.MZ)({attribute:!1})],key:"entities",value:void 0},{kind:"field",decorators:[(0,x.MZ)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"field",decorators:[(0,x.MZ)()],key:"label",value:void 0},{kind:"field",key:"_entityKeys",value:function(){return new WeakMap}},{kind:"method",key:"_getKey",value:function(e){return this._entityKeys.has(e)||this._entityKeys.set(e,Math.random().toString()),this._entityKeys.get(e)}},{kind:"method",key:"render",value:function(){var e=this;return this.entities?(0,H.qy)(j||(j=(0,s.A)([" <h3> ",' </h3> <ha-sortable handle-selector=".handle" @item-moved="','"> <div class="entities"> ',' </div> </ha-sortable> <ha-entity-picker class="add-entity" .hass="','" .entityFilter="','" @value-changed="','"></ha-entity-picker> '])),this.label||this.hass.localize("ui.panel.lovelace.editor.card.generic.entities")+" ("+this.hass.localize("ui.panel.lovelace.editor.card.config.required")+")",this._entityMoved,(0,A.u)(this.entities,(function(t){return e._getKey(t)}),(function(t,i){return(0,H.qy)(w||(w=(0,s.A)([' <div class="entity" data-entity-id="','"> <div class="handle"> <ha-svg-icon .path="','"></ha-svg-icon> </div> <ha-entity-picker .hass="','" .value="','" .index="','" .entityFilter="','" @value-changed="','" allow-custom-entity></ha-entity-picker> </div> '])),t.entity,"M7,19V17H9V19H7M11,19V17H13V19H11M15,19V17H17V19H15M7,15V13H9V15H7M11,15V13H13V15H11M15,15V13H17V15H15M7,11V9H9V11H7M11,11V9H13V11H11M15,11V9H17V11H15M7,7V5H9V7H7M11,7V5H13V7H11M15,7V5H17V7H15Z",e.hass,t.entity,i,e.entityFilter,e._valueChanged)})),this.hass,this.entityFilter,this._addEntity):H.s6}},{kind:"method",key:"_addEntity",value:(i=(0,c.A)((0,r.A)().mark((function e(t){var i,n;return(0,r.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(""!==(i=t.detail.value)){e.next=3;break}return e.abrupt("return");case 3:n=this.entities.concat({entity:i}),t.target.value="",(0,M.r)(this,"entities-changed",{entities:n});case 6:case"end":return e.stop()}}),e,this)}))),function(e){return i.apply(this,arguments)})},{kind:"method",key:"_entityMoved",value:function(e){e.stopPropagation();var t=e.detail,i=t.oldIndex,n=t.newIndex,a=this.entities.concat();a.splice(n,0,a.splice(i,1)[0]),(0,M.r)(this,"entities-changed",{entities:a})}},{kind:"method",key:"_valueChanged",value:function(e){var t=e.detail.value,i=e.target.index,n=this.entities.concat();""===t||void 0===t?n.splice(i,1):n[i]=Object.assign(Object.assign({},n[i]),{},{entity:t}),(0,M.r)(this,"entities-changed",{entities:n})}},{kind:"get",static:!0,key:"styles",value:function(){return(0,H.AH)(Y||(Y=(0,s.A)(["ha-entity-picker{margin-top:8px}.add-entity{display:block;margin-left:31px;margin-inline-start:31px;margin-inline-end:initial;direction:var(--direction)}.entity{display:flex;align-items:center}.entity .handle{padding-right:8px;cursor:move;cursor:grab;padding-inline-end:8px;padding-inline-start:initial;direction:var(--direction)}.entity .handle>*{pointer-events:none}.entity ha-entity-picker{flex-grow:1}"])))}}]}}),H.WF),n(),e.next=52;break;case 49:e.prev=49,e.t2=e.catch(0),n(e.t2);case 52:case"end":return e.stop()}}),e,null,[[0,49]])})));return function(t,i){return e.apply(this,arguments)}}())},45003:function(e,t,i){i.d(t,{j:function(){return n}});var n=["relative","total","date","time","datetime"]},73707:function(e,t,i){var n=i(22858).A,a=i(33994).A;i.a(e,function(){var e=n(a().mark((function e(n,r){var c,s,o,l,d,u,h,v,f,y,g,k,p,m,_,b,H,x,A,M,V,q,j,w;return a().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(e.prev=0,i.r(t),i.d(t,{HuiPictureGlanceCardEditor:function(){return w}}),c=i(64599),s=i(35806),o=i(71008),l=i(62193),d=i(2816),u=i(27927),h=i(81027),v=i(50693),f=i(26098),y=i(15112),g=i(29818),k=i(66419),p=i(34897),i(36185),m=i(66018),_=i(66028),b=i(76914),H=i(56124),x=i(93161),A=i(3532),!(M=n([m])).then){e.next=34;break}return e.next=30,M;case 30:e.t1=e.sent,e.t0=(0,e.t1)(),e.next=35;break;case 34:e.t0=M;case 35:m=e.t0[0],q=(0,k.kp)(H.H,(0,k.Ik)({title:(0,k.lq)((0,k.Yj)()),entity:(0,k.lq)((0,k.Yj)()),image:(0,k.lq)((0,k.Yj)()),image_entity:(0,k.lq)((0,k.Yj)()),camera_image:(0,k.lq)((0,k.Yj)()),camera_view:(0,k.lq)((0,k.Yj)()),aspect_ratio:(0,k.lq)((0,k.Yj)()),tap_action:(0,k.lq)(b.k),hold_action:(0,k.lq)(b.k),entities:(0,k.YO)(x.l),theme:(0,k.lq)((0,k.Yj)())})),j=[{name:"title",selector:{text:{}}},{name:"image",selector:{image:{}}},{name:"image_entity",selector:{entity:{domain:["image","person"]}}},{name:"camera_image",selector:{entity:{domain:"camera"}}},{name:"",type:"grid",schema:[{name:"camera_view",selector:{select:{options:["auto","live"]}}},{name:"aspect_ratio",selector:{text:{}}}]},{name:"entity",selector:{entity:{}}},{name:"theme",selector:{theme:{}}},{name:"tap_action",selector:{ui_action:{}}},{name:"hold_action",selector:{ui_action:{}}}],w=(0,u.A)([(0,g.EM)("hui-picture-glance-card-editor")],(function(e,t){var i=function(t){function i(){var t;(0,o.A)(this,i);for(var n=arguments.length,a=new Array(n),r=0;r<n;r++)a[r]=arguments[r];return t=(0,l.A)(this,i,[].concat(a)),e(t),t}return(0,d.A)(i,t),(0,s.A)(i)}(t);return{F:i,d:[{kind:"field",decorators:[(0,g.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,g.wk)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,g.wk)()],key:"_configEntities",value:void 0},{kind:"method",key:"setConfig",value:function(e){(0,k.vA)(e,q),this._config=e,this._configEntities=(0,_._)(e.entities)}},{kind:"get",key:"_tap_action",value:function(){return this._config.tap_action||{action:"toggle"}}},{kind:"get",key:"_hold_action",value:function(){return this._config.hold_action||{action:"more-info"}}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return y.s6;var e=Object.assign({camera_view:"auto"},this._config);return(0,y.qy)(V||(V=(0,c.A)([' <ha-form .hass="','" .data="','" .schema="','" .computeLabel="','" @value-changed="','"></ha-form> <div class="card-config"> <hui-entity-editor .hass="','" .entities="','" @entities-changed="','"></hui-entity-editor> </div> '])),this.hass,e,j,this._computeLabelCallback,this._valueChanged,this.hass,this._configEntities,this._changed)}},{kind:"method",key:"_valueChanged",value:function(e){(0,p.r)(this,"config-changed",{config:e.detail.value})}},{kind:"method",key:"_changed",value:function(e){this._config&&this.hass&&(e.detail&&e.detail.entities&&(this._config=Object.assign(Object.assign({},this._config),{},{entities:e.detail.entities}),this._configEntities=(0,_._)(this._config.entities)),(0,p.r)(this,"config-changed",{config:this._config}))}},{kind:"field",key:"_computeLabelCallback",value:function(){var e=this;return function(t){switch(t.name){case"theme":case"tap_action":case"hold_action":return"".concat(e.hass.localize("ui.panel.lovelace.editor.card.generic.".concat(t.name))," (").concat(e.hass.localize("ui.panel.lovelace.editor.card.config.optional"),")");case"entity":return e.hass.localize("ui.panel.lovelace.editor.card.picture-glance.state_entity");default:return e.hass.localize("ui.panel.lovelace.editor.card.generic.".concat(t.name))}}}},{kind:"field",static:!0,key:"styles",value:function(){return A.U}}]}}),y.WF),r(),e.next=45;break;case 42:e.prev=42,e.t2=e.catch(0),r(e.t2);case 45:case"end":return e.stop()}}),e,null,[[0,42]])})));return function(t,i){return e.apply(this,arguments)}}())},93161:function(e,t,i){i.d(t,{l:function(){return c}});var n=i(66419),a=i(45003),r=i(76914),c=(0,n.KC)([(0,n.Ik)({entity:(0,n.Yj)(),name:(0,n.lq)((0,n.Yj)()),icon:(0,n.lq)((0,n.Yj)()),image:(0,n.lq)((0,n.Yj)()),secondary_info:(0,n.lq)((0,n.Yj)()),format:(0,n.lq)((0,n.vP)(a.j)),state_color:(0,n.lq)((0,n.zM)()),tap_action:(0,n.lq)(r.k),hold_action:(0,n.lq)(r.k),double_tap_action:(0,n.lq)(r.k)}),(0,n.Yj)()])}}]);
//# sourceMappingURL=73707.OhTG8JViLU0.js.map