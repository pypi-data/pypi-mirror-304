"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[73613],{77275:function(e,t,n){var a=n(22858).A,r=n(33994).A;n.a(e,function(){var e=a(r().mark((function e(a,i){var s,o,l,c,d;return r().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(e.prev=0,n.d(t,{A:function(){return d}}),s=n(83052),o=n(72698),!(l=a([s,o])).then){e.next=12;break}return e.next=8,l;case 8:e.t1=e.sent,e.t0=(0,e.t1)(),e.next=13;break;case 12:e.t0=l;case 13:c=e.t0,s=c[0],o=c[1],d=(0,s.i1)({name:"@fullcalendar/daygrid",initialView:"dayGridMonth",views:{dayGrid:{component:o.eu,dateProfileGeneratorClass:o.LH},dayGridDay:{type:"dayGrid",duration:{days:1}},dayGridWeek:{type:"dayGrid",duration:{weeks:1}},dayGridMonth:{type:"dayGrid",duration:{months:1},fixedWeekCount:!0},dayGridYear:{type:"dayGrid",duration:{years:1}}}}),i(),e.next=23;break;case 20:e.prev=20,e.t2=e.catch(0),i(e.t2);case 23:case"end":return e.stop()}}),e,null,[[0,20]])})));return function(t,n){return e.apply(this,arguments)}}())},66563:function(e,t,n){var a=n(22858).A,r=n(33994).A;n.a(e,function(){var e=a(r().mark((function e(a,i){var s,o,l,c,d,u,f,v;return r().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(e.prev=0,f=function(e){return!1===e?null:(0,l.x)(e)},n.d(t,{A:function(){return v}}),s=n(83052),o=n(71490),l=n(93637),!(c=a([l,s,o])).then){e.next=14;break}return e.next=10,c;case 10:e.t1=e.sent,e.t0=(0,e.t1)(),e.next=15;break;case 14:e.t0=c;case 15:d=e.t0,l=d[0],s=d[1],o=d[2],u={listDayFormat:f,listDaySideFormat:f,noEventsClassNames:l.n,noEventsContent:l.n,noEventsDidMount:l.n,noEventsWillUnmount:l.n},v=(0,s.i1)({name:"@fullcalendar/list",optionRefiners:u,views:{list:{component:o.u,buttonTextKey:"list",listDayFormat:{month:"long",day:"numeric",year:"numeric"}},listDay:{type:"list",duration:{days:1},listDayFormat:{weekday:"long"}},listWeek:{type:"list",duration:{weeks:1},listDayFormat:{weekday:"long"},listDaySideFormat:{month:"long",day:"numeric",year:"numeric"}},listMonth:{type:"list",duration:{month:1},listDaySideFormat:{weekday:"long"}},listYear:{type:"list",duration:{year:1},listDaySideFormat:{weekday:"long"}}}}),i(),e.next=27;break;case 24:e.prev=24,e.t2=e.catch(0),i(e.t2);case 27:case"end":return e.stop()}}),e,null,[[0,24]])})));return function(t,n){return e.apply(this,arguments)}}())},71490:function(e,t,n){var a=n(22858).A,r=n(33994).A;n.a(e,function(){var e=a(r().mark((function e(a,i){var s,o,l,c,d,u,f,v,h,y,p,g,m,b,x,k,w,D,A,C;return r().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(e.prev=0,C=function(e){var t,n,a=[];for(t=0;t<e.length;t+=1)(a[(n=e[t]).dayIndex]||(a[n.dayIndex]=[])).push(n);return a},A=function(e){for(var t=(0,f.q)(e.renderRange.start),n=e.renderRange.end,a=[],r=[];t<n;)a.push(t),r.push({start:t,end:(0,f.t)(t,1)}),t=(0,f.t)(t,1);return{dayDates:a,dayRanges:r}},D=function(e){return e.text},k=function(e){return e.text},x=function(e,t,n,a,r){var i=n.options;if(!1!==i.displayEventTime){var s,o=e.eventRange.def,l=e.eventRange.instance,c=!1;if(o.allDay?c=!0:(0,f.az)(e.eventRange.range)?e.isStart?s=(0,f.bQ)(e,t,n,null,null,l.range.start,e.end):e.isEnd?s=(0,f.bQ)(e,t,n,null,null,e.start,l.range.end):c=!0:s=(0,f.bQ)(e,t,n),c){var d={text:n.options.allDayText,view:n.viewApi};return(0,v.n)(f.C,{elTag:"td",elClasses:["fc-list-event-time"],elAttrs:{headers:"".concat(a," ").concat(r)},renderProps:d,generatorName:"allDayContent",customGenerator:i.allDayContent,defaultGenerator:k,classNameGenerator:i.allDayClassNames,didMount:i.allDayDidMount,willUnmount:i.allDayWillUnmount})}return(0,v.n)("td",{className:"fc-list-event-time"},s)}return null},b=function(e,t){var n=(0,f.bU)(e,t);return(0,v.n)("a",Object.assign({},n),e.eventRange.def.title)},p=function(e){return(0,v.n)(v.FK,null,e.text&&(0,v.n)("a",Object.assign({id:e.textId,className:"fc-list-day-text"},e.navLinkAttrs),e.text),e.sideText&&(0,v.n)("a",Object.assign({"aria-hidden":!0,className:"fc-list-day-side-text"},e.sideNavLinkAttrs),e.sideText))},n.d(t,{u:function(){return w}}),s=n(64782),o=n(41981),l=n(71008),c=n(35806),d=n(62193),u=n(2816),n(81027),n(89655),n(26098),f=n(93637),v=n(45166),!(h=a([f])).then){e.next=28;break}return e.next=24,h;case 24:e.t1=e.sent,e.t0=(0,e.t1)(),e.next=29;break;case 28:e.t0=h;case 29:f=e.t0[0],y=function(e){function t(){var e;return(0,l.A)(this,t),(e=(0,d.A)(this,t,arguments)).state={textId:(0,f.a5)()},e}return(0,u.A)(t,e),(0,c.A)(t,[{key:"render",value:function(){var e=this.context,t=e.theme,n=e.dateEnv,a=e.options,r=e.viewApi,i=this.props,s=i.cellId,l=i.dayDate,c=i.todayRange,d=this.state.textId,u=(0,f.a_)(l,c),h=a.listDayFormat?n.format(l,a.listDayFormat):"",y=a.listDaySideFormat?n.format(l,a.listDaySideFormat):"",g=Object.assign({date:n.toDate(l),view:r,textId:d,text:h,sideText:y,navLinkAttrs:(0,f.b0)(this.context,l),sideNavLinkAttrs:(0,f.b0)(this.context,l,"day",!1)},u);return(0,v.n)(f.C,{elTag:"tr",elClasses:["fc-list-day"].concat((0,o.A)((0,f.aZ)(u,t))),elAttrs:{"data-date":(0,f.bv)(l)},renderProps:g,generatorName:"dayHeaderContent",customGenerator:a.dayHeaderContent,defaultGenerator:p,classNameGenerator:a.dayHeaderClassNames,didMount:a.dayHeaderDidMount,willUnmount:a.dayHeaderWillUnmount},(function(e){return(0,v.n)("th",{scope:"colgroup",colSpan:3,id:s,"aria-labelledby":d},(0,v.n)(e,{elTag:"div",elClasses:["fc-list-day-cushion",t.getClass("tableCellShaded")]}))}))}}])}(f.B),g=(0,f.x)({hour:"numeric",minute:"2-digit",meridiem:"short"}),m=function(e){function t(){return(0,l.A)(this,t),(0,d.A)(this,t,arguments)}return(0,u.A)(t,e),(0,c.A)(t,[{key:"render",value:function(){var e=this.props,t=this.context,n=t.options,a=e.seg,r=e.timeHeaderId,i=e.eventHeaderId,s=e.dateHeaderId,o=n.eventTimeFormat||g;return(0,v.n)(f.cn,Object.assign({},e,{elTag:"tr",elClasses:["fc-list-event",a.eventRange.def.url&&"fc-event-forced-url"],defaultGenerator:function(){return b(a,t)},seg:a,timeText:"",disableDragging:!0,disableResizing:!0}),(function(e,n){return(0,v.n)(v.FK,null,x(a,o,t,r,s),(0,v.n)("td",{"aria-hidden":!0,className:"fc-list-event-graphic"},(0,v.n)("span",{className:"fc-list-event-dot",style:{borderColor:n.borderColor||n.backgroundColor}})),(0,v.n)(e,{elTag:"td",elClasses:["fc-list-event-title"],elAttrs:{headers:"".concat(i," ").concat(s)}}))}))}}])}(f.B),w=function(e){function t(){var e;return(0,l.A)(this,t),(e=(0,d.A)(this,t,arguments)).computeDateVars=(0,f.z)(A),e.eventStoreToSegs=(0,f.z)(e._eventStoreToSegs),e.state={timeHeaderId:(0,f.a5)(),eventHeaderId:(0,f.a5)(),dateHeaderIdRoot:(0,f.a5)()},e.setRootEl=function(t){t?e.context.registerInteractiveComponent(e,{el:t}):e.context.unregisterInteractiveComponent(e)},e}return(0,u.A)(t,e),(0,c.A)(t,[{key:"render",value:function(){var e=this.props,t=this.context,n=this.computeDateVars(e.dateProfile),a=n.dayDates,r=n.dayRanges,i=this.eventStoreToSegs(e.eventStore,e.eventUiBases,r);return(0,v.n)(f.ct,{elRef:this.setRootEl,elClasses:["fc-list",t.theme.getClass("table"),!1!==t.options.stickyHeaderDates?"fc-list-sticky":""],viewSpec:t.viewSpec},(0,v.n)(f.cd,{liquid:!e.isHeightAuto,overflowX:e.isHeightAuto?"visible":"hidden",overflowY:e.isHeightAuto?"visible":"auto"},i.length>0?this.renderSegList(i,a):this.renderEmptyMessage()))}},{key:"renderEmptyMessage",value:function(){var e=this.context,t=e.options,n=e.viewApi,a={text:t.noEventsText,view:n};return(0,v.n)(f.C,{elTag:"div",elClasses:["fc-list-empty"],renderProps:a,generatorName:"noEventsContent",customGenerator:t.noEventsContent,defaultGenerator:D,classNameGenerator:t.noEventsClassNames,didMount:t.noEventsDidMount,willUnmount:t.noEventsWillUnmount},(function(e){return(0,v.n)(e,{elTag:"div",elClasses:["fc-list-empty-cushion"]})}))}},{key:"renderSegList",value:function(e,t){var n=this.context,a=n.theme,r=n.options,i=this.state,o=i.timeHeaderId,l=i.eventHeaderId,c=i.dateHeaderIdRoot,d=C(e);return(0,v.n)(f.ch,{unit:"day"},(function(e,n){for(var i=[],u=0;u<d.length;u+=1){var h=d[u];if(h){var p=(0,f.bv)(t[u]),g=c+"-"+p;i.push((0,v.n)(y,{key:p,cellId:g,dayDate:t[u],todayRange:n})),h=(0,f.bR)(h,r.eventOrder);var b,x=(0,s.A)(h);try{for(x.s();!(b=x.n()).done;){var k=b.value;i.push((0,v.n)(m,Object.assign({key:p+":"+k.eventRange.instance.instanceId,seg:k,isDragging:!1,isResizing:!1,isDateSelecting:!1,isSelected:!1,timeHeaderId:o,eventHeaderId:l,dateHeaderId:g},(0,f.bS)(k,n,e))))}}catch(w){x.e(w)}finally{x.f()}}}return(0,v.n)("table",{className:"fc-list-table "+a.getClass("table")},(0,v.n)("thead",null,(0,v.n)("tr",null,(0,v.n)("th",{scope:"col",id:o},r.timeHint),(0,v.n)("th",{scope:"col","aria-hidden":!0}),(0,v.n)("th",{scope:"col",id:l},r.eventHint))),(0,v.n)("tbody",null,i))}))}},{key:"_eventStoreToSegs",value:function(e,t,n){return this.eventRangesToSegs((0,f.af)(e,t,this.props.dateProfile.activeRange,this.context.options.nextDayThreshold).fg,n)}},{key:"eventRangesToSegs",value:function(e,t){var n,a=[],r=(0,s.A)(e);try{for(r.s();!(n=r.n()).done;){var i=n.value;a.push.apply(a,(0,o.A)(this.eventRangeToSegs(i,t)))}}catch(l){r.e(l)}finally{r.f()}return a}},{key:"eventRangeToSegs",value:function(e,t){var n,a,r,i=this.context.dateEnv,s=this.context.options.nextDayThreshold,o=e.range,l=e.def.allDay,c=[];for(n=0;n<t.length;n+=1)if((a=(0,f.o)(o,t[n]))&&(r={component:this,eventRange:e,start:a.start,end:a.end,isStart:e.isStart&&a.start.valueOf()===o.start.valueOf(),isEnd:e.isEnd&&a.end.valueOf()===o.end.valueOf(),dayIndex:n},c.push(r),!r.isEnd&&!l&&n+1<t.length&&o.end<i.add(t[n+1].start,s))){r.end=o.end,r.isEnd=!0;break}return c}}])}(f.be),(0,f.cw)(':root{--fc-list-event-dot-width:10px;--fc-list-event-hover-bg-color:#f5f5f5}.fc-theme-standard .fc-list{border:1px solid var(--fc-border-color)}.fc .fc-list-empty{align-items:center;background-color:var(--fc-neutral-bg-color);display:flex;height:100%;justify-content:center}.fc .fc-list-empty-cushion{margin:5em 0}.fc .fc-list-table{border-style:hidden;width:100%}.fc .fc-list-table tr>*{border-left:0;border-right:0}.fc .fc-list-sticky .fc-list-day>*{background:var(--fc-page-bg-color);position:sticky;top:0}.fc .fc-list-table thead{left:-10000px;position:absolute}.fc .fc-list-table tbody>tr:first-child th{border-top:0}.fc .fc-list-table th{padding:0}.fc .fc-list-day-cushion,.fc .fc-list-table td{padding:8px 14px}.fc .fc-list-day-cushion:after{clear:both;content:"";display:table}.fc-theme-standard .fc-list-day-cushion{background-color:var(--fc-neutral-bg-color)}.fc-direction-ltr .fc-list-day-text,.fc-direction-rtl .fc-list-day-side-text{float:left}.fc-direction-ltr .fc-list-day-side-text,.fc-direction-rtl .fc-list-day-text{float:right}.fc-direction-ltr .fc-list-table .fc-list-event-graphic{padding-right:0}.fc-direction-rtl .fc-list-table .fc-list-event-graphic{padding-left:0}.fc .fc-list-event.fc-event-forced-url{cursor:pointer}.fc .fc-list-event:hover td{background-color:var(--fc-list-event-hover-bg-color)}.fc .fc-list-event-graphic,.fc .fc-list-event-time{white-space:nowrap;width:1px}.fc .fc-list-event-dot{border:calc(var(--fc-list-event-dot-width)/2) solid var(--fc-event-border-color);border-radius:calc(var(--fc-list-event-dot-width)/2);box-sizing:content-box;display:inline-block;height:0;width:0}.fc .fc-list-event-title a{color:inherit;text-decoration:none}.fc .fc-list-event.fc-event-forced-url:hover a{text-decoration:underline}'),i(),e.next=42;break;case 39:e.prev=39,e.t2=e.catch(0),i(e.t2);case 42:case"end":return e.stop()}}),e,null,[[0,39]])})));return function(t,n){return e.apply(this,arguments)}}())}}]);
//# sourceMappingURL=73613.FzN3UCeYjQs.js.map