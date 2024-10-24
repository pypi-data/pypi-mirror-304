export const id=24387;export const ids=[24387];export const modules={24387:(i,t,s)=>{s.r(t);var e=s(36312),a=(s(16891),s(72606),s(15112)),o=s(77706),n=s(34897),c=(s(37629),s(3276)),l=s(96961),r=s(55321);(0,e.A)([(0,o.EM)("dialog-matter-ping-node")],(function(i,t){return{F:class extends t{constructor(...t){super(...t),i(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"device_id",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_status",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_pingResultEntries",value:void 0},{kind:"method",key:"showDialog",value:async function(i){this.device_id=i.device_id}},{kind:"method",key:"render",value:function(){return this.device_id?a.qy` <ha-dialog open @closed="${this.closeDialog}" .heading="${(0,c.l)(this.hass,this.hass.localize("ui.panel.config.matter.ping_node.title"))}"> ${"failed"===this._status?a.qy` <div class="flex-container"> <ha-svg-icon .path="${"M12,2C17.53,2 22,6.47 22,12C22,17.53 17.53,22 12,22C6.47,22 2,17.53 2,12C2,6.47 6.47,2 12,2M15.59,7L12,10.59L8.41,7L7,8.41L10.59,12L7,15.59L8.41,17L12,13.41L15.59,17L17,15.59L13.41,12L17,8.41L15.59,7Z"}" class="failed"></ha-svg-icon> <div class="status"> <p> ${this.hass.localize(this._pingResultEntries?"ui.panel.config.matter.ping_node.no_ip_found":"ui.panel.config.matter.ping_node.ping_failed")} </p> </div> </div> <mwc-button slot="primaryAction" @click="${this.closeDialog}"> ${this.hass.localize("ui.common.close")} </mwc-button> `:this._pingResultEntries?a.qy` <h2> ${this.hass.localize("ui.panel.config.matter.ping_node.ping_complete")} </h2> <mwc-list> ${this._pingResultEntries.map((([i,t])=>a.qy`<ha-list-item hasMeta noninteractive>${i} <ha-svg-icon slot="meta" .path="${t?"M12 2C6.5 2 2 6.5 2 12S6.5 22 12 22 22 17.5 22 12 17.5 2 12 2M10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z":"M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"}" class="${t?"success":"failed"}"></ha-svg-icon> </ha-list-item>`))} </mwc-list> <mwc-button slot="primaryAction" @click="${this.closeDialog}"> ${this.hass.localize("ui.common.close")} </mwc-button> `:"started"===this._status?a.qy` <div class="flex-container"> <ha-circular-progress indeterminate></ha-circular-progress> <div class="status"> <p> <b> ${this.hass.localize("ui.panel.config.matter.ping_node.in_progress")} </b> </p> </div> </div> <mwc-button slot="primaryAction" @click="${this.closeDialog}"> ${this.hass.localize("ui.common.close")} </mwc-button> `:a.qy` <p> ${this.hass.localize("ui.panel.config.matter.ping_node.introduction")} </p> <p> <em> ${this.hass.localize("ui.panel.config.matter.ping_node.battery_device_warning")} </em> </p> <mwc-button slot="primaryAction" @click="${this._startPing}"> ${this.hass.localize("ui.panel.config.matter.ping_node.start_ping")} </mwc-button> `} </ha-dialog> `:a.s6}},{kind:"method",key:"_startPing",value:async function(){if(this.hass){this._status="started";try{const i=await(0,l.OW)(this.hass,this.device_id),t=Object.entries(i);0===t.length&&(this._status="failed"),this._pingResultEntries=t}catch(i){this._status="failed"}}}},{kind:"method",key:"closeDialog",value:function(){this.device_id=void 0,this._status=void 0,this._pingResultEntries=void 0,(0,n.r)(this,"dialog-closed",{dialog:this.localName})}},{kind:"get",static:!0,key:"styles",value:function(){return[r.RF,r.nA,a.AH`.success{color:var(--success-color)}.failed{color:var(--error-color)}.flex-container{display:flex;align-items:center}.stages{margin-top:16px}.stage{padding:8px}mwc-list{--mdc-list-side-padding:0}.flex-container ha-circular-progress,.flex-container ha-svg-icon{margin-right:20px}.flex-container ha-svg-icon{width:68px;height:48px}`]}}]}}),a.WF)}};
//# sourceMappingURL=24387.RBIqgY3d9F4.js.map