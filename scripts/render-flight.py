#!/usr/bin/env python3
"""Render retained flight telemetry; never run or modify a simulation.

Usage: python3 scripts/render-flight.py RUN_DIRECTORY assets/projects
Requires ffmpeg with librsvg support. The input directory contains flight.json
and scenario.json. Animation selects recorded samples without interpolation.
"""

import bisect
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile


def render(run, output):
    flight = json.loads((run / 'flight.json').read_text())
    scenario = json.loads((run / 'scenario.json').read_text())
    assert flight['physical_outcome'] == 'landed_on_target'
    assert flight['mission_outcome'] == 'success'
    assert flight['integrity_passed'] and flight['final_source_replay_passed']
    assert flight['correction_count'] == 3
    assert flight['input_identity'] == 'fnv1a64:c17a2218c281cc8d', 'Expected the retained plateau flight'
    samples = flight['ordinary_flight']['samples']
    times = [sample['sim_time_s'] for sample in samples]
    handoffs = [cycle['current_state'] for cycle in flight['cycles'][1:]]
    scale = 878 / 1220

    def point(position):
        return 72 + (position['x'] + 1060) * scale, 480 - position['y'] * scale

    def pairs(positions):
        return ' '.join(f'{x:.2f},{y:.2f}' for x, y in map(point, positions))

    terrain = pairs(scenario['world']['terrain']['points_m'])
    grid = ''.join(f'<path d="M72 {480-height*scale:.2f}H950"/>'
                   for height in [0, 100, 200, 300, 400])
    launch_x, _ = point(samples[0]['observation']['position_m'])
    end_x, _ = point(samples[-1]['observation']['position_m'])

    def scene(index, poster=False):
        sample = samples[index]
        current_time = times[index]
        observation = sample['observation']
        x, y = point(observation['position_m'])
        trace = pairs(s['observation']['position_m'] for s in samples[:index + 1])
        markers = []
        for state in handoffs:
            if state['sim_time_s'] <= current_time:
                mx, my = point(state['position_m'])
                markers.append(f'<circle cx="{mx:.2f}" cy="{my:.2f}" r="7" '
                               'fill="#101a21" stroke="#ffbe78" stroke-width="2.5"/>')
        angle = math.degrees(observation['attitude_rad'])
        throttle = sample['held_command']['throttle_frac']
        plume = ''
        if throttle > 0 and index < len(samples) - 1:
            length = 9 + 18 * throttle
            plume = f'<path d="M-3 7L0 {length:.2f}L3 7" fill="#ffbe78"/>'
        status = 'Target landing' if index == len(samples) - 1 else 'In flight'
        clock = '900 m · 46.4 s' if poster else f'{current_time:04.1f} s / 46.4 s · 6× playback'
        replan_label = 'replan' if len(markers) == 1 else 'replans'
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="576" viewBox="0 0 1024 576" role="img" aria-labelledby="title desc">
<title id="title">Powered Descent Lab: recorded plateau flight</title>
<desc id="desc">Retained policy-3 flight positions across a 900-metre transfer. Three replans clear a 315-metre plateau before a verified target landing. Both plot axes use the same scale. The vehicle marker is schematic.</desc>
<rect width="1024" height="576" fill="#101a21"/>
<g font-family="sans-serif" fill="#b4c7d0">
<text x="72" y="65" font-size="15" letter-spacing="2">RECORDED FLIGHT</text>
<text x="72" y="102" font-size="29" fill="#e8f1f4">Terrain-aware landing</text>
<text x="950" y="66" text-anchor="end" font-size="16">{clock}</text>
<g stroke="#24343e" stroke-width="1">{grid}</g>
<polygon points="72,480 {terrain} 950,530 72,530" fill="#293a43"/>
<polyline points="{terrain}" fill="none" stroke="#7f929b" stroke-width="2"/>
<polyline points="{trace}" fill="none" stroke="#81dfca" stroke-width="3.5" stroke-linejoin="round"/>
{''.join(markers)}
<path d="M{launch_x - 14:.2f} 481h28M{end_x - 14:.2f} 481h28" stroke="#81dfca" stroke-width="3"/>
<g transform="translate({x:.2f} {y:.2f}) rotate({angle:.2f})">
{plume}<path d="M0-15L5-7V6H-5V-7Z" fill="#e8f1f4" stroke="#101a21" stroke-width="1.5"/>
<path d="M-5 2L-9 9H-3M5 2L9 9H3" fill="#b4c7d0"/>
</g>
<text x="{launch_x:.2f}" y="511" text-anchor="middle" font-size="14">Launch</text>
<text x="{end_x:.2f}" y="511" text-anchor="middle" font-size="14">Touchdown</text>
<circle cx="79" cy="553" r="4" fill="#81dfca"/><text x="93" y="558" font-size="14">{status}</text>
<circle cx="256" cy="553" r="4" fill="none" stroke="#ffbe78" stroke-width="2"/><text x="270" y="558" font-size="14">{len(markers)} {replan_label}</text>
<text x="950" y="558" text-anchor="end" font-size="13">v2_plateau_wide · policy 3</text>
</g></svg>
'''

    output.mkdir(parents=True, exist_ok=True)
    (output / 'powered-descent.svg').write_text(scene(len(samples) - 1, poster=True))
    fps, speed, start_hold, end_hold = 30, 6, 0.6, 1.5
    duration = start_hold + times[-1] / speed + end_hold
    with tempfile.TemporaryDirectory(prefix='devlog-flight-') as scratch:
        scratch = Path(scratch)
        for frame in range(math.ceil(duration * fps)):
            time = max(0, min(times[-1], (frame / fps - start_hold) * speed))
            index = max(0, bisect.bisect_right(times, time) - 1)
            (scratch / f'frame-{frame:04d}.svg').write_text(scene(index))
        subprocess.run([
            'ffmpeg', '-v', 'error', '-y', '-framerate', str(fps),
            '-i', str(scratch / 'frame-%04d.svg'), '-an', '-c:v', 'libx264',
            '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
            str(output / 'powered-descent.mp4'),
        ], check=True)
    print(f'Rendered {len(samples)} retained samples, {len(handoffs)} replans; {duration:.1f}s clip.')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    render(Path(sys.argv[1]), Path(sys.argv[2]))
