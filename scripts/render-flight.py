#!/usr/bin/env python3
"""Render the retained random-462 flight without running a simulation.

Usage: python3 scripts/render-flight.py RUN_DIRECTORY assets/projects
Requires ffmpeg with librsvg support. RUN_DIRECTORY is runs/random-462 in
capture-terrain-correction-20261008-v1. Its receipt must authenticate the input
scenario, feedback, attempt and command replay. Frames select recorded samples
without interpolation; the enlarged vehicle is a presentation marker.
"""

import bisect
from hashlib import sha256
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile


SCENARIO_SHA256 = '603490ca2a7832c06dd6c383310898ad39cf770cfe1e444a10104c2dc28b875b'
FEEDBACK_SHA256 = '6527a6d0fa94dcd0b5f40d902049df1559c0b25a227f36fabe73bb25ab9dfa78'
FPS, SPEED, START_HOLD, END_HOLD = 30, 6, 0.6, 1.5
THRUST_COLOR, PAD_COLOR, TRAIL_COLOR = '#ff5b54', '#7ce39b', '#70cddd'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_flight(run):
    receipt = json.loads((run.parent.parent / 'receipt.json').read_text())['files']
    inputs = {}
    for name in ('scenario.json', 'feedback.json', 'attempt.json', 'command-replay.json'):
        data = (run / name).read_bytes()
        require(sha256(data).hexdigest() == receipt[f'runs/{run.name}/{name}'],
                f'Receipt mismatch: {name}')
        inputs[name] = json.loads(data)
    scenario, flight = inputs['scenario.json'], inputs['feedback.json']
    require(run.name == 'random-462', 'Expected the selected procedural-terrain case')
    require(sha256((run / 'scenario.json').read_bytes()).hexdigest() == SCENARIO_SHA256,
            'Expected the frozen mountains scenario')
    require(sha256((run / 'feedback.json').read_bytes()).hexdigest() == FEEDBACK_SHA256,
            'Expected the retained terrain-correction flight')
    require(flight['scenario_sha256'] == SCENARIO_SHA256, 'Flight/scenario identity mismatch')
    require(flight['candidate_id'] == 'ballistic_feedback_v3_terrain_correction',
            'Expected the terrain-correction candidate')
    require(scenario['metadata']['recipe'] == 'mountains_8x' and scenario['seed'] == 784925805,
            'Expected the procedural terrain recipe and seed')
    final = flight['final_state']
    require(flight['stop'] == 'physical_terminal'
            and final['physical_outcome'] == 'landed_on_target'
            and final['mission_outcome'] == 'success', 'Flight did not land successfully')
    require(flight['integrity_passed'] and flight['source_replay_passed']
            and flight['decisions_reproduced'], 'Flight verification incomplete')
    replay = inputs['command-replay.json']
    require(replay['passed'] and replay['final_state'] == final, 'Command replay mismatch')
    samples = flight['ordinary_flight']['samples']
    times = [s['sim_time_s'] for s in samples]
    require(times[0] == 0 and all(a < b for a, b in zip(times, times[1:])),
            'Sample times must start at zero and increase')
    require(times[-1] == final['sim_time_s']
            and samples[-1]['observation']['position_m'] == final['position_m'],
            'Samples must include the final landing state')
    return scenario, flight


def render(run, output):
    scenario, flight = load_flight(run)
    samples = flight['ordinary_flight']['samples']
    times = [s['sim_time_s'] for s in samples]
    positions = [s['observation']['position_m'] for s in samples]
    terrain = scenario['world']['terrain']['points_m']
    points = terrain + positions
    require(all(math.isfinite(p[axis]) for p in points for axis in ('x', 'y')),
            'Geometry must be finite')
    xmin, xmax = min(p['x'] for p in points), max(p['x'] for p in points)
    ymin, ymax = min(p['y'] for p in points), max(p['y'] for p in points)
    scale = min(916 / (xmax - xmin), 400 / (ymax - ymin))
    midx, midy = (xmin + xmax) / 2, (ymin + ymax) / 2

    def point(position):
        return 512 + (position['x'] - midx) * scale, 304 - (position['y'] - midy) * scale

    def pairs(positions):
        return ' '.join(f'{x:.2f},{y:.2f}' for x, y in map(point, positions))

    pads = []
    for pad in scenario['world']['landing_pads']:
        x, y = point({'x': pad['center_x_m'], 'y': pad['surface_y_m']})
        width = pad['width_m'] * scale
        pads.append(f'<path d="M{x-width/2:.2f} {y:.2f}h{width:.2f}" '
                    f'stroke="{PAD_COLOR}" stroke-width="4"/>')
    base = scenario['vehicle']['geometry']['touchdown_base_offset_m'] * scale

    def scene(index, poster=False):
        sample = samples[index]
        observation = sample['observation']
        x, y = point(observation['position_m'])
        # PD Lab angles tilt toward +x, which is positive SVG rotation.
        angle = math.degrees(observation['attitude_rad'])
        throttle = sample['held_command']['throttle_frac']
        plume = ''
        if throttle > 0 and index < len(samples) - 1:
            length = (7 + 19 * throttle) * (1 + 0.1 * math.sin(times[index] * 37))
            plume = (f'<path d="M-3 {base+3:.2f}L0 {base+length:.2f}L3 {base+3:.2f}" '
                     f'stroke="{THRUST_COLOR}" stroke-width="2.6"/>')
        trace = pairs(positions if poster else positions[:index + 1])
        clock = f'{times[-1]:.1f} s · {SPEED}× playback' if poster else f'{times[index]:04.1f} / {times[-1]:.1f} s · {SPEED}×'
        status = 'TARGET LANDING' if index == len(samples) - 1 else 'LIFTOFF' if times[index] < 4 else 'IN FLIGHT'
        if poster:
            status = 'RECORDED FLIGHT · VERIFIED LANDING'
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="576" viewBox="0 0 1024 576" role="img" aria-labelledby="title desc">
<title id="title">Powered Descent Lab: procedural mountain flight</title>
<desc id="desc">Custom vector telemetry visualization of random-462 from the October 8, 2026 terrain-correction sweep. A verified 1,200-metre transfer over procedural mountains. Original terrain, recorded positions and attitude, equal-scale axes, and an enlarged triangular vehicle anchored at its recorded touchdown base. Pylander-inspired white outlines on black with red thrust, green landing pads and a cyan flight trail; not a native application recording.</desc>
<rect width="1024" height="576" fill="black"/>
<g font-family="monospace" fill="white">
<text x="40" y="49" font-size="24">Procedural terrain</text>
<text x="984" y="48" text-anchor="end" font-size="15" opacity="0.7">{clock}</text>
<polyline points="{pairs(terrain)}" fill="none" stroke="white" stroke-width="2.2" stroke-linejoin="round"/>
{''.join(pads)}
<polyline points="{trace}" fill="none" stroke="{TRAIL_COLOR}" stroke-opacity="0.6" stroke-width="1.5" stroke-dasharray="2 6" stroke-linecap="round"/>
<g transform="translate({x:.2f} {y:.2f}) rotate({angle:.2f})" fill="none" stroke="white" stroke-width="2.2" stroke-linejoin="round">
{plume}<path d="M0 {base-24:.2f}L-9 {base:.2f}H9Z" fill="black"/>
</g>
<text x="40" y="549" font-size="12" letter-spacing="1.3" opacity="0.55">TELEMETRY VISUALIZATION</text>
<text x="984" y="549" text-anchor="end" font-size="12" letter-spacing="1" opacity="0.7">{status}</text>
</g></svg>
'''

    output.mkdir(parents=True, exist_ok=True)
    poster_index = min(range(len(samples)), key=lambda i: abs(positions[i]['x'] - 760))
    (output / 'powered-descent-terrain.svg').write_text(scene(poster_index, poster=True))
    duration = START_HOLD + times[-1] / SPEED + END_HOLD
    with tempfile.TemporaryDirectory(prefix='devlog-flight-') as scratch:
        scratch = Path(scratch)
        for frame in range(math.ceil(duration * FPS)):
            time = max(0, min(times[-1], (frame / FPS - START_HOLD) * SPEED))
            index = max(0, bisect.bisect_right(times, time) - 1)
            (scratch / f'frame-{frame:04d}.svg').write_text(scene(index))
        subprocess.run([
            'ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS),
            '-i', str(scratch / 'frame-%04d.svg'), '-an', '-c:v', 'libx264',
            '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
            str(output / 'powered-descent-terrain.mp4'),
        ], check=True)
    print(f'Rendered {len(samples)} retained samples and {len(terrain)} terrain vertices; '
          f'{duration:.1f}s clip, {times[-1]:.1f}s verified landing.')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    render(Path(sys.argv[1]), Path(sys.argv[2]))
