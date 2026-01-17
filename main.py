import argparse

import sonos


def list_speakers(args: argparse.Namespace) -> None:
    speakers = sonos.discover_speakers()
    if not speakers:
        print("No speakers found")
        return
    for speaker in speakers:
        print(f"{speaker['name']} - {speaker['ip']}")


def speaker_play(args: argparse.Namespace) -> None:
    if sonos.play(args.speaker_name):
        print(f"Playing on speaker: {args.speaker_name}")
    else:
        print(f"Speaker not found: {args.speaker_name}")


def speaker_pause(args: argparse.Namespace) -> None:
    if sonos.pause(args.speaker_name):
        print(f"Paused speaker: {args.speaker_name}")
    else:
        print(f"Speaker not found: {args.speaker_name}")


def speaker_set_source(args: argparse.Namespace) -> None:
    success, error = sonos.set_source(args.speaker_name, args.source)
    if success:
        print(f"Set {args.speaker_name} source to {args.source}")
    else:
        print(error)


def speaker_set_volume(args: argparse.Namespace) -> None:
    if sonos.set_volume(args.speaker_name, args.volume):
        print(f"Set {args.speaker_name} volume to {args.volume}")
    else:
        print(f"Speaker not found: {args.speaker_name}")


def speaker_play_uri(args: argparse.Namespace) -> None:
    title = getattr(args, "title", "") or ""
    if sonos.play_uri(args.speaker_name, args.uri, title):
        print(f"Playing {title or args.uri} on {args.speaker_name}")
    else:
        print(f"Speaker not found: {args.speaker_name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sonos Controller")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # list-speakers action
    list_speakers_parser = subparsers.add_parser(
        "list-speakers", help="List all available speakers"
    )
    list_speakers_parser.set_defaults(func=list_speakers)

    # speaker action
    speaker_parser = subparsers.add_parser("speaker", help="Control a specific speaker")
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

    set_source_parser = speaker_subparsers.add_parser(
        "set-source", help="Set speaker source"
    )
    set_source_parser.add_argument(
        "source", choices=["line-in", "music"], help="Source to set"
    )
    set_source_parser.set_defaults(func=speaker_set_source)

    set_volume_parser = speaker_subparsers.add_parser(
        "set-volume", help="Set speaker volume"
    )
    set_volume_parser.add_argument(
        "volume",
        type=int,
        choices=range(0, 101),
        metavar="0-100",
        help="Volume level (0-100)",
    )
    set_volume_parser.set_defaults(func=speaker_set_volume)

    play_uri_parser = speaker_subparsers.add_parser("play-uri", help="Play a URI")
    play_uri_parser.add_argument("uri", help="URI to play")
    play_uri_parser.add_argument("--title", help="Title for the stream", default="")
    play_uri_parser.set_defaults(func=speaker_play_uri)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
