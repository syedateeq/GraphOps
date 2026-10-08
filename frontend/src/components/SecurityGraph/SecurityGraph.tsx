import { useRef, useEffect, useCallback } from 'react'
import cytoscape, { type Core, type ElementDefinition } from 'cytoscape'
import type { BlastRadiusResponse, AttackPathResponse } from '../../services/api'

/* ── Node colour map ──────────────────────────────────── */
const NODE_COLORS: Record<string, string> = {
  User:          '#38bdf8',
  Device:        '#a78bfa',
  Server:        '#34d399',
  Application:   '#fbbf24',
  Database:      '#f87171',
  IP:            '#64748b',
  Vulnerability: '#fb923c',
}

const NODE_SHAPES: Record<string, string> = {
  User:          'ellipse',
  Device:        'round-rectangle',
  Server:        'hexagon',
  Application:   'diamond',
  Database:      'barrel',
  IP:            'ellipse',
  Vulnerability: 'triangle',
}

/* ── Helpers ──────────────────────────────────────────── */

function primaryLabel(labels: string[]): string {
  for (const l of labels) {
    if (NODE_COLORS[l]) return l
  }
  return labels[0] ?? 'Node'
}

function displayName(node: Record<string, unknown>): string {
  for (const key of ['name', 'hostname', 'deviceId', 'userId', 'serverId', 'appId', 'databaseId', 'cveId', 'address']) {
    if (node[key] && typeof node[key] === 'string') return node[key] as string
  }
  return 'Unknown'
}

function nodeId(node: Record<string, unknown>): string {
  for (const key of ['deviceId', 'userId', 'serverId', 'appId', 'databaseId', 'cveId', 'address']) {
    if (node[key] && typeof node[key] === 'string') return node[key] as string
  }
  return (node['elementId'] as string) ?? 'unknown'
}

/* ── Props ────────────────────────────────────────────── */
export interface SecurityGraphProps {
  blastRadius: BlastRadiusResponse | null
  attackPath: AttackPathResponse | null
  highlightMode: 'none' | 'blast' | 'attack'
  onNodeClick?: (nodeData: Record<string, unknown>) => void
}

export default function SecurityGraph({
  blastRadius,
  attackPath,
  highlightMode,
  onNodeClick,
}: SecurityGraphProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const cyRef = useRef<Core | null>(null)

  /* ── Build elements from blast radius data ─────────── */
  const buildElements = useCallback((): ElementDefinition[] => {
    if (!blastRadius) return []

    const elements: ElementDefinition[] = []
    const nodeSet = new Set<string>()

    // Add the compromised device itself
    const compId = blastRadius.compromised_device
    nodeSet.add(compId)
    elements.push({
      data: {
        id: compId,
        label: compId,
        nodeType: 'Device',
        isCompromised: true,
        _raw: { deviceId: compId, labels: ['Device'] },
      },
    })

    // Add all reachable nodes
    for (const n of blastRadius.all_nodes) {
      const nid = nodeId(n)
      if (nodeSet.has(nid)) continue
      nodeSet.add(nid)
      const lab = primaryLabel(n.labels)
      elements.push({
        data: {
          id: nid,
          label: displayName(n),
          nodeType: lab,
          criticality: (n as Record<string, unknown>)['criticality'] ?? '',
          _raw: n,
        },
      })
    }

    // Add relationships
    const edgeSet = new Set<string>()
    for (const r of blastRadius.relationships) {
      // Map element IDs to our node IDs
      const srcEl = r.startNodeElementId
      const tgtEl = r.endNodeElementId

      // Find our IDs from the node data
      const srcNode = blastRadius.all_nodes.find(
        (n) => (n as Record<string, unknown>)['elementId'] === srcEl
      )
      const tgtNode = blastRadius.all_nodes.find(
        (n) => (n as Record<string, unknown>)['elementId'] === tgtEl
      )

      let srcId = srcNode ? nodeId(srcNode) : ''
      let tgtId = tgtNode ? nodeId(tgtNode) : ''

      // The compromised device itself might not be in all_nodes
      if (!srcId && srcEl) srcId = compId
      if (!tgtId && tgtEl) tgtId = compId

      if (!srcId || !tgtId) continue
      if (!nodeSet.has(srcId) || !nodeSet.has(tgtId)) continue

      const edgeKey = `${srcId}-${r.type}-${tgtId}`
      if (edgeSet.has(edgeKey)) continue
      edgeSet.add(edgeKey)

      elements.push({
        data: {
          id: edgeKey,
          source: srcId,
          target: tgtId,
          label: r.type,
          relType: r.type,
        },
      })
    }

    return elements
  }, [blastRadius])

  /* ── Init / update graph ───────────────────────────── */
  useEffect(() => {
    if (!containerRef.current) return

    const elements = buildElements()

    if (cyRef.current) {
      cyRef.current.destroy()
      cyRef.current = null
    }

    if (elements.length === 0) return

    const cy = cytoscape({
      container: containerRef.current,
      elements,
      style: [
        {
          selector: 'node',
          style: {
            'label': 'data(label)',
            'text-valign': 'bottom',
            'text-halign': 'center',
            'font-size': '9px',
            'font-family': 'Inter, system-ui, sans-serif',
            'color': '#94a3b8',
            'text-margin-y': 5,
            'text-wrap': 'ellipsis',
            'text-max-width': '80px',
            'width': 28,
            'height': 28,
            'border-width': 2,
            'border-color': '#1e293b',
            'background-color': '#64748b',
            'transition-property': 'background-color, border-color, width, height, opacity',
            'transition-duration': 200,
          },
        },
        // Dynamic node colours by type
        ...Object.entries(NODE_COLORS).map(([label, color]) => ({
          selector: `node[nodeType="${label}"]`,
          style: {
            'background-color': color,
            'shape': (NODE_SHAPES[label] ?? 'ellipse') as cytoscape.Css.NodeShape,
          },
        })),
        // Compromised node
        {
          selector: 'node[?isCompromised]',
          style: {
            'border-color': '#f87171',
            'border-width': 3,
            'width': 36,
            'height': 36,
          },
        },
        // Critical nodes
        {
          selector: 'node[criticality="critical"]',
          style: {
            'border-color': '#f87171',
            'border-width': 2,
          },
        },
        {
          selector: 'node[criticality="high"]',
          style: {
            'border-color': '#fb923c',
            'border-width': 2,
          },
        },
        // Edges
        {
          selector: 'edge',
          style: {
            'width': 1.5,
            'line-color': '#1e293b',
            'target-arrow-color': '#1e293b',
            'target-arrow-shape': 'triangle',
            'arrow-scale': 0.7,
            'curve-style': 'bezier',
            'label': 'data(label)',
            'font-size': '6px',
            'font-family': 'Inter, system-ui, sans-serif',
            'color': '#475569',
            'text-rotation': 'autorotate',
            'text-background-color': '#060a13',
            'text-background-opacity': 0.8,
            'text-background-padding': '2px',
            'transition-property': 'line-color, target-arrow-color, width, opacity',
            'transition-duration': 200,
          },
        },
        // Dimmed classes
        {
          selector: '.dimmed',
          style: {
            'opacity': 0.15,
          },
        },
        {
          selector: '.blast-highlight',
          style: {
            'opacity': 1,
            'border-color': '#38bdf8',
            'border-width': 2,
          },
        },
        {
          selector: '.blast-highlight-edge',
          style: {
            'opacity': 1,
            'line-color': '#38bdf8',
            'target-arrow-color': '#38bdf8',
            'width': 2,
          },
        },
        {
          selector: '.attack-path-node',
          style: {
            'opacity': 1,
            'border-color': '#f87171',
            'border-width': 3,
            'width': 34,
            'height': 34,
          },
        },
        {
          selector: '.attack-path-edge',
          style: {
            'opacity': 1,
            'line-color': '#f87171',
            'target-arrow-color': '#f87171',
            'width': 3,
          },
        },
        {
          selector: ':selected',
          style: {
            'border-color': '#fbbf24',
            'border-width': 3,
          },
        },
      ],
      layout: {
        name: 'cose',
        animate: false,
        padding: 40,
        nodeRepulsion: () => 8000,
        idealEdgeLength: () => 120,
        edgeElasticity: () => 100,
        gravity: 0.3,
        numIter: 1000,
      } as cytoscape.CoseLayoutOptions,
      minZoom: 0.2,
      maxZoom: 3,
      wheelSensitivity: 0.3,
    })

    // Click handler
    cy.on('tap', 'node', (evt) => {
      const data = evt.target.data()
      onNodeClick?.(data._raw ?? data)
    })

    cyRef.current = cy

    return () => {
      cy.destroy()
      cyRef.current = null
    }
  }, [buildElements, onNodeClick])

  /* ── Apply highlight mode ──────────────────────────── */
  useEffect(() => {
    const cy = cyRef.current
    if (!cy) return

    // Reset all
    cy.elements().removeClass('dimmed blast-highlight blast-highlight-edge attack-path-node attack-path-edge')

    if (highlightMode === 'blast' && blastRadius) {
      // Dim everything, then highlight blast radius nodes
      cy.elements().addClass('dimmed')

      const compId = blastRadius.compromised_device
      const affectedIds = new Set<string>([compId])
      for (const n of blastRadius.all_nodes) {
        affectedIds.add(nodeId(n))
      }

      cy.nodes().forEach((node) => {
        if (affectedIds.has(node.id())) {
          node.removeClass('dimmed').addClass('blast-highlight')
        }
      })

      cy.edges().forEach((edge) => {
        const s = edge.source().id()
        const t = edge.target().id()
        if (affectedIds.has(s) && affectedIds.has(t)) {
          edge.removeClass('dimmed').addClass('blast-highlight-edge')
        }
      })
    }

    if (highlightMode === 'attack' && attackPath?.shortest_path) {
      cy.elements().addClass('dimmed')

      const pathNodeIds = new Set<string>()
      for (const n of attackPath.shortest_path.nodes) {
        pathNodeIds.add(nodeId(n))
      }

      cy.nodes().forEach((node) => {
        if (pathNodeIds.has(node.id())) {
          node.removeClass('dimmed').addClass('attack-path-node')
        }
      })

      // Highlight edges between consecutive path nodes
      const pathNodes = attackPath.shortest_path.nodes.map((n) => nodeId(n))
      for (let i = 0; i < pathNodes.length - 1; i++) {
        const a = pathNodes[i]
        const b = pathNodes[i + 1]
        cy.edges().forEach((edge) => {
          const s = edge.source().id()
          const t = edge.target().id()
          if ((s === a && t === b) || (s === b && t === a)) {
            edge.removeClass('dimmed').addClass('attack-path-edge')
          }
        })
      }
    }
  }, [highlightMode, blastRadius, attackPath])

  /* ── Public method: fit ─────────────────────────────── */
  useEffect(() => {
    // Expose fit via a data attribute
    const el = containerRef.current
    if (el) {
      (el as HTMLDivElement & { cyFit?: () => void }).cyFit = () => {
        cyRef.current?.fit(undefined, 40)
      }
    }
  })

  return (
    <div
      ref={containerRef}
      className="graph-container"
      style={{ width: '100%', height: '100%' }}
    />
  )
}
