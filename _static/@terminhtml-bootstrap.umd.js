(function(n){typeof define=="function"&&define.amd?define(n):n()})(function(){"use strict";var g=Object.defineProperty;var u=Object.getOwnPropertySymbols;var C=Object.prototype.hasOwnProperty,E=Object.prototype.propertyIsEnumerable;var T=(n,e,t)=>e in n?g(n,e,{enumerable:!0,configurable:!0,writable:!0,value:t}):n[e]=t,a=(n,e)=>{for(var t in e||(e={}))C.call(e,t)&&T(n,t,e[t]);if(u)for(var t of u(e))E.call(e,t)&&T(n,t,e[t]);return n};const e=`https://unpkg.com/terminhtml@${1}.x/dist/`,t=`${e}terminhtml.es.js`,f=`${e}src/termynal.css`,L={class:"terminhtml"};function p(o){window.addEventListener("load",()=>{M(o).catch(console.error)})}async function M(o){H();const r=a(a({},L),o).class;return await h(r)}async function h(o){const s=await import(t),r=document.querySelectorAll(`.${o}`),c=[];for(const i of r){const w=new s.TerminHTML(i);c.push(w)}let d=[...c];function l(){d=d.filter(i=>i.container.getBoundingClientRect().top-innerHeight<=0?(i.init(),!1):!0)}window.addEventListener("scroll",l);const y=()=>window.removeEventListener("scroll",l);return setTimeout(l,50),{stopListener:y,terminHTMLs:c}}const m="terminhtml-styles";function H(){if(!document.getElementById(m)){const o=document.getElementsByTagName("head")[0],s=document.createElement("link");s.id=m,s.rel="stylesheet",s.type="text/css",s.href=f,s.media="all",o.appendChild(s)}}p()});
//# sourceMappingURL=@terminhtml-bootstrap.umd.js.map
