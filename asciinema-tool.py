#! /usr/bin/python

import os
import sys
import argparse
from csv import reader

fuzzy = 'soft'
selection_type = 'time'

parser = argparse.ArgumentParser(
        description = '''
        This program can manipulate asciinema cast files. The modified cast file will be output to stdout.
        '''
        , epilog = '''
        '''
        )

actions = parser.add_argument_group('Actions')
exclusive = actions.add_mutually_exclusive_group()

exclusive.add_argument( "--print"
        , dest = "print_deltas"
        , action = "store_true" 
        , help = "Print the frame numbers and deltas between frames"
        )
exclusive.add_argument( "--change"
        , dest = "change_deltas"
        , nargs = 3
        , type = float
        , metavar = ('delta', 'start', 'stop')
        , help="Change the deltas of frames between start and stop"
        )
exclusive.add_argument( "--cut" 
        , dest = "cut_frames"
        , nargs = 2
        , type = float
        , metavar = ('start', 'stop')
        , help = "Remove the frames between start and stop"
        )
exclusive.add_argument( "--add-delay" 
        , dest = "add_delay"
        , nargs = 2
        , type = float
        , metavar = ('delay', 'point')
        , help = "Add a delay at point"
        )

parser.add_argument( "--nofuzzy"
        , dest = "fuzziness"
        , default = "soft"
        , const = "hard"
        , action = "store_const"
        , help = "If set, all frames between the start and stop points will be set to delta. Otherwise, only the matching frames between the start and stop points that exceed the delta will be set to delta"
        )
parser.add_argument( "--frame"
        , dest = "selection_type"
        , default = "time"
        , const = "frame"
        , action = "store_const"
        , help = "If set, use frame numbers instead of time when specifying start and stop"
        )
parser.add_argument( "cast"
        , type = argparse.FileType('r') 
        , help = "The cast file to process."
        )


cli = parser.parse_args()


## Functions
#

# def test(castdata):
#     for line in castdata:
#         if line.startswith('{'):
#             sys.stdout.write( line )
#         else:
# 
#             sep1 = line.find(',')
#             sep2 = line.find(',', sep1+1)
# 
#             sbloc = line.find('[')
#             ebloc = line.rfind(']')
# 
#             ts = float( line[sbloc+1:sep1])
#             parameter = line[sep1+1:sep2]
#             data = line[sep2+1:ebloc]
# 
#             sys.stdout.write ("{0:f}---{1:s}---{2:s}\n".format(ts, parameter, data) )



def frame_parse(frame):
    sep1 = frame.find(',')
    sep2 = frame.find(',', sep1+1)

    sbloc = frame.find('[')
    ebloc = frame.rfind(']')

    ts = float( frame[sbloc+1:sep1])
    parameter = frame[sep1+1:sep2]
    data = frame[sep2+1:ebloc]

    return ts, parameter, data


def test(castdata):
    for line in castdata:
        if line.startswith('{'):
            sys.stdout.write( line )
        else:
            ts, parameter, data = frame_parse(line)
            sys.stdout.write ("{0:f}---{1:s}---{2:s}\n".format(ts, parameter, data) )



def deltas_print(castdata):
    frame = 0

    sys.stdout.write ( "{0:>8s} --- {1:>12s} --- {2:<12s} --- {3:<s}\n".format('Frame', 'Delta', 'Time Stamp', 'String') )

    for line in castdata:
        if line.startswith('{'):
            sys.stdout.write( line )
        else:
            ts, parameter, data = frame_parse(line)

            try:
                ts_prev
            except NameError:
                ts_prev = ts

            delta = ts - ts_prev

            sys.stdout.write ( "{0:>8d} --- {1:>12f} --- {2:<12f} --- {3:<s}\n".format(frame, delta, ts, data) )

            ts_prev = ts

        frame += 1





def deltas_change(castdata, dtype, fuzzy, delta, start, stop):
    # dtype is either frame or time. This is how the selections are made.
    # fuzzy is either hard or soft. Determines id timestamps are hard set 
    #     to reflect delta or only changes if the deltas between the
    #     output exceeds the delta.

    frame = 0

    delta = float(delta)

    for line in castdata:
        if line.startswith('{'):
            sys.stdout.write( line )
        elif line.startswith('['):
            ts_file, parameter, data = frame_parse(line)

            try:
                ts_file_prev
            except NameError:
                ts_file_prev = ts_file

            ts_delta = ts_file - ts_file_prev

            if dtype == "time" and ts_file >= start and ts_file <= stop:
                if fuzzy == "hard": ts_delta = delta
                elif fuzzy == "soft" and ts_delta > delta: ts_delta = delta


            elif dtype == "frame" and frame >= start and frame <= stop:
                if fuzzy == "hard": ts_delta = delta
                elif fuzzy == "soft" and ts_delta > delta: ts_delta = delta


            try:
                ts_new_prev
            except NameError:
                ts_new = ts_file
            else:
                ts_new = ts_new_prev + ts_delta


            sys.stdout.write ( "[{0:f}, {1:s}, {2:s}]\n".format(ts_new, parameter, data) )

            ts_file_prev = ts_file
            ts_new_prev = ts_new

        frame += 1



def add_delay(castdata, dtype, delay, point):
    # dtype is either frame or time. This is how the selections are made.
    # delay is the delay to add in seconds.
    # point is either the time or frame number the delay will be inserted before.

    frame = 0
    delay_temp = 0

    for line in castdata:
        if line.startswith('{'):
            sys.stdout.write( line )
        elif line.startswith('['):
            ts_file, parameter, data = frame_parse(line)

            try:
                inserted
            except NameError:
                if dtype == "time" and ts_file >= point:
                    delay_temp = delay
#                    sys.stdout.write ( "[{0:>f}, \"o\", \"\"]\n".format(delay) )
                    
                    inserted = "true"
                    
                if dtype == "frame" and frame >= point:
                    delay_temp = delay
#                    sys.stdout.write ( "[{0:>f}, \"o\", \"\"]\n".format(delay) )
                    
                    inserted = "true"
                    

            ts_new = ts_file + delay_temp

            sys.stdout.write ( "[{0:f}, {1:s}, {2:s}]\n".format(ts_new, parameter, data) )

        frame += 1


def frames_cut(castdata, dtype, start, stop):
    # dtype is either frame or time. This is how the selections are made.
    # start and stop are the frames or times to cut, 
    #     specifying 0 for either cuts from the beginning or to the end

    frame = 0
    cut_total = 0

    for line in castdata:
        if line.startswith('{'):
            sys.stdout.write( line )
        elif line.startswith('['):
            ts_file, parameter, data = frame_parse(line)


            if ( dtype == "time" and ts_file < start ) or ( dtype == "frame" and frame < start ):
                ts_new = ts_file
                sys.stdout.write ( "[{0:f}, {1:s}, {2:s}]\n".format(ts_new, parameter, data) )
            else:
                try:
                    ts_start
                except NameError:
                    ts_start = ts_file

            if ( dtype == "time" and ts_file > stop ) or ( dtype == "frame" and frame > stop ):
                try:
                    ts_delta
                except NameError:
                    ts_delta = ts_file - ts_start

                ts_new = ts_file - ts_delta
                sys.stdout.write ( "[{0:f}, {1:s}, {2:s}]\n".format(ts_new, parameter, data) )

        frame += 1



def main():
#    test(cli.cast)

    if cli.add_delay:
        add_delay(cli.cast, cli.selection_type, cli.add_delay[0], cli.add_delay[1])

    if cli.change_deltas:
        deltas_change(cli.cast, cli.selection_type, cli.fuzziness, cli.change_deltas[0], cli.change_deltas[1], cli.change_deltas[2])

    if cli.cut_frames:
        frames_cut(cli.cast, cli.selection_type, cli.cut_frames[0], cli.cut_frames[1])

    if cli.print_deltas:
        deltas_print(cli.cast)




## Main
#

if __name__ == "__main__":
    main()

