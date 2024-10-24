"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[62983],{62983:function(e,i,s){s.r(i);var t,a,n,o,c,r,d,l=s(64599),h=s(33994),u=s(22858),v=s(35806),_=s(71008),f=s(62193),k=s(2816),m=s(27927),g=s(35890),p=(s(81027),s(54838),s(15112)),L=s(29818),b=s(34897),y=(s(37629),s(3276)),w=s(97247),A=s(55321);(0,m.A)([(0,L.EM)("dialog-zwave_js-remove-failed-node")],(function(e,i){var s,m,C=function(i){function s(){var i;(0,_.A)(this,s);for(var t=arguments.length,a=new Array(t),n=0;n<t;n++)a[n]=arguments[n];return i=(0,f.A)(this,s,[].concat(a)),e(i),i}return(0,k.A)(s,i),(0,v.A)(s)}(i);return{F:C,d:[{kind:"field",decorators:[(0,L.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,L.wk)()],key:"device_id",value:void 0},{kind:"field",decorators:[(0,L.wk)()],key:"_status",value:function(){return""}},{kind:"field",decorators:[(0,L.wk)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,L.wk)()],key:"_node",value:void 0},{kind:"field",key:"_subscribed",value:void 0},{kind:"method",key:"disconnectedCallback",value:function(){(0,g.A)(C,"disconnectedCallback",this,3)([]),this._unsubscribe()}},{kind:"method",key:"showDialog",value:(m=(0,u.A)((0,h.A)().mark((function e(i){return(0,h.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:this.device_id=i.device_id;case 1:case"end":return e.stop()}}),e,this)}))),function(e){return m.apply(this,arguments)})},{kind:"method",key:"closeDialog",value:function(){this._unsubscribe(),this.device_id=void 0,this._status="",(0,b.r)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"closeDialogFinished",value:function(){history.back(),this.closeDialog()}},{kind:"method",key:"render",value:function(){return this.device_id?(0,p.qy)(t||(t=(0,l.A)([' <ha-dialog open @closed="','" .heading="','"> '," "," "," "," </ha-dialog> "])),this.closeDialog,(0,y.l)(this.hass,this.hass.localize("ui.panel.config.zwave_js.remove_failed_node.title")),""===this._status?(0,p.qy)(a||(a=(0,l.A)([' <div class="flex-container"> <ha-svg-icon .path="','" class="introduction"></ha-svg-icon> <div class="status"> ',' </div> </div> <mwc-button slot="primaryAction" @click="','"> '," </mwc-button> "])),"M22 14H21C21 10.13 17.87 7 14 7H13V5.73C13.6 5.39 14 4.74 14 4C14 2.9 13.11 2 12 2S10 2.9 10 4C10 4.74 10.4 5.39 11 5.73V7H10C6.13 7 3 10.13 3 14H2C1.45 14 1 14.45 1 15V18C1 18.55 1.45 19 2 19H3V20C3 21.11 3.9 22 5 22H19C20.11 22 21 21.11 21 20V19H22C22.55 19 23 18.55 23 18V15C23 14.45 22.55 14 22 14M9.86 16.68L8.68 17.86L7.5 16.68L6.32 17.86L5.14 16.68L6.32 15.5L5.14 14.32L6.32 13.14L7.5 14.32L8.68 13.14L9.86 14.32L8.68 15.5L9.86 16.68M18.86 16.68L17.68 17.86L16.5 16.68L15.32 17.86L14.14 16.68L15.32 15.5L14.14 14.32L15.32 13.14L16.5 14.32L17.68 13.14L18.86 14.32L17.68 15.5L18.86 16.68Z",this.hass.localize("ui.panel.config.zwave_js.remove_failed_node.introduction"),this._startExclusion,this.hass.localize("ui.panel.config.zwave_js.remove_failed_node.remove_device")):"","started"===this._status?(0,p.qy)(n||(n=(0,l.A)([' <div class="flex-container"> <ha-circular-progress indeterminate></ha-circular-progress> <div class="status"> <p> <b> '," </b> </p> </div> </div> "])),this.hass.localize("ui.panel.config.zwave_js.remove_failed_node.in_progress")):"","failed"===this._status?(0,p.qy)(o||(o=(0,l.A)([' <div class="flex-container"> <ha-svg-icon .path="','" class="error"></ha-svg-icon> <div class="status"> <p> '," </p> ",' </div> </div> <mwc-button slot="primaryAction" @click="','"> '," </mwc-button> "])),"M12,2C17.53,2 22,6.47 22,12C22,17.53 17.53,22 12,22C6.47,22 2,17.53 2,12C2,6.47 6.47,2 12,2M15.59,7L12,10.59L8.41,7L7,8.41L10.59,12L7,15.59L8.41,17L12,13.41L15.59,17L17,15.59L13.41,12L17,8.41L15.59,7Z",this.hass.localize("ui.panel.config.zwave_js.remove_failed_node.removal_failed"),this._error?(0,p.qy)(c||(c=(0,l.A)([" <p><em> "," </em></p> "])),this._error.message):"",this.closeDialog,this.hass.localize("ui.common.close")):"","finished"===this._status?(0,p.qy)(r||(r=(0,l.A)([' <div class="flex-container"> <ha-svg-icon .path="','" class="success"></ha-svg-icon> <div class="status"> <p> ',' </p> </div> </div> <mwc-button slot="primaryAction" @click="','"> '," </mwc-button> "])),"M12 2C6.5 2 2 6.5 2 12S6.5 22 12 22 22 17.5 22 12 17.5 2 12 2M10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z",this.hass.localize("ui.panel.config.zwave_js.remove_failed_node.removal_finished",{id:this._node.node_id}),this.closeDialogFinished,this.hass.localize("ui.common.close")):""):p.s6}},{kind:"method",key:"_startExclusion",value:function(){var e=this;this.hass&&(this._status="started",this._subscribed=(0,w.tj)(this.hass,this.device_id,(function(i){return e._handleMessage(i)})).catch((function(i){e._status="failed",e._error=i})))}},{kind:"method",key:"_handleMessage",value:function(e){"exclusion started"===e.event&&(this._status="started"),"node removed"===e.event&&(this._status="finished",this._node=e.node,this._unsubscribe())}},{kind:"method",key:"_unsubscribe",value:(s=(0,u.A)((0,h.A)().mark((function e(){var i;return(0,h.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!this._subscribed){e.next=6;break}return e.next=3,this._subscribed;case 3:(i=e.sent)instanceof Function&&i(),this._subscribed=void 0;case 6:"finished"!==this._status&&(this._status="");case 7:case"end":return e.stop()}}),e,this)}))),function(){return s.apply(this,arguments)})},{kind:"get",static:!0,key:"styles",value:function(){return[A.nA,(0,p.AH)(d||(d=(0,l.A)([".success{color:var(--success-color)}.failed{color:var(--warning-color)}.flex-container{display:flex;align-items:center}ha-svg-icon{width:68px;height:48px}.flex-container ha-circular-progress,.flex-container ha-svg-icon{margin-right:20px;margin-inline-end:20px;margin-inline-start:initial}"])))]}}]}}),p.WF)}}]);
//# sourceMappingURL=62983.X4pQ96pxvhI.js.map