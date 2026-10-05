/* Stable SVG geometry animated from declarative states. Compatible with local Reveal 5.2.0. */
(function (root) {
  'use strict';
  const copy = value => JSON.parse(JSON.stringify(value));
  const mix = (a, b, t) => a + (b - a) * t;
  const ease = t => 1 - Math.pow(1 - t, 3);
  const color = (a, b, t) => '#' + [1, 3, 5].map(i => Math.round(mix(parseInt(a.slice(i, i + 2), 16), parseInt(b.slice(i, i + 2), 16), t)).toString(16).padStart(2, '0')).join('');
  function port(node, endpoint) {
    const at = endpoint.at === undefined ? 0.5 : endpoint.at;
    switch (endpoint.side) {
      case 'left': return [node.x, node.y + node.h * at];
      case 'right': return [node.x + node.w, node.y + node.h * at];
      case 'top': return [node.x + node.w * at, node.y];
      case 'bottom': return [node.x + node.w * at, node.y + node.h];
      default: throw new Error('Unknown connection port');
    }
  }
  function route(nodes, link) {
    const a = port(nodes[link.from.node], link.from), b = port(nodes[link.to.node], link.to);
    // An orthogonal route is readable during a resize, without path morph topology changes.
    const horizontal = ['left', 'right'].includes(link.from.side);
    const endHorizontal = ['left', 'right'].includes(link.to.side);
    if (horizontal !== endHorizontal) return {a, b, path: horizontal ? `M${a[0]} ${a[1]}H${b[0]}V${b[1]}` : `M${a[0]} ${a[1]}V${b[1]}H${b[0]}`};
    const middle = horizontal ? (a[0] + b[0]) / 2 : (a[1] + b[1]) / 2;
    return {a, b, path: horizontal ? `M${a[0]} ${a[1]}H${middle}V${b[1]}H${b[0]}` : `M${a[0]} ${a[1]}V${middle}H${b[0]}V${b[1]}`};
  }
  function interpolate(start, target, t) {
    const result = copy(target);
    for (const type of ['nodes', 'links']) {
      for (const [id, end] of Object.entries(target[type])) {
        const old = start[type][id], item = result[type][id];
        for (const field of ['x', 'y', 'w', 'h', 'opacity', 'fontSize', 'iconScale', 'labelOffset']) {
          if (typeof end[field] === 'number') item[field] = mix(old[field], end[field], t);
        }
        for (const field of ['stroke', 'fill', 'color']) {
          if (end[field]) item[field] = color(old[field], end[field], t);
        }
        item.label = old.label === end.label || t >= 0.5 ? end.label : old.label;
        const startingOpacity = old.labelOpacity === undefined ? 1 : old.labelOpacity;
        item.labelOpacity = old.label === end.label ? mix(startingOpacity, 1, t) : t < 0.5 ? startingOpacity * (1 - t * 2) : (t - 0.5) * 2;
        if (type === 'links') {
          for (const field of ['from', 'to']) {
            // Re-anchoring a link to another node switches at the midpoint. Use a fade
            // or separate link for topology changes; the smooth path handles same ports.
            if (old[field].node === end[field].node && old[field].side === end[field].side) {
              item[field].at = mix(old[field].at ?? 0.5, end[field].at ?? 0.5, t);
            } else item[field] = copy(t < 0.5 ? old[field] : end[field]);
          }
        }
      }
    }
    return result;
  }
  const set = (element, values) => { if (element) for (const [key, value] of Object.entries(values)) element.setAttribute(key, value); };
  function textLines(element, label, x, y, fontSize, anchor) {
    const lines = label.split('\n');
    set(element, {x, y, 'text-anchor': anchor, 'font-size': fontSize});
    if (element.dataset.label !== label) {
      element.replaceChildren(...lines.map(line => {
        const span = element.ownerDocument.createElementNS('http://www.w3.org/2000/svg', 'tspan');
        span.textContent = line;
        return span;
      }));
      element.dataset.label = label;
    }
    [...element.children].forEach((span, i) => set(span, {x, y: y + (i - (lines.length - 1) / 2) * fontSize * 1.3}));
  }
  function render(scene, state) {
    for (const [id, node] of Object.entries(state.nodes)) {
      const group = scene.nodes.get(id), part = name => group.querySelector(`[data-part="${name}"]`);
      const {x, y, w, h, kind} = node;
      set(group, {opacity: node.opacity, 'aria-hidden': String(node.opacity < 0.01)});
      set(part('frame'), {x, y, width: w, height: h, fill: kind === 'callout' ? `url(#${scene.config.id}-red-dots)` : node.fill, stroke: node.stroke});
      if (kind === 'container') set(part('detail'), {x: x + 7, y: y + 7, width: w - 14, height: h - 14, stroke: node.stroke, opacity: 0.4});
      if (kind === 'storage') {
        set(part('frame'), {fill: `url(#${scene.config.id}-dots)`});
        set(part('detail'), {x: x + 8, y: y + 8, width: w - 16, height: h - 16, fill: node.fill, stroke: node.stroke, opacity: 1});
        const scale = node.iconScale ?? 1;
        const ix = x + 26, iy = y + h / 2 - 30 * scale;
        set(part('icon'), {d: `M${ix} ${iy}h${42*scale}v${60*scale}h${-42*scale}Z M${ix+8*scale} ${iy+12*scale}h${26*scale} M${ix+8*scale} ${iy+24*scale}h${26*scale} M${ix+8*scale} ${iy+36*scale}h${26*scale} M${ix+8*scale} ${iy+48*scale}h${26*scale}`, stroke: node.stroke});
      }
      if (kind === 'chip' || kind === 'memory') {
        let pins = '';
        for (let i = 1; i <= 6; i++) {
          const px = x + w * i / 7;
          pins += `M${px} ${y+h}v7 `;
          if (kind === 'chip') pins += `M${px} ${y}v-7 `;
        }
        if (kind === 'chip') for (let i = 1; i <= 4; i++) {
          const py = y + h * i / 5;
          pins += `M${x} ${py}h-7 M${x+w} ${py}h7 `;
        }
        set(part('icon'), {d: pins, stroke: node.stroke});
      }
      const labelX = kind === 'container' ? x + 24 : kind === 'storage' ? x + w * 0.60 : x + w / 2;
      const labelY = kind === 'container' ? y + 42 : y + h / 2 + node.fontSize * 0.34;
      textLines(part('label'), node.label, labelX, labelY, node.fontSize, kind === 'container' ? 'start' : 'middle');
      set(part('label'), {fill: node.color, opacity: node.labelOpacity ?? 1});
    }
    for (const [id, link] of Object.entries(state.links)) {
      const group = scene.links.get(id), line = group.querySelector('[data-part="line"]'), label = group.querySelector('[data-part="label"]');
      const path = route(state.nodes, link);
      set(group, {opacity: link.opacity, 'aria-hidden': String(link.opacity < 0.01)});
      set(line, {d: path.path, stroke: link.stroke, 'stroke-dasharray': link.dashed ? '7 7' : 'none'});
      set(scene.svg.querySelector(`[data-arrow="${id}"]`), {fill: link.stroke});
      textLines(label, link.label, (path.a[0] + path.b[0]) / 2, (path.a[1] + path.b[1]) / 2 + link.labelOffset, 20, 'middle');
      set(label, {fill: link.stroke, opacity: link.labelOpacity ?? 1});
    }
    scene.current = state;
  }
  function createPlugin() {
    let deck, scenes = [], media, destroyed = false;
    function stateIndex(scene) {
      return [...scene.element.querySelectorAll('.ps-diagram-step.visible')].reduce((n, step) => Math.max(n, Number(step.dataset.diagramStep)), 0);
    }
    function transition(scene, index, immediate) {
      const target = scene.config.stages[index];
      if (!target) throw new Error('Diagram stage out of range');
      if (!immediate && scene.index === index) return;
      cancelAnimationFrame(scene.frame);
      scene.index = index;
      scene.element.dataset.psState = String(index);
      scene.element.dataset.psStage = target.name;
      const heading = scene.element.querySelector('[data-ps-heading]');
      if (target.emphasis) {
        const at = target.heading.indexOf(target.emphasis), accent = heading.ownerDocument.createElement('span');
        accent.className = 'accent'; accent.textContent = target.emphasis;
        heading.replaceChildren(heading.ownerDocument.createTextNode(target.heading.slice(0, at)), accent, heading.ownerDocument.createTextNode(target.heading.slice(at + target.emphasis.length)));
      } else heading.textContent = target.heading;
      scene.svg.querySelector('desc').textContent = target.description;
      const finish = () => {render(scene, copy(target)); scene.element.dataset.psAnimating = 'false';};
      if (immediate || media.matches || !scene.config.duration) { finish(); return; }
      const start = copy(scene.current), started = performance.now();
      scene.element.dataset.psAnimating = 'true';
      function tick(now) {
        if (destroyed) return;
        const progress = Math.min(1, (now - started) / scene.config.duration);
        render(scene, interpolate(start, target, ease(progress)));
        if (progress < 1) scene.frame = requestAnimationFrame(tick);
        else finish();
      }
      scene.frame = requestAnimationFrame(tick);
    }
    function sync() {
      for (const scene of scenes) {
        const offSlide = scene.element.closest('section') !== deck.getCurrentSlide();
        transition(scene, stateIndex(scene), offSlide || !scene.current);
      }
    }
    function settle() {for (const scene of scenes) transition(scene, stateIndex(scene), true);}
    function mediaChanged() {if (media.matches) settle();}
    return {
      id: 'ps-diagrams',
      init(instance) {
        deck = instance;
        media = window.matchMedia('(prefers-reduced-motion: reduce)');
        scenes = [...deck.getRevealElement().querySelectorAll('[data-ps-scene]')].map(element => {
          const svg = element.querySelector('svg'), config = JSON.parse(svg.querySelector('[data-ps-config]').textContent);
          return {element, svg, config, frame: 0, index: -1,
            nodes: new Map([...svg.querySelectorAll('[data-node]')].map(node => [node.dataset.node, node])),
            links: new Map([...svg.querySelectorAll('[data-link]')].map(link => [link.dataset.link, link]))};
        });
        for (const event of ['ready', 'slidechanged']) deck.on(event, settle);
        for (const event of ['fragmentshown', 'fragmenthidden']) deck.on(event, sync);
        media.addEventListener('change', mediaChanged);
        // Render immediately; ready reconciles direct fragment hashes after Reveal initializes.
        settle();
      },
      settle,
      destroy() {
        destroyed = true;
        for (const event of ['ready', 'slidechanged']) deck.off(event, settle);
        for (const event of ['fragmentshown', 'fragmenthidden']) deck.off(event, sync);
        media.removeEventListener('change', mediaChanged);
        for (const scene of scenes) cancelAnimationFrame(scene.frame);
      }
    };
  }
  root.PlanetScaleDiagrams = {createPlugin};
  if (typeof module !== 'undefined' && module.exports) module.exports = {port, route, interpolate, ease};
})(typeof window !== 'undefined' ? window : globalThis);
