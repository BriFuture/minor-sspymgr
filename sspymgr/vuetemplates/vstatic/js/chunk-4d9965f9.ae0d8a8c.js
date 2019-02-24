(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-4d9965f9"],{"0751":function(t,n,a){"use strict";var e=function(){var t=this,n=t.$createElement,a=t._self._c||n;return a("div",[a("div",{staticClass:"row"},[a("b-form-group",{staticClass:"col-12 col-sm-6"},[a("label",[t._v("邮箱：")]),a("b-form-input",{attrs:{readonly:!0,value:t.user.email}})],1),a("b-form-group",{staticClass:"col-12 col-sm-6"},[a("label",[t._v("类型：")]),a("b-form-select",{on:{change:function(n){t.applyStatusChanged()}},model:{value:t.user.type,callback:function(n){t.$set(t.user,"type",n)},expression:"user.type"}},[a("option",{domProps:{value:null}},[t._v("空白")]),a("option",{attrs:{value:"notified"}},[t._v("邮件通知过")]),a("option",{attrs:{value:"active"}},[t._v("已激活")]),a("option",{attrs:{value:"banned"}},[t._v("已禁用")])])],1),a("b-form-group",{staticClass:"col-12 col-sm-6"},[a("label",[t._v("用户名：")]),a("b-form-input",{attrs:{readonly:!0,value:t.user.username}})],1),a("b-form-group",{staticClass:"col-12 col-sm-6"},[a("label",[t._v("备注：")]),a("b-form-input",{on:{input:function(n){t.applyStatusChanged()}},model:{value:t.user.comment,callback:function(n){t.$set(t.user,"comment",n)},expression:"user.comment"}})],1)],1),a("b-button",{staticClass:"float-right",attrs:{variant:t.applyStatus},on:{click:function(n){t.applyChanges()}}},[t._v("应用")])],1)},o=[],c=a("be6c"),s={name:"userItem",props:{user:{type:Object,default:{}}},data:function(){return{applyStatus:"secondary"}},methods:{applyStatusChanged:function(){this.applyStatus="primary"},applyChanges:function(){var t=this;Object(c["u"])({userId:this.user.id,comment:this.user.comment,type:this.user.type}).then(function(n){t.applyStatus="secondary"})}},created:function(){this.applyStatus="secondary"}},r=s,i=a("2877"),u=Object(i["a"])(r,e,o,!1,null,null,null);u.options.__file="UserItem.vue";n["a"]=u.exports},"5dbc":function(t,n,a){var e=a("d3f4"),o=a("8b97").set;t.exports=function(t,n,a){var c,s=n.constructor;return s!==a&&"function"==typeof s&&(c=s.prototype)!==a.prototype&&e(c)&&o&&o(t,c),t}},"883f":function(t,n,a){"use strict";var e=function(){var t=this,n=t.$createElement,a=t._self._c||n;return a("div",[a("b-card",[a("div",{staticClass:"row"},[a("div",{staticClass:"col-12 col-sm-9"},[a("account-basic-info",{attrs:{accountId:t.account.id,userEmail:t.account.email,port:t.account.port}}),a("div",{staticClass:"row py-2"},[a("div",{staticClass:"col-12 col-sm-4 text-left text-md"},[a("text-input",{attrs:{"input-prop":{title:"Host",icon:"fas fa-network-wired"}},model:{value:t.account.server,callback:function(n){t.$set(t.account,"server",n)},expression:"account.server"}})],1),a("div",{staticClass:"col-12 col-sm-4 text-left text-md"},[a("text-input",{attrs:{"input-prop":{title:"Password",icon:"fas fa-key"}},on:{valueChanged:function(n){t.isPasswordChanged=!0}},model:{value:t.account.password,callback:function(n){t.$set(t.account,"password",n)},expression:"account.password"}}),a("button",{staticClass:"btn btn-primary mx-2",attrs:{type:"button",disabled:!t.isPasswordChanged},on:{click:function(n){t.updatePassword()}}},[t._v(t._s("Update"))]),a("button",{staticClass:"btn btn-primary mx-2",attrs:{type:"button"},on:{click:function(n){t.randomPassword()}}},[t._v(t._s("Random"))])],1),a("div",{staticClass:"col-12 col-sm-4 text-left text-md"},[a("text-input",{attrs:{"input-prop":{title:"TotalFlow",icon:"fas fa-globe"},value:t.totalFlow},on:{valueChanged:function(n){t.onFlowChanged(n)}}}),a("button",{staticClass:"btn btn-primary mx-3",attrs:{disabled:!t.isFlowChanged},on:{click:function(n){t.updateFlow()}}},[t._v(t._s("Modify"))])],1)])],1),a("div",{staticClass:"col-12 col-sm-3 text-center"},[a("b-alert",{attrs:{variant:"primary",show:""}},[t._v("\r\n          使用 shadowsocks 手机客户端的“扫一扫”导入配置\r\n        ")]),a("qrcode-vue",{staticClass:"d-inline-block mx-auto",attrs:{value:t.ssAddress,size:200,level:"H"}})],1)])]),a("div",{staticClass:"row border-bottom py-2"},[a("div",{staticClass:"col-12 text-left text-lg"},[t._v(t._s("FlowUsage:")+"\r\n      "),a("b-progress",{staticClass:"mb-3",attrs:{max:t.totalFlow,"show-value":"",precision:1}},[a("b-progress-bar",{attrs:{value:t.$convertFlow(t.accFlow.flow,"GB"),variant:"primary"}}),a("b-progress-bar",{attrs:{value:t.totalFlow-t.$convertFlow(t.accFlow.flow,"GB"),variant:"success"}})],1)],1)]),a("div",{staticClass:"border-bottom my-2"},[a("div",{staticClass:"row pb-2",on:{click:function(n){t.showExpireModify()}}},[a("span",{staticClass:"col-4 text-left text-lg"},[t._v(t._s("Expire:"))]),a("span",{staticClass:"col-5 text-left text-md"},[t._v(t._s(t.$formatTime(t.account.expire)))]),a("button",{staticClass:"col-2 btn btn-primary py-0"},[t._v(t._s("Modify"))])]),a("div",{directives:[{name:"show",rawName:"v-show",value:t.isExpireModify,expression:"isExpireModify"}],staticClass:"border border-primary mt-3"},[a("div",{staticClass:"row my-2 mx-auto"},[a("button",{staticClass:"btn btn-secondary col mx-3",attrs:{value:"-1"},on:{click:function(n){t.modifyExpiration(-1)}}},[t._v(t._s("-1d"))]),a("button",{staticClass:"btn btn-secondary col mx-3",attrs:{value:"-7"},on:{click:function(n){t.modifyExpiration(-7)}}},[t._v(t._s("-7d"))]),a("button",{staticClass:"btn btn-secondary col mx-3",attrs:{value:"-15"},on:{click:function(n){t.modifyExpiration(-15)}}},[t._v(t._s("-15d"))]),a("button",{staticClass:"btn btn-secondary col mx-3",attrs:{value:"-30"},on:{click:function(n){t.modifyExpiration(-30)}}},[t._v(t._s("-30d"))]),a("button",{staticClass:"btn btn-success col mx-3",on:{click:function(n){t.acc_time_custom("-")}}},[t._v(t._s("Custom Sub"))])]),a("div",{staticClass:"row my-2 mx-auto"},[a("button",{staticClass:"btn btn-primary col mx-3",attrs:{value:"+1"},on:{click:function(n){t.modifyExpiration(1)}}},[t._v(t._s("+1d"))]),a("button",{staticClass:"btn btn-primary col mx-3",attrs:{value:"+7"},on:{click:function(n){t.modifyExpiration(7)}}},[t._v(t._s("+7d"))]),a("button",{staticClass:"btn btn-primary col mx-3",attrs:{value:"+15"},on:{click:function(n){t.modifyExpiration(15)}}},[t._v(t._s("+15d"))]),a("button",{staticClass:"btn btn-primary col mx-3",attrs:{value:"+30"},on:{click:function(n){t.modifyExpiration(30)}}},[t._v(t._s("+30d"))]),a("button",{staticClass:"btn btn-success col mx-3",on:{click:function(n){t.acc_time_custom("+")}}},[t._v(t._s("Custom Add"))])])])]),a("div",{staticClass:"row border-bottom my-2"},[a("span",{staticClass:"col-6 text-left text-lg"},[t._v(t._s("Status:")+" ")]),a("span",{staticClass:"col-6 text-left text-md"},[t._v(t._s(t.account.status))])]),a("div",{staticClass:"row border-bottom my-2"},[a("span",{staticClass:"col-6 text-left text-lg"},[t._v(t._s("Create Time:")+" ")]),a("span",{staticClass:"col-6 text-left text-md"},[t._v(t._s(t.$formatTime(t.account.createTime)))])]),t.account.userId?a("div",{staticClass:"row border-bottom my-2"},[a("span",{staticClass:"col-6 text-left text-lg"},[t._v(t._s("Last Connected:")+" ")]),a("span",{staticClass:"col-6 text-left text-md"},[t._v(t._s(t.$formatTime(t.accFlow.updateTime)))])]):t._e()],1)},o=[],c=a("be6c"),s=a("446e"),r=function(){var t=this,n=t.$createElement,a=t._self._c||n;return a("div",[a("div",{staticClass:"row border-bottom py-2"},[a("div",{staticClass:"col-12 col-sm-4 text-left text-md"},[a("text-input",{attrs:{"input-prop":{title:"Account",icon:"fas fa-user-circle"},readonly:!0},model:{value:t.accountId,callback:function(n){t.accountId=n},expression:"accountId"}})],1),a("div",{staticClass:"col-12 col-sm-4 text-left text-md"},[a("text-input",{attrs:{"input-prop":{title:"Belongs To:",icon:"far fa-user"},readonly:!0},model:{value:t.userEmail,callback:function(n){t.userEmail=n},expression:"userEmail"}})],1),a("div",{staticClass:"col-12 col-sm-4 text-left text-md"},[a("text-input",{attrs:{"input-prop":{title:"Port",icon:"fas fa-ethernet"},readonly:!0},model:{value:t.port,callback:function(n){t.port=n},expression:"port"}})],1)])])},i=[],u=(a("c5f6"),{name:"accountBasicInfo",components:{TextInput:s["a"]},props:{accountId:Number,userEmail:String,port:Number}}),l=u,d=a("2877"),p=Object(d["a"])(l,r,i,!1,null,null,null);p.options.__file="AccountBasicInfo.vue";var f=p.exports,m=a("d7b0"),b=1073741824,v={name:"accountDetail",components:{TextInput:s["a"],AccountBasicInfo:f,QrcodeVue:m["a"]},props:{account:{type:Object,default:{}},accFlow:{type:Object,default:{}},ssAddress:{type:String,default:""}},data:function(){return{isExpireModify:!1,isPasswordChanged:!1,isFlowChanged:!1}},computed:{totalFlow:function(){return this.account.totalFlow/b}},methods:{showExpireModify:function(){this.isExpireModify=!this.isExpireModify},modifyExpiration:function(t){var n=this;Object(c["p"])({port:this.account.port,days:t}).then(function(t){n.account.expire=t.nexpire})},onFlowChanged:function(t){this.isFlowChanged=!0,this.account.totalFlow=t*b},updateFlow:function(){var t=this;Object(c["q"])({port:this.account.port,flow:this.account.totalFlow,flowUnit:1}).then(function(n){t.isFlowChanged=!1})},updatePassword:function(t){var n=this;Object(c["r"])({password:this.account.password,port:this.account.port}).then(function(t){n.isPasswordChanged=!1})},randomPassword:function(){var t=this;Object(c["o"])({port:this.account.port}).then(function(n){"success"===n.status&&(t.account.password=n.password,t.isFlowChanged=!1)})}}},_=v,x=Object(d["a"])(_,e,o,!1,null,null,null);x.options.__file="AccountItem.vue";n["a"]=x.exports},"8b97":function(t,n,a){var e=a("d3f4"),o=a("cb7c"),c=function(t,n){if(o(t),!e(n)&&null!==n)throw TypeError(n+": can't set as prototype!")};t.exports={set:Object.setPrototypeOf||("__proto__"in{}?function(t,n,e){try{e=a("9b43")(Function.call,a("11e9").f(Object.prototype,"__proto__").set,2),e(t,[]),n=!(t instanceof Array)}catch(o){n=!0}return function(t,a){return c(t,a),n?t.__proto__=a:e(t,a),t}}({},!1):void 0),check:c}},9287:function(t,n,a){"use strict";a.r(n);var e=function(){var t=this,n=t.$createElement,a=t._self._c||n;return a("div",[a("div",{staticClass:"my-2"},[a("b-button",{attrs:{variant:"primary"},on:{click:function(n){t.$router.go(-1)}}},[t._v("\r\n      "+t._s("返回")+"\r\n    ")])],1),a("b-card",[a("user-item",{attrs:{user:t.user}})],1),a("div",[a("account-item",{attrs:{account:t.account,accFlow:t.accountFlow}})],1)],1)},o=[],c=a("be6c"),s=a("883f"),r=a("0751"),i={name:"userDetail",components:{AccountItem:s["a"],UserItem:r["a"]},data:function(){return{user:{},userType:null,account:{},accountFlow:{}}},created:function(){var t=this;Object(c["n"])({userId:this.$route.params.id}).then(function(n){"success"===n.status&&(t.user=n.user,t.userType=t.user.type,t.account=n.account,t.accountFlow=n.accountFlow)})}},u=i,l=a("2877"),d=Object(l["a"])(u,e,o,!1,null,null,null);d.options.__file="UserDetail.vue";n["default"]=d.exports},aa77:function(t,n,a){var e=a("5ca1"),o=a("be13"),c=a("79e5"),s=a("fdef"),r="["+s+"]",i="​",u=RegExp("^"+r+r+"*"),l=RegExp(r+r+"*$"),d=function(t,n,a){var o={},r=c(function(){return!!s[t]()||i[t]()!=i}),u=o[t]=r?n(p):s[t];a&&(o[a]=u),e(e.P+e.F*r,"String",o)},p=d.trim=function(t,n){return t=String(o(t)),1&n&&(t=t.replace(u,"")),2&n&&(t=t.replace(l,"")),t};t.exports=d},be6c:function(t,n,a){"use strict";a.d(n,"f",function(){return o}),a.d(n,"m",function(){return c}),a.d(n,"s",function(){return s}),a.d(n,"t",function(){return r}),a.d(n,"c",function(){return i}),a.d(n,"h",function(){return u}),a.d(n,"n",function(){return l}),a.d(n,"e",function(){return d}),a.d(n,"d",function(){return p}),a.d(n,"l",function(){return f}),a.d(n,"g",function(){return m}),a.d(n,"k",function(){return b}),a.d(n,"j",function(){return v}),a.d(n,"o",function(){return _}),a.d(n,"r",function(){return x}),a.d(n,"q",function(){return y}),a.d(n,"p",function(){return w}),a.d(n,"u",function(){return C}),a.d(n,"a",function(){return h}),a.d(n,"i",function(){return g}),a.d(n,"b",function(){return E});a("cadf"),a("551c"),a("097d");var e=a("4182"),o=function(t){return Object(e["a"])("/api/admin/product/getAll",t)},c=function(t){return Object(e["a"])("/api/admin/product/get",t)},s=function(t){return Object(e["a"])("/api/admin/product/update",t)},r=function(t){return Object(e["a"])("/api/admin/productQrcode/update",t)},i=function(t){return Object(e["a"])("/api/admin/productQrcode/delete",t)},u=function(t){return Object(e["a"])("/api/admin/user/getAll",t)},l=function(t){return Object(e["a"])("/api/admin/user/getDetail",t)},d=function(t){return Object(e["a"])("/api/admin/account/get",t)},p=function(t){return Object(e["a"])("/api/admin/account/getDetail",t)},f=function(t){return Object(e["a"])("/api/admin/orderHistory/get",t)},m=function(t){return Object(e["a"])("/api/admin/setting/getAll",t)},b=function(t){return Object(e["a"])("/api/admin/email/getPage",t)},v=function(t){return Object(e["a"])("/api/admin/flowUsage/getInDay",t)},_=function(t){return Object(e["a"])("/api/admin/account/randomPassword",t)},x=function(t){return Object(e["a"])("/api/admin/account/updatePassword",t)},y=function(t){return Object(e["a"])("/api/admin/account/updateTotalFlow",t)},w=function(t){return Object(e["a"])("/api/admin/account/updateExpiration",t)},C=function(t){return Object(e["a"])("/api/admin/user/updateInfo",t)},h=function(t){return Object(e["a"])("/api/admin/announcement/create",t)},g=function(t){return Object(e["a"])("/api/admin/announcement/getAll",t)},E=function(t){return Object(e["a"])("/api/admin/announcement/delete",t)}},c5f6:function(t,n,a){"use strict";var e=a("7726"),o=a("69a8"),c=a("2d95"),s=a("5dbc"),r=a("6a99"),i=a("79e5"),u=a("9093").f,l=a("11e9").f,d=a("86cc").f,p=a("aa77").trim,f="Number",m=e[f],b=m,v=m.prototype,_=c(a("2aeb")(v))==f,x="trim"in String.prototype,y=function(t){var n=r(t,!1);if("string"==typeof n&&n.length>2){n=x?n.trim():p(n,3);var a,e,o,c=n.charCodeAt(0);if(43===c||45===c){if(a=n.charCodeAt(2),88===a||120===a)return NaN}else if(48===c){switch(n.charCodeAt(1)){case 66:case 98:e=2,o=49;break;case 79:case 111:e=8,o=55;break;default:return+n}for(var s,i=n.slice(2),u=0,l=i.length;u<l;u++)if(s=i.charCodeAt(u),s<48||s>o)return NaN;return parseInt(i,e)}}return+n};if(!m(" 0o1")||!m("0b1")||m("+0x1")){m=function(t){var n=arguments.length<1?0:t,a=this;return a instanceof m&&(_?i(function(){v.valueOf.call(a)}):c(a)!=f)?s(new b(y(n)),a,m):y(n)};for(var w,C=a("9e1e")?u(b):"MAX_VALUE,MIN_VALUE,NaN,NEGATIVE_INFINITY,POSITIVE_INFINITY,EPSILON,isFinite,isInteger,isNaN,isSafeInteger,MAX_SAFE_INTEGER,MIN_SAFE_INTEGER,parseFloat,parseInt,isInteger".split(","),h=0;C.length>h;h++)o(b,w=C[h])&&!o(m,w)&&d(m,w,l(b,w));m.prototype=v,v.constructor=m,a("2aba")(e,f,m)}},fdef:function(t,n){t.exports="\t\n\v\f\r   ᠎             　\u2028\u2029\ufeff"}}]);
//# sourceMappingURL=chunk-4d9965f9.ae0d8a8c.js.map