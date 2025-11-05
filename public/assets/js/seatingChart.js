/**
 * D3.js Seating Chart Module
 * Renders hemicycle seating charts for legislative chambers
 */

(function (global) {
  'use strict';

  // Base dimensions (at scale = 1.0)
  const BASE_WIDTH = 480;
  const BASE_HEIGHT = 320;
  const DEFAULT_SCALE = 0.75;

  /**
   * Calculate hemicycle positions for seats
   * @param {number} totalSeats - Total number of seats
   * @param {number} numRows - Number of concentric rows
   * @param {number} width - Chart width
   * @param {number} height - Chart height
   * @returns {Array} Array of {x, y, angle} positions
   */
  function calculateHemicyclePositions(totalSeats, numRows, width, height) {
    const positions = [];
    const centerX = width / 2;
    const centerY = height * 0.85; // Position hemicycle lower in viewport

    // Calculate seats per row (more in back rows)
    const seatsPerRow = [];
    let remainingSeats = totalSeats;

    for (let row = 0; row < numRows; row++) {
      // Front rows have fewer seats, back rows have more
      const ratio = (row + 1) / numRows;
      const rowSeats = Math.round((totalSeats / numRows) * (0.7 + ratio * 0.6));
      seatsPerRow.push(Math.min(rowSeats, remainingSeats));
      remainingSeats -= seatsPerRow[row];
    }

    // Adjust if we have leftover seats
    let rowIndex = numRows - 1;
    while (remainingSeats > 0) {
      seatsPerRow[rowIndex]++;
      remainingSeats--;
      rowIndex = (rowIndex - 1 + numRows) % numRows;
    }

    // Calculate positions
    let seatIndex = 0;
    for (let row = 0; row < numRows; row++) {
      const rowSeats = seatsPerRow[row];
      const radius = (height * 0.15) + (row * (height * 0.65) / numRows);

      for (let seat = 0; seat < rowSeats; seat++) {
        // Distribute evenly across 180 degrees (π radians)
        const angle = Math.PI * (seat / (rowSeats - 1 || 1));
        const x = centerX + radius * Math.cos(Math.PI - angle);
        const y = centerY - radius * Math.sin(Math.PI - angle);

        positions.push({
          x,
          y,
          angle,
          row,
          seatIndex: seatIndex++
        });
      }
    }

    return positions;
  }

  /**
   * Prepare seat data by combining positions with party information
   */
  function prepareSeatData(chamberData) {
    const seats = [];
    let seatNumber = 0;

    // Sort parties to put them in consistent order
    const parties = [...chamberData.parties].sort((a, b) => b.seats - a.seats);

    for (const party of parties) {
      for (let i = 0; i < party.seats; i++) {
        seats.push({
          seatNumber: seatNumber++,
          party: party.code,
          partyLabel: party.label,
          color: party.color,
          label: null,
          url: null
        });
      }
    }

    // Merge with labels if provided
    if (chamberData.labels && chamberData.labels.length > 0) {
      chamberData.labels.forEach(labelInfo => {
        if (seats[labelInfo.seat]) {
          seats[labelInfo.seat].label = labelInfo.label;
          seats[labelInfo.seat].url = labelInfo.url;
        }
      });
    }

    return seats;
  }

  /**
   * Generic chamber renderer
   */
  function renderChamber(containerId, chamberData, options = {}) {
    const container = d3.select(`#${containerId}`);
    if (container.empty()) {
      console.error(`Container #${containerId} not found`);
      return;
    }

    // Clear existing content
    container.html('');

    // Options
    const scale = options.scale || DEFAULT_SCALE;
    const width = BASE_WIDTH * scale;
    const height = BASE_HEIGHT * scale;
    const numRows = options.rows || (chamberData.total > 200 ? 8 : 5);
    const seatRadius = options.seatRadius || (chamberData.total > 200 ? 3.5 : 5);

    // Calculate positions
    const positions = calculateHemicyclePositions(chamberData.total, numRows, width, height);

    // Prepare seat data
    const seatData = prepareSeatData(chamberData);

    // Merge positions with seat data
    const seats = seatData.map((seat, i) => ({
      ...seat,
      ...positions[i]
    }));

    // Create SVG
    const svg = container
      .append('svg')
      .attr('class', 'chart-svg')
      .attr('width', width)
      .attr('height', height)
      .attr('role', 'img')
      .attr('aria-label', `${options.title || 'Chamber'} seating chart with ${chamberData.total} seats`);

    // Create tooltip
    const tooltip = container
      .append('div')
      .attr('class', 'seating-tooltip')
      .attr('role', 'tooltip')
      .attr('aria-hidden', 'true');

    // Track active parties for legend toggle
    const activeParties = new Set(chamberData.parties.map(p => p.code));

    // Draw majority marker
    if (chamberData.majority) {
      const majorityIndex = chamberData.majority - 1;
      if (seats[majorityIndex]) {
        const majorityPos = seats[majorityIndex];

        // Draw a small arc at the majority line
        const centerX = width / 2;
        const centerY = height * 0.85;
        const innerRadius = majorityPos.row * (height * 0.65) / numRows + (height * 0.15);
        const outerRadius = innerRadius + (height * 0.1);

        const majorityAngle = majorityPos.angle;

        // Draw radial line
        svg.append('line')
          .attr('class', 'majority-line')
          .attr('x1', centerX + innerRadius * Math.cos(Math.PI - majorityAngle))
          .attr('y1', centerY - innerRadius * Math.sin(Math.PI - majorityAngle))
          .attr('x2', centerX + outerRadius * Math.cos(Math.PI - majorityAngle))
          .attr('y2', centerY - outerRadius * Math.sin(Math.PI - majorityAngle));

        // Add text annotation
        svg.append('text')
          .attr('class', 'majority-text')
          .attr('x', centerX + (outerRadius + 15) * Math.cos(Math.PI - majorityAngle))
          .attr('y', centerY - (outerRadius + 15) * Math.sin(Math.PI - majorityAngle))
          .text(`${chamberData.majority} to majority`);
      }
    }

    // Draw seats
    const seatGroups = svg.selectAll('.seat')
      .data(seats)
      .enter()
      .append('circle')
      .attr('class', d => `seat ${d.url ? 'clickable' : ''}`)
      .attr('cx', d => d.x)
      .attr('cy', d => d.y)
      .attr('r', seatRadius)
      .attr('fill', d => d.color)
      .attr('data-party', d => d.party)
      .attr('tabindex', d => d.url ? 0 : -1)
      .attr('role', d => d.url ? 'link' : 'presentation')
      .attr('aria-label', d => {
        let label = `${d.partyLabel} seat ${d.seatNumber + 1}`;
        if (d.label) label += `, ${d.label}`;
        return label;
      })
      .on('mouseover', function(event, d) {
        // Show tooltip
        let tooltipContent = `<div class="party-name">${d.partyLabel}</div>`;
        tooltipContent += `<div class="seat-info">Seat ${d.seatNumber + 1}`;
        if (d.label) tooltipContent += ` • ${d.label}`;
        tooltipContent += '</div>';

        tooltip
          .html(tooltipContent)
          .classed('visible', true)
          .style('left', (event.pageX + 10) + 'px')
          .style('top', (event.pageY - 10) + 'px')
          .attr('aria-hidden', 'false');
      })
      .on('mousemove', function(event) {
        tooltip
          .style('left', (event.pageX + 10) + 'px')
          .style('top', (event.pageY - 10) + 'px');
      })
      .on('mouseout', function() {
        tooltip
          .classed('visible', false)
          .attr('aria-hidden', 'true');
      })
      .on('click', function(event, d) {
        if (d.url) {
          window.open(d.url, '_blank', 'noopener,noreferrer');
        }
      })
      .on('keydown', function(event, d) {
        if (d.url && (event.key === 'Enter' || event.key === ' ')) {
          event.preventDefault();
          window.open(d.url, '_blank', 'noopener,noreferrer');
        }
      });

    // Create legend
    const legend = container
      .append('div')
      .attr('class', 'chart-legend')
      .attr('role', 'list');

    chamberData.parties.forEach(party => {
      const legendItem = legend
        .append('div')
        .attr('class', 'legend-item')
        .attr('role', 'listitem')
        .attr('tabindex', 0)
        .attr('aria-label', `Toggle ${party.label} seats (${party.seats} seats)`)
        .on('click', function() {
          toggleParty(party.code);
        })
        .on('keydown', function(event) {
          if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            toggleParty(party.code);
          }
        });

      legendItem
        .append('div')
        .attr('class', 'legend-dot')
        .style('background-color', party.color);

      legendItem
        .append('span')
        .attr('class', 'legend-label')
        .text(party.label);

      legendItem
        .append('span')
        .attr('class', 'legend-count')
        .text(`(${party.seats})`);
    });

    // Toggle party visibility
    function toggleParty(partyCode) {
      if (activeParties.has(partyCode)) {
        activeParties.delete(partyCode);
      } else {
        activeParties.add(partyCode);
      }

      // Update seat visibility
      svg.selectAll('.seat')
        .classed('hidden', d => !activeParties.has(d.party));

      // Update legend item appearance
      legend.selectAll('.legend-item')
        .classed('inactive', function() {
          const item = d3.select(this);
          const partyLabel = item.select('.legend-label').text();
          const party = chamberData.parties.find(p => p.label === partyLabel);
          return party && !activeParties.has(party.code);
        });
    }

    return {
      svg,
      tooltip,
      legend,
      seats
    };
  }

  /**
   * Render House chamber
   */
  function renderHouse(containerId, chamberData, options = {}) {
    return renderChamber(containerId, chamberData, {
      ...options,
      rows: options.rows || 8,
      seatRadius: options.seatRadius || 3.5,
      title: 'House of Representatives'
    });
  }

  /**
   * Render Senate chamber
   */
  function renderSenate(containerId, chamberData, options = {}) {
    return renderChamber(containerId, chamberData, {
      ...options,
      rows: options.rows || 5,
      seatRadius: options.seatRadius || 5,
      title: 'Senate'
    });
  }

  // Export functions
  if (typeof module !== 'undefined' && module.exports) {
    // Node.js / CommonJS
    module.exports = {
      renderChamber,
      renderHouse,
      renderSenate
    };
  } else {
    // Browser global
    global.SeatChart = {
      renderChamber,
      renderHouse,
      renderSenate
    };
  }

})(typeof window !== 'undefined' ? window : this);
