<template>
  <div ref="container" class="org-d3-tree-container">
    <svg ref="svg" :height="height" :width="width"></svg>
  </div>
</template>

<script setup>
  import { onMounted, ref, watch } from 'vue'
  import * as d3 from 'd3'

  const props = defineProps({
    members: Array, // flat array of members
    rootId: Number,
    width: { type: Number, default: 1200 },
    height: { type: Number, default: 600 },
  })

  const svg = ref(null)
  const container = ref(null)

  function buildHierarchy(members, rootId) {
    const map = {}
    members.forEach((m) => (map[m.id] = { ...m, children: [] }))
    const root = map[rootId]
    members.forEach((m) => {
      if (m.supervisor_id && map[m.supervisor_id]) {
        map[m.supervisor_id].children.push(map[m.id])
      }
    })
    return root
  }

  // Helper to measure text width using SVG
  function measureText(text, fontSize = 15, fontWeight = 400) {
    const tempSvg = d3.select(svg.value)
    const tempText = tempSvg
      .append('text')
      .attr('font-size', fontSize)
      .attr('font-weight', fontWeight)
      .attr('visibility', 'hidden')
      .text(text)
    const width = tempText.node().getBBox().width
    tempText.remove()
    return width
  }

  function computeBoxSizes(root) {
    root.each((d) => {
      const name = d.data.first_name + ' ' + d.data.last_name
      const position = d.data.position || ''
      // Word wrap position to max 20 chars per line
      const posLines = []
      let str = position
      while (str.length > 0) {
        if (str.length <= 20) {
          posLines.push(str)
          break
        }
        let idx = str.lastIndexOf(' ', 20)
        if (idx === -1) idx = 20
        posLines.push(str.slice(0, idx))
        str = str.slice(idx).trim()
      }
      d.data._posLines = posLines
      // Measure width for each line
      const nameWidth = measureText(name, 15, 600)
      const posLineWidths = posLines.map((line) => measureText(line, 13, 400))
      const maxPosWidth = posLineWidths.length ? Math.max(...posLineWidths) : 0
      d.data.boxWidth = Math.max(120, nameWidth, maxPosWidth) + 32 // padding
      // Calculate boxHeight and store for later use
      d.data._nameY = -((posLines.length * 16) / 2) + 7 // name y offset so name is always near the top
      d.data._firstPosY = d.data._nameY + 20 // first position line y offset
      d.data.boxHeight = 24 + posLines.length * 16 + 16 // 24 for name+padding, 16 per line, 16 bottom padding
    })
  }

  // Custom horizontal layout to prevent overlap
  function layoutTree(root) {
    // Assign x = depth, y = breadth
    const nodeHeight = 100
    const nodeWSpacing = 80 // horizontal gap between nodes (increased for connectors)
    let maxDepth = 0
    root.each((d) => {
      d.x = d.depth * (220 + nodeWSpacing) // increased horizontal spacing
      maxDepth = Math.max(maxDepth, d.depth)
    })
    // Recursively set y positions to avoid overlap
    let nextY = 0
    function setY(d) {
      if (!d.children || d.children.length === 0) {
        d.y = nextY + d.data.boxHeight / 2
        nextY += d.data.boxHeight + nodeHeight / 2
      } else {
        d.children.forEach((c) => setY(c))
        const minY = d3.min(d.children, (c) => c.y - c.data.boxHeight / 2)
        const maxY = d3.max(d.children, (c) => c.y + c.data.boxHeight / 2)
        d.y = (minY + maxY) / 2
      }
    }
    setY(root)
  }

  function renderTree() {
    if (!props.members.length || !props.rootId) return
    const data = buildHierarchy(props.members, props.rootId)
    const root = d3.hierarchy(data)

    // Precompute box sizes
    computeBoxSizes(root)
    // Custom layout
    layoutTree(root)

    const svgEl = d3.select(svg.value)
    svgEl.selectAll('*').remove()

    // Draw links
    svgEl
      .selectAll('path.link')
      .data(root.links())
      .enter()
      .append('path')
      .attr('class', 'link')
      .attr('d', (d) => {
        // Horizontal elbow connector
        const startX = d.source.x + d.source.data.boxWidth / 2
        const startY = d.source.y
        const endX = d.target.x - d.target.data.boxWidth / 2
        const endY = d.target.y
        return `M${startX},${startY}C${(startX + endX) / 2},${startY} ${(startX + endX) / 2},${endY} ${endX},${endY}`
      })
      .attr('stroke', '#1976d2')
      .attr('stroke-width', 2)
      .attr('fill', 'none')

    // Adjust SVG viewBox and centering for root node
    // Calculate min/max x/y to fit all nodes
    const nodes = root.descendants()
    const minX = Math.min(...nodes.map((d) => d.x - d.data.boxWidth / 2))
    const maxX = Math.max(...nodes.map((d) => d.x + d.data.boxWidth / 2))
    const minY = Math.min(...nodes.map((d) => d.y - d.data.boxHeight / 2))
    const maxY = Math.max(...nodes.map((d) => d.y + d.data.boxHeight / 2))
    svgEl.attr(
      'viewBox',
      `${minX - 40} ${minY - 40} ${maxX - minX + 80} ${maxY - minY + 80}`
    )

    const node = svgEl
      .selectAll('g.node')
      .data(root.descendants())
      .enter()
      .append('g')
      .attr('class', 'node')
      .attr('transform', (d) => `translate(${d.x},${d.y})`)

    node
      .append('rect')
      .attr('width', (d) => d.data.boxWidth)
      .attr('height', (d) => d.data.boxHeight)
      .attr('x', (d) => -d.data.boxWidth / 2)
      .attr('y', (d) => -d.data.boxHeight / 2)
      .attr('fill', '#fff')
      .attr('stroke', '#1976d2')
      .attr('rx', 8)
      .attr('ry', 8)

    node
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('y', (d) => d.data._nameY)
      .attr('font-size', 15)
      .attr('font-weight', 600)
      .text((d) => d.data.first_name + ' ' + d.data.last_name)

    // Word wrap position text to 20 chars per line and render tspans
    node
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('y', (d) => d.data._firstPosY)
      .attr('font-size', 13)
      .attr('fill', '#888')
      .selectAll('tspan')
      .data((d) => d.data._posLines || [])
      .enter()
      .append('tspan')
      .attr('x', 0)
      .attr('dy', (d, i) => (i === 0 ? 0 : 16))
      .text((d) => d)
  }

  onMounted(renderTree)
  watch(() => [props.members, props.rootId], renderTree, { deep: true })
</script>

<style scoped>
  .org-d3-tree-container {
    display: flex;
    justify-content: center;
    margin-top: 32px;
    overflow-x: auto;
  }
  .link {
    stroke: #1976d2;
    stroke-width: 2;
    fill: none;
  }
</style>
