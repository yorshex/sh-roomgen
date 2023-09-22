#!/usr/bin/env python3

'''
Copyright (c) 2023 Maxim "yorshex" Ershov

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.
'''

import argparse
import math

def main():
    parser = argparse.ArgumentParser(description='Generate a generic Smash Hit room')

    parser.add_argument('-o', '--output-file', dest='output_file', type=argparse.FileType('w', encoding='utf-8'), required=True,
                        metavar='output-file',
                        help='file to which the room will be written; required')

    parser.add_argument('-s', '--segment', dest='segments', action='append', required=True,
                        metavar='segment',
                        help='add a segment to appear; you can specify multiple segments; at least one segment is required')

    parser.add_argument('--start', dest='start_segment',
                        metavar='start-segment',
                        help='set start segment')

    parser.add_argument('--end', dest='end_segment',
                        metavar='end-segment',
                        help='set end segment')

    parser.add_argument('-l', '--length', dest='length', type=float, default=100.0,
                        metavar='length',
                        help='set length; 100 by default')

    parser.add_argument('--training-length', dest='length_training', type=float,
                        metavar='length',
                        help='set length in training mode')

    parser.add_argument('--mayhem-length',dest='length_mayhem', type=float,
                        metavar='length',
                        help='set length in mayhem mode')

    parser.add_argument('-r', '--rotation', nargs=2, dest='rotation', type=float,
                        metavar=('amount', 'range'),
                        help="set rotation; ragne is set in degrees; setting range to 0 results in CW/CCW rotation")

    parser.add_argument('-g', '--gravity', dest='gravity', type=float,
                        metavar='gravity',
                        help="set gravity")

    parser.add_argument('-f', '--fog', nargs=6, dest='fog', type=float, default=[1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                        metavar=('r_upper', 'g_upper', 'b_upper', 'r_lower', 'g_lower', 'b_lower'),
                        help="set fog color; white-black by default")

    parser.add_argument('-p', '--particles', dest='particles',
                        metavar='particles',
                        help="set particle effects; possible values in OG Smash Hit: 'starfield', 'lowrising', 'lowrising2', 'sidesrising', 'fallinglite', 'bubbles', 'dustyfalling'")

    parser.add_argument('-m', '--music', dest='music',
                        metavar='music',
                        help='set music')

    parser.add_argument('-E', '--echo', nargs=4, dest='echo', type=float,
                        metavar=('volume', 'dalay', 'fallback_volume', 'fallback_lowpass'),
                        help="set echo effect")

    parser.add_argument('-R', '--reverb', nargs=3, dest='reverb', type=float,
                        metavar=('volume', 'length', 'lowpass'),
                        help="set reverberation effect")

    parser.add_argument('-L', '--lowpass', dest='lowpass', type=float,
                        metavar='strength',
                        help="set low pass effect")

    params = parser.parse_args()

    f = params.output_file
    f.write('''-- generated using roomgen
-- https://github.com/yorshex/sh-roomgen
''')
    f.write('''
function init()
\tpStart = mgGetBool("start", false)
\tpEnd = mgGetBool("end", false)
''')
    if params.rotation is not None:
        params.rotation[1] = math.radians(params.rotation[1])
        f.write(f'\n\tmgRotation({str(params.rotation)[1:-1]})')
    if params.gravity is not None:
        f.write(f'\n\tmgGravity({params.gravity})')
    f.write(f'\n\tmgFogColor({str(params.fog)[1:-1]})')
    if params.particles is not None:
        f.write(f'\n\tmgParticles("{params.particles}")')
    if params.music is not None:
        f.write(f'\n\tmgMusic("{params.music}")')
    if params.echo is not None:
        f.write(f'\n\tmgEcho({str(params.echo)[1:-1]})')
    if params.reverb is not None:
        f.write(f'\n\tmgReverb({str(params.reverb)[1:-1]})')
    if params.lowpass is not None:
        f.write(f'\n\tmgLowPass({params.lowpass})')
    f.write('\n')
    f.write(f'''
\tlocal l = 0

\tlocal L = {params.length}''')
    if params.length_training is not None:
        f.write(f'\n\tif mgGet("player.mode")=="0" then L = {params.length_training}')
    if params.length_mayhem is not None:
        f.write(f'\n\tif mgGet("player.mode")=="2" then L = {params.length_mayhem}')
    f.write('\n')
    for segment in params.segments:
        f.write(f'\n\tconfSegment("{segment}", 1)')
    f.write('\n')
    if params.start_segment is not None:
        f.write(f'''
\tif pStart then
\t\tl = l + mgSegment("{params.start_segment}", -l)
\tend''')
    f.write(f'''
\twhile l < L do
\t\ts = nextSegment()
\t\tl = l + mgSegment(s, -l)
\tend''')
    if params.end_segment is not None:
        f.write(f'''
\tif pEnd then
\t\tl = l + mgSegment("{params.end_segment}", -l)
\tend''')
    f.write('\n')
    f.write(f'''
\tmgLength(l)
end

function tick()
end''')

if __name__ == '__main__':
    main()
else:
    raise Exception("Don't use " + __name__ + " as a module")
