"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[47076],{78691:function(e,t,n){var r=n(22858).A,o=n(33994).A;n.a(e,function(){var e=r(o().mark((function e(r,i){var a,u,c,s,f,l,_;return o().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(e.prev=0,n.d(t,{EO:function(){return _},ol:function(){return f},xo:function(){return l}}),a=n(35193),u=n(45269),!(c=r([a])).then){e.next=12;break}return e.next=8,c;case 8:e.t1=e.sent,e.t0=(0,e.t1)(),e.next=13;break;case 12:e.t0=c;case 13:a=e.t0[0],s=function(e,t,n,r){var o=n((0,a.L_)(e,t),r);return o instanceof Date?(0,a.uk)(o,t):o},f=function(e,t,n,r,o){return n.time_zone===u.Wj.server?s(e,r.time_zone,t,o):t(e,o)},l=function(e,t,n,r,o){return n.time_zone===u.Wj.server?s(e,r.time_zone,t,o):t(e,o)},_=function(e,t,n,r,o){return l(e,n,r,o,r.time_zone===u.Wj.server?(0,a.L_)(t,o.time_zone):t)},i(),e.next=24;break;case 21:e.prev=21,e.t2=e.catch(0),i(e.t2);case 24:case"end":return e.stop()}}),e,null,[[0,21]])})));return function(t,n){return e.apply(this,arguments)}}())},10469:function(e,t,n){n.d(t,{$:function(){return o}});var r=n(64782),o=(n(89655),function(e,t){var n,o={},i=(0,r.A)(e);try{for(i.s();!(n=i.n()).done;){var a=n.value,u=t(a);u in o?o[u].push(a):o[u]=[a]}}catch(c){i.e(c)}finally{i.f()}return o})},31265:function(e,t,n){n.d(t,{JW:function(){return p},TC:function(){return a},VN:function(){return u},Vx:function(){return c},XQ:function(){return _},eM:function(){return f},iH:function(){return s},k3:function(){return y},m4:function(){return o},qf:function(){return i},yv:function(){return l}});var r=n(41981),o=(n(81027),n(13025),n(44124),n(26098),n(39790),n(253),n(2075),n(94438),33524==n.j?["migration_error","setup_error","setup_retry"]:null),i=33524==n.j?["not_loaded","loaded","setup_error","setup_retry"]:null,a=function(e,t,n){var r={type:"config_entries/subscribe"};return n&&n.type&&(r.type_filter=n.type),e.connection.subscribeMessage((function(e){return t(e)}),r)},u=function(e,t){var n={};return t&&(t.type&&(n.type_filter=t.type),t.domain&&(n.domain=t.domain)),e.callWS(Object.assign({type:"config_entries/get"},n))},c=function(e,t){return e.callWS({type:"config_entries/get_single",entry_id:t})},s=function(e,t,n){return e.callWS(Object.assign({type:"config_entries/update",entry_id:t},n))},f=function(e,t){return e.callApi("DELETE","config/config_entries/entry/".concat(t))},l=function(e,t){return e.callApi("POST","config/config_entries/entry/".concat(t,"/reload"))},_=function(e,t){return e.callWS({type:"config_entries/disable",entry_id:t,disabled_by:"user"})},y=function(e,t){return e.callWS({type:"config_entries/disable",entry_id:t,disabled_by:null})},p=function(e,t){if(!t)return e;var n=e.find((function(e){return e.entry_id===t}));if(!n)return e;var o=e.filter((function(e){return e.entry_id!==t}));return[n].concat((0,r.A)(o))}},47076:function(e,t,n){var r=n(22858).A,o=n(33994).A;n.a(e,function(){var e=r(o().mark((function e(r,i){var a,u,c,s,f,l,_,y,p,g,d,m,v,h,b,w,A,k,x,T,W,D,j,S,E,O,C,P,z,L,M,B,N,V,H,X,$,q,I,J,K,Q,R,G,U,F,Y,Z,ee,te,ne,re,oe,ie,ae,ue,ce,se,fe,le,_e,ye,pe,ge,de,me,ve,he,be,we,Ae,ke,xe;return o().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(e.prev=0,n.d(t,{AN:function(){return fe},B2:function(){return ie},BV:function(){return oe},DR:function(){return ke},E$:function(){return se},GW:function(){return re},KJ:function(){return ve},Q4:function(){return ee},RB:function(){return Y},WN:function(){return ue},X4:function(){return be},_d:function(){return me},al:function(){return ge},bs:function(){return ae},c:function(){return ne},gv:function(){return we},m7:function(){return F},oU:function(){return te},tb:function(){return pe},uh:function(){return Z},yM:function(){return he}}),a=n(658),u=n(41981),c=n(64782),s=n(33994),f=n(22858),l=n(71499),_=n(81027),y=n(82386),p=n(95737),g=n(97741),d=n(89655),m=n(26098),v=n(99471),h=n(10507),b=n(39790),w=n(9241),A=n(66457),k=n(36604),x=n(99019),T=n(92765),W=n(253),D=n(54846),j=n(16891),S=n(66555),E=n(96858),O=n(74312),C=n(40102),P=n(76476),z=n(56235),L=n(7792),M=n(46091),B=n(34542),N=n(23566),V=n(31077),H=n(97405),X=n(88444),$=n(94100),q=n(78691),I=n(41924),J=n(10469),K=n(31265),Q=n(4826),!(R=r([q,I])).then){e.next=72;break}return e.next=68,R;case 68:e.t1=e.sent,e.t0=(0,e.t1)(),e.next=73;break;case 72:e.t0=R;case 73:G=e.t0,q=G[0],I=G[1],U=[],F=function(){return{stat_energy_from:"",stat_cost:null,entity_energy_price:null,number_energy_price:null}},Y=function(){return{stat_energy_to:"",stat_compensation:null,entity_energy_price:null,number_energy_price:null}},Z=function(){return{type:"grid",flow_from:[],flow_to:[],cost_adjustment_day:0}},ee=function(){return{type:"solar",stat_energy_from:"",config_entry_solar_forecast:null}},te=function(){return{type:"battery",stat_energy_from:"",stat_energy_to:""}},ne=function(){return{type:"gas",stat_energy_from:"",stat_cost:null,entity_energy_price:null,number_energy_price:null}},re=function(){return{type:"water",stat_energy_from:"",stat_cost:null,entity_energy_price:null,number_energy_price:null}},oe=function(e){return e.callWS({type:"energy/info"})},ie=33524==n.j?function(){var e=(0,f.A)((0,s.A)().mark((function e(t){return(0,s.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,t.loadBackendTranslation("issues","energy");case 2:return e.abrupt("return",t.callWS({type:"energy/validate"}));case 3:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}():null,ae=function(e){return e.callWS({type:"energy/get_prefs"})},ue=33524==n.j?function(){var e=(0,f.A)((0,s.A)().mark((function e(t,n){var r;return(0,s.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return r=t.callWS(Object.assign({type:"energy/save_prefs"},n)),_e(t),e.abrupt("return",r);case 3:case"end":return e.stop()}}),e)})));return function(t,n){return e.apply(this,arguments)}}():null,ce=function(){var e=(0,f.A)((0,s.A)().mark((function e(t,n,r,o,i){var a,u=arguments;return(0,s.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return a=u.length>5&&void 0!==u[5]?u[5]:"hour",e.abrupt("return",t.callWS({type:"energy/fossil_energy_consumption",start_time:n.toISOString(),end_time:null==i?void 0:i.toISOString(),energy_statistic_ids:r,co2_statistic_id:o,period:a}));case 2:case"end":return e.stop()}}),e)})));return function(t,n,r,o,i){return e.apply(this,arguments)}}(),se=function(e){return(0,J.$)(e.energy_sources,(function(e){return e.type}))},fe=function(e,t,n){var r,o=[],i=(0,c.A)(e.energy_sources);try{for(i.s();!(r=i.n()).done;){var a=r.value;if(!n||n.includes(a.type))if("solar"!==a.type)if("gas"!==a.type&&"water"!==a.type)if("battery"!==a.type){var s,f=(0,c.A)(a.flow_from);try{for(f.s();!(s=f.n()).done;){var l=s.value;o.push(l.stat_energy_from),l.stat_cost&&o.push(l.stat_cost);var _=t.cost_sensors[l.stat_energy_from];_&&o.push(_)}}catch(v){f.e(v)}finally{f.f()}var y,p=(0,c.A)(a.flow_to);try{for(p.s();!(y=p.n()).done;){var g=y.value;o.push(g.stat_energy_to),g.stat_compensation&&o.push(g.stat_compensation);var d=t.cost_sensors[g.stat_energy_to];d&&o.push(d)}}catch(v){p.e(v)}finally{p.f()}}else o.push(a.stat_energy_from),o.push(a.stat_energy_to);else{o.push(a.stat_energy_from),a.stat_cost&&o.push(a.stat_cost);var m=t.cost_sensors[a.stat_energy_from];m&&o.push(m)}else o.push(a.stat_energy_from)}}catch(v){i.e(v)}finally{i.f()}return n&&!n.includes("device")||o.push.apply(o,(0,u.A)(e.device_consumption.map((function(e){return e.stat_consumption})))),o},le=function(){var e=(0,f.A)((0,s.A)().mark((function e(t,n,r,o,i){var f,l,_,y,p,g,d,m,v,h,b,w,A,k,x,T,W,D,j,S,E,N,V,H,X,$,I,J,R,G,U,F,Y,Z,ee,te,ne,re,ie,ae,ue,se,le,_e,ye,pe,ge;return(0,s.A)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,Promise.all([(0,K.VN)(t,{domain:"co2signal"}),oe(t)]);case 2:if(f=e.sent,l=(0,a.A)(f,2),_=l[0],y=l[1],!(p=_.length?_[0]:void 0)){e.next=21;break}d=0,m=Object.values(t.entities);case 9:if(!(d<m.length)){e.next=21;break}if("co2signal"===(v=m[d]).platform){e.next=13;break}return e.abrupt("continue",18);case 13:if((h=t.states[v.entity_id])&&"%"===h.attributes.unit_of_measurement){e.next=16;break}return e.abrupt("continue",18);case 16:return g=h.entity_id,e.abrupt("break",21);case 18:d++,e.next=9;break;case 21:b=[],w=(0,c.A)(n.energy_sources);try{for(w.s();!(A=w.n()).done;)if("grid"===(k=A.value).type){x=(0,c.A)(k.flow_from);try{for(x.s();!(T=x.n()).done;)W=T.value,b.push(W.stat_energy_from)}catch(s){x.e(s)}finally{x.f()}}}catch(s){w.e(s)}finally{w.f()}return D=fe(n,y,["grid","solar","battery","gas","device"]),j=fe(n,y,["water"]),S=[].concat((0,u.A)(D),(0,u.A)(j)),E=(0,O.c)(o||new Date,r),N=E>35?"month":E>2?"day":"hour",V=t.config.unit_system.length||"",H={energy:"kWh",volume:"km"===V?"m³":"ft³"},X={volume:"km"===V?"L":"gal"},$=D.length?(0,Q.sz)(t,r,o,D,N,H,["change"]):{},I=j.length?(0,Q.sz)(t,r,o,j,N,X,["change"]):{},U={},F={},i&&(R=(0,q.xo)(r,C.e,t.locale,t.config)&&(0,q.xo)(o||new Date,P.c,t.locale,t.config)?(0,q.ol)(r,z.P,t.locale,t.config,-(0,q.EO)(o||new Date,r,L.W,t.locale,t.config)-1):(0,q.ol)(r,M.f,t.locale,t.config,-1*(E+1)),G=(0,B.A)(r,-1),D.length&&(U=(0,Q.sz)(t,R,G,D,N,H,["change"])),j.length&&(F=(0,Q.sz)(t,R,G,j,N,X,["change"]))),void 0!==g&&(Y=ce(t,r,b,g,o,E>35?"month":E>2?"day":"hour"),i&&(Z=ce(t,R,b,g,G,E>35?"month":E>2?"day":"hour"))),ee={},te=S.length?(0,Q.Wr)(t,S):[],e.next=42,Promise.all([$,I,U,F,te,Y,Z]);case 42:return ne=e.sent,re=(0,a.A)(ne,7),ie=re[0],ae=re[1],ue=re[2],se=re[3],le=re[4],_e=re[5],ye=re[6],pe=Object.assign(Object.assign({},ie),ae),i&&(J=Object.assign(Object.assign({},ue),se)),S.length&&le.forEach((function(e){ee[e.statistic_id]=e})),ge={start:r,end:o,startCompare:R,endCompare:G,info:y,prefs:n,stats:pe,statsMetadata:ee,statsCompare:J,co2SignalConfigEntry:p,co2SignalEntity:g,fossilEnergyConsumption:_e,fossilEnergyConsumptionCompare:ye},e.abrupt("return",ge);case 56:case"end":return e.stop()}}),e)})));return function(t,n,r,o,i){return e.apply(this,arguments)}}(),_e=function(e){U.forEach((function(t){var n=pe(e,{key:t});n.clearPrefs(),n._active&&n.refresh()}))},ye=function(e){if(e._refreshTimeout&&clearTimeout(e._refreshTimeout),e._active&&(!e.end||e.end>new Date)){var t=new Date;t.getMinutes()>=20&&t.setHours(t.getHours()+1),t.setMinutes(20,0,0),e._refreshTimeout=window.setTimeout((function(){return e.refresh()}),t.getTime()-Date.now())}},pe=function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},n="_energy";if(t.key){if(!t.key.startsWith("energy_"))throw new Error("Key need to start with energy_");n="_".concat(t.key)}if(e.connection[n])return e.connection[n];U.push(t.key);var r=(0,X.X)(e.connection,n,(0,f.A)((0,s.A)().mark((function t(){return(0,s.A)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(r.prefs){t.next=4;break}return t.next=3,ae(e);case 3:r.prefs=t.sent;case 4:return ye(r),t.abrupt("return",le(e,r.prefs,r.start,r.end,r.compare));case 6:case"end":return t.stop()}}),t)})))),o=r.subscribe;r.subscribe=function(e){var t=o(e);return r._active++,void 0===r._refreshTimeout&&ye(r),function(){r._active--,r._active<1&&(clearTimeout(r._refreshTimeout),r._refreshTimeout=void 0),t()}},r._active=0,r.prefs=t.prefs;var i=new Date,a=(0,I.LW)(i,e.locale,e.config).split(":")[0];r.start=(0,q.ol)("0"===a?(0,M.f)(i,-1):i,N.o,e.locale,e.config),r.end=(0,q.ol)("0"===a?(0,M.f)(i,-1):i,V.D,e.locale,e.config);var u=function(){r._updatePeriodTimeout=window.setTimeout((function(){r.start=(0,q.ol)(new Date,N.o,e.locale,e.config),r.end=(0,q.ol)(new Date,V.D,e.locale,e.config),u()}),(0,H.L)((0,q.ol)(i,V.D,e.locale,e.config),1).getTime()-Date.now())};return u(),r.clearPrefs=function(){r.prefs=void 0},r.setPeriod=function(t,n){var o;r.start=t,r.end=n,r.start.getTime()!==(0,q.ol)(new Date,N.o,e.locale,e.config).getTime()||(null===(o=r.end)||void 0===o?void 0:o.getTime())!==(0,q.ol)(new Date,V.D,e.locale,e.config).getTime()||r._updatePeriodTimeout?r._updatePeriodTimeout&&(clearTimeout(r._updatePeriodTimeout),r._updatePeriodTimeout=void 0):u()},r.setCompare=function(e){r.compare=e},r},ge=function(e){return e.callWS({type:"energy/solar_forecast"})},de=["volume","energy"],me=function(e){var t,n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},r=arguments.length>2?arguments[2]:void 0,o=(0,c.A)(e.energy_sources);try{for(o.s();!(t=o.n()).done;){var i=t.value;if("gas"===i.type&&(!r||r!==i.stat_energy_from)){var a=n[i.stat_energy_from];if(de.includes(null==a?void 0:a.unit_class))return a.unit_class}}}catch(u){o.e(u)}finally{o.f()}},ve=function(e,t){var n=me(t,arguments.length>2&&void 0!==arguments[2]?arguments[2]:{});if(void 0!==n)return"energy"===n?"kWh":"km"===e.config.unit_system.length?"m³":"ft³"},he=function(e){return"km"===e.config.unit_system.length?"L":"gal"},be="/docs/energy/faq/#troubleshooting-missing-entities",we=(0,$.A)((function(e){return{summedData:Ae(e),compareSummedData:e.statsCompare?Ae(e,!0):void 0}})),Ae=function(e,t){var n,r={},o=(0,c.A)(e.prefs.energy_sources);try{for(o.s();!(n=o.n()).done;){var i=n.value;if("solar"!==i.type)if("battery"!==i.type){if("grid"===i.type){var u,s=(0,c.A)(i.flow_from);try{for(s.s();!(u=s.n()).done;){var f=u.value;r.from_grid?r.from_grid.push(f.stat_energy_from):r.from_grid=[f.stat_energy_from]}}catch(g){s.e(g)}finally{s.f()}var l,_=(0,c.A)(i.flow_to);try{for(_.s();!(l=_.n()).done;){var y=l.value;r.to_grid?r.to_grid.push(y.stat_energy_to):r.to_grid=[y.stat_energy_to]}}catch(g){_.e(g)}finally{_.f()}}}else r.to_battery?(r.to_battery.push(i.stat_energy_to),r.from_battery.push(i.stat_energy_from)):(r.to_battery=[i.stat_energy_to],r.from_battery=[i.stat_energy_from]);else r.solar?r.solar.push(i.stat_energy_from):r.solar=[i.stat_energy_from]}}catch(g){o.e(g)}finally{o.f()}var p={};return Object.entries(r).forEach((function(n){var r=(0,a.A)(n,2),o=r[0],i=r[1],u={},c={};i.forEach((function(n){var r=t?e.statsCompare[n]:e.stats[n];if(r){r.forEach((function(e){if(null!==e.change&&void 0!==e.change){var t=e.change;u[e.start]=e.start in u?u[e.start]+t:t}})),c[n]={}}})),p[o]=u})),p},ke=(0,$.A)((function(e,t){return{consumption:xe(e),compareConsumption:t?xe(t):void 0}})),xe=function(e){var t={total:{}};return Object.keys(e).forEach((function(n){Object.keys(e[n]).forEach((function(n){if(void 0===t.total[n]){var r,o,i,a,u,c=((null===(r=e.from_grid)||void 0===r?void 0:r[n])||0)+((null===(o=e.solar)||void 0===o?void 0:o[n])||0)+((null===(i=e.from_battery)||void 0===i?void 0:i[n])||0)-((null===(a=e.to_grid)||void 0===a?void 0:a[n])||0)-((null===(u=e.to_battery)||void 0===u?void 0:u[n])||0);t.total[n]=c}}))})),t},i(),e.next=111;break;case 108:e.prev=108,e.t2=e.catch(0),i(e.t2);case 111:case"end":return e.stop()}}),e,null,[[0,108]])})));return function(t,n){return e.apply(this,arguments)}}())}}]);
//# sourceMappingURL=47076.Rmg5sjBAmyQ.js.map