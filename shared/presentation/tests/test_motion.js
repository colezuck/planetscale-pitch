'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {port, route, interpolate, ease} = require('../diagram-motion.js');
const scene = JSON.parse(fs.readFileSync(path.join(__dirname,'../examples/capacity-model.json'),'utf8'));
// Resolve just the fields needed by the pure geometry functions from the authored example.
let nodes = Object.fromEntries(scene.nodes.map(n => [n.id, {...n, opacity:n.opacity ?? 1, stroke:n.stroke ?? '#a5a5a5', fill:n.fill ?? '#111111', color:n.color ?? '#fafafa'}]));
let links = Object.fromEntries(scene.links.map(l => [l.id, {stroke:'#a5a5a5',opacity:1,label:'',labelOffset:-18,...l}]));
const states = scene.stages.map(stage => {
  for(const [id,overrides] of Object.entries(stage.nodes ?? {})) nodes[id] = {...nodes[id],...overrides};
  for(const [id,overrides] of Object.entries(stage.links ?? {})) links[id] = {...links[id],...overrides};
  return JSON.parse(JSON.stringify({nodes,links}));
});
const middle = interpolate(states[0],states[1],0.5);
assert.equal(middle.nodes.cpu.w,163.5);
// Paths must be recomputed from moving box ports, including midway through the tween.
for (const state of [states[0],middle,states[1]]) {
  const connection = route(state.nodes,state.links.request);
  assert.equal(connection.a[0],state.nodes.compute.x + state.nodes.compute.w);
  assert.equal(connection.b[0],state.nodes.storage.x);
}
// An interrupted forward animation reverses from its current geometry, not a stale endpoint.
const reverse = interpolate(middle,states[0],0.5);
assert.equal(reverse.nodes.cpu.w,154.25);
assert.equal(states[0].nodes.cpu.w,145);
assert.equal(interpolate(middle,states[0],1).nodes.cpu.w,145);
// Both axes and perpendicular endpoints produce a valid elbow, and every port is defined.
assert.deepEqual(port({x:10,y:20,w:100,h:50},{side:'bottom',at:0.25}),[35,70]);
assert.equal(route({a:{x:0,y:0,w:10,h:10},b:{x:30,y:30,w:10,h:10}},{from:{node:'a',side:'right'},to:{node:'b',side:'top'}}).path,'M10 5H35V30');
assert.equal(ease(0),0);assert.equal(ease(1),1);
console.log('Motion geometry, moving connectors, and interrupted reverse navigation checked.');

const iconStart = {nodes:{disk:{iconScale:1,label:"SSD"}},links:{}};
const iconEnd = {nodes:{disk:{iconScale:1.8,label:"SSD"}},links:{}};
const iconMid = interpolate(iconStart,iconEnd,0.5);
assert.equal(iconMid.nodes.disk.iconScale,1.4);
assert.equal(interpolate(iconMid,iconStart,1).nodes.disk.iconScale,1);
