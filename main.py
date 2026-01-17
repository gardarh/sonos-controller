import argparse

import soco


def list_speakers(args):
    speakers = soco.discover()
    if not speakers:
        print("No speakers found")
        return
    for speaker in speakers:
        print(f"{speaker.player_name} - {speaker.ip_address}")


def get_speaker_by_name(name):
    speakers = soco.discover()
    if not speakers:
        return None
    for speaker in speakers:
        if speaker.player_name == name:
            return speaker
    return None


def speaker_play(args):
    speaker = get_speaker_by_name(args.speaker_name)
    if not speaker:
        print(f"Speaker not found: {args.speaker_name}")
        return
    speaker.play()
    print(f"Playing on speaker: {args.speaker_name}")


def speaker_pause(args):
    speaker = get_speaker_by_name(args.speaker_name)
    if not speaker:
        print(f"Speaker not found: {args.speaker_name}")
        return
    speaker.pause()
    print(f"Paused speaker: {args.speaker_name}")


def speaker_set_to_line_in(args):
    speaker = get_speaker_by_name(args.speaker_name)
    if not speaker:
        print(f"Speaker not found: {args.speaker_name}")
        return
    speaker.switch_to_line_in()
    print(f"Switched {args.speaker_name} to line-in")


def speaker_set_volume(args):
    speaker = get_speaker_by_name(args.speaker_name)
    if not speaker:
        print(f"Speaker not found: {args.speaker_name}")
        return
    speaker.volume = args.volume
    print(f"Set {args.speaker_name} volume to {args.volume}")


def main():
    parser = argparse.ArgumentParser(description="Sonos Controller")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # list-speakers action
    list_speakers_parser = subparsers.add_parser(
        "list-speakers", help="List all available speakers"
    )
    list_speakers_parser.set_defaults(func=list_speakers)

    # speaker action
    speaker_parser = subparsers.add_parser(
        "speaker", help="Control a specific speaker"
    )
    speaker_parser.add_argument(
        "--speaker-name", required=True, help="Name of the speaker to control"
    )

    # speaker sub-actions
    speaker_subparsers = speaker_parser.add_subparsers(
        dest="speaker_action", required=True
    )

    play_parser = speaker_subparsers.add_parser("play", help="Play on the speaker")
    play_parser.set_defaults(func=speaker_play)

    pause_parser = speaker_subparsers.add_parser("pause", help="Pause the speaker")
    pause_parser.set_defaults(func=speaker_pause)

    set_to_line_in_parser = speaker_subparsers.add_parser(
        "set-to-line-in", help="Switch speaker to its line-in input"
    )
    set_to_line_in_parser.set_defaults(func=speaker_set_to_line_in)

    set_volume_parser = speaker_subparsers.add_parser(
        "set-volume", help="Set speaker volume"
    )
    set_volume_parser.add_argument(
        "volume", type=int, choices=range(0, 101), metavar="0-100",
        help="Volume level (0-100)"
    )
    set_volume_parser.set_defaults(func=speaker_set_volume)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
