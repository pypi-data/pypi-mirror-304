export const id=39260;export const ids=[39260];export const modules={39260:(e,a,t)=>{t.r(a),t.d(a,{ZHAAddGroupPage:()=>l});var i=t(36312),s=t(68689),o=(t(16891),t(72606),t(15112)),d=t(77706),n=t(16312),r=(t(37629),t(15419));t(77980),t(71622),t(90431),t(23081);let l=(0,i.A)([(0,d.EM)("zha-add-group-page")],(function(e,a){class t extends a{constructor(...a){super(...a),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,d.MZ)({type:Array})],key:"deviceEndpoints",value:()=>[]},{kind:"field",decorators:[(0,d.wk)()],key:"_processingAdd",value:()=>!1},{kind:"field",decorators:[(0,d.wk)()],key:"_groupName",value:()=>""},{kind:"field",decorators:[(0,d.wk)()],key:"_groupId",value:void 0},{kind:"field",decorators:[(0,d.P)("zha-device-endpoint-data-table",!0)],key:"_zhaDevicesDataTable",value:void 0},{kind:"field",key:"_firstUpdatedCalled",value:()=>!1},{kind:"field",key:"_selectedDevicesToAdd",value:()=>[]},{kind:"method",key:"connectedCallback",value:function(){(0,s.A)(t,"connectedCallback",this,3)([]),this.hass&&this._firstUpdatedCalled&&this._fetchData()}},{kind:"method",key:"firstUpdated",value:function(e){(0,s.A)(t,"firstUpdated",this,3)([e]),this.hass&&this._fetchData(),this._firstUpdatedCalled=!0}},{kind:"method",key:"render",value:function(){return o.qy` <hass-subpage .hass="${this.hass}" .narrow="${this.narrow}" .header="${this.hass.localize("ui.panel.config.zha.groups.create_group")}"> <ha-config-section .isWide="${!this.narrow}"> <p slot="introduction"> ${this.hass.localize("ui.panel.config.zha.groups.create_group_details")} </p> <ha-textfield type="string" .value="${this._groupName}" @change="${this._handleNameChange}" .placeholder="${this.hass.localize("ui.panel.config.zha.groups.group_name_placeholder")}"></ha-textfield> <ha-textfield type="number" .value="${this._groupId}" @change="${this._handleGroupIdChange}" .placeholder="${this.hass.localize("ui.panel.config.zha.groups.group_id_placeholder")}"></ha-textfield> <div class="header"> ${this.hass.localize("ui.panel.config.zha.groups.add_members")} </div> <zha-device-endpoint-data-table .hass="${this.hass}" .deviceEndpoints="${this.deviceEndpoints}" .narrow="${this.narrow}" selectable @selection-changed="${this._handleAddSelectionChanged}"> </zha-device-endpoint-data-table> <div class="buttons"> <mwc-button .disabled="${!this._groupName||""===this._groupName||this._processingAdd}" @click="${this._createGroup}" class="button"> ${this._processingAdd?o.qy`<ha-circular-progress indeterminate size="small" .ariaLabel="${this.hass.localize("ui.panel.config.zha.groups.creating_group")}"></ha-circular-progress>`:""} ${this.hass.localize("ui.panel.config.zha.groups.create")}</mwc-button> </div> </ha-config-section> </hass-subpage> `}},{kind:"method",key:"_fetchData",value:async function(){this.deviceEndpoints=await(0,r.zt)(this.hass)}},{kind:"method",key:"_handleAddSelectionChanged",value:function(e){this._selectedDevicesToAdd=e.detail.value}},{kind:"method",key:"_createGroup",value:async function(){this._processingAdd=!0;const e=this._selectedDevicesToAdd.map((e=>{const a=e.split("_");return{ieee:a[0],endpoint_id:a[1]}})),a=this._groupId?parseInt(this._groupId,10):void 0,t=await(0,r.$)(this.hass,this._groupName,a,e);this._selectedDevicesToAdd=[],this._processingAdd=!1,this._groupName="",this._zhaDevicesDataTable.clearSelection(),(0,n.o)(`/config/zha/group/${t.group_id}`,{replace:!0})}},{kind:"method",key:"_handleGroupIdChange",value:function(e){this._groupId=e.target.value}},{kind:"method",key:"_handleNameChange",value:function(e){this._groupName=e.target.value||""}},{kind:"get",static:!0,key:"styles",value:function(){return[o.AH`.header{font-family:var(--paper-font-display1_-_font-family);-webkit-font-smoothing:var(--paper-font-display1_-_-webkit-font-smoothing);font-size:var(--paper-font-display1_-_font-size);font-weight:var(--paper-font-display1_-_font-weight);letter-spacing:var(--paper-font-display1_-_letter-spacing);line-height:var(--paper-font-display1_-_line-height);opacity:var(--dark-primary-opacity)}.button{float:right}ha-config-section :last-child{padding-bottom:24px}.buttons{align-items:flex-end;padding:8px}.buttons .warning{--mdc-theme-primary:var(--error-color)}`]}}]}}),o.WF)}};
//# sourceMappingURL=39260.YB8aKWoLDzQ.js.map