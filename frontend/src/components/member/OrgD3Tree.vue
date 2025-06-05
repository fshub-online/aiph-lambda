<template>
  <div ref="container" class="org-d3-tree-container">
    <svg ref="svg" :preserveAspectRatio="'xMidYMid meet'"></svg>
  </div>
</template>

<script setup>
  import { onMounted, ref, watch } from 'vue'
  import * as d3 from 'd3'

  const props = defineProps({
    members: Array, // flat array of members
    rootId: Number,
    width: { type: Number, default: 2200 }, // larger default width
    height: { type: Number, default: 2000 }, // larger default height
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
        let idx = str.lastIndexOf(' ', 25)
        if (idx === -1) idx = 25
        posLines.push(str.slice(0, idx))
        str = str.slice(idx).trim()
      }
      d.data._posLines = posLines
      // Measure width for each line
      const nameWidth = measureText(name, 22, 700) // larger font
      const posLineWidths = posLines.map((line) => measureText(line, 18, 400))
      const maxPosWidth = posLineWidths.length ? Math.max(...posLineWidths) : 0
      d.data.boxWidth = Math.max(200, nameWidth, maxPosWidth) + 28 // more padding
      // Calculate boxHeight and store for later use
      d.data._nameY = -((posLines.length * 22) / 2) + 7 // name y offset so name is always near the top
      d.data._firstPosY = d.data._nameY + 28 // first position line y offset
      d.data.boxHeight = 36 + posLines.length * 22 + 24 // 36 for name+padding, 22 per line, 24 bottom padding
    })
  }

  // Custom vertical layout to prevent overlap
  function layoutTree(root) {
    // Assign x = depth (vertical), y = breadth (horizontal)
    const nodeHeight = 120
    const nodeVSpacing = 80 // vertical gap between levels
    const nodeHSpacing = 80 // horizontal gap between siblings
    let maxDepth = 0
    // First, compute x (vertical) by depth
    root.each((d) => {
      d.x = d.depth * (nodeHeight + nodeVSpacing)
      maxDepth = Math.max(maxDepth, d.depth)
    })
    // Recursively set y positions to avoid overlap
    let nextY = 0
    function setY(d) {
      if (!d.children || d.children.length === 0) {
        d.y = nextY + d.data.boxWidth / 2
        nextY += d.data.boxWidth + nodeHSpacing / 2
      } else {
        d.children.forEach((c) => setY(c))
        const minY = d3.min(d.children, (c) => c.y - c.data.boxWidth / 2)
        const maxY = d3.max(d.children, (c) => c.y + c.data.boxWidth / 2)
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

    // Calculate min/max x/y to fit all nodes
    const nodes = root.descendants()
    const minX = Math.min(...nodes.map((d) => d.x - d.data.boxHeight / 2))
    const maxX = Math.max(...nodes.map((d) => d.x + d.data.boxHeight / 2))
    const minY = Math.min(...nodes.map((d) => d.y - d.data.boxWidth / 2))
    const maxY = Math.max(...nodes.map((d) => d.y + d.data.boxWidth / 2))
    const treeWidth = maxY - minY + 80
    const treeHeight = maxX - minX + 80

    // Set viewBox to fit the tree bounding box
    svgEl.attr(
      'viewBox',
      `${minY - 40} ${minX - 40} ${treeWidth} ${treeHeight}`
    )

    // Responsive horizontal scaling
    const containerEl = container.value
    const containerWidth = containerEl ? containerEl.clientWidth : treeWidth
    let scaleX = 1
    if (treeWidth > containerWidth) {
      scaleX = containerWidth / treeWidth
    }

    // Create a group for scaling
    const g = svgEl.append('g').attr('transform', `scale(${scaleX},1)`)
    g.selectAll('path.link')
      .data(root.links())
      .enter()
      .append('path')
      .attr('class', 'link')
      .attr('d', (d) => {
        // Vertical elbow connector (top-to-bottom)
        const startX = d.source.y
        const startY = d.source.x + d.source.data.boxHeight / 2
        const endX = d.target.y
        const endY = d.target.x - d.target.data.boxHeight / 2
        return `M${startX},${startY}C${startX},${(startY + endY) / 2} ${endX},${(startY + endY) / 2} ${endX},${endY}`
      })
      .attr('stroke', '#1976d2')
      .attr('stroke-width', 4)
      .attr('fill', 'none')

    // Draw nodes
    const node = g
      .selectAll('g.node')
      .data(root.descendants())
      .enter()
      .append('g')
      .attr('class', 'node')
      .attr('transform', (d) => `translate(${d.y},${d.x})`)

    node
      .append('rect')
      .attr('width', (d) => d.data.boxWidth)
      .attr('height', (d) => d.data.boxHeight)
      .attr('x', (d) => -d.data.boxWidth / 2)
      .attr('y', (d) => -d.data.boxHeight / 2)
      .attr('fill', '#fff')
      .attr('stroke', '#1976d2')
      .attr('stroke-width', 4)
      .attr('rx', 12)
      .attr('ry', 12)

    node
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('y', (d) => d.data._nameY)
      .attr('font-size', 22)
      .attr('font-weight', 700)
      .text((d) => d.data.first_name + ' ' + d.data.last_name)

    // Word wrap position text to 20 chars per line and render tspans
    node
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('y', (d) => d.data._firstPosY)
      .attr('font-size', 18)
      .attr('fill', '#888')
      .selectAll('tspan')
      .data((d) => d.data._posLines || [])
      .enter()
      .append('tspan')
      .attr('x', 0)
      .attr('dy', (d, i) => (i === 0 ? 0 : 22))
      .text((d) => d)
  }

  onMounted(renderTree)
  watch(() => [props.members, props.rootId], renderTree, { deep: true })
</script>

<style scoped>
  .org-d3-tree-container {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    margin-top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background: #ffffff;
    border-radius: 12px;
    padding: 0;
  }
  .link {
    stroke: #1976d2;
    stroke-width: 4;
    fill: none;
  }
</style>
