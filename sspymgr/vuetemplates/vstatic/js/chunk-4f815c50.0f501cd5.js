(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-4f815c50"],{"017a":function(t,n,e){"use strict";var a=e("04a3"),u=e.n(a);u.a},"04a3":function(t,n,e){},"26fa":function(t,n,e){"use strict";e.r(n);var a=function(){var t=this,n=t.$createElement,e=t._self._c||n;return e("div",{staticClass:"table-responsive"},[e("table",{staticClass:"table table-striped"},[t._m(0),e("tbody",t._l(t.settings,function(n){return e("tr",{key:n.id},[e("td",[t._v(t._s(n.id))]),e("td",[t._v(t._s(n.key))]),"Image"===n.type?[e("td",[n.value?e("span",{staticClass:"btn p-0"},[e("img",{attrs:{src:"data:image/png;base64, "+n.value,width:"32",height:"32"}})]):t._e()]),e("td",[e("button",{staticClass:"btn btn-sm btn-primary",attrs:{type:"button"}},[t._v(t._s("update"))])])]:"Boolean"===n.type?[e("td",[e("a-switch",{attrs:{checked:"1"===n.value},on:{change:function(e){t.switchSetting(n)}}})],1),t._m(1,!0)]:"Number"==n.type?[e("td",[e("input",{attrs:{type:"number"},domProps:{value:n.value}})]),t._m(2,!0)]:[e("td",[t._v(t._s(n.value))]),e("td",[e("button",{staticClass:"btn btn-sm btn-primary",attrs:{type:"button"}},[t._v(t._s("update"))])])]],2)}),0)])])},u=[function(){var t=this,n=t.$createElement,e=t._self._c||n;return e("thead",[e("tr",[e("th",{attrs:{scope:"col"}},[t._v("#")]),e("th",{attrs:{scope:"col"}},[t._v("Key")]),e("th",{attrs:{scope:"col"}},[t._v("Value")]),e("th",{attrs:{scope:"col"}},[t._v("Action")])])])},function(){var t=this,n=t.$createElement,e=t._self._c||n;return e("td",[e("label")])},function(){var t=this,n=t.$createElement,e=t._self._c||n;return e("td",[e("label")])}],r=(e("cadf"),e("551c"),e("097d"),e("be6c")),i={name:"adminWebSetting",data:function(){return{settings:[]}},methods:{switchSetting:function(t){"1"===t.value?t.value="0":t.value="1"}},created:function(){var t=this;Object(r["g"])().then(function(n){t.settings=n.setting})}},c=i,o=(e("017a"),e("2877")),d=Object(o["a"])(c,a,u,!1,null,null,null);d.options.__file="Websetting.vue";n["default"]=d.exports},be6c:function(t,n,e){"use strict";e.d(n,"f",function(){return u}),e.d(n,"m",function(){return r}),e.d(n,"s",function(){return i}),e.d(n,"t",function(){return c}),e.d(n,"c",function(){return o}),e.d(n,"h",function(){return d}),e.d(n,"n",function(){return s}),e.d(n,"e",function(){return f}),e.d(n,"d",function(){return l}),e.d(n,"l",function(){return p}),e.d(n,"g",function(){return b}),e.d(n,"k",function(){return m}),e.d(n,"j",function(){return g}),e.d(n,"o",function(){return v}),e.d(n,"r",function(){return _}),e.d(n,"q",function(){return j}),e.d(n,"p",function(){return h}),e.d(n,"u",function(){return O}),e.d(n,"a",function(){return w}),e.d(n,"i",function(){return y}),e.d(n,"b",function(){return k});e("cadf"),e("551c"),e("097d");var a=e("4182"),u=function(t){return Object(a["a"])("/api/admin/product/getAll",t)},r=function(t){return Object(a["a"])("/api/admin/product/get",t)},i=function(t){return Object(a["a"])("/api/admin/product/update",t)},c=function(t){return Object(a["a"])("/api/admin/productQrcode/update",t)},o=function(t){return Object(a["a"])("/api/admin/productQrcode/delete",t)},d=function(t){return Object(a["a"])("/api/admin/user/getAll",t)},s=function(t){return Object(a["a"])("/api/admin/user/getDetail",t)},f=function(t){return Object(a["a"])("/api/admin/account/get",t)},l=function(t){return Object(a["a"])("/api/admin/account/getDetail",t)},p=function(t){return Object(a["a"])("/api/admin/orderHistory/get",t)},b=function(t){return Object(a["a"])("/api/admin/setting/getAll",t)},m=function(t){return Object(a["a"])("/api/admin/email/getPage",t)},g=function(t){return Object(a["a"])("/api/admin/flowUsage/getInDay",t)},v=function(t){return Object(a["a"])("/api/admin/account/randomPassword",t)},_=function(t){return Object(a["a"])("/api/admin/account/updatePassword",t)},j=function(t){return Object(a["a"])("/api/admin/account/updateTotalFlow",t)},h=function(t){return Object(a["a"])("/api/admin/account/updateExpiration",t)},O=function(t){return Object(a["a"])("/api/admin/user/updateInfo",t)},w=function(t){return Object(a["a"])("/api/admin/announcement/create",t)},y=function(t){return Object(a["a"])("/api/admin/announcement/getAll",t)},k=function(t){return Object(a["a"])("/api/admin/announcement/delete",t)}}}]);
//# sourceMappingURL=chunk-4f815c50.0f501cd5.js.map